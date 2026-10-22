#!/usr/bin/env python3
"""Speaker Tuner - GTK4/libadwaita front end for a PipeWire filter-chain.

Adds a virtual output with low cut, 10-band EQ, boost + limiter, overdrive,
stereo width, crosstalk-cancellation 3D and a virtual crossover in front of
any PipeWire sink.

Every setting is a control on a fixed filter graph, so changes are pushed live
with `pw-cli set-param` (no audio restart). The config file is rewritten on each
change so the settings survive reboots.
"""
import json
import os
import subprocess
import sys

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, GLib, Gtk  # noqa: E402

APP_ID = "io.github.pjamessteven.SpeakerTuner"
VERSION = "0.1.0"
NODE_NAME = "effect_input.speaker_tuner"
OUT_NODE_NAME = "effect_output.speaker_tuner"
CONF_PATH = os.path.expanduser("~/.config/pipewire/pipewire.conf.d/speaker-tuner.conf")
SETTINGS_PATH = os.path.expanduser("~/.config/speaker-tuner/settings.json")
LIMITER_URI = "urn:zamaudio:ZaMaximX2"
GRAPH_VERSION = 5  # bump when the node layout changes (needs an audio restart)

EQ_FREQS = [31, 62, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
EQ_Q = 1.41  # one-octave bands
LP_OFF, HP_OFF = 23000.0, 5.0  # crossover filters parked outside the audible range

PRESETS = {
    "Flat": [0] * 10,
    "Loudness": [0, 0, 3, 3, 1, 0, 0, 1, 2, 2],
    "Bass": [0, 0, 5, 4, 2, 0, 0, 0, 0, 0],
    "Vocal": [0, 0, -2, -1, 1, 2, 3, 2, 0, 0],
    "Treble": [0, 0, 0, 0, 0, 0, 1, 2, 3, 4],
}

DEFAULTS = {
    "target_sink": "",
    "boost_db": 0.0,
    "ceiling_db": -1.0,
    "release_ms": 25.0,
    "protect_hz": 20.0,  # 20 = off
    "eq": [0.0] * 10,
    "crossover": False,
    "xover_hz": 250.0,
    "sub_side": "left",
    "sub_db": 0.0,
    "top_db": 0.0,
    "drive_db": 0.0,
    "width_pct": 100.0,
    "xtc_pct": 0.0,
    "xtc_us": 90.0,
}


# ---------------------------------------------------------------- graph model

def node_specs():
    """(name, type, label/plugin) for every node in the fixed graph."""
    specs = []
    for x in "lr":
        specs += [
            (f"copy_{x}", "builtin", "copy"),
            (f"mix_{x}", "builtin", "mixer"),
            (f"hp1_{x}", "builtin", "bq_highpass"),
            (f"hp2_{x}", "builtin", "bq_highpass"),
        ]
        specs += [(f"eq{i}_{x}", "builtin", "bq_peaking") for i in range(len(EQ_FREQS))]
        specs += [
            (f"lp1_{x}", "builtin", "bq_lowpass"),
            (f"lp2_{x}", "builtin", "bq_lowpass"),
            (f"xh1_{x}", "builtin", "bq_highpass"),
            (f"xh2_{x}", "builtin", "bq_highpass"),
            (f"trim_{x}", "builtin", "linear"),
            (f"bpa_{x}", "builtin", "bq_highpass"),
            (f"bpb_{x}", "builtin", "bq_lowpass"),
            (f"dly_{x}", "builtin", "delay"),
            (f"dly2_{x}", "builtin", "delay"),
            (f"xtc_{x}", "builtin", "mixer"),
        ]
    specs.append(("lim", "lv2", LIMITER_URI))
    specs += [("drive_l", "builtin", "linear"), ("drive_r", "builtin", "linear")]
    return specs


def chain(x):
    return ([f"mix_{x}", f"hp1_{x}", f"hp2_{x}"]
            + [f"eq{i}_{x}" for i in range(len(EQ_FREQS))]
            + [f"lp1_{x}", f"lp2_{x}", f"xh1_{x}", f"xh2_{x}", f"trim_{x}"])


def controls(s):
    """Map of 'node:Control' -> value for the given settings."""
    c = {}
    sub = "l" if s["sub_side"] == "left" else "r"
    for x in "lr":
        if s["crossover"]:
            c[f"mix_{x}:Gain 1"], c[f"mix_{x}:Gain 2"] = 0.5, 0.5
        else:  # mid/side width: own = (1+w)/2, other = (1-w)/2
            w = s["width_pct"] / 100
            own, other = (1 + w) / 2, (1 - w) / 2
            c[f"mix_{x}:Gain 1"], c[f"mix_{x}:Gain 2"] = (own, other) if x == "l" else (other, own)
        low_cut = float(s["protect_hz"]) if s["protect_hz"] > 20 else HP_OFF
        for n, q in (("hp1", 0.5412), ("hp2", 1.3066)):  # 4th-order Butterworth
            c[f"{n}_{x}:Freq"], c[f"{n}_{x}:Q"] = low_cut, q
        for i, f in enumerate(EQ_FREQS):
            c[f"eq{i}_{x}:Freq"], c[f"eq{i}_{x}:Q"] = float(f), EQ_Q
            c[f"eq{i}_{x}:Gain"] = float(s["eq"][i])
        is_sub = s["crossover"] and x == sub
        is_top = s["crossover"] and x != sub
        for n in ("lp1", "lp2"):  # Linkwitz-Riley 4th order = 2x Butterworth Q 0.7071
            c[f"{n}_{x}:Freq"], c[f"{n}_{x}:Q"] = (float(s["xover_hz"]) if is_sub else LP_OFF), 0.7071
        for n in ("xh1", "xh2"):
            c[f"{n}_{x}:Freq"], c[f"{n}_{x}:Q"] = (float(s["xover_hz"]) if is_top else HP_OFF), 0.7071
        trim_db = s["sub_db"] if is_sub else s["top_db"] if is_top else 0.0
        c[f"trim_{x}:Mult"], c[f"trim_{x}:Add"] = 10 ** (trim_db / 20), 0.0
        # 3D: crosstalk cancellation (RACE-style, unrolled to 2 terms since the graph can't loop).
        # out = own - g*D(other) + g^2*D2(own), cancellation path band-limited to 250 Hz-5 kHz.
        g = 0.0 if s["crossover"] else 0.71 * s["xtc_pct"] / 100  # 100% = -3 dB
        d = s["xtc_us"] / 1e6
        c[f"bpa_{x}:Freq"], c[f"bpa_{x}:Q"] = 250.0, 0.7071
        c[f"bpb_{x}:Freq"], c[f"bpb_{x}:Q"] = 5000.0, 0.7071
        c[f"dly_{x}:Delay (s)"], c[f"dly2_{x}:Delay (s)"] = d, 2 * d
        c[f"xtc_{x}:Gain 1"], c[f"xtc_{x}:Gain 2"], c[f"xtc_{x}:Gain 3"] = 1.0, -g, g * g
    c["lim:gain"] = float(s["boost_db"])
    c["lim:thresh"] = float(s["ceiling_db"])
    c["lim:rel"] = float(s["release_ms"])
    for x in "lr":  # post-limiter gain: anything above 0 dBFS hard-clips at the DAC
        c[f"drive_{x}:Mult"], c[f"drive_{x}:Add"] = 10 ** (s["drive_db"] / 20), 0.0
    return c


def conf_text(s):
    c = controls(s)
    lines = []
    for name, typ, what in node_specs():
        ctl = " ".join(f'"{k.split(":", 1)[1]}" = {v:.6g}' for k, v in c.items() if k.split(":", 1)[0] == name)
        key = "plugin" if typ == "lv2" else "label"
        ctl_part = f" control = {{ {ctl} }}" if ctl else ""
        cfg = ' config = { "max-delay" = 0.01 }' if what == "delay" else ""
        lines.append(f'                {{ type = {typ} name = {name} {key} = "{what}"{cfg}{ctl_part} }}')
    links = []
    for src in "lr":
        for dst in "lr":
            links.append(f'{{ output = "copy_{src}:Out" input = "mix_{dst}:In {1 if src == "l" else 2}" }}')
    for x in "lr":
        ch = chain(x)
        links += [f'{{ output = "{a}:Out" input = "{b}:In" }}' for a, b in zip(ch, ch[1:])]
    for x, o in (("l", "r"), ("r", "l")):
        links += [
            f'{{ output = "trim_{x}:Out" input = "xtc_{x}:In 1" }}',
            f'{{ output = "trim_{x}:Out" input = "bpa_{x}:In" }}',
            f'{{ output = "bpa_{x}:Out" input = "bpb_{x}:In" }}',
            f'{{ output = "bpb_{x}:Out" input = "dly_{x}:In" }}',
            f'{{ output = "dly_{x}:Out" input = "xtc_{o}:In 2" }}',
            f'{{ output = "bpb_{x}:Out" input = "dly2_{x}:In" }}',
            f'{{ output = "dly2_{x}:Out" input = "xtc_{x}:In 3" }}',
        ]
    links.append('{ output = "xtc_l:Out" input = "lim:lv2_audio_in_1" }')
    links.append('{ output = "xtc_r:Out" input = "lim:lv2_audio_in_2" }')
    links.append('{ output = "lim:lv2_audio_out_1" input = "drive_l:In" }')
    links.append('{ output = "lim:lv2_audio_out_2" input = "drive_r:In" }')
    link_txt = "\n".join("                " + l for l in links)
    node_txt = "\n".join(lines)
    target = s["target_sink"]
    target_line = f'\n            target.object  = "{target}"' if target else ""
    return f"""# Generated by Speaker Tuner (graph v{GRAPH_VERSION}) - edits here are overwritten.
context.modules = [
{{   name = libpipewire-module-filter-chain
    args = {{
        node.description = "Speaker Tuner"
        media.name       = "Speaker Tuner"
        filter.graph = {{
            nodes = [
{node_txt}
            ]
            links = [
{link_txt}
            ]
            inputs  = [ "copy_l:In" "copy_r:In" ]
            outputs = [ "drive_l:Out" "drive_r:Out" ]
        }}
        capture.props = {{
            node.name      = "{NODE_NAME}"
            media.class    = Audio/Sink
            audio.channels = 2
            audio.position = [ FL FR ]
            priority.session = 2000
        }}
        playback.props = {{
            node.name      = "{OUT_NODE_NAME}"
            node.passive   = true
            audio.channels = 2
            audio.position = [ FL FR ]{target_line}
            stream.dont-remix = true
        }}
    }}
}}
]
"""


# ------------------------------------------------------------- pipewire glue

def run(*args):
    return subprocess.run(args, capture_output=True, text=True)


def find_node():
    """Return (node id, set of control names) for the filter sink, or (None, None)."""
    r = run("pw-dump", "Node")
    if r.returncode != 0:
        return None, None
    try:
        objs = json.loads(r.stdout)
    except json.JSONDecodeError:
        return None, None
    for o in objs:
        info = o.get("info") or {}
        if (info.get("props") or {}).get("node.name") != NODE_NAME:
            continue
        names = set()
        for p in (info.get("params") or {}).get("Props", []):
            a = p.get("params")
            if a:
                names.update(a[0::2])
        return o["id"], names
    return None, None


def push_live(node_id, c):
    parts = " ".join(f'"{k}" {v:.6g}' for k, v in c.items())
    return run("pw-cli", "set-param", str(node_id), "Props", f"{{ params = [ {parts} ] }}").returncode == 0


def default_sink():
    return run("pactl", "get-default-sink").stdout.strip()


def hardware_sinks():
    """[(name, description)] of every sink except our own filter."""
    r = run("pactl", "--format=json", "list", "sinks")
    try:
        sinks = [(x["name"], x.get("description") or x["name"]) for x in json.loads(r.stdout)]
    except (json.JSONDecodeError, KeyError, TypeError):
        r = run("pactl", "list", "short", "sinks")
        sinks = [(ln.split("\t")[1],) * 2 for ln in r.stdout.splitlines() if "\t" in ln]
    # Skip our own sink and other filter-chain/virtual effect sinks to avoid stacking filters.
    return [x for x in sinks if x[0] != NODE_NAME and not x[0].startswith("effect_input.")]


LV2_DIRS = [os.path.expanduser("~/.lv2"), "/usr/local/lib/lv2", "/usr/local/lib64/lv2", "/usr/lib/lv2",
            "/usr/lib64/lv2", "/usr/lib/x86_64-linux-gnu/lv2", "/usr/lib/aarch64-linux-gnu/lv2"]
SPA_DIRS = ["/usr/lib64/spa-0.2", "/usr/lib/spa-0.2", "/usr/lib/x86_64-linux-gnu/spa-0.2",
            "/usr/lib/aarch64-linux-gnu/spa-0.2", "/usr/local/lib/spa-0.2", "/usr/local/lib64/spa-0.2"]


def missing_deps():
    """Human-readable list of missing runtime pieces."""
    missing = []
    for tool in ("pw-cli", "pw-dump", "pactl"):
        if not any(os.access(os.path.join(d, tool), os.X_OK) for d in os.environ.get("PATH", "").split(":")):
            missing.append(tool)
    lv2_dirs = [d for d in os.environ.get("LV2_PATH", "").split(":") if d] + LV2_DIRS
    if not any(os.path.isdir(os.path.join(d, "ZaMaximX2.lv2")) for d in lv2_dirs):
        missing.append("ZaMaximX2 LV2 plugin (zam-plugins)")
    # PipeWire >= 1.4 ships LV2 support for filter-chain as a separate plugin.
    graph_dirs = [os.path.join(d, "filter-graph") for d in SPA_DIRS if os.path.isdir(os.path.join(d, "filter-graph"))]
    if graph_dirs and not any(os.path.exists(os.path.join(d, "libspa-filter-graph-plugin-lv2.so")) for d in graph_dirs):
        missing.append("PipeWire filter-chain LV2 support")
    return missing


def load_settings():
    s = dict(DEFAULTS)
    try:
        with open(SETTINGS_PATH) as f:
            s.update(json.load(f))
    except (OSError, json.JSONDecodeError):
        pass
    s["eq"] = (list(s["eq"]) + [0.0] * 10)[:10]
    return s


def save_settings(s):
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(s, f, indent=2)
    os.makedirs(os.path.dirname(CONF_PATH), exist_ok=True)
    tmp = CONF_PATH + ".tmp"
    with open(tmp, "w") as f:
        f.write(conf_text(s))
    os.replace(tmp, CONF_PATH)




PROFILES_PATH = os.path.join(os.path.dirname(SETTINGS_PATH), "profiles.json")
DEVICE_KEYS = ("target_sink",)  # per-machine, not stored in profiles


def load_profiles():
    try:
        with open(PROFILES_PATH) as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def save_profiles(profiles):
    os.makedirs(os.path.dirname(PROFILES_PATH), exist_ok=True)
    with open(PROFILES_PATH, "w") as f:
        json.dump(profiles, f, indent=2, sort_keys=True)


# ------------------------------------------------------------------------ UI

class Window(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Speaker Tuner", default_width=560, default_height=760)
        self.s = load_settings()
        self.node_id = None
        self.pending = 0
        self.building = True
        self.needs_restart = False
        self.scales = {}

        if not self.s["target_sink"]:
            self.s["target_sink"] = self.pick_initial_sink()
            save_settings(self.s)

        view = Adw.ToolbarView()
        header = Adw.HeaderBar()
        view.add_top_bar(header)
        self.banner = Adw.Banner()
        self.banner.connect("button-clicked", self.on_reload)
        view.add_top_bar(self.banner)

        self.toasts = Adw.ToastOverlay()
        page = Adw.PreferencesPage()
        self.toasts.set_child(page)
        view.set_content(self.toasts)
        self.set_content(view)

        # Device
        g = Adw.PreferencesGroup()
        page.add(g)
        self.sinks = hardware_sinks()
        self.device_row = Adw.ComboRow(title="Output device")
        self.device_row.connect("notify::selected", self.on_device)
        g.add(self.device_row)
        self.default_row = Adw.SwitchRow(title="Use Speaker Tuner")
        self.default_row.connect("notify::active", self.on_default_toggled)
        g.add(self.default_row)

        # Profiles: one row, actions as icon buttons
        g = Adw.PreferencesGroup()
        page.add(g)
        self.profile_row = Adw.ComboRow(title="Profile")
        self.profile_row.connect("notify::selected", self.on_profile_selected)
        for icon, tip, cb in (("document-save-symbolic", "Save as…", self.on_save_profile),
                              ("user-trash-symbolic", "Delete profile", self.on_delete_profile),
                              ("edit-undo-symbolic", "Reset to defaults", self.on_reset)):
            btn = Gtk.Button(icon_name=icon, tooltip_text=tip, valign=Gtk.Align.CENTER, css_classes=["flat"])
            btn.connect("clicked", cb)
            self.profile_row.add_suffix(btn)
            if cb == self.on_delete_profile:
                self.delete_btn = btn
        g.add(self.profile_row)

        # Loudness
        g = Adw.PreferencesGroup(title="Loudness")
        page.add(g)
        g.add(self.slider_row("boost_db", "Boost", "Gain into the limiter", 0, 20, 0.5, "{:+.1f} dB"))
        g.add(self.slider_row("ceiling_db", "Ceiling", "Highest output level", -6, 0, 0.1, "{:.1f} dBFS"))
        g.add(self.slider_row("release_ms", "Limiter release", "Longer is smoother, shorter is louder", 1, 100, 1, "{:.0f} ms"))
        g.add(self.slider_row("drive_db", "Overdrive", "Gain after the limiter. Above 0 it clips (crackles)", 0, 18, 0.5, "{:+.1f} dB"))

        # Speaker protection
        g = Adw.PreferencesGroup(
            title="Speaker",
            description="Small speakers can't play deep bass. Cutting it lets them go louder with less distortion",
        )
        page.add(g)
        g.add(self.slider_row("protect_hz", "Low cut", "4th-order high-pass", 20, 300, 5,
                              lambda v: "Off" if v <= 20 else f"{v:.0f} Hz"))

        # EQ
        g = Adw.PreferencesGroup(title="Equalizer")
        page.add(g)
        presets = Gtk.DropDown.new_from_strings(["Custom"] + list(PRESETS))
        presets.set_valign(Gtk.Align.CENTER)
        presets.connect("notify::selected", self.on_preset)
        g.set_header_suffix(presets)
        self.presets = presets
        box = Gtk.Box(spacing=2, homogeneous=True, margin_top=6, margin_bottom=6)
        self.eq_scales = []
        for i, f in enumerate(EQ_FREQS):
            col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            val = Gtk.Label(css_classes=["caption", "numeric"])
            sc = Gtk.Scale.new_with_range(Gtk.Orientation.VERTICAL, -12, 12, 0.5)
            sc.set_inverted(True)
            sc.set_draw_value(False)
            sc.set_size_request(-1, 130)
            sc.add_mark(0, Gtk.PositionType.LEFT, None)
            sc.connect("value-changed", self.on_eq, i, val)
            lab = Gtk.Label(label=f"{f // 1000}k" if f >= 1000 else str(f), css_classes=["caption", "dim-label"])
            col.append(val)
            col.append(sc)
            col.append(lab)
            box.append(col)
            self.eq_scales.append((sc, val))
        g.add(Gtk.Frame(child=box, css_classes=["view"]))

        # 3D
        g = Adw.PreferencesGroup(
            title="3D",
            description="Best sitting centred, about an arm's length away. Off while the crossover is on",
        )
        page.add(g)
        g.add(self.slider_row("width_pct", "Stereo width", "100% is normal", 0, 200, 5, "{:.0f}%"))
        g.add(self.slider_row("xtc_pct", "3D amount", "Crosstalk cancellation, pushes sound past the speakers", 0, 100, 5, "{:.0f}%"))
        g.add(self.slider_row("xtc_us", "3D delay", "Tune for your seating distance", 20, 300, 5, "{:.0f} µs"))

        # Crossover
        g = Adw.PreferencesGroup(
            title="Virtual crossover",
            description="Mixes to mono, then one speaker plays the lows and the other the highs",
        )
        page.add(g)
        self.xo_row = Adw.SwitchRow(title="Enable crossover")
        self.xo_row.connect("notify::active", lambda r, _: self.set("crossover", r.get_active()))
        g.add(self.xo_row)
        g.add(self.slider_row("xover_hz", "Crossover frequency", "Linkwitz-Riley 24 dB/oct", 80, 2000, 10, "{:.0f} Hz"))
        self.side_row = Adw.ComboRow(title="Bass speaker", model=Gtk.StringList.new(["Left", "Right"]))
        self.side_row.connect("notify::selected", lambda r, _: self.set("sub_side", "left" if r.get_selected() == 0 else "right"))
        g.add(self.side_row)
        g.add(self.slider_row("sub_db", "Bass speaker level", None, -12, 12, 0.5, "{:+.1f} dB"))
        g.add(self.slider_row("top_db", "Treble speaker level", None, -12, 12, 0.5, "{:+.1f} dB"))

        self.fill_devices()
        self.fill_profiles()
        self.sync_ui()
        self.building = False
        self.refresh_state()

    # -- widgets

    def slider_row(self, key, title, subtitle, lo, hi, step, fmt):
        fmt_fn = fmt if callable(fmt) else fmt.format
        row = Adw.ActionRow(title=title)
        if subtitle:
            row.set_tooltip_text(subtitle)
        val = Gtk.Label(css_classes=["numeric", "dim-label"], width_chars=9, xalign=1)
        sc = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, lo, hi, step)
        sc.set_draw_value(False)
        sc.set_hexpand(True)
        sc.set_size_request(200, -1)
        sc.set_valign(Gtk.Align.CENTER)

        def changed(scale):
            v = round(scale.get_value() / step) * step
            val.set_text(fmt_fn(v))
            self.set(key, v)

        sc.connect("value-changed", changed)
        row.add_suffix(sc)
        row.add_suffix(val)
        self.scales[key] = (sc, val, fmt_fn)
        return row

    def sync_ui(self):
        """Push self.s into every widget without triggering applies."""
        was, self.building = self.building, True
        for key, (sc, val, fmt_fn) in self.scales.items():
            sc.set_value(self.s[key])
            val.set_text(fmt_fn(self.s[key]))
        for (sc, val), gdb in zip(self.eq_scales, self.s["eq"]):
            sc.set_value(gdb)
            val.set_text(f"{gdb:+.1f}")
        self.xo_row.set_active(self.s["crossover"])
        self.side_row.set_selected(0 if self.s["sub_side"] == "left" else 1)
        self.sync_preset()
        self.building = was

    def sync_preset(self):
        """Select the preset matching the current EQ, or "Custom"."""
        names = list(PRESETS)
        match = next((i + 1 for i, n in enumerate(names) if [float(x) for x in PRESETS[n]] == self.s["eq"]), 0)
        was, self.building = self.building, True
        self.presets.set_selected(match)
        self.building = was

    def fill_devices(self):
        was, self.building = self.building, True
        names = [n for n, _ in self.sinks]
        if self.s["target_sink"] and self.s["target_sink"] not in names:
            self.sinks.append((self.s["target_sink"], f"{self.s['target_sink']} (not connected)"))
        self.device_row.set_model(Gtk.StringList.new([d for _, d in self.sinks]))
        for i, (n, _) in enumerate(self.sinks):
            if n == self.s["target_sink"]:
                self.device_row.set_selected(i)
        self.building = was

    def fill_profiles(self, select=None):
        was, self.building = self.building, True
        self.profiles = load_profiles()
        self.profile_names = sorted(self.profiles, key=str.casefold)
        self.profile_row.set_model(Gtk.StringList.new(self.profile_names or ["No saved profiles"]))
        self.profile_row.set_sensitive(bool(self.profile_names))
        self.delete_btn.set_sensitive(bool(self.profile_names))
        current = select if select is not None else self.s.get("profile")
        self.profile_row.set_selected(self.profile_names.index(current) if current in self.profile_names
                                      else Gtk.INVALID_LIST_POSITION)
        self.building = was

    def pick_initial_sink(self):
        names = [n for n, _ in hardware_sinks()]
        cur = default_sink()
        if cur in names:
            return cur
        non_hdmi = [n for n in names if "hdmi" not in n.lower()]
        return (non_hdmi or names or [""])[0]

    # -- settings

    def set(self, key, value):
        if self.building:
            return
        self.s[key] = value
        self.schedule_apply()

    def on_eq(self, scale, i, val):
        v = round(scale.get_value() * 2) / 2
        val.set_text(f"{v:+.1f}")
        if not self.building:
            self.s["eq"][i] = v
            self.sync_preset()
            self.schedule_apply()

    def on_preset(self, dd, _):
        idx = dd.get_selected()
        if self.building or idx in (0, Gtk.INVALID_LIST_POSITION):
            return
        self.s["eq"] = [float(x) for x in PRESETS[list(PRESETS)[idx - 1]]]
        was, self.building = self.building, True
        for (sc, val), gdb in zip(self.eq_scales, self.s["eq"]):
            sc.set_value(gdb)
            val.set_text(f"{gdb:+.1f}")
        self.building = was
        self.schedule_apply()

    def apply_values(self, values):
        """Replace everything except device settings with `values`, then update UI and audio."""
        keep = {k: self.s[k] for k in DEVICE_KEYS}
        self.s = json.loads(json.dumps(DEFAULTS))
        self.s.update({k: v for k, v in values.items() if k in DEFAULTS})
        self.s.update(keep)
        self.s["eq"] = (list(self.s["eq"]) + [0.0] * 10)[:10]
        self.sync_ui()
        self.schedule_apply()

    # -- profiles

    def on_profile_selected(self, row, _):
        idx = row.get_selected()
        if self.building or idx == Gtk.INVALID_LIST_POSITION or idx >= len(self.profile_names):
            return
        name = self.profile_names[idx]
        self.apply_values(self.profiles[name])
        self.s["profile"] = name
        self.toast(f"Loaded “{name}”")

    def on_save_profile(self, _row):
        entry = Gtk.Entry(text=self.s.get("profile") or "", placeholder_text="Profile name", activates_default=True)
        dlg = Adw.AlertDialog(heading="Save profile", body="Save the current settings under a name.")
        dlg.set_extra_child(entry)
        dlg.add_response("cancel", "Cancel")
        dlg.add_response("save", "Save")
        dlg.set_response_appearance("save", Adw.ResponseAppearance.SUGGESTED)
        dlg.set_default_response("save")
        dlg.set_close_response("cancel")
        entry.connect("changed", lambda e: dlg.set_response_enabled("save", bool(e.get_text().strip())))
        dlg.set_response_enabled("save", bool(entry.get_text().strip()))

        def done(d, response):
            name = entry.get_text().strip()
            if response != "save" or not name:
                return
            profiles = load_profiles()
            profiles[name] = {k: v for k, v in self.s.items() if k in DEFAULTS and k not in DEVICE_KEYS}
            try:
                save_profiles(profiles)
            except OSError as e:
                self.toast(f"Could not save profile: {e}")
                return
            self.s["profile"] = name
            self.schedule_apply()
            self.fill_profiles(select=name)
            self.toast(f"Saved “{name}”")

        dlg.connect("response", done)
        dlg.present(self)

    def on_delete_profile(self, _row):
        idx = self.profile_row.get_selected()
        if idx == Gtk.INVALID_LIST_POSITION or idx >= len(self.profile_names):
            self.toast("Pick a profile to delete first")
            return
        name = self.profile_names[idx]
        dlg = Adw.AlertDialog(heading=f"Delete “{name}”?", body="Your current settings stay as they are.")
        dlg.add_response("cancel", "Cancel")
        dlg.add_response("delete", "Delete")
        dlg.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
        dlg.set_close_response("cancel")

        def done(d, response):
            if response != "delete":
                return
            profiles = load_profiles()
            profiles.pop(name, None)
            save_profiles(profiles)
            if self.s.get("profile") == name:
                self.s.pop("profile", None)
                self.schedule_apply()
            self.fill_profiles()
            self.toast(f"Deleted “{name}”")

        dlg.connect("response", done)
        dlg.present(self)

    def on_reset(self, _row):
        dlg = Adw.AlertDialog(heading="Reset to defaults?",
                              body="Turns off every effect. Saved profiles and your output device are kept.")
        dlg.add_response("cancel", "Cancel")
        dlg.add_response("reset", "Reset")
        dlg.set_response_appearance("reset", Adw.ResponseAppearance.DESTRUCTIVE)
        dlg.set_close_response("cancel")

        def done(d, response):
            if response == "reset":
                self.apply_values({})
                self.s.pop("profile", None)
                self.fill_profiles()
                self.toast("Reset to defaults")

        dlg.connect("response", done)
        dlg.present(self)

    # -- audio

    def schedule_apply(self):
        if self.pending:
            GLib.source_remove(self.pending)
        self.pending = GLib.timeout_add(60, self.apply)

    def apply(self):
        self.pending = 0
        try:
            save_settings(self.s)
        except OSError as e:
            self.toast(f"Could not save settings: {e}")
        if self.node_id is not None and not self.banner.get_revealed():
            if not push_live(self.node_id, controls(self.s)):
                self.refresh_state()
        return GLib.SOURCE_REMOVE

    def show_banner(self, title, button=None):
        self.banner.set_title(title)
        self.banner.set_button_label(button)
        self.banner.set_revealed(True)

    def refresh_state(self):
        missing = missing_deps()
        if missing:
            self.node_id = None
            self.show_banner("Missing: " + ", ".join(missing) + ". See the README to install them.")
            return
        self.node_id, names = find_node()
        if self.node_id is None:
            self.show_banner("Speaker Tuner isn't loaded yet", "Load (restarts audio)")
        elif "xtc_l:Gain 3" not in names or self.needs_restart:
            self.show_banner("Restart audio to apply the change", "Restart audio")
        else:
            self.banner.set_revealed(False)
            push_live(self.node_id, controls(self.s))
        was, self.building = self.building, True
        self.default_row.set_active(default_sink() == NODE_NAME)
        self.building = was

    def on_device(self, row, _):
        idx = row.get_selected()
        if self.building or idx == Gtk.INVALID_LIST_POSITION or idx >= len(self.sinks):
            return
        name = self.sinks[idx][0]
        if name == self.s["target_sink"]:
            return
        self.s["target_sink"] = name
        save_settings(self.s)
        self.needs_restart = True
        self.refresh_state()

    def on_reload(self, _banner):
        save_settings(self.s)
        self.banner.set_revealed(False)
        self.toast("Restarting audio…")
        GLib.timeout_add(50, self._restart)

    def _restart(self):
        run("systemctl", "--user", "restart", "pipewire", "pipewire-pulse", "wireplumber")
        GLib.timeout_add(2500, self._after_restart)
        return GLib.SOURCE_REMOVE

    def _after_restart(self):
        self.needs_restart = False
        run("pactl", "set-default-sink", NODE_NAME)
        self.refresh_state()
        if self.node_id is None:
            self.toast("The filter didn't load. Check `journalctl --user -u pipewire`.")
        else:
            self.toast("Loaded. Restart your music player if it went quiet.")
        return GLib.SOURCE_REMOVE

    def on_default_toggled(self, row, _):
        if self.building:
            return
        run("pactl", "set-default-sink", NODE_NAME if row.get_active() else self.s["target_sink"])

    def toast(self, msg):
        self.toasts.add_toast(Adw.Toast(title=msg, timeout=3))


class App(Adw.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID)

    def do_activate(self):
        win = self.props.active_window or Window(self)
        win.present()


def main():
    if "--version" in sys.argv:
        print(VERSION)
        return 0
    if "--print-conf" in sys.argv:
        print(conf_text(load_settings()))
        return 0
    return App().run([sys.argv[0]])


if __name__ == "__main__":
    sys.exit(main())

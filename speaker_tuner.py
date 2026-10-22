#!/usr/bin/env python3
"""Speaker Tuner - a system-wide EQ, crossover and speaker tuner for PipeWire.

GTK4/libadwaita front end for a PipeWire filter-chain. It adds a virtual output
in front of any sink with: a 10-band parametric EQ (with live spectrum), boost +
limiter, overdrive, stereo width, crosstalk-cancellation 3D, and per-channel
routing/crossovers for any channel layout (2.0, 2.1, 5.1, 7.1, ...).

Every setting is a control on a filter graph whose layout only depends on the
target device's channels, so changes are pushed live with `pw-cli set-param`
(no audio restart). The config file is rewritten on each change so settings
survive reboots.
"""
import array
import cmath
import json
import math
import os
import subprocess
import sys

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gdk, GLib, Gtk  # noqa: E402

APP_ID = "io.github.pjamessteven.SpeakerTuner"
VERSION = "0.3.0"
NODE_NAME = "effect_input.speaker_tuner"
OUT_NODE_NAME = "effect_output.speaker_tuner"
CONF_PATH = os.path.expanduser("~/.config/pipewire/pipewire.conf.d/speaker-tuner.conf")
SETTINGS_PATH = os.path.expanduser("~/.config/speaker-tuner/settings.json")
PROFILES_PATH = os.path.join(os.path.dirname(SETTINGS_PATH), "profiles.json")
LIMITER_URI = "urn:zamaudio:ZaMaximX2"
GRAPH_VERSION = 7  # bump when the node layout changes (needs an audio restart)
RATE = 48000

EQ_FREQS = [31, 62, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
EQ_Q = 1.41  # one-octave bands
LP_OFF, HP_OFF = 23000.0, 5.0  # filters parked outside the audible range
FREQ_MIN, FREQ_MAX = 20.0, 20000.0
MAX_INPUTS = 8  # builtin mixer has 8 inputs

PRESETS = {
    "Flat": [0] * 10,
    "Loudness": [0, 0, 3, 3, 1, 0, 0, 1, 2, 2],
    "Bass": [0, 0, 5, 4, 2, 0, 0, 0, 0, 0],
    "Vocal": [0, 0, -2, -1, 1, 2, 3, 2, 0, 0],
    "Treble": [0, 0, 0, 0, 0, 0, 1, 2, 3, 4],
}

CHANNEL_NAMES = {"FL": "Front left", "FR": "Front right", "FC": "Center", "LFE": "Subwoofer (LFE)",
                 "RL": "Rear left", "RR": "Rear right", "SL": "Side left", "SR": "Side right",
                 "RC": "Rear center", "MONO": "Mono"}
PULSE_TO_PW = {"front-left": "FL", "front-right": "FR", "front-center": "FC", "lfe": "LFE",
               "rear-left": "RL", "rear-right": "RR", "rear-center": "RC", "side-left": "SL",
               "side-right": "SR", "mono": "MONO"}
SOURCES = [("same", "Same channel"), ("left", "Left"), ("right", "Right"), ("mono", "Mono (L+R)"),
           ("all", "All channels"), ("off", "Off")]

DEFAULT_BANDS = [{"f": float(f), "g": 0.0, "q": EQ_Q} for f in EQ_FREQS]
DEFAULT_CHANNEL = {"src": "same", "hp": FREQ_MIN, "lp": FREQ_MAX, "db": 0.0, "delay_ms": 0.0, "invert": False}

DEFAULTS = {
    "target_sink": "",
    "target_positions": ["FL", "FR"],
    "boost_db": 0.0,
    "ceiling_db": -1.0,
    "release_ms": 25.0,
    "drive_db": 0.0,
    "bands": DEFAULT_BANDS,
    "channels": {},
    "spatial_on": False,
    "width_pct": 100.0,
    "xtc_pct": 0.0,
    "xtc_us": 90.0,
    "spectrum_on": True,
}
DEVICE_KEYS = ("target_sink", "target_positions")  # per-machine, not stored in profiles


def clone(x):
    return json.loads(json.dumps(x))


def capture_positions(positions):
    """Input channels of our virtual sink: always FL/FR (for stereo apps), plus the device's other channels."""
    extra = [p for p in positions if p not in ("FL", "FR", "MONO")]
    return (["FL", "FR"] + extra)[:MAX_INPUTS]


def channel_cfg(s, pos):
    cfg = dict(DEFAULT_CHANNEL)
    if pos == "MONO":
        cfg["src"] = "mono"
    cfg.update(s["channels"].get(pos, {}))
    return cfg


# ---------------------------------------------------------------- setups

def setup_presets(positions):
    """Name -> function(positions) -> channels dict, for the channel layouts where they make sense."""
    mains = [p for p in positions if p != "LFE"]
    out = {"Pass-through": lambda: {}}
    out["Small speakers (low cut 120 Hz)"] = lambda: {p: {"hp": 120.0} for p in mains}
    if "FL" in positions and "FR" in positions and len(positions) == 2:
        out["Split: left bass, right treble"] = lambda: {
            "FL": {"src": "mono", "lp": 300.0}, "FR": {"src": "mono", "hp": 300.0}}
    if len(positions) > 2:
        def stereo_all():
            m = {"FL": "left", "FR": "right", "FC": "mono", "RL": "left", "SL": "left",
                 "RR": "right", "SR": "right", "RC": "mono", "LFE": "all"}
            ch = {p: {"src": m.get(p, "mono")} for p in positions}
            if "LFE" in positions:
                ch["LFE"]["lp"] = 80.0
            return ch
        out["Stereo to all speakers"] = stereo_all
    if "LFE" in positions:
        def bass_mgmt():
            ch = {p: {"hp": 80.0} for p in mains}
            ch["LFE"] = {"src": "all", "lp": 80.0}
            return ch
        out["Bass management (80 Hz)"] = bass_mgmt
    return out


# ---------------------------------------------------------------- graph model
#
#  per input channel:  copy → (FL/FR: width mix) → 10-band EQ → (FL/FR: 3D crosstalk cancel) → bus
#  per output channel: source mix of buses → high-pass → low-pass → level/polarity → delay
#                      → limiter (pairs) → overdrive → device channel

def nid(prefix, pos):
    return f"{prefix}_{pos.lower()}"


def node_specs(positions):
    cap = capture_positions(positions)
    specs = []
    for p in cap:
        specs.append((nid("in", p), "builtin", "copy"))
        if p in ("FL", "FR"):
            specs.append((nid("mix", p), "builtin", "mixer"))
        specs += [(nid(f"eq{i}", p), "builtin", "bq_peaking") for i in range(len(EQ_FREQS))]
        if p in ("FL", "FR"):
            specs += [(nid("bpa", p), "builtin", "bq_highpass"), (nid("bpb", p), "builtin", "bq_lowpass"),
                      (nid("dly", p), "builtin", "delay"), (nid("dly2", p), "builtin", "delay"),
                      (nid("xtc", p), "builtin", "mixer")]
    for q in positions:
        specs += [(nid("src", q), "builtin", "mixer"),
                  (nid("hp1", q), "builtin", "bq_highpass"), (nid("hp2", q), "builtin", "bq_highpass"),
                  (nid("lp1", q), "builtin", "bq_lowpass"), (nid("lp2", q), "builtin", "bq_lowpass"),
                  (nid("gain", q), "builtin", "linear"), (nid("cdly", q), "builtin", "delay"),
                  (nid("drive", q), "builtin", "linear")]
    specs += [(f"lim{j}", "lv2", LIMITER_URI) for j in range((len(positions) + 1) // 2)]
    return specs


def bus(p):
    return f"{nid('xtc', p)}:Out" if p in ("FL", "FR") else f"{nid('eq' + str(len(EQ_FREQS) - 1), p)}:Out"


def source_weights(src, q, cap):
    """Mixer gain for each capture channel feeding output channel q."""
    w = [0.0] * len(cap)
    idx = {p: i for i, p in enumerate(cap)}
    if src == "same" and q in idx:
        w[idx[q]] = 1.0
    elif src in ("left", "right"):
        w[idx["FL" if src == "left" else "FR"]] = 1.0
    elif src == "mono" or (src == "same" and q not in idx):
        w[idx["FL"]] = w[idx["FR"]] = 0.5
    elif src == "all":  # e.g. a subwoofer: own channel + every other channel's bass (stereo L+R sums to unity)
        for i in range(len(cap)):
            w[i] = 0.5
        if q in idx:
            w[idx[q]] = 1.0
    return w


def controls(s):
    """Map of 'node:Control' -> value for the given settings."""
    positions = s["target_positions"]
    cap = capture_positions(positions)
    c = {}
    w = s["width_pct"] / 100 if s["spatial_on"] else 1.0
    own, other = (1 + w) / 2, (1 - w) / 2
    c["mix_fl:Gain 1"], c["mix_fl:Gain 2"] = own, other
    c["mix_fr:Gain 1"], c["mix_fr:Gain 2"] = other, own
    for p in cap:
        for i, b in enumerate(s["bands"]):
            c[f"{nid(f'eq{i}', p)}:Freq"] = float(b["f"])
            c[f"{nid(f'eq{i}', p)}:Q"] = float(b["q"])
            c[f"{nid(f'eq{i}', p)}:Gain"] = float(b["g"])
    # 3D: crosstalk cancellation (RACE-style, unrolled to 2 terms since the graph can't loop).
    # out = own - g*D(other) + g^2*D2(own), cancellation path band-limited to 250 Hz-5 kHz.
    g = 0.71 * s["xtc_pct"] / 100 if s["spatial_on"] else 0.0  # 100% = -3 dB
    d = s["xtc_us"] / 1e6
    for p in ("FL", "FR"):
        c[f"{nid('bpa', p)}:Freq"], c[f"{nid('bpa', p)}:Q"] = 250.0, 0.7071
        c[f"{nid('bpb', p)}:Freq"], c[f"{nid('bpb', p)}:Q"] = 5000.0, 0.7071
        c[f"{nid('dly', p)}:Delay (s)"], c[f"{nid('dly2', p)}:Delay (s)"] = d, 2 * d
        x = nid("xtc", p)
        c[f"{x}:Gain 1"], c[f"{x}:Gain 2"], c[f"{x}:Gain 3"] = 1.0, -g, g * g
    drive = 10 ** (s["drive_db"] / 20)
    for q in positions:
        cfg = channel_cfg(s, q)
        for i, wt in enumerate(source_weights(cfg["src"], q, cap)):
            c[f"{nid('src', q)}:Gain {i + 1}"] = wt
        hp = float(cfg["hp"]) if cfg["hp"] > FREQ_MIN else HP_OFF
        lp = float(cfg["lp"]) if cfg["lp"] < FREQ_MAX else LP_OFF
        for n in ("hp1", "hp2"):  # Linkwitz-Riley 4th order = 2x Butterworth Q 0.7071
            c[f"{nid(n, q)}:Freq"], c[f"{nid(n, q)}:Q"] = hp, 0.7071
        for n in ("lp1", "lp2"):
            c[f"{nid(n, q)}:Freq"], c[f"{nid(n, q)}:Q"] = lp, 0.7071
        level = 10 ** (cfg["db"] / 20) * (-1 if cfg["invert"] else 1)
        c[f"{nid('gain', q)}:Mult"], c[f"{nid('gain', q)}:Add"] = level, 0.0
        c[f"{nid('cdly', q)}:Delay (s)"] = cfg["delay_ms"] / 1000
        # post-limiter gain: anything above 0 dBFS hard-clips at the DAC
        c[f"{nid('drive', q)}:Mult"], c[f"{nid('drive', q)}:Add"] = drive, 0.0
    for j in range((len(positions) + 1) // 2):
        c[f"lim{j}:gain"] = float(s["boost_db"])
        c[f"lim{j}:thresh"] = float(s["ceiling_db"])
        c[f"lim{j}:rel"] = float(s["release_ms"])
    return c


def conf_text(s):
    positions = list(s["target_positions"]) or ["FL", "FR"]
    cap = capture_positions(positions)
    c = controls(s)
    lines = []
    for name, typ, what in node_specs(positions):
        ctl = " ".join(f'"{k.split(":", 1)[1]}" = {v:.6g}' for k, v in c.items() if k.split(":", 1)[0] == name)
        key = "plugin" if typ == "lv2" else "label"
        ctl_part = f" control = {{ {ctl} }}" if ctl else ""
        cfg = ""
        if what == "delay":
            cfg = ' config = { "max-delay" = %s }' % ("0.05" if name.startswith("cdly") else "0.01")
        lines.append(f'                {{ type = {typ} name = {name} {key} = "{what}"{cfg}{ctl_part} }}')

    links = []

    def link(a, b):
        links.append(f'{{ output = "{a}" input = "{b}" }}')

    last_eq = len(EQ_FREQS) - 1
    for p in cap:
        first = nid("eq0", p)
        if p in ("FL", "FR"):
            link(f"in_fl:Out", f"{nid('mix', p)}:In 1")
            link(f"in_fr:Out", f"{nid('mix', p)}:In 2")
            link(f"{nid('mix', p)}:Out", f"{first}:In")
        else:
            link(f"{nid('in', p)}:Out", f"{first}:In")
        for i in range(last_eq):
            link(f"{nid(f'eq{i}', p)}:Out", f"{nid(f'eq{i + 1}', p)}:In")
    for p, o in (("FL", "FR"), ("FR", "FL")):
        e = f"{nid(f'eq{last_eq}', p)}:Out"
        link(e, f"{nid('xtc', p)}:In 1")
        link(e, f"{nid('bpa', p)}:In")
        link(f"{nid('bpa', p)}:Out", f"{nid('bpb', p)}:In")
        link(f"{nid('bpb', p)}:Out", f"{nid('dly', p)}:In")
        link(f"{nid('dly', p)}:Out", f"{nid('xtc', o)}:In 2")
        link(f"{nid('bpb', p)}:Out", f"{nid('dly2', p)}:In")
        link(f"{nid('dly2', p)}:Out", f"{nid('xtc', p)}:In 3")
    for k, q in enumerate(positions):
        for i, p in enumerate(cap):
            link(bus(p), f"{nid('src', q)}:In {i + 1}")
        chain = ["src", "hp1", "hp2", "lp1", "lp2", "gain", "cdly"]
        for a, b in zip(chain, chain[1:]):
            link(f"{nid(a, q)}:Out", f"{nid(b, q)}:In")
        j, n = divmod(k, 2)
        link(f"{nid('cdly', q)}:Out", f"lim{j}:lv2_audio_in_{n + 1}")
        link(f"lim{j}:lv2_audio_out_{n + 1}", f"{nid('drive', q)}:In")

    node_txt = "\n".join(lines)
    link_txt = "\n".join("                " + l for l in links)
    ins = " ".join(f'"{nid("in", p)}:In"' for p in cap)
    outs = " ".join(f'"{nid("drive", q)}:Out"' for q in positions)
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
            inputs  = [ {ins} ]
            outputs = [ {outs} ]
        }}
        capture.props = {{
            node.name      = "{NODE_NAME}"
            media.class    = Audio/Sink
            audio.channels = {len(cap)}
            audio.position = [ {" ".join(cap)} ]
            priority.session = 2000
        }}
        playback.props = {{
            node.name      = "{OUT_NODE_NAME}"
            node.passive   = true
            audio.channels = {len(positions)}
            audio.position = [ {" ".join(positions)} ]{target_line}
            stream.dont-remix = true
        }}
    }}
}}
]
"""


def graph_matches(names, positions):
    """True if the loaded filter was built for this graph version and channel layout."""
    if not names or f"lim0:gain" not in names or "bpa_fl:Freq" not in names:
        return False
    loaded = {n.split(":")[0][4:] for n in names if n.startswith("src_") and n.endswith(":Gain 1")}
    return loaded == {p.lower() for p in positions}


# ---------------------------------------------------------------- EQ maths

def peaking_response(freqs, bands):
    """Combined magnitude in dB of RBJ peaking filters (as PipeWire's bq_peaking) at each frequency."""
    out = [0.0] * len(freqs)
    for b in bands:
        if abs(b["g"]) < 1e-6:
            continue
        A = 10 ** (b["g"] / 40)
        w0 = 2 * math.pi * b["f"] / RATE
        alpha = math.sin(w0) / (2 * b["q"])
        cw = math.cos(w0)
        b0, b1, b2 = 1 + alpha * A, -2 * cw, 1 - alpha * A
        a0, a1, a2 = 1 + alpha / A, -2 * cw, 1 - alpha / A
        for i, f in enumerate(freqs):
            z1 = cmath.exp(-1j * 2 * math.pi * f / RATE)
            z2 = z1 * z1
            h = (b0 + b1 * z1 + b2 * z2) / (a0 + a1 * z1 + a2 * z2)
            out[i] += 20 * math.log10(max(abs(h), 1e-9))
    return out


class FFT:
    """Small radix-2 FFT so the spectrum works without numpy."""

    def __init__(self, n):
        self.n = n
        bits = n.bit_length() - 1
        self.rev = [int(f"{i:0{bits}b}"[::-1], 2) for i in range(n)]
        self.tw = [cmath.exp(-2j * math.pi * k / n) for k in range(n // 2)]
        self.win = [0.5 - 0.5 * math.cos(2 * math.pi * i / (n - 1)) for i in range(n)]

    def magnitudes(self, samples):
        n = self.n
        a = [complex(samples[self.rev[i]] * self.win[self.rev[i]]) for i in range(n)]
        size = 2
        while size <= n:
            half, step = size // 2, n // size
            tw = self.tw[::step][:half]
            for start in range(0, n, size):
                for k in range(half):
                    i, j = start + k, start + k + half
                    t = tw[k] * a[j]
                    a[j] = a[i] - t
                    a[i] = a[i] + t
            size *= 2
        return [abs(x) for x in a[: n // 2]]


class Analyzer:
    """Streams the device's output through `pw-record` and keeps a smoothed log-frequency spectrum."""

    N = 2048

    def __init__(self, on_update):
        self.on_update = on_update
        self.proc = None
        self.watch = 0
        self.timer = 0
        self.buf = bytearray()
        self.fft = FFT(self.N)
        self.columns = 96
        self.edges = [FREQ_MIN * (FREQ_MAX / FREQ_MIN) ** (i / self.columns) for i in range(self.columns + 1)]
        self.levels = [-120.0] * self.columns
        self.fresh = False

    def start(self, target):
        self.stop()
        if not target:
            return
        try:
            self.proc = subprocess.Popen(
                ["pw-record", "--target", target, "-P", "{ stream.capture.sink = true node.dont-reconnect = true }",
                 "--format", "f32", "--channels", "1", "--rate", str(RATE), "--raw", "-"],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        except OSError:
            self.proc = None
            return
        os.set_blocking(self.proc.stdout.fileno(), False)
        self.watch = GLib.io_add_watch(self.proc.stdout.fileno(), GLib.IO_IN | GLib.IO_HUP, self._read)
        self.timer = GLib.timeout_add(66, self._tick)

    def stop(self):
        if self.watch:
            GLib.source_remove(self.watch)
            self.watch = 0
        if self.timer:
            GLib.source_remove(self.timer)
            self.timer = 0
        if self.proc:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self.proc.kill()
            self.proc = None
        self.levels = [-120.0] * self.columns

    def _read(self, fd, cond):
        try:
            data = os.read(fd, 65536)
        except BlockingIOError:
            return True
        if not data:
            self.watch = 0
            return False
        self.buf += data
        keep = self.N * 4
        if len(self.buf) > keep:
            del self.buf[: len(self.buf) - keep]
        self.fresh = True
        return True

    def _tick(self):
        if self.fresh and len(self.buf) >= self.N * 4:
            self.fresh = False
            samples = array.array("f")
            samples.frombytes(bytes(self.buf[-self.N * 4:]))
            mags = self.fft.magnitudes(samples)
            hz_per_bin = RATE / self.N
            norm = 4.0 / self.N  # Hann window, one-sided: full-scale sine ~ 0 dB
            for c in range(self.columns):
                lo = max(1, int(self.edges[c] / hz_per_bin))
                hi = max(lo + 1, int(self.edges[c + 1] / hz_per_bin) + 1)
                peak = max(mags[lo:hi]) * norm
                db = 20 * math.log10(max(peak, 1e-7))
                prev = self.levels[c]
                self.levels[c] = db if db > prev else prev - 3.0  # fast attack, slow fall
        else:
            self.levels = [max(-120.0, v - 3.0) for v in self.levels]
        self.on_update()
        return True


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
    """[(name, description, [positions])] of every sink except our own and other effect sinks."""
    r = run("pactl", "--format=json", "list", "sinks")
    sinks = []
    try:
        for x in json.loads(r.stdout):
            cmap = x.get("channel_map") or "front-left,front-right"
            pos = [PULSE_TO_PW.get(c, c.upper().replace("-", "_")) for c in cmap.split(",")]
            sinks.append((x["name"], x.get("description") or x["name"], pos))
    except (json.JSONDecodeError, KeyError, TypeError):
        r = run("pactl", "list", "short", "sinks")
        sinks = [(ln.split("\t")[1], ln.split("\t")[1], ["FL", "FR"]) for ln in r.stdout.splitlines() if "\t" in ln]
    # Skip our own sink and other filter-chain/virtual effect sinks to avoid stacking filters.
    return [x for x in sinks if x[0] != NODE_NAME and not x[0].startswith("effect_input.")]


LV2_DIRS = [os.path.expanduser("~/.lv2"), "/usr/local/lib/lv2", "/usr/local/lib64/lv2", "/usr/lib/lv2",
            "/usr/lib64/lv2", "/usr/lib/x86_64-linux-gnu/lv2", "/usr/lib/aarch64-linux-gnu/lv2"]
SPA_DIRS = ["/usr/lib64/spa-0.2", "/usr/lib/spa-0.2", "/usr/lib/x86_64-linux-gnu/spa-0.2",
            "/usr/lib/aarch64-linux-gnu/spa-0.2", "/usr/local/lib/spa-0.2", "/usr/local/lib64/spa-0.2"]


def missing_deps():
    """Human-readable list of missing runtime pieces."""
    missing = []
    for tool in ("pw-cli", "pw-dump", "pw-record", "pactl"):
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


# ------------------------------------------------------------- settings

def migrate(values):
    """Convert settings/profiles from older versions in place."""
    v = dict(values)
    if "bands" not in v and "eq" in v:
        gains = (list(v["eq"]) + [0.0] * 10)[:10]
        v["bands"] = [{"f": float(f), "g": float(g), "q": EQ_Q} for f, g in zip(EQ_FREQS, gains)]
    if "channels" not in v and any(k in v for k in ("crossover", "protect_hz")):
        protect = float(v.get("protect_hz", 20.0))
        ch = {}
        if v.get("crossover"):
            xo = float(v.get("xover_hz", 250.0))
            sub, top = ("FL", "FR") if v.get("sub_side", "left") == "left" else ("FR", "FL")
            ch[sub] = {"src": "mono", "lp": xo, "db": float(v.get("sub_db", 0.0))}
            ch[top] = {"src": "mono", "hp": xo, "db": float(v.get("top_db", 0.0))}
            if protect > FREQ_MIN:
                ch[sub]["hp"] = protect
                ch[top]["hp"] = max(xo, protect)
        elif protect > FREQ_MIN:
            ch = {"FL": {"hp": protect}, "FR": {"hp": protect}}
        v["channels"] = ch
    if "spatial_on" not in v:
        v["spatial_on"] = v.get("xtc_pct", 0) > 0 or v.get("width_pct", 100) != 100
    return v


def normalize(values):
    v = migrate(values)
    s = clone(DEFAULTS)
    s.update({k: clone(x) for k, x in v.items() if k in DEFAULTS or k == "profile"})
    bands = [dict(DEFAULT_BANDS[i], **b) for i, b in enumerate(list(s["bands"])[:10])]
    s["bands"] = bands + clone(DEFAULT_BANDS[len(bands):])
    if not isinstance(s["channels"], dict):
        s["channels"] = {}
    return s


def load_settings():
    try:
        with open(SETTINGS_PATH) as f:
            return normalize(json.load(f))
    except (OSError, json.JSONDecodeError):
        return normalize({})


def save_settings(s):
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(s, f, indent=2)
    os.makedirs(os.path.dirname(CONF_PATH), exist_ok=True)
    tmp = CONF_PATH + ".tmp"
    with open(tmp, "w") as f:
        f.write(conf_text(s))
    os.replace(tmp, CONF_PATH)


def load_profiles():
    try:
        with open(PROFILES_PATH) as f:
            data = json.load(f)
        return {k: migrate(v) for k, v in data.items()} if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def save_profiles(profiles):
    os.makedirs(os.path.dirname(PROFILES_PATH), exist_ok=True)
    with open(PROFILES_PATH, "w") as f:
        json.dump(profiles, f, indent=2, sort_keys=True)


def profile_values(s):
    return {k: clone(v) for k, v in s.items() if k in DEFAULTS and k not in DEVICE_KEYS}


# ------------------------------------------------------------- formatting

def fmt_hz(f):
    return f"{f / 1000:.1f} kHz" if f >= 1000 else f"{f:.0f} Hz"


def to_log(f):
    return math.log10(f)


def from_log(v):
    return 10 ** v


# ------------------------------------------------------------------------ EQ widget

class EqGraph(Gtk.DrawingArea):
    """Parametric EQ: response curve, draggable band handles, and a live spectrum behind it."""

    DB_RANGE = 15.0
    SPEC_FLOOR = -90.0

    def __init__(self, win):
        super().__init__(hexpand=True, content_height=260)
        self.win = win
        self.selected = 0
        self.drag_band = None
        self.drag_start = (0, 0, 0, 0)
        self.curve_cache = None
        self.set_draw_func(self.draw)
        self.set_focusable(True)

        drag = Gtk.GestureDrag()
        drag.connect("drag-begin", self.on_drag_begin)
        drag.connect("drag-update", self.on_drag_update)
        drag.connect("drag-end", lambda *_: setattr(self, "drag_band", None))
        self.add_controller(drag)
        click = Gtk.GestureClick()
        click.connect("pressed", self.on_click)
        self.add_controller(click)
        scroll = Gtk.EventControllerScroll(flags=Gtk.EventControllerScrollFlags.VERTICAL)
        scroll.connect("scroll", self.on_scroll)
        self.add_controller(scroll)

    # geometry
    def x_of(self, f, w):
        return (math.log10(f) - math.log10(FREQ_MIN)) / (math.log10(FREQ_MAX) - math.log10(FREQ_MIN)) * w

    def f_of(self, x, w):
        t = min(max(x / max(w, 1), 0), 1)
        return FREQ_MIN * (FREQ_MAX / FREQ_MIN) ** t

    def y_of(self, db, h):
        return h / 2 - db / self.DB_RANGE * (h / 2 - 12)

    def db_of(self, y, h):
        return (h / 2 - y) / (h / 2 - 12) * self.DB_RANGE

    def band_at(self, x, y):
        w, h = self.get_width(), self.get_height()
        best, dist = None, 14.0
        for i, b in enumerate(self.win.s["bands"]):
            d = math.hypot(self.x_of(b["f"], w) - x, self.y_of(b["g"], h) - y)
            if d < dist:
                best, dist = i, d
        return best

    # interaction
    def on_drag_begin(self, gesture, x, y):
        self.grab_focus()
        i = self.band_at(x, y)
        self.drag_band = i
        if i is not None:
            self.select(i)
            b = self.win.s["bands"][i]
            self.drag_start = (x, y, b["f"], b["g"])

    def on_drag_update(self, gesture, dx, dy):
        if self.drag_band is None:
            return
        w, h = self.get_width(), self.get_height()
        x0, y0, _f0, _g0 = self.drag_start
        b = self.win.s["bands"][self.drag_band]
        b["f"] = round(self.f_of(x0 + dx, w), 1)
        b["g"] = round(min(max(self.db_of(y0 + dy, h), -self.DB_RANGE), self.DB_RANGE) * 2) / 2
        self.win.on_bands_changed()

    def on_click(self, gesture, n_press, x, y):
        i = self.band_at(x, y)
        if i is None:
            return
        self.select(i)
        if n_press == 2:  # double-click: flatten band
            self.win.s["bands"][i]["g"] = 0.0
            self.win.on_bands_changed()

    def on_scroll(self, ctrl, dx, dy):
        b = self.win.s["bands"][self.selected]
        b["q"] = round(min(max(b["q"] * (0.9 if dy > 0 else 1.1), 0.1), 10.0), 2)
        self.win.on_bands_changed()
        return True

    def select(self, i):
        self.selected = i
        self.win.on_band_selected(i)
        self.queue_draw()

    def invalidate(self):
        self.curve_cache = None
        self.queue_draw()

    # drawing
    def draw(self, area, cr, w, h):
        fg = self.get_color()
        try:
            accent = Adw.StyleManager.get_default().get_accent_color_rgba()
        except AttributeError:  # libadwaita < 1.6
            accent = Gdk.RGBA()
            accent.parse("#3584e4")

        # background + grid
        cr.set_source_rgba(fg.red, fg.green, fg.blue, 0.04)
        cr.rectangle(0, 0, w, h)
        cr.fill()
        cr.set_line_width(1)
        cr.select_font_face("Sans")
        cr.set_font_size(10)
        for f in (50, 100, 200, 500, 1000, 2000, 5000, 10000):
            x = round(self.x_of(f, w)) + 0.5
            cr.set_source_rgba(fg.red, fg.green, fg.blue, 0.08)
            cr.move_to(x, 0)
            cr.line_to(x, h)
            cr.stroke()
            cr.set_source_rgba(fg.red, fg.green, fg.blue, 0.4)
            cr.move_to(x + 3, h - 4)
            cr.show_text(f"{f // 1000}k" if f >= 1000 else str(f))
        for db in (-12, -6, 0, 6, 12):
            y = round(self.y_of(db, h)) + 0.5
            cr.set_source_rgba(fg.red, fg.green, fg.blue, 0.16 if db == 0 else 0.08)
            cr.move_to(0, y)
            cr.line_to(w, y)
            cr.stroke()
            cr.set_source_rgba(fg.red, fg.green, fg.blue, 0.4)
            cr.move_to(3, y - 3)
            cr.show_text(f"{db:+d}" if db else "0 dB")

        # live spectrum (own scale: SPEC_FLOOR..0 dBFS over the full height)
        an = self.win.analyzer
        if self.win.s["spectrum_on"] and an.proc:
            cr.move_to(0, h)
            for c, lvl in enumerate(an.levels):
                x0 = self.x_of(an.edges[c], w)
                x1 = self.x_of(an.edges[c + 1], w)
                t = min(max((lvl - self.SPEC_FLOOR) / -self.SPEC_FLOOR, 0), 1)
                y = h - t * h
                cr.line_to(x0, y)
                cr.line_to(x1, y)
            cr.line_to(w, h)
            cr.close_path()
            cr.set_source_rgba(fg.red, fg.green, fg.blue, 0.13)
            cr.fill()

        # response curve
        if self.curve_cache is None or self.curve_cache[0] != w:
            n = max(int(w / 3), 64)
            freqs = [self.f_of(i * w / (n - 1), w) for i in range(n)]
            self.curve_cache = (w, freqs, peaking_response(freqs, self.win.s["bands"]))
        _, freqs, resp = self.curve_cache
        cr.set_line_width(2.5)
        for i, (f, db) in enumerate(zip(freqs, resp)):
            x, y = self.x_of(f, w), self.y_of(max(min(db, self.DB_RANGE + 3), -self.DB_RANGE - 3), h)
            cr.move_to(x, y) if i == 0 else cr.line_to(x, y)
        cr.set_source_rgba(accent.red, accent.green, accent.blue, 1)
        cr.stroke_preserve()
        cr.line_to(w, self.y_of(0, h))
        cr.line_to(0, self.y_of(0, h))
        cr.close_path()
        cr.set_source_rgba(accent.red, accent.green, accent.blue, 0.15)
        cr.fill()

        # band handles
        for i, b in enumerate(self.win.s["bands"]):
            x, y = self.x_of(b["f"], w), self.y_of(b["g"], h)
            r = 7 if i == self.selected else 5
            cr.arc(x, y, r, 0, 2 * math.pi)
            cr.set_source_rgba(accent.red, accent.green, accent.blue, 1 if i == self.selected else 0.75)
            cr.fill_preserve()
            cr.set_source_rgba(1, 1, 1, 0.9)
            cr.set_line_width(1.5)
            cr.stroke()


# ------------------------------------------------------------------------ UI

class Window(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Speaker Tuner", default_width=1180, default_height=820)
        self.set_size_request(360, 480)
        self.s = load_settings()
        self.node_id = None
        self.pending = 0
        self.building = True
        self.needs_restart = False
        self.loaders = []  # callables that push self.s into widgets
        self.profiles = {}
        self.profile_names = []
        self.analyzer = Analyzer(self.on_spectrum)

        self.sinks = hardware_sinks()
        if not self.s["target_sink"] or self.s["target_sink"] not in [n for n, _, _ in self.sinks]:
            if not self.s["target_sink"]:
                self.s["target_sink"] = self.pick_initial_sink()
        for n, _, pos in self.sinks:
            if n == self.s["target_sink"]:
                self.s["target_positions"] = pos

        # header: profile bar
        view = Adw.ToolbarView()
        header = Adw.HeaderBar()
        pbox = Gtk.Box(spacing=6)
        pbox.append(Gtk.Label(label="Profile", css_classes=["dim-label"]))
        self.profile_dd = Gtk.DropDown()
        self.profile_dd.connect("notify::selected", self.on_profile_selected)
        pbox.append(self.profile_dd)
        actions = Gtk.Box(css_classes=["linked"])
        for icon, tip, cb in (("document-save-symbolic", "Save as new profile…", self.on_save_profile),
                              ("user-trash-symbolic", "Delete profile", self.on_delete_profile),
                              ("edit-undo-symbolic", "Reset to defaults", self.on_reset)):
            btn = Gtk.Button(icon_name=icon, tooltip_text=tip)
            btn.connect("clicked", cb)
            actions.append(btn)
            if cb == self.on_delete_profile:
                self.delete_btn = btn
        pbox.append(actions)
        header.pack_start(pbox)
        view.add_top_bar(header)
        self.banner = Adw.Banner()
        self.banner.connect("button-clicked", self.on_reload)
        view.add_top_bar(self.banner)

        self.toasts = Adw.ToastOverlay()
        scroller = Gtk.ScrolledWindow(hscrollbar_policy=Gtk.PolicyType.NEVER)
        self.columns = Gtk.Box(spacing=24, margin_top=18, margin_bottom=24, margin_start=18, margin_end=18,
                               homogeneous=False)
        left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18, width_request=380)
        right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18, hexpand=True)
        self.columns.append(left)
        self.columns.append(right)
        scroller.set_child(self.columns)
        self.toasts.set_child(scroller)
        view.set_content(self.toasts)
        self.set_content(view)

        bp = Adw.Breakpoint.new(Adw.BreakpointCondition.parse("max-width: 900sp"))
        bp.add_setter(self.columns, "orientation", Gtk.Orientation.VERTICAL)
        bp.add_setter(left, "width-request", -1)
        self.add_breakpoint(bp)

        # ---- left column: output, loudness, channels
        g = Adw.PreferencesGroup(title="Output")
        left.append(g)
        self.device_row = Adw.ComboRow(title="Device")
        self.device_row.connect("notify::selected", self.on_device)
        g.add(self.device_row)
        self.default_row = Adw.SwitchRow(title="Use Speaker Tuner", subtitle="Make it the default output")
        self.default_row.connect("notify::active", self.on_default_toggled)
        g.add(self.default_row)

        g = Adw.PreferencesGroup(title="Loudness")
        left.append(g)
        g.add(self.slider("Boost", "Gain into the limiter", 0, 20, 0.5, lambda v: f"{v:+.1f} dB", "boost_db"))
        g.add(self.slider("Ceiling", "Highest output level", -6, 0, 0.1, lambda v: f"{v:.1f} dBFS", "ceiling_db"))
        g.add(self.slider("Limiter release", "Longer is smoother, shorter is louder", 1, 100, 1,
                          lambda v: f"{v:.0f} ms", "release_ms"))
        g.add(self.slider("Overdrive", "Gain after the limiter. Above 0 it clips (crackles)", 0, 18, 0.5,
                          lambda v: f"{v:+.1f} dB", "drive_db"))

        self.channels_group = Adw.PreferencesGroup(
            title="Channels", description="Routing, crossover, level and delay for each speaker channel")
        left.append(self.channels_group)
        self.setup_dd = Gtk.DropDown(valign=Gtk.Align.CENTER, tooltip_text="Apply a channel setup")
        self.setup_dd.connect("notify::selected", self.on_setup)
        self.channels_group.set_header_suffix(self.setup_dd)
        self.channel_rows = []

        # ---- right column: EQ, 3D
        g = Adw.PreferencesGroup(title="Equalizer",
                                 description="Drag points to shape the curve, scroll to change width, double-click to reset")
        right.append(g)
        hdr = Gtk.Box(spacing=6, valign=Gtk.Align.CENTER)
        self.spectrum_btn = Gtk.ToggleButton(label="Spectrum", tooltip_text="Show the live output spectrum")
        self.spectrum_btn.connect("toggled", self.on_spectrum_toggled)
        hdr.append(self.spectrum_btn)
        self.presets = Gtk.DropDown.new_from_strings(["Custom"] + list(PRESETS))
        self.presets.connect("notify::selected", self.on_preset)
        hdr.append(self.presets)
        g.set_header_suffix(hdr)
        self.eq = EqGraph(self)
        frame = Gtk.Frame(child=self.eq, css_classes=["view"])
        g.add(frame)
        band_box = Gtk.Box(spacing=12, margin_top=8, halign=Gtk.Align.CENTER)
        self.band_label = Gtk.Label(css_classes=["heading"], width_chars=7)
        band_box.append(self.band_label)
        self.spin_f = self.spin(band_box, "Freq", FREQ_MIN, FREQ_MAX, 1, 0, "f")
        self.spin_g = self.spin(band_box, "Gain", -15, 15, 0.5, 1, "g")
        self.spin_q = self.spin(band_box, "Q", 0.1, 10, 0.05, 2, "q")
        g.add(band_box)

        g = Adw.PreferencesGroup(title="3D", description="Best sitting centred, about an arm's length away")
        right.append(g)
        self.spatial_row = Adw.SwitchRow(title="Enable 3D")
        self.spatial_row.connect("notify::active", self.on_spatial)
        g.add(self.spatial_row)
        self.spatial_sliders = [
            self.slider("Stereo width", "100% is normal", 0, 200, 5, lambda v: f"{v:.0f}%", "width_pct"),
            self.slider("3D amount", "Crosstalk cancellation, pushes sound past the speakers", 0, 100, 5,
                        lambda v: f"{v:.0f}%", "xtc_pct"),
            self.slider("3D delay", "Tune for your seating distance", 20, 300, 5, lambda v: f"{v:.0f} µs", "xtc_us"),
        ]
        for r in self.spatial_sliders:
            g.add(r)

        self.loaders.append(self.load_misc)
        self.fill_devices()
        self.build_channels()
        self.fill_profiles()
        self.sync_ui()
        self.building = False
        self.connect("close-request", self.on_close)
        self.refresh_state()
        self.update_analyzer()

    # -- widget factories

    def slider(self, title, tip, lo, hi, step, fmt, key=None, get=None, put=None, log=False):
        """ActionRow with a scale. Reads/writes self.s[key], or uses get()/put(v) for nested values."""
        get = get or (lambda: self.s[key])
        put = put or (lambda v: self.s.__setitem__(key, v))
        row = Adw.ActionRow(title=title, tooltip_text=tip)
        val = Gtk.Label(css_classes=["numeric", "dim-label"], width_chars=9, xalign=1)
        lo_s, hi_s = (to_log(lo), to_log(hi)) if log else (lo, hi)
        sc = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, lo_s, hi_s, 0.001 if log else step)
        sc.set_draw_value(False)
        sc.set_hexpand(True)
        sc.set_size_request(140, -1)
        sc.set_valign(Gtk.Align.CENTER)

        def value_of(scale_v):
            v = from_log(scale_v) if log else scale_v
            return round(v / step) * step

        def changed(scale):
            v = value_of(scale.get_value())
            val.set_text(fmt(v))
            if not self.building:
                put(v)
                self.schedule_apply()

        def load():
            v = get()
            sc.set_value(to_log(min(max(v, lo), hi)) if log else v)
            val.set_text(fmt(v))

        sc.connect("value-changed", changed)
        row.add_suffix(sc)
        row.add_suffix(val)
        self.loaders.append(load)
        return row

    def spin(self, box, label, lo, hi, step, digits, key):
        box.append(Gtk.Label(label=label, css_classes=["dim-label"]))
        sp = Gtk.SpinButton.new_with_range(lo, hi, step)
        sp.set_digits(digits)
        sp.set_width_chars(6 if key == "f" else 4)

        def changed(s):
            if self.building:
                return
            self.s["bands"][self.eq.selected][key] = s.get_value()
            self.on_bands_changed(from_spin=True)

        sp.connect("value-changed", changed)
        box.append(sp)
        return sp

    # -- sync

    def load_misc(self):
        self.spatial_row.set_active(self.s["spatial_on"])
        for r in self.spatial_sliders:
            r.set_sensitive(self.s["spatial_on"])
        self.spectrum_btn.set_active(self.s["spectrum_on"])

    def sync_ui(self):
        was, self.building = self.building, True
        for load in self.loaders:
            load()
        self.on_band_selected(self.eq.selected)
        self.sync_preset()
        self.eq.invalidate()
        self.building = was

    def sync_preset(self):
        gains = [b["g"] for b in self.s["bands"]]
        default_shape = all(abs(b["f"] - f) < 0.5 and abs(b["q"] - EQ_Q) < 0.01
                            for b, f in zip(self.s["bands"], EQ_FREQS))
        match = 0
        if default_shape:
            match = next((i + 1 for i, n in enumerate(PRESETS) if [float(x) for x in PRESETS[n]] == gains), 0)
        was, self.building = self.building, True
        self.presets.set_selected(match)
        self.building = was

    def fill_devices(self):
        was, self.building = self.building, True
        names = [n for n, _, _ in self.sinks]
        if self.s["target_sink"] and self.s["target_sink"] not in names:
            self.sinks.append((self.s["target_sink"], f"{self.s['target_sink']} (not connected)",
                               self.s["target_positions"]))
        labels = [f"{d} ({len(p)} ch)" if len(p) != 2 else d for _, d, p in self.sinks]
        self.device_row.set_model(Gtk.StringList.new(labels))
        for i, (n, _, _) in enumerate(self.sinks):
            if n == self.s["target_sink"]:
                self.device_row.set_selected(i)
        self.building = was

    def pick_initial_sink(self):
        names = [n for n, _, _ in self.sinks]
        cur = default_sink()
        if cur in names:
            return cur
        non_hdmi = [n for n in names if "hdmi" not in n.lower()]
        return (non_hdmi or names or [""])[0]

    def fill_profiles(self, select=None):
        was, self.building = self.building, True
        self.profiles = load_profiles()
        self.profile_names = sorted(self.profiles, key=str.casefold)
        self.profile_dd.set_model(Gtk.StringList.new(["None"] + self.profile_names))
        current = select if select is not None else self.s.get("profile")
        if current not in self.profile_names:
            self.s.pop("profile", None)
        self.profile_dd.set_selected(self.profile_names.index(current) + 1 if current in self.profile_names else 0)
        self.delete_btn.set_sensitive(current in self.profile_names)
        self.building = was

    # -- channels

    def build_channels(self):
        for row in self.channel_rows:
            self.channels_group.remove(row)
        self.channel_rows = []
        self.loaders = [l for l in self.loaders if not getattr(l, "channel_loader", False)]
        positions = self.s["target_positions"]
        self.setups = setup_presets(positions)
        was, self.building = self.building, True
        self.setup_dd.set_model(Gtk.StringList.new(["Setup…"] + list(self.setups)))
        self.setup_dd.set_selected(0)
        self.building = was
        for pos in positions:
            row = self.channel_row(pos)
            self.channels_group.add(row)
            self.channel_rows.append(row)

    def channel_row(self, pos):
        exp = Adw.ExpanderRow(title=CHANNEL_NAMES.get(pos, pos))

        def cfg():
            return channel_cfg(self.s, pos)

        def put(key):
            def _put(v):
                ch = self.s["channels"].setdefault(pos, {})
                ch[key] = v
                exp.set_subtitle(self.channel_summary(pos))
            return _put

        src = Adw.ComboRow(title="Source", model=Gtk.StringList.new([n for _, n in SOURCES]))

        def src_changed(row, _):
            if self.building:
                return
            put("src")(SOURCES[row.get_selected()][0])
            self.schedule_apply()

        src.connect("notify::selected", src_changed)
        exp.add_row(src)
        exp.add_row(self.slider("High-pass", "Cuts below this frequency (24 dB/oct)", FREQ_MIN, FREQ_MAX, 1,
                                lambda v: "Off" if v <= FREQ_MIN + 0.5 else fmt_hz(v),
                                get=lambda: cfg()["hp"], put=put("hp"), log=True))
        exp.add_row(self.slider("Low-pass", "Cuts above this frequency (24 dB/oct)", FREQ_MIN, FREQ_MAX, 1,
                                lambda v: "Off" if v >= FREQ_MAX - 0.5 else fmt_hz(v),
                                get=lambda: cfg()["lp"], put=put("lp"), log=True))
        exp.add_row(self.slider("Level", None, -24, 12, 0.5, lambda v: f"{v:+.1f} dB",
                                get=lambda: cfg()["db"], put=put("db")))
        exp.add_row(self.slider("Delay", "Time-align speakers at different distances", 0, 20, 0.05,
                                lambda v: f"{v:.2f} ms", get=lambda: cfg()["delay_ms"], put=put("delay_ms")))
        inv = Adw.SwitchRow(title="Invert polarity")

        def inv_changed(row, _):
            if self.building:
                return
            put("invert")(row.get_active())
            self.schedule_apply()

        inv.connect("notify::active", inv_changed)
        exp.add_row(inv)

        def load():
            c = cfg()
            src.set_selected([k for k, _ in SOURCES].index(c["src"]) if c["src"] in [k for k, _ in SOURCES] else 0)
            inv.set_active(bool(c["invert"]))
            exp.set_subtitle(self.channel_summary(pos))

        # the sliders above registered their own loaders; tag them all so a rebuild can drop them
        n_sliders = 4
        for l in self.loaders[-n_sliders:]:
            l.channel_loader = True
        load.channel_loader = True
        self.loaders.append(load)
        was, self.building = self.building, True
        for l in self.loaders[-(n_sliders + 1):]:
            l()
        self.building = was
        return exp

    def channel_summary(self, pos):
        c = channel_cfg(self.s, pos)
        parts = [dict(SOURCES)[c["src"]]]
        if c["hp"] > FREQ_MIN + 0.5:
            parts.append(f"HP {fmt_hz(c['hp'])}")
        if c["lp"] < FREQ_MAX - 0.5:
            parts.append(f"LP {fmt_hz(c['lp'])}")
        if c["db"]:
            parts.append(f"{c['db']:+.1f} dB")
        if c["delay_ms"]:
            parts.append(f"{c['delay_ms']:.2f} ms")
        if c["invert"]:
            parts.append("inverted")
        return " · ".join(parts)

    def on_setup(self, dd, _):
        idx = dd.get_selected()
        if self.building or idx in (0, Gtk.INVALID_LIST_POSITION):
            return
        name = list(self.setups)[idx - 1]
        self.s["channels"] = self.setups[name]()
        self.sync_ui()
        self.schedule_apply()
        self.toast(f"Applied “{name}”")
        was, self.building = self.building, True
        dd.set_selected(0)
        self.building = was

    # -- EQ

    def on_bands_changed(self, from_spin=False):
        self.eq.invalidate()
        if not from_spin:
            was, self.building = self.building, True
            self.on_band_selected(self.eq.selected)
            self.building = was
        self.sync_preset()
        self.schedule_apply()

    def on_band_selected(self, i):
        b = self.s["bands"][i]
        self.band_label.set_text(f"Band {i + 1}")
        was, self.building = self.building, True
        self.spin_f.set_value(b["f"])
        self.spin_g.set_value(b["g"])
        self.spin_q.set_value(b["q"])
        self.building = was

    def on_preset(self, dd, _):
        idx = dd.get_selected()
        if self.building or idx in (0, Gtk.INVALID_LIST_POSITION):
            return
        gains = PRESETS[list(PRESETS)[idx - 1]]
        self.s["bands"] = [{"f": float(f), "g": float(g), "q": EQ_Q} for f, g in zip(EQ_FREQS, gains)]
        self.on_bands_changed()

    def on_spectrum_toggled(self, btn):
        if self.building:
            return
        self.s["spectrum_on"] = btn.get_active()
        self.update_analyzer()
        self.schedule_apply()

    def update_analyzer(self):
        if self.s["spectrum_on"] and self.get_visible():
            self.analyzer.start(self.s["target_sink"])
        else:
            self.analyzer.stop()
        self.eq.queue_draw()

    def on_spectrum(self):
        self.eq.queue_draw()

    # -- other settings

    def on_spatial(self, row, _):
        for r in self.spatial_sliders:
            r.set_sensitive(row.get_active())
        if not self.building:
            self.s["spatial_on"] = row.get_active()
            self.schedule_apply()

    def apply_values(self, values):
        """Replace everything except device settings with `values`, then update UI and audio."""
        keep = {k: self.s[k] for k in DEVICE_KEYS}
        self.s = normalize({k: v for k, v in values.items() if k != "profile"})
        self.s.update(keep)
        self.sync_ui()
        self.schedule_apply()

    # -- profiles

    def on_profile_selected(self, dd, _):
        idx = dd.get_selected()
        if self.building or idx == Gtk.INVALID_LIST_POSITION:
            return
        if idx == 0:  # "None": keep the current sound, stop auto-saving into a profile
            self.s.pop("profile", None)
            self.delete_btn.set_sensitive(False)
            self.schedule_apply()
            return
        name = self.profile_names[idx - 1]
        self.apply_values(self.profiles[name])
        self.s["profile"] = name
        self.delete_btn.set_sensitive(True)
        self.toast(f"Loaded “{name}”")

    def on_save_profile(self, _btn):
        entry = Gtk.Entry(placeholder_text="Profile name", activates_default=True)
        dlg = Adw.AlertDialog(heading="Save as new profile",
                              body="Changes you make afterwards are saved into it automatically.")
        dlg.set_extra_child(entry)
        dlg.add_response("cancel", "Cancel")
        dlg.add_response("save", "Save")
        dlg.set_response_appearance("save", Adw.ResponseAppearance.SUGGESTED)
        dlg.set_default_response("save")
        dlg.set_close_response("cancel")
        entry.connect("changed", lambda e: dlg.set_response_enabled("save", bool(e.get_text().strip())))
        dlg.set_response_enabled("save", False)

        def done(d, response):
            name = entry.get_text().strip()
            if response != "save" or not name:
                return
            profiles = load_profiles()
            profiles[name] = profile_values(self.s)
            try:
                save_profiles(profiles)
            except OSError as e:
                self.toast(f"Could not save profile: {e}")
                return
            self.s["profile"] = name
            self.fill_profiles(select=name)
            self.schedule_apply()
            self.toast(f"Saved “{name}”")

        dlg.connect("response", done)
        dlg.present(self)

    def on_delete_profile(self, _btn):
        name = self.s.get("profile")
        if name not in self.profile_names:
            self.toast("Pick a profile to delete first")
            return
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
            self.s.pop("profile", None)
            self.fill_profiles()
            self.schedule_apply()
            self.toast(f"Deleted “{name}”")

        dlg.connect("response", done)
        dlg.present(self)

    def on_reset(self, _btn):
        dlg = Adw.AlertDialog(heading="Reset to defaults?",
                              body="Turns off every effect and resets all channels. "
                                   "Saved profiles and your output device are kept.")
        dlg.add_response("cancel", "Cancel")
        dlg.add_response("reset", "Reset")
        dlg.set_response_appearance("reset", Adw.ResponseAppearance.DESTRUCTIVE)
        dlg.set_close_response("cancel")

        def done(d, response):
            if response == "reset":
                self.apply_values({})
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
            name = self.s.get("profile")
            if name and name in self.profiles:  # auto-save edits into the active profile
                values = profile_values(self.s)
                if self.profiles[name] != values:
                    self.profiles[name] = values
                    save_profiles(self.profiles)
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
        elif self.needs_restart or not graph_matches(names, self.s["target_positions"]):
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
        name, _, positions = self.sinks[idx]
        if name == self.s["target_sink"]:
            return
        self.s["target_sink"] = name
        self.s["target_positions"] = positions
        save_settings(self.s)
        self.build_channels()
        self.needs_restart = True
        self.refresh_state()
        self.update_analyzer()

    def on_reload(self, _banner):
        save_settings(self.s)
        self.banner.set_revealed(False)
        self.analyzer.stop()
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
        self.update_analyzer()
        if self.node_id is None:
            self.toast("The filter didn't load. Check `journalctl --user -u pipewire`.")
        else:
            self.toast("Loaded. Restart your music player if it went quiet.")
        return GLib.SOURCE_REMOVE

    def on_default_toggled(self, row, _):
        if self.building:
            return
        run("pactl", "set-default-sink", NODE_NAME if row.get_active() else self.s["target_sink"])

    def on_close(self, _win):
        self.analyzer.stop()
        if self.pending:
            GLib.source_remove(self.pending)
            self.apply()
        return False

    def toast(self, msg):
        self.toasts.add_toast(Adw.Toast(title=msg, timeout=3))


class App(Adw.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID)

    def do_activate(self):
        win = self.props.active_window or Window(self)
        win.present()
        win.update_analyzer()


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

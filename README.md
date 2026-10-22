# Dolbro™ Speaker Tuner

**Get the most out of your shitty laptop speakers, or your 5.1 system.**

Speaker Tuner is a system-wide EQ, crossover and speaker tuner for Linux
desktops running PipeWire. It adds a virtual output, **Speaker Tuner**, in
front of any sound device, from a laptop's built-in speakers to a stereo pair
with a sub or a full 7.1 setup, and every app plays through it.

<img src="data/screenshots/main.png" alt="Speaker Tuner window">

<img src="data/screenshots/spectrum.gif" alt="Shaping the EQ curve over the live output spectrum">

## Features

- **An EQ you can draw:** sweep across the graph in either direction to paint
  the curve, or drag individual points. The curve passes through your points
  (the app works out the filter gains for you), and you can scroll to make a
  band wider or narrower or type exact frequency, gain and width values. A
  **live spectrum** of what's playing is drawn behind the curve.
- **Per-channel routing and crossovers for any layout** (2.0, 2.1, 4.0, 5.1,
  7.1, …). For each speaker channel you set:
  - the source: same channel, left, right, mono, all channels (for a sub) or off
  - high-pass and low-pass crossover filters (Linkwitz-Riley, 24 dB/oct)
  - level, delay (for time alignment) and polarity
- **One-click channel setups:** low cut for small speakers, a left-bass /
  right-treble split for laptops, stereo to all speakers, and 80 Hz bass
  management for systems with a subwoofer.
- **Loudness:** up to +20 dB of boost into a look-ahead limiter (ZaMaximX2),
  plus optional **overdrive** for when you want it louder than clean allows.
- **3D:** stereo width plus crosstalk cancellation in the style of
  Ambiophonics/RACE, which spreads sound wider than closely spaced speakers
  such as a laptop's.
- **Presets:** a list at the top of the window. Click one to load it, or save the
  current sound as a new one. Changes save into the active preset as you go.

## Why not Easy Effects, JamesDSP or similar?

Those are great, flexible tools. Speaker Tuner trades their flexibility for
being built into the audio system and focused on speakers:

- **Nothing to keep running.** The processing is a PipeWire `filter-chain`
  loaded by PipeWire itself. The app is just a settings window: close it and
  your sound stays tuned, from login onward, with no background service or
  autostart entry.
- **System-level and multichannel.** It sits in front of one device as a
  proper N-channel sink, so 5.1 content stays 5.1, and you get real per-channel
  crossovers, delays and bass management, not just a stereo effects chain.
- **Live changes without dropouts.** The filter layout is fixed, so moving a
  slider updates the running filter (`pw-cli set-param`) instead of rebuilding
  a pipeline.
- **Speaker-first defaults.** Low cut, limiter, overdrive, 3D and crossovers
  are the controls that matter for small or multi-way speakers, all on one
  screen.
- **Tiny and transparent.** One Python file, no compiled code, and the whole
  DSP setup is a readable config file in
  `~/.config/pipewire/pipewire.conf.d/speaker-tuner.conf`. Uninstalling
  removes it.

If you want convolution, plugin chains, per-app effects or microphone
processing, Easy Effects is the better tool.

## Requirements

- PipeWire with `pipewire-pulse` and WirePlumber (the default on most current
  distros), plus `pw-cli`, `pw-dump`, `pw-record` and `pactl`.
- Python 3 with GObject introspection, GTK 4 (4.10+) and libadwaita 1.5 or
  newer.
- The **ZaMaximX2** LV2 plugin from [zam-plugins](https://github.com/zamaudio/zam-plugins).
- PipeWire's **LV2 support for filter-chain**. Since PipeWire 1.4 some distros
  package it separately.

| Distro | Packages |
|---|---|
| Fedora | `python3-gobject gtk4 libadwaita lv2-zam-plugins pipewire-module-filter-chain-lv2` |
| Debian / Ubuntu | `python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 zam-plugins` |
| Arch | `python-gobject gtk4 libadwaita zam-plugins-lv2` |

Package names change between releases, so check your distro if one isn't
found. The app shows a banner naming anything that's missing.

## Install

```sh
git clone https://github.com/pjamessteven/dolbro-speaker-tuner.git
cd dolbro-speaker-tuner
./install.sh
```

This installs for your user only, with no root needed. Open **Speaker Tuner**,
pick your output device, and click **Load** in the banner. Audio restarts
once to load the filter. Changing to a device with a different channel layout
needs one more restart, which the app offers.

To uninstall:

```sh
./install.sh --uninstall
```

That removes the app and the PipeWire filter. Saved settings and profiles stay
in `~/.config/speaker-tuner/` until you delete them.

## How it works

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

The graph's layout depends only on the device's channels. Everything else is
a parameter, and turning a feature off sets it to a neutral value, such as
0 dB or a filter moved outside the audible range.

The 3D effect is RACE unrolled to two terms:
`out = own − g·D(other) + g²·D₂(own)`, band-limited to 250 Hz–5 kHz. PipeWire's
filter graphs can't contain feedback loops, so it isn't fully recursive.

The spectrum is read with `pw-record` from the device you're tuning, and only
while the window is open.

## Tips

- **Laptops:** apply the *Small speakers* setup (120 Hz low cut) and add
  6–10 dB of boost. That's roughly what Windows enhancements such as Dolby do
  on most laptops.
- **Subwoofer:** apply *Bass management (80 Hz)*, then fine-tune the
  subwoofer's level and delay until bass sounds even at your seat.
- **3D:** sit centred, set 3D amount to about 70%, then move 3D delay until the
  sound spreads wider than the speakers.
- **Overdrive** sends clipped audio to your speakers. Use it sparingly on small
  drivers.

## License

MIT. See [LICENSE](LICENSE).

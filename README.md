<p align="center">
  <img src="data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Sound Tuner icon">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>Get the most out of your shitty laptop speakers, or finely tune your audiophilic soundsystem.</b></p>

<!-- languages -->
<p align="center"><sub><b>English</b> · <a href="translations/README.ar.md">العربية</a> · <a href="translations/README.bn.md">বাংলা</a> · <a href="translations/README.cs.md">Čeština</a> · <a href="translations/README.da.md">Dansk</a> · <a href="translations/README.de.md">Deutsch</a> · <a href="translations/README.el.md">Ελληνικά</a> · <a href="translations/README.es.md">Español</a> · <a href="translations/README.fa.md">فارسی</a> · <a href="translations/README.fi.md">Suomi</a> · <a href="translations/README.fr.md">Français</a> · <a href="translations/README.he.md">עברית</a> · <a href="translations/README.hi.md">हिन्दी</a> · <a href="translations/README.hu.md">Magyar</a> · <a href="translations/README.id.md">Bahasa Indonesia</a> · <a href="translations/README.it.md">Italiano</a> · <a href="translations/README.ja.md">日本語</a> · <a href="translations/README.ko.md">한국어</a> · <a href="translations/README.nb.md">Norsk bokmål</a> · <a href="translations/README.nl.md">Nederlands</a> · <a href="translations/README.pl.md">Polski</a> · <a href="translations/README.pt_BR.md">Português (Brasil)</a> · <a href="translations/README.ro.md">Română</a> · <a href="translations/README.ru.md">Русский</a> · <a href="translations/README.sv.md">Svenska</a> · <a href="translations/README.th.md">ไทย</a> · <a href="translations/README.tr.md">Türkçe</a> · <a href="translations/README.uk.md">Українська</a> · <a href="translations/README.vi.md">Tiếng Việt</a> · <a href="translations/README.zh_CN.md">简体中文</a> · <a href="translations/README.zh_TW.md">繁體中文</a></sub></p>
<!-- /languages -->


Sound Tuner is a system-wide EQ, crossover and speaker tuner for Linux
devices running PipeWire. It adds a virtual output, **Sound Tuner**, in
front of any sound device, from a laptop's built-in speakers to a stereo pair
with a sub or a full 7.1 setup, and every app plays through it.

<img src="data/screenshots/main.webp" alt="Sound Tuner: shaping the EQ curve over the live output spectrum">

On phones and narrow windows the settings move into a slide-out panel:

<img src="data/screenshots/mobile.png" alt="Sound Tuner on a phone: equalizer and settings panel" width="420">

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
  plus optional **overdrive** for when you want it louder than clean allows,
  and a switch to let GNOME's volume slider go past 100%.
- **3D:** stereo width plus crosstalk cancellation in the style of
  Ambiophonics/RACE, which spreads sound wider than closely spaced speakers
  such as a laptop's.
- **Presets:** a list at the top of the window. Click one to load it, or save the
  current sound as a new one. Changes save into the active preset as you go.

## How it compares to Easy Effects, JamesDSP, etc.

- **Modern, easy UI:** one clean screen. Draw the EQ curve, set loudness and
  3D, and pick a preset, without digging through plugin panels. It's
  mobile-friendly too, adapting from phones up to wide desktop screens.
- **Nothing to keep running:** processing runs inside PipeWire itself. Close
  the app and your sound stays tuned from login onward.
- **True multichannel:** 5.1 stays 5.1, with per-channel crossovers, delays
  and bass management.
- **No dropouts:** changes apply to the running filter live.
- **Tiny:** one Python file and one readable PipeWire config.
- **Hard to clip:** the chain always ends in a look-ahead limiter. See below.

### Why other EQ apps can sound distorted

EQ and bass boosts can push the signal past 0 dBFS, the most the sound chip
can play, and it clips unless a limiter catches it. Sound Tuner always ends
with a look-ahead limiter set below 0 dBFS, so boosts get louder instead of
crackling. (Overdrive deliberately bypasses this.) Its processing also runs
inside PipeWire itself rather than in a separate app process, so there's one
less program that has to keep up in real time.

## Install

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

The script installs any missing dependencies with your package manager (dnf,
apt or pacman). It shows the exact command and asks before using `sudo`. It
then installs the app for your user only.

Open **Sound Tuner**, pick your output device, and click **Load** in the
banner. Audio restarts once to load the filter.

| Option | What it does |
|---|---|
| `--yes` | install dependencies without asking |
| `--no-deps` | skip dependencies, install the app only |
| `--dry-run` | show what would be installed, change nothing |
| `--uninstall` | remove the app and the PipeWire filter (keeps your presets) |

### Dependencies

Installed for you by `install.sh`:

- PipeWire tools: `pw-cli`, `pw-dump`, `pw-record` and `pactl`
- Python 3 with GTK 4 and libadwaita 1.5+
- The ZaMaximX2 limiter from [zam-plugins](https://github.com/zamaudio/zam-plugins)
- PipeWire's LV2 support for filter-chain

You need a Linux device already running PipeWire with WirePlumber, which is the
default on current Fedora, Ubuntu, Debian and Arch. The Fedora package names
are tested; on other distros, if a package name has changed, the script tells
you what's missing so you can install it yourself.

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

## Translations

The app and this README are available in 30 languages. The app follows your
system language automatically. Translations live in `locale/<language>.json`
(app) and `translations/README.<language>.md` (docs). Corrections from native
speakers are very welcome: edit the file and open a pull request.

## License

MIT. See [LICENSE](LICENSE).

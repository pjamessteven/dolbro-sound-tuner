#!/bin/sh
# Install Speaker Tuner for the current user (no root needed).
#   ./install.sh              install or update
#   ./install.sh --uninstall  remove the app and its PipeWire filter (keeps saved profiles)
set -e
APP_ID=io.github.pjamessteven.SpeakerTuner
SRC="$(cd "$(dirname "$0")" && pwd)"
SHARE="${XDG_DATA_HOME:-$HOME/.local/share}"
CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}"
BIN="$HOME/.local/bin"

if [ "$1" = "--uninstall" ]; then
    rm -f "$BIN/speaker-tuner" "$SHARE/applications/$APP_ID.desktop"
    rm -rf "$SHARE/speaker-tuner"
    if [ -f "$CONFIG/pipewire/pipewire.conf.d/speaker-tuner.conf" ]; then
        rm -f "$CONFIG/pipewire/pipewire.conf.d/speaker-tuner.conf"
        systemctl --user restart pipewire pipewire-pulse wireplumber 2>/dev/null || true
    fi
    command -v update-desktop-database >/dev/null && update-desktop-database "$SHARE/applications" || true
    echo "Speaker Tuner removed. Saved settings and profiles are in $CONFIG/speaker-tuner (delete it to remove them)."
    exit 0
fi

python3 -c 'import gi; gi.require_version("Gtk", "4.0"); gi.require_version("Adw", "1"); from gi.repository import Adw; assert (Adw.get_major_version(), Adw.get_minor_version()) >= (1, 5)' 2>/dev/null || {
    echo "Speaker Tuner needs Python GObject with GTK 4 and libadwaita 1.5 or newer." >&2
    exit 1
}

install -Dm755 "$SRC/speaker_tuner.py" "$SHARE/speaker-tuner/speaker_tuner.py"
mkdir -p "$BIN"
cat > "$BIN/speaker-tuner" <<WRAP
#!/bin/sh
exec python3 "$SHARE/speaker-tuner/speaker_tuner.py" "\$@"
WRAP
chmod 755 "$BIN/speaker-tuner"
mkdir -p "$SHARE/applications"
sed "s|^Exec=.*|Exec=$BIN/speaker-tuner|" "$SRC/data/$APP_ID.desktop" > "$SHARE/applications/$APP_ID.desktop.tmp"
mv "$SHARE/applications/$APP_ID.desktop.tmp" "$SHARE/applications/$APP_ID.desktop"
command -v update-desktop-database >/dev/null && update-desktop-database "$SHARE/applications" || true

echo "Installed. Open \"Speaker Tuner\" from your app grid, or run: speaker-tuner"
missing=$(python3 -c "
import importlib.util, sys
spec = importlib.util.spec_from_file_location('st', '$SHARE/speaker-tuner/speaker_tuner.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(', '.join(m.missing_deps()))" 2>/dev/null || true)
if [ -n "$missing" ]; then
    echo
    echo "Still missing: $missing"
    echo "See \"Requirements\" in README.md for the package names on your distro."
fi

#!/bin/sh
# Install Sound Tuner for the current user.
#   ./install.sh              install dependencies (asks first, needs sudo) and the app
#   ./install.sh --yes        same, without asking before installing packages
#   ./install.sh --no-deps    install the app only
#   ./install.sh --dry-run    show which packages would be installed, change nothing
#   ./install.sh --uninstall  remove the app and its PipeWire filter (keeps saved profiles)
set -e
APP_ID=io.github.pjamessteven.SpeakerTuner
SRC="$(cd "$(dirname "$0")" && pwd)"
SHARE="${XDG_DATA_HOME:-$HOME/.local/share}"
CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}"
BIN="$HOME/.local/bin"

ASSUME_YES=0 NO_DEPS=0 DRY_RUN=0
for arg in "$@"; do
    case "$arg" in
        --uninstall) MODE=uninstall ;;
        --yes|-y) ASSUME_YES=1 ;;
        --no-deps) NO_DEPS=1 ;;
        --dry-run) DRY_RUN=1 ;;
        *) echo "Unknown option: $arg" >&2; exit 2 ;;
    esac
done

if [ "$MODE" = "uninstall" ]; then
    rm -f "$BIN/speaker-tuner" "$SHARE/applications/$APP_ID.desktop" "$SHARE/icons/hicolor/scalable/apps/$APP_ID.svg"
    rm -rf "$SHARE/speaker-tuner"
    if [ -f "$CONFIG/pipewire/pipewire.conf.d/speaker-tuner.conf" ]; then
        rm -f "$CONFIG/pipewire/pipewire.conf.d/speaker-tuner.conf"
        systemctl --user restart pipewire pipewire-pulse wireplumber 2>/dev/null || true
    fi
    command -v update-desktop-database >/dev/null && update-desktop-database "$SHARE/applications" || true
    echo "Sound Tuner removed. Saved settings and profiles are in $CONFIG/speaker-tuner (delete it to remove them)."
    exit 0
fi

# ---------------------------------------------------------------- dependencies

have_ui() {
    python3 -c 'import gi; gi.require_version("Gtk", "4.0"); gi.require_version("Adw", "1"); from gi.repository import Adw; assert (Adw.get_major_version(), Adw.get_minor_version()) >= (1, 5)' 2>/dev/null
}

have_limiter() {
    for d in ${LV2_PATH:+$(echo "$LV2_PATH" | tr ':' ' ')} "$HOME/.lv2" /usr/local/lib/lv2 /usr/local/lib64/lv2 \
             /usr/lib/lv2 /usr/lib64/lv2 /usr/lib/x86_64-linux-gnu/lv2 /usr/lib/aarch64-linux-gnu/lv2; do
        [ -d "$d/ZaMaximX2.lv2" ] && return 0
    done
    return 1
}

have_lv2_filter() {
    # PipeWire >= 1.4 ships filter-chain LV2 support as a separate plugin; older versions have it built in.
    found_dir=0
    for d in /usr/lib64/spa-0.2 /usr/lib/spa-0.2 /usr/lib/x86_64-linux-gnu/spa-0.2 /usr/lib/aarch64-linux-gnu/spa-0.2 \
             /usr/local/lib/spa-0.2 /usr/local/lib64/spa-0.2; do
        if [ -d "$d/filter-graph" ]; then
            found_dir=1
            [ -e "$d/filter-graph/libspa-filter-graph-plugin-lv2.so" ] && return 0
        fi
    done
    [ "$found_dir" = 0 ]
}

have_pw_tools() { command -v pw-cli >/dev/null && command -v pw-dump >/dev/null && command -v pw-record >/dev/null; }
have_pactl() { command -v pactl >/dev/null; }

if command -v dnf >/dev/null; then
    PM=dnf
elif command -v apt-get >/dev/null; then
    PM=apt
elif command -v pacman >/dev/null; then
    PM=pacman
else
    PM=
fi

# Packages for each missing piece, per package manager.
pkgs_for() {
    case "$PM:$1" in
        dnf:ui) echo "python3-gobject gtk4 libadwaita" ;;
        dnf:limiter) echo "lv2-zam-plugins" ;;
        dnf:lv2filter) echo "pipewire-module-filter-chain-lv2" ;;
        dnf:pwtools) echo "pipewire-utils" ;;
        dnf:pactl) echo "pulseaudio-utils" ;;
        apt:ui) echo "python3-gi gir1.2-gtk-4.0 gir1.2-adw-1" ;;
        apt:limiter) echo "zam-plugins" ;;
        apt:lv2filter) echo "libspa-0.2-modules" ;;
        apt:pwtools) echo "pipewire-bin" ;;
        apt:pactl) echo "pulseaudio-utils" ;;
        pacman:ui) echo "python-gobject gtk4 libadwaita" ;;
        pacman:limiter) echo "zam-plugins-lv2" ;;
        pacman:lv2filter) echo "pipewire" ;;
        pacman:pwtools) echo "pipewire" ;;
        pacman:pactl) echo "libpulse" ;;
    esac
}

missing=""
have_ui || missing="$missing ui"
have_limiter || missing="$missing limiter"
have_lv2_filter || missing="$missing lv2filter"
have_pw_tools || missing="$missing pwtools"
have_pactl || missing="$missing pactl"

describe() {
    case "$1" in
        ui) echo "Python GTK 4 + libadwaita" ;;
        limiter) echo "ZaMaximX2 limiter (zam-plugins)" ;;
        lv2filter) echo "PipeWire LV2 filter support" ;;
        pwtools) echo "PipeWire tools (pw-cli, pw-dump, pw-record)" ;;
        pactl) echo "pactl" ;;
    esac
}

if [ -n "$missing" ] && [ "$NO_DEPS" = 0 ]; then
    echo "Missing:"
    for m in $missing; do echo "  - $(describe "$m")"; done
    if [ -z "$PM" ]; then
        echo "Couldn't find dnf, apt or pacman. Install the above with your package manager, then run this again." >&2
        exit 1
    fi
    pkgs=$(for m in $missing; do pkgs_for "$m"; done | tr ' ' '\n' | sort -u | tr '\n' ' ')
    case "$PM" in
        dnf) cmd="sudo dnf install -y $pkgs" ;;
        apt) cmd="sudo apt-get install -y $pkgs" ;;
        pacman) cmd="sudo pacman -S --needed --noconfirm $pkgs" ;;
    esac
    echo
    echo "Will run: $cmd"
    if [ "$DRY_RUN" = 1 ]; then
        echo "(dry run: nothing installed)"
        exit 0
    fi
    if [ "$ASSUME_YES" = 0 ]; then
        if [ -t 0 ]; then
            printf "Install these packages now? [Y/n] "
            read -r answer
            case "$answer" in [nN]*) echo "Skipped. Run with --no-deps to install the app anyway." >&2; exit 1 ;; esac
        else
            echo "Not running interactively: re-run with --yes to install them, or --no-deps to skip." >&2
            exit 1
        fi
    fi
    if ! sh -c "$cmd"; then
        echo >&2
        echo "Package install failed. Package names differ between distro releases;" >&2
        echo "install the missing pieces listed above yourself, then run ./install.sh --no-deps" >&2
        exit 1
    fi
elif [ "$DRY_RUN" = 1 ]; then
    echo "All dependencies are installed."
    exit 0
fi

if ! have_ui; then
    echo "Sound Tuner needs Python GObject with GTK 4 and libadwaita 1.5 or newer." >&2
    exit 1
fi

# ---------------------------------------------------------------- app

install -Dm755 "$SRC/speaker_tuner.py" "$SHARE/speaker-tuner/speaker_tuner.py"
mkdir -p "$BIN"
cat > "$BIN/speaker-tuner" <<WRAP
#!/bin/sh
exec python3 "$SHARE/speaker-tuner/speaker_tuner.py" "\$@"
WRAP
chmod 755 "$BIN/speaker-tuner"
install -Dm644 "$SRC/data/icons/$APP_ID.svg" "$SHARE/icons/hicolor/scalable/apps/$APP_ID.svg"
command -v gtk-update-icon-cache >/dev/null && gtk-update-icon-cache -q -t "$SHARE/icons/hicolor" 2>/dev/null || true
mkdir -p "$SHARE/applications"
sed "s|^Exec=.*|Exec=$BIN/speaker-tuner|" "$SRC/data/$APP_ID.desktop" > "$SHARE/applications/$APP_ID.desktop.tmp"
mv "$SHARE/applications/$APP_ID.desktop.tmp" "$SHARE/applications/$APP_ID.desktop"
command -v update-desktop-database >/dev/null && update-desktop-database "$SHARE/applications" || true

echo "Installed. Open \"Sound Tuner\" from your app grid, or run: speaker-tuner"

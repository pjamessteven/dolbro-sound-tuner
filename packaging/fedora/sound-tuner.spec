Name:           sound-tuner
Version:        0.4.0
Release:        1%{?dist}
Summary:        System-wide EQ, crossovers and loudness for your speakers

License:        MIT
URL:            https://github.com/pjamessteven/dolbro-sound-tuner
Source0:        %{url}/archive/v%{version}/dolbro-sound-tuner-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  desktop-file-utils
BuildRequires:  appstream

Requires:       python3
Requires:       python3-gobject
Requires:       gtk4
Requires:       libadwaita
Requires:       pipewire
Requires:       pipewire-utils
Requires:       pulseaudio-utils
Requires:       pipewire-module-filter-chain-lv2
Requires:       lv2-zam-plugins
Requires:       hicolor-icon-theme

%description
Sound Tuner adds a tuned output in front of any PipeWire sound device: an
equalizer you can draw over a live spectrum, boost with a look-ahead limiter,
3D virtual surround, and per-channel routing, crossovers and bass management
for 2.0 up to 7.1. Processing runs inside PipeWire itself.

%prep
%autosetup -n dolbro-sound-tuner-%{version}

%build
python3 -m py_compile speaker_tuner.py

%install
%make_install PREFIX=%{_prefix}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/io.github.pjamessteven.SpeakerTuner.desktop
appstreamcli validate --no-net %{buildroot}%{_metainfodir}/io.github.pjamessteven.SpeakerTuner.metainfo.xml

%files
%license %{_datadir}/licenses/sound-tuner/LICENSE
%doc README.md
%{_bindir}/sound-tuner
%{_datadir}/sound-tuner/
%{_datadir}/applications/io.github.pjamessteven.SpeakerTuner.desktop
%{_datadir}/icons/hicolor/scalable/apps/io.github.pjamessteven.SpeakerTuner.svg
%{_metainfodir}/io.github.pjamessteven.SpeakerTuner.metainfo.xml

%changelog
* Fri Oct 23 2026 pjamessteven <peter@detrans.ai> - 0.4.0-1
- First packaged release

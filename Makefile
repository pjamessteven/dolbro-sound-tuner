# System-wide install, used by distro packages (RPM, AUR):
#   make install PREFIX=/usr DESTDIR=/path/to/buildroot
# For a per-user install without root, use ./install.sh instead.

PREFIX ?= /usr/local
DESTDIR ?=
APP_ID = io.github.pjamessteven.SpeakerTuner
DATADIR = $(DESTDIR)$(PREFIX)/share
APPDIR = $(DATADIR)/sound-tuner

.PHONY: install uninstall check

install:
	install -Dm644 speaker_tuner.py $(APPDIR)/speaker_tuner.py
	install -d $(APPDIR)/locale
	for f in locale/*.json; do \
		case "$$f" in */strings.json) ;; *) install -m644 "$$f" $(APPDIR)/locale/ ;; esac; \
	done
	install -d $(DESTDIR)$(PREFIX)/bin
	printf '#!/bin/sh\nexec python3 %s/share/sound-tuner/speaker_tuner.py "$$@"\n' "$(PREFIX)" > $(DESTDIR)$(PREFIX)/bin/sound-tuner
	chmod 755 $(DESTDIR)$(PREFIX)/bin/sound-tuner
	install -d $(DATADIR)/applications
	sed 's|^Exec=.*|Exec=sound-tuner|' data/$(APP_ID).desktop > $(DATADIR)/applications/$(APP_ID).desktop
	install -Dm644 data/icons/$(APP_ID).svg $(DATADIR)/icons/hicolor/scalable/apps/$(APP_ID).svg
	install -Dm644 data/$(APP_ID).metainfo.xml $(DATADIR)/metainfo/$(APP_ID).metainfo.xml
	install -Dm644 LICENSE $(DATADIR)/licenses/sound-tuner/LICENSE

uninstall:
	rm -rf $(APPDIR)
	rm -f $(DESTDIR)$(PREFIX)/bin/sound-tuner \
		$(DATADIR)/applications/$(APP_ID).desktop \
		$(DATADIR)/icons/hicolor/scalable/apps/$(APP_ID).svg \
		$(DATADIR)/metainfo/$(APP_ID).metainfo.xml \
		$(DATADIR)/licenses/sound-tuner/LICENSE

check:
	python3 -m py_compile speaker_tuner.py
	desktop-file-validate data/$(APP_ID).desktop
	appstreamcli validate --no-net data/$(APP_ID).metainfo.xml

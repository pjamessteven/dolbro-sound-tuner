<p align="center">
  <img src="../data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Sound-Tuner-Symbol">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>Hol das Letzte aus deinen miesen Laptop-Lautsprechern raus – oder stimm deine Audiophilen-Anlage bis ins Detail ab.</b></p>

<!-- languages -->
<p align="center"><sub><a href="../README.md">English</a> · <a href="README.ar.md">العربية</a> · <a href="README.bn.md">বাংলা</a> · <a href="README.cs.md">Čeština</a> · <a href="README.da.md">Dansk</a> · <b>Deutsch</b> · <a href="README.el.md">Ελληνικά</a> · <a href="README.es.md">Español</a> · <a href="README.fa.md">فارسی</a> · <a href="README.fi.md">Suomi</a> · <a href="README.fr.md">Français</a> · <a href="README.he.md">עברית</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.hu.md">Magyar</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.it.md">Italiano</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.nb.md">Norsk bokmål</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.pl.md">Polski</a> · <a href="README.pt_BR.md">Português (Brasil)</a> · <a href="README.ro.md">Română</a> · <a href="README.ru.md">Русский</a> · <a href="README.sv.md">Svenska</a> · <a href="README.th.md">ไทย</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.uk.md">Українська</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.zh_CN.md">简体中文</a> · <a href="README.zh_TW.md">繁體中文</a></sub></p>
<!-- /languages -->


Sound Tuner ist ein systemweiter EQ, eine Frequenzweiche und ein
Lautsprecher-Tuner für Linux-Desktops mit PipeWire. Er fügt eine virtuelle
Ausgabe, **Sound Tuner**, vor jedem beliebigen Audiogerät ein – von den
eingebauten Lautsprechern eines Laptops bis zu einem Stereopaar mit Sub oder
einem kompletten 7.1-System –, und alle Apps spielen darüber ab.

<img src="../data/screenshots/main.webp" alt="Sound Tuner: Formen der EQ-Kurve über dem Live-Spektrum der Ausgabe">

Auf Smartphones und in schmalen Fenstern wandern die Einstellungen in ein ausklappbares Seitenfeld:

<img src="../data/screenshots/mobile.png" alt="Sound Tuner auf einem Smartphone: Equalizer und Einstellungsfeld" width="420">

## Funktionen

- **Ein EQ, den du zeichnen kannst:** Fahr in beliebiger Richtung über den
  Graphen, um die Kurve zu malen, oder zieh einzelne Punkte. Die Kurve verläuft
  durch deine Punkte (die App berechnet die Filterverstärkungen für dich), und
  du kannst scrollen, um ein Band breiter oder schmaler zu machen, oder exakte
  Werte für Frequenz, Verstärkung und Breite eingeben. Hinter der Kurve wird
  ein **Live-Spektrum** dessen angezeigt, was gerade läuft.
- **Routing und Frequenzweichen pro Kanal für jede Konfiguration** (2.0, 2.1,
  4.0, 5.1, 7.1, …). Für jeden Lautsprecherkanal legst du fest:
  - die Quelle: gleicher Kanal, links, rechts, mono, alle Kanäle (für einen Sub) oder aus
  - Hochpass- und Tiefpass-Weichenfilter (Linkwitz-Riley, 24 dB/Okt.)
  - Pegel, Verzögerung (für die Laufzeitkorrektur) und Polarität
- **Kanalkonfigurationen mit einem Klick:** Low-Cut für kleine Lautsprecher,
  eine Aufteilung links Bass / rechts Höhen für Laptops, Stereo auf alle
  Lautsprecher und 80-Hz-Bassmanagement für Systeme mit Subwoofer.
- **Lautheit:** bis zu +20 dB Anhebung in einen Look-ahead-Limiter
  (ZaMaximX2), dazu optionaler **Overdrive**, wenn es lauter sein soll, als es
  sauber geht, und ein Schalter, mit dem GNOMEs Lautstärkeregler über 100 %
  hinausgehen darf.
- **3D:** Stereobreite plus Übersprechunterdrückung im Stil von
  Ambiophonics/RACE, die den Klang breiter auffächert als eng beieinander
  stehende Lautsprecher, etwa die eines Laptops.
- **Voreinstellungen:** eine Liste oben im Fenster. Klick auf eine, um sie zu
  laden, oder speichere den aktuellen Klang als neue. Änderungen werden laufend
  in der aktiven Voreinstellung gespeichert.

## Im Vergleich zu Easy Effects, JamesDSP usw.

- **Moderne, einfache Oberfläche:** ein aufgeräumter Bildschirm. EQ-Kurve
  zeichnen, Lautheit und 3D einstellen und eine Voreinstellung wählen, ohne
  sich durch Plugin-Panels zu wühlen. Sie ist auch mobiltauglich und passt
  sich vom Smartphone bis zum breiten Desktop-Bildschirm an.
- **Nichts muss weiterlaufen:** Die Verarbeitung läuft direkt in PipeWire.
  Schließ die App, und dein Klang bleibt ab der Anmeldung abgestimmt.
- **Echtes Mehrkanal:** 5.1 bleibt 5.1, mit Frequenzweichen, Verzögerungen
  und Bassmanagement pro Kanal.
- **Keine Aussetzer:** Änderungen werden live auf den laufenden Filter
  angewendet.
- **Winzig:** eine Python-Datei und eine gut lesbare PipeWire-Konfiguration.
- **Schwer zu übersteuern:** Die Kette endet immer in einem
  Look-ahead-Limiter. Siehe unten.

### Warum andere EQ-Apps verzerrt klingen können

EQ und Bass-Boosts können das Signal über 0 dBFS treiben, das Maximum, das der
Soundchip wiedergeben kann, und dann clippt es, sofern kein Limiter eingreift.
Sound Tuner endet immer mit einem Look-ahead-Limiter, der unter 0 dBFS
eingestellt ist, sodass Anhebungen lauter werden statt zu knistern.
(Overdrive umgeht das absichtlich.) Außerdem läuft die Verarbeitung direkt in
PipeWire statt in einem separaten App-Prozess, es gibt also ein Programm
weniger, das in Echtzeit mithalten muss.

## Installation

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

Das Skript installiert fehlende Abhängigkeiten mit deinem Paketmanager (dnf,
apt oder pacman). Es zeigt den genauen Befehl an und fragt nach, bevor es
`sudo` verwendet. Danach installiert es die App nur für deinen Benutzer.

Öffne **Sound Tuner**, wähle dein Ausgabegerät und klick im Banner auf
**Laden**. Das Audio startet einmal neu, um den Filter zu laden.

| Option | Funktion |
|---|---|
| `--yes` | Abhängigkeiten ohne Nachfrage installieren |
| `--no-deps` | Abhängigkeiten überspringen, nur die App installieren |
| `--dry-run` | anzeigen, was installiert würde, nichts ändern |
| `--uninstall` | App und PipeWire-Filter entfernen (deine Voreinstellungen bleiben erhalten) |

### Abhängigkeiten

Werden von `install.sh` für dich installiert:

- PipeWire-Werkzeuge: `pw-cli`, `pw-dump`, `pw-record` und `pactl`
- Python 3 mit GTK 4 und libadwaita 1.5+
- Der ZaMaximX2-Limiter aus [zam-plugins](https://github.com/zamaudio/zam-plugins)
- PipeWires LV2-Unterstützung für filter-chain

Du brauchst einen Desktop, auf dem bereits PipeWire mit WirePlumber läuft –
das ist der Standard bei aktuellen Versionen von Fedora, Ubuntu, Debian und
Arch. Die Fedora-Paketnamen sind getestet; falls sich auf anderen
Distributionen ein Paketname geändert hat, sagt dir das Skript, was fehlt,
damit du es selbst installieren kannst.

## Funktionsweise

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

Der Aufbau des Graphen hängt nur von den Kanälen des Geräts ab. Alles andere
ist ein Parameter, und das Ausschalten einer Funktion setzt ihn auf einen
neutralen Wert, etwa 0 dB oder einen Filter außerhalb des hörbaren Bereichs.

Der 3D-Effekt ist RACE, auf zwei Terme ausgerollt:
`out = own − g·D(other) + g²·D₂(own)`, bandbegrenzt auf 250 Hz–5 kHz. Die
Filtergraphen von PipeWire können keine Rückkopplungsschleifen enthalten,
daher ist er nicht vollständig rekursiv.

Das Spektrum wird mit `pw-record` vom Gerät gelesen, das du gerade abstimmst,
und nur, solange das Fenster geöffnet ist.

## Tipps

- **Laptops:** Wende die Konfiguration *Kleine Lautsprecher* an (Low-Cut bei
  120 Hz) und gib 6–10 dB Anhebung dazu. Das entspricht ungefähr dem, was
  Windows-Klangverbesserungen wie Dolby auf den meisten Laptops machen.
- **Subwoofer:** Wende *Bassmanagement (80 Hz)* an und justiere dann Pegel und
  Verzögerung des Subwoofers, bis der Bass an deinem Platz gleichmäßig klingt.
- **3D:** Setz dich mittig, stell die 3D-Stärke auf etwa 70 % und verändere
  dann die 3D-Verzögerung, bis sich der Klang breiter als die Lautsprecher
  auffächert.
- **Overdrive** schickt übersteuertes Audio an deine Lautsprecher. Bei kleinen
  Treibern sparsam einsetzen.

## Lizenz

MIT. Siehe [LICENSE](../LICENSE).

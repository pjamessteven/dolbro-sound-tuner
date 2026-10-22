<p align="center">
  <img src="../data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Pictogram van Sound Tuner">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>Haal alles uit je waardeloze laptopspeakers, of stem je audiofiele geluidsinstallatie tot in de puntjes af.</b></p>

<!-- languages -->
<p align="center"><sub><a href="../README.md">English</a> · <a href="README.ar.md">العربية</a> · <a href="README.bn.md">বাংলা</a> · <a href="README.cs.md">Čeština</a> · <a href="README.da.md">Dansk</a> · <a href="README.de.md">Deutsch</a> · <a href="README.el.md">Ελληνικά</a> · <a href="README.es.md">Español</a> · <a href="README.fa.md">فارسی</a> · <a href="README.fi.md">Suomi</a> · <a href="README.fr.md">Français</a> · <a href="README.he.md">עברית</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.hu.md">Magyar</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.it.md">Italiano</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.nb.md">Norsk bokmål</a> · <b>Nederlands</b> · <a href="README.pl.md">Polski</a> · <a href="README.pt_BR.md">Português (Brasil)</a> · <a href="README.ro.md">Română</a> · <a href="README.ru.md">Русский</a> · <a href="README.sv.md">Svenska</a> · <a href="README.th.md">ไทย</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.uk.md">Українська</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.zh_CN.md">简体中文</a> · <a href="README.zh_TW.md">繁體中文</a></sub></p>
<!-- /languages -->


Sound Tuner is een systeembrede EQ, crossover en luidsprekertuner voor
Linux-desktops met PipeWire. Het voegt een virtuele uitvoer, **Sound Tuner**,
toe vóór elk geluidsapparaat, van de ingebouwde speakers van een laptop tot
een stereopaar met sub of een complete 7.1-opstelling, en alle apps spelen
erdoorheen af.

<img src="../data/screenshots/main.webp" alt="Sound Tuner: de EQ-curve vormgeven boven het live uitvoerspectrum">

Op telefoons en in smalle vensters verhuizen de instellingen naar een uitschuifpaneel:

<img src="../data/screenshots/mobile.png" alt="Sound Tuner op een telefoon: equalizer en instellingenpaneel" width="420">

## Functies

- **Een EQ die je tekent:** veeg in beide richtingen over de grafiek om de
  curve te schilderen, of sleep losse punten. De curve loopt door je punten
  (de app berekent de filterversterkingen voor je), en je kunt scrollen om
  een band breder of smaller te maken, of exacte waarden voor frequentie,
  versterking en breedte invoeren. Achter de curve wordt een **live spectrum**
  getekend van wat er speelt.
- **Routering en crossovers per kanaal voor elke opstelling** (2.0, 2.1, 4.0,
  5.1, 7.1, …). Voor elk luidsprekerkanaal stel je in:
  - de bron: zelfde kanaal, links, rechts, mono, alle kanalen (voor een sub) of uit
  - hoogdoorlaat- en laagdoorlaat-scheidingsfilters (Linkwitz-Riley, 24 dB/oct)
  - niveau, vertraging (voor tijdsuitlijning) en polariteit
- **Kanaalindelingen met één klik:** laag afsnijden voor kleine speakers, een
  splitsing links bas / rechts hoog voor laptops, stereo naar alle
  luidsprekers en 80 Hz-basbeheer voor systemen met een subwoofer.
- **Loudness:** tot +20 dB boost in een look-ahead-limiter (ZaMaximX2), plus
  optionele **overdrive** voor als je het harder wilt dan schoon geluid
  toelaat, en een schakelaar waarmee de volumeschuif van GNOME boven 100% mag.
- **3D:** stereobreedte plus overspraakonderdrukking in de stijl van
  Ambiophonics/RACE, die het geluid breder uitspreidt dan dicht op elkaar
  geplaatste speakers, zoals die van een laptop.
- **Voorinstellingen:** een lijst bovenaan het venster. Klik op een
  voorinstelling om die te laden, of sla het huidige geluid op als nieuwe.
  Wijzigingen worden gaandeweg in de actieve voorinstelling opgeslagen.

## Hoe het zich verhoudt tot Easy Effects, JamesDSP, enz.

- **Moderne, eenvoudige interface:** één overzichtelijk scherm. Teken de
  EQ-curve, stel loudness en 3D in en kies een voorinstelling, zonder door
  pluginpanelen te hoeven graven. Ook geschikt voor mobiel: de interface past
  zich aan van telefoons tot brede desktopschermen.
- **Niets dat open hoeft te blijven:** de verwerking draait in PipeWire zelf.
  Sluit de app en je geluid blijft afgestemd vanaf het inloggen.
- **Echt meerkanaals:** 5.1 blijft 5.1, met crossovers, vertragingen en
  basbeheer per kanaal.
- **Geen haperingen:** wijzigingen worden live op het draaiende filter
  toegepast.
- **Piepklein:** één Python-bestand en één leesbare PipeWire-configuratie.
- **Moeilijk te laten clippen:** de keten eindigt altijd in een
  look-ahead-limiter. Zie hieronder.

### Waarom andere EQ-apps vervormd kunnen klinken

EQ en basboosts kunnen het signaal boven 0 dBFS duwen, het maximum dat de
geluidschip kan weergeven, en dan clipt het, tenzij een limiter het opvangt.
Sound Tuner eindigt altijd met een look-ahead-limiter die onder 0 dBFS is
ingesteld, zodat boosts luider worden in plaats van te kraken. (Overdrive
omzeilt dit bewust.) De verwerking draait bovendien in PipeWire zelf in
plaats van in een apart app-proces, dus er is één programma minder dat in
realtime moet bijblijven.

## Installatie

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

Het script installeert ontbrekende afhankelijkheden met je pakketbeheerder
(dnf, apt of pacman). Het toont de exacte opdracht en vraagt het eerst
voordat het `sudo` gebruikt. Daarna installeert het de app alleen voor jouw
gebruiker.

Open **Sound Tuner**, kies je uitvoerapparaat en klik op **Laden** in de
banner. De audio herstart eenmalig om het filter te laden.

| Optie | Wat het doet |
|---|---|
| `--yes` | afhankelijkheden installeren zonder te vragen |
| `--no-deps` | afhankelijkheden overslaan, alleen de app installeren |
| `--dry-run` | tonen wat er geïnstalleerd zou worden, niets wijzigen |
| `--uninstall` | de app en het PipeWire-filter verwijderen (je voorinstellingen blijven bewaard) |

### Afhankelijkheden

Worden voor je geïnstalleerd door `install.sh`:

- PipeWire-hulpmiddelen: `pw-cli`, `pw-dump`, `pw-record` en `pactl`
- Python 3 met GTK 4 en libadwaita 1.5+
- De ZaMaximX2-limiter uit [zam-plugins](https://github.com/zamaudio/zam-plugins)
- LV2-ondersteuning van PipeWire voor filter-chain

Je hebt een desktop nodig waarop PipeWire met WirePlumber al draait; dat is
de standaard op actuele versies van Fedora, Ubuntu, Debian en Arch. De
Fedora-pakketnamen zijn getest; als op andere distributies een pakketnaam is
veranderd, vertelt het script je wat er ontbreekt, zodat je het zelf kunt
installeren.

## Hoe het werkt

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

De opbouw van de graaf hangt alleen af van de kanalen van het apparaat. Al
het andere is een parameter, en een functie uitschakelen zet die op een
neutrale waarde, zoals 0 dB of een filter dat buiten het hoorbare bereik is
geschoven.

Het 3D-effect is RACE, uitgeschreven tot twee termen:
`out = own − g·D(other) + g²·D₂(own)`, bandbegrensd tot 250 Hz–5 kHz. De
filtergrafen van PipeWire kunnen geen terugkoppelingslussen bevatten, dus
het is niet volledig recursief.

Het spectrum wordt met `pw-record` uitgelezen van het apparaat dat je
afstemt, en alleen zolang het venster open is.

## Tips

- **Laptops:** pas de indeling *Kleine luidsprekers* toe (laag afsnijden op
  120 Hz) en voeg 6–10 dB boost toe. Dat is ongeveer wat
  Windows-geluidsverbeteringen zoals Dolby op de meeste laptops doen.
- **Subwoofer:** pas *Basbeheer (80 Hz)* toe en stel daarna het niveau en de
  vertraging van de subwoofer fijn af tot de bas op je luisterplek gelijkmatig
  klinkt.
- **3D:** ga in het midden zitten, zet de 3D-sterkte op ongeveer 70% en
  verschuif dan de 3D-vertraging tot het geluid zich breder uitspreidt dan de
  speakers.
- **Overdrive** stuurt geclipte audio naar je speakers. Gebruik het spaarzaam
  bij kleine drivers.

## Licentie

MIT. Zie [LICENSE](../LICENSE).

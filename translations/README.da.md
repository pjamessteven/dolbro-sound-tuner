<p align="center">
  <img src="../data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Ikon for Sound Tuner">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>Få det bedste ud af dine elendige laptophøjttalere, eller finjustér dit audiofile lydanlæg.</b></p>

<!-- languages -->
<p align="center"><sub><a href="../README.md">English</a> · <a href="README.ar.md">العربية</a> · <a href="README.bn.md">বাংলা</a> · <a href="README.cs.md">Čeština</a> · <b>Dansk</b> · <a href="README.de.md">Deutsch</a> · <a href="README.el.md">Ελληνικά</a> · <a href="README.es.md">Español</a> · <a href="README.fa.md">فارسی</a> · <a href="README.fi.md">Suomi</a> · <a href="README.fr.md">Français</a> · <a href="README.he.md">עברית</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.hu.md">Magyar</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.it.md">Italiano</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.nb.md">Norsk bokmål</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.pl.md">Polski</a> · <a href="README.pt_BR.md">Português (Brasil)</a> · <a href="README.ro.md">Română</a> · <a href="README.ru.md">Русский</a> · <a href="README.sv.md">Svenska</a> · <a href="README.th.md">ไทย</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.uk.md">Українська</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.zh_CN.md">简体中文</a> · <a href="README.zh_TW.md">繁體中文</a></sub></p>
<!-- /languages -->


Sound Tuner er en systemdækkende equalizer, delefilter og højttalerjustering til
Linux-skriveborde, der kører PipeWire. Den tilføjer en virtuel udgang, **Sound Tuner**,
foran en hvilken som helst lydenhed, fra en laptops indbyggede højttalere til et stereopar
med subwoofer eller et komplet 7.1-anlæg, og alle apps spiller igennem den.

<img src="../data/screenshots/main.webp" alt="Sound Tuner: EQ-kurven formes oven på udgangens livespektrum">

På telefoner og smalle vinduer flyttes indstillingerne ind i et udskydeligt panel:

<img src="../data/screenshots/mobile.png" alt="Sound Tuner på en telefon: equalizer og indstillingspanel" width="420">

## Funktioner

- **En EQ, du kan tegne:** stryg hen over grafen i begge retninger for at male
  kurven, eller træk i enkelte punkter. Kurven går gennem dine punkter
  (appen regner filtrenes forstærkning ud for dig), og du kan rulle for at gøre et
  bånd bredere eller smallere eller indtaste præcise værdier for frekvens, forstærkning og bredde. Et
  **livespektrum** af det, der spiller, tegnes bag kurven.
- **Routing og delefiltre pr. kanal til ethvert layout** (2.0, 2.1, 4.0, 5.1,
  7.1, …). For hver højttalerkanal indstiller du:
  - kilden: samme kanal, venstre, højre, mono, alle kanaler (til en sub) eller fra
  - højpas- og lavpasdelefiltre (Linkwitz-Riley, 24 dB/okt)
  - niveau, forsinkelse (til tidsjustering) og polaritet
- **Kanalopsætninger med ét klik:** lavcut til små højttalere, opdeling med bas til venstre /
  diskant til højre til laptops, stereo til alle højttalere og 80 Hz-basstyring
  til anlæg med subwoofer.
- **Loudness:** op til +20 dB boost ind i en fremadskuende begrænser (ZaMaximX2),
  plus valgfri **overdrive**, når du vil have det højere, end det kan gå rent,
  og en kontakt, der lader GNOMEs lydstyrkeskyder gå over 100 %.
- **3D:** stereobredde plus krydstaleudligning i stil med
  Ambiophonics/RACE, som spreder lyden bredere end tætsiddende højttalere
  som en laptops.
- **Forudindstillinger:** en liste øverst i vinduet. Klik på en for at indlæse den, eller gem
  den aktuelle lyd som en ny. Ændringer gemmes i den aktive forudindstilling, mens du arbejder.

## Sådan klarer den sig i forhold til Easy Effects, JamesDSP osv.

- **Moderne, nem brugerflade:** én overskuelig skærm. Tegn EQ-kurven, indstil loudness og
  3D, og vælg en forudindstilling, uden at rode rundt i plugin-paneler. Den er
  også mobilvenlig og tilpasser sig alt fra telefoner op til brede skrivebordsskærme.
- **Intet, der skal køre:** behandlingen foregår inde i selve PipeWire. Luk
  appen, og din lyd forbliver tunet fra login og fremefter.
- **Ægte flerkanal:** 5.1 forbliver 5.1, med delefiltre, forsinkelser
  og basstyring pr. kanal.
- **Ingen udfald:** ændringer anvendes live på det kørende filter.
- **Lillebitte:** én Python-fil og én læsbar PipeWire-konfiguration.
- **Svær at klippe:** kæden ender altid i en fremadskuende begrænser. Se nedenfor.

### Hvorfor andre EQ-apps kan lyde forvrængede

EQ og basboost kan presse signalet over 0 dBFS, det maksimale lydchippen
kan spille, og så klipper det, medmindre en begrænser griber det. Sound Tuner slutter altid
med en fremadskuende begrænser sat under 0 dBFS, så boost bliver højere i stedet for at
knitre. (Overdrive går bevidst uden om dette.) Behandlingen kører desuden
inde i selve PipeWire i stedet for i en separat app-proces, så der er ét
program mindre, der skal følge med i realtid.

## Installation

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

Scriptet installerer eventuelle manglende afhængigheder med din pakkehåndtering (dnf,
apt eller pacman). Det viser den præcise kommando og spørger, før det bruger `sudo`. Derefter
installeres appen kun for din bruger.

Åbn **Sound Tuner**, vælg din udgangsenhed, og klik på **Indlæs** i
banneret. Lyden genstarter én gang for at indlæse filteret.

| Tilvalg | Hvad det gør |
|---|---|
| `--yes` | installér afhængigheder uden at spørge |
| `--no-deps` | spring afhængigheder over, installér kun appen |
| `--dry-run` | vis, hvad der ville blive installeret, uden at ændre noget |
| `--uninstall` | fjern appen og PipeWire-filteret (beholder dine forudindstillinger) |

### Afhængigheder

Installeres for dig af `install.sh`:

- PipeWire-værktøjer: `pw-cli`, `pw-dump`, `pw-record` og `pactl`
- Python 3 med GTK 4 og libadwaita 1.5+
- Begrænseren ZaMaximX2 fra [zam-plugins](https://github.com/zamaudio/zam-plugins)
- PipeWires LV2-understøttelse til filter-chain

Du skal have et skrivebord, der allerede kører PipeWire med WirePlumber, hvilket er
standard på nuværende Fedora, Ubuntu, Debian og Arch. Fedoras pakkenavne
er testet; på andre distributioner fortæller scriptet, hvis et pakkenavn er ændret,
hvad der mangler, så du selv kan installere det.

## Sådan virker det

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

Grafens opbygning afhænger kun af enhedens kanaler. Alt andet er
en parameter, og når en funktion slås fra, sættes den til en neutral værdi, f.eks.
0 dB eller et filter flyttet uden for det hørbare område.

3D-effekten er RACE udfoldet til to led:
`out = own − g·D(other) + g²·D₂(own)`, båndbegrænset til 250 Hz–5 kHz. PipeWires
filtergrafer kan ikke indeholde tilbagekoblingssløjfer, så den er ikke fuldt rekursiv.

Spektret læses med `pw-record` fra den enhed, du tuner, og kun
mens vinduet er åbent.

## Tips

- **Laptops:** anvend opsætningen *Små højttalere* (lavcut ved 120 Hz), og tilføj
  6–10 dB boost. Det er nogenlunde, hvad Windows-forbedringer som Dolby gør
  på de fleste laptops.
- **Subwoofer:** anvend *Basstyring (80 Hz)*, og finjustér derefter
  subwooferens niveau og forsinkelse, indtil bassen lyder jævn, hvor du sidder.
- **3D:** sid i midten, sæt 3D-mængde til omkring 70 %, og flyt derefter 3D-forsinkelse, indtil
  lyden spredes bredere end højttalerne.
- **Overdrive** sender klippet lyd til dine højttalere. Brug det sparsomt på små
  enheder.

## Licens

MIT. Se [LICENSE](../LICENSE).

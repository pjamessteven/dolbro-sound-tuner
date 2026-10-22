<p align="center">
  <img src="../data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Ikon for Sound Tuner">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>Få mest mulig ut av de elendige laptophøyttalerne dine, eller finjuster det audiofile lydanlegget ditt.</b></p>

<!-- languages -->
<p align="center"><sub><a href="../README.md">English</a> · <a href="README.ar.md">العربية</a> · <a href="README.bn.md">বাংলা</a> · <a href="README.cs.md">Čeština</a> · <a href="README.da.md">Dansk</a> · <a href="README.de.md">Deutsch</a> · <a href="README.el.md">Ελληνικά</a> · <a href="README.es.md">Español</a> · <a href="README.fa.md">فارسی</a> · <a href="README.fi.md">Suomi</a> · <a href="README.fr.md">Français</a> · <a href="README.he.md">עברית</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.hu.md">Magyar</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.it.md">Italiano</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <b>Norsk bokmål</b> · <a href="README.nl.md">Nederlands</a> · <a href="README.pl.md">Polski</a> · <a href="README.pt_BR.md">Português (Brasil)</a> · <a href="README.ro.md">Română</a> · <a href="README.ru.md">Русский</a> · <a href="README.sv.md">Svenska</a> · <a href="README.th.md">ไทย</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.uk.md">Українська</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.zh_CN.md">简体中文</a> · <a href="README.zh_TW.md">繁體中文</a></sub></p>
<!-- /languages -->


Sound Tuner er en systemomfattende equalizer, delefilter og høyttalerjustering for
Linux-skrivebord som kjører PipeWire. Den legger til en virtuell utgang, **Sound Tuner**,
foran hvilken som helst lydenhet, fra en laptops innebygde høyttalere til et stereopar
med subwoofer eller et komplett 7.1-oppsett, og alle apper spiller gjennom den.

<img src="../data/screenshots/main.webp" alt="Sound Tuner: EQ-kurven formes over utgangens livespekter">

På telefoner og smale vinduer flyttes innstillingene inn i et uttrekkbart panel:

<img src="../data/screenshots/mobile.png" alt="Sound Tuner på en telefon: equalizer og innstillingspanel" width="420">

## Funksjoner

- **En EQ du kan tegne:** sveip over grafen i begge retninger for å male
  kurven, eller dra enkeltpunkter. Kurven går gjennom punktene dine
  (appen regner ut filterforsterkningen for deg), og du kan rulle for å gjøre et
  bånd bredere eller smalere, eller skrive inn nøyaktige verdier for frekvens, forsterkning og bredde. Et
  **livespekter** av det som spilles, tegnes bak kurven.
- **Ruting og delefiltre per kanal for alle oppsett** (2.0, 2.1, 4.0, 5.1,
  7.1, …). For hver høyttalerkanal stiller du inn:
  - kilden: samme kanal, venstre, høyre, mono, alle kanaler (for en sub) eller av
  - høypass- og lavpassdelefiltre (Linkwitz-Riley, 24 dB/okt)
  - nivå, forsinkelse (for tidsjustering) og polaritet
- **Kanaloppsett med ett klikk:** lavkutt for små høyttalere, deling med bass til venstre /
  diskant til høyre for laptoper, stereo til alle høyttalere og 80 Hz-bassbehandling
  for anlegg med subwoofer.
- **Loudness:** opptil +20 dB boost inn i en fremoverskuende begrenser (ZaMaximX2),
  pluss valgfri **overdrive** for når du vil ha det høyere enn det går an å få det rent,
  og en bryter som lar volumglidebryteren i GNOME gå over 100 %.
- **3D:** stereobredde pluss krysstaleutligning i stil med
  Ambiophonics/RACE, som sprer lyden bredere enn tettplasserte høyttalere
  som en laptops.
- **Forhåndsinnstillinger:** en liste øverst i vinduet. Klikk på en for å laste den inn, eller lagre
  gjeldende lyd som en ny. Endringer lagres i den aktive forhåndsinnstillingen mens du jobber.

## Slik står den seg mot Easy Effects, JamesDSP osv.

- **Moderne og enkelt grensesnitt:** én ryddig skjerm. Tegn EQ-kurven, still inn loudness og
  3D, og velg en forhåndsinnstilling, uten å grave i programtilleggspaneler. Den er
  også mobilvennlig og tilpasser seg alt fra telefoner til brede skrivebordsskjermer.
- **Ingenting som må kjøre:** behandlingen skjer inne i selve PipeWire. Lukk
  appen, og lyden forblir justert fra innlogging og utover.
- **Ekte flerkanal:** 5.1 forblir 5.1, med delefiltre, forsinkelser
  og bassbehandling per kanal.
- **Ingen utfall:** endringer tas i bruk direkte i det kjørende filteret.
- **Bitteliten:** én Python-fil og én lesbar PipeWire-konfigurasjon.
- **Vanskelig å klippe:** kjeden ender alltid i en fremoverskuende begrenser. Se nedenfor.

### Hvorfor andre EQ-apper kan høres forvrengt ut

EQ og bassboost kan presse signalet over 0 dBFS, det meste lydbrikken
kan spille, og da klipper det med mindre en begrenser fanger det opp. Sound Tuner slutter alltid
med en fremoverskuende begrenser satt under 0 dBFS, så boost gir høyere lyd i stedet for
knitring. (Overdrive går bevisst forbi dette.) Behandlingen kjører dessuten
inne i selve PipeWire i stedet for i en egen app-prosess, så det er ett
program mindre som må henge med i sanntid.

## Installasjon

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

Skriptet installerer eventuelle manglende avhengigheter med pakkebehandleren din (dnf,
apt eller pacman). Det viser den nøyaktige kommandoen og spør før det bruker `sudo`. Deretter
installeres appen kun for brukeren din.

Åpne **Sound Tuner**, velg utgangsenheten din, og klikk på **Last inn** i
banneret. Lyden starter på nytt én gang for å laste inn filteret.

| Valg | Hva det gjør |
|---|---|
| `--yes` | installer avhengigheter uten å spørre |
| `--no-deps` | hopp over avhengigheter, installer bare appen |
| `--dry-run` | vis hva som ville blitt installert, endre ingenting |
| `--uninstall` | fjern appen og PipeWire-filteret (beholder forhåndsinnstillingene dine) |

### Avhengigheter

Installeres for deg av `install.sh`:

- PipeWire-verktøy: `pw-cli`, `pw-dump`, `pw-record` og `pactl`
- Python 3 med GTK 4 og libadwaita 1.5+
- Begrenseren ZaMaximX2 fra [zam-plugins](https://github.com/zamaudio/zam-plugins)
- PipeWires LV2-støtte for filter-chain

Du trenger et skrivebord som allerede kjører PipeWire med WirePlumber, noe som er
standard på nåværende Fedora, Ubuntu, Debian og Arch. Pakkenavnene for Fedora
er testet; på andre distribusjoner forteller skriptet deg hva som mangler hvis et pakkenavn
er endret, slik at du kan installere det selv.

## Slik fungerer det

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

Grafens oppbygning avhenger bare av enhetens kanaler. Alt annet er
en parameter, og når en funksjon slås av, settes den til en nøytral verdi, for eksempel
0 dB eller et filter flyttet utenfor det hørbare området.

3D-effekten er RACE utviklet til to ledd:
`out = own − g·D(other) + g²·D₂(own)`, båndbegrenset til 250 Hz–5 kHz. PipeWires
filtergrafer kan ikke inneholde tilbakekoblingssløyfer, så den er ikke fullt rekursiv.

Spekteret leses med `pw-record` fra enheten du justerer, og bare
mens vinduet er åpent.

## Tips

- **Laptoper:** bruk oppsettet *Små høyttalere* (lavkutt ved 120 Hz) og legg til
  6–10 dB boost. Det er omtrent det Windows-forbedringer som Dolby gjør
  på de fleste laptoper.
- **Subwoofer:** bruk *Bassbehandling (80 Hz)*, og finjuster deretter
  subwooferens nivå og forsinkelse til bassen høres jevn ut der du sitter.
- **3D:** sitt midt foran, sett 3D-mengde til rundt 70 %, og juster så 3D-forsinkelse til
  lyden sprer seg bredere enn høyttalerne.
- **Overdrive** sender klippet lyd til høyttalerne dine. Bruk det med måte på små
  elementer.

## Lisens

MIT. Se [LICENSE](../LICENSE).

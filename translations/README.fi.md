<p align="center">
  <img src="../data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Sound Tunerin kuvake">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>Ota kaikki irti läppärisi surkeista kaiuttimista tai hio audiofiilin äänentoistojärjestelmäsi viimeisen päälle.</b></p>

<!-- languages -->
<p align="center"><sub><a href="../README.md">English</a> · <a href="README.ar.md">العربية</a> · <a href="README.bn.md">বাংলা</a> · <a href="README.cs.md">Čeština</a> · <a href="README.da.md">Dansk</a> · <a href="README.de.md">Deutsch</a> · <a href="README.el.md">Ελληνικά</a> · <a href="README.es.md">Español</a> · <a href="README.fa.md">فارسی</a> · <b>Suomi</b> · <a href="README.fr.md">Français</a> · <a href="README.he.md">עברית</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.hu.md">Magyar</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.it.md">Italiano</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.nb.md">Norsk bokmål</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.pl.md">Polski</a> · <a href="README.pt_BR.md">Português (Brasil)</a> · <a href="README.ro.md">Română</a> · <a href="README.ru.md">Русский</a> · <a href="README.sv.md">Svenska</a> · <a href="README.th.md">ไทย</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.uk.md">Українська</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.zh_CN.md">简体中文</a> · <a href="README.zh_TW.md">繁體中文</a></sub></p>
<!-- /languages -->


Sound Tuner on järjestelmänlaajuinen taajuuskorjain, jakosuodin ja
kaiutinsäädin PipeWireä käyttäville Linux-työpöydille. Se lisää minkä tahansa
äänilaitteen eteen virtuaalisen ulostulon, **Sound Tuner**, oli laite sitten
läppärin sisäiset kaiuttimet, subwooferilla varustettu stereopari tai
täysi 7.1-järjestelmä, ja kaikki sovellukset soivat sen kautta.

<img src="../data/screenshots/main.webp" alt="Sound Tuner: taajuuskorjaimen käyrän muotoilu reaaliaikaisen ulostulospektrin päällä">

Puhelimissa ja kapeissa ikkunoissa asetukset siirtyvät esiin liukuvaan paneeliin:

<img src="../data/screenshots/mobile.png" alt="Sound Tuner puhelimessa: taajuuskorjain ja asetuspaneeli" width="420">

## Ominaisuudet

- **Taajuuskorjain, jonka voi piirtää:** pyyhkäise kaavion yli kumpaan
  suuntaan tahansa maalataksesi käyrän tai vedä yksittäisiä pisteitä. Käyrä
  kulkee pisteidesi kautta (sovellus laskee suodinten vahvistukset puolestasi),
  ja voit vierittää leventääksesi tai kaventaaksesi kaistaa tai kirjoittaa
  tarkat taajuus-, vahvistus- ja leveysarvot. Käyrän taakse piirretään
  **reaaliaikainen spektri** siitä, mitä soi.
- **Kanavakohtainen reititys ja jakosuotimet mille tahansa kokoonpanolle**
  (2.0, 2.1, 4.0, 5.1, 7.1, …). Jokaiselle kaiutinkanavalle asetetaan:
  - lähde: sama kanava, vasen, oikea, mono, kaikki kanavat (subwooferille) tai pois
  - ylipäästö- ja alipäästöjakosuotimet (Linkwitz-Riley, 24 dB/oct)
  - taso, viive (aika-asettelua varten) ja napaisuus
- **Kanava-asettelut yhdellä napsautuksella:** alarajaus pienille
  kaiuttimille, vasen basso / oikea diskantti -jako läppäreille, stereo kaikkiin
  kaiuttimiin sekä 80 Hz:n bassonhallinta subwooferilla varustetuille
  järjestelmille.
- **Äänekkyys:** jopa +20 dB korotusta ennakoivaan limitteriin (ZaMaximX2),
  lisäksi valinnainen **overdrive**, kun haluat kovempaa kuin puhdas ääni
  sallii, sekä kytkin, jolla GNOMEn äänenvoimakkuuden liukusäädin pääsee yli
  100 %:n.
- **3D:** stereoleveys sekä Ambiophonics/RACE-tyylinen ylikuulumisen
  vaimennus, joka levittää äänen leveämmälle kuin lähekkäin olevat kaiuttimet,
  kuten läppärin, muuten antaisivat.
- **Esiasetukset:** luettelo ikkunan yläreunassa. Lataa esiasetus
  napsauttamalla sitä tai tallenna nykyinen ääni uudeksi. Muutokset
  tallentuvat aktiiviseen esiasetukseen sitä mukaa kuin teet niitä.

## Miten se vertautuu Easy Effectsiin, JamesDSP:hen ym.

- **Moderni ja helppo käyttöliittymä:** yksi selkeä näkymä. Piirrä
  taajuuskorjaimen käyrä, säädä äänekkyys ja 3D ja valitse esiasetus ilman
  liitännäispaneelien penkomista. Se toimii myös mobiilissa ja mukautuu
  puhelimista leveisiin työpöytänäyttöihin.
- **Mitään ei tarvitse pitää käynnissä:** käsittely tapahtuu PipeWiren
  sisällä. Sulje sovellus, ja äänesi pysyy säädettynä kirjautumisesta lähtien.
- **Aito monikanavaisuus:** 5.1 pysyy 5.1:nä kanavakohtaisine jakosuotimineen,
  viiveineen ja bassonhallintoineen.
- **Ei katkoja:** muutokset otetaan käyttöön käynnissä olevaan suotimeen
  lennosta.
- **Pienen pieni:** yksi Python-tiedosto ja yksi helppolukuinen PipeWire-määritys.
- **Vaikea saada säröytymään:** ketju päättyy aina ennakoivaan limitteriin.
  Katso alta.

### Miksi muut taajuuskorjainsovellukset voivat kuulostaa säröisiltä

Taajuuskorjain ja bassokorotukset voivat työntää signaalin yli 0 dBFS:n, joka
on suurin taso, jonka äänipiiri pystyy toistamaan, ja silloin ääni leikkautuu,
ellei limitteri ota sitä kiinni. Sound Tuner päättyy aina ennakoivaan
limitteriin, joka on asetettu alle 0 dBFS:n, joten korotukset kuuluvat
kovempana äänenä eivätkä rätinänä. (Overdrive ohittaa tämän tarkoituksella.)
Lisäksi sen käsittely tapahtuu PipeWiren sisällä eikä erillisessä
sovellusprosessissa, joten reaaliajassa mukana pysyttäviä ohjelmia on yksi
vähemmän.

## Asennus

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

Skripti asentaa puuttuvat riippuvuudet paketinhallintasi avulla (dnf, apt tai
pacman). Se näyttää tarkan komennon ja kysyy ennen kuin käyttää `sudo`a.
Sen jälkeen se asentaa sovelluksen vain omalle käyttäjällesi.

Avaa **Sound Tuner**, valitse ulostulolaitteesi ja napsauta bannerin
**Lataa**-painiketta. Ääni käynnistyy kerran uudelleen suotimen lataamiseksi.

| Valitsin | Mitä se tekee |
|---|---|
| `--yes` | asentaa riippuvuudet kysymättä |
| `--no-deps` | ohittaa riippuvuudet, asentaa vain sovelluksen |
| `--dry-run` | näyttää, mitä asennettaisiin, muuttamatta mitään |
| `--uninstall` | poistaa sovelluksen ja PipeWire-suotimen (esiasetukset säilyvät) |

### Riippuvuudet

`install.sh` asentaa nämä puolestasi:

- PipeWire-työkalut: `pw-cli`, `pw-dump`, `pw-record` ja `pactl`
- Python 3, GTK 4 ja libadwaita 1.5+
- ZaMaximX2-limitteri [zam-plugins](https://github.com/zamaudio/zam-plugins)-kokoelmasta
- PipeWiren LV2-tuki filter-chainia varten

Tarvitset työpöydän, jossa PipeWire ja WirePlumber ovat jo käytössä, mikä on
oletus nykyisissä Fedorassa, Ubuntussa, Debianissa ja Archissa. Fedoran
pakettinimet on testattu; jos muissa jakeluissa jonkin paketin nimi on
muuttunut, skripti kertoo, mitä puuttuu, jotta voit asentaa sen itse.

## Miten se toimii

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

Graafin rakenne riippuu vain laitteen kanavista. Kaikki muu on parametreja,
ja ominaisuuden poistaminen käytöstä asettaa sen neutraaliin arvoon, kuten
0 dB tai kuuluvan alueen ulkopuolelle siirretty suodin.

3D-efekti on kahteen termiin avattu RACE:
`out = own − g·D(other) + g²·D₂(own)`, kaistarajattuna välille 250 Hz–5 kHz.
PipeWiren suodingraafit eivät voi sisältää takaisinkytkentäsilmukoita, joten
se ei ole täysin rekursiivinen.

Spektri luetaan `pw-record`illa säädettävästä laitteesta, ja vain silloin,
kun ikkuna on auki.

## Vinkkejä

- **Läppärit:** ota käyttöön *Pienet kaiuttimet* -asettelu (alarajaus 120 Hz)
  ja lisää 6–10 dB korotusta. Suunnilleen tätä Windowsin äänenparannukset,
  kuten Dolby, tekevät useimmissa läppäreissä.
- **Subwoofer:** ota käyttöön *Bassonhallinta (80 Hz)* ja hienosäädä sitten
  subwooferin tasoa ja viivettä, kunnes basso kuulostaa tasaiselta
  kuuntelupaikallasi.
- **3D:** istu keskellä, aseta 3D-määrä noin 70 %:iin ja säädä sitten
  3D-viivettä, kunnes ääni levittäytyy kaiuttimia leveämmälle.
- **Overdrive** lähettää kaiuttimiin leikkautunutta ääntä. Käytä sitä
  säästeliäästi pienten elementtien kanssa.

## Lisenssi

MIT. Katso [LICENSE](../LICENSE).

<p align="center">
  <img src="../data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Ikon för Sound Tuner">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>Få ut det mesta av dina skitkassa laptophögtalare, eller finjustera ditt audiofila ljudsystem.</b></p>

<!-- languages -->
<p align="center"><sub><a href="../README.md">English</a> · <a href="README.ar.md">العربية</a> · <a href="README.bn.md">বাংলা</a> · <a href="README.cs.md">Čeština</a> · <a href="README.da.md">Dansk</a> · <a href="README.de.md">Deutsch</a> · <a href="README.el.md">Ελληνικά</a> · <a href="README.es.md">Español</a> · <a href="README.fa.md">فارسی</a> · <a href="README.fi.md">Suomi</a> · <a href="README.fr.md">Français</a> · <a href="README.he.md">עברית</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.hu.md">Magyar</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.it.md">Italiano</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.nb.md">Norsk bokmål</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.pl.md">Polski</a> · <a href="README.pt_BR.md">Português (Brasil)</a> · <a href="README.ro.md">Română</a> · <a href="README.ru.md">Русский</a> · <b>Svenska</b> · <a href="README.th.md">ไทย</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.uk.md">Українська</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.zh_CN.md">简体中文</a> · <a href="README.zh_TW.md">繁體中文</a></sub></p>
<!-- /languages -->


Sound Tuner är en systemomfattande equalizer, delningsfilter och högtalarjustering
för Linux-skrivbord som kör PipeWire. Den lägger till en virtuell utgång, **Sound Tuner**,
framför valfri ljudenhet, från en laptops inbyggda högtalare till ett stereopar
med subwoofer eller ett komplett 7.1-system, och alla appar spelar genom den.

<img src="../data/screenshots/main.webp" alt="Sound Tuner: EQ-kurvan formas ovanpå utgångens livespektrum">

På telefoner och smala fönster flyttas inställningarna till en utfällbar panel:

<img src="../data/screenshots/mobile.png" alt="Sound Tuner på en telefon: equalizer och inställningspanel" width="420">

## Funktioner

- **En EQ du kan rita:** svep över grafen åt valfritt håll för att måla
  kurvan, eller dra enskilda punkter. Kurvan går genom dina punkter
  (appen räknar ut filtrens förstärkning åt dig), och du kan rulla för att göra ett
  band bredare eller smalare, eller skriva in exakta värden för frekvens, förstärkning och bredd. Ett
  **livespektrum** av det som spelas ritas bakom kurvan.
- **Dirigering och delningsfilter per kanal för alla uppsättningar** (2.0, 2.1, 4.0, 5.1,
  7.1, …). För varje högtalarkanal ställer du in:
  - källan: samma kanal, vänster, höger, mono, alla kanaler (för en sub) eller av
  - högpass- och lågpassdelningsfilter (Linkwitz-Riley, 24 dB/okt)
  - nivå, fördröjning (för tidsjustering) och polaritet
- **Kanaluppsättningar med ett klick:** lågavskärning för små högtalare, uppdelning med bas till vänster /
  diskant till höger för laptops, stereo till alla högtalare och 80 Hz-bashantering
  för system med subwoofer.
- **Loudness:** upp till +20 dB boost in i en framåtblickande begränsare (ZaMaximX2),
  plus valfri **överstyrning** för när du vill ha det högre än vad som går rent,
  och en brytare som låter GNOME:s volymreglage gå över 100 %.
- **3D:** stereobredd plus överhörningsutsläckning i stil med
  Ambiophonics/RACE, som sprider ljudet bredare än tätt placerade högtalare
  som en laptops.
- **Förinställningar:** en lista högst upp i fönstret. Klicka på en för att läsa in den, eller spara
  det aktuella ljudet som en ny. Ändringar sparas i den aktiva förinställningen medan du jobbar.

## Hur den står sig mot Easy Effects, JamesDSP m.fl.

- **Modernt och enkelt gränssnitt:** en enda ren vy. Rita EQ-kurvan, ställ in loudness och
  3D, och välj en förinställning, utan att gräva i insticksmodulpaneler. Den är
  mobilvänlig också och anpassar sig från telefoner upp till breda skrivbordsskärmar.
- **Inget som måste vara igång:** bearbetningen sker inuti PipeWire självt. Stäng
  appen och ljudet förblir justerat från inloggningen och framåt.
- **Äkta flerkanal:** 5.1 förblir 5.1, med delningsfilter, fördröjningar
  och bashantering per kanal.
- **Inga avbrott:** ändringar tillämpas direkt på det körande filtret.
- **Pytteliten:** en Python-fil och en läsbar PipeWire-konfiguration.
- **Svår att klippa:** kedjan slutar alltid i en framåtblickande begränsare. Se nedan.

### Varför andra EQ-appar kan låta förvrängda

EQ och basförstärkning kan driva signalen över 0 dBFS, det mesta ljudkretsen
kan spela, och då klipps den om inte en begränsare fångar upp den. Sound Tuner slutar alltid
med en framåtblickande begränsare inställd under 0 dBFS, så boost ger högre ljud i stället för
knaster. (Överstyrning kringgår detta medvetet.) Bearbetningen sker dessutom
inuti PipeWire självt i stället för i en separat appprocess, så det finns ett
program mindre som måste hänga med i realtid.

## Installation

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

Skriptet installerar eventuella saknade beroenden med din pakethanterare (dnf,
apt eller pacman). Det visar exakt vilket kommando som körs och frågar innan det använder `sudo`. Sedan
installeras appen enbart för din användare.

Öppna **Sound Tuner**, välj din utgångsenhet och klicka på **Läs in** i
bannern. Ljudet startas om en gång för att läsa in filtret.

| Flagga | Vad den gör |
|---|---|
| `--yes` | installera beroenden utan att fråga |
| `--no-deps` | hoppa över beroenden, installera bara appen |
| `--dry-run` | visa vad som skulle installeras, ändra ingenting |
| `--uninstall` | ta bort appen och PipeWire-filtret (behåller dina förinställningar) |

### Beroenden

Installeras åt dig av `install.sh`:

- PipeWire-verktyg: `pw-cli`, `pw-dump`, `pw-record` och `pactl`
- Python 3 med GTK 4 och libadwaita 1.5+
- Begränsaren ZaMaximX2 från [zam-plugins](https://github.com/zamaudio/zam-plugins)
- PipeWires LV2-stöd för filter-chain

Du behöver ett skrivbord som redan kör PipeWire med WirePlumber, vilket är
standard på aktuella Fedora, Ubuntu, Debian och Arch. Paketnamnen för Fedora
är testade; på andra distributioner, om ett paketnamn har ändrats, talar skriptet om
vad som saknas så att du kan installera det själv.

## Så fungerar det

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

Grafens uppbyggnad beror bara på enhetens kanaler. Allt annat är
en parameter, och att stänga av en funktion sätter den till ett neutralt värde, till exempel
0 dB eller ett filter som flyttats utanför det hörbara området.

3D-effekten är RACE utvecklad till två termer:
`out = own − g·D(other) + g²·D₂(own)`, bandbegränsad till 250 Hz–5 kHz. PipeWires
filtergrafer kan inte innehålla återkopplingsslingor, så den är inte helt rekursiv.

Spektrumet läses med `pw-record` från enheten du justerar, och bara
medan fönstret är öppet.

## Tips

- **Laptops:** tillämpa uppsättningen *Små högtalare* (lågavskärning vid 120 Hz) och lägg till
  6–10 dB boost. Det är ungefär vad Windows-förbättringar som Dolby gör
  på de flesta laptops.
- **Subwoofer:** tillämpa *Bashantering (80 Hz)* och finjustera sedan
  subwooferns nivå och fördröjning tills basen låter jämn där du sitter.
- **3D:** sitt centrerat, ställ 3D-mängd på cirka 70 % och flytta sedan 3D-fördröjning tills
  ljudet sprids bredare än högtalarna.
- **Överstyrning** skickar klippt ljud till dina högtalare. Använd den sparsamt med små
  element.

## Licens

MIT. Se [LICENSE](../LICENSE).

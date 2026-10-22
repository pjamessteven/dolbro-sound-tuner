<p align="center">
  <img src="../data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Sound Tuner ikon">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>Hozd ki a maximumot a vacak laptophangszóróidból, vagy hangold finomra az audiofil hangrendszeredet.</b></p>

<!-- languages -->
<p align="center"><sub><a href="../README.md">English</a> · <a href="README.ar.md">العربية</a> · <a href="README.bn.md">বাংলা</a> · <a href="README.cs.md">Čeština</a> · <a href="README.da.md">Dansk</a> · <a href="README.de.md">Deutsch</a> · <a href="README.el.md">Ελληνικά</a> · <a href="README.es.md">Español</a> · <a href="README.fa.md">فارسی</a> · <a href="README.fi.md">Suomi</a> · <a href="README.fr.md">Français</a> · <a href="README.he.md">עברית</a> · <a href="README.hi.md">हिन्दी</a> · <b>Magyar</b> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.it.md">Italiano</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.nb.md">Norsk bokmål</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.pl.md">Polski</a> · <a href="README.pt_BR.md">Português (Brasil)</a> · <a href="README.ro.md">Română</a> · <a href="README.ru.md">Русский</a> · <a href="README.sv.md">Svenska</a> · <a href="README.th.md">ไทย</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.uk.md">Українська</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.zh_CN.md">简体中文</a> · <a href="README.zh_TW.md">繁體中文</a></sub></p>
<!-- /languages -->


A Sound Tuner egy rendszerszintű hangszínszabályzó, keresztváltó és
hangszóróhangoló PipeWire-t futtató linuxos asztali környezetekhez. Egy
virtuális kimenetet, a **Sound Tunert** helyezi bármely hangeszköz elé, a laptop
beépített hangszóróitól a mélysugárzós sztereó páron át egy teljes 7.1-es
rendszerig, és minden alkalmazás ezen keresztül szól.

<img src="../data/screenshots/main.webp" alt="Sound Tuner: a hangszínszabályzó görbéjének formázása az élő kimeneti spektrum fölött">

Telefonon és keskeny ablakokban a beállítások egy kicsúszó panelre kerülnek:

<img src="../data/screenshots/mobile.png" alt="Sound Tuner telefonon: hangszínszabályzó és beállítások panel" width="420">

## Funkciók

- **Rajzolható hangszínszabályzó:** húzd végig a grafikonon bármelyik irányba a
  görbe megrajzolásához, vagy mozgasd az egyes pontokat. A görbe átmegy a
  pontjaidon (a szűrők erősítését az alkalmazás számolja ki helyetted), és
  görgetéssel szélesítheted vagy keskenyítheted a sávot, illetve pontos
  frekvencia-, erősítés- és szélességértékeket is beírhatsz. A görbe mögött az
  éppen szóló hang **élő spektruma** látható.
- **Csatornánkénti útválasztás és keresztváltók bármilyen elrendezéshez**
  (2.0, 2.1, 4.0, 5.1, 7.1, …). Minden hangszórócsatornához beállíthatod:
  - a forrást: azonos csatorna, bal, jobb, monó, minden csatorna (mélysugárzóhoz)
    vagy ki
  - a felüláteresztő és aluláteresztő keresztváltószűrőket (Linkwitz-Riley,
    24 dB/oktáv)
  - a szintet, a késleltetést (időbeli igazításhoz) és a polaritást
- **Egykattintásos csatornabeállítások:** mélyvágás kis hangszórókhoz, bal
  basszus / jobb magas felosztás laptopokhoz, sztereó minden hangszóróra és
  80 Hz-es basszuskezelés mélysugárzós rendszerekhez.
- **Hangosság:** akár +20 dB felerősítés egy előretekintő limiterbe
  (ZaMaximX2), plusz opcionális **overdrive**, ha hangosabban szeretnéd, mint
  ami tisztán kijön, és egy kapcsoló, amellyel a GNOME hangerő-csúszkája 100%
  fölé mehet.
- **3D:** sztereó szélesség és Ambiophonics/RACE-stílusú áthallás-kioltás,
  amely a közel elhelyezett hangszórókon – például egy laptopén – túlra
  szélesíti a hangot.
- **Előbeállítások:** egy lista az ablak tetején. Kattints egyre a
  betöltéséhez, vagy mentsd el a jelenlegi hangzást újként. A módosítások menet
  közben mentődnek az aktív előbeállításba.

## Összevetés az Easy Effects-szel, a JamesDSP-vel és társaikkal

- **Modern, egyszerű felület:** egyetlen letisztult képernyő. Rajzold meg a
  hangszínszabályzó görbéjét, állítsd be a hangosságot és a 3D-t, válassz
  előbeállítást, mindezt bővítménypanelek közti turkálás nélkül. Mobilbarát is,
  a telefonoktól a széles asztali képernyőkig alkalmazkodik.
- **Semminek sem kell futnia:** a feldolgozás magában a PipeWire-ben történik.
  Zárd be az alkalmazást, és a hangod a bejelentkezéstől kezdve hangolt marad.
- **Valódi többcsatornás hang:** az 5.1 5.1 marad, csatornánkénti
  keresztváltókkal, késleltetéssel és basszuskezeléssel.
- **Nincs kiesés:** a módosítások élőben érvényesülnek a futó szűrőn.
- **Pici:** egy Python-fájl és egy olvasható PipeWire-konfiguráció.
- **Nehéz túlvezérelni:** a lánc mindig egy előretekintő limiterrel végződik.
  Lásd lent.

### Miért szólhatnak torzan más hangszínszabályzók

A hangszínszabályzás és a basszuskiemelés 0 dBFS fölé tolhatja a jelet, ami a
legtöbb, amit a hangchip le tud játszani, és a jel levágódik (clipping), hacsak
egy limiter meg nem fogja. A Sound Tuner mindig egy 0 dBFS alá állított
előretekintő limiterrel zárul, így a kiemelések hangosítanak recsegés helyett.
(Az overdrive ezt szándékosan megkerüli.) A feldolgozás ráadásul magában a
PipeWire-ben fut, nem külön alkalmazásfolyamatban, így eggyel kevesebb program
kell, hogy valós időben lépést tartson.

## Telepítés

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

A szkript a csomagkezelőddel (dnf, apt vagy pacman) telepíti a hiányzó
függőségeket. Megmutatja a pontos parancsot, és a `sudo` használata előtt
rákérdez. Ezután csak a saját felhasználód számára telepíti az alkalmazást.

Nyisd meg a **Sound Tunert**, válaszd ki a kimeneti eszközt, és kattints a
sávban a **Betöltés** gombra. A hang egyszer újraindul a szűrő betöltéséhez.

| Kapcsoló | Mit csinál |
|---|---|
| `--yes` | rákérdezés nélkül telepíti a függőségeket |
| `--no-deps` | kihagyja a függőségeket, csak az alkalmazást telepíti |
| `--dry-run` | megmutatja, mi települne, de semmit sem módosít |
| `--uninstall` | eltávolítja az alkalmazást és a PipeWire-szűrőt (az előbeállítások megmaradnak) |

### Függőségek

Az `install.sh` telepíti őket helyetted:

- PipeWire-eszközök: `pw-cli`, `pw-dump`, `pw-record` és `pactl`
- Python 3 GTK 4-gyel és libadwaita 1.5+ verzióval
- A ZaMaximX2 limiter a [zam-plugins](https://github.com/zamaudio/zam-plugins) csomagból
- A PipeWire LV2-támogatása a filter-chainhez

Olyan asztali környezet kell, amelyen már PipeWire fut WirePlumberrel; ez az
alapértelmezés a jelenlegi Fedora, Ubuntu, Debian és Arch rendszereken. A
Fedora-csomagnevek teszteltek; más disztribúciókon, ha egy csomag neve
megváltozott, a szkript megmondja, mi hiányzik, hogy magad telepíthesd.

## Hogyan működik

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

A gráf felépítése csak az eszköz csatornáitól függ. Minden más paraméter, és
egy funkció kikapcsolása semleges értékre állítja azt, például 0 dB-re, vagy a
szűrőt a hallható tartományon kívülre tolja.

A 3D-effektus két tagra kifejtett RACE:
`out = own − g·D(other) + g²·D₂(own)`, 250 Hz–5 kHz közé sávkorlátozva. A
PipeWire szűrőgráfjai nem tartalmazhatnak visszacsatoló hurkot, ezért nem
teljesen rekurzív.

A spektrumot a `pw-record` olvassa a hangolt eszközről, és csak addig, amíg az
ablak nyitva van.

## Tippek

- **Laptopok:** alkalmazd a *Kis hangszórók* beállítást (120 Hz-es mélyvágás),
  és adj hozzá 6–10 dB felerősítést. Nagyjából ezt csinálják a Windows
  hangjavításai, például a Dolby, a legtöbb laptopon.
- **Mélysugárzó:** alkalmazd a *Basszuskezelés (80 Hz)* beállítást, majd
  finomhangold a mélysugárzó szintjét és késleltetését, amíg a basszus
  egyenletesen nem szól a helyeden.
- **3D:** ülj középre, állítsd a 3D mértékét kb. 70%-ra, majd addig állítsd a
  3D késleltetést, amíg a hang a hangszórókon túlra nem szélesedik.
- Az **overdrive** levágott hangot küld a hangszóróidra. Kis hangszórókon
  óvatosan használd.

## Licenc

MIT. Lásd: [LICENSE](../LICENSE).

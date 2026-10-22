<p align="center">
  <img src="../data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Pictograma Sound Tuner">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>Scoate maximum din difuzoarele jalnice ale laptopului sau reglează fin sistemul tău audio de audiofil.</b></p>

<!-- languages -->
<p align="center"><sub><a href="../README.md">English</a> · <a href="README.ar.md">العربية</a> · <a href="README.bn.md">বাংলা</a> · <a href="README.cs.md">Čeština</a> · <a href="README.da.md">Dansk</a> · <a href="README.de.md">Deutsch</a> · <a href="README.el.md">Ελληνικά</a> · <a href="README.es.md">Español</a> · <a href="README.fa.md">فارسی</a> · <a href="README.fi.md">Suomi</a> · <a href="README.fr.md">Français</a> · <a href="README.he.md">עברית</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.hu.md">Magyar</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.it.md">Italiano</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.nb.md">Norsk bokmål</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.pl.md">Polski</a> · <a href="README.pt_BR.md">Português (Brasil)</a> · <b>Română</b> · <a href="README.ru.md">Русский</a> · <a href="README.sv.md">Svenska</a> · <a href="README.th.md">ไทย</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.uk.md">Українська</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.zh_CN.md">简体中文</a> · <a href="README.zh_TW.md">繁體中文</a></sub></p>
<!-- /languages -->


Sound Tuner este un egalizator, crossover și instrument de reglare a
difuzoarelor la nivel de sistem pentru desktopurile Linux care rulează
PipeWire. Adaugă o ieșire virtuală, **Sound Tuner**, în fața oricărui dispozitiv
audio, de la difuzoarele integrate ale unui laptop până la o pereche stereo cu
subwoofer sau un sistem 7.1 complet, iar toate aplicațiile cântă prin ea.

<img src="../data/screenshots/main.webp" alt="Sound Tuner: modelarea curbei egalizatorului peste spectrul live al ieșirii">

Pe telefoane și în ferestrele înguste, setările se mută într-un panou glisant:

<img src="../data/screenshots/mobile.png" alt="Sound Tuner pe un telefon: egalizator și panoul de setări" width="420">

## Funcții

- **Un egalizator pe care îl desenezi:** trage peste grafic în orice direcție ca
  să pictezi curba sau mută puncte individuale. Curba trece prin punctele tale
  (aplicația calculează câștigurile filtrelor pentru tine), iar cu rotița poți
  face o bandă mai lată sau mai îngustă ori poți introduce valori exacte de
  frecvență, câștig și lățime. În spatele curbei se desenează un **spectru
  live** al ce se aude.
- **Rutare și crossovere pe fiecare canal, pentru orice configurație** (2.0,
  2.1, 4.0, 5.1, 7.1, …). Pentru fiecare canal de difuzor setezi:
  - sursa: același canal, stânga, dreapta, mono, toate canalele (pentru un
    subwoofer) sau oprit
  - filtre de crossover trece-sus și trece-jos (Linkwitz-Riley, 24 dB/oct)
  - nivelul, întârzierea (pentru alinierea în timp) și polaritatea
- **Configurații de canale dintr-un clic:** tăierea joaselor pentru difuzoare
  mici, împărțire bas în stânga / înalte în dreapta pentru laptopuri, stereo pe
  toate difuzoarele și gestionarea basului la 80 Hz pentru sistemele cu
  subwoofer.
- **Volum:** până la +20 dB de amplificare într-un limitator cu look-ahead
  (ZaMaximX2), plus **overdrive** opțional pentru când vrei mai tare decât
  permite sunetul curat, și un comutator care lasă glisorul de volum din GNOME
  să treacă de 100%.
- **3D:** lățime stereo plus anularea diafoniei în stilul Ambiophonics/RACE,
  care extinde sunetul mai larg decât difuzoarele apropiate, cum sunt cele ale
  unui laptop.
- **Presetări:** o listă în partea de sus a ferestrei. Dă clic pe una ca s-o
  încarci sau salvează sunetul curent ca presetare nouă. Modificările se
  salvează în presetarea activă pe măsură ce lucrezi.

## Cum se compară cu Easy Effects, JamesDSP etc.

- **Interfață modernă și simplă:** un singur ecran curat. Desenează curba
  egalizatorului, setează volumul și 3D-ul și alege o presetare, fără să
  scotocești prin panouri de pluginuri. Merge bine și pe mobil, adaptându-se de
  la telefoane până la ecrane late de desktop.
- **Nimic nu trebuie să ruleze în fundal:** procesarea are loc chiar în
  PipeWire. Închide aplicația și sunetul rămâne reglat încă de la autentificare.
- **Multicanal adevărat:** 5.1 rămâne 5.1, cu crossovere, întârzieri și
  gestionarea basului pe fiecare canal.
- **Fără întreruperi:** modificările se aplică live filtrului care rulează.
- **Minuscul:** un singur fișier Python și o configurație PipeWire ușor de citit.
- **Greu de saturat:** lanțul se termină mereu cu un limitator cu look-ahead.
  Vezi mai jos.

### De ce alte egalizatoare pot suna distorsionat

Egalizarea și amplificarea basului pot împinge semnalul peste 0 dBFS, maximul pe
care îl poate reda cipul audio, iar acesta se saturează (clipping) dacă nu îl
prinde un limitator. Sound Tuner se termină mereu cu un limitator cu look-ahead
setat sub 0 dBFS, așa că amplificările dau sunet mai tare în loc de pârâituri.
(Overdrive-ul ocolește intenționat acest lucru.) În plus, procesarea rulează
chiar în PipeWire, nu într-un proces separat al aplicației, deci e un program
mai puțin care trebuie să țină pasul în timp real.

## Instalare

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

Scriptul instalează dependențele lipsă cu managerul tău de pachete (dnf, apt
sau pacman). Îți arată comanda exactă și te întreabă înainte să folosească
`sudo`. Apoi instalează aplicația doar pentru utilizatorul tău.

Deschide **Sound Tuner**, alege dispozitivul de ieșire și dă clic pe
**Încarcă** în banner. Sunetul repornește o dată ca să încarce filtrul.

| Opțiune | Ce face |
|---|---|
| `--yes` | instalează dependențele fără să întrebe |
| `--no-deps` | sare peste dependențe, instalează doar aplicația |
| `--dry-run` | arată ce s-ar instala, fără să schimbe nimic |
| `--uninstall` | elimină aplicația și filtrul PipeWire (păstrează presetările) |

### Dependențe

Instalate pentru tine de `install.sh`:

- Utilitarele PipeWire: `pw-cli`, `pw-dump`, `pw-record` și `pactl`
- Python 3 cu GTK 4 și libadwaita 1.5+
- Limitatorul ZaMaximX2 din [zam-plugins](https://github.com/zamaudio/zam-plugins)
- Suportul LV2 al PipeWire pentru filter-chain

Ai nevoie de un desktop care rulează deja PipeWire cu WirePlumber, ceea ce este
implicit pe versiunile actuale de Fedora, Ubuntu, Debian și Arch. Numele
pachetelor pentru Fedora sunt testate; pe alte distribuții, dacă numele unui
pachet s-a schimbat, scriptul îți spune ce lipsește ca să-l instalezi singur.

## Cum funcționează

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

Structura grafului depinde doar de canalele dispozitivului. Tot restul este un
parametru, iar dezactivarea unei funcții o setează la o valoare neutră, cum ar
fi 0 dB sau un filtru mutat în afara domeniului audibil.

Efectul 3D este RACE desfășurat la doi termeni:
`out = own − g·D(other) + g²·D₂(own)`, cu banda limitată la 250 Hz–5 kHz.
Grafurile de filtre din PipeWire nu pot conține bucle de reacție, așa că nu este
complet recursiv.

Spectrul este citit cu `pw-record` de pe dispozitivul pe care îl reglezi și
doar cât timp fereastra este deschisă.

## Sfaturi

- **Laptopuri:** aplică configurația *Difuzoare mici* (tăiere joase la 120 Hz)
  și adaugă 6–10 dB de amplificare. Cam asta fac îmbunătățirile audio din
  Windows, precum Dolby, pe majoritatea laptopurilor.
- **Subwoofer:** aplică *Gestionare bas (80 Hz)*, apoi reglează fin nivelul și
  întârzierea subwooferului până când basul sună uniform acolo unde stai.
- **3D:** așază-te central, setează intensitatea 3D la aproximativ 70%, apoi
  modifică întârzierea 3D până când sunetul se întinde dincolo de difuzoare.
- **Overdrive-ul** trimite sunet saturat către difuzoare. Folosește-l cu
  măsură pe difuzoarele mici.

## Licență

MIT. Vezi [LICENSE](../LICENSE).

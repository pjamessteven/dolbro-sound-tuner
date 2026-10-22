<p align="center">
  <img src="../data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Ikona Sound Tuner">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>Vymáčkněte maximum z mizerných reproduktorů v notebooku, nebo do detailu vylaďte svou audiofilskou sestavu.</b></p>

<!-- languages -->
<p align="center"><sub><a href="../README.md">English</a> · <a href="README.ar.md">العربية</a> · <a href="README.bn.md">বাংলা</a> · <b>Čeština</b> · <a href="README.da.md">Dansk</a> · <a href="README.de.md">Deutsch</a> · <a href="README.el.md">Ελληνικά</a> · <a href="README.es.md">Español</a> · <a href="README.fa.md">فارسی</a> · <a href="README.fi.md">Suomi</a> · <a href="README.fr.md">Français</a> · <a href="README.he.md">עברית</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.hu.md">Magyar</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.it.md">Italiano</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.nb.md">Norsk bokmål</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.pl.md">Polski</a> · <a href="README.pt_BR.md">Português (Brasil)</a> · <a href="README.ro.md">Română</a> · <a href="README.ru.md">Русский</a> · <a href="README.sv.md">Svenska</a> · <a href="README.th.md">ไทย</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.uk.md">Українська</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.zh_CN.md">简体中文</a> · <a href="README.zh_TW.md">繁體中文</a></sub></p>
<!-- /languages -->


Sound Tuner je systémový ekvalizér, výhybka a ladič reproduktorů pro linuxová
desktopová prostředí s PipeWire. Přidá virtuální výstup **Sound Tuner** před
libovolné zvukové zařízení, od vestavěných reproduktorů notebooku po stereo pár
se subwooferem nebo kompletní sestavu 7.1, a všechny aplikace hrají přes něj.

<img src="../data/screenshots/main.webp" alt="Sound Tuner: tvarování křivky ekvalizéru nad živým spektrem výstupu">

Na telefonech a v úzkých oknech se nastavení přesune do vysouvacího panelu:

<img src="../data/screenshots/mobile.png" alt="Sound Tuner na telefonu: ekvalizér a panel nastavení" width="420">

## Funkce

- **Ekvalizér, který si nakreslíte:** přejeďte po grafu libovolným směrem a
  namalujte křivku, nebo přetahujte jednotlivé body. Křivka prochází vašimi
  body (zisky filtrů za vás dopočítá aplikace) a kolečkem myši můžete pásmo
  rozšířit nebo zúžit, případně zadat přesné hodnoty frekvence, zisku a šířky.
  Za křivkou se vykresluje **živé spektrum** toho, co právě hraje.
- **Směrování a výhybky pro každý kanál v libovolném uspořádání** (2.0, 2.1,
  4.0, 5.1, 7.1, …). Pro každý kanál reproduktoru nastavíte:
  - zdroj: stejný kanál, levý, pravý, mono, všechny kanály (pro subwoofer) nebo
    vypnuto
  - výhybkové filtry horní a dolní propust (Linkwitz-Riley, 24 dB/okt.)
  - úroveň, zpoždění (pro časové srovnání) a polaritu
- **Nastavení kanálů jedním kliknutím:** ořez basů pro malé reproduktory,
  rozdělení basy vlevo / výšky vpravo pro notebooky, stereo do všech
  reproduktorů a správa basů na 80 Hz pro sestavy se subwooferem.
- **Hlasitost:** až +20 dB zesílení do limiteru s předstihem (ZaMaximX2), k tomu
  volitelný **overdrive**, když chcete hlasitěji, než dovolí čistý zvuk, a
  přepínač, který posuvníku hlasitosti v GNOME dovolí jít nad 100 %.
- **3D:** šířka sterea plus potlačení přeslechů ve stylu Ambiophonics/RACE,
  které rozšíří zvuk dál, než sahají těsně umístěné reproduktory, třeba ty v
  notebooku.
- **Předvolby:** seznam v horní části okna. Kliknutím předvolbu načtete, nebo
  aktuální zvuk uložíte jako novou. Změny se do aktivní předvolby ukládají
  průběžně.

## Srovnání s Easy Effects, JamesDSP a dalšími

- **Moderní, jednoduché rozhraní:** jedna přehledná obrazovka. Nakreslete
  křivku ekvalizéru, nastavte hlasitost a 3D a vyberte předvolbu, bez
  prohrabávání panelů pluginů. Hodí se i pro mobily, přizpůsobí se od telefonů
  až po široké monitory.
- **Nic nemusí běžet na pozadí:** zpracování probíhá přímo v PipeWire. Zavřete
  aplikaci a zvuk zůstane vyladěný hned od přihlášení.
- **Skutečný vícekanálový zvuk:** z 5.1 zůstane 5.1, s výhybkami, zpožděním a
  správou basů pro každý kanál.
- **Žádné výpadky:** změny se projeví v běžícím filtru naživo.
- **Malinký:** jeden soubor v Pythonu a jedna čitelná konfigurace PipeWire.
- **Těžko se přebudí:** řetězec vždy končí limiterem s předstihem. Viz níže.

### Proč mohou jiné ekvalizéry znít zkresleně

Ekvalizér a zesílení basů mohou signál vytlačit nad 0 dBFS, tedy maximum, které
zvukový čip dokáže přehrát, a pokud ho nezachytí limiter, dojde k ořezu. Sound
Tuner vždy končí limiterem s předstihem nastaveným pod 0 dBFS, takže zesílení
zvuk zesílí, místo aby praskal. (Overdrive tohle záměrně obchází.) Zpracování
navíc běží přímo v PipeWire, ne v samostatném procesu aplikace, takže je o
jeden program méně, který musí stíhat v reálném čase.

## Instalace

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

Skript nainstaluje chybějící závislosti pomocí vašeho správce balíčků (dnf, apt
nebo pacman). Ukáže přesný příkaz a před použitím `sudo` se zeptá. Potom
nainstaluje aplikaci jen pro vašeho uživatele.

Otevřete **Sound Tuner**, vyberte výstupní zařízení a v liště klikněte na
**Načíst**. Zvuk se jednou restartuje, aby se filtr načetl.

| Volba | Co dělá |
|---|---|
| `--yes` | nainstaluje závislosti bez ptaní |
| `--no-deps` | přeskočí závislosti, nainstaluje jen aplikaci |
| `--dry-run` | ukáže, co by se nainstalovalo, nic nezmění |
| `--uninstall` | odebere aplikaci a filtr PipeWire (předvolby ponechá) |

### Závislosti

Nainstaluje je za vás `install.sh`:

- Nástroje PipeWire: `pw-cli`, `pw-dump`, `pw-record` a `pactl`
- Python 3 s GTK 4 a libadwaita 1.5+
- Limiter ZaMaximX2 ze [zam-plugins](https://github.com/zamaudio/zam-plugins)
- Podpora LV2 v PipeWire pro filter-chain

Potřebujete desktop, na kterém už běží PipeWire s WirePlumberem, což je výchozí
stav v aktuálních verzích Fedory, Ubuntu, Debianu a Archu. Názvy balíčků pro
Fedoru jsou otestované; pokud se v jiné distribuci název balíčku změnil, skript
vám řekne, co chybí, abyste to mohli nainstalovat sami.

## Jak to funguje

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

Uspořádání grafu závisí jen na kanálech zařízení. Všechno ostatní je parametr a
vypnutí funkce ji nastaví na neutrální hodnotu, například 0 dB nebo filtr
posunutý mimo slyšitelné pásmo.

Efekt 3D je RACE rozvinutý do dvou členů:
`out = own − g·D(other) + g²·D₂(own)`, s pásmem omezeným na 250 Hz–5 kHz.
Grafy filtrů v PipeWire nemohou obsahovat zpětnovazební smyčky, takže není
plně rekurzivní.

Spektrum se čte pomocí `pw-record` ze zařízení, které ladíte, a jen dokud je
okno otevřené.

## Tipy

- **Notebooky:** použijte nastavení *Malé reproduktory* (ořez basů 120 Hz) a
  přidejte 6–10 dB zesílení. Zhruba tohle dělají na většině notebooků
  vylepšení zvuku ve Windows, jako je Dolby.
- **Subwoofer:** použijte *Správa basů (80 Hz)* a pak dolaďte úroveň a zpoždění
  subwooferu, dokud basy nezní na vašem místě vyrovnaně.
- **3D:** sedněte si doprostřed, nastavte míru 3D zhruba na 70 % a pak měňte
  zpoždění 3D, dokud se zvuk nerozšíří za hranice reproduktorů.
- **Overdrive** posílá do reproduktorů ořezaný zvuk. U malých měničů ho
  používejte s rozvahou.

## Licence

MIT. Viz [LICENSE](../LICENSE).

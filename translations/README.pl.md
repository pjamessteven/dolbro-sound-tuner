<p align="center">
  <img src="../data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Ikona Sound Tuner">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>Wyciśnij maksimum z badziewnych głośników w laptopie albo dopieść swój audiofilski zestaw grający.</b></p>

<!-- languages -->
<p align="center"><sub><a href="../README.md">English</a> · <a href="README.ar.md">العربية</a> · <a href="README.bn.md">বাংলা</a> · <a href="README.cs.md">Čeština</a> · <a href="README.da.md">Dansk</a> · <a href="README.de.md">Deutsch</a> · <a href="README.el.md">Ελληνικά</a> · <a href="README.es.md">Español</a> · <a href="README.fa.md">فارسی</a> · <a href="README.fi.md">Suomi</a> · <a href="README.fr.md">Français</a> · <a href="README.he.md">עברית</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.hu.md">Magyar</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.it.md">Italiano</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.nb.md">Norsk bokmål</a> · <a href="README.nl.md">Nederlands</a> · <b>Polski</b> · <a href="README.pt_BR.md">Português (Brasil)</a> · <a href="README.ro.md">Română</a> · <a href="README.ru.md">Русский</a> · <a href="README.sv.md">Svenska</a> · <a href="README.th.md">ไทย</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.uk.md">Українська</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.zh_CN.md">简体中文</a> · <a href="README.zh_TW.md">繁體中文</a></sub></p>
<!-- /languages -->


Sound Tuner to systemowy korektor, zwrotnica i narzędzie do strojenia głośników
dla linuksowych pulpitów z PipeWire. Dodaje wirtualne wyjście **Sound Tuner**
przed dowolnym urządzeniem dźwiękowym, od wbudowanych głośników laptopa po parę
stereo z subwooferem albo pełny zestaw 7.1, a wszystkie aplikacje grają przez
nie.

<img src="../data/screenshots/main.webp" alt="Sound Tuner: kształtowanie krzywej korektora na tle widma wyjścia na żywo">

Na telefonach i w wąskich oknach ustawienia trafiają do wysuwanego panelu:

<img src="../data/screenshots/mobile.png" alt="Sound Tuner na telefonie: korektor i panel ustawień" width="420">

## Funkcje

- **Korektor, który można narysować:** przeciągnij po wykresie w dowolnym
  kierunku, aby namalować krzywą, albo przesuwaj pojedyncze punkty. Krzywa
  przechodzi przez twoje punkty (aplikacja sama wylicza wzmocnienia filtrów),
  a przewijaniem możesz poszerzyć lub zwęzić pasmo albo wpisać dokładne
  wartości częstotliwości, wzmocnienia i szerokości. Za krzywą rysowane jest
  **widmo na żywo** tego, co aktualnie gra.
- **Kierowanie sygnału i zwrotnice dla każdego kanału w dowolnym układzie**
  (2.0, 2.1, 4.0, 5.1, 7.1, …). Dla każdego kanału głośnikowego ustawiasz:
  - źródło: ten sam kanał, lewy, prawy, mono, wszystkie kanały (dla subwoofera)
    lub wyłączone
  - filtry zwrotnicy górno- i dolnoprzepustowe (Linkwitz-Riley, 24 dB/okt.)
  - poziom, opóźnienie (do wyrównania czasowego) i polaryzację
- **Konfiguracje kanałów jednym kliknięciem:** odcięcie basu dla małych
  głośników, podział bas po lewej / soprany po prawej dla laptopów, stereo na
  wszystkie głośniki oraz zarządzanie basem 80 Hz dla zestawów z subwooferem.
- **Głośność:** do +20 dB podbicia przed limiterem z wyprzedzeniem (ZaMaximX2),
  do tego opcjonalny **przester**, gdy chcesz głośniej, niż pozwala czysty
  dźwięk, oraz przełącznik pozwalający suwakowi głośności GNOME wyjść ponad
  100%.
- **3D:** szerokość stereo plus eliminacja przesłuchu w stylu
  Ambiophonics/RACE, która rozprasza dźwięk szerzej niż blisko ustawione
  głośniki, np. w laptopie.
- **Ustawienia wstępne:** lista u góry okna. Kliknij jedno, aby je wczytać, albo
  zapisz bieżący dźwięk jako nowe. Zmiany zapisują się w aktywnym ustawieniu na
  bieżąco.

## Jak wypada na tle Easy Effects, JamesDSP itp.

- **Nowoczesny, prosty interfejs:** jeden przejrzysty ekran. Narysuj krzywą
  korektora, ustaw głośność i 3D, wybierz ustawienie wstępne, bez przekopywania
  się przez panele wtyczek. Działa też dobrze na urządzeniach mobilnych,
  dopasowując się od telefonów po szerokie ekrany komputerów.
- **Nic nie musi działać w tle:** przetwarzanie odbywa się w samym PipeWire.
  Zamknij aplikację, a dźwięk pozostanie dostrojony od samego zalogowania.
- **Prawdziwa wielokanałowość:** 5.1 zostaje 5.1, ze zwrotnicami, opóźnieniami
  i zarządzaniem basem dla każdego kanału.
- **Bez przerw w dźwięku:** zmiany trafiają do działającego filtra na żywo.
- **Malutki:** jeden plik w Pythonie i jedna czytelna konfiguracja PipeWire.
- **Trudno go przesterować:** łańcuch zawsze kończy się limiterem z
  wyprzedzeniem. Szczegóły poniżej.

### Dlaczego inne korektory potrafią brzmieć na przesterowane

Korektor i podbicie basu mogą wypchnąć sygnał ponad 0 dBFS, czyli maksimum,
jakie układ dźwiękowy jest w stanie odtworzyć, i wtedy sygnał się obcina, chyba
że złapie go limiter. Sound Tuner zawsze kończy łańcuch limiterem z
wyprzedzeniem ustawionym poniżej 0 dBFS, więc podbicia dają większą głośność
zamiast trzasków. (Przester celowo to omija.) Przetwarzanie działa też w samym
PipeWire, a nie w osobnym procesie aplikacji, więc jest o jeden program mniej,
który musi nadążać w czasie rzeczywistym.

## Instalacja

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

Skrypt instaluje brakujące zależności za pomocą menedżera pakietów (dnf, apt
lub pacman). Pokazuje dokładne polecenie i pyta przed użyciem `sudo`. Następnie
instaluje aplikację tylko dla twojego użytkownika.

Otwórz **Sound Tuner**, wybierz urządzenie wyjściowe i kliknij **Wczytaj** na
banerze. Dźwięk zrestartuje się raz, aby wczytać filtr.

| Opcja | Co robi |
|---|---|
| `--yes` | instaluje zależności bez pytania |
| `--no-deps` | pomija zależności, instaluje tylko aplikację |
| `--dry-run` | pokazuje, co zostałoby zainstalowane, niczego nie zmienia |
| `--uninstall` | usuwa aplikację i filtr PipeWire (zachowuje ustawienia wstępne) |

### Zależności

Instalowane automatycznie przez `install.sh`:

- Narzędzia PipeWire: `pw-cli`, `pw-dump`, `pw-record` i `pactl`
- Python 3 z GTK 4 i libadwaita 1.5+
- Limiter ZaMaximX2 z [zam-plugins](https://github.com/zamaudio/zam-plugins)
- Obsługa LV2 w PipeWire dla filter-chain

Potrzebujesz pulpitu, na którym już działa PipeWire z WirePlumberem, co jest
domyślne w aktualnych wersjach Fedory, Ubuntu, Debiana i Archa. Nazwy pakietów
dla Fedory są przetestowane; w innych dystrybucjach, jeśli nazwa pakietu się
zmieniła, skrypt powie, czego brakuje, żebyś mógł to doinstalować samodzielnie.

## Jak to działa

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

Układ grafu zależy wyłącznie od kanałów urządzenia. Cała reszta to parametry,
a wyłączenie funkcji ustawia ją na wartość neutralną, np. 0 dB albo filtr
przesunięty poza zakres słyszalny.

Efekt 3D to RACE rozwinięty do dwóch wyrazów:
`out = own − g·D(other) + g²·D₂(own)`, z pasmem ograniczonym do 250 Hz–5 kHz.
Grafy filtrów PipeWire nie mogą zawierać pętli sprzężenia zwrotnego, więc nie
jest on w pełni rekurencyjny.

Widmo jest odczytywane przez `pw-record` z urządzenia, które stroisz, i tylko
wtedy, gdy okno jest otwarte.

## Wskazówki

- **Laptopy:** zastosuj konfigurację *Małe głośniki* (odcięcie basu 120 Hz) i
  dodaj 6–10 dB podbicia. Mniej więcej to samo robią ulepszenia dźwięku w
  Windowsie, takie jak Dolby, na większości laptopów.
- **Subwoofer:** zastosuj *Zarządzanie basem (80 Hz)*, a potem dostrój poziom i
  opóźnienie subwoofera, aż bas będzie brzmiał równo w miejscu, w którym
  siedzisz.
- **3D:** usiądź na środku, ustaw siłę 3D na około 70%, a potem zmieniaj
  opóźnienie 3D, aż dźwięk rozejdzie się szerzej niż głośniki.
- **Przester** wysyła do głośników obcięty dźwięk. Używaj go oszczędnie przy
  małych przetwornikach.

## Licencja

MIT. Zobacz [LICENSE](../LICENSE).

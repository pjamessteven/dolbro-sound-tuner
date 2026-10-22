<p align="center">
  <img src="../data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Sound Tuner simgesi">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>Dizüstü bilgisayarınızın berbat hoparlörlerinden sonuna kadar yararlanın ya da odyofil ses sisteminize ince ayar yapın.</b></p>

<!-- languages -->
<p align="center"><sub><a href="../README.md">English</a> · <a href="README.ar.md">العربية</a> · <a href="README.bn.md">বাংলা</a> · <a href="README.cs.md">Čeština</a> · <a href="README.da.md">Dansk</a> · <a href="README.de.md">Deutsch</a> · <a href="README.el.md">Ελληνικά</a> · <a href="README.es.md">Español</a> · <a href="README.fa.md">فارسی</a> · <a href="README.fi.md">Suomi</a> · <a href="README.fr.md">Français</a> · <a href="README.he.md">עברית</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.hu.md">Magyar</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.it.md">Italiano</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.nb.md">Norsk bokmål</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.pl.md">Polski</a> · <a href="README.pt_BR.md">Português (Brasil)</a> · <a href="README.ro.md">Română</a> · <a href="README.ru.md">Русский</a> · <a href="README.sv.md">Svenska</a> · <a href="README.th.md">ไทย</a> · <b>Türkçe</b> · <a href="README.uk.md">Українська</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.zh_CN.md">简体中文</a> · <a href="README.zh_TW.md">繁體中文</a></sub></p>
<!-- /languages -->


Sound Tuner, PipeWire çalıştıran Linux masaüstleri için sistem genelinde
çalışan bir ekolayzır, crossover ve hoparlör ayarlayıcısıdır. Dizüstü
bilgisayarın dahili hoparlörlerinden subwoofer’lı bir stereo çifte ya da tam
bir 7.1 sisteme kadar her ses aygıtının önüne **Sound Tuner** adlı sanal bir
çıkış ekler ve tüm uygulamalar onun üzerinden çalar.

<img src="../data/screenshots/main.webp" alt="Sound Tuner: canlı çıkış spektrumu üzerinde ekolayzır eğrisini şekillendirme">

Telefonlarda ve dar pencerelerde ayarlar kayarak açılan bir panele taşınır:

<img src="../data/screenshots/mobile.png" alt="Telefonda Sound Tuner: ekolayzır ve ayarlar paneli" width="420">

## Özellikler

- **Çizebileceğiniz bir ekolayzır:** eğriyi boyamak için grafiğin üzerinde
  herhangi bir yöne sürükleyin ya da noktaları tek tek taşıyın. Eğri
  noktalarınızdan geçer (filtre kazançlarını uygulama sizin için hesaplar);
  bir bandı genişletmek ya da daraltmak için kaydırabilir veya tam frekans,
  kazanç ve genişlik değerlerini yazabilirsiniz. Eğrinin arkasında çalan
  sesin **canlı spektrumu** çizilir.
- **Her düzen için kanal başına yönlendirme ve crossover’lar** (2.0, 2.1,
  4.0, 5.1, 7.1, …). Her hoparlör kanalı için şunları ayarlarsınız:
  - kaynak: aynı kanal, sol, sağ, mono, tüm kanallar (subwoofer için) ya da kapalı
  - yüksek geçiren ve alçak geçiren crossover filtreleri (Linkwitz-Riley, 24 dB/oct)
  - seviye, gecikme (zaman hizalaması için) ve polarite
- **Tek tıkla kanal düzenleri:** küçük hoparlörler için alt kesim, dizüstü
  bilgisayarlar için sol bas / sağ tiz bölmesi, tüm hoparlörlere stereo ve
  subwoofer’lı sistemler için 80 Hz bas yönetimi.
- **Ses yüksekliği:** ileriye bakan bir sınırlayıcıya (ZaMaximX2) giden
  +20 dB’e kadar güçlendirme, temiz sesin izin verdiğinden daha yüksek ses
  istediğinizde isteğe bağlı **overdrive** ve GNOME’un ses düzeyi kaydırıcısının
  %100’ü aşmasına izin veren bir anahtar.
- **3D:** stereo genişliği ile birlikte Ambiophonics/RACE tarzında karışma
  (crosstalk) iptali; bu, sesi dizüstü bilgisayardakiler gibi birbirine yakın
  duran hoparlörlerin izin verdiğinden daha geniş yayar.
- **Ön ayarlar:** pencerenin üstünde bir liste. Yüklemek için birine tıklayın
  ya da geçerli sesi yeni bir ön ayar olarak kaydedin. Değişiklikler siz
  çalıştıkça etkin ön ayara kaydedilir.

## Easy Effects, JamesDSP vb. ile karşılaştırma

- **Modern, kolay arayüz:** tek ve sade bir ekran. Ekolayzır eğrisini çizin,
  ses yüksekliğini ve 3D’yi ayarlayın, bir ön ayar seçin; eklenti panelleri
  arasında kaybolmadan. Mobil dostudur da; telefonlardan geniş masaüstü
  ekranlarına kadar uyum sağlar.
- **Açık tutmanız gereken bir şey yok:** işleme doğrudan PipeWire’ın içinde
  yapılır. Uygulamayı kapatın, sesiniz oturum açtığınız andan itibaren ayarlı
  kalır.
- **Gerçek çok kanallı:** 5.1, kanal başına crossover’lar, gecikmeler ve bas
  yönetimiyle 5.1 olarak kalır.
- **Kesinti yok:** değişiklikler çalışan filtreye anında uygulanır.
- **Minicik:** tek bir Python dosyası ve okunabilir tek bir PipeWire
  yapılandırması.
- **Kırpılması zor:** zincir her zaman ileriye bakan bir sınırlayıcıyla
  biter. Aşağıya bakın.

### Diğer ekolayzır uygulamaları neden bozuk ses çıkarabilir

Ekolayzır ve bas güçlendirmeleri sinyali, ses çipinin çalabileceği en yüksek
seviye olan 0 dBFS’nin ötesine itebilir ve bir sınırlayıcı yakalamazsa ses
kırpılır. Sound Tuner her zaman 0 dBFS’nin altına ayarlanmış, ileriye bakan
bir sınırlayıcıyla biter; böylece güçlendirmeler cızırtı yerine daha yüksek
ses olarak duyulur. (Overdrive bunu bilerek atlar.) Ayrıca işleme ayrı bir
uygulama sürecinde değil doğrudan PipeWire’ın içinde yapılır; yani gerçek
zamanlı olarak yetişmesi gereken bir program eksik olur.

## Kurulum

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

Betik eksik bağımlılıkları paket yöneticinizle (dnf, apt veya pacman) kurar.
`sudo` kullanmadan önce tam komutu gösterir ve onayınızı ister. Ardından
uygulamayı yalnızca sizin kullanıcınız için kurar.

**Sound Tuner**’ı açın, çıkış aygıtınızı seçin ve banttaki **Yükle**
düğmesine tıklayın. Filtreyi yüklemek için ses bir kez yeniden başlatılır.

| Seçenek | Ne yapar |
|---|---|
| `--yes` | bağımlılıkları sormadan kurar |
| `--no-deps` | bağımlılıkları atlar, yalnızca uygulamayı kurar |
| `--dry-run` | neyin kurulacağını gösterir, hiçbir şeyi değiştirmez |
| `--uninstall` | uygulamayı ve PipeWire filtresini kaldırır (ön ayarlarınızı korur) |

### Bağımlılıklar

`install.sh` tarafından sizin için kurulanlar:

- PipeWire araçları: `pw-cli`, `pw-dump`, `pw-record` ve `pactl`
- GTK 4 ve libadwaita 1.5+ ile Python 3
- [zam-plugins](https://github.com/zamaudio/zam-plugins) içindeki ZaMaximX2 sınırlayıcısı
- filter-chain için PipeWire’ın LV2 desteği

WirePlumber ile PipeWire’ı zaten çalıştıran bir masaüstüne ihtiyacınız var;
bu, güncel Fedora, Ubuntu, Debian ve Arch’ta varsayılandır. Fedora paket
adları test edilmiştir; diğer dağıtımlarda bir paketin adı değiştiyse betik
neyin eksik olduğunu söyler, böylece kendiniz kurabilirsiniz.

## Nasıl çalışır

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

Grafiğin yapısı yalnızca aygıtın kanallarına bağlıdır. Geri kalan her şey
bir parametredir ve bir özelliği kapatmak onu 0 dB ya da duyulabilir aralığın
dışına taşınmış bir filtre gibi nötr bir değere ayarlar.

3D efekti, iki terime açılmış RACE’tir:
`out = own − g·D(other) + g²·D₂(own)`, 250 Hz–5 kHz bandıyla sınırlıdır.
PipeWire’ın filtre grafikleri geri besleme döngüleri içeremediğinden tam
olarak özyinelemeli değildir.

Spektrum, ayarladığınız aygıttan `pw-record` ile ve yalnızca pencere açıkken
okunur.

## İpuçları

- **Dizüstü bilgisayarlar:** *Küçük hoparlörler* düzenini (120 Hz alt kesim)
  uygulayın ve 6–10 dB güçlendirme ekleyin. Dolby gibi Windows ses
  iyileştirmelerinin çoğu dizüstü bilgisayarda yaptığı kabaca budur.
- **Subwoofer:** *Bas yönetimi (80 Hz)* düzenini uygulayın, ardından bas
  oturduğunuz yerde dengeli duyulana kadar subwoofer’ın seviyesine ve
  gecikmesine ince ayar yapın.
- **3D:** ortada oturun, 3D miktarını yaklaşık %70’e ayarlayın, ardından ses
  hoparlörlerden daha geniş yayılana kadar 3D gecikmesini değiştirin.
- **Overdrive** hoparlörlerinize kırpılmış ses gönderir. Küçük sürücülerde
  idareli kullanın.

## Lisans

MIT. Bkz. [LICENSE](../LICENSE).

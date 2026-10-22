<p align="center">
  <img src="../data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Ikon Sound Tuner">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>Maksimalkan speaker laptop ampasmu, atau setel sistem suara audiofilmu sampai detail terkecil.</b></p>

<!-- languages -->
<p align="center"><sub><a href="../README.md">English</a> · <a href="README.ar.md">العربية</a> · <a href="README.bn.md">বাংলা</a> · <a href="README.cs.md">Čeština</a> · <a href="README.da.md">Dansk</a> · <a href="README.de.md">Deutsch</a> · <a href="README.el.md">Ελληνικά</a> · <a href="README.es.md">Español</a> · <a href="README.fa.md">فارسی</a> · <a href="README.fi.md">Suomi</a> · <a href="README.fr.md">Français</a> · <a href="README.he.md">עברית</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.hu.md">Magyar</a> · <b>Bahasa Indonesia</b> · <a href="README.it.md">Italiano</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.nb.md">Norsk bokmål</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.pl.md">Polski</a> · <a href="README.pt_BR.md">Português (Brasil)</a> · <a href="README.ro.md">Română</a> · <a href="README.ru.md">Русский</a> · <a href="README.sv.md">Svenska</a> · <a href="README.th.md">ไทย</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.uk.md">Українська</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.zh_CN.md">简体中文</a> · <a href="README.zh_TW.md">繁體中文</a></sub></p>
<!-- /languages -->


Sound Tuner adalah EQ, crossover, dan penyetel speaker tingkat sistem untuk desktop
Linux yang menjalankan PipeWire. Aplikasi ini menambahkan keluaran virtual, **Sound Tuner**,
di depan perangkat suara apa pun, mulai dari speaker bawaan laptop hingga sepasang speaker stereo
dengan subwoofer atau sistem 7.1 lengkap, dan semua aplikasi memutar suara melaluinya.

<img src="../data/screenshots/main.webp" alt="Sound Tuner: membentuk kurva EQ di atas spektrum keluaran langsung">

Di ponsel dan jendela sempit, pengaturan dipindahkan ke panel geser:

<img src="../data/screenshots/mobile.png" alt="Sound Tuner di ponsel: equalizer dan panel pengaturan" width="420">

## Fitur

- **EQ yang bisa kamu gambar:** sapukan di atas grafik ke arah mana pun untuk melukis
  kurvanya, atau seret titik satu per satu. Kurva melewati titik-titikmu
  (aplikasi menghitung penguatan filternya untukmu), dan kamu bisa menggulir untuk membuat
  pita lebih lebar atau lebih sempit, atau mengetik nilai frekuensi, penguatan, dan lebar yang tepat.
  **Spektrum langsung** dari apa yang sedang diputar digambar di belakang kurva.
- **Perutean dan crossover per kanal untuk tata letak apa pun** (2.0, 2.1, 4.0, 5.1,
  7.1, …). Untuk setiap kanal speaker kamu bisa mengatur:
  - sumber: kanal yang sama, kiri, kanan, mono, semua kanal (untuk sub) atau mati
  - filter crossover high-pass dan low-pass (Linkwitz-Riley, 24 dB/okt)
  - level, tunda (untuk penyelarasan waktu), dan polaritas
- **Pengaturan kanal sekali klik:** potong bawah untuk speaker kecil, pemisahan bass kiri /
  treble kanan untuk laptop, stereo ke semua speaker, dan manajemen bass 80 Hz
  untuk sistem dengan subwoofer.
- **Loudness:** boost hingga +20 dB ke dalam limiter look-ahead (ZaMaximX2),
  plus **overdrive** opsional untuk saat kamu ingin lebih keras daripada yang bisa bersih,
  dan sakelar agar penggeser volume GNOME bisa melewati 100%.
- **3D:** lebar stereo plus pembatalan crosstalk ala
  Ambiophonics/RACE, yang menyebarkan suara lebih lebar daripada speaker yang berdekatan
  seperti speaker laptop.
- **Prasetel:** daftar di bagian atas jendela. Klik salah satu untuk memuatnya, atau simpan
  suara saat ini sebagai prasetel baru. Perubahan tersimpan ke prasetel aktif seiring kamu mengatur.

## Perbandingan dengan Easy Effects, JamesDSP, dll.

- **UI modern dan mudah:** satu layar yang rapi. Gambar kurva EQ, atur loudness dan
  3D, lalu pilih prasetel, tanpa mengubek-ubek panel plugin. Aplikasi ini juga
  ramah ponsel, menyesuaikan diri dari ponsel hingga layar desktop lebar.
- **Tidak ada yang perlu terus berjalan:** pemrosesan berlangsung di dalam PipeWire sendiri. Tutup
  aplikasinya dan suaramu tetap tersetel sejak login.
- **Multikanal sungguhan:** 5.1 tetap 5.1, dengan crossover, tunda,
  dan manajemen bass per kanal.
- **Tanpa putus suara:** perubahan langsung diterapkan ke filter yang sedang berjalan.
- **Mungil:** satu file Python dan satu konfigurasi PipeWire yang mudah dibaca.
- **Sulit clipping:** rantainya selalu berakhir di limiter look-ahead. Lihat di bawah.

### Kenapa aplikasi EQ lain bisa terdengar pecah

EQ dan boost bass bisa mendorong sinyal melewati 0 dBFS, batas maksimum yang bisa diputar
chip suara, dan sinyal akan clipping kecuali ditangkap limiter. Sound Tuner selalu diakhiri
dengan limiter look-ahead yang disetel di bawah 0 dBFS, sehingga boost membuat suara lebih keras alih-alih
kresek-kresek. (Overdrive sengaja melewati ini.) Pemrosesannya juga berjalan
di dalam PipeWire sendiri, bukan di proses aplikasi terpisah, jadi ada satu
program lebih sedikit yang harus mengejar waktu nyata.

## Instalasi

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

Skrip ini memasang dependensi yang belum ada dengan manajer paketmu (dnf,
apt, atau pacman). Skrip menampilkan perintah persisnya dan bertanya dulu sebelum memakai `sudo`. Setelah itu
aplikasi dipasang hanya untuk penggunamu.

Buka **Sound Tuner**, pilih perangkat keluaranmu, lalu klik **Muat** di
banner. Audio dimulai ulang sekali untuk memuat filter.

| Opsi | Fungsinya |
|---|---|
| `--yes` | pasang dependensi tanpa bertanya |
| `--no-deps` | lewati dependensi, pasang aplikasinya saja |
| `--dry-run` | tampilkan apa yang akan dipasang, tanpa mengubah apa pun |
| `--uninstall` | hapus aplikasi dan filter PipeWire (prasetelmu tetap disimpan) |

### Dependensi

Dipasangkan untukmu oleh `install.sh`:

- Alat PipeWire: `pw-cli`, `pw-dump`, `pw-record`, dan `pactl`
- Python 3 dengan GTK 4 dan libadwaita 1.5+
- Limiter ZaMaximX2 dari [zam-plugins](https://github.com/zamaudio/zam-plugins)
- Dukungan LV2 PipeWire untuk filter-chain

Kamu memerlukan desktop yang sudah menjalankan PipeWire dengan WirePlumber, yang merupakan
bawaan di Fedora, Ubuntu, Debian, dan Arch versi terkini. Nama paket Fedora
sudah diuji; di distro lain, jika nama paket berubah, skrip akan memberi tahu
apa yang kurang sehingga kamu bisa memasangnya sendiri.

## Cara kerjanya

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

Tata letak graf hanya bergantung pada kanal perangkat. Semua hal lainnya adalah
parameter, dan mematikan sebuah fitur akan menyetelnya ke nilai netral, misalnya
0 dB atau filter yang dipindahkan ke luar rentang yang bisa didengar.

Efek 3D adalah RACE yang diuraikan menjadi dua suku:
`out = own − g·D(other) + g²·D₂(own)`, dibatasi pada pita 250 Hz–5 kHz. Graf filter
PipeWire tidak bisa memuat loop umpan balik, jadi efek ini tidak sepenuhnya rekursif.

Spektrum dibaca dengan `pw-record` dari perangkat yang sedang kamu setel, dan hanya
selama jendela terbuka.

## Tips

- **Laptop:** terapkan pengaturan *Speaker kecil* (potong bawah 120 Hz) dan tambahkan
  boost 6–10 dB. Kira-kira itulah yang dilakukan peningkatan Windows seperti Dolby
  di kebanyakan laptop.
- **Subwoofer:** terapkan *Manajemen bass (80 Hz)*, lalu setel halus
  level dan tunda subwoofer sampai bass terdengar rata di tempat dudukmu.
- **3D:** duduk di tengah, setel intensitas 3D sekitar 70%, lalu geser tunda 3D sampai
  suara menyebar lebih lebar daripada speaker.
- **Overdrive** mengirim audio yang clipping ke speakermu. Gunakan secukupnya pada
  driver kecil.

## Lisensi

MIT. Lihat [LICENSE](../LICENSE).

<p align="center">
  <img src="../data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Biểu tượng Sound Tuner">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>Vắt kiệt sức mạnh của cặp loa laptop "cùi bắp", hoặc tinh chỉnh dàn âm thanh audiophile của bạn.</b></p>

<!-- languages -->
<p align="center"><sub><a href="../README.md">English</a> · <a href="README.ar.md">العربية</a> · <a href="README.bn.md">বাংলা</a> · <a href="README.cs.md">Čeština</a> · <a href="README.da.md">Dansk</a> · <a href="README.de.md">Deutsch</a> · <a href="README.el.md">Ελληνικά</a> · <a href="README.es.md">Español</a> · <a href="README.fa.md">فارسی</a> · <a href="README.fi.md">Suomi</a> · <a href="README.fr.md">Français</a> · <a href="README.he.md">עברית</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.hu.md">Magyar</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.it.md">Italiano</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.nb.md">Norsk bokmål</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.pl.md">Polski</a> · <a href="README.pt_BR.md">Português (Brasil)</a> · <a href="README.ro.md">Română</a> · <a href="README.ru.md">Русский</a> · <a href="README.sv.md">Svenska</a> · <a href="README.th.md">ไทย</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.uk.md">Українська</a> · <b>Tiếng Việt</b> · <a href="README.zh_CN.md">简体中文</a> · <a href="README.zh_TW.md">繁體中文</a></sub></p>
<!-- /languages -->


Sound Tuner là bộ EQ, phân tần và tinh chỉnh loa áp dụng cho toàn hệ thống, dành cho
máy tính Linux chạy PipeWire. Ứng dụng thêm một đầu ra ảo, **Sound Tuner**,
đặt trước bất kỳ thiết bị âm thanh nào, từ loa tích hợp của laptop đến cặp loa stereo
kèm loa sub hay cả một dàn 7.1, và mọi ứng dụng đều phát qua nó.

<img src="../data/screenshots/main.webp" alt="Sound Tuner: tạo hình đường cong EQ trên phổ đầu ra trực tiếp">

Trên điện thoại và cửa sổ hẹp, phần cài đặt chuyển vào một bảng trượt:

<img src="../data/screenshots/mobile.png" alt="Sound Tuner trên điện thoại: bộ cân bằng và bảng cài đặt" width="420">

## Tính năng

- **EQ có thể vẽ bằng tay:** quét qua biểu đồ theo bất kỳ hướng nào để vẽ
  đường cong, hoặc kéo từng điểm riêng lẻ. Đường cong đi qua các điểm của bạn
  (ứng dụng tự tính độ lợi của các bộ lọc), và bạn có thể cuộn để làm một
  dải rộng hơn hoặc hẹp hơn, hoặc nhập chính xác tần số, độ lợi và độ rộng.
  **Phổ trực tiếp** của nội dung đang phát được vẽ phía sau đường cong.
- **Định tuyến và phân tần theo từng kênh cho mọi bố cục** (2.0, 2.1, 4.0, 5.1,
  7.1, …). Với mỗi kênh loa, bạn đặt:
  - nguồn: cùng kênh, trái, phải, mono, tất cả các kênh (cho loa sub) hoặc tắt
  - bộ lọc phân tần thông cao và thông thấp (Linkwitz-Riley, 24 dB/oct)
  - mức, độ trễ (để căn chỉnh thời gian) và cực tính
- **Thiết lập kênh bằng một cú nhấp:** cắt trầm cho loa nhỏ, chia bass bên trái /
  treble bên phải cho laptop, stereo ra tất cả các loa, và quản lý bass 80 Hz
  cho hệ thống có loa siêu trầm.
- **Độ to:** tăng tới +20 dB vào một bộ giới hạn look-ahead (ZaMaximX2),
  cộng thêm **overdrive** tùy chọn khi bạn muốn to hơn mức âm thanh còn sạch,
  và một công tắc cho phép thanh âm lượng của GNOME vượt quá 100%.
- **3D:** độ rộng stereo cộng với khử xuyên âm theo kiểu
  Ambiophonics/RACE, giúp âm thanh lan rộng hơn so với các loa đặt sát nhau
  như loa laptop.
- **Cấu hình sẵn:** một danh sách ở đầu cửa sổ. Nhấp vào một mục để tải, hoặc lưu
  âm thanh hiện tại thành cấu hình mới. Các thay đổi được lưu vào cấu hình đang dùng ngay khi bạn chỉnh.

## So sánh với Easy Effects, JamesDSP, v.v.

- **Giao diện hiện đại, dễ dùng:** một màn hình gọn gàng. Vẽ đường cong EQ, chỉnh độ to và
  3D, rồi chọn một cấu hình sẵn, không cần lục lọi các bảng plugin. Ứng dụng
  cũng thân thiện với di động, thích ứng từ điện thoại đến màn hình máy tính rộng.
- **Không cần chạy nền:** việc xử lý diễn ra ngay bên trong PipeWire. Đóng
  ứng dụng và âm thanh của bạn vẫn được tinh chỉnh từ lúc đăng nhập trở đi.
- **Đa kênh thực thụ:** 5.1 vẫn là 5.1, với phân tần, độ trễ
  và quản lý bass cho từng kênh.
- **Không bị ngắt tiếng:** thay đổi được áp dụng trực tiếp lên bộ lọc đang chạy.
- **Siêu nhỏ gọn:** một tệp Python và một tệp cấu hình PipeWire dễ đọc.
- **Khó bị méo:** chuỗi xử lý luôn kết thúc bằng bộ giới hạn look-ahead. Xem bên dưới.

### Vì sao các ứng dụng EQ khác có thể nghe bị méo

EQ và tăng bass có thể đẩy tín hiệu vượt quá 0 dBFS, mức tối đa mà chip âm thanh
có thể phát, và tín hiệu sẽ bị cắt (clipping) nếu không có bộ giới hạn chặn lại. Sound Tuner luôn kết thúc
bằng bộ giới hạn look-ahead đặt dưới 0 dBFS, nên khi tăng âm thì tiếng to hơn thay vì
rè. (Overdrive cố ý bỏ qua điều này.) Việc xử lý cũng chạy
ngay bên trong PipeWire thay vì trong một tiến trình ứng dụng riêng, nên bớt được một
chương trình phải theo kịp thời gian thực.

## Cài đặt

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

Script sẽ cài các phụ thuộc còn thiếu bằng trình quản lý gói của bạn (dnf,
apt hoặc pacman). Nó hiển thị chính xác lệnh sẽ chạy và hỏi trước khi dùng `sudo`. Sau đó
nó cài ứng dụng chỉ cho người dùng của bạn.

Mở **Sound Tuner**, chọn thiết bị đầu ra và nhấp **Tải** trên
biểu ngữ. Âm thanh sẽ khởi động lại một lần để tải bộ lọc.

| Tùy chọn | Chức năng |
|---|---|
| `--yes` | cài phụ thuộc mà không hỏi |
| `--no-deps` | bỏ qua phụ thuộc, chỉ cài ứng dụng |
| `--dry-run` | hiển thị những gì sẽ được cài, không thay đổi gì |
| `--uninstall` | gỡ ứng dụng và bộ lọc PipeWire (giữ lại các cấu hình sẵn của bạn) |

### Phụ thuộc

Được `install.sh` cài giúp bạn:

- Công cụ PipeWire: `pw-cli`, `pw-dump`, `pw-record` và `pactl`
- Python 3 với GTK 4 và libadwaita 1.5+
- Bộ giới hạn ZaMaximX2 từ [zam-plugins](https://github.com/zamaudio/zam-plugins)
- Hỗ trợ LV2 của PipeWire cho filter-chain

Bạn cần một môi trường desktop đã chạy PipeWire với WirePlumber, vốn là
mặc định trên các bản Fedora, Ubuntu, Debian và Arch hiện nay. Tên gói của Fedora
đã được kiểm thử; trên các bản phân phối khác, nếu tên gói đã thay đổi, script sẽ cho bạn biết
còn thiếu gì để bạn tự cài.

## Cách hoạt động

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

Bố cục của đồ thị chỉ phụ thuộc vào các kênh của thiết bị. Mọi thứ khác đều là
tham số, và tắt một tính năng sẽ đặt nó về giá trị trung tính, chẳng hạn
0 dB hoặc một bộ lọc được dời ra ngoài dải nghe được.

Hiệu ứng 3D là RACE được khai triển thành hai số hạng:
`out = own − g·D(other) + g²·D₂(own)`, giới hạn trong dải 250 Hz–5 kHz. Đồ thị bộ lọc
của PipeWire không thể chứa vòng phản hồi, nên nó không hoàn toàn đệ quy.

Phổ được đọc bằng `pw-record` từ thiết bị bạn đang tinh chỉnh, và chỉ
khi cửa sổ đang mở.

## Mẹo

- **Laptop:** áp dụng thiết lập *Loa nhỏ* (cắt trầm 120 Hz) và tăng thêm
  6–10 dB. Đó gần như là những gì các tính năng nâng cao của Windows như Dolby làm
  trên hầu hết laptop.
- **Loa siêu trầm:** áp dụng *Quản lý bass (80 Hz)*, rồi tinh chỉnh
  mức và độ trễ của loa siêu trầm cho đến khi tiếng bass nghe đều tại chỗ ngồi của bạn.
- **3D:** ngồi chính giữa, đặt mức 3D khoảng 70%, rồi điều chỉnh độ trễ 3D cho đến khi
  âm thanh lan rộng hơn các loa.
- **Overdrive** đưa âm thanh bị cắt (clipping) ra loa của bạn. Hãy dùng tiết chế với các
  củ loa nhỏ.

## Giấy phép

MIT. Xem [LICENSE](../LICENSE).

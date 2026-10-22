<p align="center">
  <img src="../data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Sound Tuner 图标">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>让你那破笔记本喇叭发挥到极致，或者把你的发烧级音响系统调得明明白白。</b></p>

<!-- languages -->
<p align="center"><sub><a href="../README.md">English</a> · <a href="README.ar.md">العربية</a> · <a href="README.bn.md">বাংলা</a> · <a href="README.cs.md">Čeština</a> · <a href="README.da.md">Dansk</a> · <a href="README.de.md">Deutsch</a> · <a href="README.el.md">Ελληνικά</a> · <a href="README.es.md">Español</a> · <a href="README.fa.md">فارسی</a> · <a href="README.fi.md">Suomi</a> · <a href="README.fr.md">Français</a> · <a href="README.he.md">עברית</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.hu.md">Magyar</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.it.md">Italiano</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.nb.md">Norsk bokmål</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.pl.md">Polski</a> · <a href="README.pt_BR.md">Português (Brasil)</a> · <a href="README.ro.md">Română</a> · <a href="README.ru.md">Русский</a> · <a href="README.sv.md">Svenska</a> · <a href="README.th.md">ไทย</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.uk.md">Українська</a> · <a href="README.vi.md">Tiếng Việt</a> · <b>简体中文</b> · <a href="README.zh_TW.md">繁體中文</a></sub></p>
<!-- /languages -->


Sound Tuner 是一款适用于运行 PipeWire 的 Linux 桌面的全局 EQ、分频器和扬声器调校工具。
它会在任意音频设备前面添加一个虚拟输出 **Sound Tuner**——无论是笔记本内置扬声器、
带低音炮的立体声音箱，还是完整的 7.1 系统——所有应用的声音都会经过它播放。

<img src="../data/screenshots/main.webp" alt="Sound Tuner：在实时输出频谱上调整 EQ 曲线">

在手机和窄窗口上，设置会移到一个可滑出的面板中：

<img src="../data/screenshots/mobile.png" alt="手机上的 Sound Tuner：均衡器和设置面板" width="420">

## 功能

- **可以直接画的 EQ：** 在图表上朝任意方向划动即可画出曲线，也可以拖动单个点。
  曲线会精确经过你放置的点（滤波器增益由应用自动计算），你还可以滚动来加宽或收窄频段，
  或者直接输入精确的频率、增益和带宽数值。曲线后方会显示正在播放内容的**实时频谱**。
- **适用于任何布局的分声道路由和分频**（2.0、2.1、4.0、5.1、
  7.1……）。每个扬声器声道都可以设置：
  - 音源：同一声道、左、右、单声道、所有声道（用于低音炮）或关闭
  - 高通和低通分频滤波器（Linkwitz-Riley，24 dB/oct）
  - 电平、延迟（用于时间对齐）和极性
- **一键声道配置：** 小型扬声器的低切、笔记本适用的左低音 /
  右高音分离、立体声输出到所有扬声器，以及适用于带低音炮系统的 80 Hz 低音管理。
- **响度：** 在前瞻限幅器（ZaMaximX2）之前最多可提升 +20 dB，
  另有可选的**过载**，用于想要比干净声音更响的时候，
  还有一个开关可以让 GNOME 的音量滑块超过 100%。
- **3D：** 立体声宽度加上 Ambiophonics/RACE 风格的串扰消除，
  能让间距很近的扬声器（比如笔记本的）发出更宽广的声音。
- **预设：** 窗口顶部有一个列表。点击即可加载，也可以将当前声音保存为新预设。
  更改会随时保存到当前使用的预设中。

## 与 Easy Effects、JamesDSP 等的比较

- **现代、易用的界面：** 只有一个简洁的界面。画 EQ 曲线、设置响度和
  3D、选择预设，都不用在插件面板里翻来翻去。它还适配移动端，
  从手机到宽屏桌面都能自适应。
- **无需常驻后台：** 处理在 PipeWire 内部进行。关掉应用后，
  从登录开始声音就一直保持调校后的效果。
- **真正的多声道：** 5.1 依然是 5.1，支持分声道分频、延迟和低音管理。
- **不断音：** 更改会实时应用到正在运行的滤波器上。
- **小巧：** 只有一个 Python 文件和一个易读的 PipeWire 配置文件。
- **不容易削波：** 处理链的末端始终是前瞻限幅器。详见下文。

### 为什么其他 EQ 应用听起来会失真

EQ 和低音提升可能会把信号推过 0 dBFS，也就是声卡芯片能播放的最大值，
如果没有限幅器拦住，就会削波。Sound Tuner 的处理链末端始终是一个设定在 0 dBFS
以下的前瞻限幅器，所以提升只会让声音更响，而不会噼啪作响。（过载会刻意绕过这一点。）
它的处理也在 PipeWire 内部运行，而不是在单独的应用进程中，
因此少了一个需要实时跟上的程序。

## 安装

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

该脚本会用你的包管理器（dnf、apt 或 pacman）安装缺少的依赖。
在使用 `sudo` 之前，它会显示确切的命令并征求你的同意。
然后它只会为当前用户安装应用。

打开 **Sound Tuner**，选择你的输出设备，然后点击横幅中的 **Load**。
音频会重启一次以加载滤波器。

| 选项 | 作用 |
|---|---|
| `--yes` | 安装依赖时不询问 |
| `--no-deps` | 跳过依赖，只安装应用 |
| `--dry-run` | 显示将要安装的内容，不做任何更改 |
| `--uninstall` | 移除应用和 PipeWire 滤波器（保留你的预设） |

### 依赖

由 `install.sh` 为你安装：

- PipeWire 工具：`pw-cli`、`pw-dump`、`pw-record` 和 `pactl`
- 带有 GTK 4 和 libadwaita 1.5+ 的 Python 3
- 来自 [zam-plugins](https://github.com/zamaudio/zam-plugins) 的 ZaMaximX2 限幅器
- PipeWire 用于 filter-chain 的 LV2 支持

你需要一个已经运行 PipeWire 和 WirePlumber 的桌面，这在当前的 Fedora、Ubuntu、
Debian 和 Arch 上都是默认配置。Fedora 的包名已经过测试；在其他发行版上，
如果某个包名有变化，脚本会告诉你缺少什么，方便你自行安装。

## 工作原理

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

图的结构只取决于设备的声道。其他一切都是参数，关闭某个功能时会将其设为中性值，
例如 0 dB，或把滤波器移到可听范围之外。

3D 效果是将 RACE 展开到两项：
`out = own − g·D(other) + g²·D₂(own)`，频带限制在 250 Hz–5 kHz。PipeWire 的
滤波器图不能包含反馈回路，所以它并不是完全递归的。

频谱通过 `pw-record` 从你正在调校的设备读取，并且只在窗口打开时读取。

## 小贴士

- **笔记本：** 应用 *Small speakers* 配置（120 Hz 低切），再加上
  6–10 dB 的提升。这大致就是 Dolby 等 Windows 音效增强在大多数笔记本上所做的事。
- **低音炮：** 应用 *Bass management (80 Hz)*，然后微调低音炮的电平和延迟，
  直到在你的座位上听到的低音均匀为止。
- **3D：** 坐在正中间，把 3D 强度设为 70% 左右，然后调整 3D 延迟，
  直到声音扩展到扬声器之外。
- **过载**会把削波的音频送到扬声器。在小尺寸单元上请谨慎使用。

## 许可证

MIT。参见 [LICENSE](../LICENSE)。

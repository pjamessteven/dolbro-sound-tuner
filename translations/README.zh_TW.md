<p align="center">
  <img src="../data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Sound Tuner 圖示">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>把你那爛筆電喇叭榨出最大潛力，或是把你的發燒級音響系統調到剛剛好。</b></p>

<!-- languages -->
<p align="center"><sub><a href="../README.md">English</a> · <a href="README.ar.md">العربية</a> · <a href="README.bn.md">বাংলা</a> · <a href="README.cs.md">Čeština</a> · <a href="README.da.md">Dansk</a> · <a href="README.de.md">Deutsch</a> · <a href="README.el.md">Ελληνικά</a> · <a href="README.es.md">Español</a> · <a href="README.fa.md">فارسی</a> · <a href="README.fi.md">Suomi</a> · <a href="README.fr.md">Français</a> · <a href="README.he.md">עברית</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.hu.md">Magyar</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.it.md">Italiano</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.nb.md">Norsk bokmål</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.pl.md">Polski</a> · <a href="README.pt_BR.md">Português (Brasil)</a> · <a href="README.ro.md">Română</a> · <a href="README.ru.md">Русский</a> · <a href="README.sv.md">Svenska</a> · <a href="README.th.md">ไทย</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.uk.md">Українська</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.zh_CN.md">简体中文</a> · <b>繁體中文</b></sub></p>
<!-- /languages -->


Sound Tuner 是一款適用於執行 PipeWire 的 Linux 桌面的全系統 EQ、分音器與喇叭調校工具。
它會在任何音訊裝置前面加上一個虛擬輸出 **Sound Tuner**——不論是筆電內建喇叭、
搭配重低音的立體聲喇叭，還是完整的 7.1 系統——所有應用程式的聲音都會經過它播放。

<img src="../data/screenshots/main.webp" alt="Sound Tuner：在即時輸出頻譜上調整 EQ 曲線">

在手機和窄視窗上，設定會移到可滑出的面板中：

<img src="../data/screenshots/mobile.png" alt="手機上的 Sound Tuner：等化器與設定面板" width="420">

## 功能

- **可以直接畫的 EQ：** 在圖表上往任一方向劃過就能畫出曲線，也可以拖曳個別的點。
  曲線會準確通過你放的點（濾波器增益由應用程式自動算好），你還可以捲動來加寬或縮窄頻段，
  或直接輸入精確的頻率、增益與頻寬數值。曲線後方會顯示正在播放內容的**即時頻譜**。
- **適用於任何配置的分聲道路由與分音**（2.0、2.1、4.0、5.1、
  7.1……）。每個喇叭聲道都可以設定：
  - 音源：相同聲道、左、右、單聲道、所有聲道（用於重低音）或關閉
  - 高通與低通分音濾波器（Linkwitz-Riley，24 dB/oct）
  - 準位、延遲（用於時間對齊）與極性
- **一鍵聲道配置：** 小型喇叭的低切、筆電適用的左低音 /
  右高音分離、立體聲輸出到所有喇叭，以及適用於有重低音系統的 80 Hz 低音管理。
- **響度：** 在前瞻限幅器（ZaMaximX2）之前最多可增強 +20 dB，
  另有可選的**過載**，給想要比乾淨音量更大聲的時候用，
  還有一個開關可讓 GNOME 的音量滑桿超過 100%。
- **3D：** 立體聲寬度加上 Ambiophonics/RACE 風格的串音消除，
  讓間距很近的喇叭（例如筆電的）也能發出更寬廣的聲音。
- **預設集：** 視窗頂端有一個清單。點一下即可載入，也能將目前的聲音儲存為新預設集。
  變更會隨時儲存到使用中的預設集。

## 與 Easy Effects、JamesDSP 等的比較

- **現代、好上手的介面：** 只有一個簡潔的畫面。畫 EQ 曲線、設定響度與
  3D、挑選預設集，都不用在外掛面板裡翻找。它也適合行動裝置，
  從手機到寬螢幕桌面都能自動調整。
- **不需常駐執行：** 處理在 PipeWire 內部進行。關掉應用程式後，
  從登入開始聲音就一直維持調校後的效果。
- **真正的多聲道：** 5.1 依然是 5.1，支援分聲道分音、延遲與低音管理。
- **不會斷音：** 變更會即時套用到正在執行的濾波器。
- **輕巧：** 只有一個 Python 檔案和一個易讀的 PipeWire 設定檔。
- **不容易削波：** 處理鏈的最後一定是前瞻限幅器。詳見下文。

### 為什麼其他 EQ 應用程式聽起來會失真

EQ 和低音增強可能會把訊號推過 0 dBFS，也就是音效晶片能播放的最大值，
如果沒有限幅器擋下來，就會削波。Sound Tuner 的處理鏈最後一定是設定在 0 dBFS
以下的前瞻限幅器，所以增強只會讓聲音更大，而不會劈啪作響。（過載會刻意繞過這一點。）
它的處理也是在 PipeWire 內部執行，而不是在獨立的應用程式行程中，
因此少了一個必須即時跟上的程式。

## 安裝

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

此指令稿會用你的套件管理器（dnf、apt 或 pacman）安裝缺少的相依套件。
在使用 `sudo` 之前，它會顯示確切的指令並詢問你。
接著只為目前使用者安裝應用程式。

開啟 **Sound Tuner**，選擇你的輸出裝置，然後按一下橫幅中的 **Load**。
音訊會重新啟動一次以載入濾波器。

| 選項 | 作用 |
|---|---|
| `--yes` | 安裝相依套件時不詢問 |
| `--no-deps` | 略過相依套件，只安裝應用程式 |
| `--dry-run` | 顯示將會安裝的內容，不做任何變更 |
| `--uninstall` | 移除應用程式與 PipeWire 濾波器（保留你的預設集） |

### 相依套件

由 `install.sh` 替你安裝：

- PipeWire 工具：`pw-cli`、`pw-dump`、`pw-record` 與 `pactl`
- 搭配 GTK 4 與 libadwaita 1.5+ 的 Python 3
- 來自 [zam-plugins](https://github.com/zamaudio/zam-plugins) 的 ZaMaximX2 限幅器
- PipeWire 用於 filter-chain 的 LV2 支援

你需要一個已經在執行 PipeWire 與 WirePlumber 的桌面，這在目前的 Fedora、Ubuntu、
Debian 與 Arch 上都是預設配置。Fedora 的套件名稱已經過測試；在其他發行版上，
如果套件名稱有變更，指令稿會告訴你缺少什麼，方便你自行安裝。

## 運作原理

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

圖的結構只取決於裝置的聲道。其他一切都是參數，關閉某項功能時會將它設為中性值，
例如 0 dB，或把濾波器移到可聽範圍之外。

3D 效果是將 RACE 展開到兩項：
`out = own − g·D(other) + g²·D₂(own)`，頻帶限制在 250 Hz–5 kHz。PipeWire 的
濾波器圖無法包含回授迴路，所以它並非完全遞迴。

頻譜是透過 `pw-record` 從你正在調校的裝置讀取，而且只在視窗開啟時讀取。

## 小訣竅

- **筆電：** 套用 *Small speakers* 配置（120 Hz 低切），再加上
  6–10 dB 的增強。這大致就是 Dolby 等 Windows 音效強化功能在多數筆電上所做的事。
- **重低音：** 套用 *Bass management (80 Hz)*，然後微調重低音的準位與延遲，
  直到在你的座位上聽到的低音均勻為止。
- **3D：** 坐在正中間，把 3D 強度設為約 70%，然後調整 3D 延遲，
  直到聲音擴展到喇叭之外。
- **過載**會把削波的音訊送到喇叭。在小尺寸單體上請斟酌使用。

## 授權

MIT。請參閱 [LICENSE](../LICENSE)。

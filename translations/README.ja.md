<p align="center">
  <img src="../data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Sound Tuner のアイコン">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>ショボいノートPCのスピーカーを限界まで鳴らすもよし、こだわりのオーディオシステムを細かく追い込むもよし。</b></p>

<!-- languages -->
<p align="center"><sub><a href="../README.md">English</a> · <a href="README.ar.md">العربية</a> · <a href="README.bn.md">বাংলা</a> · <a href="README.cs.md">Čeština</a> · <a href="README.da.md">Dansk</a> · <a href="README.de.md">Deutsch</a> · <a href="README.el.md">Ελληνικά</a> · <a href="README.es.md">Español</a> · <a href="README.fa.md">فارسی</a> · <a href="README.fi.md">Suomi</a> · <a href="README.fr.md">Français</a> · <a href="README.he.md">עברית</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.hu.md">Magyar</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.it.md">Italiano</a> · <b>日本語</b> · <a href="README.ko.md">한국어</a> · <a href="README.nb.md">Norsk bokmål</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.pl.md">Polski</a> · <a href="README.pt_BR.md">Português (Brasil)</a> · <a href="README.ro.md">Română</a> · <a href="README.ru.md">Русский</a> · <a href="README.sv.md">Svenska</a> · <a href="README.th.md">ไทย</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.uk.md">Українська</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.zh_CN.md">简体中文</a> · <a href="README.zh_TW.md">繁體中文</a></sub></p>
<!-- /languages -->


Sound Tuner は、PipeWire で動作する Linux デスクトップ向けの、システム全体に効く
EQ・クロスオーバー・スピーカーチューナーです。あらゆるサウンドデバイスの手前に
仮想出力 **Sound Tuner** を追加します。ノートPCの内蔵スピーカーから、
サブウーファー付きのステレオペア、本格的な 7.1 環境まで対応し、すべてのアプリの音が
これを通って再生されます。

<img src="../data/screenshots/main.webp" alt="Sound Tuner: 再生中の出力スペクトルに重ねて EQ カーブを調整しているところ">

スマートフォンや幅の狭いウィンドウでは、設定はスライド式のパネルに移動します。

<img src="../data/screenshots/mobile.png" alt="スマートフォン上の Sound Tuner: イコライザーと設定パネル" width="420">

## 機能

- **描ける EQ:** グラフ上をどちらの方向にでもなぞってカーブを描いたり、
  個々のポイントをドラッグしたりできます。カーブは置いたポイントを必ず通り
  （フィルターのゲインはアプリが計算します）、スクロールでバンドの幅を広げたり
  狭めたりしたり、周波数・ゲイン・幅を正確な値で入力したりもできます。
  カーブの背後には、再生中の音の**リアルタイムスペクトル**が表示されます。
- **あらゆる構成に対応したチャンネルごとのルーティングとクロスオーバー**（2.0、2.1、4.0、5.1、
  7.1 など）。スピーカーの各チャンネルについて次の項目を設定できます。
  - ソース: 同じチャンネル、左、右、モノラル、全チャンネル（サブウーファー用）、またはオフ
  - ハイパス／ローパスのクロスオーバーフィルター（Linkwitz-Riley、24 dB/oct）
  - レベル、ディレイ（タイムアライメント用）、極性
- **ワンクリックのチャンネル構成:** 小型スピーカー向けのローカット、ノートPC向けの
  左が低音／右が高音の分割、全スピーカーへのステレオ出力、サブウーファーのある
  システム向けの 80 Hz ベースマネジメント。
- **ラウドネス:** 先読みリミッター（ZaMaximX2）の手前で最大 +20 dB のブーストが可能。
  さらに、クリーンに出せる以上の音量が欲しいときのためのオプションの**オーバードライブ**と、
  GNOME の音量スライダーで 100% を超えられるようにするスイッチも備えています。
- **3D:** ステレオ幅の調整に加え、Ambiophonics/RACE 方式のクロストークキャンセルにより、
  ノートPCのように間隔の狭いスピーカーでも音を広く広げます。
- **プリセット:** ウィンドウ上部に一覧が表示されます。クリックで読み込み、
  現在のサウンドを新しいプリセットとして保存することもできます。変更は使用中の
  プリセットにその都度保存されます。

## Easy Effects や JamesDSP などとの違い

- **モダンで簡単な UI:** すっきりした 1 画面だけ。プラグインのパネルを掘り進めなくても、
  EQ カーブを描き、ラウドネスと 3D を設定し、プリセットを選べます。
  モバイルにも対応し、スマートフォンから横長のデスクトップ画面まで画面に合わせて変化します。
- **常駐させるものはなし:** 処理は PipeWire 自体の中で行われます。アプリを閉じても、
  ログイン直後からずっとチューニングされた音のままです。
- **本物のマルチチャンネル:** 5.1 は 5.1 のまま。チャンネルごとのクロスオーバー、ディレイ、
  ベースマネジメントに対応します。
- **音切れなし:** 変更は動作中のフィルターにリアルタイムで反映されます。
- **超軽量:** Python ファイル 1 つと、読みやすい PipeWire 設定ファイル 1 つだけ。
- **クリップしにくい:** 処理チェーンの最後は必ず先読みリミッターです。詳しくは下記を参照してください。

### ほかの EQ アプリで音が歪むことがある理由

EQ や低音ブーストは、サウンドチップが再生できる上限である 0 dBFS を超えて信号を
押し上げることがあり、リミッターで抑えない限りクリップしてしまいます。
Sound Tuner は必ず 0 dBFS より低く設定した先読みリミッターで処理を締めくくるため、
ブーストしてもバリバリ割れずに音量が上がります（オーバードライブは意図的にこれを回避します）。
また、処理は別のアプリプロセスではなく PipeWire 自体の中で行われるので、
リアルタイムに追従しなければならないプログラムが 1 つ減ります。

## インストール

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

このスクリプトは、足りない依存パッケージをパッケージマネージャー（dnf、
apt、pacman）でインストールします。`sudo` を使う前に、実行するコマンドをそのまま表示して
確認を求めます。その後、アプリを現在のユーザーにのみインストールします。

**Sound Tuner** を開き、出力デバイスを選んで、バナーの **Load** をクリックします。
フィルターを読み込むため、オーディオが一度再起動します。

| オプション | 内容 |
|---|---|
| `--yes` | 確認なしで依存パッケージをインストール |
| `--no-deps` | 依存パッケージを省略し、アプリのみインストール |
| `--dry-run` | インストールされる内容を表示するだけで、何も変更しない |
| `--uninstall` | アプリと PipeWire フィルターを削除（プリセットは残ります） |

### 依存パッケージ

`install.sh` が自動でインストールします。

- PipeWire ツール: `pw-cli`、`pw-dump`、`pw-record`、`pactl`
- GTK 4 と libadwaita 1.5 以降を備えた Python 3
- [zam-plugins](https://github.com/zamaudio/zam-plugins) の ZaMaximX2 リミッター
- filter-chain 用の PipeWire の LV2 サポート

PipeWire と WirePlumber がすでに動作しているデスクトップが必要です。これは現在の
Fedora、Ubuntu、Debian、Arch ではデフォルトです。Fedora のパッケージ名は
テスト済みです。ほかのディストリビューションでパッケージ名が変わっている場合は、
足りないものをスクリプトが表示するので、自分でインストールできます。

## 仕組み

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

グラフの構造はデバイスのチャンネル構成だけで決まります。それ以外はすべて
パラメーターで、機能をオフにすると、0 dB やフィルターを可聴域の外に移すといった
中立の値に設定されます。

3D 効果は、RACE を 2 項まで展開したものです:
`out = own − g·D(other) + g²·D₂(own)`。帯域は 250 Hz～5 kHz に制限されています。
PipeWire のフィルターグラフにはフィードバックループを含められないため、完全な再帰処理ではありません。

スペクトルは、チューニング中のデバイスから `pw-record` で読み取ります。
読み取るのはウィンドウが開いている間だけです。

## ヒント

- **ノートPC:** *Small speakers*（120 Hz ローカット）構成を適用し、
  6～10 dB のブーストを加えます。これは、ほとんどのノートPCで Dolby などの
  Windows の音響強化機能がやっていることとほぼ同じです。
- **サブウーファー:** *Bass management (80 Hz)* を適用してから、座る位置で低音が均一に
  聞こえるまでサブウーファーのレベルとディレイを微調整します。
- **3D:** 中央に座り、3D の強さを 70% 程度に設定してから、音がスピーカーより
  広く広がるまで 3D ディレイを動かします。
- **オーバードライブ**はクリップした音をスピーカーに送ります。小さなドライバーでは控えめに使ってください。

## ライセンス

MIT。[LICENSE](../LICENSE) を参照してください。

<p align="center">
  <img src="../data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Sound Tuner 아이콘">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>구린 노트북 스피커를 한계까지 쥐어짜거나, 오디오파일급 사운드 시스템을 섬세하게 튜닝하세요.</b></p>

<!-- languages -->
<p align="center"><sub><a href="../README.md">English</a> · <a href="README.ar.md">العربية</a> · <a href="README.bn.md">বাংলা</a> · <a href="README.cs.md">Čeština</a> · <a href="README.da.md">Dansk</a> · <a href="README.de.md">Deutsch</a> · <a href="README.el.md">Ελληνικά</a> · <a href="README.es.md">Español</a> · <a href="README.fa.md">فارسی</a> · <a href="README.fi.md">Suomi</a> · <a href="README.fr.md">Français</a> · <a href="README.he.md">עברית</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.hu.md">Magyar</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.it.md">Italiano</a> · <a href="README.ja.md">日本語</a> · <b>한국어</b> · <a href="README.nb.md">Norsk bokmål</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.pl.md">Polski</a> · <a href="README.pt_BR.md">Português (Brasil)</a> · <a href="README.ro.md">Română</a> · <a href="README.ru.md">Русский</a> · <a href="README.sv.md">Svenska</a> · <a href="README.th.md">ไทย</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.uk.md">Українська</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.zh_CN.md">简体中文</a> · <a href="README.zh_TW.md">繁體中文</a></sub></p>
<!-- /languages -->


Sound Tuner는 PipeWire를 사용하는 Linux 데스크톱용 시스템 전역 EQ, 크로스오버,
스피커 튜너입니다. 노트북 내장 스피커부터 서브우퍼가 딸린 스테레오 한 쌍,
완전한 7.1 구성까지, 어떤 사운드 장치 앞에든 가상 출력 **Sound Tuner**를 추가하며
모든 앱의 소리가 이를 거쳐 재생됩니다.

<img src="../data/screenshots/main.webp" alt="Sound Tuner: 실시간 출력 스펙트럼 위에서 EQ 커브를 조정하는 모습">

휴대폰이나 좁은 창에서는 설정이 밀어서 여는 패널로 이동합니다.

<img src="../data/screenshots/mobile.png" alt="휴대폰에서 실행한 Sound Tuner: 이퀄라이저와 설정 패널" width="420">

## 기능

- **그려서 쓰는 EQ:** 그래프 위를 어느 방향으로든 쓸어서 커브를 그리거나,
  개별 포인트를 드래그하세요. 커브는 지정한 포인트를 정확히 지나가며
  (필터 게인은 앱이 알아서 계산합니다), 스크롤로 밴드를 넓히거나 좁히고,
  주파수·게인·폭 값을 직접 입력할 수도 있습니다. 커브 뒤에는 재생 중인 소리의
  **실시간 스펙트럼**이 표시됩니다.
- **어떤 구성이든 채널별 라우팅과 크로스오버** (2.0, 2.1, 4.0, 5.1,
  7.1, …). 스피커 채널마다 다음을 설정할 수 있습니다.
  - 소스: 같은 채널, 왼쪽, 오른쪽, 모노, 모든 채널(서브우퍼용) 또는 끔
  - 하이패스 및 로우패스 크로스오버 필터 (Linkwitz-Riley, 24 dB/oct)
  - 레벨, 지연(타임 얼라인먼트용), 극성
- **원클릭 채널 구성:** 소형 스피커용 로우 컷, 노트북용 왼쪽 저음 /
  오른쪽 고음 분리, 모든 스피커에 스테레오, 서브우퍼가 있는 시스템용 80 Hz
  베이스 매니지먼트.
- **라우드니스:** 룩어헤드 리미터(ZaMaximX2) 앞단에서 최대 +20 dB 부스트,
  깨끗하게 낼 수 있는 것보다 더 크게 듣고 싶을 때를 위한 선택형 **오버드라이브**,
  그리고 GNOME 음량 슬라이더가 100%를 넘을 수 있게 해 주는 스위치.
- **3D:** 스테레오 폭 조절과 함께 Ambiophonics/RACE 방식의 크로스토크 캔슬레이션으로,
  노트북처럼 간격이 좁은 스피커에서도 소리를 더 넓게 퍼뜨립니다.
- **프리셋:** 창 상단의 목록에서 클릭하면 불러오고, 현재 사운드를 새 프리셋으로
  저장할 수도 있습니다. 변경 사항은 사용 중인 프리셋에 바로바로 저장됩니다.

## Easy Effects, JamesDSP 등과 비교하면

- **현대적이고 쉬운 UI:** 깔끔한 화면 하나. 플러그인 패널을 뒤질 필요 없이 EQ 커브를
  그리고, 라우드니스와 3D를 설정하고, 프리셋을 고르면 끝입니다. 모바일 친화적이라
  휴대폰부터 넓은 데스크톱 화면까지 알맞게 맞춰집니다.
- **계속 띄워 둘 필요 없음:** 처리는 PipeWire 내부에서 이루어집니다. 앱을 닫아도
  로그인한 순간부터 튜닝된 소리가 그대로 유지됩니다.
- **진짜 멀티채널:** 5.1은 5.1 그대로, 채널별 크로스오버, 지연,
  베이스 매니지먼트를 지원합니다.
- **끊김 없음:** 변경 사항이 실행 중인 필터에 실시간으로 적용됩니다.
- **초경량:** Python 파일 하나와 읽기 쉬운 PipeWire 설정 파일 하나가 전부입니다.
- **클리핑이 어려움:** 처리 체인의 끝은 언제나 룩어헤드 리미터입니다. 아래를 참고하세요.

### 다른 EQ 앱에서 소리가 찌그러지는 이유

EQ와 저음 부스트는 사운드 칩이 낼 수 있는 최대치인 0 dBFS를 넘어 신호를 밀어 올릴 수
있고, 리미터가 잡아 주지 않으면 클리핑이 발생합니다. Sound Tuner는 항상 0 dBFS보다
낮게 설정된 룩어헤드 리미터로 끝나기 때문에, 부스트하면 지직거리는 대신 소리가
커집니다. (오버드라이브는 일부러 이를 우회합니다.) 또한 처리가 별도의 앱 프로세스가
아니라 PipeWire 내부에서 이루어지므로, 실시간으로 따라잡아야 하는 프로그램이
하나 줄어듭니다.

## 설치

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

스크립트는 누락된 의존성을 패키지 관리자(dnf, apt 또는 pacman)로 설치합니다.
`sudo`를 사용하기 전에 실행할 명령어를 그대로 보여 주고 확인을 받습니다.
그런 다음 앱을 현재 사용자에게만 설치합니다.

**Sound Tuner**를 열고 출력 장치를 선택한 다음, 배너의 **Load**를 클릭하세요.
필터를 로드하기 위해 오디오가 한 번 다시 시작됩니다.

| 옵션 | 동작 |
|---|---|
| `--yes` | 묻지 않고 의존성 설치 |
| `--no-deps` | 의존성은 건너뛰고 앱만 설치 |
| `--dry-run` | 설치될 항목만 보여 주고 아무것도 변경하지 않음 |
| `--uninstall` | 앱과 PipeWire 필터 제거 (프리셋은 유지) |

### 의존성

`install.sh`가 대신 설치해 줍니다.

- PipeWire 도구: `pw-cli`, `pw-dump`, `pw-record`, `pactl`
- GTK 4와 libadwaita 1.5 이상을 갖춘 Python 3
- [zam-plugins](https://github.com/zamaudio/zam-plugins)의 ZaMaximX2 리미터
- filter-chain용 PipeWire LV2 지원

PipeWire와 WirePlumber가 이미 실행 중인 데스크톱이 필요하며, 이는 최신 Fedora,
Ubuntu, Debian, Arch의 기본 구성입니다. Fedora 패키지 이름은 테스트를 거쳤습니다.
다른 배포판에서 패키지 이름이 바뀐 경우, 스크립트가 무엇이 누락되었는지 알려 주므로
직접 설치할 수 있습니다.

## 작동 방식

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

그래프의 구조는 오직 장치의 채널 구성에 따라 결정됩니다. 나머지는 모두 매개변수이며,
기능을 끄면 0 dB나 가청 범위 밖으로 옮긴 필터처럼 중립적인 값으로 설정됩니다.

3D 효과는 RACE를 두 항까지 전개한 것입니다:
`out = own − g·D(other) + g²·D₂(own)`, 대역은 250 Hz–5 kHz로 제한됩니다. PipeWire의
필터 그래프는 피드백 루프를 포함할 수 없으므로 완전한 재귀 방식은 아닙니다.

스펙트럼은 튜닝 중인 장치에서 `pw-record`로 읽어 오며, 창이 열려 있는 동안에만
읽습니다.

## 팁

- **노트북:** *Small speakers* 구성(120 Hz 로우 컷)을 적용하고
  6–10 dB 부스트를 더하세요. 대부분의 노트북에서 Dolby 같은 Windows 음향 향상 기능이
  하는 일과 거의 같습니다.
- **서브우퍼:** *Bass management (80 Hz)*를 적용한 다음, 앉은 자리에서 저음이 고르게
  들릴 때까지 서브우퍼의 레벨과 지연을 미세 조정하세요.
- **3D:** 가운데에 앉아 3D 강도를 약 70%로 설정한 뒤, 소리가 스피커보다 넓게
  퍼질 때까지 3D 지연을 조절하세요.
- **오버드라이브**는 클리핑된 오디오를 스피커로 보냅니다. 작은 드라이버에서는 적당히 사용하세요.

## 라이선스

MIT. [LICENSE](../LICENSE)를 참고하세요.

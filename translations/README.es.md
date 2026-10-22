<p align="center">
  <img src="../data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Icono de Sound Tuner">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>Exprime al máximo los altavoces cutres de tu portátil, o afina hasta el último detalle tu equipo de audiófilo.</b></p>

<!-- languages -->
<p align="center"><sub><a href="../README.md">English</a> · <a href="README.ar.md">العربية</a> · <a href="README.bn.md">বাংলা</a> · <a href="README.cs.md">Čeština</a> · <a href="README.da.md">Dansk</a> · <a href="README.de.md">Deutsch</a> · <a href="README.el.md">Ελληνικά</a> · <b>Español</b> · <a href="README.fa.md">فارسی</a> · <a href="README.fi.md">Suomi</a> · <a href="README.fr.md">Français</a> · <a href="README.he.md">עברית</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.hu.md">Magyar</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.it.md">Italiano</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.nb.md">Norsk bokmål</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.pl.md">Polski</a> · <a href="README.pt_BR.md">Português (Brasil)</a> · <a href="README.ro.md">Română</a> · <a href="README.ru.md">Русский</a> · <a href="README.sv.md">Svenska</a> · <a href="README.th.md">ไทย</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.uk.md">Українська</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.zh_CN.md">简体中文</a> · <a href="README.zh_TW.md">繁體中文</a></sub></p>
<!-- /languages -->


Sound Tuner es un ecualizador, crossover y afinador de altavoces para todo el
sistema, pensado para escritorios Linux con PipeWire. Añade una salida
virtual, **Sound Tuner**, delante de cualquier dispositivo de sonido, desde
los altavoces integrados de un portátil hasta una pareja estéreo con
subwoofer o un equipo 7.1 completo, y todas las aplicaciones suenan a través
de ella.

<img src="../data/screenshots/main.webp" alt="Sound Tuner: dando forma a la curva de ecualización sobre el espectro de salida en directo">

En teléfonos y ventanas estrechas, los ajustes pasan a un panel deslizante:

<img src="../data/screenshots/mobile.png" alt="Sound Tuner en un teléfono: ecualizador y panel de ajustes" width="420">

## Características

- **Un ecualizador que se dibuja:** pasa el cursor por la gráfica en
  cualquier dirección para pintar la curva, o arrastra puntos individuales. La
  curva pasa por tus puntos (la aplicación calcula las ganancias de los
  filtros por ti), y puedes desplazar la rueda para ensanchar o estrechar una
  banda, o escribir valores exactos de frecuencia, ganancia y anchura. Detrás
  de la curva se dibuja un **espectro en directo** de lo que está sonando.
- **Enrutamiento y crossovers por canal para cualquier disposición** (2.0,
  2.1, 4.0, 5.1, 7.1…). Para cada canal de altavoz defines:
  - la fuente: mismo canal, izquierdo, derecho, mono, todos los canales (para un subwoofer) o desactivado
  - filtros de cruce paso alto y paso bajo (Linkwitz-Riley, 24 dB/oct)
  - nivel, retardo (para la alineación temporal) y polaridad
- **Configuraciones de canales con un clic:** corte de graves para altavoces
  pequeños, división graves a la izquierda / agudos a la derecha para
  portátiles, estéreo a todos los altavoces y gestión de graves a 80 Hz para
  equipos con subwoofer.
- **Sonoridad:** hasta +20 dB de realce hacia un limitador con anticipación
  (ZaMaximX2), además de **saturación** opcional para cuando lo quieres más
  alto de lo que permite un sonido limpio, y un interruptor para que el
  control de volumen de GNOME pase del 100 %.
- **3D:** anchura estéreo más cancelación de diafonía al estilo
  Ambiophonics/RACE, que abre el sonido más allá de altavoces muy juntos, como
  los de un portátil.
- **Preajustes:** una lista en la parte superior de la ventana. Haz clic en
  uno para cargarlo, o guarda el sonido actual como uno nuevo. Los cambios se
  van guardando en el preajuste activo sobre la marcha.

## Comparación con Easy Effects, JamesDSP, etc.

- **Interfaz moderna y sencilla:** una sola pantalla limpia. Dibuja la curva
  de ecualización, ajusta la sonoridad y el 3D y elige un preajuste, sin
  pelearte con paneles de plugins. También está pensada para móviles y se
  adapta desde teléfonos hasta pantallas de escritorio anchas.
- **Nada que mantener abierto:** el procesamiento se ejecuta dentro del
  propio PipeWire. Cierra la aplicación y tu sonido sigue afinado desde que
  inicias sesión.
- **Multicanal de verdad:** el 5.1 sigue siendo 5.1, con crossovers,
  retardos y gestión de graves por canal.
- **Sin cortes:** los cambios se aplican en directo al filtro en ejecución.
- **Diminuto:** un archivo de Python y una configuración de PipeWire legible.
- **Difícil de saturar:** la cadena siempre termina en un limitador con
  anticipación. Más detalles abajo.

### Por qué otras aplicaciones de ecualización pueden sonar distorsionadas

El ecualizador y los realces de graves pueden llevar la señal por encima de
0 dBFS, lo máximo que puede reproducir el chip de sonido, y se recorta a
menos que un limitador la frene. Sound Tuner siempre termina con un limitador
con anticipación ajustado por debajo de 0 dBFS, así que los realces suben el
volumen en vez de crepitar. (La saturación se salta esto a propósito.) Además,
su procesamiento se ejecuta dentro del propio PipeWire en lugar de en un
proceso de aplicación aparte, así que hay un programa menos que tiene que
seguir el ritmo en tiempo real.

## Instalación

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

El script instala las dependencias que falten con tu gestor de paquetes (dnf,
apt o pacman). Muestra el comando exacto y pregunta antes de usar `sudo`.
Después instala la aplicación solo para tu usuario.

Abre **Sound Tuner**, elige tu dispositivo de salida y haz clic en
**Cargar** en el aviso. El audio se reinicia una vez para cargar el filtro.

| Opción | Qué hace |
|---|---|
| `--yes` | instala las dependencias sin preguntar |
| `--no-deps` | omite las dependencias e instala solo la aplicación |
| `--dry-run` | muestra lo que se instalaría, sin cambiar nada |
| `--uninstall` | elimina la aplicación y el filtro de PipeWire (conserva tus preajustes) |

### Dependencias

`install.sh` las instala por ti:

- Herramientas de PipeWire: `pw-cli`, `pw-dump`, `pw-record` y `pactl`
- Python 3 con GTK 4 y libadwaita 1.5+
- El limitador ZaMaximX2 de [zam-plugins](https://github.com/zamaudio/zam-plugins)
- La compatibilidad con LV2 de PipeWire para filter-chain

Necesitas un escritorio que ya use PipeWire con WirePlumber, que es lo
predeterminado en las versiones actuales de Fedora, Ubuntu, Debian y Arch.
Los nombres de paquetes de Fedora están probados; en otras distribuciones, si
algún nombre de paquete ha cambiado, el script te dice qué falta para que lo
instales tú mismo.

## Cómo funciona

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

La estructura del grafo depende solo de los canales del dispositivo. Todo lo
demás es un parámetro, y desactivar una función lo pone en un valor neutro,
como 0 dB o un filtro desplazado fuera del rango audible.

El efecto 3D es RACE desarrollado en dos términos:
`out = own − g·D(other) + g²·D₂(own)`, limitado a la banda de 250 Hz–5 kHz.
Los grafos de filtros de PipeWire no pueden contener bucles de
realimentación, así que no es totalmente recursivo.

El espectro se lee con `pw-record` del dispositivo que estás afinando, y solo
mientras la ventana está abierta.

## Consejos

- **Portátiles:** aplica la configuración *Altavoces pequeños* (corte de
  graves a 120 Hz) y añade entre 6 y 10 dB de realce. Es más o menos lo que
  hacen las mejoras de sonido de Windows, como Dolby, en la mayoría de
  portátiles.
- **Subwoofer:** aplica *Gestión de graves (80 Hz)* y después ajusta el nivel
  y el retardo del subwoofer hasta que los graves suenen uniformes en tu
  sitio.
- **3D:** siéntate en el centro, pon la intensidad 3D en torno al 70 % y
  luego mueve el retardo 3D hasta que el sonido se abra más allá de los
  altavoces.
- **La saturación** envía audio recortado a tus altavoces. Úsala con
  moderación en altavoces pequeños.

## Licencia

MIT. Consulta [LICENSE](../LICENSE).

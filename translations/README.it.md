<p align="center">
  <img src="../data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Icona di Sound Tuner">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>Spremi al massimo quelle schifezze di altoparlanti del tuo portatile, o regola fino all'ultimo dettaglio il tuo impianto da audiofilo.</b></p>

<!-- languages -->
<p align="center"><sub><a href="../README.md">English</a> · <a href="README.ar.md">العربية</a> · <a href="README.bn.md">বাংলা</a> · <a href="README.cs.md">Čeština</a> · <a href="README.da.md">Dansk</a> · <a href="README.de.md">Deutsch</a> · <a href="README.el.md">Ελληνικά</a> · <a href="README.es.md">Español</a> · <a href="README.fa.md">فارسی</a> · <a href="README.fi.md">Suomi</a> · <a href="README.fr.md">Français</a> · <a href="README.he.md">עברית</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.hu.md">Magyar</a> · <a href="README.id.md">Bahasa Indonesia</a> · <b>Italiano</b> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.nb.md">Norsk bokmål</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.pl.md">Polski</a> · <a href="README.pt_BR.md">Português (Brasil)</a> · <a href="README.ro.md">Română</a> · <a href="README.ru.md">Русский</a> · <a href="README.sv.md">Svenska</a> · <a href="README.th.md">ไทย</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.uk.md">Українська</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.zh_CN.md">简体中文</a> · <a href="README.zh_TW.md">繁體中文</a></sub></p>
<!-- /languages -->


Sound Tuner è un equalizzatore, crossover e sintonizzatore per altoparlanti a
livello di sistema, per desktop Linux con PipeWire. Aggiunge un'uscita
virtuale, **Sound Tuner**, davanti a qualsiasi dispositivo audio, dagli
altoparlanti integrati di un portatile a una coppia stereo con subwoofer o a
un impianto 7.1 completo, e tutte le app suonano attraverso di essa.

<img src="../data/screenshots/main.webp" alt="Sound Tuner: modellazione della curva di equalizzazione sullo spettro di uscita in tempo reale">

Su telefoni e finestre strette le impostazioni si spostano in un pannello a scomparsa:

<img src="../data/screenshots/mobile.png" alt="Sound Tuner su un telefono: equalizzatore e pannello delle impostazioni" width="420">

## Funzionalità

- **Un equalizzatore da disegnare:** passa sul grafico in qualsiasi direzione
  per dipingere la curva, oppure trascina singoli punti. La curva passa per i
  tuoi punti (l'app calcola i guadagni dei filtri al posto tuo), e puoi
  scorrere per allargare o restringere una banda, oppure digitare valori
  esatti di frequenza, guadagno e ampiezza. Dietro la curva viene disegnato
  uno **spettro in tempo reale** di ciò che è in riproduzione.
- **Instradamento e crossover per canale per qualsiasi configurazione** (2.0,
  2.1, 4.0, 5.1, 7.1, …). Per ogni canale degli altoparlanti imposti:
  - la sorgente: stesso canale, sinistro, destro, mono, tutti i canali (per un subwoofer) o disattivato
  - filtri crossover passa-alto e passa-basso (Linkwitz-Riley, 24 dB/ott)
  - livello, ritardo (per l'allineamento temporale) e polarità
- **Configurazioni dei canali con un clic:** taglio dei bassi per
  altoparlanti piccoli, divisione bassi a sinistra / alti a destra per i
  portatili, stereo su tutti gli altoparlanti e gestione dei bassi a 80 Hz
  per impianti con subwoofer.
- **Loudness:** fino a +20 dB di amplificazione verso un limiter con
  look-ahead (ZaMaximX2), più un **overdrive** opzionale per quando lo vuoi
  più forte di quanto consenta un suono pulito, e un interruttore per far
  superare il 100% al cursore del volume di GNOME.
- **3D:** ampiezza stereo più cancellazione del crosstalk in stile
  Ambiophonics/RACE, che allarga il suono oltre altoparlanti ravvicinati come
  quelli di un portatile.
- **Preset:** un elenco nella parte alta della finestra. Fai clic su uno per
  caricarlo, oppure salva il suono attuale come nuovo preset. Le modifiche
  vengono salvate nel preset attivo man mano.

## Confronto con Easy Effects, JamesDSP, ecc.

- **Interfaccia moderna e semplice:** un'unica schermata pulita. Disegna la
  curva dell'equalizzatore, regola loudness e 3D e scegli un preset, senza
  scavare tra pannelli di plugin. È anche adatta ai dispositivi mobili e si
  adatta dai telefoni fino agli schermi desktop più larghi.
- **Niente da tenere aperto:** l'elaborazione avviene direttamente in
  PipeWire. Chiudi l'app e il tuo suono resta regolato fin dall'accesso.
- **Vero multicanale:** il 5.1 resta 5.1, con crossover, ritardi e gestione
  dei bassi per canale.
- **Nessuna interruzione:** le modifiche si applicano in tempo reale al
  filtro in esecuzione.
- **Minuscolo:** un solo file Python e una configurazione PipeWire leggibile.
- **Difficile da far distorcere:** la catena termina sempre con un limiter
  con look-ahead. Vedi sotto.

### Perché altre app di equalizzazione possono suonare distorte

L'equalizzazione e il potenziamento dei bassi possono spingere il segnale
oltre 0 dBFS, il massimo che il chip audio può riprodurre, e il segnale va in
clipping a meno che un limiter non lo intercetti. Sound Tuner termina sempre
con un limiter con look-ahead impostato sotto 0 dBFS, così le amplificazioni
alzano il volume invece di gracchiare. (L'overdrive aggira deliberatamente
questo limiter.) Inoltre l'elaborazione avviene direttamente in PipeWire
anziché in un processo applicativo separato, quindi c'è un programma in meno
che deve tenere il passo in tempo reale.

## Installazione

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

Lo script installa le dipendenze mancanti con il tuo gestore di pacchetti
(dnf, apt o pacman). Mostra il comando esatto e chiede conferma prima di
usare `sudo`. Poi installa l'app solo per il tuo utente.

Apri **Sound Tuner**, scegli il dispositivo di uscita e fai clic su
**Carica** nel banner. L'audio si riavvia una volta per caricare il filtro.

| Opzione | Cosa fa |
|---|---|
| `--yes` | installa le dipendenze senza chiedere |
| `--no-deps` | salta le dipendenze, installa solo l'app |
| `--dry-run` | mostra cosa verrebbe installato, senza modificare nulla |
| `--uninstall` | rimuove l'app e il filtro PipeWire (mantiene i tuoi preset) |

### Dipendenze

Installate per te da `install.sh`:

- Strumenti di PipeWire: `pw-cli`, `pw-dump`, `pw-record` e `pactl`
- Python 3 con GTK 4 e libadwaita 1.5+
- Il limiter ZaMaximX2 di [zam-plugins](https://github.com/zamaudio/zam-plugins)
- Il supporto LV2 di PipeWire per filter-chain

Ti serve un desktop che usi già PipeWire con WirePlumber, che è la
configurazione predefinita nelle versioni attuali di Fedora, Ubuntu, Debian e
Arch. I nomi dei pacchetti Fedora sono testati; su altre distribuzioni, se il
nome di un pacchetto è cambiato, lo script ti dice cosa manca così puoi
installarlo da te.

## Come funziona

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

La struttura del grafo dipende solo dai canali del dispositivo. Tutto il
resto è un parametro, e disattivare una funzione lo imposta su un valore
neutro, come 0 dB o un filtro spostato fuori dalla gamma udibile.

L'effetto 3D è RACE sviluppato su due termini:
`out = own − g·D(other) + g²·D₂(own)`, limitato alla banda 250 Hz–5 kHz. I
grafi dei filtri di PipeWire non possono contenere cicli di retroazione,
quindi non è completamente ricorsivo.

Lo spettro viene letto con `pw-record` dal dispositivo che stai regolando, e
solo mentre la finestra è aperta.

## Suggerimenti

- **Portatili:** applica la configurazione *Altoparlanti piccoli* (taglio dei
  bassi a 120 Hz) e aggiungi 6–10 dB di amplificazione. È più o meno ciò che
  fanno i miglioramenti audio di Windows come Dolby sulla maggior parte dei
  portatili.
- **Subwoofer:** applica *Gestione dei bassi (80 Hz)*, poi regola con
  precisione livello e ritardo del subwoofer finché i bassi non suonano
  uniformi nella tua posizione d'ascolto.
- **3D:** siediti al centro, imposta l'intensità 3D a circa il 70%, poi
  regola il ritardo 3D finché il suono non si allarga oltre gli altoparlanti.
- **L'overdrive** invia audio in clipping agli altoparlanti. Usalo con
  moderazione sui driver piccoli.

## Licenza

MIT. Vedi [LICENSE](../LICENSE).

<p align="center">
  <img src="../data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Icône de Sound Tuner">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>Tirez le meilleur de vos haut-parleurs de portable pourris, ou peaufinez votre système audiophile dans les moindres détails.</b></p>

<!-- languages -->
<p align="center"><sub><a href="../README.md">English</a> · <a href="README.ar.md">العربية</a> · <a href="README.bn.md">বাংলা</a> · <a href="README.cs.md">Čeština</a> · <a href="README.da.md">Dansk</a> · <a href="README.de.md">Deutsch</a> · <a href="README.el.md">Ελληνικά</a> · <a href="README.es.md">Español</a> · <a href="README.fa.md">فارسی</a> · <a href="README.fi.md">Suomi</a> · <b>Français</b> · <a href="README.he.md">עברית</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.hu.md">Magyar</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.it.md">Italiano</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.nb.md">Norsk bokmål</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.pl.md">Polski</a> · <a href="README.pt_BR.md">Português (Brasil)</a> · <a href="README.ro.md">Română</a> · <a href="README.ru.md">Русский</a> · <a href="README.sv.md">Svenska</a> · <a href="README.th.md">ไทย</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.uk.md">Українська</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.zh_CN.md">简体中文</a> · <a href="README.zh_TW.md">繁體中文</a></sub></p>
<!-- /languages -->


Sound Tuner est un égaliseur, un filtre de séparation et un outil de réglage
des haut-parleurs pour tout le système, destiné aux bureaux Linux qui
utilisent PipeWire. Il ajoute une sortie virtuelle, **Sound Tuner**, devant
n’importe quel périphérique audio, des haut-parleurs intégrés d’un portable à
une paire stéréo avec caisson de basses ou à une installation 7.1 complète,
et toutes les applications passent par elle.

<img src="../data/screenshots/main.webp" alt="Sound Tuner : façonnage de la courbe d’égalisation sur le spectre de sortie en direct">

Sur les téléphones et dans les fenêtres étroites, les paramètres passent dans un panneau coulissant :

<img src="../data/screenshots/mobile.png" alt="Sound Tuner sur un téléphone : égaliseur et panneau des paramètres" width="420">

## Fonctionnalités

- **Un égaliseur que l’on dessine :** balayez le graphique dans un sens ou
  dans l’autre pour peindre la courbe, ou faites glisser des points
  individuels. La courbe passe par vos points (l’application calcule les gains
  des filtres pour vous), et vous pouvez faire défiler pour élargir ou
  resserrer une bande, ou saisir des valeurs exactes de fréquence, de gain et
  de largeur. Un **spectre en direct** de ce qui est en cours de lecture est
  affiché derrière la courbe.
- **Routage et filtres de séparation par canal, pour toute configuration**
  (2.0, 2.1, 4.0, 5.1, 7.1…). Pour chaque canal de haut-parleur, vous
  définissez :
  - la source : même canal, gauche, droite, mono, tous les canaux (pour un caisson) ou désactivé
  - des filtres de séparation passe-haut et passe-bas (Linkwitz-Riley, 24 dB/oct)
  - le niveau, le délai (pour l’alignement temporel) et la polarité
- **Configurations de canaux en un clic :** coupe-bas pour petits
  haut-parleurs, séparation graves à gauche / aigus à droite pour les
  portables, stéréo vers tous les haut-parleurs, et gestion des graves à
  80 Hz pour les systèmes avec caisson de basses.
- **Loudness :** jusqu’à +20 dB d’amplification vers un limiteur à
  anticipation (ZaMaximX2), plus un **overdrive** optionnel pour quand vous
  voulez plus fort que ce qu’un son propre permet, et un interrupteur pour
  laisser le curseur de volume de GNOME dépasser 100 %.
- **3D :** largeur stéréo plus annulation de diaphonie dans le style
  Ambiophonics/RACE, qui étend le son au-delà de haut-parleurs rapprochés,
  comme ceux d’un portable.
- **Préréglages :** une liste en haut de la fenêtre. Cliquez sur l’un d’eux
  pour le charger, ou enregistrez le son actuel comme nouveau préréglage. Les
  modifications sont enregistrées au fur et à mesure dans le préréglage actif.

## Comparaison avec Easy Effects, JamesDSP, etc.

- **Interface moderne et simple :** un seul écran épuré. Dessinez la courbe
  d’égalisation, réglez le loudness et la 3D, choisissez un préréglage, sans
  fouiller dans des panneaux de plugins. Elle est aussi adaptée au mobile et
  s’ajuste des téléphones jusqu’aux grands écrans de bureau.
- **Rien à laisser tourner :** le traitement s’exécute dans PipeWire
  lui-même. Fermez l’application et votre son reste réglé dès la connexion.
- **Vrai multicanal :** le 5.1 reste du 5.1, avec filtres de séparation,
  délais et gestion des graves par canal.
- **Aucune coupure :** les modifications s’appliquent en direct au filtre en
  cours d’exécution.
- **Minuscule :** un seul fichier Python et une configuration PipeWire
  lisible.
- **Difficile à faire saturer :** la chaîne se termine toujours par un
  limiteur à anticipation. Voir ci-dessous.

### Pourquoi d’autres égaliseurs peuvent sonner saturés

L’égalisation et l’accentuation des graves peuvent pousser le signal au-delà
de 0 dBFS, le maximum que la puce audio peut restituer, et il écrête à moins
qu’un limiteur ne le rattrape. Sound Tuner se termine toujours par un
limiteur à anticipation réglé sous 0 dBFS, si bien que les amplifications
rendent le son plus fort au lieu de le faire crépiter. (L’overdrive
contourne volontairement ce limiteur.) Son traitement s’exécute aussi dans
PipeWire lui-même plutôt que dans un processus applicatif séparé : c’est un
programme de moins qui doit suivre le rythme en temps réel.

## Installation

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

Le script installe les dépendances manquantes avec votre gestionnaire de
paquets (dnf, apt ou pacman). Il affiche la commande exacte et demande votre
accord avant d’utiliser `sudo`. Il installe ensuite l’application pour votre
utilisateur uniquement.

Ouvrez **Sound Tuner**, choisissez votre périphérique de sortie et cliquez
sur **Charger** dans le bandeau. L’audio redémarre une fois pour charger le
filtre.

| Option | Effet |
|---|---|
| `--yes` | installer les dépendances sans demander |
| `--no-deps` | ignorer les dépendances, installer uniquement l’application |
| `--dry-run` | afficher ce qui serait installé, sans rien modifier |
| `--uninstall` | supprimer l’application et le filtre PipeWire (conserve vos préréglages) |

### Dépendances

Installées pour vous par `install.sh` :

- Outils PipeWire : `pw-cli`, `pw-dump`, `pw-record` et `pactl`
- Python 3 avec GTK 4 et libadwaita 1.5+
- Le limiteur ZaMaximX2 de [zam-plugins](https://github.com/zamaudio/zam-plugins)
- La prise en charge LV2 de PipeWire pour filter-chain

Il vous faut un bureau qui utilise déjà PipeWire avec WirePlumber, ce qui est
le cas par défaut sur les versions actuelles de Fedora, Ubuntu, Debian et
Arch. Les noms de paquets Fedora sont testés ; sur d’autres distributions, si
un nom de paquet a changé, le script vous indique ce qui manque pour que vous
puissiez l’installer vous-même.

## Fonctionnement

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

La structure du graphe ne dépend que des canaux du périphérique. Tout le
reste est un paramètre, et désactiver une fonctionnalité le règle sur une
valeur neutre, comme 0 dB ou un filtre déplacé hors de la plage audible.

L’effet 3D est un RACE déroulé sur deux termes :
`out = own − g·D(other) + g²·D₂(own)`, limité à la bande 250 Hz–5 kHz. Les
graphes de filtres de PipeWire ne peuvent pas contenir de boucles de
rétroaction, il n’est donc pas entièrement récursif.

Le spectre est lu avec `pw-record` depuis le périphérique que vous réglez, et
uniquement tant que la fenêtre est ouverte.

## Astuces

- **Portables :** appliquez la configuration *Petits haut-parleurs* (coupe-bas
  à 120 Hz) et ajoutez 6 à 10 dB d’amplification. C’est à peu près ce que
  font les améliorations audio de Windows comme Dolby sur la plupart des
  portables.
- **Caisson de basses :** appliquez *Gestion des graves (80 Hz)*, puis
  ajustez finement le niveau et le délai du caisson jusqu’à ce que les graves
  soient homogènes à votre place d’écoute.
- **3D :** asseyez-vous au centre, réglez l’intensité 3D à environ 70 %, puis
  ajustez le délai 3D jusqu’à ce que le son s’étende au-delà des
  haut-parleurs.
- **L’overdrive** envoie un signal écrêté à vos haut-parleurs. Utilisez-le
  avec modération sur de petits haut-parleurs.

## Licence

MIT. Voir [LICENSE](../LICENSE).

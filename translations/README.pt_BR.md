<p align="center">
  <img src="../data/icons/io.github.pjamessteven.SpeakerTuner.svg" width="128" alt="Ícone do Sound Tuner">
</p>

<h1 align="center">Dolbro™ Sound Tuner</h1>

<p align="center"><b>Tire o máximo dos alto-falantes porcarias do seu notebook, ou faça o ajuste fino do seu sistema de som de audiófilo.</b></p>

<!-- languages -->
<p align="center"><sub><a href="../README.md">English</a> · <a href="README.ar.md">العربية</a> · <a href="README.bn.md">বাংলা</a> · <a href="README.cs.md">Čeština</a> · <a href="README.da.md">Dansk</a> · <a href="README.de.md">Deutsch</a> · <a href="README.el.md">Ελληνικά</a> · <a href="README.es.md">Español</a> · <a href="README.fa.md">فارسی</a> · <a href="README.fi.md">Suomi</a> · <a href="README.fr.md">Français</a> · <a href="README.he.md">עברית</a> · <a href="README.hi.md">हिन्दी</a> · <a href="README.hu.md">Magyar</a> · <a href="README.id.md">Bahasa Indonesia</a> · <a href="README.it.md">Italiano</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a> · <a href="README.nb.md">Norsk bokmål</a> · <a href="README.nl.md">Nederlands</a> · <a href="README.pl.md">Polski</a> · <b>Português (Brasil)</b> · <a href="README.ro.md">Română</a> · <a href="README.ru.md">Русский</a> · <a href="README.sv.md">Svenska</a> · <a href="README.th.md">ไทย</a> · <a href="README.tr.md">Türkçe</a> · <a href="README.uk.md">Українська</a> · <a href="README.vi.md">Tiếng Việt</a> · <a href="README.zh_CN.md">简体中文</a> · <a href="README.zh_TW.md">繁體中文</a></sub></p>
<!-- /languages -->


O Sound Tuner é um equalizador, crossover e ajustador de alto-falantes para o
sistema inteiro, feito para desktops Linux com PipeWire. Ele adiciona uma saída
virtual, **Sound Tuner**, na frente de qualquer dispositivo de som, desde os
alto-falantes embutidos de um notebook até um par estéreo com subwoofer ou um
sistema 7.1 completo, e todos os aplicativos tocam através dela.

<img src="../data/screenshots/main.webp" alt="Sound Tuner: moldando a curva do equalizador sobre o espectro da saída ao vivo">

Em celulares e janelas estreitas, as configurações vão para um painel deslizante:

<img src="../data/screenshots/mobile.png" alt="Sound Tuner em um celular: equalizador e painel de configurações" width="420">

## Recursos

- **Um equalizador que você desenha:** passe o cursor pelo gráfico em qualquer
  direção para pintar a curva, ou arraste pontos individuais. A curva passa
  pelos seus pontos (o aplicativo calcula os ganhos dos filtros para você), e
  você pode rolar para deixar uma banda mais larga ou mais estreita, ou digitar
  valores exatos de frequência, ganho e largura. Um **espectro ao vivo** do que
  está tocando é desenhado atrás da curva.
- **Roteamento e crossovers por canal para qualquer layout** (2.0, 2.1, 4.0,
  5.1, 7.1, …). Para cada canal de alto-falante você define:
  - a origem: mesmo canal, esquerdo, direito, mono, todos os canais (para um
    subwoofer) ou desligado
  - filtros de crossover passa-alta e passa-baixa (Linkwitz-Riley, 24 dB/oct)
  - nível, atraso (para alinhamento temporal) e polaridade
- **Configurações de canais com um clique:** corte de graves para alto-falantes
  pequenos, divisão graves à esquerda / agudos à direita para notebooks, estéreo
  em todos os alto-falantes e gerenciamento de graves em 80 Hz para sistemas com
  subwoofer.
- **Loudness:** até +20 dB de reforço em um limitador com look-ahead
  (ZaMaximX2), além de **overdrive** opcional para quando você quiser mais alto
  do que o som limpo permite, e uma opção para deixar o controle de volume do
  GNOME passar de 100%.
- **3D:** largura estéreo mais cancelamento de crosstalk no estilo
  Ambiophonics/RACE, que espalha o som além de alto-falantes muito próximos,
  como os de um notebook.
- **Predefinições:** uma lista no topo da janela. Clique em uma para carregá-la,
  ou salve o som atual como uma nova. As alterações são salvas na predefinição
  ativa conforme você mexe.

## Comparação com Easy Effects, JamesDSP etc.

- **Interface moderna e fácil:** uma única tela limpa. Desenhe a curva do
  equalizador, ajuste o loudness e o 3D e escolha uma predefinição, sem ficar
  vasculhando painéis de plugins. Também funciona bem no celular, adaptando-se
  de telas de celular até telas largas de desktop.
- **Nada precisa ficar rodando:** o processamento acontece dentro do próprio
  PipeWire. Feche o aplicativo e o seu som continua ajustado desde o login.
- **Multicanal de verdade:** 5.1 continua 5.1, com crossovers, atrasos e
  gerenciamento de graves por canal.
- **Sem cortes no áudio:** as alterações são aplicadas ao vivo no filtro em
  execução.
- **Minúsculo:** um arquivo Python e uma configuração do PipeWire fácil de ler.
- **Difícil de saturar:** a cadeia sempre termina em um limitador com
  look-ahead. Veja abaixo.

### Por que outros equalizadores podem soar distorcidos

Equalização e reforço de graves podem empurrar o sinal além de 0 dBFS, o máximo
que o chip de som consegue reproduzir, e ele satura (clipping) a menos que um
limitador o segure. O Sound Tuner sempre termina com um limitador com look-ahead
ajustado abaixo de 0 dBFS, então os reforços ficam mais altos em vez de
chiarem. (O overdrive ignora isso de propósito.) Além disso, o processamento
roda dentro do próprio PipeWire e não em um processo separado de aplicativo,
então há um programa a menos que precisa dar conta em tempo real.

## Instalação

```sh
git clone https://github.com/pjamessteven/dolbro-sound-tuner.git
cd dolbro-sound-tuner
./install.sh
```

O script instala as dependências que faltarem com o seu gerenciador de pacotes
(dnf, apt ou pacman). Ele mostra o comando exato e pergunta antes de usar
`sudo`. Depois, instala o aplicativo apenas para o seu usuário.

Abra o **Sound Tuner**, escolha o seu dispositivo de saída e clique em
**Carregar** no banner. O áudio reinicia uma vez para carregar o filtro.

| Opção | O que faz |
|---|---|
| `--yes` | instala as dependências sem perguntar |
| `--no-deps` | pula as dependências e instala só o aplicativo |
| `--dry-run` | mostra o que seria instalado, sem alterar nada |
| `--uninstall` | remove o aplicativo e o filtro do PipeWire (mantém suas predefinições) |

### Dependências

Instaladas para você pelo `install.sh`:

- Ferramentas do PipeWire: `pw-cli`, `pw-dump`, `pw-record` e `pactl`
- Python 3 com GTK 4 e libadwaita 1.5+
- O limitador ZaMaximX2 do [zam-plugins](https://github.com/zamaudio/zam-plugins)
- Suporte a LV2 do PipeWire para o filter-chain

Você precisa de um desktop que já rode PipeWire com WirePlumber, o padrão nas
versões atuais de Fedora, Ubuntu, Debian e Arch. Os nomes de pacotes do Fedora
são testados; em outras distros, se o nome de algum pacote tiver mudado, o
script diz o que está faltando para você instalar por conta própria.

## Como funciona

```
per input channel:   width (FL/FR) → 10-band EQ → 3D crosstalk cancellation (FL/FR)
per output channel:  source mix → high-pass → low-pass → level/polarity → delay
                     → limiter → overdrive → device channel
```

A estrutura do grafo depende apenas dos canais do dispositivo. Todo o resto é
um parâmetro, e desligar um recurso o coloca em um valor neutro, como 0 dB ou
um filtro movido para fora da faixa audível.

O efeito 3D é o RACE desenrolado em dois termos:
`out = own − g·D(other) + g²·D₂(own)`, com banda limitada a 250 Hz–5 kHz. Os
grafos de filtros do PipeWire não podem conter laços de realimentação, então ele
não é totalmente recursivo.

O espectro é lido com `pw-record` a partir do dispositivo que você está
ajustando, e só enquanto a janela está aberta.

## Dicas

- **Notebooks:** aplique a configuração *Alto-falantes pequenos* (corte de
  graves em 120 Hz) e adicione 6–10 dB de reforço. É mais ou menos o que os
  aprimoramentos do Windows, como o Dolby, fazem na maioria dos notebooks.
- **Subwoofer:** aplique *Gerenciamento de graves (80 Hz)* e depois faça o
  ajuste fino do nível e do atraso do subwoofer até os graves soarem uniformes
  onde você está sentado.
- **3D:** sente-se no centro, ajuste a intensidade 3D para cerca de 70% e depois
  mexa no atraso 3D até o som se espalhar além dos alto-falantes.
- **Overdrive** envia áudio saturado para os seus alto-falantes. Use com
  moderação em alto-falantes pequenos.

## Licença

MIT. Veja [LICENSE](../LICENSE).

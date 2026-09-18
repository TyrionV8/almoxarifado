# Pinagem da WeAct STM32H743 Core Board — imagens, pinos e fileiras

Atualizado em 17/09/2026. Leia antes de alterar qualquer pinagem da H743.

## Placa

- **WeAct Studio MiniSTM32H7xx** com **STM32H743VIT6** (V = 100 pinos, I = 2 MiB de Flash, T = LQFP, 6 = −40 a +85 °C). O mesmo circuito também é vendido com STM32H750VBT6; a unidade do acervo é a H743, conforme as fotos enviadas pelo usuário em 17/09/2026.
- A marcação do chip termina em **V**, que indica a revisão V do silício (até 480 MHz). A revisão Y ficaria limitada a 400 MHz.
- Serigrafia com SB1–SB6 e R9 no verso, igual ao desenho da **V1.1/V1.2**. O esquema usado é o V1.2 ([h743-schematic.pdf](../assets/documents/h743-schematic.pdf)); diferenças para a V1.1 não afetam os headers (capacitor no VBAT, chip de reset MAX809 e pull-up de 100 kΩ no CS da flash SPI).
- Recursos: TFT 0,96″ ST7735 (80 × 160), conector de câmera DVP de 24 vias, microSD, Flash QSPI de 8 MB e Flash SPI de 8 MB (as duas PY25Q64HA, no verso), USB-C, botões NR/B0/K1, LED azul E3, LED vermelho PWR, cristais de 25 MHz e 32,768 kHz, regulador DC-DC de 1 A.

## Regras principais

1. **Pino do CI = número do LQFP100** da tabela 9 do DS12110 Rev 7 ([stm32h743vi.pdf](../assets/documents/stm32h743vi.pdf)). Exemplos: PE2 = 1, PC13 = 7, PA13 = 72, PA14 = 76, BOOT0 = 94.
2. **Vista de cima com o display no topo e o USB-C embaixo**, como na foto do usuário e no desenho mecânico WeAct. A posição 1 dos headers fica junto ao display/SWD e a 22 junto ao USB-C/microSD.
3. **Dois headers duplos 2 × 22 com paridade invertida**, conforme esquema, desenho mecânico (pino 1 quadrado) e serigrafia do verso:
   - esquerdo = **P2**: fileira **externa = pinos pares**, interna = ímpares (P2-1 GND é o furo quadrado interno);
   - direito = **P1**: fileira **externa = pinos ímpares**, interna = pares (P1-1 GND é o furo quadrado externo).
   Nas imagens, a linha de cima de cada par é a fileira externa e a de baixo é a interna.
4. **A serigrafia dos nomes fica no verso**, espelhada. Nas imagens ela é repetida ao lado dos furos para facilitar a leitura.
5. **PC2_C e PC3_C** (pinos 17 e 18): no LQFP100 só existem os pads analógicos `_C` (nota 6 da tabela 9). As funções digitais de PC2/PC3 só chegam a eles com a chave analógica fechada (registrador SYSCFG_PMCR). As imagens mostram as AF de PC2/PC3 com esse aviso.
6. **Muitos pinos do header já estão ligados na placa** (LCD, câmera, microSD, flashes, USB, LED, K1). As imagens marcam isso em "uso na placa" (simples) ou numa etiqueta amarela sob o nome (completa).

## Imagens exibidas na ficha

A aba **Pinagem** mostra sete imagens, nesta ordem (campo `pinouts`), no mesmo esquema da H7R3: duas visões gerais da placa inteira e cinco folhas legíveis no painel. As folhas usam a classe `pinout-sheet` (largura total, sem limite de altura).

| Ordem | Arquivo | Conteúdo |
| ---: | --- | --- |
| 1 | [h743-pinout-simple.png](../assets/pinouts/h743-pinout-simple.png) | Visão geral simples: placa inteira, uso na placa, três funções por pino, nome, número LQFP100 e pino do header. |
| 2 | [h743-pinout-full.png](../assets/pinouts/h743-pinout-full.png) | Visão geral completa: todas as AF0–AF15 e funções adicionais em colunas por grupo (≈15,5 mil px de largura; ampliar para ler). |
| 3 | [h743-pinout-simple-left.png](../assets/pinouts/h743-pinout-simple-left.png) | Simples, header esquerdo P2, com a faixa da placa em escala e linhas até os furos. |
| 4 | [h743-pinout-simple-right.png](../assets/pinouts/h743-pinout-simple-right.png) | Idem, header direito P1. |
| 5 | [h743-pinout-full-left.png](../assets/pinouts/h743-pinout-full-left.png) | Completa, P2: lista na ordem física, externo/interno, AF com número, funções adicionais tracejadas, tolerância 5 V (FT) ou 3,6 V (TT). |
| 6 | [h743-pinout-full-right.png](../assets/pinouts/h743-pinout-full-right.png) | Idem, P1. |
| 7 | [h743-pinout-full-extra.png](../assets/pinouts/h743-pinout-full-extra.png) | Pinos fora dos headers (PA13, PA14, PC14, PC15, PH0, PH1, BOOT0) e notas: recursos da placa, SWD/USB/alimentação, como ler, cuidados e pontes de solda. |

SHA-256 (geração de 17/09/2026):

- `h743-pinout-full-extra.png`: `a0f6aa592022450acf1bb36c8d03ab613e5fced0129690120ce1f63b92885876`
- `h743-pinout-full-left.png`: `996f111317c265ff7ff4e59396445a21d0f6813161bc5210eebbdf2616670629`
- `h743-pinout-full.png`: `7a1b8ab5ad4aafbc25c971ba33adb8d0698bc7cc5d89fe3da1a64c9d14f1475b`
- `h743-pinout-full-right.png`: `b7c4febbdc8eaa7e1e096d18a0c63fa344f3a6151e5c28744f2d0185f24157bb`
- `h743-pinout-simple-left.png`: `6131da2ae3532b42fe6118b93a0b9aceffb19fa779d00487f26ecca53824d7d2`
- `h743-pinout-simple.png`: `4055b54fe6d5a40b58049aa4a911d2b6de26ef4636b94f76fec6d0fc125166fc`
- `h743-pinout-simple-right.png`: `78c43c7caf74d52287c8d2fe537f656bd88a475bb27aac50e205037c2afcb5e6`

A placa é desenhada em escala a partir do desenho mecânico WeAct V1.2 (40,64 × 66,88 mm; furos a 1,27 e 3,81 mm da borda; passo 2,54 mm), com 22,9 px/mm no CSS (2,54 mm = duas linhas de 29 px). Posições dos componentes conferidas em [weact-h743-boardshape.png](../assets/pinouts/sources/weact-h743-boardshape.png).

## Como as imagens são feitas

Diferente da H7R3 e da G474, o gerador está versionado: [scripts/make_h743_pinouts.py](../scripts/make_h743_pinouts.py). Requer Poppler (`pdftotext`), Pillow e Google Chrome/Chromium.

```bash
# Regera as sete imagens (≈1 min). Passe nomes de arquivo para gerar só algumas.
python3 scripts/make_h743_pinouts.py
```

1. Lê o datasheet local pelas coordenadas das palavras (`pdftotext -bbox`):
   - tabelas 10–14 e 17 (AF0–AF15 das portas A–E e H). Cada página pode ter duas tabelas; o cabeçalho de cada uma é detectado e a última linha dele (…SPDIFRX1 / ETH) serve de limite superior, para não vazar texto do cabeçalho na primeira linha de pinos;
   - tabela 9 (número LQFP100, estrutura de E/S e funções adicionais). PC13, PC2_C e PC3_C são preenchidos à mão no gerador porque a leitura por coordenadas não separa essas linhas (conferidos nas páginas 64–66).
2. Headers P1/P2 e ligações da placa estão escritos no gerador, copiados do esquema V1.2 (página 1: Peripherals e I/O PIN).
3. Monta HTML/SVG e fotografa com o Chrome headless em escala 2×, recortando a sobra da janela.

A extração foi conferida pino a pino contra o texto da tabela 9: todas as AF dos pinos da placa aparecem na linha correspondente (as únicas diferenças são nomes que a tabela 9 abrevia, como `USART2_RTS/USART2_DE` e `ETH_MII_…/ETH_RMII_…`).

As AF da tabela valem para toda a família H742/H743; LCD-TFT, JPEG e Chrom-ART existem na H743 (a H742 não tem). Ethernet e USB HS (ULPI) precisam de PHY externo, que a placa não tem.

## Tabela de conferência dos headers

Posição 1 = junto ao display. Formato: conector-pino · **sinal** · número LQFP100. Colunas na ordem física, da esquerda para a direita, com a placa vista de cima.

| Pos. | Esquerdo externo (par) | Esquerdo interno (ímpar) | Direito interno (par) | Direito externo (ímpar) |
| ---: | --- | --- | --- | --- |
| 1 | P2-2 · **3V3** | P2-1 · **GND** | P1-2 · **5V** | P1-1 · **GND** |
| 2 | P2-4 · **PE3** · 2 | P2-3 · **PE2** · 1 | P1-4 · **PE0** · 97 | P1-3 · **PE1** · 98 |
| 3 | P2-6 · **PE5** · 4 | P2-5 · **PE4** · 3 | P1-6 · **PB8** · 95 | P1-5 · **PB9** · 96 |
| 4 | P2-8 · **VBAT** | P2-7 · **PE6** · 5 | P1-8 · **PB6** · 92 | P1-7 · **PB7** · 93 |
| 5 | P2-10 · **NRST** | P2-9 · **PC13** · 7 | P1-10 · **PB4** · 90 | P1-9 · **PB5** · 91 |
| 6 | P2-12 · **PC1** · 16 | P2-11 · **PC0** · 15 | P1-12 · **PD7** · 88 | P1-11 · **PB3** · 89 |
| 7 | P2-14 · **PC3_C** · 18 | P2-13 · **PC2_C** · 17 | P1-14 · **PD5** · 86 | P1-13 · **PD6** · 87 |
| 8 | P2-16 · **VREF+** | P2-15 · **GND** | P1-16 · **PD3** · 84 | P1-15 · **PD4** · 85 |
| 9 | P2-18 · **PA1** · 23 | P2-17 · **PA0** · 22 | P1-18 · **PD1** · 82 | P1-17 · **PD2** · 83 |
| 10 | P2-20 · **PA3** · 25 | P2-19 · **PA2** · 24 | P1-20 · **PC12** · 80 | P1-19 · **PD0** · 81 |
| 11 | P2-22 · **PA5** · 29 | P2-21 · **PA4** · 28 | P1-22 · **PC10** · 78 | P1-21 · **PC11** · 79 |
| 12 | P2-24 · **PA7** · 31 | P2-23 · **PA6** · 30 | P1-24 · **PA12** · 71 | P1-23 · **PA15** · 77 |
| 13 | P2-26 · **PC5** · 33 | P2-25 · **PC4** · 32 | P1-26 · **PA10** · 69 | P1-25 · **PA11** · 70 |
| 14 | P2-28 · **PB1** · 35 | P2-27 · **PB0** · 34 | P1-28 · **PA8** · 67 | P1-27 · **PA9** · 68 |
| 15 | P2-30 · **PE7** · 37 | P2-29 · **PB2** · 36 | P1-30 · **PC8** · 65 | P1-29 · **PC9** · 66 |
| 16 | P2-32 · **PE9** · 39 | P2-31 · **PE8** · 38 | P1-32 · **PC6** · 63 | P1-31 · **PC7** · 64 |
| 17 | P2-34 · **PE11** · 41 | P2-33 · **PE10** · 40 | P1-34 · **PD14** · 61 | P1-33 · **PD15** · 62 |
| 18 | P2-36 · **PE13** · 43 | P2-35 · **PE12** · 42 | P1-36 · **PD12** · 59 | P1-35 · **PD13** · 60 |
| 19 | P2-38 · **PE15** · 45 | P2-37 · **PE14** · 44 | P1-38 · **PD10** · 57 | P1-37 · **PD11** · 58 |
| 20 | P2-40 · **PB11** · 47 | P2-39 · **PB10** · 46 | P1-40 · **PD8** · 55 | P1-39 · **PD9** · 56 |
| 21 | P2-42 · **5V** | P2-41 · **3V3** | P1-42 · **PB14** · 53 | P1-41 · **PB15** · 54 |
| 22 | P2-44 · **GND** | P2-43 · **GND** | P1-44 · **PB12** · 51 | P1-43 · **PB13** · 52 |

Observações:

- **5V**: entrada de 3,3–5,5 V do regulador; o VBUS do USB chega por diodo B5819. Fechar **SB6** curto-circuita o diodo para alimentar dispositivos USB (modo host).
- **3V3**: saída do regulador DC-DC (SY8088 por padrão, 1 A). **VBAT** (VB) vem do pino ou do 3V3 pelo BAT54C. **VREF+** (V+) liga ao 3V3 por R9 (0 Ω).
- **NRST** (NR) tem o supervisor MAX809 e o botão NR.

## Pinos do MCU fora dos headers

| Sinal | LQFP100 | Uso na placa |
| --- | ---: | --- |
| PA13 | 72 | SWD · DIO (22 Ω em série) |
| PA14 | 76 | SWD · CLK (22 Ω em série) |
| PC14 | 8 | cristal 32,768 kHz |
| PC15 | 9 | cristal 32,768 kHz |
| PH0 | 12 | cristal 25 MHz |
| PH1 | 13 | cristal 25 MHz |
| BOOT0 | 94 | botão B0 (10 kΩ para GND) |

## Recursos da placa ligados a pinos dos headers

| Recurso | Pinos |
| --- | --- |
| TFT ST7735 (SPI4) | PE12 SCK · PE14 SDA/MOSI · PE13 DC (WR_RS) · PE11 CS · PE10 luz de fundo (TIM1_CH2N) · reset = reset do sistema |
| Câmera DVP (DCMI) | D0–D7 = PC6, PC7, PE0, PE1, PE4, PD3, PE5, PE6 · VSYNC PB7 · HSYNC PA4 · PIXCLK PA6 · XCLK PA8 (MCO1) · SCL PB8 · SDA PB9 (I2C1) · PWDN PA7 (SB1) · reset = reset do sistema |
| microSD (SDMMC1) | D0–D3 = PC8–PC11 · CLK PC12 · CMD PD2 · detecção PD4 (SB2) |
| Flash QSPI 8 MB | IO0 PD11 · IO1 PD12 · IO2 PE2 · IO3 PD13 · CLK PB2 · NCS PB6 |
| Flash SPI 8 MB (SPI1) | SCK PB3 · MISO PB4 · MOSI PD7 · CS PD6 (SB3) |
| USB-C (OTG_FS) | D− PA11 · D+ PA12 |
| LED azul E3 | PE3, ativo em alto (transistor) |
| Botão K1 | PC13, pressionado = 3V3 (330 Ω) |

Pontes de solda: SB1–SB3 aparecem fechadas no esquema; **SB4/SB5** (alimentação de foco da câmera) ficam abertas e devem ser soldadas para OV5640 com foco automático, segundo o README WeAct; **SB6** liga VBUS ao 5V.

## Ao mudar uma pinagem da H743

1. Pino do CI = número LQFP100 da tabela 9 do DS12110.
2. Respeite a paridade: externa = par no esquerdo (P2) e ímpar no direito (P1).
3. Edite o gerador e rode `python3 scripts/make_h743_pinouts.py`; mantenha os sete nomes `h743-pinout-*.png` (o teste `test_h743_pinout_versions` exige exatamente esses). Atualize os SHA-256 acima.
4. Se mudar nomes, ordem ou títulos, crie uma migração que atualize `pinouts` no SQLite, rode `python3 scripts/export.py` e ajuste os testes.

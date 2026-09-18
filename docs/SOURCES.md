# Fontes e créditos

Documentos obtidos em 12/09/2026; os três da H743 em 17/09/2026. Os originais permanecem sem alterações; as prévias são renderizações das páginas identificadas. Direitos e marcas continuam pertencendo aos respectivos autores. Não há licença única aplicada aos documentos de terceiros.

| Arquivo local | Páginas | Origem |
| --- | ---: | --- |
| [pic16f887.pdf](../assets/documents/pic16f887.pdf) | 288 | [Fabricante / repositório oficial](https://ww1.microchip.com/downloads/en/devicedoc/41291d.pdf) |
| [pic12f675.pdf](../assets/documents/pic12f675.pdf) | 132 | [Fabricante / repositório oficial](https://ww1.microchip.com/downloads/en/devicedoc/41190c.pdf) |
| [pic12f683.pdf](../assets/documents/pic12f683.pdf) | 176 | [Fabricante / repositório oficial](https://ww1.microchip.com/downloads/en/devicedoc/41211d_.pdf) |
| [pic12f1501.pdf](../assets/documents/pic12f1501.pdf) | 292 | [Fabricante / repositório oficial](https://ww1.microchip.com/downloads/aemDocuments/documents/OTH/ProductDocuments/DataSheets/40001615C.pdf) |
| [atmega328p.pdf](../assets/documents/atmega328p.pdf) | 294 | [Fabricante / repositório oficial](https://docs.arduino.cc/resources/datasheets/ATmega328P-datasheet.pdf) |
| [uno-pinout.pdf](../assets/documents/uno-pinout.pdf) | 5 | [Fabricante / repositório oficial](https://docs.arduino.cc/resources/pinouts/A000066-full-pinout.pdf) |
| [nano-pinout.pdf](../assets/documents/nano-pinout.pdf) | 3 | [Fabricante / repositório oficial](https://docs.arduino.cc/resources/pinouts/A000005-full-pinout.pdf) |
| [stm32f103c8.pdf](../assets/documents/stm32f103c8.pdf) | 117 | [Fabricante / repositório oficial](https://raw.githubusercontent.com/WeActStudio/BluePill-Plus/master/Doc/STM32F103C8T6/DS5319-STM32F103x8-Datasheet.pdf) |
| [stm32g474.pdf](../assets/documents/stm32g474.pdf) | 236 | [Fabricante / repositório oficial](https://raw.githubusercontent.com/WeActStudio/WeActStudio.STM32G474CoreBoard/master/Doc/STM32G474xE_DS12288.pdf) |
| [g474-long-schematic.pdf](../assets/documents/g474-long-schematic.pdf) | 1 | [Fabricante / repositório oficial](https://raw.githubusercontent.com/WeActStudio/WeActStudio.STM32G474CoreBoard/master/Hardware/QFN48/WeAct-STM32G474CoreBoard_Long/WeAct-STM32G474CoreBoard_Long_V10%20SchDoc.pdf) |
| [g474-long-pinout.pdf](../assets/documents/g474-long-pinout.pdf) | 3 | [Fabricante / repositório oficial](https://raw.githubusercontent.com/WeActStudio/WeActStudio.STM32G474CoreBoard/master/Hardware/QFN48/WeAct-STM32G474CoreBoard_Long/WeAct-STM32G474CoreBoard_Long_V10%20Board%20Shape%20%E5%A4%96%E5%BD%A2.pdf) |
| [stm32h7r3.pdf](../assets/documents/stm32h7r3.pdf) | 320 | [Fabricante / repositório oficial](https://raw.githubusercontent.com/WeActStudio/WeActStudio.STM32H7R3Zx_CoreBoard/master/Doc/stm32h7r3z8.pdf) |
| [h7-schematic.pdf](../assets/documents/h7-schematic.pdf) | 4 | [Fabricante / repositório oficial](https://raw.githubusercontent.com/WeActStudio/WeActStudio.STM32H7R3Zx_CoreBoard/master/Hardware/WeAct-STM32H7R3Zx_CoreBoard_V10%20SchDoc.pdf) |
| [h7-pinout.pdf](../assets/documents/h7-pinout.pdf) | 3 | [Fabricante / repositório oficial](https://raw.githubusercontent.com/WeActStudio/WeActStudio.STM32H7R3Zx_CoreBoard/master/Hardware/WeAct-STM32H7R3Zx_CoreBoard_V10%20Board%20Shape%20%E5%A4%96%E5%BD%A2.pdf) |
| [stm32f411ce.pdf](../assets/documents/stm32f411ce.pdf) | 149 | [Fabricante / repositório oficial](https://raw.githubusercontent.com/WeActStudio/WeActStudio.MiniSTM32F4x1/master/Datasheet/STM32F411CEU6_Datasheet.pdf) |
| [blackpill-pinout.pdf](../assets/documents/blackpill-pinout.pdf) | 1 | [Fabricante / repositório oficial](https://raw.githubusercontent.com/WeActStudio/WeActStudio.MiniSTM32F4x1/master/General%20document/STM32F4x1%20v2.0+%20Pin%20Layout.pdf) |
| [stm32h743vi.pdf](../assets/documents/stm32h743vi.pdf) | 357 | [Fabricante / repositório oficial](https://raw.githubusercontent.com/WeActStudio/MiniSTM32H7xx/master/Datasheet/MCU/STM32H743VI_Datasheet.pdf) · ST DS12110 Rev 7 |
| [h743-schematic.pdf](../assets/documents/h743-schematic.pdf) | 6 | [Fabricante / repositório oficial](https://raw.githubusercontent.com/WeActStudio/MiniSTM32H7xx/master/Hardware/STM32H7xx%20SchDoc%20V12.pdf) · esquema V1.2 |
| [h743-pinout.pdf](../assets/documents/h743-pinout.pdf) | 3 | [Fabricante / repositório oficial](https://raw.githubusercontent.com/WeActStudio/MiniSTM32H7xx/master/Hardware/STM32H7xx_BoardShape%20Board%20Shape%20%E5%A4%96%E5%BD%A2%20V12.pdf) · desenho mecânico V1.2 |

## Pinagens

As prévias são recortes das páginas e imagens listadas abaixo, sem redesenho e sem arte gerada. As exceções são a G474 Long, a H7R3 e a H743, que usam desenhos próprios descritos em [G474-PINOUT.md](G474-PINOUT.md), [H7R3-PINOUT.md](H7R3-PINOUT.md) e [H743-PINOUT.md](H743-PINOUT.md). A numeração é a física do PDF (começando em 1), não a impressa. `scripts/prepare_pinouts.py` reproduz cada recorte a partir dos arquivos versionados.

| Componente | Fonte | Trecho usado |
| --- | --- | --- |
| PIC16F887 | pic16f887.pdf | p. 8 (diagrama PDIP-40) + p. 9 (Tabela 3, resumo dos 40 pinos) |
| PIC12F675 | pic12f675.pdf | p. 4 (diagrama PDIP do F675) + p. 8 (Tabela 1-1, descrição dos pinos) |
| PIC12F683 | pic12f683.pdf | p. 4 (diagrama PDIP + Tabela 1); os encapsulamentos DFN foram recortados fora |
| PIC12F1501 | pic12f1501.pdf | p. 3 (diagrama) + p. 4 (Tabela 1, alocação de funções) |
| BluePill | bluepill-generic-f103.png | imagem completa, sem recorte |
| Uno | atmega328p.pdf (Figura 1-1, tabela 28.1) + uno-pinout.pdf (p. 1 e 3) | desenho próprio `uno-pinout-simple.png` (gerado por `scripts/make_arduino_pinouts.py`) seguido do recorte oficial `uno-pinout.png` (p. 1). Ver [ARDUINO-PINOUT.md](ARDUINO-PINOUT.md) |
| Nano | atmega328p.pdf (Figura 1-1, tabela 28.1) + nano-pinout.pdf (p. 1–3) | desenho próprio `nano-pinout-simple.png` (gerado por `scripts/make_arduino_pinouts.py`) seguido do recorte oficial `nano-pinout.png` (p. 1). Ver [ARDUINO-PINOUT.md](ARDUINO-PINOUT.md) |
| BlackPill | blackpill-pinout.pdf | p. 1, página inteira e inalterada |
| G474 Long | stm32g474.pdf (tabelas 12 e 13) + g474-long-schematic.pdf + weact-g474-long-board.png | desenhos próprios empilhados: `g474-long-pinout-simple.png` (visão rápida) e `g474-long-pinout-full.png` (todas as funções), ambos com numeração UFQFPN48 conferida. Ver [G474-PINOUT.md](G474-PINOUT.md) |
| H7R3 | stm32h7r3.pdf (tabelas 2, 3, 19 e 20) + h7-schematic.pdf + h7-pinout.pdf | duas visões gerais (`h7-pinout-simple.png`, `h7-pinout-full.png`) e cinco folhas por header (`h7-pinout-simple-left/right.png`, `h7-pinout-full-left/right/extra.png`), com esferas UFBGA144 SMPS GP. Ver [H7R3-PINOUT.md](H7R3-PINOUT.md) |
| H743 | stm32h743vi.pdf (tabelas 9–14 e 17) + h743-schematic.pdf + h743-pinout.pdf + weact-h743-boardshape.png | mesma organização da H7R3: duas visões gerais (`h743-pinout-simple.png`, `h743-pinout-full.png`) e cinco folhas (`h743-pinout-simple-left/right.png`, `h743-pinout-full-left/right/extra.png`), com números LQFP100; geradas por `scripts/make_h743_pinouts.py`. Ver [H743-PINOUT.md](H743-PINOUT.md) |

Desenhos de pinagem sem PDF oficial ficam em `assets/pinouts/sources/`. URL, SHA-256, crédito e licença de cada um estão em `data/pinout_sources.json`.

## Créditos

- Microchip / Atmel: datasheets dos PICs e ATmega328P. Avisos de direitos preservados nos PDFs.
- STMicroelectronics: datasheets STM32; algumas cópias distribuídas no repositório oficial WeAct.
- WeAct Studio: diagramas, esquemas, renders e documentação de suas placas. BlackPill pinout: Richard Balint, conforme crédito no próprio desenho. As pinagens da H7R3 (simples e completa) são desenhos do almoxarifado a partir do DS14360 (STMicroelectronics), do esquema e do desenho mecânico WeAct. As pinagens da H743 são desenhos do almoxarifado a partir do DS12110 (STMicroelectronics), do esquema V1.2 e do desenho mecânico WeAct MiniSTM32H7xx. As pinagens da G474 Long (simples e completa) são desenhos do almoxarifado: a simples usa o render oficial WeAct como fundo, e a completa usa dados do DS12288 (STMicroelectronics), o esquema WeAct e uma foto da placa do usuário.
- BluePill: *The Generic STM32F103 Pinout Diagram*, de Rasmus Friis Kjeldsen (reblag.dk/stm32), publicado no Wikimedia Commons sob Creative Commons Attribution-ShareAlike 4.0. Usado sem alteração; o crédito e a licença aparecem na aba de pinagem e em `data/pinout_sources.json`. Obras derivadas deste desenho precisam manter a mesma licença.
- Arduino: pinouts Uno e Nano, licença Creative Commons Attribution-ShareAlike 4.0 indicada nos documentos. As prévias mantêm os créditos da página.
- Print da variante BlackPill: fornecido pelo usuário nesta tarefa; imagem de anúncio usada apenas como evidência de variante, não como fonte de limites elétricos.
- LinkeDOM 0.18.12: biblioteca MIT para testes de estrutura de documento. [Licença incluída](../tests/vendor/LICENSE-linkedom), obtida do [registro npm](https://registry.npmjs.org/linkedom/-/linkedom-0.18.12.tgz). Não é carregada pela aplicação.

## Rastreabilidade

`data/sources.json` registra a URL original e o SHA-256 de cada PDF; `data/pinout_sources.json` faz o mesmo para as imagens de pinagem, somando crédito e licença. Os testes conferem os arquivos contra esses hashes. A data é de obtenção, não de revisão do documento.

Documentação de contexto pessoal, confirmações do usuário e limites da identificação estão em [handoff.md](../handoff.md). Os arquivos externos do Obsidian e TCC foram apenas lidos.

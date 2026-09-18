# Handoff — Almoxarifado

Atualizado em 17/09/2026. Este documento é a entrada de contexto para agentes futuros.

## 1. Objetivo e contrato com o usuário

Catálogo pessoal de componentes para comparar os itens que o usuário possui e escolher um microcontrolador para cada projeto. A primeira categoria é microcontroladores; outras serão acrescentadas depois. A experiência principal é uma tabela expansível, com ficha técnica, pinagem, datasheet e documentação educativa integrada.

Repositório local: `/home/davi/repos/almoxarifado`. O projeto começou com apenas README e commit inicial `af3e1a1`. Não havia código ou alterações locais a preservar. O usuário autorizou implementar e comitar o projeto e o banco; não pediu publicação web. Não foi feito push nesta entrega.

Requisitos prioritários:

- Clonar e abrir, sem instalação, servidor, conta ou senha.
- SQLite versionado; atualização distribuída por Git pull/push.
- Conteúdo legível em português, termos explicados, poucas etapas para usar.
- Preservar outros repositórios, Obsidian, TCC e montagens físicas.
- README curto; este handoff completo e atualizado junto com cada melhoria.
- Não realizar alterações físicas, programação de placas ou pedir segredos.

## 2. Arquitetura e decisões

**Página estática em HTML (HyperText Markup Language), CSS (Cascading Style Sheets) e JavaScript**, sem framework, dependências de execução ou hospedagem. A folha de estilo usa fontes do sistema. O arquivo `index.html` é a entrada final, não uma etapa de build.

**SQLite é a fonte canônica dos dados**, mas não é consultado em tempo de execução pelo navegador. Navegadores não abrem automaticamente um SQLite vizinho via `file://` como uma aplicação nativa. Para preservar “clonar e abrir”, `scripts/export.py` gera `data/catalog.js`, um snapshot (cópia de leitura) do banco carregado por uma tag script clássica. Na abertura por `file://` não usa fetch, módulos externos, servidor, WebAssembly ou CDN (Content Delivery Network, rede de distribuição); o `localStorage` guarda só a preferência de colunas.

O mesmo exportador gera `data/inventory.sql`, uma representação textual revisável do banco. Atualizações devem incluir SQLite, SQL e catálogo JS no mesmo commit. Nunca editar os arquivos gerados para mudar dados: editar SQLite e exportar.

**Dois modos (decisão de 13/09/2026).** O usuário pediu uma forma simples de registrar, pelo site, quando uma unidade entra em uso, é descartada ou comprada. Navegador por `file://` não grava arquivos; por isso:

- **Consulta** — abrir `index.html` direto, como antes. A aba Histórico mostra os registros e uma instrução para o modo de registro.
- **Registro** — `python3 scripts/server.py` (só biblioteca padrão) serve os mesmos arquivos em `http://127.0.0.1:8765`, detecta-se por `GET api/status` e habilita o formulário. Cada `POST` grava no SQLite em transação, valida o saldo e regenera `catalog.js` + `inventory.sql` na hora; o usuário só comita `data/`. O servidor escuta apenas em 127.0.0.1, recusa `Host`/`Origin` diferentes e corpo que não seja JSON (proteção contra CSRF e DNS rebinding) e não serve arquivos ocultos (`.git`).

Busca, filtros e seleção para comparar continuam não persistidos. Não existe cadastro de novos modelos pela interface (isso segue via migração + agentes).

**Menos conteúdo fixo no código.** Colunas da tabela, grupos e cores, campos da ficha, famílias, classes de processamento, categorias/dicas do glossário, guias de pinos, subtítulos, Flash resumida, aceleradores e avisos de pinagem saíram de `app.js` e foram para tabelas/campos do SQLite (seção 4). O JavaScript só guarda comportamento e textos de interface. O antigo `assets/app.js` foi dividido em scripts clássicos em `assets/js/` (não módulos ES, que falham em `file://`); `index.html` os carrega em ordem e todos compartilham o escopo global.

O plugin Sites foi solicitado e suas orientações de interface e SQLite foram consultadas. A solicitação expressa de funcionamento local dispensa registro e publicação. Não há projeto hospedado, `.openai/hosting.json`, conta Cloudflare ou credenciais. O pacote Sites inicialmente legível deixou de aparecer no cache durante o trabalho; não foi possível executar seu configurador (Node inicialmente fora do PATH e, posteriormente, pacote ausente). Isso não afeta os arquivos estáticos entregues.

## 3. Organização

| Caminho | Responsabilidade |
| --- | --- |
| `index.html` | Estrutura, navegação, primeira tela e ícone incorporado |
| `assets/style.css` | Folha única organizada em 11 seções numeradas (tokens, base, estrutura, catálogo, tabela, ficha, histórico, comparação, documentação, dialog, responsivo) |
| `assets/js/core.js` | Utilitários, `state`, índices do catálogo (`loadCatalog`), formatação, estoque e `api()` do servidor |
| `assets/js/documentation.js` | Glossário (dialog, tooltip, página) e página de ferramentas |
| `assets/js/table.js` | Página do catálogo, resumo, filtros, renderizadores por formato de coluna e seletor de colunas |
| `assets/js/history.js` | Aba Histórico: saldo, formulário, linha do tempo, gravar/apagar |
| `assets/js/reader.js` | Datasheet comentado |
| `assets/js/detail.js` | Ficha expandida e abas (especificações, pinagem, PDF) |
| `assets/js/compare.js` | Comparação e barra de seleção |
| `assets/js/app.js` | Navegação, eventos delegados (`clickActions`) e inicialização — carregado por último |
| `data/inventory.sqlite` | Banco canônico, incluído no Git |
| `data/inventory.sql` | Dump textual determinístico; permite reconstrução e revisão |
| `data/catalog.js` | Snapshot determinístico para `file://` |
| `data/sources.json` | URLs, data de obtenção e SHA-256 dos documentos |
| `assets/glossary/*.svg` | Figuras do glossário (QSPI e SPI), desenhadas à mão em SVG; abertas no dialog do termo e ampliáveis em nova aba |
| `data/readers/*.js` | Texto de cada PDF separado por página, carregado sob demanda |
| `assets/documents/*.pdf` | 19 documentos originais locais |
| `assets/pinouts/*.png` | 10 prévias recortadas de páginas e renders oficiais |
| `assets/pinouts/sources/*.png` | Desenhos de pinagem sem PDF oficial, como baixados |
| `data/pinout_sources.json` | URL, SHA-256, crédito e licença desses desenhos |
| `docs/evidence/blackpill-variant.png` | Print fornecido pelo usuário da variante adquirida |
| `docs/SOURCES.md` | Proveniência, créditos e versões documentais |
| `docs/H7R3-PINOUT.md` | Pinagens simples/completa da H7R3, esferas UFBGA144 SMPS GP, paridade das fileiras dos headers duplos e tabela de conferência |
| `docs/ARDUINO-PINOUT.md` | Folhas simples do Uno e do Nano: gerador, fontes, diferenças entre as placas, interrupções |
| `scripts/make_arduino_pinouts.py` | Gera `uno-pinout-simple.png` e `nano-pinout-simple.png` a partir de listas de pinos; requer Pillow |
| `docs/H743-PINOUT.md` | Pinagens da WeAct H743 (LQFP100), paridade P1/P2, recursos da placa ligados aos headers, tabela de conferência e como regerar |
| `scripts/make_h743_pinouts.py` | Gera as sete imagens da H743 a partir do DS12110 local (pdftotext -bbox) e do mapa do esquema; requer Poppler, Pillow e Chrome |
| `docs/G474-PINOUT.md` | Pinagens simples/completa da G474, regra UFQFPN48 × LQFP48, histórico da correção e tabela pino a pino |
| `scripts/db.py` | Biblioteca compartilhada: conexão, `add_movement`/`delete_movement` com validação de saldo, `build_catalog`, snapshots |
| `scripts/migrate.py` | Migrações por `PRAGMA user_version` (v1→v2: histórico e conteúdo da interface) |
| `scripts/server.py` | Servidor local opcional com API de movimentações |
| `scripts/export.py` | Atualiza e confere catálogo JS e dump SQL |
| `scripts/seed.py` | Restaura banco ausente a partir do dump; recusa sobrescrita |
| `scripts/download_sources.py` | Lista explícita de downloads públicos; uso de manutenção |
| `scripts/prepare_documents.py` | Extração textual dos datasheets usando Poppler |
| `scripts/prepare_pinouts.py` | Recorta todas as pinagens; requer Poppler e Pillow |
| `tests/test_inventory.py` | Integridade, conteúdo vindo do banco, arquivos, hashes, reconstrução, regras de movimentação e API do servidor |
| `tests/interface.mjs` | Fluxos da interface em DOM simulado, incluindo histórico em consulta e registro (fetch simulado) |
| `tests/vendor/` | LinkeDOM 0.18.12 e licença MIT, somente para testes |

Nenhum recurso de execução depende de caminhos absolutos desta máquina. O print foi copiado do anexo, não referenciado em `/tmp`. A página também pode ser servida como arquivos estáticos por qualquer servidor, mas isso não é requisito.

## 4. Modelo de dados

SQLite `PRAGMA user_version=6` (migrações em `scripts/migrate.py`; a 3 e a 4 só trocam as pinagens do Uno e do Nano; a 5 cadastra a WeAct H743, a compra de 1 unidade, 4 termos do glossário e a compatibilidade do ST-Link; a 6 acrescenta `aliases`, `figure` e `figure_caption` ao glossário e transforma Quad-SPI em QSPI).

- `categories(id, name)`: inclui `microcontroladores`; o nome vira título e breadcrumb.
- `families(id, name, description, tone, position)`: PIC/AVR/STM32; `tone` é a cor na interface.
- `components(id, category_id, name, family→families, kind, estimated, position, specs)`.
  - **Não há mais coluna `quantity`**: quantidades vêm das movimentações.
  - `kind`: `chip` ou `placa`. `estimated`: 0 ou 1; apenas quantidades PIC são estimadas.
  - `specs`: JSON validado pelo SQLite, com os campos técnicos (flexível para categorias futuras).
  - `clock`: número em MHz; `ram`: inteiro em bytes. `flash`, `external`, `adc`, `gpio`, etc.: texto com unidades.
  - `datasheet`, `pinout`, `pinout_source`, `schematic`: nomes de arquivos locais.
  - `pinouts` (opcional): lista ordenada `{file, title, notice}`; G474, H7R3 e H743 usam. `pinout` continua sendo o primeiro arquivo.
  - Campos de interface (v2): `subtitle` (linha abaixo do nome), `flash_short` (coluna Flash), `processing_class` (→`processing_classes`), `accelerators`, `pin_guide` (→`pin_guides`), `pinout_notice` (aviso na aba Pinagem; BluePill) e `<coluna>_note` (asterisco numa métrica; `coremark_note` da BluePill).
  - `origin`, `notes`, `evidence`, `variant`: contexto do acervo. O antigo `status` foi removido (substituído pelo estoque calculado).
- `movement_types(id, label, action, delta_total, delta_in_use, tone, description, position)`: `compra` (+1 total), `uso` (+1 em uso), `devolucao` (−1 em uso), `descarte` (−1 total), `descarte_em_uso` (−1 total e −1 em uso), `entrada` (+1 total sem compra; cadastro inicial). `action` é o texto do botão no formulário.
- `movements(id, component_id, type_id, quantity>0, date AAAA-MM-DD, note, created_at UTC)`.
- View `component_stock(component_id, total, in_use, available)` = soma de `quantity × delta`. Disponível = total − em uso.
- **Regra de saldo** (`db.check_balances`): percorrendo o histórico por `(date, id)`, em uso e disponível nunca ficam negativos. Vale para inserir (inclusive com data retroativa) e para apagar. Datas futuras são recusadas. A interface desabilita os tipos impossíveis, mas a regra oficial é a do Python.
- `spec_fields(key, label, format text|mhz|bytes, in_sheet, in_compare, position)`: linhas da ficha e da comparação.
- `column_groups(id, label, tone, position)` e `table_columns(key, label, group_id, width, format, field, unit, digits, term, help, position)`: as 23 colunas. `format` escolhe o renderizador em `table.js` (`component`, `family`, `stock`, `class`, `metric`, `annotated`, `text`, `mhz`, `bytes`); `field` lê outro campo (Flash usa `flash_short`); `width` já é a largura final em px. A chave da coluna de quantidade é `stock`.
- `processing_classes(name, rank)`: ordenação da classe de processamento.
- `glossary_categories(id, name, icon, description, tips JSON, position)` e `glossary(term, category_id, position, meaning, short, detail, example, aliases, figure, figure_caption)`: 98 termos (TCM, QSPI, SDMMC e DCMI entraram na v5). `aliases` é uma lista JSON de outras grafias que o reconhecedor de termos também transforma em botão (QSPI: Quad-SPI, QUADSPI, Quad SPI); nenhum nome pode se repetir entre termos e sinônimos (teste). `figure` é um SVG em `assets/glossary/` mostrado no dialog do termo, com `figure_caption`. `detail` aceita parágrafos separados por linha em branco; nesse caso o dialog empilha funcionamento e exemplo; `position` define a ordem dentro da categoria e, portanto, os “termos relacionados”.
- `pin_guides(guide, position, label, term)`: botões de ajuda da aba Pinagem (`pic12`, `pic`, `avr`, `stm32`).
- `tools(id, name, quantity, description, compatibility)`: acessórios de programação/conexão (quantidade simples, sem histórico).

Não há índices especulativos além de chaves primárias; o catálogo inteiro é exportado e filtrado na memória do navegador. `catalog.js` traz, por componente, `stock {total, in_use, available}` e `history` (ordem cronológica). Uma categoria futura ainda exigirá adaptar navegação e textos; adicionar uma linha em categories sozinho não implementa nova experiência.

## 5. Acervo e identificação

| Item | Total (disp./total em 13/09/2026) | Identificação / estado |
| --- | ---: | --- |
| PIC16F887-I/P | 2 estimadas | PDIP-40, 8.192 palavras de 14 bits, 368 B SRAM |
| PIC12F675-I/P | 3 estimadas | PDIP-8, sem PWM por hardware |
| PIC12F683-I/P | 2 estimadas | PDIP-8, CCP/PWM |
| PIC12F1501-I/P | 3 estimadas | PDIP-8, PWM/CLC/NCO/CWG, HEF |
| Arduino Uno | 0/0 | Referência Uno R3/ATmega328P. O cadastro tinha 1; o usuário relatou em 13/09/2026 que quebrou “um dos Arduinos Uno”, registrado como descarte. Se havia mais de um, falta registrar a entrada |
| Arduino Nano | 1/2 | Referência Nano clássico/ATmega328P; o soldado em PCB foi registrado como “em uso”, o solto como disponível (interpretação do agente; o usuário pode registrar “Parei de usar”) |
| BluePill | 3 | STM32F103C8T6 confirmado pelo usuário em 12/09/2026: duas unidades com conector USB-C e uma com micro-USB |
| WeAct BlackPill | 0/1 | STM32F411CEU6, HSE 25 MHz, Flash externa 8 MB, em uso no TCC |
| WeAct G474 Long | 1 | STM32G474CEU6, UFQFPN48, 512 KiB Flash e 128 KiB SRAM; recém-adquirida |
| WeAct H7R3 | 1 | STM32H7R3Z8J6, UFBGA144, 64 KiB internos e 8 MiB externos; recém-adquirida |
| WeAct H743 | 1 (17/09/2026) | STM32H743VIT6, LQFP100, 2 MiB Flash, 1.056 KiB RAM, 480 MHz; placa MiniSTM32H7xx com TFT 0,96″, câmera DVP, microSD, Flash QSPI 8 MB + SPI 8 MB. Identificada pelas fotos do usuário (frente e verso) |

Total cadastrado na v1: 19 unidades. Após o descarte do Uno: 18 no total, 2 em uso, 16 disponíveis (inclui 10 PIC estimadas). A migração converteu cada quantidade antiga em movimentação `entrada` (PICs datadas de 07/05/2026, demais 12/09/2026) ou `compra` (G474 e H7R3, recém-adquiridas; data real da compra não registrada). Não declarar recebimento ou teste das novas placas. Números atualizados ficam no próprio banco — esta tabela é só o retrato da migração.

Ferramentas: 1 CH343P, 1 ST-Link V2, 1 PICkit 3. “picokit 3” foi normalizado para PICkit 3. Não são contadas como microcontroladores.

### Fontes pessoais lidas, sem modificação

- `/home/davi/repos/obsidian-vault/Peças disponiveis/Inventario_Componentes_Eletronicos_Obsidian.md` — documento de 07/05/2026. Contém os quatro PICs e quantidades estimadas. BT145 e IRFP4227 não foram importados porque a categoria solicitada é microcontroladores.
- `/home/davi/repos/TCC/DOCUMENTACAO_TECNICA_CRONOLOGICA.md` — identifica a BlackPill STM32F411CEU6, cristal de 25 MHz e uso da CPU a 96 MHz. Seção 7.5 continha incerteza histórica de capacidade da Flash externa.
- `/home/davi/repos/obsidian-vault/TCC - PIPboy/BlackPill - STM32F411 + 25Mhz + 8M flash.md`.
- `/home/davi/repos/obsidian-vault/TCC - PIPboy/Firmware para leitura e Gravação em 8M de Flash.md` — informa Flash montada e ligações propostas.
- Conversa “Comparar placas STM32”, id `6a9714da-dba0-83e9-8e38-df50b08b01bc`, consultada nesta tarefa. A resposta final corrigida identifica CEU6 Long como 512 KB Flash / 128 KB RAM; não reaproveitar a identificação errada de um anúncio anterior.
- Usuário confirmou nesta tarefa: BlackPill com Flash externa **8 MB**, WeAct. Essa confirmação substitui a incerteza histórica. Print `docs/evidence/blackpill-variant.png` mostra a opção **F411 25M HSE 8MFlash**. Não registrar novamente como capacidade desconhecida.

Em 12/09/2026 o usuário confirmou que as três BluePill são STM32F103C8T6, duas com conector USB-C e uma com micro-USB. Isso encerra a incerteza anterior: a ficha deixou de ser marcada como referência. A busca local havia encontrado uma conversa citada como “Branch · Software para programar Bluepill”, mas o texto consolidado correspondente descreve BlackPill F411; não confundir nome de conversa com prova de MCU, nem importar a identificação de um módulo ADS1256 + F103 de outro projeto como se fosse a BluePill. Continua valendo: não assumir 128 KiB de Flash, porque o datasheet C8 declara 64 KiB.

## 6. Notas técnicas a preservar

- Memória PIC deve conservar **palavras × 14 bits**. KiB é uma equivalência de capacidade, não garante que toolchains tratem programa como bytes comuns.
- SRAM em bytes no banco; interface converte para KiB (kibibytes, 1.024 bytes). MiB = 1.048.576 bytes. Anúncios frequentemente usam KB/MB para capacidades binárias.
- BlackPill: 512 KiB internos, 128 KiB SRAM, 8 MiB de Flash SPI externa conforme confirmação do usuário. F411 não tem DAC nem CAN. O clock máximo é 100 MHz; 96 MHz é configuração do TCC, 25 MHz é cristal externo.
- Flash externa montada não prova que o logger esteja implementado no firmware do TCC. Não mudar essa afirmação sem revisar o firmware.
- G474CEU6: 512 KiB Flash; SRAM 96 + 32 KiB CCM. Long é formato físico; não implica mais pinos que a versão compacta CEU6. O diagrama incluído é QFN48 Long, não QFP48 nem compacto. **Número de pino do CI = coluna UFQFPN48 da tabela 12 do DS12288**, nunca LQFP48 (o LQFP48 nem tem PC4/PC6/PC10/PC11 e desloca a numeração a partir de PB0). Versões antigas do desenho simples tinham 13 números errados (PB10, VREF+, PB11–PB15, PC6, PA8–PA12); as duas imagens atuais estão corrigidas e conferidas. Detalhes e tabela em `docs/G474-PINOUT.md`.
- H7R3: 64 KiB de Flash interna podem hospedar boot e/ou código; não tratar como zero Flash nem como 8 MB internos. A placa WeAct adiciona 8 MB externos. H7R3 **não possui DAC**; fonte usada DS14360 Rev 3. Possui Cortex-M7 com FPU de dupla precisão. Não importar recursos gráficos de H7R7 indiscriminadamente para H7R3.
- H743 (17/09/2026): identificada pelas duas fotos enviadas pelo usuário — marcação **STM32H743VIT6** (terminando em "V", revisão V, 480 MHz) e serigrafia WeAct Studio com SB1–SB6 e R9 no verso (desenho V1.1/V1.2; usado o esquema V1.2). As fotos não ficaram salvas no repositório (o cache do anexo não estava mais disponível); se o usuário quiser evidência como a da BlackPill, pedir as fotos de novo e gravar em `docs/evidence/`. A compra foi registrada como `compra` de 1 unidade em 17/09/2026, com a data real desconhecida — não declarar teste nem uso. **Não confundir com a H750VBT6** (mesma placa, 128 KiB de Flash). RAM: 864 KiB de SRAM + 192 KiB de TCM = 1.056 KiB (a WeAct anuncia "1 MB"). CoreMark 2424 é o valor publicado pela ST para a H743 a 480 MHz (não está no DS12110 local; por isso `coremark_note`); DMIPS 1027 e 2,14 DMIPS/MHz vêm da capa do DS12110. PC2/PC3 existem no LQFP100 só como pads `_C` analógicos. Vários pinos dos headers já estão ligados a LCD, câmera, microSD e flashes — ver `docs/H743-PINOUT.md`.
- GPIO, ADC, DAC e interfaces da família não equivalem automaticamente a sinais expostos na placa nem disponíveis simultaneamente. Verificar encapsulamento e funções alternativas.
- PIC12: GP3/RA3 somente entrada. PIC16F887: RE3 somente entrada. PIC12F675 não tem PWM de hardware. PIC12F1501 usa HEF, não EEPROM clássica.
- PIC ICSP e conector ICSP AVR têm protocolos/sinais diferentes. PICkit 3 não é programador AVR genérico.
- CH343P é ponte USB–UART, não depurador SWD. Níveis elétricos do módulo precisam ser conferidos quando for conectar.
- ST-Link V2: não prometer H7RS sem conferir versão do software, firmware e suporte do gravador. Nenhuma gravação física foi feita.

## 7. Interface e documentação interativa

Os scripts de `assets/js/` renderizam tudo a partir do catálogo, usando escape de conteúdo (`esc`, `annotate`). Delegação de eventos mantém as ações disponíveis após rerender. A seleção de comparação está num Set em memória. A tabela oferece 23 colunas configuráveis, que podem ser exibidas, ocultadas, reordenadas e restauradas; preferências ficam no `localStorage` do navegador. Cabeçalhos com seta ordenam as linhas. Filtros por família e tipo e busca percorrem os campos do item.

As métricas de processamento exibidas incluem classe editorial, aceleradores confirmados, MIPS, DMIPS e CoreMark quando existe uma referência publicada aplicável. MIPS (milhões de instruções por segundo), DMIPS (Dhrystone Million Instructions Per Second) e CoreMark são escalas diferentes e não devem ser comparadas diretamente. A nota abaixo da tabela explicita essa fronteira e identifica o CoreMark da BluePill como referência da mesma família, não medição da variante C8 exata.

Cada linha abre uma seção com abas: especificações, histórico, pinagem, datasheet comentado e original. A aba ativa fica em `state.tab` e sobrevive a um redesenho (necessário após gravar um registro). Abas respondem às setas, Home e End. Ajuda rápida aparece por hover/foco; clique abre um dialog nativo que oferece fechamento e Escape. Termos também podem ser acessados por toque. Layout possui adaptações até telas estreitas e rolagem horizontal da tabela.

**Documentação ampliada (13/09/2026):** a aba Documentação deixou de ser apenas uma grade de títulos. Ela agora começa com dois esquemas conceituais clicáveis e traz um navegador dos 94 termos com busca e filtro por sete categorias. Cada cartão mostra sigla, significado completo, resumo e exemplo antes da abertura. O dialog de cada termo separa linguagem simples, funcionamento/interpretação, exemplo do acervo, checklist de três cuidados relativo à categoria e até cinco termos relacionados. O tooltip de hover/foco também mostra nome completo e resumo. Desde a v2 as categorias, a ordem e os checklists também vêm do SQLite (`glossary_categories`, `glossary.category_id/position`).

**Quantidade X/Y e histórico (13/09/2026):** a coluna “Disponível / total” mostra `disponíveis/total` (asterisco se estimado) e “N em uso”; verde com unidades livres, âmbar quando todas estão em uso, vermelho quando o total é zero. Clicar nela abre a ficha direto na aba Histórico. O resumo do topo mostra modelos, disponíveis/total, em uso e famílias, todos calculados. A ficha tem no cabeçalho três contadores (disponíveis, em uso, total). A aba Histórico tem, à esquerda, o formulário (tipo em botões coloridos, quantidade, data — padrão hoje, sem futuro — e observação) ou o aviso de modo consulta; à direita, a linha do tempo mais recente primeiro, com o saldo disponível/total depois de cada registro e “×” para apagar (só no modo registro, com confirmação). Após gravar, o servidor devolve o catálogo inteiro e a página chama `loadCatalog` + `drawRows`, preservando busca, filtros e aba.

**Visual (13/09/2026, a pedido do usuário):** cabeçalhos das colunas 14 px em peso 800 com filete da cor do grupo; grupos 12 px; menu lateral escuro (verde `#0f3b2e`), itens 17 px semibold e item ativo verde vivo; ficha mais compacta (paddings e linhas da ficha técnica reduzidos, 13 px); paleta mais saturada com tokens `--green/teal/blue/violet/orange/amber/red/slate` e classes `tone-*`, cujos nomes vêm do banco. Famílias: PIC laranja, AVR verde-azulado, STM32 azul. Grupos: Acervo verde, Desempenho violeta, Periféricos azul, Elétrica âmbar. A classe de processamento é uma pílula violeta que escurece com o rank.

**Largura (12/09/2026, ainda válido):** a tabela rola na horizontal dentro de `.table-wrap`, que tem `position:relative`. Sem isso, o `.sr-only` do cabeçalho (`position:absolute`) escapava e alargava a página até ~2.983 px. O detalhamento (`.detail-cell>.detail`) é `position:sticky;left:0` e usa a largura visível da tabela via `--detail-width`, atualizada por `fitDetailWidth()` a cada `drawRows` e `resize`. As imagens de pinagem usam `max-width:100%` e `max-height:min(750px,80vh)`, sem faixas brancas. As larguras de coluna vêm de `table_columns.width` (já incluem a antiga ampliação de 15%). Conferido no Chrome em 1920, 1440, 1100, 700 e ~480 px: largura da página igual à da janela.

**Pinagem da H7R3 em folhas (13/09/2026):** a ficha mostra primeiro as duas visões gerais da placa inteira, `h7-pinout-simple.png` e `h7-pinout-full.png`, mantidas a pedido do usuário. A completa foi regerada com os nomes de AF corrigidos. Em seguida vêm cinco folhas por header (`h7-pinout-simple-left/right`, `h7-pinout-full-left/right/extra`), porque imagens únicas de 5.600–10.900 px ficavam com texto de 2–6 px no painel. Imagens vindas do campo `pinouts` recebem a classe `pinout-sheet` (`detail.js`, `pinoutFigures`): largura total do detalhamento, sem `max-height`. Isso também vale para a G474. Detalhes e hashes em `docs/H7R3-PINOUT.md`. As mudanças de desempenho (MIPS/DMIPS/CoreMark) de outro agente no mesmo intervalo foram preservadas; todos os testes passam.

**Pinagem da H743 (17/09/2026):** mesma organização da H7R3 (duas visões gerais + cinco folhas), a pedido do usuário ("gerar as imagens das pinagens no mesmo padrão"). Diferenças: o pino do CI é o **número LQFP100**; a vista é de cima com o **display no topo** (USB-C embaixo, como na placa e no desenho WeAct); P2 = esquerdo (externa = pares) e P1 = direito (externa = ímpares); e o gerador **está versionado** (`scripts/make_h743_pinouts.py`), lendo as AF direto do PDF local. Leia `docs/H743-PINOUT.md`.

**Datasheet comentado:** arquivo JS por PDF, carregado sob demanda por tag script clássica (compatível com `file://`). Contém páginas de texto extraídas por `pdftotext -layout`, navegação e busca circular por página. Um reconhecedor insensível a maiúsculas transforma os 94 termos cadastrados em botões. Não é um tradutor, modelo de linguagem nem glossário de todas as palavras dos PDFs. Subsímbolos como VDD com formatação especial ou texto dentro de desenhos podem não casar com o reconhecedor.

**Documento original:** objeto PDF local com link alternativo. Diagramação e desenhos do fabricante são preservados. O visualizador nativo de PDF não recebe os tooltips do aplicativo; estes ficam na leitura comentada e nas fichas. Comportamento do visualizador varia conforme navegador. Não prometer anotação visual sobre cada palavra do PDF original.

**Pinagem:** recortes de páginas e imagens oficiais, sem desenho inventado ou arte gerada por IA. `scripts/prepare_pinouts.py` descarta cabeçalho, rodapé, espaço vazio e encapsulamentos que não estão no acervo, e empilha diagrama e tabela de funções quando o fabricante as publica em páginas separadas. Cada ficha mostra o crédito da imagem, gravado em `pinout_credit`.

Os quatro PICs trazem o diagrama PDIP mais a tabela de alocação de funções. **Uno (13/09/2026):** a pedido do usuário (“imagem com poucos dados”), a ficha mostra primeiro `uno-pinout-simple.png`, desenho do almoxarifado no estilo simples da G474/H7R3 com porta, pino DIP-28/QFP-32 e funções de todos os furos, e depois a folha oficial Arduino como referência. **Nano (13/09/2026):** mesma solução, com `nano-pinout-simple.png` (chip QFP-32, A6/A7 só analógicos, dois RST, FT232RL/CH340) antes da folha oficial. Diferente da G474, o gerador das duas está versionado: `scripts/make_arduino_pinouts.py`; leia `docs/ARDUINO-PINOUT.md`. As caixas de PCINT dizem “sem attachInterrupt”: só D2/D3 aceitam `attachInterrupt()`. BluePill passou a usar *The Generic STM32F103 Pinout Diagram* de Rasmus Friis Kjeldsen, CC BY-SA 4.0 — desenho da placa, com funções alternativas e limites elétricos; a imagem mostra a variante micro-USB, e duas das três unidades são USB-C. Obra derivada desse desenho precisa manter a mesma licença. **Exceção à regra de não redesenhar:** a pedido do usuário, a H7R3 mostra as folhas `h7-pinout-simple-left/right.png` e `h7-pinout-full-left/right/extra.png`, desenhos do almoxarifado no mesmo estilo dos da G474. Pino do CI = esfera da coluna UFBGA144 SMPS GP (não a GFx); headers duplos com paridade invertida: externa = par em P1/P3, ímpar em P2/P4; LTDC, ETH MII e Hexa-SPI omitidos por não existirem no Z8J6. Leia `docs/H7R3-PINOUT.md`. O recorte `h7-pinout.png` continua gerado por `prepare_pinouts.py`, mas não é exibido. A G474 Long mostra dois desenhos feitos para o almoxarifado, empilhados pelo campo `pinouts`: `g474-long-pinout-simple.png` (colunas sobre o render WeAct; funções principais) e, abaixo, `g474-long-pinout-full.png` (vetorial; todas as AF0–AF15 com número, funções adicionais, tolerância FT/TT e pinos fora dos headers). Ambas usam a numeração UFQFPN48 conferida na tabela 12 e no esquema. São os únicos arquivos de pinagem da G474; o antigo recorte `g474-long-pinout.png` e a receita dele em `prepare_pinouts.py` foram removidos. Leia `docs/G474-PINOUT.md` antes de alterar essas imagens. A pinagem da BlackPill não foi alterada a pedido do usuário: continua sendo o desenho WeAct v2.0+ de Richard Balint, byte a byte igual, com anotações de família — o datasheet F411 prevalece para recursos do chip.

## 8. Manutenção

Executar na raiz do clone. Uso normal só precisa do navegador. Manutenção do banco requer Python 3 com sqlite3 (biblioteca padrão). Extração textual requer Poppler; recortar pinagens requer Poppler e Pillow (`python3-pil`); testes DOM requerem Node.js moderno, que nesta máquina não está no PATH (há um binário em `~/.lmstudio/.internal/utils/node`). Nenhuma dependência é instalada ao abrir o site.

Registrar compra, uso ou descarte (uso diário):

```bash
# Abre o site no navegador com o formulário da aba Histórico; Ctrl+C encerra.
python3 scripts/server.py
# Depois, guardar no Git: data/inventory.sqlite, data/inventory.sql e data/catalog.js.
```

Agentes também podem registrar sem navegador, com a mesma validação:

```bash
python3 -c "import sys; sys.path.insert(0,'scripts'); import db; con=db.connect(); db.add_movement(con,'uno','compra',1,'2026-09-20','Nota'); db.write_snapshots(con)"
```

Mudança de estrutura: acrescentar função em `scripts/migrate.py` (`MIGRATIONS[3] = ...`), subir `db.SCHEMA_VERSION`, rodar `python3 scripts/migrate.py` e exportar. Não reescrever migrações já aplicadas.

Depois de editar o SQLite:

```bash
# Gera a página de dados e a representação SQL revisável a partir do banco.
python3 scripts/export.py

# Confere se os dois arquivos gerados correspondem exatamente ao banco.
python3 scripts/export.py --check

# Valida banco, fontes, arquivos e reconstrução.
python3 -m unittest discover -s tests -v

# Testa as interações em uma árvore de documento simulada, sem navegador.
node tests/interface.mjs
```

A opção `--check` não grava; falha se qualquer snapshot estiver desatualizado. `-m` executa módulo Python; `discover -s tests` procura testes na pasta tests; `-v` detalha os resultados. `node` executa JavaScript fora do navegador.

Para adicionar componente, usar uma migração explícita no SQLite com parâmetros e transação; preencher proveniência e pendências. Para permitir revisão, exportar e revisar `git diff -- data/inventory.sql`. Nunca excluir o banco para rodar seed: o seed é apenas restauração quando o banco não existe, a partir do SQL versionado.

Atualização voluntária dos documentos:

```bash
# Obtém apenas documentos listados que ainda não estão presentes; requer internet.
python3 scripts/download_sources.py

# Extrai o texto dos datasheets; requer Poppler instalado.
python3 scripts/prepare_documents.py

# Recorta todas as pinagens; requer Poppler e Pillow.
python3 scripts/prepare_pinouts.py

# Inclui a proveniência atualizada no snapshot do catálogo.
python3 scripts/export.py
```

O script de download não atualiza silenciosamente um PDF existente. Para mudar revisão, preservar o anterior até validar o substituto, alterar a lista explicitamente, conferir contagem/pinagens e atualizar docs/SOURCES.md. Hashes são SHA-256 (resumo criptográfico do conteúdo), úteis para detectar alteração dos arquivos.

### Git e conflitos de banco

Banco binário não deve ser mesclado automaticamente. Rever as alterações SQL dos dois lados, resolver a intenção das mudanças, aplicar numa cópia validada e gerar os snapshots novamente. Não executar o dump de uma versão por cima de um banco existente. O teste de roundtrip já verifica que a versão SQL atual reconstrói os mesmos registros.

Comitar somente arquivos desta tarefa. `git pull` recebe atualizações, `git push` envia commits; o usuário executa normalmente. Não há sincronização automática nem escrita em serviço externo.

## 9. Validação desta entrega

- 12 testes de dados passaram: integridade SQLite, chaves estrangeiras, quantidades, variantes confirmadas, métricas publicadas, todos os caminhos locais, versões de pinagem, hashes de todos os PDFs, hashes/crédito/licença das imagens de pinagem, existência dos textos, reconstrução por SQL, exportação determinística e ausência de dependências de rede de execução.
- Testes de interação passaram com LinkeDOM: busca com/sem resultado, filtro de família, expansão, caminhos de pinagem e PDF, comparação/diferenças/remoção, esquemas da documentação, 94 cartões, busca e filtro por categoria, estrutura detalhada do dialog, ferramentas, leitor e busca/paginação/limites.
- Sintaxe JavaScript verificada pelo Node.
- Pinagem G474 (12/09/2026): 10 testes de dados e o teste de interface passaram. `test_g474_pinout_versions` confere a ordem simples → completa, os PNGs e que não existam outros arquivos de pinagem da G474; o teste de interface confere as duas imagens empilhadas na aba. Números UFQFPN48 conferidos contra a tabela 12 do DS12288 e o U1 do esquema WeAct.
- Todas as prévias de pinagem foram inspecionadas como imagens locais depois do recorte: os quatro PICs com diagrama e tabela, BluePill, Uno, Nano, G474 Long, H7R3 e a BlackPill inalterada. O arquivo da BlackPill foi conferido por hash antes e depois de rodar o gerador.
- Os PDFs são snapshots técnicos, não todos as revisões mais recentes. Seu hash, data de obtenção e número de páginas estão registrados; não afirmar revisão de todas as páginas ou todas as especificações elétricas.
- Validação visual em navegador real concluída em 12/09/2026 por servidor HTTP local temporário, restrito a `127.0.0.1:8765`: tabela larga, menu aberto, ocultar coluna, restaurar e persistência após recarregar foram conferidos. O servidor foi encerrado; nenhuma porta é necessária para o uso normal por `file://`.

- Entrega de 13/09/2026 (histórico, organização e visual): 20 testes Python passaram (acrescentados conteúdo vindo do banco, consistência de todos os históricos, compra/uso/liberação/descarte, recusa de saldo negativo, data inválida/futura/retroativa, apagar mantendo saldo válido, API do servidor com banco temporário, bloqueio de Host/Origin/Content-Type e de `.git`) e o teste de interface passou (tabela gerada do banco, X/Y por componente, histórico em consulta, formulário com tipos desabilitados e gravação com fetch simulado). No Chrome headless: servidor numa cópia do projeto (sem tocar o banco real), registro “Parei de usar” pelo formulário atualizou a linha para 2/2 e gravou `catalog.js`/`inventory.sql`; `file://` mostrou o aviso de consulta; largura da página igual à janela em 1600, 1280 e 480 px. Migração v1→v2 conferida: totais antigos = soma das movimentações (menos o Uno descartado) e `foreign_key_check` vazio.

- Entrega de 17/09/2026 (WeAct H743): migração v5 aplicada; 23 testes Python passaram (novos: `test_h743_pinout_versions`, `test_h743_header_map`, métricas e variante da H743) e o teste de interface passou (11 modelos, 5 STM32, sete imagens da H743 na aba Pinagem, 98 termos). As sete imagens foram inspecionadas visualmente. A extração das AF foi conferida contra a tabela 9 do DS12110; um vazamento do cabeçalho das tabelas ("CEC", "ETH" falsos em PB0, PE0, PE14, PD8, PC0) foi encontrado e corrigido antes da geração final.

- Entrega de 17/09/2026 (documentação de QSPI, a pedido do usuário: "adicione documentação para QSPI também, assim como tem para SPI"): "QSPI" na ficha da H743 não virava termo porque o verbete se chamava Quad-SPI. A migração v6 renomeou para QSPI, criou sinônimos e reescreveu a explicação em quatro parágrafos (ligação e bit QE, fases do comando e dummy, modos indireto/polling/mapeado em 0x9000 0000 com páginas de 256 B e setores de 4 KiB, velocidade até 133 MHz e bancos). Novas figuras `assets/glossary/qspi.svg` (SPI × QSPI com os pinos da H743 e leitura EBh 1-4-4 clock a clock) e `spi.svg` (barramento com dois CS, byte 9Fh no modo 0 e tabela CPOL/CPHA). Conferido no Chrome: dialog alarga para até 1040 px quando há figura. 23 testes Python e o de interface passaram (sinônimos únicos, figuras SVG existentes, "QSPI" da ficha abre o termo com figura).

## 10. Próximos passos e limites concretos

1. Usuário abrir index.html, conferir tabela, expandir BlackPill/G474, visualizar pinagem e datasheet, comparar dois componentes. Registrar o resultado da revisão visual e corrigir qualquer problema encontrado.
2. BluePill: marcação C8T6 confirmada pelo usuário e qualificação de referência retirada. Falta, se o usuário quiser, um desenho específico da variante USB-C — o diagrama atual é da variante micro-USB e serve para as três porque o chip é o mesmo.
3. Confirmar as revisões Uno/Nano e quantidades PIC somente quando houver nova informação, sem impedir a consulta atual.
4. Expandir glossário conforme termos que o usuário encontrar. Para cobertura visual sobre todas as palavras do PDF original, uma etapa futura poderia usar um renderizador local com camada de texto; avaliar tamanho e compatibilidade `file://` antes de mudar a arquitetura.
5. H743: se o usuário enviar de novo as fotos, guardá-las em `docs/evidence/` e preencher `evidence`. Conferir no próprio verso se SB1–SB3 estão fechadas e SB4–SB6 abertas antes de usar PA7, PD4 ou PD6 como GPIO livre.
6. Adicionar novas categorias apenas quando solicitado; não incluir automaticamente os semicondutores de potência do Obsidian.
7. Resolvido pelo próprio usuário via `scripts/server.py` em 13/09/2026: apagou o descarte do Uno criado pela migração (Uno voltou a 1/1) e registrou `descarte_em_uso` do Nano soldado (“tentei dessoldar e derreti ela”), deixando o Nano em 1/1. Registros do usuário são a fonte de verdade; não recriar os da migração. O teste de interface usa um catálogo de fixture para o histórico e não depende desses números.

Para qualquer etapa manual, seguir instruções do usuário: concluir trabalho independente primeiro, fornecer seção “Ação manual necessária”, comandos mínimos explicados e diretório, nunca pedir senha, aguardar “feito” ou saída e continuar.

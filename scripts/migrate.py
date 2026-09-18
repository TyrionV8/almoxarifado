"""Aplica, em transação, as migrações pendentes do banco (PRAGMA user_version).

Uso: python3 scripts/migrate.py   (depois: python3 scripts/export.py)

Cada migração é um registro histórico: não altere uma migração já aplicada;
acrescente uma nova função e registre-a em MIGRATIONS.
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import db  # noqa: E402


# ---------------------------------------------------------------- versão 2
# Histórico de unidades (disponível / em uso / total) e conteúdo que antes
# ficava fixo em assets/app.js: colunas da tabela, campos da ficha, categorias
# do glossário, guias de pinos, classes de processamento e famílias.

FAMILIES = [
    ('PIC', 'PIC', 'Microchip PIC de 8 bits', 'orange'),
    ('AVR', 'AVR', 'Microchip AVR (Arduino)', 'teal'),
    ('STM32', 'STM32', 'ST Microelectronics Arm Cortex-M', 'blue'),
]

MOVEMENT_TYPES = [
    # id, rótulo no histórico, texto no formulário, efeito no total, efeito em uso, cor, explicação
    ('compra', 'Compra', 'Comprei mais', 1, 0, 'green', 'Unidades novas entram como disponíveis.'),
    ('uso', 'Em uso', 'Coloquei em uso', 0, 1, 'blue', 'Unidades disponíveis passam a ficar ocupadas em um projeto.'),
    ('devolucao', 'Liberada', 'Parei de usar', 0, -1, 'teal', 'Unidades em uso voltam a ficar disponíveis.'),
    ('descarte', 'Descarte', 'Descartei (quebrou, perdi, doei)', -1, 0, 'red', 'Unidades disponíveis saem do acervo.'),
    ('descarte_em_uso', 'Descarte em uso', 'Descartei uma que estava em uso', -1, -1, 'red', 'Unidades que estavam em uso saem do acervo.'),
    ('entrada', 'Entrada', 'Entrada sem compra (contagem, presente)', 1, 0, 'slate', 'Cadastro inicial ou unidades recebidas sem compra.'),
]

# Quantidades da versão 1 viram movimentações; datas conforme a origem de cada registro.
INITIAL_MOVEMENTS = [
    ('pic16f887', 'entrada', 2, '2026-05-07', 'Quantidade estimada no inventário do Obsidian.'),
    ('pic12f675', 'entrada', 3, '2026-05-07', 'Quantidade estimada no inventário do Obsidian.'),
    ('pic12f683', 'entrada', 2, '2026-05-07', 'Quantidade estimada no inventário do Obsidian.'),
    ('pic12f1501', 'entrada', 3, '2026-05-07', 'Quantidade estimada no inventário do Obsidian.'),
    ('uno', 'entrada', 1, '2026-09-12', 'Cadastro inicial do catálogo.'),
    ('uno', 'descarte', 1, '2026-09-13', 'Quebrou sem querer.'),
    ('nano', 'entrada', 2, '2026-09-12', 'Cadastro inicial: um soldado em placa de circuito impresso (PCB) e outro solto.'),
    ('nano', 'uso', 1, '2026-09-12', 'Unidade soldada em placa de circuito impresso (PCB).'),
    ('bluepill', 'entrada', 3, '2026-09-12', 'Cadastro inicial: duas com USB-C e uma com micro-USB.'),
    ('blackpill', 'entrada', 1, '2026-09-12', 'Cadastro inicial do catálogo.'),
    ('blackpill', 'uso', 1, '2026-09-12', 'Montagem do TCC.'),
    ('g474', 'compra', 1, '2026-09-12', 'Recém-adquirida; data exata da compra não registrada.'),
    ('h7r3', 'compra', 1, '2026-09-12', 'Recém-adquirida; data exata da compra não registrada.'),
]

SPEC_FIELDS = [
    # chave, rótulo, formato, na ficha, na comparação
    ('variant', 'Variante da placa', 'text', 1, 1),
    ('cpu', 'CPU', 'text', 1, 1),
    ('clock', 'Clock máximo', 'mhz', 1, 1),
    ('oscillator', 'Oscilador da placa / chip', 'text', 1, 1),
    ('flash', 'Flash interna', 'text', 1, 1),
    ('external', 'Flash externa', 'text', 1, 1),
    ('ram', 'SRAM', 'bytes', 1, 1),
    ('eeprom', 'EEPROM / HEF', 'text', 1, 1),
    ('package', 'Encapsulamento', 'text', 1, 1),
    ('gpio', 'GPIO', 'text', 1, 1),
    ('adc', 'ADC', 'text', 1, 1),
    ('dac', 'DAC', 'text', 1, 1),
    ('pwm', 'PWM', 'text', 1, 1),
    ('timers', 'Timer', 'text', 1, 1),
    ('serial', 'Comunicação', 'text', 1, 1),
    ('voltage', 'Lógica / alimentação de referência', 'text', 1, 1),
    ('temperature', 'Temperatura', 'text', 1, 1),
    ('programmer', 'Gravação', 'text', 1, 1),
    ('special', 'Outros recursos', 'text', 1, 1),
    ('use', 'Aplicações', 'text', 0, 1),
    ('notes', 'Observações', 'text', 0, 1),
]

COLUMN_GROUPS = [
    ('acervo', 'Acervo', 'green'),
    ('desempenho', 'Desempenho e memória', 'violet'),
    ('perifericos', 'Periféricos', 'blue'),
    ('eletrica', 'Elétrica', 'amber'),
    ('detalhes', 'Detalhes', 'slate'),
]

TABLE_COLUMNS = [
    # chave, rótulo, grupo, largura, formato, campo, unidade, casas, termo, ajuda
    ('name', 'Componente', 'acervo', 270, 'component', None, None, None, None, None),
    ('family', 'Família', 'acervo', 90, 'family', None, None, None, None, None),
    ('stock', 'Disponível / total', 'acervo', 130, 'stock', None, None, None, None,
     'Unidades disponíveis / total no acervo. Registre compras, uso e descartes na aba Histórico.'),
    ('processing_class', 'Classe de processamento', 'desempenho', 178, 'class', None, None, None, None, None),
    ('mips_peak', 'Pico MIPS', 'desempenho', 144, 'metric', None, 'MIPS', 0, 'MIPS',
     'Milhões de instruções por segundo. Usado aqui somente para PIC e ATmega328P.'),
    ('coremark', 'CoreMark', 'desempenho', 144, 'metric', None, None, None, 'CoreMark',
     'Pontuação do benchmark CoreMark. Maior é melhor.'),
    ('coremark_per_mhz', 'CoreMark/MHz', 'desempenho', 167, 'metric', None, None, 2, 'CoreMark',
     'CoreMark dividido pela frequência em megahertz.'),
    ('dmips', 'DMIPS', 'desempenho', 121, 'metric', None, None, 0, 'DMIPS',
     'Resultado do benchmark Dhrystone. Maior é melhor.'),
    ('dmips_per_mhz', 'DMIPS/MHz', 'desempenho', 144, 'metric', None, None, 2, 'DMIPS',
     'DMIPS dividido pela frequência em megahertz.'),
    ('relative_bluepill', 'Relativo à BluePill', 'desempenho', 178, 'metric', None, '×', 2, None,
     'DMIPS do componente dividido pelos 90 DMIPS da BluePill.'),
    ('accelerators', 'Aceleradores', 'desempenho', 253, 'annotated', None, None, None, None, None),
    ('cpu', 'Núcleo / recursos', 'desempenho', 218, 'text', None, None, None, 'CPU', None),
    ('clock', 'Clock', 'desempenho', 106, 'mhz', None, None, None, 'Clock', None),
    ('flash', 'Flash', 'desempenho', 121, 'annotated', 'flash_short', None, None, 'Flash', None),
    ('ram', 'SRAM', 'desempenho', 121, 'bytes', None, None, None, 'SRAM', None),
    ('eeprom', 'EEPROM / HEF', 'desempenho', 167, 'annotated', None, None, None, 'EEPROM', None),
    ('gpio', 'GPIO', 'perifericos', 201, 'annotated', None, None, None, 'GPIO', None),
    ('adc', 'ADC', 'perifericos', 213, 'annotated', None, None, None, 'ADC', None),
    ('dac', 'DAC', 'perifericos', 173, 'annotated', None, None, None, 'DAC', None),
    ('pwm', 'PWM', 'perifericos', 201, 'annotated', None, None, None, 'PWM', None),
    ('timers', 'Temporizadores', 'perifericos', 242, 'annotated', None, None, None, 'Timer', None),
    ('serial', 'Comunicação', 'perifericos', 282, 'annotated', None, None, None, None, None),
    ('voltage', 'Lógica', 'eletrica', 115, 'text', None, None, None, None, None),
]

PROCESSING_CLASSES = [
    ('Essencial', 1), ('Básico', 2), ('Intermediário', 3),
    ('Avançado', 4), ('Avançado especializado', 5), ('Alto desempenho', 6),
]

COMPONENT_EXTRAS = {
    # subtítulo na tabela, Flash resumida, classe, aceleradores, guia de pinos
    'pic16f887': ('PDIP-40', '14 KiB', 'Essencial', 'Nenhum dedicado', 'pic'),
    'pic12f675': ('PDIP-8', '1,75 KiB', 'Essencial', 'Nenhum dedicado', 'pic12'),
    'pic12f683': ('PDIP-8', '3,5 KiB', 'Essencial', 'Nenhum dedicado', 'pic12'),
    'pic12f1501': ('PDIP-8', '1,75 KiB', 'Essencial', 'CLC · NCO · CWG', 'pic12'),
    'uno': ('Placa · ATmega328P', '32 KiB', 'Básico', 'Nenhum dedicado', 'avr'),
    'nano': ('Placa · ATmega328P', '32 KiB', 'Básico', 'Nenhum dedicado', 'avr'),
    'bluepill': ('STM32F103C8T6', '64 KiB', 'Intermediário', 'Nenhum dedicado', 'stm32'),
    'blackpill': ('STM32F411CEU6', '512 KiB', 'Avançado', 'FPU · DSP', 'stm32'),
    'g474': ('STM32G474CEU6', '512 KiB', 'Avançado especializado', 'FPU · DSP · CORDIC · FMAC', 'stm32'),
    'h7r3': ('STM32H7R3Z8J6', '64 KiB de boot Flash', 'Alto desempenho', 'FPU dupla precisão · DSP · cache · CORDIC', 'stm32'),
}

BLUEPILL_PINOUT_NOTICE = ('Diagrama genérico da placa BluePill STM32F103. As três unidades são STM32F103C8T6, duas com '
                          'conector USB-C e uma com micro-USB; o desenho mostra a variante micro-USB. Confira a posição '
                          'do conector e dos jumpers BOOT antes de ligar.')
BLUEPILL_COREMARK_NOTE = ('Referência publicada para o STM32F103RB da mesma família; não é uma medição do STM32F103C8 exato.')

PIC12_PINS = [
    ('1 · VDD', 'VDD'), ('2 · GP5 / RA5 · clock', 'Clock'), ('3 · GP4 / RA4 · analógico', 'ADC'),
    ('4 · GP3 / RA3 · MCLR / VPP', 'MCLR'), ('5 · GP2 / RA2 · funções alternativas', 'GPIO'),
    ('6 · GP1 / RA1 · ICSPCLK', 'ICSP'), ('7 · GP0 / RA0 · ICSPDAT', 'ICSP'), ('8 · VSS', 'VSS'),
]
GENERIC_PINS = [('Alimentação e referência', 'VDD'), ('Pinos de entrada / saída', 'GPIO'),
                ('Entradas analógicas', 'ADC'), ('Comunicação serial', 'UART'), ('Sinais SPI', 'SPI')]
PROGRAMMING_TERM = {'pic': 'ICSP', 'avr': 'Bootloader', 'stm32': 'SWD'}

GLOSSARY_CATEGORIES = [
    ('fundamentos', 'Processamento e desempenho', '◎',
     'Como o microcontrolador executa trabalho e como comparar sua capacidade sem confundir frequência, arquitetura e testes.',
     ['MCU', 'CPU', 'Clock', 'MHz', 'PLL', 'MIPS', 'DMIPS', 'CoreMark', 'FPU', 'DSP', 'DMA', 'CORDIC', 'FMAC', 'Watchdog', 'Interrupt'],
     ['Compare números obtidos pelo mesmo método; MIPS, DMIPS e CoreMark usam escalas diferentes.',
      'Confirme se o recurso é do núcleo, de um periférico ou de um acelerador separado.',
      'Frequência máxima indica ritmo de clock, não garante sozinha menor tempo de execução.']),
    ('memoria', 'Memória e inicialização', '▤',
     'Onde programa e dados ficam guardados, o que se perde ao desligar e como o firmware começa a executar.',
     ['Flash', 'SRAM', 'EEPROM', 'HEF', 'CCM'],
     ['Separe memória não volátil, que retém dados sem energia, da memória de trabalho volátil.',
      'Confira tamanho, endereço, resistência a escritas e quais controladores conseguem acessar cada banco.',
      'Reserve margem para pilha, buffers e atualizações; a capacidade anunciada não fica toda livre para a aplicação.']),
    ('analogico', 'Analógico, tempo e controle', '∿',
     'Como tensões viram números, números viram sinais e temporizadores coordenam medições e acionamentos.',
     ['ADC', 'DAC', 'PWM', 'Timer', 'HRTIM', 'CCP', 'ECCP', 'OPAMP', 'VREF', 'LSB', 'INL', 'DNL', 'ENOB', 'SNR', 'SPS', 'MSPS', 'NCO', 'CWG', 'CLC'],
     ['Resolução nominal não é o mesmo que precisão: referência, ruído, linearidade e tempo de aquisição também importam.',
      'Verifique se o canal chega ao pino da placa e se não conflita com outra função alternativa.',
      'Para cargas de potência, a saída do microcontrolador comanda um driver; ela não deve alimentar a carga diretamente.']),
    ('comunicacao', 'Pinos e comunicação', '⇄',
     'Como bits e sinais trafegam entre o microcontrolador, sensores, módulos e o computador.',
     ['GPIO', 'GPIO 5 V tolerant', 'UART', 'USART', 'EUSART', 'SPI', 'I2C', 'USB', 'CAN', 'FDCAN', 'MSSP', 'MOSI', 'MISO', 'SCK', 'SDA', 'SCL', 'TX', 'RX', 'CS', 'Pull-up', 'Open Drain', 'PHY'],
     ['Antes de ligar, confirme tensão lógica, direção do sinal, referência GND e pinagem dos dois lados.',
      'Controlador interno, transceptor elétrico e conector físico são partes diferentes; a placa pode não incluir todas.',
      'Funções alternativas compartilham pinos, portanto nem todas as interfaces ficam disponíveis simultaneamente.']),
    ('eletrica', 'Alimentação, clock e limites', '⚡',
     'Tensões, correntes, referências e condições que definem uma conexão segura e confiável.',
     ['VDD', 'VSS', 'GND', 'VIL', 'VIH', 'VOL', 'VOH', 'IDD', 'Absolute Maximum Ratings', 'Typical', 'Min', 'Max', 'VBAT', 'HSE', 'HSI', 'LSE', 'RTC'],
     ['Projete com as condições operacionais recomendadas; limite máximo absoluto é fronteira de dano, não ponto de trabalho.',
      'Leia sempre unidade, tensão de alimentação, temperatura e corrente usadas na medição da tabela.',
      'Terra comum é necessário para sinais referenciados, mas não corrige níveis lógicos incompatíveis.']),
    ('gravacao', 'Gravação e depuração', '⌁',
     'Como carregar firmware, escolher o modo de partida, reiniciar e investigar o programa em execução.',
     ['SWD', 'ICSP', 'DFU', 'Bootloader', 'BOOT0', 'NRST', 'MCLR', 'Fuses'],
     ['Confirme família do chip, interface, tensão de referência e suporte do software antes de conectar o gravador.',
      'Bootloader ocupa ou redireciona parte da memória; o endereço da aplicação precisa corresponder ao método de inicialização.',
      'Bits de configuração podem alterar clock, proteção e reset; registre o estado antes de modificá-los.']),
    ('fisico', 'Encapsulamento e documentos', '▦',
     'Como reconhecer o componente físico, orientar seus pinos e localizar a informação completa do fabricante.',
     ['KiB', 'Pinout', 'Datasheet', 'PDIP', 'LQFP', 'UFQFPN', 'UFBGA', 'PCB'],
     ['Confirme código completo, encapsulamento, revisão da placa e orientação do pino 1.',
      'Pinout resume posições; datasheet define limites; manual de referência detalha registros e periféricos.',
      'O número de terminais do encapsulamento não equivale à quantidade de GPIO livres.']),
]

SCHEMA_2 = '''
CREATE TABLE families(
  id TEXT PRIMARY KEY, name TEXT NOT NULL, description TEXT NOT NULL,
  tone TEXT NOT NULL, position INTEGER NOT NULL);
CREATE TABLE components_v2(
  id TEXT PRIMARY KEY,
  category_id TEXT NOT NULL REFERENCES categories(id),
  name TEXT NOT NULL,
  family TEXT NOT NULL REFERENCES families(id),
  kind TEXT NOT NULL CHECK(kind IN ('chip','placa')),
  estimated INTEGER NOT NULL CHECK(estimated IN (0,1)),
  position INTEGER NOT NULL,
  specs TEXT NOT NULL CHECK(json_valid(specs)));
CREATE TABLE movement_types(
  id TEXT PRIMARY KEY, label TEXT NOT NULL, action TEXT NOT NULL,
  delta_total INTEGER NOT NULL CHECK(delta_total IN (-1,0,1)),
  delta_in_use INTEGER NOT NULL CHECK(delta_in_use IN (-1,0,1)),
  tone TEXT NOT NULL, description TEXT NOT NULL, position INTEGER NOT NULL);
CREATE TABLE movements(
  id INTEGER PRIMARY KEY,
  component_id TEXT NOT NULL REFERENCES components(id),
  type_id TEXT NOT NULL REFERENCES movement_types(id),
  quantity INTEGER NOT NULL CHECK(quantity > 0),
  date TEXT NOT NULL CHECK(date GLOB '[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]'),
  note TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL);
CREATE TABLE spec_fields(
  key TEXT PRIMARY KEY, label TEXT NOT NULL,
  format TEXT NOT NULL CHECK(format IN ('text','mhz','bytes')),
  in_sheet INTEGER NOT NULL CHECK(in_sheet IN (0,1)),
  in_compare INTEGER NOT NULL CHECK(in_compare IN (0,1)),
  position INTEGER NOT NULL);
CREATE TABLE column_groups(
  id TEXT PRIMARY KEY, label TEXT NOT NULL, tone TEXT NOT NULL, position INTEGER NOT NULL);
CREATE TABLE table_columns(
  key TEXT PRIMARY KEY, label TEXT NOT NULL,
  group_id TEXT NOT NULL REFERENCES column_groups(id),
  width INTEGER NOT NULL CHECK(width > 0),
  format TEXT NOT NULL CHECK(format IN ('component','family','stock','class','metric','annotated','text','mhz','bytes')),
  field TEXT, unit TEXT, digits INTEGER, term TEXT REFERENCES glossary(term), help TEXT,
  position INTEGER NOT NULL);
CREATE TABLE processing_classes(name TEXT PRIMARY KEY, rank INTEGER NOT NULL UNIQUE);
CREATE TABLE glossary_categories(
  id TEXT PRIMARY KEY, name TEXT NOT NULL, icon TEXT NOT NULL, description TEXT NOT NULL,
  tips TEXT NOT NULL CHECK(json_valid(tips)), position INTEGER NOT NULL);
CREATE TABLE glossary_v2(
  term TEXT PRIMARY KEY,
  category_id TEXT NOT NULL REFERENCES glossary_categories(id),
  position INTEGER NOT NULL,
  meaning TEXT NOT NULL, short TEXT NOT NULL, detail TEXT NOT NULL, example TEXT NOT NULL);
CREATE TABLE pin_guides(
  guide TEXT NOT NULL, position INTEGER NOT NULL, label TEXT NOT NULL,
  term TEXT NOT NULL REFERENCES glossary(term),
  PRIMARY KEY(guide, position));
'''

# Criada depois das tabelas renomeadas: o SQLite revalida views a cada ALTER TABLE.
STOCK_VIEW = '''
CREATE VIEW component_stock AS
  SELECT c.id AS component_id,
         COALESCE(SUM(m.quantity * t.delta_total), 0) AS total,
         COALESCE(SUM(m.quantity * t.delta_in_use), 0) AS in_use,
         COALESCE(SUM(m.quantity * (t.delta_total - t.delta_in_use)), 0) AS available
  FROM components c
  LEFT JOIN movements m ON m.component_id = c.id
  LEFT JOIN movement_types t ON t.id = m.type_id
  GROUP BY c.id;
'''


def run_script(con: sqlite3.Connection, script: str) -> None:
    # executescript() faria COMMIT antes; comandos individuais mantêm a migração numa só transação.
    for statement in script.split(';\n'):
        if statement.strip():
            con.execute(statement)


def migrate_to_2(con: sqlite3.Connection) -> None:
    run_script(con, SCHEMA_2)
    con.executemany('INSERT INTO families VALUES (?, ?, ?, ?, ?)',
                    [(*family, i) for i, family in enumerate(FAMILIES, 1)])

    for position, row in enumerate(con.execute('SELECT * FROM components ORDER BY rowid').fetchall(), 1):
        specs = json.loads(row['specs'])
        subtitle, flash_short, processing_class, accelerators, pin_guide = COMPONENT_EXTRAS[row['id']]
        specs.pop('status', None)  # substituído pelo estoque calculado e pelo histórico
        specs.update(subtitle=subtitle, flash_short=flash_short, processing_class=processing_class,
                     accelerators=accelerators, pin_guide=pin_guide)
        if row['id'] == 'bluepill':
            specs.update(pinout_notice=BLUEPILL_PINOUT_NOTICE, coremark_note=BLUEPILL_COREMARK_NOTE)
        con.execute('INSERT INTO components_v2 VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (row['id'], row['category_id'], row['name'], row['family'], row['kind'], row['estimated'],
                     position, json.dumps(specs, ensure_ascii=False, sort_keys=True)))
    old_totals = dict(con.execute('SELECT id, quantity FROM components'))
    con.execute('DROP TABLE components')
    con.execute('ALTER TABLE components_v2 RENAME TO components')
    run_script(con, STOCK_VIEW)

    con.executemany('INSERT INTO movement_types VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    [(*kind, i) for i, kind in enumerate(MOVEMENT_TYPES, 1)])
    created = db.now()
    con.executemany('INSERT INTO movements(component_id, type_id, quantity, date, note, created_at) VALUES (?, ?, ?, ?, ?, ?)',
                    [(*movement, created) for movement in INITIAL_MOVEMENTS])
    discarded = {'uno': 1}
    for component_id, total in con.execute('SELECT component_id, total FROM component_stock'):
        assert total == old_totals[component_id] - discarded.get(component_id, 0), component_id

    con.executemany('INSERT INTO spec_fields VALUES (?, ?, ?, ?, ?, ?)',
                    [(*field, i) for i, field in enumerate(SPEC_FIELDS, 1)])
    con.executemany('INSERT INTO column_groups VALUES (?, ?, ?, ?)',
                    [(*group, i) for i, group in enumerate(COLUMN_GROUPS, 1)])
    con.executemany('INSERT INTO table_columns VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    [(*column, i) for i, column in enumerate(TABLE_COLUMNS, 1)])
    con.executemany('INSERT INTO processing_classes VALUES (?, ?)', PROCESSING_CLASSES)

    category_of = {}
    for position, (cid, name, icon, description, terms, tips) in enumerate(GLOSSARY_CATEGORIES, 1):
        con.execute('INSERT INTO glossary_categories VALUES (?, ?, ?, ?, ?, ?)',
                    (cid, name, icon, description, json.dumps(tips, ensure_ascii=False), position))
        category_of.update({term: (cid, i) for i, term in enumerate(terms, 1)})
    for row in con.execute('SELECT * FROM glossary').fetchall():
        cid, position = category_of[row['term']]
        con.execute('INSERT INTO glossary_v2 VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (row['term'], cid, position, row['meaning'], row['short'], row['detail'], row['example']))
    con.execute('DROP TABLE glossary')
    con.execute('ALTER TABLE glossary_v2 RENAME TO glossary')

    guides = [('pic12', i, label, term) for i, (label, term) in enumerate(PIC12_PINS, 1)]
    for guide, term in PROGRAMMING_TERM.items():
        pins = GENERIC_PINS + [('Gravação / depuração', term)]
        guides += [(guide, i, label, t) for i, (label, t) in enumerate(pins, 1)]
    con.executemany('INSERT INTO pin_guides VALUES (?, ?, ?, ?)', guides)


# ---------------------------------------------------------------- versão 3
# Arduino Uno: folha simples com todos os pinos (scripts/make_arduino_pinouts.py) antes da folha oficial.

UNO_PINOUTS = [
    {'file': 'uno-pinout-simple.png', 'title': 'Simples · todos os pinos com porta, número no chip e funções', 'notice': ''},
    {'file': 'uno-pinout.png', 'title': 'Folha oficial Arduino UNO R3 (A000066) · referência', 'notice': ''},
]
UNO_PINOUT_CREDIT = ('Simples: desenho do almoxarifado a partir do datasheet ATmega328P (Figura 1-1, tabela 28.1) e da folha '
                     'oficial Arduino A000066 · oficial: Arduino, CC BY-SA 4.0')


def migrate_to_3(con: sqlite3.Connection) -> None:
    specs = json.loads(con.execute("SELECT specs FROM components WHERE id = 'uno'").fetchone()[0])
    specs.update(pinout=UNO_PINOUTS[0]['file'], pinouts=UNO_PINOUTS, pinout_credit=UNO_PINOUT_CREDIT)
    con.execute("UPDATE components SET specs = ? WHERE id = 'uno'", (json.dumps(specs, ensure_ascii=False, sort_keys=True),))


# ---------------------------------------------------------------- versão 4
# Arduino Nano: mesma solução do Uno (folha simples gerada + folha oficial como referência).

NANO_PINOUTS = [
    {'file': 'nano-pinout-simple.png', 'title': 'Simples · todos os pinos com porta, número no chip e funções', 'notice': ''},
    {'file': 'nano-pinout.png', 'title': 'Folha oficial Arduino Nano (A000005) · referência', 'notice': ''},
]
NANO_PINOUT_CREDIT = ('Simples: desenho do almoxarifado a partir do datasheet ATmega328P (Figura 1-1, tabela 28.1) e da folha '
                      'oficial Arduino A000005 · oficial: Arduino, CC BY-SA 4.0')


def migrate_to_4(con: sqlite3.Connection) -> None:
    specs = json.loads(con.execute("SELECT specs FROM components WHERE id = 'nano'").fetchone()[0])
    specs.update(pinout=NANO_PINOUTS[0]['file'], pinouts=NANO_PINOUTS, pinout_credit=NANO_PINOUT_CREDIT)
    con.execute("UPDATE components SET specs = ? WHERE id = 'nano'", (json.dumps(specs, ensure_ascii=False, sort_keys=True),))


# ---------------------------------------------------------------- versão 5
# WeAct MiniSTM32H743 (STM32H743VIT6), adquirida pelo usuário; fotos da placa enviadas em 17/09/2026.
# Pinagens geradas por scripts/make_h743_pinouts.py (docs/H743-PINOUT.md).

H743_PINOUTS = [
    {'file': 'h743-pinout-simple.png', 'title': 'Visão geral · simples (placa inteira) · clique para ampliar', 'notice': ''},
    {'file': 'h743-pinout-full.png', 'title': 'Visão geral · completa (placa inteira) · clique para ampliar', 'notice': ''},
    {'file': 'h743-pinout-simple-left.png', 'title': 'Simples · header esquerdo (P2)', 'notice': ''},
    {'file': 'h743-pinout-simple-right.png', 'title': 'Simples · header direito (P1)', 'notice': ''},
    {'file': 'h743-pinout-full-left.png', 'title': 'Completa · header esquerdo (P2) · todas as funções', 'notice': ''},
    {'file': 'h743-pinout-full-right.png', 'title': 'Completa · header direito (P1) · todas as funções', 'notice': ''},
    {'file': 'h743-pinout-full-extra.png', 'title': 'Completa · pinos fora dos headers e notas', 'notice': ''},
]

H743_SPECS = {
    'accelerators': 'FPU dupla precisão · DSP · cache L1 · Chrom-ART · JPEG',
    'adc': '3 ADCs · 16 bits · até 3,6 MSPS',
    'clock': 480,
    'coremark': 2424,
    'coremark_note': 'Valor publicado pela ST para o STM32H743 a 480 MHz (página da série STM32H7); não consta no DS12110 local.',
    'coremark_per_mhz': 5.05,
    'cpu': 'Cortex-M7 · 32 bits · FPU dupla precisão · DSP · cache L1 16 + 16 KiB',
    'dac': '2 canais · 12 bits (PA4 e PA5)',
    'datasheet': 'stm32h743vi.pdf',
    'dmips': 1027,
    'dmips_per_mhz': 2.14,
    'eeprom': 'Sem EEPROM',
    'external': '8 MB Flash QSPI + 8 MB Flash SPI na placa (WeAct) · microSD',
    'flash': '2 MiB (2 bancos de 1 MiB)',
    'flash_short': '2 MiB',
    'gpio': '82 no chip (LQFP100); 76 nos headers, vários já ligados a LCD, câmera, microSD e flashes',
    'logic': '3,3 V',
    'notes': ('RAM: 1.056 KiB = 864 KiB de SRAM (AXI 512 + SRAM1–3 288 + SRAM4 64) + 192 KiB de TCM (64 ITCM + 128 DTCM), '
              'mais 4 KiB de backup; nem todo banco é acessível por todo DMA. A placa ocupa pinos dos headers: TFT em PE10–PE14, '
              'câmera DCMI, microSD em PC8–PC12/PD2 e flashes em PB2–PB4/PB6/PD6/PD7/PD11–PD13/PE2. '
              'PC2_C/PC3_C são pads analógicos. Ethernet e USB HS precisam de PHY externo.'),
    'origin': 'Fotos da placa enviadas pelo usuário em 17/09/2026 (chip STM32H743VIT6, serigrafia WeAct Studio); documentação oficial WeActStudio/MiniSTM32H7xx',
    'oscillator': 'Cristal 25 MHz (HSE) + 32,768 kHz (LSE); núcleo até 480 MHz via PLL',
    'package': 'STM32H743VIT6 · LQFP-100',
    'pin_guide': 'stm32',
    'pinout': H743_PINOUTS[0]['file'],
    'pinout_credit': ('Desenhos do almoxarifado gerados por scripts/make_h743_pinouts.py a partir do ST DS12110 Rev 7 '
                      '(tabelas 9–14), do esquema e do desenho mecânico WeAct STM32H7xx V1.2 · pino do CI = número do LQFP100'),
    'pinout_source': 'h743-pinout.pdf',
    'pinouts': H743_PINOUTS,
    'processing_class': 'Alto desempenho',
    'programmer': 'ST-Link V2 · SWD (conector de 4 furos); USB DFU segurando B0; UART PA9/PA10 pelo bootloader',
    'pwm': 'HRTIM + timers avançados e gerais',
    'ram': 1081344,
    'relative_bluepill': 11.41,
    'schematic': 'h743-schematic.pdf',
    'serial': 'USART/UART · LPUART · SPI/I2S · I2C · USB FS · FDCAN · SDMMC · Ethernet (com PHY)',
    'special': 'Câmera DCMI · LCD-TFT · JPEG · Chrom-ART · 2 comparadores · 2 OPAMP · DFSDM',
    'subtitle': 'STM32H743VIT6',
    'temperature': '−40 a +85 °C (sufixo 6)',
    'timers': 'HRTIM + 2 avançados + 10 gerais (2 de 32 bits) + 2 básicos + 5 low-power + 2 watchdogs + SysTick',
    'use': 'Câmera e display, processamento de imagem e áudio, DSP em ponto flutuante e registro em microSD.',
    'variant': 'WeAct MiniSTM32H7xx · H743VIT6 · TFT 0,96″ · 8 MB QSPI + 8 MB SPI',
    'voltage': '3,3 V',
}

NEW_TERMS = [
    # termo, categoria, significado, resumo, funcionamento, exemplo
    ('TCM', 'memoria', 'Tightly-Coupled Memory · memória acoplada ao núcleo',
     'RAM ligada diretamente ao Cortex-M7, sem cache e com tempo de acesso fixo.',
     'ITCM guarda código e DTCM guarda dados críticos; o acesso não passa pelo barramento AXI. Confira quais controladores DMA alcançam cada banco antes de colocar buffers nela.',
     'H743: 64 KiB de ITCM e 128 KiB de DTCM somados aos 864 KiB de SRAM.'),
    ('Quad-SPI', 'memoria', 'Quad Serial Peripheral Interface · SPI de quatro linhas de dados',
     'Interface para memória Flash externa com quatro vias de dados.',
     'Transfere 4 bits por clock e, em modo mapeado, deixa a CPU ler a Flash externa como se fosse memória interna. Pinos, modo e comandos precisam corresponder ao chip de memória.',
     'H743 WeAct: Flash QSPI de 8 MB em PB2, PB6, PD11–PD13 e PE2.'),
    ('SDMMC', 'comunicacao', 'Secure Digital / MultiMediaCard interface',
     'Controlador de cartão SD em barramento de 1 ou 4 bits.',
     'Usa CLK, CMD e D0–D3; costuma ser acompanhado de biblioteca de sistema de arquivos (FAT). Pull-ups e comprimento das trilhas afetam a velocidade máxima.',
     'H743 WeAct: microSD no SDMMC1 (PC8–PC12 e PD2), detecção em PD4.'),
    ('DCMI', 'comunicacao', 'Digital Camera Interface · interface de câmera digital',
     'Recebe imagem de sensores com barramento paralelo (DVP).',
     'Captura 8 a 14 bits por pulso de PIXCLK, sincronizados por HSYNC e VSYNC, normalmente com DMA para a RAM. O sensor é configurado à parte por I2C (SCCB).',
     'H743 WeAct: conector de câmera de 24 vias para OV2640, OV7725 ou OV5640.'),
]


def migrate_to_5(con: sqlite3.Connection) -> None:
    position = con.execute('SELECT MAX(position) FROM components').fetchone()[0] + 1
    con.execute('INSERT INTO components VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                ('h743', 'microcontroladores', 'WeAct H743', 'STM32', 'placa', 0, position,
                 json.dumps(H743_SPECS, ensure_ascii=False, sort_keys=True)))
    con.execute('INSERT INTO movements(component_id, type_id, quantity, date, note, created_at) VALUES (?, ?, ?, ?, ?, ?)',
                ('h743', 'compra', 1, '2026-09-17', 'Recém-adquirida; fotos da placa enviadas pelo usuário. Data exata da compra não registrada.',
                 '2026-09-17T12:00:00+00:00'))
    for term, category, meaning, short, detail, example in NEW_TERMS:
        after = con.execute('SELECT COALESCE(MAX(position), 0) + 1 FROM glossary WHERE category_id = ?', (category,)).fetchone()[0]
        con.execute('INSERT INTO glossary VALUES (?, ?, ?, ?, ?, ?, ?)', (term, category, after, meaning, short, detail, example))
    con.execute("""UPDATE tools SET compatibility = ? WHERE id = 'stlink'""",
                ('BluePill F103, BlackPill F411 e H743 via SWD. G474 requer software atualizado; conferir suporte H7RS para H7R3 '
                 'e variante/firmware do gravador.',))


# ---------------------------------------------------------------- versão 6
# Glossário com sinônimos reconhecidos no texto (aliases), figura opcional e explicação em parágrafos.
# QSPI ganha documentação completa e diagrama; SPI ganha diagrama (assets/glossary/*.svg).

QSPI_DETAIL = (
    'Ligação: CLK e NCS (seleção, ativa em nível baixo) mais IO0–IO3. As quatro linhas são bidirecionais: IO0 e IO1 fazem o papel '
    'de MOSI e MISO quando a memória fala SPI comum, e IO2/IO3 são os antigos /WP e /HOLD da Flash. Por isso a mesma Flash '
    'funciona em SPI (1 linha), Dual (2) ou Quad (4); o modo quad normalmente precisa ser liberado pelo bit QE do registrador de '
    'status da memória.\n\n'
    'Cada acesso tem fases: instrução (8 bits, muitas vezes numa linha só), endereço (24 bits até 16 MB; 32 bits acima), bytes de '
    'modo, ciclos dummy (tempo para a memória buscar o dado) e dados. No comando EBh, notação 1-4-4, a instrução usa 1 linha e '
    'endereço e dados usam 4: cada byte passa em 2 clocks, contra 8 no SPI comum. Comando, largura de cada fase e número de dummy '
    'precisam bater com o datasheet da Flash; um valor errado desloca todos os bits lidos.\n\n'
    'O periférico QUADSPI do STM32H743 tem três modos: indireto (o programa envia comandos e lê ou grava por registrador ou DMA), '
    'polling de status (espera a Flash terminar uma gravação sem ocupar a CPU) e mapeado em memória (a Flash aparece a partir de '
    '0x9000 0000 e pode ser lida, e até executada, como memória comum, passando pelo cache). Gravar e apagar exige o modo indireto: '
    'apague setores de 4 KiB antes e grave em páginas de até 256 bytes.\n\n'
    'Velocidade: a QUADSPI do H743 chega a 133 MHz (DS12110), mas o limite real depende da Flash, do comando e das trilhas; comece '
    'com o divisor de clock alto e suba. Diferente do SPI, não é um barramento para vários periféricos: cada banco atende uma '
    'memória (os dois bancos juntos formam o modo Dual-Flash de 8 bits).'
)


def migrate_to_6(con: sqlite3.Connection) -> None:
    con.execute("ALTER TABLE glossary ADD COLUMN aliases TEXT NOT NULL DEFAULT '[]' CHECK(json_valid(aliases))")
    con.execute('ALTER TABLE glossary ADD COLUMN figure TEXT')
    con.execute('ALTER TABLE glossary ADD COLUMN figure_caption TEXT')
    con.execute(
        """UPDATE glossary SET term = 'QSPI', meaning = ?, short = ?, detail = ?, example = ?, aliases = ?, figure = ?, figure_caption = ?
           WHERE term = 'Quad-SPI'""",
        ('Quad Serial Peripheral Interface · SPI de quatro linhas de dados (Quad-SPI, QUADSPI)',
         'Versão do SPI que usa quatro linhas de dados ao mesmo tempo para ler e gravar memória Flash externa até 4× mais rápido. '
         'No STM32 ela também deixa o programa ler, e até executar código, direto da Flash externa.',
         QSPI_DETAIL,
         'H743 WeAct: Flash PY25Q64HA de 8 MB no QUADSPI banco 1 — CLK PB2, NCS PB6, IO0 PD11, IO1 PD12, IO2 PE2 e IO3 PD13 '
         '(esses pinos também saem nos headers). Mapeada em 0x9000 0000, guarda imagens e fontes do display ou código. '
         'A H7R3 usa o XSPI no mesmo papel.',
         json.dumps(['Quad-SPI', 'QUADSPI', 'Quad SPI']),
         'assets/glossary/qspi.svg',
         'Em cima, a diferença de ligação entre SPI e QSPI, com os pinos da Flash QSPI da H743. Embaixo, uma leitura EBh clock a '
         'clock: instrução em uma linha, endereço, modo, dummy e dados em quatro linhas.'))
    con.execute(
        "UPDATE glossary SET figure = ?, figure_caption = ? WHERE term = 'SPI'",
        ('assets/glossary/spi.svg',
         'Barramento com um controlador e dois periféricos (SCK, MOSI e MISO compartilhados, um CS para cada), usando os pinos da '
         'Flash SPI da H743; embaixo, um byte trocado no modo 0 e a tabela dos quatro modos CPOL/CPHA.'))


# ---------------------------------------------------------------- versões 7+
# Documentação completa, termo a termo, no modelo de QSPI: explicação em parágrafos, exemplo no acervo e figura SVG.

def document_term(con: sqlite3.Connection, term: str, *, meaning: str, short: str, detail: str, example: str,
                  figure: str, caption: str, aliases: tuple = (), category: str | None = None, after: str | None = None) -> None:
    """Atualiza um termo do glossário ou, se ele não existir, cria na categoria indicada: logo depois de `after`
    (os seguintes andam uma posição, para os "termos relacionados" continuarem vizinhos) ou no fim."""
    values = (meaning, short, detail, example, json.dumps(list(aliases), ensure_ascii=False), figure, caption)
    if con.execute('SELECT 1 FROM glossary WHERE term = ?', (term,)).fetchone():
        con.execute('UPDATE glossary SET meaning = ?, short = ?, detail = ?, example = ?, aliases = ?, figure = ?, figure_caption = ? '
                    'WHERE term = ?', (*values, term))
    else:
        if after:
            position = con.execute('SELECT position + 1 FROM glossary WHERE term = ? AND category_id = ?', (after, category)).fetchone()[0]
            con.execute('UPDATE glossary SET position = position + 1 WHERE category_id = ? AND position >= ?', (category, position))
        else:
            position = con.execute('SELECT COALESCE(MAX(position), 0) + 1 FROM glossary WHERE category_id = ?', (category,)).fetchone()[0]
        con.execute('INSERT INTO glossary(term, category_id, position, meaning, short, detail, example, aliases, figure, figure_caption) '
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (term, category, position, *values))


def migrate_to_7(con: sqlite3.Connection) -> None:
    document_term(
        con, 'USART',
        meaning='Universal Synchronous/Asynchronous Receiver/Transmitter · transmissor/receptor universal síncrono e assíncrono',
        short='Periférico serial que faz tudo o que uma UART faz e ainda pode enviar o próprio clock (modo síncrono), controlar o '
              'fluxo com RTS/CTS e acionar transceptores RS-485.',
        detail=(
            'No modo assíncrono o USART é exatamente uma UART: TX e RX com quadro start, dados, paridade e stop, e baud rate combinado '
            'entre os dois lados (veja UART). O "S" de síncrono acrescenta o pino CK: o USART gera um pulso de clock para cada bit e o '
            'outro lado lê os dados nesse ritmo, sem baud rate combinado. Na prática vira um SPI mestre simples (CK = SCK, TX = MOSI, '
            'RX = MISO).\n\n'
            'Sinais extras opcionais: RTS/CTS fazem controle de fluxo por hardware. Quem recebe ativa RTS quando tem espaço e o outro '
            'lado só transmite com o seu CTS ativo, o que evita perder bytes com módulos lentos (Wi-Fi, Bluetooth, modems). DE (Driver '
            'Enable) liga o transmissor de um transceptor RS-485 só durante o envio, permitindo vários dispositivos no mesmo par de '
            'fios; no STM32 o pino RTS vira DE quando o modo RS-485 está ativo.\n\n'
            'O mesmo bloco ainda oferece half-duplex num fio só, LIN (redes automotivas), IrDA (infravermelho), Smartcard ISO 7816, '
            'detecção automática de baud rate, timeout de recepção (útil para Modbus) e modo multiprocessador. No STM32H743 cada USART '
            'tem FIFO de 16 posições na transmissão e na recepção, atende DMA, chega a 12,5 Mbit/s e tem clock independente da CPU: '
            'pode acordar o chip do modo Stop ao receber um start bit.\n\n'
            'O H743 tem quatro USART (1, 2, 3 e 6) e quatro UART (4, 5, 7 e 8). As UART não têm CK nem Smartcard, mas mantêm RTS/CTS, '
            'DE, LIN, IrDA e FIFO. Na HAL da ST, o modo síncrono usa as funções HAL_USART_* e o assíncrono (o mais comum) usa '
            'HAL_UART_*, inclusive nos USART. Cada sinal só existe em certos pinos, e o número da função alternativa muda de pino para '
            'pino: confira na pinagem completa.'),
        example='H743 WeAct: USART3 completo e livre nos headers, com PD8 TX, PD9 RX, PD10 CK, PB13 CTS e PB14 RTS/DE. O USART1 em '
                'PA9/PA10 é o mesmo usado pelo bootloader serial (gravação com o CH343P). A BlackPill F411 tem USART1, 2 e 6.',
        figure='assets/glossary/usart.svg',
        caption='Os quatro modos de ligação do USART3 da H743 (assíncrono, síncrono com CK, controle de fluxo RTS/CTS e RS-485 com '
                'DE), as diferenças entre USART e UART no H743 (DS12110, tabela 6) e os pinos livres na placa.')


def migrate_to_8(con: sqlite3.Connection) -> None:
    document_term(
        con, 'UART',
        meaning='Universal Asynchronous Receiver/Transmitter · transmissor/receptor assíncrono universal',
        short='Comunicação serial por dois fios de dados (TX e RX) sem clock: os dois lados combinam antes a velocidade e o formato, '
              'e cada byte viaja num quadro com bit de início e bit de parada.',
        detail=(
            'Ligação ponto a ponto: o TX de um vai ao RX do outro, e os GND precisam estar ligados. A linha fica em 1 quando está '
            'ociosa; um byte começa com o start bit (0), segue com 5 a 9 bits de dados, do menos significativo para o mais '
            'significativo, um bit de paridade opcional e um ou dois stop bits (1). O formato é escrito como 8N1: 8 bits de dados, '
            'sem paridade, 1 stop bit.\n\n'
            'Não existe clock no fio. O receptor detecta a descida do start bit e, a partir dela, lê cada bit no meio do seu '
            'intervalo usando o próprio clock (o STM32 amostra 16 ou 8 vezes por bit). Por isso o baud rate precisa ser igual nos '
            'dois lados e a soma dos erros de clock deve ficar abaixo de cerca de 2 %: com cristal não há problema; com oscilador RC '
            'interno ou baud rate que não divide bem o clock do periférico surgem caracteres trocados e erros de quadro. A 115 200 '
            'bit/s cada bit dura 8,68 µs e um quadro 8N1 de 10 bits leva 86,8 µs (até 11 520 bytes/s).\n\n'
            'Nível elétrico: a UART do microcontrolador trabalha em nível lógico (3,3 V no STM32, 5 V no Arduino Uno). RS-232 usa '
            'tensões de ±3 a ±15 V, invertidas, e queima o pino se ligado direto; precisa de um conversor como o MAX3232. RS-485 e LIN '
            'também exigem transceptor. Um adaptador USB–UART (CH343P, CH340, FT232) mostra a UART ao computador como porta COM, '
            '/dev/ttyUSB ou /dev/ttyACM.\n\n'
            'Na prática: receba por interrupção ou DMA para não perder bytes, trate o erro de overrun e use controle de fluxo RTS/CTS '
            'quando o outro lado for lento. Para vários dispositivos no mesmo par de fios, use RS-485 com DE (veja USART). O '
            'bootloader de fábrica do STM32 aceita gravação pela UART: no H743, USART1 em PA9/PA10 com BOOT0 em nível alto.'),
        example='H743 WeAct: USART1 em PA9 (TX) e PA10 (RX), ligado ao CH343P do acervo para console e gravação pelo bootloader. '
                'No Arduino Uno e Nano, D0/D1 são a UART do ATmega328P, já usada pela ponte USB. O PIC16F887 usa a EUSART em RC6/RC7.',
        figure='assets/glossary/uart.svg',
        caption='Ligação cruzada do CH343P ao USART1 da H743 (PA9/PA10), a forma de onda do byte 0x41 em 8N1 a 115 200 bit/s com '
                'os pontos de amostragem, a notação 8N1 e os erros mais comuns.')


def migrate_to_9(con: sqlite3.Connection) -> None:
    document_term(
        con, 'LPUART', category='comunicacao', after='EUSART', aliases=('LPUART1',),
        meaning='Low-Power Universal Asynchronous Receiver/Transmitter · UART de baixo consumo',
        short='UART que continua recebendo com o chip em modo Stop, usando o cristal de 32,768 kHz, e acorda a CPU só quando chega '
              'um dado.',
        detail=(
            'É uma UART (TX, RX e, se quiser, RTS/CTS e DE) feita para gastar pouco: ela continua recebendo com o chip em modo Stop e '
            'acorda a CPU quando chega algo. Os quadros são iguais aos de qualquer UART (start, dados, paridade, stop), então do '
            'outro lado pode estar qualquer UART comum.\n\n'
            'O segredo é o clock. O LPUART pode usar o cristal LSE de 32,768 kHz, que continua ligado no Stop. O baud rate vem de um '
            'divisor fracionário, BRR = 256 × f_clock ÷ baud: com o LSE, 9600 bit/s dá BRR ≈ 874 e erro de só 0,02 %. Como o BRR '
            'mínimo é 0x300, o limite é f_clock ÷ 3; na prática, 9600 bit/s com o LSE. Para 115 200 bit/s ou mais, use HSI, CSI ou o '
            'clock do barramento, e o consumo sobe.\n\n'
            'O despertar pode ser programado para o start bit, para qualquer quadro, para um byte específico (endereço) ou para o '
            'estado da FIFO. No STM32H743 o LPUART1 fica no domínio D3, junto com o RCC, a SRAM4 e o BDMA. Esse domínio pode seguir '
            'funcionando com D1 (CPU) e D2 (onde ficam os USART) desligados. O DMA que atende o LPUART1 é o BDMA, que trabalha com a '
            'SRAM4: confira no manual de referência RM0433 antes de montar o buffer.\n\n'
            'Em troca, perde recursos: não tem modo síncrono, LIN, IrDA, Smartcard, detecção automática de baud rate nem timeout de '
            'recepção. Use o LPUART para sensores, GPS, modems ou outro microcontrolador que enviam dados de vez em quando enquanto o '
            'sistema dorme; para console e gravação, um USART comum é mais simples.'),
        example='H743 WeAct: LPUART1 em PA9 (TX) e PA10 (RX), função alternativa AF3 — os mesmos pinos do USART1 (AF7), então só '
                'um dos dois usa o par. O cristal LSE de 32,768 kHz já está montado na placa (PC14/PC15). A G474 também tem LPUART1; '
                'F411 e F103 não têm.',
        figure='assets/glossary/lpuart.svg',
        caption='O que continua ligado no modo Stop (LSE e LPUART1 no domínio D3), o consumo ao longo do tempo com o despertar por '
                'um quadro recebido, o cálculo do baud rate com 32,768 kHz e a comparação com os USART do H743.')


def migrate_to_10(con: sqlite3.Connection) -> None:
    caption = con.execute("SELECT figure_caption FROM glossary WHERE term = 'SPI'").fetchone()[0]
    document_term(
        con, 'SPI',
        meaning='Serial Peripheral Interface · interface periférica serial',
        short='Barramento síncrono de quatro fios (clock, dados de ida, dados de volta e seleção) em que o controlador gera o clock e '
              'fala com um periférico por vez: simples, rápido e full-duplex.',
        detail=(
            'Sinais: SCK é o clock, sempre gerado pelo controlador; MOSI leva dados do controlador ao periférico e MISO traz de volta '
            '(nomes novos: COPI/CIPO, ou SDO/SDI vistos de cada chip); CS, também chamado NSS ou SS, seleciona o periférico e quase '
            'sempre é ativo em nível baixo. A cada pulso de clock sai um bit por MOSI e entra um bit por MISO ao mesmo tempo: o SPI '
            'é full-duplex, e para ler é preciso enviar alguma coisa (bytes "dummy") só para gerar o clock.\n\n'
            'Modo: CPOL diz se o clock parado fica em 0 ou 1, e CPHA diz se o dado é lido na primeira ou na segunda borda; juntos '
            'formam os modos 0 a 3. Os dois lados precisam usar o mesmo modo, a mesma ordem de bits (quase sempre o mais '
            'significativo primeiro) e um clock que o periférico aceite. Não há endereço nem confirmação de recebimento: com o modo '
            'errado, os bytes chegam deslocados ou todos iguais (0x00 ou 0xFF), sem nenhum aviso de erro.\n\n'
            'Vários periféricos compartilham SCK, MOSI e MISO, e cada um tem o seu CS; só o selecionado aciona MISO, os outros deixam '
            'a linha em alta impedância. CS por software (um GPIO comum) é o jeito mais flexível; o NSS por hardware do STM32 atende '
            'bem um único periférico. Para mais velocidade existem variantes com mais linhas de dados, Dual e Quad SPI (veja QSPI), '
            'usadas por memórias Flash.\n\n'
            'O STM32H743 tem seis SPI (SPI1 a SPI6), até 150 Mbit/s, quadros de 4 a 16 bits, FIFO, CRC por hardware e DMA; SPI1, '
            'SPI2 e SPI3 também fazem I2S (áudio), e o SPI6 fica no domínio D3, de baixo consumo. Com fios de protoboard, 1 a 10 MHz '
            'já é bastante; acima disso, fios curtos e um GND ao lado de cada sinal fazem diferença.'),
        example='H743 WeAct: SPI2 livre nos headers em PB13 (SCK), PB14 (MISO), PB15 (MOSI) e PB12 (NSS) — os mesmos pinos que o '
                'TCC usa na BlackPill para o ADS1256. Na própria placa, a flash SPI de 8 MB está no SPI1 (PB3, PB4, PD7, CS em PD6) e '
                'o display no SPI4 (PE12 e PE14).',
        figure='assets/glossary/spi.svg', caption=caption)


MIGRATIONS = {2: migrate_to_2, 3: migrate_to_3, 4: migrate_to_4, 5: migrate_to_5, 6: migrate_to_6, 7: migrate_to_7, 8: migrate_to_8,
              9: migrate_to_9, 10: migrate_to_10}


def migrate(path: Path = db.DATABASE) -> int:
    con = db.connect(path)
    con.isolation_level = None  # transações explícitas abaixo
    con.execute('PRAGMA foreign_keys = OFF')  # tabelas são recriadas durante a migração
    version = con.execute('PRAGMA user_version').fetchone()[0]
    migrated = False
    for target in sorted(v for v in MIGRATIONS if v > version):
        con.execute('BEGIN')
        try:
            MIGRATIONS[target](con)
            problems = con.execute('PRAGMA foreign_key_check').fetchall()
            if problems:
                raise RuntimeError(f'Chaves estrangeiras inválidas: {[tuple(p) for p in problems]}')
            con.execute(f'PRAGMA user_version = {target}')
            con.execute('COMMIT')
        except BaseException:
            con.execute('ROLLBACK')
            raise
        print(f'Banco migrado para a versão {target}.')
        version = target
        migrated = True
    if migrated:
        con.execute('VACUUM')  # só depois de migrar, para não alterar o binário à toa
    con.close()
    return version


if __name__ == '__main__':
    print(f'Versão atual: {migrate()}. Execute python3 scripts/export.py para atualizar os snapshots.')

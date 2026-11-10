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


def migrate_to_11(con: sqlite3.Connection) -> None:
    document_term(
        con, 'I2S', category='comunicacao', after='SPI', aliases=('I²S', 'IIS'),
        meaning='Inter-IC Sound · barramento de áudio digital entre chips',
        short='Interface serial síncrona feita para transportar áudio digital estéreo, em fluxo contínuo, entre microcontrolador, '
              'DACs, amplificadores, microfones e codecs.',
        detail=(
            'Três sinais formam o barramento: CK (ou BCLK) marca cada bit; WS (ou LRCLK) diz de qual canal é a amostra, 0 para o '
            'esquerdo e 1 para o direito, e troca uma vez por amostra, então sua frequência é a própria taxa de amostragem (Fs); SD '
            'leva os dados, uma linha por sentido. Um quarto sinal, opcional, é o MCK (master clock), normalmente 256 × Fs, que '
            'alimenta o conversor de alguns codecs e DACs.\n\n'
            'Não há endereço nem pacote: é um fluxo contínuo, amostra após amostra. No padrão Philips o bit mais significativo sai um '
            'clock depois da troca de WS; também existem os formatos justificado à esquerda (MSB junto com a troca de WS), '
            'justificado à direita e PCM/TDM. Os dois lados precisam combinar o formato, o tamanho da palavra (16, 24 ou 32 bits) e '
            'quem é o mestre que gera CK e WS.\n\n'
            'As contas definem os clocks: BCLK = Fs × bits por canal × 2 canais. A 48 kHz com 16 bits, BCLK = 1,536 MHz; com quadros '
            'de 32 bits, 3,072 MHz; MCK = 256 × 48 kHz = 12,288 MHz. Como o áudio exige frequência exata, o clock do I2S vem de um PLL '
            'dedicado (no H743, PLL2 ou PLL3, que têm ajuste fracionário); erro de clock vira deriva, estalos ou som desafinado. DMA '
            'em modo circular com buffer duplo é o jeito normal de manter o som contínuo.\n\n'
            'No STM32H743, SPI1, SPI2 e SPI3 também funcionam como I2S: mestre ou escravo, simplex, 16 ou 32 bits, de 8 a 192 kHz, '
            'com FIFO e DMA. Para mais canais existem os quatro SAI (Serial Audio Interface), com dois blocos cada, TDM, entrada PDM '
            'para microfones digitais e saída S/PDIF. Não confunda com I2C: o nome é parecido, mas I2C é um barramento de controle '
            'com endereços. Codecs costumam usar I2C para configurar e I2S para o som.'),
        example='H743 WeAct: I2S2 livre nos headers em PB13 (CK), PB12 (WS), PB15 (SDO, saída) e PB14 (SDI, entrada) — basta para um '
                'amplificador MAX98357A ou um microfone INMP441, que não usam MCK (o MCK do I2S2 fica em PC6, ocupado pela câmera). '
                'A BlackPill F411 também tem I2S; Arduino Uno e Nano não têm.',
        figure='assets/glossary/i2s.svg',
        caption='O I2S2 da H743 ligado a um amplificador MAX98357A e a um microfone INMP441, um quadro estéreo Philips de 16 bits por '
                'canal, as contas de BCLK e MCK a 48 kHz e a comparação entre I2S e SAI no H743.')


def migrate_to_12(con: sqlite3.Connection) -> None:
    document_term(
        con, 'I2C', aliases=('I²C', 'IIC', 'TWI'),
        meaning='Inter-Integrated Circuit · barramento entre circuitos',
        short='Barramento de dois fios (SDA para dados, SCL para clock) em que vários sensores e displays dividem as mesmas linhas, '
              'cada um com o seu endereço: lento, mas econômico em pinos.',
        detail=(
            'As duas linhas são de dreno aberto: nenhum chip força o nível 1, todos só puxam para 0, e resistores de pull-up levam a '
            'linha de volta a 1. Assim vários dispositivos dividem o fio sem curto-circuito, o receptor responde (ACK) na mesma linha '
            'e um periférico lento pode segurar SCL em 0 para pedir tempo (clock stretching). Sem pull-up nada funciona; muitos '
            'módulos já trazem os seus, e vários em paralelo baixam a resistência total.\n\n'
            'Toda conversa começa com START (SDA desce com SCL em 1) e termina com STOP (SDA sobe com SCL em 1). Depois do START vem '
            'o endereço de 7 bits e um bit de direção (0 = escrever, 1 = ler); o dispositivo com aquele endereço responde ACK puxando '
            'SDA para 0 no nono clock. Para ler um registrador, o controlador escreve o número do registrador, faz um repeated START '
            'e lê os bytes, respondendo NACK no último. Sem ACK no endereço, quase sempre o endereço está errado, os fios estão '
            'trocados ou falta pull-up.\n\n'
            'Velocidades: Standard 100 kbit/s, Fast 400 kbit/s e Fast-mode Plus 1 Mbit/s. O limite real é o tempo de subida: a '
            'capacitância do barramento (fios e chips, no máximo 400 pF) contra a resistência de pull-up. Resistor alto demais deixa '
            'a borda lenta; baixo demais passa da corrente que o pino consegue drenar. Fios longos pedem velocidade menor ou um '
            'extensor I2C. Dois dispositivos com o mesmo endereço exigem um multiplexador (TCA9548A) ou um pino de endereço '
            'diferente.\n\n'
            'O STM32H743 tem quatro I2C (I2C1 a I2C4), compatíveis com a especificação rev. 5: mestre, escravo e multimestre, '
            'endereços de 7 e 10 bits, filtros de ruído analógico e digital, SMBus/PMBus, DMA e clock independente, o que permite '
            'acordar do Stop ao reconhecer o próprio endereço. Fast-mode Plus exige os pinos marcados FT_f, com saída de 20 mA. O I2C4 '
            'fica no domínio D3.'),
        example='H743 WeAct: I2C2 livre em PB10 (SCL) e PB11 (SDA), ambos FT_f. O I2C1 em PB8/PB9 é o barramento de configuração da '
                'câmera (SCCB) e já tem pull-ups de 4,7 kΩ na placa: outros sensores podem entrar nele se o endereço não coincidir '
                '(a OV5640 usa 0x3C, o mesmo de muitos OLED SSD1306). No robô equilibrista, o Nano lê o MPU6050 (0x68) por I2C em '
                'A4/A5.',
        figure='assets/glossary/i2c.svg',
        caption='Barramento I2C da H743 (I2C2 em PB10/PB11) com pull-ups e três sensores, a leitura do registrador WHO_AM_I do '
                'MPU6050 passo a passo, a forma de onda de START, bit, ACK e STOP e a relação entre velocidade e resistor.')


def migrate_to_13(con: sqlite3.Connection) -> None:
    document_term(
        con, 'USB', aliases=('USB OTG',),
        meaning='Universal Serial Bus · barramento serial universal',
        short='Interface em que um host (o computador) controla tudo e os dispositivos respondem; transporta dados e energia, e o '
              'mesmo conector serve para gravar, depurar e conversar com o PC.',
        detail=(
            'Os dados trafegam num par diferencial, D+ e D−: o que conta é a diferença entre as duas linhas, o que torna o sinal '
            'resistente a ruído. VBUS leva 5 V do host para o dispositivo e GND fecha o circuito. Em full-speed o dispositivo se '
            'anuncia ligando um resistor de 1,5 kΩ entre D+ e 3,3 V (o STM32 tem esse pull-up interno). No conector USB-C, os pinos '
            'CC com 5,1 kΩ para GND dizem à fonte "sou dispositivo, pode mandar 5 V"; sem eles, carregadores USB-C não ligam o '
            'VBUS.\n\n'
            'O host manda em tudo: ao conectar, ele reseta o barramento, lê os descritores (VID, PID, classe, endpoints), dá um '
            'endereço e carrega o driver da classe. Depois consulta cada endpoint periodicamente (quadros de 1 ms em full-speed); o '
            'dispositivo nunca fala sem ser perguntado. Classes padronizadas dispensam driver próprio: CDC aparece como porta serial, '
            'HID como teclado ou mouse, MSC como pendrive, DFU como gravador, Audio e UVC para som e vídeo.\n\n'
            'Velocidades do USB 2.0: low-speed 1,5 Mbit/s, full-speed 12 Mbit/s e high-speed 480 Mbit/s. O controlador precisa de uma '
            'PHY, o circuito que fala eletricamente no par, e de um clock preciso de 48 MHz, vindo do cristal por PLL ou de um '
            'oscilador interno corrigido pelo próprio USB. OTG (On-The-Go) quer dizer que o mesmo periférico pode ser host ou '
            'dispositivo; como host, a placa precisa fornecer 5 V ao VBUS com corrente e proteção suficientes.\n\n'
            'O STM32H743 tem dois controladores USB 2.0 OTG: o OTG_HS (OTG-HS1), que chega a 480 Mbit/s só com uma PHY ULPI externa, '
            'e o OTG_FS (OTG-HS2), só full-speed. Os dois têm PHY full-speed interna, FIFO de 4 KiB, 9 endpoints e DMA, e podem usar '
            'o HSI48 corrigido pelo CRS em vez de cristal. O bootloader de fábrica aceita gravação por DFU. Sem ponte USB–UART, o '
            'próprio firmware implementa a classe, por exemplo CDC com a biblioteca USB Device da ST ou com o TinyUSB.'),
        example='H743 WeAct: USB-C no OTG_FS (PA11 D−, PA12 D+), com 5,1 kΩ nos CC e VBUS pelo diodo B5819; segurando B0 ao ligar, '
                'aparece como DFU para gravação. Um segundo USB full-speed pode sair do OTG_HS em PB14/PB15. Uno e Nano usam uma '
                'ponte (ATmega16U2, CH340 ou FT232) porque o ATmega328P não tem USB; BluePill e BlackPill têm USB nativo.',
        figure='assets/glossary/usb.svg',
        caption='O circuito do USB-C da H743 (D+ e D− em PA12/PA11, CC com 5,1 kΩ, VBUS pelo diodo B5819 e a ponte SB6 para modo '
                'host), as cinco etapas da enumeração, as velocidades do USB 2.0 e as classes de dispositivo mais comuns.')


def migrate_to_14(con: sqlite3.Connection) -> None:
    document_term(
        con, 'FDCAN', aliases=('CAN FD',),
        meaning='Flexible Data-rate CAN · CAN com taxa de dados flexível',
        short='Controlador da rede CAN, o barramento robusto de carros e máquinas, compatível com o CAN clássico e com o CAN FD, que '
              'manda até 64 bytes por mensagem com a parte de dados em velocidade maior.',
        detail=(
            'O CAN liga vários nós num único par trançado, CANH e CANL, terminado com 120 Ω em cada ponta. O microcontrolador fala com '
            'o barramento por um transceptor, porque o FDCAN só tem TX e RX em nível lógico. Não há mestre nem endereço de destino: '
            'cada mensagem tem um identificador (11 bits no formato padrão, 29 no estendido), e cada nó decide pelos filtros se ela '
            'lhe interessa.\n\n'
            'O sinal é diferencial. Com os dois fios na mesma tensão, o barramento está recessivo (bit 1); quando um transceptor '
            'puxa CANH para cima e CANL para baixo, ele fica dominante (bit 0), e um único nó dominante vence todos os recessivos. É '
            'assim que funciona a arbitragem sem colisão destrutiva: se dois nós começam juntos, cada um lê o barramento enquanto '
            'envia o ID; quem manda 1 e lê 0 perde e tenta depois, então o menor ID tem prioridade. O receptor confirma com ACK, e '
            'CRC, bit stuffing e contadores de erro tiram da rede, sozinhos, um nó defeituoso (bus-off).\n\n'
            'O CAN clássico (2.0A/B) vai até 1 Mbit/s e 8 bytes de dados. O CAN FD mantém a arbitragem na taxa nominal e, depois do '
            'bit BRS, troca para uma taxa maior só na fase de dados (tipicamente 2 a 5 Mbit/s, até 8 Mbit/s com bons transceptores), '
            'com até 64 bytes por mensagem e CRC mais forte. Nós clássicos e FD só dividem o barramento se ninguém enviar quadros FD. '
            'Os tempos de bit (prescaler, segmentos e ponto de amostragem, perto de 87,5 %) precisam ser iguais em todos os nós.\n\n'
            'O STM32H743 tem dois FDCAN (FDCAN1 e FDCAN2), compatíveis com ISO 11898-1 e CAN FD 1.0, que dividem 10 KiB de RAM de '
            'mensagens para filtros, FIFOs e buffers, e uma unidade opcional de calibração de clock. O FDCAN1 também faz TT-CAN (ISO '
            '11898-4), a comunicação disparada por tempo. Use o cristal como base do clock do CAN. Transceptores de 3,3 V '
            '(SN65HVD230, TJA1051T/3) ligam direto; os de 5 V, como o MCP2551, precisam de adaptação de nível no RX.'),
        example='H743 WeAct: FDCAN1 em PD0 (RX) e PD1 (TX) e FDCAN2 em PB12 (RX) e PB13 (TX), livres nos headers; falta só o '
                'transceptor. A G474 também tem FDCAN; a BluePill F103 tem CAN 2.0B clássico, que divide memória e pinos com o USB; a '
                'BlackPill F411 não tem CAN.',
        figure='assets/glossary/fdcan.svg',
        caption='Rede CAN com a H743 (FDCAN1 em PD0/PD1), transceptor SN65HVD230 e terminação de 120 Ω, os níveis recessivo e '
                'dominante, a arbitragem por ID entre dois nós e a comparação entre os quadros CAN 2.0 e CAN FD.')


def migrate_to_15(con: sqlite3.Connection) -> None:
    document_term(
        con, 'SDMMC', aliases=('SDIO', 'microSD'),
        meaning='Secure Digital / MultiMediaCard interface · controlador de cartão SD e eMMC',
        short='Periférico que conversa com cartões SD, microSD e memórias eMMC pelo protocolo nativo, com 4 linhas de dados em '
              'paralelo e DMA próprio: bem mais rápido que ler o cartão por SPI.',
        detail=(
            'Sinais: CLK, sempre gerado pelo microcontrolador; CMD, linha bidirecional por onde vão os comandos e voltam as respostas; '
            'e D0–D3, os dados, usados em paralelo no modo de 4 bits (no modo de 1 bit, só D0). O cartão funciona entre 2,7 e 3,6 V, '
            'e as linhas CMD e D0–D3 precisam de pull-up (tipicamente 10 a 100 kΩ). Resistores de 22 a 33 Ω em série ajudam a evitar '
            'reflexões com clock alto, e uma chave no soquete pode indicar se há cartão.\n\n'
            'Todo acesso começa com um comando de 48 bits em CMD: bit de início, número do comando (CMD17 lê um bloco, CMD24 grava), '
            'argumento de 32 bits com o endereço, CRC7 e bit de fim. O cartão responde também em CMD e, em seguida, os dados passam '
            'por D0–D3 em blocos de 512 bytes, cada linha com o seu CRC16. Na gravação, o cartão segura D0 em 0 enquanto está '
            'ocupado. Ler ou gravar vários blocos seguidos (CMD18/CMD25) é muito mais rápido que blocos soltos.\n\n'
            'Na inicialização, o controlador usa clock de até 400 kHz e uma linha: identifica o cartão, lê a capacidade, dá um '
            'endereço relativo e só então passa para 4 bits e 25 MHz (Default Speed, até 12,5 MB/s) ou 50 MHz (High Speed, até '
            '25 MB/s). Os modos UHS-I (SDR50, SDR104) exigem sinais de 1,8 V e um circuito que troque a tensão. Cartões SDSC (até '
            '2 GB) endereçam em bytes; SDHC (até 32 GB) e SDXC (até 2 TB) endereçam em blocos e vêm formatados em FAT32 ou exFAT. O '
            'sistema de arquivos fica por conta de uma biblioteca como a FatFs.\n\n'
            'O STM32H743 tem dois SDMMC, compatíveis com SD 4.1, SDIO 4.0 e eMMC 4.51 (até 8 bits), com clock de até 125 MHz e DMA '
            'interno (IDMA). Cada um atende um cartão por vez. O IDMA do SDMMC1 não alcança a DTCM: deixe os buffers na AXI SRAM e, '
            'com a cache ligada, limpe ou invalide a cache antes e depois das transferências (confira no manual RM0433). O modo '
            'SDIO também serve para módulos Wi-Fi que usam essa interface.'),
        example='H743 WeAct: microSD no SDMMC1 em 4 bits — PC8 a PC11 (D0–D3), PC12 (CLK) e PD2 (CMD) — com 22 Ω em série, '
                'pull-ups de 47 kΩ e detecção em PD4 (ponte SB2). A BlackPill F411 também tem SDIO; Arduino Uno e Nano só leem '
                'cartão por SPI, bem mais devagar.',
        figure='assets/glossary/sdmmc.svg',
        caption='O microSD da H743 no SDMMC1 (PC8 a PC12, PD2 e detecção em PD4) com 22 Ω e pull-ups de 47 kΩ, a leitura de um '
                'bloco de 512 bytes com o comando CMD17, as etapas de inicialização e velocidades e os tipos de cartão.')


def migrate_to_16(con: sqlite3.Connection) -> None:
    document_term(
        con, 'Ethernet', category='comunicacao', after='FDCAN', aliases=('ETH', 'LAN'),
        meaning='Ethernet · rede local com fio (IEEE 802.3)',
        short='A rede com fio de computadores e roteadores: com um PHY e um conector RJ45, o microcontrolador entra na rede local e '
              'fala TCP/IP, HTTP ou MQTT a 10 ou 100 Mbit/s.',
        detail=(
            'O Ethernet é dividido em partes. O MAC, dentro do microcontrolador, monta e confere os quadros: endereços de 6 bytes, '
            'tipo, dados de 46 a 1500 bytes e CRC. O PHY, um chip externo, transforma esses bits no sinal analógico do cabo e '
            'negocia velocidade e duplex com o outro lado. Entre os dois vai a interface MII (17 sinais) ou RMII (9 sinais a 50 MHz), '
            'e o PHY é configurado pelos fios de gerência MDIO/MDC. Depois do PHY vêm o transformador de isolação e o conector RJ45, '
            'muitas vezes num único componente.\n\n'
            'No cabo de par trançado, o 100BASE-TX usa um par para transmitir e outro para receber, até 100 m. O transformador isola '
            'eletricamente os dois equipamentos, por isso o PHY nunca é ligado direto no conector. Cada placa precisa de um endereço '
            'MAC único: o STM32 não traz um gravado de fábrica, então o firmware gera um, por exemplo a partir do ID único de 96 bits '
            'do chip, ou usa um de uma faixa registrada.\n\n'
            'O MAC só entrega quadros; o resto é software. Uma pilha TCP/IP como a LwIP cuida de ARP, IP, DHCP, TCP e UDP, e por cima '
            'dela vêm HTTP, MQTT, Modbus TCP ou sockets. Isso ocupa dezenas de KiB de RAM em buffers e exige um laço de rede ou um '
            'RTOS para processar os pacotes a tempo; o STM32CubeMX gera o esqueleto com LwIP.\n\n'
            'O STM32H743 tem um MAC IEEE 802.3 de 10 e 100 Mbit/s com MII ou RMII, DMA próprio com descritores, FIFOs de 2 KiB, '
            'filtros de endereço e multicast, VLAN, CRC por hardware e relógio PTP (IEEE 1588) para sincronizar o tempo pela rede. O '
            'DMA do Ethernet não alcança a DTCM: descritores e buffers ficam na SRAM do domínio D2, com a região marcada no MPU, como '
            'fazem os exemplos da ST (confira no RM0433). Em RMII, o módulo PHY ou um oscilador fornece os 50 MHz em REF_CLK.'),
        example='H743 WeAct: os 9 sinais RMII estão nos headers — REF_CLK PA1, MDIO PA2, MDC PC1, CRS_DV PA7, RXD0/RXD1 PC4/PC5, '
                'TX_EN PB11 e TXD0/TXD1 PB12/PB13 —, então um módulo LAN8720 liga com fios curtos; PA7 também é o PWDN da câmera '
                '(ponte SB1). A H7R3 também tem MAC Ethernet (só RMII no Z8J6); as outras placas do acervo não têm.',
        figure='assets/glossary/ethernet.svg',
        caption='A cadeia do Ethernet do MAC do H743 ao conector RJ45 (RMII, PHY LAN8720 e transformador), os 9 sinais RMII '
                'disponíveis nos headers da H743, a estrutura de um quadro Ethernet e a pilha de software acima do MAC.')


def migrate_to_17(con: sqlite3.Connection) -> None:
    document_term(
        con, 'PHY', aliases=('camada física',),
        meaning='Physical Layer · camada física',
        short='O circuito que transforma os bits do controlador digital no sinal elétrico que viaja no meio físico (cabo, par '
              'diferencial, fibra) e faz o caminho inverso na recepção.',
        detail=(
            'Toda interface de comunicação tem duas metades: o controlador (MAC, OTG, FDCAN, USART), que organiza os bits em quadros, '
            'e a camada física, que produz os níveis de tensão, as correntes e os tempos que o meio exige. Em interfaces simples as '
            'duas cabem no chip; nas outras, a camada física é um componente à parte, chamado de PHY no Ethernet e no USB e de '
            'transceptor no CAN, no RS-485 e no RS-232.\n\n'
            'Um PHY de Ethernet 100BASE-TX codifica os dados (4B5B, embaralhamento e MLT-3, um sinal de três níveis que reduz a '
            'frequência no cabo), recupera o clock do sinal recebido, detecta se há cabo ligado (link) e combina com o outro lado a '
            'velocidade e o duplex (autonegociação). Ele se liga ao MAC por MII ou RMII e é configurado por MDIO/MDC, com '
            'registradores padronizados: 0 (controle: reset e velocidade), 1 (status: link e negociação concluída) e 2 e 3 '
            '(identificação do fabricante). O endereço do PHY no barramento MDIO vem de pinos de configuração (straps) lidos no '
            'reset.\n\n'
            'Ter o controlador no chip não significa ter a interface pronta: faltam o PHY ou transceptor certo, os componentes do '
            'meio (transformador, terminação, conector) e, às vezes, um clock específico. Por outro lado, alguns PHY vêm integrados: '
            'o STM32 tem PHY USB full-speed interna, então basta ligar D+ e D− ao conector; para USB high-speed é preciso uma PHY '
            'ULPI externa, como a USB3300.\n\n'
            'Problemas típicos de PHY de Ethernet: sem link (cabo, transformador ou reset do PHY), MDIO sem resposta (endereço de '
            'strap diferente do usado no firmware ou falta de pull-up em MDIO), clock de 50 MHz ausente ou ruidoso no RMII e LEDs '
            'do conector trocados pelos straps. Leia primeiro os registradores de identificação: se voltarem 0xFFFF, o MDIO não '
            'está conversando.'),
        example='H743 WeAct: a placa não tem PHY Ethernet; um módulo LAN8720 (PHY, transformador, RJ45 e oscilador de 50 MHz) liga '
                'pelos pinos RMII dos headers. O USB-C usa a PHY full-speed interna do chip, e o CAN precisa de um transceptor '
                'externo como o SN65HVD230.',
        figure='assets/glossary/phy.svg',
        caption='Os controladores do H743 e as camadas físicas que cada um precisa (PHY Ethernet, PHY USB interna ou ULPI e '
                'transceptores CAN, RS-485 e RS-232), o caminho de transmissão de um PHY 100BASE-TX com a codificação MLT-3 bit a '
                'bit e os registradores MDIO usados no diagnóstico.')


def migrate_to_18(con: sqlite3.Connection) -> None:
    document_term(
        con, 'ADC',
        meaning='Analog-to-Digital Converter · conversor analógico-digital',
        short='Mede uma tensão e a transforma em número: 0 V vira 0 e a tensão de referência vira o maior código. É a porta de '
              'entrada de sensores analógicos, potenciômetros, baterias e sinais de áudio.',
        detail=(
            'O ADC dos microcontroladores é do tipo SAR (aproximações sucessivas). Primeiro, um capacitor interno carrega com a '
            'tensão do pino durante o tempo de amostragem (sample and hold); depois o conversor compara essa tensão com frações da '
            'referência, bit a bit, do mais significativo ao menos significativo, como uma busca binária. O resultado é código = '
            'V_entrada ÷ VREF+ × (2ᴺ − 1). Com VREF+ = 3,3 V, 1 LSB vale cerca de 806 µV em 12 bits e 50 µV em 16 bits. A entrada '
            'precisa ficar entre 0 V e VREF+; tensões maiores exigem divisor resistivo.\n\n'
            'Resolução não é precisão. Os bits informados dizem quantos degraus existem; ruído, erros de ganho e de offset e não '
            'linearidade decidem quantos são confiáveis. O número útil é o ENOB (bits efetivos): no STM32H743 rev V, o ADC de 16 bits '
            'tem ENOB típico de 12,2 bits em modo single-ended e 13,2 em modo diferencial (DS12110, tabela 186). Para aproveitar mais '
            'bits: calibre o ADC ao ligar, use média ou a sobreamostragem por hardware, entrada diferencial, uma referência limpa e '
            'capacitores de desacoplamento perto de VDDA e VREF+.\n\n'
            'O tempo de amostragem precisa bastar para o capacitor carregar através da resistência da fonte: um divisor de 100 kΩ '
            'ou um sensor de alta impedância exige tempo maior (a tabela 185 do DS12110 relaciona tempo mínimo e resistência) ou um '
            'buffer com amplificador operacional. Pela regra de Nyquist, a taxa de amostragem precisa passar de 2× a maior '
            'frequência do sinal, com um filtro RC antes do pino para evitar aliasing. Conversões contínuas devem usar DMA e ser '
            'disparadas por um timer, para o intervalo entre amostras ser exato.\n\n'
            'O STM32H743 tem três ADC de 16 bits (resolução configurável em 16, 14, 12, 10 ou 8 bits), com até 20 canais externos '
            'cada, modos simples e varredura, conversão simultânea ou intercalada entre ADCs, entrada diferencial, sobreamostragem, '
            'watchdog analógico (alarme de faixa) e disparo por TIM1, TIM2, TIM3, TIM4, TIM6, TIM8, TIM15, HRTIM e LPTIM1. Na '
            'revisão V, em 16 bits, chega a 3,6 MSPS nos canais diretos, 2,9 MSPS nos rápidos e 1 MSPS nos lentos. O ADC3 também '
            'lê o sensor de temperatura interno e a referência interna VREFINT.'),
        example='Um ADC de 12 bits oferece 4096 códigos. H743 WeAct: entradas livres em PA0–PA3, PA5, PB0, PB1, PC0, PC1, PC4, PC5 e '
                'nos pads PC2_C/PC3_C, com VREF+ ligado ao 3V3 pelo R9. O ADS1256 do TCC é um ADC externo de 24 bits, não o ADC de '
                '12 bits do F411.',
        figure='assets/glossary/adc.svg',
        caption='O caminho do sinal no ADC do H743 (fonte, pino, multiplexador, amostragem, conversor SAR e DMA) com a fórmula do '
                'código, os degraus de quantização, 16 bits nominais contra o ENOB medido, a carga do capacitor de amostragem e as '
                'taxas máximas por tipo de canal.')


def migrate_to_19(con: sqlite3.Connection) -> None:
    document_term(
        con, 'DAC',
        meaning='Digital-to-Analog Converter · conversor digital-analógico',
        short='Transforma um número em tensão analógica: é o caminho inverso do ADC, usado para gerar níveis de referência, formas de '
              'onda e sinais de controle.',
        detail=(
            'O DAC recebe um código e produz V = VREF+ × código ÷ (2ᴺ − 1). No STM32H743, com 12 bits e VREF+ = 3,3 V, cada degrau '
            'vale cerca de 0,8 mV; também existe o modo de 8 bits. A saída passa por um buffer interno que pode ser ligado ou '
            'desligado: ligado, a saída vai de 0,2 V a VDDA − 0,2 V e alimenta cargas de 5 kΩ ou mais; desligado, alcança de 0 a '
            'VREF+, mas com impedância de saída de cerca de 13 kΩ, servindo só para entradas de alta impedância (DS12110, tabela '
            '187).\n\n'
            'O DAC não é fonte de potência: para alimentar LED, motor, alto-falante ou qualquer carga de baixa impedância é preciso '
            'um amplificador operacional ou um transistor depois dele. A precisão depende da referência: com VREF+ ligado ao 3,3 V da '
            'placa, o ruído do regulador aparece na saída. Uma referência dedicada melhora o resultado; o VREFBUF interno do H743 só '
            'pode ser usado se o pino VREF+ não estiver ligado ao 3V3.\n\n'
            'Para gerar formas de onda, a CPU não deve escrever valor por valor: um timer (TIM6 ou TIM7, por exemplo) dispara a '
            'atualização em intervalos exatos e o DMA copia o próximo ponto de uma tabela na memória. A frequência da onda é a taxa '
            'de disparo dividida pelo número de pontos: 1 MHz ÷ 100 pontos = 10 kHz. A saída sai em degraus; um filtro RC ou ativo '
            'depois do pino suaviza a forma. O próprio DAC ainda gera ondas triangulares e ruído pseudoaleatório, úteis em '
            'testes.\n\n'
            'O STM32H743 tem um DAC com dois canais de 12 bits (DAC1_OUT1 em PA4 e DAC1_OUT2 em PA5), atualização de até cerca de '
            '1 MHz (estabiliza em ~2 µs no fundo de escala), atualização simultânea dos dois canais, DMA por canal com detecção de '
            'underrun, disparo por timer e modo sample-and-hold para economizar energia. Quando a velocidade não importa, um PWM com '
            'filtro RC faz o papel de DAC em quase qualquer pino, com mais ondulação.'),
        example='H743 WeAct: DAC1_OUT2 em PA5 está livre nos headers; DAC1_OUT1 em PA4 também é o HSYNC da câmera, e o VREF+ está '
                'ligado ao 3V3 pelo R9. O PIC12F1501 tem DAC de 5 bits; F411, F103 e ATmega328P não têm DAC — no Uno, analogWrite() '
                'é PWM, não tensão contínua.',
        figure='assets/glossary/dac.svg',
        caption='O caminho do DAC do H743 com a fórmula da tensão e as faixas de saída com o buffer ligado e desligado, a geração '
                'de um seno com timer, DMA e tabela antes e depois do filtro RC, e a comparação entre DAC e PWM filtrado.')


def migrate_to_20(con: sqlite3.Connection) -> None:
    document_term(
        con, 'PWM',
        meaning='Pulse-Width Modulation · modulação por largura de pulso',
        short='Liga e desliga uma saída muito rápido, com frequência fixa, variando só a fração do tempo em que ela fica ligada. A '
              'carga "enxerga" a média, e assim um pino digital controla brilho, velocidade e potência.',
        detail=(
            'Um timer conta de 0 até ARR (o período) e recomeça; um registrador de comparação, o CCR, define até onde a saída fica em '
            '1. O duty cycle é CCR ÷ (ARR + 1) e a frequência é f_timer ÷ ((PSC + 1) × (ARR + 1)), em que PSC é o divisor de entrada. '
            'Mudar o CCR muda a largura do pulso sem mudar a frequência, e o hardware só aplica o novo valor no fim do período, sem '
            'cortar um pulso ao meio.\n\n'
            'Frequência e resolução disputam o mesmo clock: com o timer a 240 MHz, 20 kHz deixam 12 000 degraus de duty (cerca de '
            '13,6 bits), mas 1 MHz deixa só 240. Escolha pela carga: LED acima de 1 kHz para não piscar, motor DC entre 16 e 25 kHz '
            'para ficar fora do audível, servo em 50 Hz com pulso de 1 a 2 ms, fontes chaveadas em 100 kHz ou mais (onde o HRTIM '
            'ajuda). Para virar tensão contínua, como um DAC simples, o PWM passa por um filtro RC.\n\n'
            'O pino não fornece potência: motores, fitas de LED e resistências precisam de transistor, MOSFET ou driver (ponte H), '
            'com diodo de roda livre em cargas indutivas. Em meia ponte ou ponte completa, os timers avançados geram pares '
            'complementares (CHx e CHxN) com tempo morto, um intervalo em que os dois transistores ficam desligados para nunca '
            'conduzirem juntos, e uma entrada de freio (BKIN) que desliga as saídas por hardware numa falha. O alinhamento central '
            '(contagem para cima e para baixo) reduz ruído no controle de motores.\n\n'
            'No STM32H743 quase todo timer gera PWM: TIM1 e TIM8 (avançados, com saídas complementares e tempo morto), TIM2 e TIM5 '
            '(32 bits), TIM3, TIM4, TIM12 a TIM17 e os LPTIM, com clock de até 240 MHz, além do HRTIM, com resolução de 2,1 ns. '
            'Canais do mesmo timer dividem a frequência e só variam o duty; frequências diferentes pedem timers diferentes. O DMA '
            'pode trocar o CCR a cada período, o que serve para fitas de LED endereçáveis (WS2812) ou formas de onda.'),
        example='H743 WeAct: TIM2_CH1 a CH4 em PA0–PA3, livres; TIM1_CH1/CH1N em PE9/PE8 para meia ponte; a luz de fundo do display '
                '(PE10) é TIM1_CH2N, então o brilho do LCD se ajusta por PWM. O PIC12F675 não tem PWM por hardware e o PIC12F683 tem '
                'um CCP. No Uno, analogWrite() gera PWM de cerca de 490 ou 980 Hz.',
        figure='assets/glossary/pwm.svg',
        caption='Como o timer gera o PWM (contador, ARR e CCR) com duty de 25 e 75 %, as fórmulas de frequência e duty, a troca '
                'entre frequência e resolução com o timer a 240 MHz e as saídas complementares com tempo morto em PE9/PE8.')


def migrate_to_21(con: sqlite3.Connection) -> None:
    document_term(
        con, 'Timer', aliases=('Timers', 'temporizador', 'temporizadores'),
        meaning='Timer · temporizador e contador de hardware',
        short='Contador de hardware que marca tempo sozinho, sem ocupar a CPU: gera interrupções periódicas, mede pulsos e '
              'frequências, lê encoders, dispara o ADC e produz PWM.',
        detail=(
            'Todo timer tem a mesma base: um clock de entrada passa por um divisor (PSC) e incrementa o contador (CNT) até o valor de '
            'recarga (ARR). Ao chegar lá, o contador volta a zero e gera um evento de atualização, que pode chamar uma interrupção, '
            'pedir um DMA ou disparar outro periférico (saída TRGO). O período é (PSC + 1) × (ARR + 1) ÷ f_clock: com o timer a '
            '240 MHz, PSC = 23 999 e ARR = 9 dão exatamente um evento por milissegundo, independente do que o programa esteja '
            'fazendo.\n\n'
            'Os canais de captura e comparação ampliam o uso. Em captura, uma borda no pino copia o valor do contador para o '
            'registrador CCR no mesmo instante, sem atraso de software: a diferença entre duas capturas dá período, frequência ou '
            'largura de pulso. Em comparação, quando o contador alcança o CCR, o timer muda o pino, gera PWM ou um pulso único '
            '(one-pulse). No modo encoder, dois canais leem os sinais A e B de um encoder em quadratura e o contador sobe ou desce '
            'sozinho: o CNT passa a ser a posição do eixo.\n\n'
            'Timers também se encadeiam: um timer mestre pode iniciar, pausar ou contar os eventos de outro, ou disparar conversões '
            'do ADC e atualizações do DAC em intervalos exatos, sem o jitter de fazer a mesma coisa num laço de programa. Contadores '
            'de 16 bits estouram em 65 536; para contagens longas ou rápidas, use um timer de 32 bits ou conte os estouros.\n\n'
            'O STM32H743 tem 22 timers e watchdogs, mais o SysTick: o HRTIM (alta resolução), dois avançados (TIM1 e TIM8, com '
            'saídas complementares), dez de uso geral (TIM2 e TIM5 de 32 bits; TIM3, TIM4 e TIM12 a TIM17), dois básicos (TIM6 e '
            'TIM7, sem pinos, para base de tempo e DAC), cinco de baixo consumo (LPTIM1 a LPTIM5, que funcionam no modo Stop) e dois '
            'watchdogs. O clock dos timers chega a 240 MHz, e todos podem ser congelados durante a depuração.'),
        example='H743 WeAct: TIM2 ou TIM5 em PA0–PA3, livres, para encoder (PA0/PA1) ou captura. O PIC12F675 tem Timer0 de 8 bits e '
                'Timer1 de 16 bits; no Arduino, millis() usa o Timer0 do ATmega328P.',
        figure='assets/glossary/timer.svg',
        caption='O interior de um timer do H743 (clock, prescaler, contador, ARR, evento de atualização e canais de captura e '
                'comparação), três usos além do PWM — medir frequência, ler encoder e dar ritmo ao ADC — e a tabela dos timers do '
                'H743.')


def migrate_to_22(con: sqlite3.Connection) -> None:
    document_term(
        con, 'HRTIM', aliases=('HRTIM1',),
        meaning='High-Resolution Timer · temporizador de alta resolução',
        short='Conjunto de timers sincronizados feito para eletrônica de potência: gera pulsos com passo de nanossegundos, pares com '
              'tempo morto e desligamento por falha em hardware.',
        detail=(
            'O HRTIM reúne seis timers que trabalham juntos: um mestre, que dá o ritmo e as fases, e cinco escravos (A a E), cada um '
            'com duas saídas. Cada saída é ligada e desligada por uma lista de eventos (fim do período, comparações, eventos '
            'externos, o mestre), o que permite formas de onda que um timer comum não faz: pulsos defasados entre si, frequência '
            'variável com tempo ligado constante, modos push-pull e ressonante e rajadas (burst).\n\n'
            'A diferença está no passo de tempo. No STM32H743, o núcleo do HRTIM roda a 480 MHz, então duty e período se ajustam em '
            'degraus de 2,1 ns, metade do passo de um timer comum a 240 MHz. Numa fonte buck de 200 kHz com 12 V de entrada, isso dá '
            'degraus de 5 mV na saída em vez de 10 mV. Na G474 do acervo, o HRTIM usa um DLL e chega a 184 ps, degrau cerca de 11 '
            'vezes menor que o do H743 — por isso a G474 é a escolha para controle de potência fino.\n\n'
            'A proteção também é por hardware: cinco entradas de falha (FLT) desligam as saídas em nanossegundos quando um '
            'comparador detecta sobrecorrente, sem esperar o software, e dez entradas de evento externo reagem a sinais como '
            'corrente zero ou limite de corrente. As saídas podem ser pareadas com tempo morto para meias pontes, e o HRTIM dispara o '
            'ADC num ponto exato do ciclo, por exemplo no meio do pulso, para medir a corrente longe do ruído de chaveamento.\n\n'
            'Serve para conversores buck e boost, pontes completas com deslocamento de fase, conversores LLC, conversores '
            'intercalados de várias fases, iluminação LED e inversores. Também funciona como timer comum ou como PWM de alta '
            'resolução para imitar um DAC. Trabalhar com potência exige cuidado: driver de gate adequado, layout curto, medição de '
            'corrente e primeiros testes com fonte limitada em corrente.'),
        example='H743 WeAct: no LQFP100 existem as saídas dos timers A a D (o E não tem pinos); só o timer C está livre nos headers, '
                'em PA9 (CHC1) e PA10 (CHC2), com a entrada de falha FLT1 em PA15. A G474 do acervo tem HRTIM de 184 ps com 12 '
                'saídas, mais adequado para fontes chaveadas.',
        figure='assets/glossary/hrtim.svg',
        caption='A estrutura do HRTIM do H743 (timer mestre e timers A a E, com os pinos na placa), três fases defasadas de 120°, a '
                'resolução do timer comum, do HRTIM do H743 e do HRTIM da G474 numa fonte buck de 200 kHz, e uma meia ponte com '
                'driver, tempo morto e proteção por entrada de falha.')


def migrate_to_23(con: sqlite3.Connection) -> None:
    document_term(
        con, 'Watchdog', aliases=('IWDG', 'WWDG', 'watchdogs'),
        meaning='Watchdog · temporizador de supervisão ("cão de guarda")',
        short='Contador que reinicia o chip se o programa deixar de "alimentá-lo" a tempo: a última defesa contra travamentos em '
              'equipamentos que precisam continuar funcionando sozinhos.',
        detail=(
            'O watchdog conta para baixo a partir de um valor de recarga. Quando o programa está funcionando, ele escreve uma chave '
            'num registrador de tempos em tempos e recarrega o contador ("alimenta" o watchdog). Se o programa travar num laço '
            'infinito, esperar para sempre um periférico que não responde ou se perder por um erro de memória, o contador chega ao '
            'fim e o chip é reiniciado por hardware, voltando a um estado conhecido.\n\n'
            'O IWDG (independente) usa o oscilador interno LSI, de cerca de 32 kHz, separado do clock principal: continua '
            'funcionando se o cristal ou o PLL falharem e também nos modos Stop e Standby. Tem contador de 12 bits e prescaler de /4 '
            'a /256, com prazo de cerca de 0,125 ms a 32,8 s (prazo = 4 × 2ᴾᴿ × (RL + 1) ÷ 32 kHz); depois de ligado, só um reset o '
            'desliga. Como o LSI varia com a temperatura e de chip para chip, deixe folga no prazo.\n\n'
            'O WWDG (com janela) usa o clock do barramento, tem contador de 7 bits e exige que a recarga aconteça dentro de uma '
            'janela: cedo demais também causa reset. Assim ele detecta tanto o programa parado quanto o programa que corre rápido '
            'demais, pulando etapas. Um aviso antecipado (EWI), quando o contador chega a 0x40, permite salvar dados ou registrar o '
            'erro logo antes do reset. Com o barramento a 120 MHz, o prazo vai de dezenas de microssegundos até cerca de 280 ms.\n\n'
            'Boas práticas: alimente no laço principal, depois de conferir que cada tarefa deu sinal de vida — nunca numa '
            'interrupção de timer, que continua rodando mesmo com o programa travado. Escolha um prazo acima do pior caso normal '
            '(gravar Flash, montar o cartão SD). Na inicialização, leia a causa do reset (RCC_RSR) e registre quando foi o '
            'watchdog, e congele os watchdogs durante a depuração (DBGMCU). O watchdog não conserta o erro: só tira o sistema de um '
            'estado travado.'),
        example='O STM32H743 tem um IWDG e um WWDG. No Arduino, a biblioteca avr/wdt.h usa o watchdog do ATmega328P (prazos de 15 ms '
                'a 8 s); nos PICs o WDT é ligado pelos bits de configuração, o que às vezes reinicia um programa que "funcionava" no '
                'simulador.',
        figure='assets/glossary/watchdog.svg',
        caption='O contador do watchdog sendo alimentado até um travamento provocar o reset, a comparação entre o IWDG independente '
                'e o WWDG com janela no H743, com prazos e fórmulas, e as boas práticas de uso.')


def migrate_to_24(con: sqlite3.Connection) -> None:
    document_term(
        con, 'SysTick', category='fundamentos', after='Watchdog',
        meaning='SysTick · temporizador de sistema do núcleo Arm Cortex-M',
        short='Contador simples que faz parte do núcleo Cortex-M e gera a interrupção periódica, normalmente de 1 ms, que dá ao '
              'programa a noção de tempo: HAL_Delay, HAL_GetTick, timeouts e o escalonador do RTOS dependem dele.',
        detail=(
            'O SysTick é um contador de 24 bits que desce do valor de recarga (LOAD) até zero no clock da CPU (ou no clock ÷ 8). Ao '
            'chegar a zero, recarrega sozinho e, se habilitado, gera a interrupção SysTick_Handler. Como faz parte do núcleo Arm, e '
            'não dos periféricos do fabricante, funciona igual em todos os Cortex-M: o mesmo código de tick roda num F103, num G474 '
            'ou num H743.\n\n'
            'Para um tick de 1 ms, LOAD = f_CPU ÷ 1000 − 1: 479 999 no H743 a 480 MHz, 71 999 na BluePill a 72 MHz. Como o '
            'registrador tem 24 bits (até 16 777 215), o maior período possível a 480 MHz é de cerca de 35 ms. A HAL da ST configura '
            'isso em HAL_Init() e incrementa a variável uwTick a cada interrupção; HAL_GetTick() devolve esse valor e HAL_Delay() '
            'espera comparando-o. Para medir um trecho, subtraia dois valores de HAL_GetTick(): a subtração sem sinal continua certa '
            'mesmo quando o contador de 32 bits dá a volta, depois de cerca de 49 dias.\n\n'
            'Um RTOS como o FreeRTOS usa o SysTick como relógio do escalonador: a cada tick ele decide qual tarefa roda. Nesse caso '
            'o CubeMX recomenda passar a base de tempo da HAL para outro timer (TIM6 é o comum), para os dois não disputarem a mesma '
            'interrupção. A resolução de 1 ms não serve para medir microssegundos: para isso use o contador de ciclos da CPU '
            '(DWT->CYCCNT, 1 ciclo = 2,08 ns a 480 MHz) ou um timer de 32 bits.\n\n'
            'Cuidados: HAL_Delay() dentro de uma interrupção com prioridade igual ou maior que a do SysTick trava para sempre, '
            'porque o tick nunca avança; o mesmo acontece com as interrupções desligadas. Mudar o clock do sistema exige '
            'reconfigurar o SysTick (HAL_RCC_ClockConfig já faz isso). No modo Stop o SysTick para, então o tempo "some" durante o '
            'sono; para contar tempo dormindo, use o RTC ou um LPTIM.'),
        example='Existe em todas as STM32 do acervo (H743, H7R3, G474, F411 e F103), porque faz parte do núcleo Cortex-M. Arduino Uno '
                'e Nano (ATmega328P, AVR) não têm SysTick: millis() e delay() usam o Timer0.',
        figure='assets/glossary/systick.svg',
        caption='O contador SysTick descendo e gerando a interrupção de 1 ms, as funções que dependem do tick (HAL_GetTick, '
                'HAL_Delay, timeouts e RTOS), a medição de tempo e os valores de recarga para as placas STM32 do acervo.')


def migrate_to_25(con):
    from purchase_20261026 import migrate as register_purchase
    register_purchase(con)


MIGRATIONS = {2: migrate_to_2, 3: migrate_to_3, 4: migrate_to_4, 5: migrate_to_5, 6: migrate_to_6, 7: migrate_to_7, 8: migrate_to_8,
              9: migrate_to_9, 10: migrate_to_10, 11: migrate_to_11, 12: migrate_to_12, 13: migrate_to_13, 14: migrate_to_14,
              15: migrate_to_15, 16: migrate_to_16, 17: migrate_to_17, 18: migrate_to_18, 19: migrate_to_19, 20: migrate_to_20,
              21: migrate_to_21, 22: migrate_to_22, 23: migrate_to_23, 24: migrate_to_24,
              25: migrate_to_25}


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

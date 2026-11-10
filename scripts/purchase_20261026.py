"""Migração 25: kits informados em 26/10/2026. A H743 é a unidade existente.

M12 identifica a montagem da lente, não o sensor da câmera.
"""
import json
import db

SIPEED = 'https://wiki.sipeed.com/hardware/en/tang/Tang-Nano-9K/Nano-9K.html'
WEACT = 'https://github.com/WeActStudio/MiniSTM32H7xx'


def images(prefix, title):
    return [{'file': f'{prefix}-simple.png', 'title': f'Visão simples · {title}'},
            {'file': f'{prefix}-full.png', 'title': f'Referência completa · {title}'}]


TANG = {
    'subtitle': 'GOWIN GW1NR-LV9QN88PC6/I5 · FPGA de 8.640 LUT4',
    'variant': 'Sipeed Tang Nano 9K · kit com LCD de 4,3″',
    'logic': '8.640 LUT4 · 6.480 registradores · 20 multiplicadores 18 × 18 · 2 PLL',
    'cpu': 'Lógica programável; processador RISC-V pode ser implementado no projeto',
    'oscillator': '27 MHz na placa; frequência do circuito depende do projeto e da análise de temporização',
    'external': 'Flash SPI de 32 Mbit (4 MiB)',
    'memory': '468 Kibit de RAM em blocos · 17.280 bits de Shadow SRAM · 64 Mbit (8 MiB) de PSRAM',
    'package': 'GW1NR-LV9QN88PC6/I5 · QN88P',
    'gpio': '2 fileiras de 24 furos; sinais compartilhados com tela, microSD e HDMI',
    'serial': 'HDMI (vídeo digital), RGB (vermelho/verde/azul) paralelo e SPI (interface periférica serial); demais interfaces em lógica',
    'voltage': 'Bancos de 3,3 V e 1,8 V; alimentação por USB-C de 5 V',
    'connector': '2 × 24 furos de 2,54 mm · tela RGB em cabo flexível de 40 vias',
    'programmer': 'USB-JTAG integrado com BL702; JTAG é a interface de gravação e depuração. Descrever o circuito em Verilog, uma linguagem de descrição de hardware, e gerar a configuração.',
    'special': '6 LEDs, 2 botões, leitor microSD e conector para tela SPI de 1,14″; PSRAM integrada ao chip',
    'use': 'Circuitos digitais, vídeo, interfaces paralelas e processadores RISC-V implementados em lógica.',
    'notes': 'Compra informada na variante “9k with 4.3 LCD”. Tela cadastrada separadamente em Periféricos. Recebimento e teste físico não informados. A frequência do oscilador não é um limite de processamento.',
    'origin': 'Anúncio enviado pelo usuário em 26/10/2026; características e ligações conferidas na documentação Sipeed',
    'evidence': 'docs/evidence/tangnano9k-lcd-purchase.png',
    'source_url': SIPEED,
    'datasheet': 'tangnano9k-schematic.pdf',
    'document_kind': 'esquema',
    'schematic': 'tangnano9k-schematic.pdf',
    'pinout_source': 'tangnano9k-schematic.pdf',
    'pinout': 'tangnano9k-pinout-simple.png',
    'pinouts': images('tangnano9k-pinout', '48 furos, recursos da placa e bancos de tensão'),
    'pinout_credit': 'Desenhos do almoxarifado; esquema e mapa de pinos oficiais Sipeed, consultados em 26/10/2026.',
    'pinout_notice': 'Vista superior, USB-C no topo. Pinos 79–86: lógica de 1,8 V. Tela RGB, HDMI e conectores compartilham sinais; conferir o esquema antes de usar em conjunto.',
}

LCD = {
    'subtitle': '4,3″ · 480 × 272 pixels · kit Tang Nano 9K',
    'variant': 'Tela LCD de 4,3″ do kit Sipeed Tang Nano 9K',
    'resolution': '480 × 272 pixels',
    'size': 'Diagonal de 4,3 polegadas',
    'serial': 'RGB paralelo; exemplo Sipeed com 16 bits de cor (5 vermelho, 6 verde, 5 azul)',
    'voltage': 'Referência da porta Sipeed: lógica de 3,3 V; luz de fundo pelo circuito da placa',
    'connector': 'Porta RGB de 40 vias da Tang Nano 9K; confirmar face dos contatos e pino 1 no painel recebido',
    'compatibility': 'Kit Tang Nano 9K; exemplo lcd_4.3 para 480 × 272',
    'programmer': 'Conectar à porta RGB de 40 vias da Tang Nano 9K e usar o exemplo lcd_4.3 da Sipeed. A tela recebe pixels e sinais de sincronismo continuamente.',
    'use': 'Interface gráfica, instrumentos de bancada e estudo de geração de vídeo em lógica programável.',
    'notes': 'Tamanho e resolução confirmados no anúncio. Código exato do painel, presença de toque e limites elétricos do painel não informados; não assumir toque. A folha mostra a porta da placa, não uma pinagem confirmada do painel adquirido.',
    'origin': 'Anúncio enviado em 26/10/2026, variante “9k with 4.3 LCD”; esquema e exemplo Sipeed lcd_4.3',
    'evidence': 'docs/evidence/tangnano9k-lcd-purchase.png',
    'source_url': 'https://github.com/sipeed/TangNano-9K-example/tree/main/lcd_4.3',
    'pinout_source': 'tangnano9k-schematic.pdf',
    'pinout': 'lcd43-connections-simple.png',
    'pinouts': images('lcd43-connections', 'porta RGB da Tang Nano 9K'),
    'pinout_credit': 'Desenhos do almoxarifado; porta J4 do esquema Sipeed e restrições de pinos do exemplo lcd_4.3.',
    'pinout_notice': 'Referência da porta da Tang Nano 9K. Código do painel não confirmado. Confira orientação e contatos do cabo antes de conectar.',
}

CAMERA = {
    'subtitle': 'Lente M12 · kit H743-LCD-M12 · sensor a confirmar',
    'variant': 'Módulo de câmera M12 do kit WeAct H743-LCD-M12',
    'resolution': 'A confirmar: o anúncio não identifica o sensor',
    'sensor': 'A confirmar; M12 descreve a montagem da lente, não o sensor',
    'serial': 'DVP (Digital Video Port, vídeo digital paralelo); DCMI é a interface de câmera do STM32',
    'voltage': 'Usar as alimentações da porta de câmera WeAct; não aplicar 5 V aos sinais',
    'connector': 'Referência da H743: cabo flexível de 24 vias; conferir o módulo recebido',
    'compatibility': 'Kit H743-LCD-M12; identificar o sensor antes de selecionar seu controlador de software',
    'programmer': 'Conectar à porta da H743, identificar o sensor e selecionar seu controlador de software. Configuração por SCCB (Serial Camera Control Bus, barramento de controle da câmera); pixels pelo barramento paralelo.',
    'use': 'Captura de imagens e projetos de visão embarcada com a WeAct H743.',
    'notes': 'A H743 deste kit é a mesma unidade registrada em setembro, conforme confirmação do usuário. M12 não permite concluir que seja OV2640, OV7725 ou outro sensor. Recebimento e teste físico não informados.',
    'origin': 'Anúncio enviado em 26/10/2026, variante “H743-LCD-M12”; sinais da porta no esquema oficial WeAct V1.2',
    'evidence': 'docs/evidence/weact-h743-m12-purchase.png',
    'source_url': WEACT,
    'pinout_source': 'h743-schematic.pdf',
    'pinout': 'camera-m12-connections-simple.png',
    'pinouts': images('camera-m12-connections', 'sinais da porta de câmera da H743'),
    'pinout_credit': 'Desenhos do almoxarifado; porta de câmera do esquema WeAct MiniSTM32H7xx V1.2. Não representa pinagem confirmada do sensor.',
    'pinout_notice': 'Sensor não identificado. As imagens mostram sinais da H743, sem atribuir números aos contatos do módulo adquirido.',
}


def migrate(con):
    con.execute('ALTER TABLE categories ADD COLUMN position INTEGER NOT NULL DEFAULT 1')
    con.execute('ALTER TABLE categories ADD COLUMN columns_json TEXT DEFAULT NULL CHECK(columns_json IS NULL OR json_valid(columns_json))')
    columns = {r['key']: dict(r) for r in con.execute('SELECT * FROM table_columns')}

    def layout(extra):
        return json.dumps([columns[k] for k in ('name', 'family', 'stock')] + [
            {'key': key, 'label': label, 'group_id': 'perifericos', 'width': width,
             'format': 'annotated', 'field': None, 'unit': None, 'digits': None,
             'term': None, 'help': None} for key, label, width in extra], ensure_ascii=False)

    con.execute('INSERT INTO categories VALUES (?, ?, ?, ?)', ('logica-programavel', 'Lógica programável', 2,
        layout([('logic', 'Recursos lógicos', 330), ('memory', 'Memórias', 330),
                ('external', 'Flash externa', 220), ('voltage', 'Lógica / alimentação', 260)])))
    con.execute('INSERT INTO categories VALUES (?, ?, ?, ?)', ('perifericos', 'Periféricos', 3,
        layout([('resolution', 'Resolução', 260), ('serial', 'Interface', 330),
                ('connector', 'Conexão', 330), ('compatibility', 'Compatibilidade', 330)])))
    for i, (family, description, color) in enumerate([
        ('GOWIN', 'FPGA GOWIN: matriz lógica programável', 'violet'),
        ('Display', 'Telas e módulos de visualização', 'teal'),
        ('Câmera', 'Módulos de captura de imagem', 'orange')], 4):
        con.execute('INSERT INTO families VALUES (?, ?, ?, ?, ?)', (family, family, description, color, i))
    for i, (key, label) in enumerate([('logic', 'Recursos lógicos'), ('memory', 'Memórias do dispositivo'),
                                     ('resolution', 'Resolução'), ('size', 'Tamanho'), ('sensor', 'Sensor'),
                                     ('connector', 'Conexão'), ('compatibility', 'Compatibilidade')], 22):
        con.execute('INSERT INTO spec_fields VALUES (?, ?, ?, ?, ?, ?)', (key, label, 'text', 1, 1, i))
    # Termos novos continuam acessíveis pelo mesmo glossário das fichas existentes.
    for term, meaning, short, example in [
        ('FPGA', 'Field-Programmable Gate Array · matriz de portas programável em campo',
         'Chip cujo circuito digital é configurado pelo projeto: portas, registradores e conexões passam a funcionar em paralelo.',
         'A Tang Nano 9K permite implementar vídeo, interfaces ou um processador RISC-V; esse processador não vem fixo no chip.'),
        ('LUT4', 'Look-Up Table de 4 entradas · tabela de consulta lógica de quatro entradas',
         'Pequeno bloco configurável que implementa uma função lógica de até quatro entradas. A quantidade descreve capacidade lógica, não velocidade de uma CPU.',
         'A Tang Nano 9K tem 8.640 LUT4; o uso real depende do circuito sintetizado.'),
        ('PSRAM', 'Pseudo-Static Random-Access Memory · memória de acesso aleatório pseudoestática',
         'Memória com atualização interna que apresenta uma interface mais simples ao circuito controlador. Capacidade não significa a mesma latência da RAM em blocos.',
         'O GW1NR da Tang Nano 9K inclui 64 Mbit, equivalentes a 8 MiB; o projeto precisa de um controlador para acessá-la.'),
        ('LCD', 'Liquid Crystal Display · tela de cristal líquido',
         'Painel que controla a passagem da luz para formar pixels. A interface e o controlador variam entre modelos.',
         'O kit da Tang Nano 9K inclui uma tela de 4,3 polegadas e 480 × 272 pixels; o código do painel ainda não foi confirmado.'),
        ('RGB', 'Red, Green, Blue · vermelho, verde e azul',
         'Representação de cores por três canais. Em uma porta RGB paralela, grupos de fios levam os canais junto com sinais de sincronismo.',
         'O exemplo lcd_4.3 da Sipeed usa RGB565: 5 bits vermelhos, 6 verdes e 5 azuis.'),
        ('JTAG', 'Joint Test Action Group · interface padronizada de teste e depuração',
         'Interface serial usada para testar circuitos, depurar e, em dispositivos compatíveis, carregar a configuração.',
         'O BL702 da Tang Nano 9K oferece acesso USB-JTAG integrado para configurar a FPGA.'),
        ('HDMI', 'High-Definition Multimedia Interface · interface multimídia de alta definição',
         'Interface digital de áudio e vídeo. A existência de um conector não garante que todo projeto implemente áudio ou todos os modos do padrão.',
         'A Tang Nano 9K expõe um conector HDMI; seus sinais compartilham pinos com a porta RGB.'),
        ('DVP', 'Digital Video Port · porta de vídeo digital',
         'Interface de câmera em que vários fios transportam os bits de cada pixel, acompanhados de clock e sinais de sincronismo.',
         'A porta de câmera da WeAct H743 usa D0–D7, PIXCLK, HSYNC e VSYNC; identificar o sensor antes de configurar o software.'),
        ('SCCB', 'Serial Camera Control Bus · barramento serial de controle de câmera',
         'Barramento usado para configurar registradores de sensores de imagem. Ele transmite ajustes; os pixels seguem por outra interface.',
         'Na referência WeAct H743, PB8 e PB9 são os sinais de clock e dados para configurar a câmera.')]:
        position = con.execute("SELECT COALESCE(MAX(position), 0) + 1 FROM glossary WHERE category_id = 'fundamentos'").fetchone()[0]
        con.execute('INSERT INTO glossary(term, category_id, position, meaning, short, detail, example, aliases) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (term, 'fundamentos', position, meaning, short, short, example, '[]'))
    position = con.execute('SELECT MAX(position) FROM components').fetchone()[0]
    for i, (id, category, name, family, specs) in enumerate([
        ('tangnano9k', 'logica-programavel', 'Sipeed Tang Nano 9K', 'GOWIN', TANG),
        ('lcd43', 'perifericos', 'LCD RGB 4,3″', 'Display', LCD),
        ('camera-m12', 'perifericos', 'Câmera WeAct M12', 'Câmera', CAMERA)], 1):
        con.execute('INSERT INTO components VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (id, category, name, family, 'placa', 0, position + i, json.dumps(specs, ensure_ascii=False, sort_keys=True)))
        con.execute('INSERT INTO movements(component_id, type_id, quantity, date, note, created_at) VALUES (?, ?, ?, ?, ?, ?)',
                    (id, 'compra', 1, '2026-10-26', 'Compra informada em 26/10/2026; data exata não informada. Item cadastrado separadamente do kit.', db.now()))
    specs = json.loads(con.execute("SELECT specs FROM components WHERE id = 'h743'").fetchone()['specs'])
    specs['evidence'] = 'docs/evidence/weact-h743-m12-purchase.png'
    specs['notes'] += ' Em 26/10/2026 o usuário confirmou que o kit H743-LCD-M12 é esta mesma unidade. Câmera cadastrada em Periféricos; display de 0,96″ permanece como recurso da placa.'
    con.execute("UPDATE components SET specs = ? WHERE id = 'h743'", (json.dumps(specs, ensure_ascii=False, sort_keys=True),))

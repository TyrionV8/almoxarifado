"""Gera seis folhas técnicas no padrão simples/completo do almoxarifado.

Uso: python3 scripts/make_purchase_pinouts.py (Pillow e fontes DejaVu).
Mapas: esquema Sipeed Tang Nano 9K, mapa oficial e exemplo lcd_4.3;
porta de câmera: esquema WeAct H743 V1.2. Ver docs/COMPRAS-2026-10-26.md.
Os desenhos das placas são esquemáticos, fora de escala.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/pinouts'
FONT = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
BOLD = FONT.with_name('DejaVuSans-Bold.ttf')
COLORS = {'power': '#ff2222', 'ground': '#111111', 'pin': '#2ec5e8',
          'gpio': '#fff4a3', 'rgb': '#ffbd6b', 'spi': '#8f86e8',
          'clock': '#f28b8b', 'control': '#c6def0', 'data': '#88e18c',
          'bank18': '#e2d6f1', 'other': '#f0f0f0'}

# Ordem física de cima para baixo, USB-C no topo; mapa oficial Sipeed.
LEFT = [38, 37, 36, 39, 25, 26, 27, 28, 29, 30, 33, 34,
        40, 35, 41, 42, 51, 53, 54, 55, 56, 57, 68, 69]
RIGHT = [63, 86, 85, 84, 83, 82, 81, 80, 79, 77, 76, 75,
         74, 73, 72, 71, 70, '5V', 48, 49, 31, 32, 'GND', '3V3']
PORTS = dict(zip(LEFT, ['IOB31B', 'IOB31A', 'IOB29B', 'IOB33A', 'IOB8A', 'IOB8B', 'IOB11A',
                      'IOB11B', 'IOB13A', 'IOB13B', 'IOB23A', 'IOB23B', 'IOB33B', 'IOB29A',
                      'IOB41A', 'IOB41B', 'IOR17B', 'IOR15B', 'IOR15A', 'IOR14B', 'IOR14A',
                      'IOR13A', 'IOT42B', 'IOT42A']))
PORTS.update(dict(zip(RIGHT[:17], ['IOR5A', 'IOT8A', 'IOT8B', 'IOT10A', 'IOT10B', 'IOT11A',
                                 'IOT11B', 'IOT12A', 'IOT12B', 'IOT37A', 'IOT37B', 'IOT38A',
                                 'IOT38B', 'IOT39A', 'IOT39B', 'IOT41A', 'IOT41B'])))
PORTS.update({48: 'IOR24B', 49: 'IOR24A', 31: 'IOB15A', 32: 'IOB15B'})
FUNCTIONS = {38: ('spi', 'microSD · CS'), 37: ('spi', 'microSD · MOSI'),
             36: ('spi', 'microSD · SCLK'), 39: ('spi', 'microSD · MISO'),
             33: ('rgb', 'RGB · DE'), 34: ('rgb', 'RGB · VSYNC'),
             40: ('rgb', 'RGB · HSYNC'), 35: ('clock', 'RGB · clock'),
             63: ('control', 'RGB · INIT / XL'), 86: ('clock', 'Luz de fundo · PWM'),
             77: ('spi', 'LCD SPI · dados'), 76: ('spi', 'LCD SPI · clock'),
             48: ('spi', 'LCD SPI · CS'), 49: ('spi', 'LCD SPI · RS'),
             31: ('control', 'RGB · INIT / YD'), 32: ('control', 'RGB · INIT / XR')}
for pin, label in zip([41, 42, 51, 53, 54, 55, 56, 57, 68, 69, 70, 71, 72, 73, 74, 75],
                      ['B7', 'B6', 'B5', 'B4', 'B3', 'G7', 'G6', 'G5', 'G4', 'G3',
                       'G2', 'R7', 'R6', 'R5', 'R4', 'R3']):
    FUNCTIONS[pin] = ('rgb', f'RGB · {label}')
HDMI = {68: 'CK−', 69: 'CK+', 70: 'D0−', 71: 'D0+', 72: 'D1−', 73: 'D1+', 74: 'D2−', 75: 'D2+'}

# Porta J4 da placa: o modelo exato do painel comprado não foi identificado.
LCD_PORT = [
    ('LEDK', 'Circuito de luz · VLED−'), ('LEDA', 'Circuito de luz · VLED+'),
    ('GND', 'Terra'), ('VCC', '3,3 V'),
    *[(f'R{i}', 'GND' if i < 3 else f'FPGA {78-i}') for i in range(8)],
    *[(f'G{i}', 'GND' if i < 2 else f'FPGA {[70,69,68,57,56,55][i-2]}') for i in range(8)],
    *[(f'B{i}', 'GND' if i < 3 else f'FPGA {[54,53,51,42,41][i-3]}') for i in range(8)],
    ('GND', 'Terra'), ('CLK', 'FPGA 35'), ('DISP', '3,3 V'),
    ('HSYNC', 'FPGA 40'), ('VSYNC', 'FPGA 34'), ('DEN', 'FPGA 33'),
    ('NC', 'Sem ligação'), ('GND', 'Terra'), ('XR', 'FPGA 32'),
    ('YD', 'FPGA 31'), ('XL', 'FPGA 63'), ('YU', 'FPGA 50')]

# Sinais da porta de câmera da H743: nenhuma numeração do módulo desconhecido.
CAMERA_SIGNALS = [
    ('D0', 'PC6', 'data'), ('D1', 'PC7', 'data'), ('D2', 'PE0', 'data'), ('D3', 'PE1', 'data'),
    ('D4', 'PE4', 'data'), ('D5', 'PD3', 'data'), ('D6', 'PE5', 'data'), ('D7', 'PE6', 'data'),
    ('VSYNC', 'PB7', 'clock'), ('HSYNC', 'PA4', 'clock'), ('PIXCLK', 'PA6', 'clock'),
    ('XCLK', 'PA8 · MCO1', 'clock'), ('SCL', 'PB8 · I2C1', 'control'),
    ('SDA', 'PB9 · I2C1', 'control'), ('PWDN', 'PA7 · ponte SB1', 'control')]


class Sheet:
    def __init__(self, height, title, subtitle):
        self.im = Image.new('RGB', (2800, height), 'white')
        self.d = ImageDraw.Draw(self.im)
        self.text((60, 40), title, 44, bold=True)
        self.text((60, 104), subtitle, 25, fill='#555555')
        self.d.line((60, 158, 2740, 158), fill='#cccccc', width=2)

    def text(self, xy, text, size=24, fill='#191919', bold=False, anchor=None):
        self.d.text(xy, text, font=ImageFont.truetype(str(BOLD if bold else FONT), size), fill=fill, anchor=anchor)

    def box(self, x, y, w, h, text, color='other', size=23):
        bg = COLORS.get(color, color)
        self.d.rounded_rectangle((x, y, x+w, y+h), radius=4, fill=bg, outline='#999999', width=1)
        self.text((x+w/2, y+h/2), text, size, '#ffffff' if color in ('ground', 'power') else '#111111', True, 'mm')

    def footer(self, lines):
        y = self.im.height - 80 - len(lines)*40
        self.d.line((60, y-24, 2740, y-24), fill='#cccccc', width=2)
        for line in lines:
            self.text((60, y), line, 23)
            y += 40
        self.text((2740, self.im.height-32), 'ALMOXARIFADO · 26/10/2026 · desenho fora de escala', 19, '#777777', anchor='rs')

    def save(self, name):
        self.im.save(OUT/name, optimize=True)
        print(name, self.im.size)


def board(s, x, y, w, h):
    s.d.rounded_rectangle((x, y, x+w, y+h), radius=32, fill='#242d2a', outline='#aaa27b', width=5)
    s.box(x+w/2-82, y-24, 164, 110, 'USB-C', '#d5d7d6', 23)
    s.box(x+w/2-110, y+h-75, 220, 130, 'HDMI', '#d5d7d6', 26)
    s.box(x+90, y+280, w-180, 270, 'GW1NR-9', '#a8aaa9', 24)
    s.box(x+95, y+650, w-190, 65, 'RGB · 40 vias', '#e9e9de', 21)
    s.text((x+w/2, y+590), 'TANG NANO 9K', 27, '#ffffff', True, 'mm')
    for n in range(24):
        cy = 240+n*57+24
        for cx in (x+22, x+w-22):
            s.d.ellipse((cx-10, cy-10, cx+10, cy+10), fill='#d7b64d', outline='#f9edbc', width=2)


def tang(full=False):
    s = Sheet(2050, 'SIPEED TANG NANO 9K · PINAGEM ' + ('COMPLETA' if full else 'SIMPLES'),
              'Vista superior · USB-C no topo · número do pino QN88P junto à placa · todas as posições dos dois headers')
    s.text((60, 190), 'HEADER J5 · de cima para baixo', 25, bold=True)
    s.text((1695, 190), 'HEADER J6 · de cima para baixo', 25, bold=True)
    board(s, 1180, 220, 440, 1455)
    for side, pins in [('left', LEFT), ('right', RIGHT)]:
        for n, p in enumerate(pins):
            y = 240+n*57
            x = 60 if side == 'left' else 1680
            if isinstance(p, str):
                s.box(x, y, 1060, 45, p + (' · terra' if p == 'GND' else ' · alimentação'), 'ground' if p == 'GND' else 'power')
                continue
            category, function = FUNCTIONS.get(p, ('other', 'Entrada / saída livre'))
            if full and p in HDMI:
                function += ' / HDMI '+HDMI[p]
            bank = '1,8 V' if 79 <= p <= 86 else '3,3 V'
            # Cada linha é lida da placa para fora: pino → porta → uso → tensão.
            cells = [(100, str(p), 'pin'), (200, PORTS[p] if full else 'E/S', 'gpio'),
                     (590, function, category), (140, bank, 'bank18' if bank == '1,8 V' else 'other')]
            if side == 'left':
                cells = list(reversed(cells))
            for w, label, color in cells:
                s.box(x, y, w, 45, label, color, 21 if len(label)>23 else 23)
                x += w+8
    s.footer([
        'CORES: vermelho = alimentação · preto = terra · ciano = pino físico · amarelo = porta · laranja = vídeo · roxo = SPI.',
        'E/S = entrada/saída. Funções são ligações da placa; o circuito programado define a direção e o uso de cada sinal.',
        '79–86: banco de 1,8 V. Demais sinais destes headers: 3,3 V. Não aplicar 5 V aos sinais.',
        'RGB e HDMI compartilham sinais; RGB = vermelho/verde/azul. Confira o esquema antes de usar simultaneamente.',
        'Fonte: esquema Tang_Nano_9k_3672, folha GW1NR 9K, e mapa de pinos oficiais Sipeed.'])
    s.save(f'tangnano9k-pinout-{"full" if full else "simple"}.png')


def lcd(full=False):
    s = Sheet(1950 if full else 1250, 'LCD RGB 4,3″ · ' + ('PORTA RGB DE 40 VIAS' if full else 'CONEXÕES PRINCIPAIS'),
              '480 × 272 pixels no anúncio · referência da porta J4 da Tang Nano 9K · código do painel ainda não confirmado')
    if full:
        for i, (name, signal) in enumerate(LCD_PORT):
            x, y = (60 if i < 20 else 1450), 230+(i%20)*64
            s.box(x, y, 90, 48, str(i+1), 'pin')
            category = 'ground' if name == 'GND' else 'power' if name in ('VCC', 'LEDA', 'LEDK') else 'rgb'
            s.box(x+102, y, 190, 48, name, category)
            s.box(x+304, y, 980, 48, signal, 'other')
    else:
        s.d.rounded_rectangle((1040, 255, 1800, 780), 16, fill='#c7cbca', outline='#666666', width=3)
        s.d.rectangle((1080, 295, 1760, 730), fill='#182b28')
        s.text((1420, 475), '480 × 272', 58, '#ffffff', True, 'mm')
        s.text((1420, 565), '4,3 polegadas', 31, '#ffffff', anchor='mm')
        rows = [('VERMELHO · 5 bits', 'FPGA 75, 74, 73, 72, 71', 'rgb'),
                ('VERDE · 6 bits', 'FPGA 70, 69, 68, 57, 56, 55', 'data'),
                ('AZUL · 5 bits', 'FPGA 54, 53, 51, 42, 41', 'control'),
                ('CLOCK DOS PIXELS', 'FPGA 35', 'clock'),
                ('HSYNC · VSYNC · DE', 'FPGA 40 · 34 · 33', 'clock')]
        for i, (label, signal, color) in enumerate(rows):
            y = 275+i*105
            s.box(60, y, 880, 64, label, color, 27)
            s.box(1870, y, 870, 64, signal, color, 24)
            s.d.line((940, y+32, 1040, y+32), fill='#888888', width=2)
            s.d.line((1800, y+32, 1870, y+32), fill='#888888', width=2)
        s.box(1040, 810, 760, 74, 'CABO FLEXÍVEL · PORTA RGB', 'rgb', 28)
    s.footer([
        'A folha completa numera a PORTA DA PLACA, não confirma o pinout do painel comprado. Pino 1 e face dos contatos exigem conferência.',
        'Luz de fundo: usar o circuito da placa. DISP está em 3,3 V; XR/YD/XL/YU são sinais RGB_INIT do esquema; toque não confirmado.',
        'RGB565 = 5 bits vermelhos + 6 verdes + 5 azuis. HSYNC/VSYNC = sincronismo horizontal/vertical; DE = dados válidos.',
        'Fontes: esquema oficial Sipeed, porta J4, e exemplo lcd_4.3/src/Tang_nano_9K_LCD.cst.'])
    s.save(f'lcd43-connections-{"full" if full else "simple"}.png')


def camera(full=False):
    s = Sheet(1580 if full else 1250, 'CÂMERA WEACT M12 · ' + ('SINAIS DA H743' if full else 'CONEXÕES PRINCIPAIS'),
              'Kit H743-LCD-M12 · sensor a confirmar · M12 descreve a lente, não o sensor nem sua resolução')
    if full:
        for i, (signal, gpio, color) in enumerate(CAMERA_SIGNALS):
            y = 235+i*65
            s.box(60, y, 750, 49, signal, color, 28)
            s.box(850, y, 850, 49, gpio, 'gpio', 27)
            explanation = 'Pixels da câmera → H743' if color == 'data' else 'Controle / configuração' if color == 'control' else 'Sincronismo / referência de tempo'
            s.box(1740, y, 1000, 49, explanation, color, 24)
    else:
        s.d.rounded_rectangle((1130, 280, 1650, 800), 28, fill='#303030')
        s.d.ellipse((1190, 335, 1590, 735), fill='#171c1c', outline='#777777', width=10)
        s.d.ellipse((1280, 425, 1500, 645), fill='#263d42', outline='#687d81', width=8)
        s.text((1390, 765), 'M12 · sensor a confirmar', 24, '#ffffff', anchor='mm')
        for i, (label, detail, color) in enumerate([
            ('DADOS · D0–D7', '8 sinais de pixels → H743', 'data'),
            ('SINCRONISMO', 'HSYNC · VSYNC · PIXCLK', 'clock'),
            ('CLOCK DO SENSOR', 'XCLK vindo da H743', 'clock'),
            ('CONFIGURAÇÃO', 'SCL · SDA · controle PWDN', 'control'),
            ('ALIMENTAÇÃO', 'Pela porta de câmera WeAct', 'power')]):
            y = 290+i*98
            s.box(60, y, 990, 64, label, color, 27)
            s.box(1740, y, 1000, 64, detail, color, 25)
            s.d.line((1050, y+32, 1130, y+32), fill='#888888', width=2)
            s.d.line((1650, y+32, 1740, y+32), fill='#888888', width=2)
    s.footer([
        'Referência lógica da porta da H743. Sem números de contato do módulo: sensor e revisão ainda não identificados.',
        'DVP = porta de vídeo digital paralelo; DCMI = interface de câmera digital do STM32; SCCB = barramento de configuração.',
        'SCL/SDA = clock/dados de controle; XCLK = clock para o sensor; PIXCLK = clock dos pixels; PWDN = controle de repouso.',
        'Fonte: esquema WeAct MiniSTM32H7xx V1.2. Não aplicar 5 V nos sinais; conferir orientação do cabo e a ponte SB1.'])
    s.save(f'camera-m12-connections-{"full" if full else "simple"}.png')


if __name__ == '__main__':
    for generate in (tang, lcd, camera):
        generate()
        generate(True)

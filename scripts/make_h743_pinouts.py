"""Gera as pinagens da WeAct MiniSTM32H743 (placa H743VIT6) no estilo das folhas da H7R3.

Uso: python3 scripts/make_h743_pinouts.py        (requer Poppler e Google Chrome/Chromium)

Dados:
- funções alternativas AF0–AF15: tabelas 10–14 e 17 do DS12110 Rev 7 (assets/documents/stm32h743vi.pdf),
  lidas pelas coordenadas das palavras (pdftotext -bbox);
- número do pino LQFP100, estrutura de E/S e funções adicionais: tabela 9 do mesmo datasheet;
- headers P1/P2 e ligações da placa: esquema WeAct STM32H7xx V1.2 (assets/documents/h743-schematic.pdf).

Saída: assets/pinouts/h743-pinout-*.png (sete imagens; ver docs/H743-PINOUT.md).
"""
from __future__ import annotations

import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None  # a visão geral completa passa de 100 milhões de pixels

ROOT = Path(__file__).resolve().parents[1]
DATASHEET = ROOT / 'assets/documents/stm32h743vi.pdf'
OUT = ROOT / 'assets/pinouts'
DATE = '2026-09-17'

# ---------------------------------------------------------------- dados do datasheet

def words(page: int) -> list[tuple[float, float, float, float, str]]:
    out = subprocess.check_output(['pdftotext', '-f', str(page), '-l', str(page), '-bbox', str(DATASHEET), '-']).decode()
    return [(float(a), float(b), float(c), float(d), html.unescape(t)) for a, b, c, d, t in
            re.findall(r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)<', out)]


def cells(ws, gap=9.5):
    """Agrupa palavras de uma coluna em células: linhas próximas (quebra de nome) formam uma célula."""
    lines = []
    for w in sorted(ws, key=lambda w: (round(w[1]), w[0])):
        if lines and abs(lines[-1][0] - w[1]) < 2:
            lines[-1][1].append(w)
        else:
            lines.append([w[1], [w]])
    groups = []
    for y, line in lines:
        if groups and y - groups[-1][-1][0] < gap:
            groups[-1].append((y, line))
        else:
            groups.append([(y, line)])
    return [((g[0][0] + g[-1][0]) / 2, ''.join(''.join(w[4] for w in sorted(l, key=lambda w: w[0])) for _, l in g))
            for g in groups]


def alternate_functions() -> dict[str, list[str]]:
    """Tabelas 10–18: cada página pode ter mais de uma tabela; cada tabela repete o cabeçalho AF0…AF15."""
    table = {}
    for page in range(89, 102):
        ws = words(page)
        heads = sorted(w for w in ws if w[4] == 'AF0')
        for i, head in enumerate(heads):
            y1 = heads[i + 1][1] if i + 1 < len(heads) else 1e9
            seg = [w for w in ws if head[1] - 3 <= w[1] < y1 - 3]
            xs = {int(w[4][2:]): (w[0] + w[2]) / 2 for w in seg if re.fullmatch(r'AF\d+', w[4]) and abs(w[1] - head[1]) < 3}
            if len(xs) < 16:
                continue
            x = [xs[n] for n in range(16)]
            bounds = [x[0] - (x[1] - x[0]) / 2] + [(x[n] + x[n + 1]) / 2 for n in range(15)] + [x[15] + (x[15] - x[14]) / 2]
            pins = [(w[1], w[4]) for w in seg if re.fullmatch(r'P[A-K]\d+', w[4]) and w[0] < bounds[0]]
            if not pins:
                continue
            # A última linha do cabeçalho (…SPDIFRX1 / ETH) fica logo acima da primeira linha de pinos.
            first = min(p[0] for p in pins)
            top = max([first - 25] + [w[1] + 3 for w in seg if w[4] in ('ETH', 'SPDIFRX1') and w[1] < first])
            rows = {name: [''] * 16 for _, name in pins}
            for n in range(16):
                col = [w for w in seg if bounds[n] <= (w[0] + w[2]) / 2 < bounds[n + 1] and w[1] > top
                       and not re.fullmatch(r'\d+/357|DS12110|Rev|7', w[4])]
                for y, text in cells(col):
                    near = min(pins, key=lambda p: abs(p[0] - y))
                    if abs(near[0] - y) < 30 and text != '-':
                        rows[near[1]][n] = text.replace('EVENT-OUT', 'EVENTOUT')
            table.update(rows)
    return table


def pin_definitions() -> dict[str, dict]:
    """Tabela 9: número LQFP100, estrutura de E/S e funções adicionais de cada pino do encapsulamento."""
    pins = {}
    for page in range(64, 88):
        ws = [w for w in words(page) if 185 < w[1] < 740]
        ys = sorted({round(w[1], 1) for w in ws if 303 < w[0] < 318 and w[4] in ('I/O', 'S', 'I', 'O', '-')})

        def column(x0, x1):
            found = {}
            lines = {}
            for w in sorted((w for w in ws if x0 <= w[0] < x1), key=lambda w: (round(w[1]), w[0])):
                lines.setdefault(round(w[1]), []).append(w[4])
            for y, parts in lines.items():
                anchor = min(ys, key=lambda v: abs(v - y))
                if abs(anchor - y) < 40:
                    found.setdefault(anchor, []).append(''.join(parts))
            return found

        number, name, io, extra = column(60, 88), column(255, 303), column(328, 356), column(468, 560)
        for y in ys:
            lqfp = ''.join(number.get(y, []))
            if not lqfp.isdigit():
                continue
            label = ''.join(name.get(y, []))
            key = re.match(r'(P[A-K]\d+(?:_C)?|[A-Z+]+[A-Z0-9+]*)', label).group(1)
            add = ''.join(extra.get(y, []))
            pins[key] = dict(lqfp=int(lqfp), io=''.join(io.get(y, [])),
                             add=[] if add in ('', '-') else [a for a in re.split(r',', add) if a and a != '-'])
    # Linhas que a leitura por coordenadas não separa (conferidas na página 64-66 do DS12110 Rev 7).
    pins['PC13'] = dict(lqfp=7, io='FT', add=['RTC_TAMP1/RTC_TS/WKUP2'])
    pins['PC2_C'] = dict(lqfp=17, io='TT_a', add=['ADC3_INN1', 'ADC3_INP0'])
    pins['PC3_C'] = dict(lqfp=18, io='TT_a', add=['ADC3_INP1'])
    pins.pop('PC2', None)
    pins.pop('PC3', None)
    return pins


# ---------------------------------------------------------------- placa (esquema WeAct STM32H7xx V1.2)

P1 = ['GND', '5V', 'PE1', 'PE0', 'PB9', 'PB8', 'PB7', 'PB6', 'PB5', 'PB4', 'PB3', 'PD7', 'PD6', 'PD5', 'PD4', 'PD3',
      'PD2', 'PD1', 'PD0', 'PC12', 'PC11', 'PC10', 'PA15', 'PA12', 'PA11', 'PA10', 'PA9', 'PA8', 'PC9', 'PC8', 'PC7',
      'PC6', 'PD15', 'PD14', 'PD13', 'PD12', 'PD11', 'PD10', 'PD9', 'PD8', 'PB15', 'PB14', 'PB13', 'PB12']
P2 = ['GND', '3V3', 'PE2', 'PE3', 'PE4', 'PE5', 'PE6', 'VBAT', 'PC13', 'NRST', 'PC0', 'PC1', 'PC2_C', 'PC3_C', 'GND',
      'VREF+', 'PA0', 'PA1', 'PA2', 'PA3', 'PA4', 'PA5', 'PA6', 'PA7', 'PC4', 'PC5', 'PB0', 'PB1', 'PB2', 'PE7', 'PE8',
      'PE9', 'PE10', 'PE11', 'PE12', 'PE13', 'PE14', 'PE15', 'PB10', 'PB11', '3V3', '5V', 'GND', 'GND']
OFF_HEADER = ['PA13', 'PA14', 'PC14', 'PC15', 'PH0', 'PH1', 'BOOT0']

# Uso na placa: (texto curto, grupo). Pontes SB1–SB3 aparecem fechadas no esquema; SB4/SB5 abertas.
BOARD = {
    'PE10': ('LCD · luz de fundo', 'cam'), 'PE11': ('LCD · CS', 'cam'), 'PE12': ('LCD · SCK', 'cam'),
    'PE13': ('LCD · DC (WR_RS)', 'cam'), 'PE14': ('LCD · SDA', 'cam'),
    'PC6': ('câmera · D0', 'cam'), 'PC7': ('câmera · D1', 'cam'), 'PE0': ('câmera · D2', 'cam'),
    'PE1': ('câmera · D3', 'cam'), 'PE4': ('câmera · D4', 'cam'), 'PD3': ('câmera · D5', 'cam'),
    'PE5': ('câmera · D6', 'cam'), 'PE6': ('câmera · D7', 'cam'), 'PB7': ('câmera · VSYNC', 'cam'),
    'PA4': ('câmera · HSYNC', 'cam'), 'PA6': ('câmera · PIXCLK', 'cam'), 'PA8': ('câmera · XCLK (MCO1)', 'cam'),
    'PB8': ('câmera · SCL', 'cam'), 'PB9': ('câmera · SDA', 'cam'), 'PA7': ('câmera · PWDN (SB1)', 'cam'),
    'PC8': ('microSD · D0', 'mem'), 'PC9': ('microSD · D1', 'mem'), 'PC10': ('microSD · D2', 'mem'),
    'PC11': ('microSD · D3', 'mem'), 'PC12': ('microSD · CLK', 'mem'), 'PD2': ('microSD · CMD', 'mem'),
    'PD4': ('microSD · detecção (SB2)', 'mem'),
    'PD11': ('flash QSPI · IO0', 'mem'), 'PD12': ('flash QSPI · IO1', 'mem'), 'PE2': ('flash QSPI · IO2', 'mem'),
    'PD13': ('flash QSPI · IO3', 'mem'), 'PB2': ('flash QSPI · CLK', 'mem'), 'PB6': ('flash QSPI · CS', 'mem'),
    'PB3': ('flash SPI · SCK', 'mem'), 'PB4': ('flash SPI · MISO', 'mem'), 'PD7': ('flash SPI · MOSI', 'mem'),
    'PD6': ('flash SPI · CS (SB3)', 'mem'),
    'PA11': ('USB · D−', 'usb'), 'PA12': ('USB · D+', 'usb'),
    'PE3': ('LED azul E3', 'board'), 'PC13': ('botão K1', 'board'),
    'PA13': ('SWD · DIO', 'sys'), 'PA14': ('SWD · CLK', 'sys'), 'PC14': ('cristal 32,768 kHz', 'sys'),
    'PC15': ('cristal 32,768 kHz', 'sys'), 'PH0': ('cristal 25 MHz', 'sys'), 'PH1': ('cristal 25 MHz', 'sys'),
    'BOOT0': ('botão B0', 'sys'),
}

POWER = {
    'GND': ('GROUND', 'gnd', 'G'),
    '5V': ('5V · ENTRADA 3,3–5,5 V (USB via diodo B5819)', 'pwr', '5V'),
    '3V3': ('3V3 · SAÍDA DO REGULADOR DC-DC (1 A)', 'pwr', '3V3'),
    'VBAT': ('VBAT DO RTC (BAT54C com o 3V3)', 'plain', 'VB'),
    'NRST': ('RESET · ativo em baixo · botão NR (MAX809)', 'plain', 'NR'),
    'VREF+': ('VREF+ DO ADC (R9 0 Ω → 3V3)', 'plain', 'V+'),
}

# ---------------------------------------------------------------- classificação das funções

GROUPS = [  # id, rótulo, cor forte, cor clara
    ('ana', 'Analógico', '#2fbf3a', '#e6f7e7'), ('tim', 'Timers', '#e0504a', '#fde8e7'),
    ('uart', 'UART', '#1f7fd1', '#e3f0fb'), ('spi', 'SPI · I²S', '#7a4fd6', '#efe8fb'),
    ('i2c', 'I²C · CEC', '#1a998f', '#e1f4f2'), ('can', 'CAN · USB · ETH', '#c2338f', '#fae6f2'),
    ('mem', 'Memória · SD', '#b8741a', '#fbeedb'), ('cam', 'Áudio · câmera · LCD', '#8a7a12', '#f6f1d4'),
    ('sys', 'Sistema', '#4b5563', '#eceef1'),
]
FILL = {'ana': '#43d94f', 'tim': '#f28b82', 'uart': '#3cb4e6', 'spi': '#a28ff2', 'i2c': '#bfe0f5', 'can': '#f28fdf',
        'usb': '#92e38b', 'eth': '#7fd6c4', 'mem': '#ffca7a', 'cam': '#ecd48f', 'sys': '#f4f4f4', 'board': '#ffffff'}


def group(name: str) -> str:
    rules = [('ana', r'^(ADC|DAC|COMP|OPAMP|VREF)'), ('tim', r'^(TIM|LPTIM|HRTIM)'),
             ('uart', r'^(USART|UART|LPUART|SWPMI)'), ('spi', r'^(SPI|I2S)'), ('i2c', r'^(I2C|CEC)'),
             ('can', r'^(FDCAN|OTG|ETH|MDIOS|CRS)'), ('mem', r'^(FMC|QUADSPI|SDMMC)'),
             ('cam', r'^(SAI|SPDIF|DCMI|DFSDM|LCD)')]
    for gid, pattern in rules:
        if re.match(pattern, name):
            return gid
    return 'sys'


def simple_fill(name: str) -> str:
    gid = group(name)
    if name.startswith('OTG'):
        return FILL['usb']
    if name.startswith(('ETH', 'MDIOS')):
        return FILL['eth']
    return FILL[gid]


class Pin:
    def __init__(self, name, af, info):
        self.name = name
        self.label = name
        base = name.removesuffix('_C')
        self.af = [(n, f) for n, f in enumerate(af.get(base, [''] * 16)) if f]
        self.lqfp = info.get(name, {}).get('lqfp')
        self.io = info.get(name, {}).get('io', '')
        self.add = info.get(name, {}).get('add', [])
        self.board = BOARD.get(name)

    @property
    def tolerance(self):
        if self.io.startswith('FT'):
            return '5V', 'tolerante a 5 V'
        if self.io.startswith('TT'):
            return '3V6', 'tolerante a 3,6 V'
        return '', ''

    def simple(self) -> list[str]:
        """Até três funções de grupos diferentes, na ordem de utilidade para protótipos."""
        analog = [a for a in self.add if a.startswith(('ADC', 'DAC'))]
        options = sorted(analog, key=lambda a: ('INN' in a, not a.startswith('DAC')))
        if self.name.endswith('_C'):
            return [a for a in options if 'INN' not in a][:2] + ['só analógico*']
        options += [f for _, f in self.af if not re.search(r'ULPI|FD_MODE|_COMP12|BKIN2', f)]
        order = ['ana', 'uart', 'spi', 'i2c', 'tim', 'can', 'mem', 'cam']
        chosen, used = [], set()
        for gid in order:
            for f in options:
                first = f.split('/')[0]
                if group(first) == gid and gid not in used and not first.startswith(('HRTIM', 'LPTIM', 'DFSDM', 'LCD', 'FMC_SD')):
                    chosen.append(first)
                    used.add(gid)
                    break
            if len(chosen) == 3:
                break
        return chosen


# ---------------------------------------------------------------- desenho da placa (mm, vista de cima)

W_MM, H_MM, PITCH = 40.64, 66.88, 2.54
ROW0 = (H_MM - 21 * PITCH) / 2  # 22 posições centralizadas
HOLE_X = {'L': (1.27, 3.81), 'R': (W_MM - 1.27, W_MM - 3.81)}  # (externa, interna)


def hole_y(position: int) -> float:
    return ROW0 + (position - 1) * PITCH


def silk(name: str) -> str:
    if name in POWER:
        return POWER[name][2]
    if name.endswith('_C'):
        return name[1:-2]
    return name[1:]


def board_svg(scale: float, highlight: str | None = None, labels: bool = True) -> str:
    s = scale
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W_MM * s:.1f}" height="{H_MM * s:.1f}" viewBox="0 0 {W_MM} {H_MM}">',
             '<defs><linearGradient id="usb" x1="0" x2="1"><stop offset="0" stop-color="#9aa0a8"/><stop offset=".5" stop-color="#e6e8eb"/>'
             '<stop offset="1" stop-color="#9aa0a8"/></linearGradient>'
             '<linearGradient id="sd" x1="0" x2="1"><stop offset="0" stop-color="#a7adb4"/><stop offset=".5" stop-color="#dfe2e6"/>'
             '<stop offset="1" stop-color="#a7adb4"/></linearGradient></defs>',
             f'<rect x=".15" y=".15" width="{W_MM - .3}" height="{H_MM - .3}" rx="2.2" fill="#15161a" stroke="#050506" stroke-width=".3"/>']
    for x in (2.75, W_MM - 2.75):
        for y in (2.75, H_MM - 2.75):
            parts.append(f'<circle cx="{x}" cy="{y}" r="2.1" fill="#c9a24a"/><circle cx="{x}" cy="{y}" r="1.55" fill="#f3f1ea"/>')
    if highlight:
        x0 = 0.25 if highlight == 'L' else W_MM - 5.3
        parts.append(f'<rect x="{x0}" y="{ROW0 - 1.6}" width="5.05" height="{21 * PITCH + 3.2}" rx=".8" fill="none" stroke="#f59e0b" stroke-width=".55"/>')
    # botões, LED E3, SWD
    parts.append('<text x="5.6" y="3.9" font-size="1.3" fill="#fff" font-family="DejaVu Sans" font-weight="bold">E3</text>'
                 '<rect x="7.9" y="2.9" width="1.2" height=".8" fill="#60a5fa"/>')
    for x, t in ((12.0, 'NR'), (15.8, 'B0'), (19.6, 'K1')):
        parts.append(f'<rect x="{x - 1.6}" y="3.9" width="3.2" height="3.2" rx=".3" fill="#d9d9d9"/><rect x="{x - 1.0}" y="4.3" width="2" height="2.4" rx="1" fill="#222"/>'
                     f'<text x="{x}" y="3.3" font-size="1.1" text-anchor="middle" fill="#fff" font-family="DejaVu Sans" font-weight="bold">{t}</text>')
    for i, t in enumerate(('GND', 'CLK', 'DIO', '3.3V')):
        x = 26.0 + i * PITCH
        shape = f'<rect x="{x - .75}" y="7.45" width="1.5" height="1.5" fill="#c9a24a"/>' if t == '3.3V' else f'<circle cx="{x}" cy="8.2" r=".78" fill="#c9a24a"/>'
        parts.append(shape + f'<circle cx="{x}" cy="8.2" r=".42" fill="#1b1b1b"/>'
                     f'<text x="{x}" y="6.6" font-size=".95" text-anchor="middle" fill="#fff" font-family="DejaVu Sans" font-weight="bold">{t}</text>')
    parts.append('<text x="29.8" y="5.1" font-size=".95" text-anchor="middle" fill="#fff" font-family="DejaVu Sans" font-weight="bold">SWD</text>')
    # TFT 0,96"
    parts.append('<rect x="6.6" y="10.0" width="28.2" height="13.2" rx=".4" fill="#050507" stroke="#3a3a44" stroke-width=".25"/>'
                 '<rect x="33.4" y="10.3" width="1.8" height="12.6" fill="#28306e"/>'
                 '<text x="20" y="17.4" font-size="1.7" text-anchor="middle" fill="#6b7280" font-family="DejaVu Sans" font-weight="bold">TFT 0,96″ · ST7735</text>')
    # MCU LQFP100
    parts.append('<rect x="12.5" y="26.0" width="16" height="16" fill="#9ca3af"/><rect x="13.5" y="27.0" width="14" height="14" rx=".3" fill="#2b2d31"/>'
                 '<circle cx="14.6" cy="28.1" r=".45" fill="#1b1c1f"/>'
                 '<text x="20.5" y="33.6" font-size="1.55" text-anchor="middle" fill="#d1d5db" font-family="DejaVu Sans" font-weight="bold">STM32H743</text>'
                 '<text x="20.5" y="35.6" font-size="1.15" text-anchor="middle" fill="#9ca3af" font-family="DejaVu Sans" font-weight="bold">VIT6 · LQFP100</text>')
    # PWR LED, SB2, microSD, USB-C
    parts.append('<rect x="28.2" y="52.3" width="1.2" height=".8" fill="#e11d48"/>'
                 '<text x="27.8" y="53.05" font-size=".95" text-anchor="end" fill="#fff" font-family="DejaVu Sans" font-weight="bold">PWR</text>'
                 '<text x="13.0" y="50.9" font-size=".95" fill="#fff" font-family="DejaVu Sans" font-weight="bold">SB2</text>'
                 f'<rect x="6.8" y="52.0" width="11.2" height="{H_MM - 52.0 - .2}" rx=".3" fill="url(#sd)" stroke="#6b7280" stroke-width=".15"/>'
                 '<text x="12.4" y="59.6" font-size="1.5" text-anchor="middle" fill="#6b7280" font-family="DejaVu Sans" font-weight="bold">microSD</text>'
                 f'<rect x="24.4" y="59.4" width="9" height="{H_MM - 59.4 + .6}" rx="1.2" fill="url(#usb)" stroke="#6b7280" stroke-width=".15"/>'
                 '<text x="28.9" y="63.2" font-size="1.3" text-anchor="middle" fill="#4b5563" font-family="DejaVu Sans" font-weight="bold">USB-C</text>')
    # furos dos headers e serigrafia (a serigrafia real fica no verso; aqui é repetida para leitura)
    for side, names, parity in (('L', P2, 'even-out'), ('R', P1, 'odd-out')):
        xo, xi = HOLE_X[side]
        for pos in range(1, 23):
            y = hole_y(pos)
            odd, even = names[2 * pos - 2], names[2 * pos - 1]
            out, inn = (even, odd) if parity == 'even-out' else (odd, even)
            first = (side == 'L' and pos == 1, side == 'R' and pos == 1)
            for x, is_square in ((xo, first[1]), (xi, first[0])):
                if is_square:
                    parts.append(f'<rect x="{x - .85}" y="{y - .85}" width="1.7" height="1.7" fill="#c9a24a"/>')
                else:
                    parts.append(f'<circle cx="{x}" cy="{y}" r=".85" fill="#c9a24a"/>')
                parts.append(f'<circle cx="{x}" cy="{y}" r=".45" fill="#101010"/>')
            if labels and not (side == 'R' and pos == 1):  # o conector SWD ocupa a faixa ao lado
                text = f'{silk(out)} {silk(inn)}' if side == 'L' else f'{silk(inn)} {silk(out)}'
                w = len(text) * .68 + .5
                x = 5.0 if side == 'L' else W_MM - 5.0 - w
                parts.append(f'<rect x="{x:.2f}" y="{y - .85:.2f}" width="{w:.2f}" height="1.7" rx=".3" fill="#15161a" fill-opacity=".88"/>'
                             f'<text x="{x + .25:.2f}" y="{y + .42:.2f}" font-size="1.12" fill="#fff" font-family="DejaVu Sans Mono" font-weight="bold">{text}</text>')
    parts.append('</svg>')
    return ''.join(parts)


# ---------------------------------------------------------------- HTML comum

CSS_BASE = '''
*{box-sizing:border-box;margin:0;padding:0}
body{background:#fff;font-family:"DejaVu Sans",sans-serif;color:#1f2328;-webkit-font-smoothing:antialiased}
.page{padding:28px 30px 30px}
.top{display:flex;justify-content:space-between;gap:30px;border-bottom:2px solid #d0d4da;padding-bottom:16px;margin-bottom:22px}
h1{font-size:30px;font-weight:800;letter-spacing:.5px}
.tag{display:inline-block;background:#fcd34d;border-radius:5px;padding:3px 9px;font-size:22px;font-weight:800;margin:8px 0}
.lead{font-size:14px;font-weight:700;color:#444;max-width:780px;line-height:1.45}
.map{text-align:center;font-size:10.5px;font-weight:700;color:#555}
.map svg{display:block;margin:0 auto 5px}
.legend{display:flex;flex-wrap:wrap;gap:5px 6px;align-items:center;font-size:10.5px;font-weight:800;margin-top:18px;border-top:2px solid #d0d4da;padding-top:12px}
.legend b{margin-right:6px;font-size:12px}
.legend span{border:1px solid #888;border-radius:3px;padding:2px 6px}
.foot{font-size:11px;font-weight:700;color:#444;margin-top:10px;line-height:1.5}
'''

PIN_BOX = '#27c4e0'


def esc(text) -> str:
    return html.escape(str(text))


def simple_cells(pin_name: str, pins: dict, side: str, slot: str) -> str:
    """Uma linha da folha simples: uso na placa, 3 funções, nome e caixa do pino (ordem espelhada no lado direito)."""
    if pin_name in POWER:
        text, kind, short = POWER[pin_name]
        bg, fg = {'gnd': ('#111', '#fff'), 'pwr': ('#ff1f1f', '#111'), 'plain': ('#f4f4f4', '#111')}[kind]
        wide = f'<div class="c wide" style="background:{bg};color:{fg}">{esc(text)}</div>'
        name = f'<div class="c gpio" style="background:{bg};color:{fg}">{esc(short if kind != "plain" else pin_name)}</div>'
        box = f'<div class="c box">–<small>{esc(slot)}</small></div>'
        items = [wide, name, box]
    else:
        pin = pins[pin_name]
        funcs = pin.simple()
        fn = [f'<div class="c fn" style="background:{simple_fill(f)}">{esc(f)}</div>' for f in funcs]
        fn += ['<div class="c fn empty"></div>'] * (3 - len(fn))
        board = (f'<div class="c use">{esc(pin.board[0])}</div>' if pin.board else '<div class="c use empty"></div>')
        name = f'<div class="c gpio">{esc(pin.label)}</div>'
        box = f'<div class="c box">{pin.lqfp}<small>{esc(slot)}</small></div>'
        items = [board] + list(reversed(fn)) + [name, box]
    if side == 'R':
        items = list(reversed(items))
    return ''.join(items)


SIMPLE_CSS = '''
.rows{position:relative}
.row{position:absolute;display:flex;gap:4px;height:26px}
.c{height:26px;border:1px solid #555;border-radius:3px;display:flex;align-items:center;justify-content:center;
   font-size:11.5px;font-weight:800;white-space:nowrap;overflow:hidden}
.fn{width:132px}.fn.empty{border-color:transparent}
.use{width:176px;background:#fff;border:1.5px solid #333}.use.empty{border-color:transparent}
.wide{width:{wide}px}
.gpio{width:62px;background:#fff3a0;font-size:14px}
.box{width:56px;background:''' + PIN_BOX + ''';flex-direction:column;line-height:1;font-size:13px}
.box small{font-size:8px;margin-top:1px}
.wire{position:absolute;left:0;top:0;overflow:visible}
'''


def position_rows(names: list[str], side: str) -> list[tuple[int, str, str]]:
    """(posição, sinal externo, sinal interno) na ordem física, de cima (display) para baixo (USB-C)."""
    connector = 'P2' if side == 'L' else 'P1'
    result = []
    for pos in range(1, 23):
        odd = (names[2 * pos - 2], f'{connector}-{2 * pos - 1}')
        even = (names[2 * pos - 1], f'{connector}-{2 * pos}')
        result.append((pos, even, odd) if side == 'L' else (pos, odd, even))
    return result


def simple_side_block(names, side, pins, scale, board_x, top):
    """Linhas de uma lateral, alinhadas aos furos, com fios até o furo correto."""
    row_h = PITCH * scale / 2
    rows, wires = [], []
    xo, xi = HOLE_X[side]
    for pos, out, inn in position_rows(names, side):
        hy = top + hole_y(pos) * scale
        for k, (name, slot) in enumerate((out, inn)):
            y = hy - row_h + k * row_h + 1.5
            rows.append((y, name, slot))
            hole_x = board_x + (xo if k == 0 else xi) * scale
            cy = y + 13
            if side == 'L':
                edge = board_x - 14
                if k == 0:
                    wires.append(f'M{edge - 20} {cy} H{edge} L{hole_x} {hy}')
                else:
                    gap = hy + row_h * .95
                    wires.append(f'M{edge - 20} {cy} H{edge} L{board_x + 2.54 * scale} {gap} L{hole_x} {hy}')
            else:
                edge = board_x + W_MM * scale + 14
                if k == 0:
                    wires.append(f'M{edge + 20} {cy} H{edge} L{hole_x} {hy}')
                else:
                    gap = hy + row_h * .95
                    wires.append(f'M{edge + 20} {cy} H{edge} L{board_x + (W_MM - 2.54) * scale} {gap} L{hole_x} {hy}')
    return rows, wires


# ---------------------------------------------------------------- folhas simples

def simple_sheet(side: str, pins: dict) -> str:
    scale = 22.9  # px por mm: 2,54 mm = 58 px = duas linhas de 29 px
    names = P2 if side == 'L' else P1
    visible = 13.5  # mm da placa mostrados na folha
    row_w = 176 + 3 * 132 + 62 + 56 + 5 * 4
    wide = 176 + 3 * 132 + 3 * 4
    top = 20
    width = 1400
    if side == 'L':
        row_x = 30
        board_x = row_x + row_w + 60
        clip = (board_x - 4, board_x + visible * scale)
    else:
        board_x = 30 + visible * scale - W_MM * scale
        row_x = board_x + W_MM * scale + 60
        clip = (30, 30 + visible * scale + 4)
    rows, wires = simple_side_block(names, side, pins, scale, board_x, top)
    body = []
    for y, name, slot in rows:
        body.append(f'<div class="row" style="left:{row_x}px;top:{y:.1f}px">{simple_cells(name, pins, side, slot)}</div>')
    height = H_MM * scale + 2 * top
    paths = ''.join(f'<path d="{d}"/>' for d in wires)
    title = 'HEADER ESQUERDO · P2' if side == 'L' else 'HEADER DIREITO · P1'
    parity = ('fileira externa (borda) = pinos pares; interna = ímpares' if side == 'L'
              else 'fileira externa (borda) = pinos ímpares; interna = pares')
    other = 'O header direito (P1) está na outra folha.' if side == 'L' else 'O header esquerdo (P2) está na outra folha.'
    n = '1/2' if side == 'L' else '2/2'
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS_BASE}{SIMPLE_CSS.replace('{wide}', str(wide))}
.clip{{position:absolute;top:{top}px;left:{clip[0]:.1f}px;width:{clip[1] - clip[0]:.1f}px;height:{H_MM * scale:.1f}px;overflow:hidden;
  {'-webkit-mask-image:linear-gradient(90deg,#000 80%,transparent)' if side == 'L' else '-webkit-mask-image:linear-gradient(270deg,#000 80%,transparent)'}}}
.clip svg{{position:absolute;left:{board_x - clip[0]:.1f}px;top:0}}
.wire path{{fill:none;stroke:#222;stroke-width:3;stroke-linejoin:round}}
</style></head><body><div class="page" style="width:{width}px">
<div class="top"><div><h1>WEACT STM32H743 · PINOUT SIMPLES · {n}</h1><div class="tag">{title}</div>
<p class="lead">Vista de cima, display no topo e USB-C embaixo · {parity}. Cada posição tem 2 furos:
linha de cima = externo (borda), linha de baixo = interno. Caixa azul: número do pino no CI (LQFP100) e pino do header. {other}</p></div>
<div class="map">{board_svg(4.2, side, labels=False)}display no topo · lado em amarelo</div></div>
<div class="rows" style="height:{height:.0f}px">
<div class="clip">{board_svg(scale)}</div>
<svg class="wire" width="{width}" height="{height:.0f}">{paths}</svg>
{''.join(body)}</div>
{legend_simple()}
<p class="foot">Placa: LCD ST7735 em PE10–PE14 (SPI4) · câmera DCMI em PA4/PA6/PA8/PB7–PB9/PC6/PC7/PD3/PE0/PE1/PE4–PE6 ·
microSD PC8–PC12, PD2 (detecção PD4) · flash QSPI PB2/PB6/PD11–PD13/PE2 · flash SPI PB3/PB4/PD6/PD7 · USB PA11/PA12 · LED azul PE3 · botão K1 PC13.
PC2_C/PC3_C: entradas analógicas diretas; as funções digitais de PC2/PC3 exigem fechar a chave analógica (SYSCFG_PMCR).
Três funções principais por pino; a lista completa está na versão completa. Fonte: ST DS12110 Rev 7 (tabelas 9–14) e esquema WeAct STM32H7xx V1.2.</p>
</div></body></html>'''


def legend_simple() -> str:
    items = [('POWER', '#ff1f1f', '#111'), ('GROUND', '#111', '#fff'), ('PINO DO CI', PIN_BOX, '#111'), ('NOME GPIO', '#fff3a0', '#111'),
             ('ANALÓGICO', FILL['ana'], '#111'), ('TIMER', FILL['tim'], '#111'), ('USART/UART', FILL['uart'], '#111'),
             ('SPI/I2S', FILL['spi'], '#111'), ('I2C/CEC', FILL['i2c'], '#111'), ('FDCAN', FILL['can'], '#111'),
             ('USB', FILL['usb'], '#111'), ('ETHERNET', FILL['eth'], '#111'), ('MEMÓRIA/SD', FILL['mem'], '#111'),
             ('ÁUDIO/CÂMERA/LCD', FILL['cam'], '#111'), ('SISTEMA', FILL['sys'], '#111'), ('USO NA PLACA', '#fff', '#111')]
    return '<div class="legend"><b>LEGENDA</b>' + ''.join(f'<span style="background:{b};color:{c}">{t}</span>' for t, b, c in items) + '</div>'


# ---------------------------------------------------------------- visão geral simples (placa inteira)

def simple_overview(pins: dict) -> str:
    scale = 22.9
    row_w = 176 + 3 * 132 + 62 + 56 + 5 * 4
    wide = 176 + 3 * 132 + 3 * 4
    left_x = 30
    board_x = left_x + row_w + 70
    right_x = board_x + W_MM * scale + 70
    width = right_x + row_w + 30
    top = 20
    rows_l, wires_l = simple_side_block(P2, 'L', pins, scale, board_x, top)
    rows_r, wires_r = simple_side_block(P1, 'R', pins, scale, board_x, top)
    body = [f'<div class="row" style="left:{left_x}px;top:{y:.1f}px">{simple_cells(n, pins, "L", t)}</div>' for y, n, t in rows_l]
    body += [f'<div class="row" style="left:{right_x:.1f}px;top:{y:.1f}px">{simple_cells(n, pins, "R", t)}</div>' for y, n, t in rows_r]
    height = H_MM * scale + 2 * top
    paths = ''.join(f'<path d="{d}"/>' for d in wires_l + wires_r)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS_BASE}{SIMPLE_CSS.replace('{wide}', str(wide))}
.brd{{position:absolute;top:{top}px;left:{board_x:.1f}px}}
.wire path{{fill:none;stroke:#222;stroke-width:3;stroke-linejoin:round}}
.sw{{position:absolute;right:30px;top:24px;border:1px solid #bbb;border-radius:6px;padding:8px 12px;font-size:12px;font-weight:700;background:#f4f4f4}}
</style></head><body><div class="page" style="width:{width:.0f}px;position:relative">
<h1>WEACT STUDIO STM32H743 CORE BOARD (MiniSTM32H7xx V1.2)</h1>
<p class="lead" style="max-width:none">Pinout vertical para leitura humana · STM32H743VIT6 · LQFP100 (pinos 1–100) · display no topo, USB-C embaixo · headers 2 × 22 ·
esquerdo = P2, direito = P1</p>
<div class="sw">DEBUG / SWD · conector de 4 furos no topo<br>3.3V · DIO = PA13 (pino 72) · CLK = PA14 (pino 76) · GND</div>
<div class="rows" style="height:{height:.0f}px;margin-top:18px">
<div class="brd">{board_svg(scale)}</div>
<svg class="wire" width="{width:.0f}" height="{height:.0f}">{paths}</svg>
{''.join(body)}</div>
{legend_simple()}
<p class="foot">Cada posição do header tem dois furos: a linha de cima de cada par é a fileira externa (borda da placa) e a de baixo é a interna.
Esquerdo (P2): externa = pares · direito (P1): externa = ímpares. Pino do CI = número do LQFP100 (tabela 9 do DS12110).<br>
Recursos da placa: TFT 0,96″ ST7735 (SPI4: PE12 SCK, PE14 SDA, PE13 DC, PE11 CS, PE10 luz) · câmera DVP de 24 vias (DCMI) · microSD (SDMMC1) ·
flash QSPI 8 MB (PY25Q64HA) · flash SPI 8 MB (SPI1, CS PD6 via SB3) · LED azul PE3 · K1 em PC13 (liga ao 3V3) · cristais 25 MHz e 32,768 kHz.<br>
Cuidados: vários pinos do header já estão ligados a LCD, câmera, microSD e flashes — confira a coluna "uso na placa" antes de usar como GPIO livre.
PA13/PA14 (SWD), PA15, PB3 e PB4 saem do reset em função JTAG · PC13–PC15 só drenam ~3 mA (≤ 2 MHz).</p>
</div></body></html>'''


# ---------------------------------------------------------------- folhas completas

FULL_CSS = '''
body{font-family:"DejaVu Sans Condensed","DejaVu Sans",sans-serif;background:#f7f6f3}
.kicker{font-size:13px;letter-spacing:2px;font-weight:700;color:#666}
h1{font-size:36px}
.lead{font-weight:400;font-size:15px;color:#333;max-width:900px}
.cols{display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-size:12px;font-weight:700;margin:4px 0 12px}
.cols .g{border:1.5px solid;border-radius:4px;padding:2px 7px;background:#fff}
.pos{background:#fff;border:1px solid #d6d6d6;border-radius:8px;margin-bottom:8px;padding:6px 10px 6px}
.pos h3{font-size:11px;letter-spacing:1.5px;color:#666;margin-bottom:3px}
.line{display:flex;align-items:flex-start;gap:8px;padding:4px 0}
.line+.line{border-top:1px dashed #ddd}
.side{writing-mode:vertical-rl;transform:rotate(180deg);font-size:9px;font-weight:800;letter-spacing:1px;width:12px;text-align:center}
.side.ext{color:#b45309}.side.int{color:#1d4ed8}
.pb{width:58px;height:34px;border:1.5px solid #111;border-radius:5px;background:#fff;display:flex;flex-direction:column;align-items:center;
    justify-content:center;font-size:15px;font-weight:800;line-height:1;flex:none}
.pb small{font-size:8.5px;color:#555;margin-top:2px}
.nm{width:94px;min-height:34px;border-radius:5px;background:#16181c;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;
    font-size:19px;font-weight:800;flex:none;line-height:1.05;padding:2px 0}
.nm small{font-size:8.5px;background:#fcd34d;color:#111;border-radius:3px;padding:1px 4px;margin-top:2px;white-space:nowrap}
.tol{width:34px;height:34px;border:1px solid #9bd3a6;background:#e9f7ec;color:#1f7a32;border-radius:4px;font-size:11px;font-weight:800;
     display:flex;flex-direction:column;align-items:center;justify-content:center;flex:none;line-height:1}
.tol small{font-size:7.5px;font-weight:600}
.tol.tt{border-color:#e7c07b;background:#fdf3df;color:#8a5a00}
.tol.none{visibility:hidden}
.chips{display:flex;flex-wrap:wrap;gap:4px;flex:1;align-items:center;min-height:34px}
.chip{display:inline-flex;align-items:center;border:1.5px solid;border-radius:4px;background:#fff;font-size:13px;font-weight:700;height:24px;padding-left:6px;white-space:nowrap}
.chip i{font-style:normal;color:#fff;font-size:10.5px;height:100%;display:flex;align-items:center;padding:0 4px;margin-left:5px}
.chip.add{border-style:dashed;padding-right:6px}
.bar{flex:1;height:34px;border-radius:5px;display:flex;align-items:center;padding-left:14px;font-size:17px;font-weight:800}
.none-af{font-size:11px;color:#777;font-weight:600}
.notes{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px}
.note{background:#fff;border:1px solid #d6d6d6;border-radius:8px;padding:10px 14px;font-size:12.5px;line-height:1.55}
.note h4{font-size:11px;letter-spacing:1.5px;color:#666;margin-bottom:4px}
.note li{margin-left:16px}
.note code{font-family:"DejaVu Sans Mono";font-size:11px;background:#f1f1f1;padding:0 3px;border-radius:2px}
'''


def chip(name: str, af: int | None) -> str:
    gid = group(name)
    strong = next(g[2] for g in GROUPS if g[0] == gid)
    if af is None:
        return f'<span class="chip add" style="border-color:{strong};color:{strong}">{esc(name)}</span>'
    return f'<span class="chip" style="border-color:{strong};color:{strong}">{esc(name)}<i style="background:{strong}">{af}</i></span>'


def full_line(name: str, pins: dict, label: tuple | None, slot: str = '') -> str:
    side = f'<div class="side {label[0]}">{label[1]}</div>' if label else ''
    if name in POWER:
        text, kind, short = POWER[name]
        bg, fg = {'gnd': ('#2a2d33', '#fff'), 'pwr': ('#d7263d', '#fff'), 'plain': ('#eceef1', '#111')}[kind]
        bar_bg = {'gnd': '#2a2d33', 'pwr': '#fde2e6', 'plain': '#f3f4f6'}[kind]
        bar_fg = {'gnd': '#fff', 'pwr': '#b3172d', 'plain': '#333'}[kind]
        return (f'<div class="line">{side}<div class="pb">–<small>{esc(slot)}</small></div>'
                f'<div class="nm" style="background:{bg};color:{fg}">{esc(short if kind != "plain" else name)}</div>'
                f'<div class="tol none"></div><div class="bar" style="background:{bar_bg};color:{bar_fg}">{esc(text)}</div></div>')
    pin = pins[name]
    tol, tol_text = pin.tolerance
    cls = 'tol' + (' tt' if tol == '3V6' else '') + ('' if tol else ' none')
    tol_html = f'<div class="{cls}">{tol}<small>{esc(pin.io)}</small></div>'
    chips = ''.join(chip(f, n) for n, f in pin.af) + ''.join(chip(a, None) for a in pin.add)
    if pin.name.endswith('_C'):
        chips = '<span class="chip add" style="border-color:#4b5563;color:#4b5563">AF de ' + pin.name[:-2] + ' só com a chave analógica fechada</span>' + chips
    board = f'<small>{esc(pin.board[0])}</small>' if pin.board else ''
    number = pin.lqfp if pin.lqfp else '–'
    return (f'<div class="line">{side}<div class="pb">{number}<small>{esc(slot) or "fora"}</small></div>'
            f'<div class="nm">{esc(pin.label)}{board}</div>{tol_html}<div class="chips">{chips or "<span class=none-af>sem funções alternativas</span>"}</div></div>')


def group_legend() -> str:
    return ('<div class="cols">Cores das funções: ' + ''.join(f'<span class="g" style="border-color:{g[2]};color:{g[2]}">{g[1]}</span>' for g in GROUPS)
            + '<span>· número = AF no GPIOx_AFR · tracejado = função adicional (ADC, WKUP, OSC…) · 5V/3V6 = tolerância do pino</span></div>')


def full_sheet(side: str, pins: dict) -> str:
    names = P2 if side == 'L' else P1
    title = 'HEADER ESQUERDO · P2' if side == 'L' else 'HEADER DIREITO · P1'
    parity = 'fileira externa = pinos pares' if side == 'L' else 'fileira externa = pinos ímpares'
    n = '1/3' if side == 'L' else '2/3'
    blocks = []
    for pos, out, inn in position_rows(names, side):
        head = f'POSIÇÃO {pos} DE 22' + (' · JUNTO AO DISPLAY / SWD' if pos == 1 else ' · JUNTO AO USB-C' if pos == 22 else '')
        blocks.append(f'<div class="pos"><h3>{head}</h3>{full_line(out[0], pins, ("ext", "EXTERNO"), out[1])}{full_line(inn[0], pins, ("int", "INTERNO"), inn[1])}</div>')
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS_BASE}{FULL_CSS}</style></head><body>
<div class="page" style="width:1500px"><div class="top"><div><div class="kicker">PINOUT COMPLETO · VISTA DE CIMA · DISPLAY NO TOPO · FOLHA {n}</div>
<h1>WeAct STM32H743 Core Board</h1><div class="tag">{title}</div>
<p class="lead">{parity}. Posições na ordem física a partir do display (topo); em cada posição, <b>EXTERNO</b> (borda) e <b>INTERNO</b>.
Caixa branca: <b>pino do CI</b> (LQFP100) e pino do header. Todas as funções alternativas (AF0–AF15) e adicionais do DS12110. Etiqueta amarela = ligação já feita na placa.</p></div>
<div class="map">{board_svg(4.6, side, labels=False)}lado em amarelo</div></div>
{group_legend()}{''.join(blocks)}
<p class="foot">Fonte: ST DS12110 Rev 7 (tabela 9: pino LQFP100, estrutura de E/S, funções adicionais; tabelas 10–14: AF0–AF15) · esquema WeAct STM32H7xx V1.2.
As AF valem para toda a família H742/H743; LCD-TFT, JPEG e Chrom-ART existem na H743. Gerado por scripts/make_h743_pinouts.py · {DATE}</p>
</div></body></html>'''


def full_extra(pins: dict) -> str:
    lines = ''.join(f'<div class="pos">{full_line(n, pins, None)}</div>' for n in OFF_HEADER)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS_BASE}{FULL_CSS}</style></head><body>
<div class="page" style="width:1500px"><div class="kicker">PINOUT COMPLETO · FOLHA 3/3</div><h1>WeAct STM32H743 Core Board</h1>
<div class="tag">PINOS FORA DOS HEADERS E NOTAS</div>
<p class="lead" style="margin-bottom:12px">Sinais do MCU ligados só a componentes da placa (SWD, cristais, BOOT0), com todas as funções, seguidos das notas de uso.
USB (PA11/PA12), LCD, câmera, microSD e flashes usam pinos que também estão nos headers — veja as folhas 1 e 2.</p>
{group_legend()}{lines}
<div class="notes">
<div class="note"><h4>RECURSOS DA PLACA</h4><ul>
<li><b>TFT 0,96″ ST7735</b> (80 × 160) no SPI4: <code>PE12</code> SCK · <code>PE14</code> SDA · <code>PE13</code> DC · <code>PE11</code> CS · <code>PE10</code> luz de fundo (TIM1_CH2N) · reset = reset do sistema</li>
<li><b>Câmera DVP</b> (FPC 24 vias, DCMI): D0–D7 = <code>PC6 PC7 PE0 PE1 PE4 PD3 PE5 PE6</code> · VSYNC <code>PB7</code> · HSYNC <code>PA4</code> · PIXCLK <code>PA6</code> · XCLK <code>PA8</code> (MCO1) · SCCB <code>PB8/PB9</code> (I2C1) · PWDN <code>PA7</code> (SB1)</li>
<li><b>microSD</b> (SDMMC1, 4 bits): <code>PC8–PC11</code> D0–D3 · <code>PC12</code> CLK · <code>PD2</code> CMD · detecção <code>PD4</code> (SB2)</li>
<li><b>Flash QSPI 8 MB</b> PY25Q64HA: <code>PD11 PD12 PE2 PD13</code> IO0–IO3 · <code>PB2</code> CLK · <code>PB6</code> NCS</li>
<li><b>Flash SPI 8 MB</b> PY25Q64HA no SPI1: <code>PB3</code> SCK · <code>PB4</code> MISO · <code>PD7</code> MOSI · <code>PD6</code> CS (SB3, pull-up 100 kΩ)</li>
<li><b>LED azul E3</b>: <code>PE3</code> (ativo em alto, via transistor) · <b>K1</b>: <code>PC13</code> (pressionado = 3V3) · LED vermelho PWR no 3V3</li>
</ul></div>
<div class="note"><h4>SWD, USB E ALIMENTAÇÃO</h4><ul>
<li><b>SWD</b> (4 furos no topo): 3.3V · DIO = <code>PA13</code> (pino 72) · CLK = <code>PA14</code> (pino 76) · GND; resistores de 22 Ω em série</li>
<li><b>USB-C</b> (OTG_FS): <code>PA11</code> D− · <code>PA12</code> D+ · DFU: segurar B0, ligar o cabo</li>
<li><b>5V</b>: entrada de 3,3–5,5 V; o VBUS chega pelo diodo B5819 (SB6 fecha o diodo para alimentar dispositivos USB)</li>
<li><b>3V3</b>: regulador DC-DC de 1 A (SY8088; variantes XT3410/TLV62569) · <b>VB</b>: VBAT do RTC por BAT54C</li>
<li><b>V+</b>: VREF+ do ADC, ligado ao 3V3 por R9 (0 Ω) — retire R9 para usar referência externa</li>
<li><b>Cristais</b>: 25 MHz em <code>PH0/PH1</code> · 32,768 kHz em <code>PC14/PC15</code> · reset por MAX809 + botão NR</li>
</ul></div>
<div class="note"><h4>COMO LER</h4><ul>
<li>O pino do CI é o <b>número do LQFP100</b> da tabela 9 do DS12110 (encapsulamento VxT6)</li>
<li>Vista de cima com o display no topo · esquerdo (P2): externa = pares · direito (P1): externa = ímpares</li>
<li>A serigrafia dos nomes fica no <b>verso</b>, espelhada; na frente só há furos</li>
<li>Número no chip = AF; tracejado = função adicional (ativada pelo periférico, sem AF)</li>
</ul></div>
<div class="note"><h4>CUIDADOS E PONTES DE SOLDA</h4><ul>
<li><b>PC2_C/PC3_C</b> (pinos 17/18): no LQFP100 só existem os pads _C; PC2/PC3 digitais passam por chave analógica (SYSCFG_PMCR)</li>
<li><b>PA13, PA14, PA15, PB3, PB4</b> saem do reset em função JTAG/SWD; PB3/PB4 também são a flash SPI</li>
<li><b>PC13–PC15</b> drenam só ~3 mA, até 2 MHz — não alimente LED por eles</li>
<li><b>SB1</b> PWDN→PA7 · <b>SB2</b> microSD→PD4 · <b>SB3</b> CS da flash SPI→PD6 · <b>SB4/SB5</b> AF 2V8/GND da câmera (soldar para OV5640 com foco) · <b>SB6</b> VBUS→5V</li>
</ul></div></div>
<p class="foot">Fonte: ST DS12110 Rev 7 (tabelas 9, 10–14 e 17) · esquema e desenho mecânico WeAct STM32H7xx V1.2 · README do repositório WeActStudio/MiniSTM32H7xx.
Gerado por scripts/make_h743_pinouts.py · {DATE}</p></div></body></html>'''


# ---------------------------------------------------------------- visão geral completa (placa inteira)

def full_overview(pins: dict) -> str:
    """Placa inteira com todas as funções em colunas por grupo, alinhadas aos furos."""
    scale = 22.9
    row_h = PITCH * scale / 2
    order_l = [g[0] for g in reversed(GROUPS)]  # do lado esquerdo, sistema fica na borda da folha
    order_r = [g[0] for g in GROUPS]
    top = 20

    def cols_for(names):
        width = {g[0]: 0 for g in GROUPS}
        for name in names:
            if name in POWER:
                continue
            per = {}
            for n, f in pins[name].af:
                per.setdefault(group(f), []).append((f, n))
            for a in pins[name].add:
                per.setdefault(group(a), []).append((a, None))
            for gid, items in per.items():
                width[gid] = max(width[gid], sum(len(f) * 6.3 + (22 if n is not None else 12) + 4 for f, n in items))
        return {k: max(v, 40) + 8 for k, v in width.items()}

    def small_chip(name, af):
        gid = group(name)
        strong, light = next((g[2], g[3]) for g in GROUPS if g[0] == gid)
        num = f'<i style="background:{strong}">{af}</i>' if af is not None else ''
        dash = 'dashed' if af is None else 'solid'
        return f'<span class="sc" style="border:1px {dash} {strong};background:{light}">{esc(name)}{num}</span>'

    def side_html(names, side, x0, widths, order):
        out = []
        rows, _ = simple_side_block(names, side, pins, scale, 0, top)
        for y, name, slot in rows:
            if name in POWER:
                text, kind, short = POWER[name]
                bg, fg = {'gnd': ('#111', '#fff'), 'pwr': ('#fde2e6', '#b3172d'), 'plain': ('#f3f4f6', '#333')}[kind]
                cells = f'<div class="cell wide" style="width:{sum(widths.values()):.0f}px;background:{bg};color:{fg}">{esc(text)}</div>'
                nm = f'<div class="nm2" style="background:{"#111" if kind == "gnd" else "#d7263d" if kind == "pwr" else "#9ca3af"}">{esc(short)}</div>'
                box = f'<div class="bx">–<small>{esc(slot)}</small></div>'
            else:
                pin = pins[name]
                per = {}
                for n, f in pin.af:
                    per.setdefault(group(f), []).append(small_chip(f, n))
                for a in pin.add:
                    per.setdefault(group(a), []).append(small_chip(a, None))
                seq = order
                cells = ''.join(f'<div class="cell" style="width:{widths[g]:.0f}px;justify-content:{"flex-end" if side == "L" else "flex-start"}">{"".join(per.get(g, []))}</div>' for g in seq)
                board = f'<small>{esc(pin.board[0])}</small>' if pin.board else ''
                nm = f'<div class="nm2">{esc(pin.label)}{board}</div>'
                box = f'<div class="bx">{pin.lqfp}<small>{esc(slot)}</small></div>'
            parts = [cells, nm, box] if side == 'L' else [box, nm, cells]
            out.append(f'<div class="r" style="left:{x0:.1f}px;top:{y:.1f}px">{"".join(parts)}</div>')
        return out

    wl, wr = cols_for(P2), cols_for(P1)
    left_w = sum(wl.values()) + 120 + 56 + 10
    right_w = sum(wr.values()) + 120 + 56 + 10
    left_x = 30
    board_x = left_x + left_w + 70
    right_x = board_x + W_MM * scale + 70
    width = right_x + right_w + 30
    _, wires_l = simple_side_block(P2, 'L', pins, scale, board_x, top)
    _, wires_r = simple_side_block(P1, 'R', pins, scale, board_x, top)
    body = side_html(P2, 'L', left_x, wl, order_l) + side_html(P1, 'R', right_x, wr, order_r)
    head_l = ''.join(f'<span style="width:{wl[g]:.0f}px;color:{next(x[2] for x in GROUPS if x[0] == g)}">{next(x[1] for x in GROUPS if x[0] == g)}</span>' for g in order_l)
    head_r = ''.join(f'<span style="width:{wr[g]:.0f}px;color:{next(x[2] for x in GROUPS if x[0] == g)}">{next(x[1] for x in GROUPS if x[0] == g)}</span>' for g in order_r)
    height = H_MM * scale + 2 * top
    paths = ''.join(f'<path d="{d}"/>' for d in wires_l + wires_r)
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS_BASE}{FULL_CSS}
.rows{{position:relative}}
.r{{position:absolute;display:flex;gap:4px;height:26px;align-items:center}}
.cell{{height:26px;display:flex;gap:3px;align-items:center;border-bottom:1px solid #e5e5e5;overflow:hidden}}
.cell.wide{{justify-content:center;font-size:12px;font-weight:800;border-radius:3px;border:0}}
.sc{{display:inline-flex;align-items:center;height:20px;border-radius:3px;font-size:10.5px;font-weight:700;padding-left:4px;white-space:nowrap;padding-right:4px}}
.sc i{{font-style:normal;color:#fff;font-size:9px;margin-left:4px;margin-right:-4px;height:100%;display:flex;align-items:center;padding:0 3px}}
.nm2{{width:120px;height:26px;background:#16181c;color:#fff;border-radius:3px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:13px;font-weight:800;line-height:1}}
.nm2 small{{font-size:7.5px;color:#fcd34d;margin-top:1px}}
.bx{{width:56px;height:26px;background:#fff;border:1px solid #111;border-radius:3px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:12px;font-weight:800;line-height:1}}
.bx small{{font-size:7.5px;color:#555}}
.brd{{position:absolute;top:{top}px;left:{board_x:.1f}px}}
.wire{{position:absolute;left:0;top:0}}
.wire path{{fill:none;stroke:#222;stroke-width:2.5;stroke-linejoin:round}}
.gh{{display:flex;gap:4px;font-size:10px;font-weight:800;letter-spacing:.5px;position:absolute;top:-4px}}
.gh span{{text-align:center}}
</style></head><body><div class="page" style="width:{width:.0f}px">
<div class="kicker">PINOUT COMPLETO · VISTA DE CIMA · DISPLAY NO TOPO</div>
<h1>WeAct STM32H743 Core Board <span style="font-size:18px;color:#666">STM32H743VIT6 · LQFP100 · 480 MHz · 2 MiB Flash · 1 MiB RAM · 8 MB QSPI + 8 MB SPI · todas as funções AF0–AF15 e adicionais</span></h1>
{group_legend()}
<div class="rows" style="height:{height + 20:.0f}px;margin-top:26px">
<div class="gh" style="left:{left_x}px">{head_l}</div><div class="gh" style="left:{right_x + 186:.1f}px">{head_r}</div>
<div class="brd">{board_svg(scale)}</div>
<svg class="wire" width="{width:.0f}" height="{height:.0f}">{paths}</svg>
{''.join(body)}</div>
<p class="foot">Esquerdo = P2 (externa = pares) · direito = P1 (externa = ímpares). Pino do CI = LQFP100. Etiqueta amarela sob o nome = ligação feita na placa.
Fonte: ST DS12110 Rev 7 (tabelas 9–14) e esquema WeAct STM32H7xx V1.2 · pinos fora dos headers e notas na folha "Completa · pinos fora dos headers" · {DATE}</p>
</div></body></html>'''


# ---------------------------------------------------------------- renderização

def chrome() -> str:
    for name in ('google-chrome', 'chromium', 'chromium-browser'):
        if shutil.which(name):
            return name
    raise SystemExit('Chrome/Chromium não encontrado no PATH.')


def render(markup: str, out: Path, width: int, height: int, tmp: Path) -> None:
    page = tmp / (out.stem + '.html')
    page.write_text(markup)
    shot = tmp / (out.stem + '.png')
    subprocess.run([chrome(), '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=2',
                    f'--window-size={width},{height}', f'--screenshot={shot}', page.as_uri()],
                   check=True, capture_output=True)
    im = Image.open(shot).convert('RGB')
    # Recorta a sobra da janela: última linha com algum pixel diferente do fundo.
    gray = im.convert('L')
    bg = gray.getpixel((gray.width - 1, gray.height - 1))
    mask = gray.point(lambda v: 255 if abs(v - bg) > 6 else 0)
    box = mask.getbbox()
    bottom = min(im.height, box[3] + 50) if box else im.height
    im.crop((0, 0, im.width, bottom)).save(out, optimize=True)
    print(out.name, Image.open(out).size)


def build() -> dict:
    af = alternate_functions()
    info = pin_definitions()
    names = [n for n in P1 + P2 + OFF_HEADER if n not in POWER]
    pins = {n: Pin(n, af, info) for n in dict.fromkeys(names)}
    missing = [n for n, p in pins.items() if not p.lqfp or (n not in ('BOOT0',) and not p.af)]
    if missing:
        raise SystemExit(f'Pinos sem dados no datasheet: {missing}')
    return pins


def main() -> None:
    pins = build()
    sheets = {
        'h743-pinout-simple.png': (simple_overview, None, 2300),
        'h743-pinout-full.png': (full_overview, None, 2200),
        'h743-pinout-simple-left.png': (simple_sheet, 'L', 2300),
        'h743-pinout-simple-right.png': (simple_sheet, 'R', 2300),
        'h743-pinout-full-left.png': (full_sheet, 'L', 7000),
        'h743-pinout-full-right.png': (full_sheet, 'R', 7000),
        'h743-pinout-full-extra.png': (full_extra, None, 3500),
    }
    only = set(sys.argv[1:])
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        for name, (fn, arg, height) in sheets.items():
            if only and name not in only:
                continue
            markup = fn(arg, pins) if arg else fn(pins)
            match = re.search(r'class="page" style="width:(\d+)', markup)
            render(markup, OUT / name, int(match.group(1)), height, tmp)


if __name__ == '__main__':
    main()

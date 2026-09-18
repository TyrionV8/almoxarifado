"""Dados, documentos, movimentações e servidor local; roda só com Python 3 padrão."""
import hashlib
import http.client
import json
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import db  # noqa: E402
import server  # noqa: E402

PNG = b'\x89PNG\r\n\x1a\n'


def load_js_json(path: Path):
    return json.loads(path.read_text().split(' = ', 1)[1].removesuffix(';\n'))


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.db = db.connect(db.DATABASE, readonly=True)
        self.data = load_js_json(ROOT / 'data/catalog.js')
        self.parts = {p['id']: p for p in self.data['components']}

    def tearDown(self):
        self.db.close()

    def test_integrity_foreign_keys_and_version(self):
        self.assertEqual(self.db.execute('PRAGMA integrity_check').fetchone()[0], 'ok')
        self.assertEqual(self.db.execute('PRAGMA foreign_key_check').fetchall(), [])
        self.assertEqual(self.db.execute('PRAGMA user_version').fetchone()[0], db.SCHEMA_VERSION)

    def test_inventory_scope_and_stock(self):
        parts = self.data['components']
        self.assertEqual(len(parts), 11)
        self.assertEqual(len(self.data['tools']), 3)
        for part in parts:
            stock = part['stock']
            self.assertEqual(stock['available'], stock['total'] - stock['in_use'], part['id'])
            self.assertGreaterEqual(stock['available'], 0)
            self.assertGreaterEqual(stock['in_use'], 0)
            self.assertNotIn('quantity', part)
        self.assertEqual(sum(p['stock']['total'] for p in parts if p['estimated']), 10)

    def test_every_history_is_consistent(self):
        for part in self.data['components']:
            db.check_balances(self.db, part['id'])
            self.assertTrue(part['history'], part['id'])
            dates = [m['date'] for m in part['history']]
            self.assertEqual(dates, sorted(dates), part['id'])

    def test_database_driven_interface_content(self):
        glossary = {t['term'] for t in self.data['glossary']}
        self.assertEqual(len(glossary), 100)
        categories = {c['id'] for c in self.data['glossary_categories']}
        self.assertTrue(all(t['category_id'] in categories for t in self.data['glossary']))
        self.assertTrue(all(len(c['tips']) == 3 for c in self.data['glossary_categories']))
        names = [n.lower() for t in self.data['glossary'] for n in [t['term'], *t['aliases']]]
        self.assertEqual(len(names), len(set(names)), 'sinônimo repetido ou igual a outro termo')
        figures = {t['term']: t['figure'] for t in self.data['glossary'] if t['figure']}
        # Termos documentados no modelo de QSPI: figura e explicação em vários parágrafos.
        documented = ['QSPI', 'SPI', 'USART', 'UART', 'LPUART', 'I2S', 'I2C']
        self.assertEqual(sorted(figures), sorted(documented))
        for term in documented:
            detail = next(t['detail'] for t in self.data['glossary'] if t['term'] == term)
            self.assertGreaterEqual(detail.count('\n\n'), 3, term)
        for term, figure in figures.items():
            self.assertTrue((ROOT / figure).read_text().lstrip().startswith('<svg'), term)
        qspi = next(t for t in self.data['glossary'] if t['term'] == 'QSPI')
        self.assertIn('Quad-SPI', qspi['aliases'])
        self.assertIn('0x9000 0000', qspi['detail'])
        self.assertEqual(len(self.data['table_columns']), 23)
        groups = {g['id'] for g in self.data['column_groups']}
        for column in self.data['table_columns']:
            self.assertIn(column['group_id'], groups, column['key'])
            self.assertTrue(column['term'] is None or column['term'] in glossary, column['key'])
        self.assertTrue({p['term'] for p in self.data['pin_guides']} <= glossary)
        classes = {c['name'] for c in self.data['processing_classes']}
        guides = {p['guide'] for p in self.data['pin_guides']}
        families = {f['id'] for f in self.data['families']}
        for part in self.data['components']:
            self.assertIn(part['processing_class'], classes, part['id'])
            self.assertIn(part['pin_guide'], guides, part['id'])
            self.assertIn(part['family'], families, part['id'])
            self.assertTrue(part['subtitle'] and part['flash_short'] and part['accelerators'], part['id'])

    def test_confirmed_variants(self):
        p = self.parts
        self.assertIn('STM32F411CEU6', p['blackpill']['package'])
        self.assertIn('8 MiB', p['blackpill']['external'])
        self.assertIn('25 MHz', p['blackpill']['oscillator'])
        self.assertIn('STM32G474CEU6', p['g474']['package'])
        self.assertEqual(p['g474']['ram'], 131072)
        self.assertIn('64 KiB', p['h7r3']['flash'])
        self.assertEqual(p['h7r3']['dac'], 'Não')
        self.assertIn('STM32H743VIT6', p['h743']['package'])
        self.assertEqual((p['h743']['clock'], p['h743']['ram']), (480, 1081344))
        self.assertIn('2 MiB', p['h743']['flash'])

    def test_published_performance_metrics(self):
        p = self.parts
        for component_id in ('pic16f887', 'pic12f675', 'pic12f683', 'pic12f1501'):
            self.assertEqual(p[component_id]['mips_peak'], 5)
        self.assertEqual(p['uno']['mips_peak'], 16)
        self.assertEqual(p['nano']['mips_peak'], 16)
        expected = {'bluepill': (108.26, 90, 1.0), 'blackpill': (339, 125, 1.39), 'g474': (569, 213, 2.37), 'h7r3': (3196, 1284, 14.27),
                    'h743': (2424, 1027, 11.41)}
        for component_id, (coremark, dmips, relative) in expected.items():
            self.assertEqual(p[component_id]['coremark'], coremark)
            self.assertEqual(p[component_id]['dmips'], dmips)
            self.assertEqual(p[component_id]['relative_bluepill'], relative)
        self.assertIn('STM32F103RB', p['bluepill']['coremark_note'])
        self.assertTrue({'MIPS', 'DMIPS', 'CoreMark'} <= {t['term'] for t in self.data['glossary']})

    def test_every_local_asset(self):
        for p in self.data['components']:
            for directory, key in [('assets/documents', 'datasheet'), ('assets/pinouts', 'pinout'), ('assets/documents', 'pinout_source')]:
                self.assertTrue((ROOT / directory / p[key]).is_file(), (p['id'], key))
            self.assertTrue((ROOT / 'data/readers' / p['datasheet'].replace('.pdf', '.js')).is_file())
            if p.get('schematic'):
                self.assertTrue((ROOT / 'assets/documents' / p['schematic']).is_file())
            if p.get('evidence'):
                self.assertTrue((ROOT / p['evidence']).is_file())
        html = (ROOT / 'index.html').read_text()
        for script in (ROOT / 'assets/js').glob('*.js'):
            self.assertIn(f'assets/js/{script.name}', html)

    def test_source_checksums_and_readers(self):
        for source in self.data['sources']:
            path = ROOT / source['file']
            blob = path.read_bytes()
            self.assertTrue(blob.startswith(b'%PDF'))
            self.assertEqual(hashlib.sha256(blob).hexdigest(), source['sha256'])
            pages = load_js_json(ROOT / 'data/readers' / path.with_suffix('.js').name)
            self.assertTrue(any(page.strip() for page in pages))

    def test_pinout_credits_and_sources(self):
        for part in self.data['components']:
            self.assertTrue(part.get('pinout_credit'), part['id'])
        for source in json.loads((ROOT / 'data/pinout_sources.json').read_text()):
            blob = (ROOT / source['file']).read_bytes()
            self.assertTrue(blob.startswith(PNG), source['file'])
            self.assertEqual(hashlib.sha256(blob).hexdigest(), source['sha256'])
            self.assertTrue(source['credit'] and source['license'], source['file'])

    def test_g474_pinout_versions(self):
        # Simples e completa aparecem empilhadas, ambas com numeração UFQFPN48 (docs/G474-PINOUT.md).
        g474 = self.parts['g474']
        self.assertEqual([p['file'] for p in g474['pinouts']], ['g474-long-pinout-simple.png', 'g474-long-pinout-full.png'])
        self.assertEqual(g474['pinout'], g474['pinouts'][0]['file'])
        for p in g474['pinouts']:
            self.assertTrue((ROOT / 'assets/pinouts' / p['file']).read_bytes().startswith(PNG), p['file'])
        self.assertEqual(sorted(p.name for p in (ROOT / 'assets/pinouts').glob('g474*.png')), ['g474-long-pinout-full.png', 'g474-long-pinout-simple.png'])

    def test_arduino_pinout_versions(self):
        # Folha simples gerada por scripts/make_arduino_pinouts.py primeiro; folha oficial como referência (docs/ARDUINO-PINOUT.md).
        generator = (ROOT / 'scripts/make_arduino_pinouts.py').read_text()
        for board in ('uno', 'nano'):
            part = self.parts[board]
            self.assertEqual([p['file'] for p in part['pinouts']], [f'{board}-pinout-simple.png', f'{board}-pinout.png'])
            self.assertEqual(part['pinout'], f'{board}-pinout-simple.png')
            for p in part['pinouts']:
                self.assertTrue((ROOT / 'assets/pinouts' / p['file']).read_bytes().startswith(PNG), p['file'])
        for gpio in ['PD0', 'PD1', 'PD2', 'PD3', 'PD4', 'PD5', 'PD6', 'PD7', 'PB0', 'PB1', 'PB2', 'PB3', 'PB4', 'PB5', 'PC6', 'ADC6', 'ADC7']:
            self.assertIn(f"'{gpio}'", generator)

    def test_h7r3_pinout_versions(self):
        # Visões gerais e folhas por header; pinos do CI pela esfera UFBGA144 SMPS GP (docs/H7R3-PINOUT.md).
        h7 = self.parts['h7r3']
        files = ['h7-pinout-simple.png', 'h7-pinout-full.png', 'h7-pinout-simple-left.png', 'h7-pinout-simple-right.png',
                 'h7-pinout-full-left.png', 'h7-pinout-full-right.png', 'h7-pinout-full-extra.png']
        self.assertEqual([p['file'] for p in h7['pinouts']], files)
        self.assertEqual(sorted(p.name for p in (ROOT / 'assets/pinouts').glob('h7-pinout-*.png')), sorted(files))
        self.assertEqual(h7['pinout'], files[0])
        for p in h7['pinouts']:
            self.assertTrue((ROOT / 'assets/pinouts' / p['file']).read_bytes().startswith(PNG), p['file'])

    def test_h743_pinout_versions(self):
        # Mesma organização da H7R3; pino do CI = número LQFP100; geradas por scripts/make_h743_pinouts.py (docs/H743-PINOUT.md).
        h743 = self.parts['h743']
        files = [f'h743-pinout-{n}.png' for n in ('simple', 'full', 'simple-left', 'simple-right', 'full-left', 'full-right', 'full-extra')]
        self.assertEqual([p['file'] for p in h743['pinouts']], files)
        self.assertEqual(sorted(p.name for p in (ROOT / 'assets/pinouts').glob('h743-pinout-*.png')), sorted(files))
        self.assertEqual(h743['pinout'], files[0])
        for p in h743['pinouts']:
            self.assertTrue((ROOT / 'assets/pinouts' / p['file']).read_bytes().startswith(PNG), p['file'])

    def test_h743_header_map(self):
        # Headers conforme o esquema WeAct STM32H7xx V1.2 (P1 e P2, 2 × 22) e números LQFP100 do DS12110.
        import make_h743_pinouts as gen
        self.assertEqual((len(gen.P1), len(gen.P2)), (44, 44))
        self.assertEqual(gen.P1[:4] + gen.P1[-2:], ['GND', '5V', 'PE1', 'PE0', 'PB13', 'PB12'])
        self.assertEqual(gen.P2[:4] + gen.P2[-4:], ['GND', '3V3', 'PE2', 'PE3', '3V3', '5V', 'GND', 'GND'])
        gpio = [n for n in gen.P1 + gen.P2 if n not in gen.POWER]
        self.assertEqual((len(gpio), len(set(gpio))), (76, 76))
        self.assertIn('76 nos headers', self.parts['h743']['gpio'])

    def test_sql_roundtrip(self):
        restored = sqlite3.connect(':memory:')
        restored.executescript((ROOT / 'data/inventory.sql').read_text())
        tables = [row[0] for row in self.db.execute("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name")]
        for table in tables + ['component_stock']:
            query = f'SELECT * FROM {table} ORDER BY 1, 2'
            self.assertEqual([tuple(r) for r in self.db.execute(query)], restored.execute(query).fetchall(), table)
        self.assertEqual(restored.execute('PRAGMA user_version').fetchone()[0], db.SCHEMA_VERSION)
        restored.close()

    def test_deterministic_exports(self):
        subprocess.run([sys.executable, str(ROOT / 'scripts/export.py'), '--check'], check=True, capture_output=True)

    def test_no_external_runtime_dependencies(self):
        html = (ROOT / 'index.html').read_text()
        css = (ROOT / 'assets/style.css').read_text()
        scripts = {path.name: path.read_text() for path in (ROOT / 'assets/js').glob('*.js')}
        self.assertNotRegex(html, r'(?:src|href)="https?://')
        self.assertNotRegex(css, r'@import|url\([\'"]?https?://')
        for name, js in scripts.items():
            self.assertNotRegex(js, r'\b(?:XMLHttpRequest|WebSocket)\s*\(', name)
            self.assertNotRegex(js, r'fetch\([\'"`]?https?:', name)
        # Único acesso de rede: api() fala com o servidor local, pela mesma origem, em caminhos relativos.
        self.assertEqual([name for name, js in scripts.items() if 'fetch(' in js], ['core.js'])


class MovementTests(unittest.TestCase):
    """Regras de registro numa cópia temporária do banco."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'inventory.sqlite'
        shutil.copy(db.DATABASE, self.path)
        self.con = db.connect(self.path)
        # Estado conhecido, independente do que o usuário registrar no banco real.
        with self.con:
            self.con.execute('DELETE FROM movements')
        db.add_movement(self.con, 'bluepill', 'entrada', 3, '2026-09-12')
        db.add_movement(self.con, 'blackpill', 'entrada', 1, '2026-09-12')
        db.add_movement(self.con, 'blackpill', 'uso', 1, '2026-09-12')

    def tearDown(self):
        self.con.close()
        self.tmp.cleanup()

    def stock(self, component_id):
        row = self.con.execute('SELECT total, in_use, available FROM component_stock WHERE component_id = ?', (component_id,)).fetchone()
        return dict(row)

    def test_purchase_use_release_and_discard(self):
        db.add_movement(self.con, 'bluepill', 'compra', 2, '2026-09-13', 'Loja')
        db.add_movement(self.con, 'bluepill', 'uso', 3, '2026-09-13')
        self.assertEqual(self.stock('bluepill'), {'total': 5, 'in_use': 3, 'available': 2})
        db.add_movement(self.con, 'bluepill', 'devolucao', 1, '2026-09-13')
        db.add_movement(self.con, 'bluepill', 'descarte_em_uso', 2, '2026-09-13', 'Queimou')
        db.add_movement(self.con, 'bluepill', 'descarte', 1, '2026-09-13')
        self.assertEqual(self.stock('bluepill'), {'total': 2, 'in_use': 0, 'available': 2})

    def test_rejects_impossible_movements(self):
        for args in [('uno', 'uso', 1, '2026-09-13'),              # nenhuma unidade
                     ('bluepill', 'devolucao', 1, '2026-09-13'),   # nenhuma em uso
                     ('blackpill', 'descarte', 1, '2026-09-13'),   # a única está em uso
                     ('bluepill', 'descarte', 4, '2026-09-13'),
                     ('bluepill', 'compra', 0, '2026-09-13'),
                     ('bluepill', 'compra', True, '2026-09-13'),
                     ('bluepill', 'compra', 1, '13/09/2026'),
                     ('bluepill', 'compra', 1, '2999-01-01'),
                     ('bluepill', 'inexistente', 1, '2026-09-13'),
                     ('nada', 'compra', 1, '2026-09-13'),
                     ('bluepill', 'descarte', 1, '2026-01-01')]:   # retroativo: antes da entrada
            with self.subTest(args=args), self.assertRaises(db.InventoryError):
                db.add_movement(self.con, *args)
        self.assertEqual(self.con.execute('SELECT COUNT(*) FROM movements').fetchone()[0], 3)

    def test_delete_keeps_history_valid(self):
        entry = self.con.execute("SELECT id FROM movements WHERE component_id = 'blackpill' AND type_id = 'entrada'").fetchone()[0]
        with self.assertRaises(db.InventoryError):
            db.delete_movement(self.con, entry)  # a unidade em uso ficaria sem entrada
        self.assertTrue(self.con.execute('SELECT 1 FROM movements WHERE id = ?', (entry,)).fetchone())
        new = db.add_movement(self.con, 'g474', 'compra', 1, '2026-09-13')
        db.delete_movement(self.con, new)
        self.assertEqual(self.stock('g474')['total'], 0)


class ServerTests(unittest.TestCase):
    """API do servidor local contra cópias temporárias do banco e dos snapshots."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        shutil.copy(db.DATABASE, self.base / 'inventory.sqlite')
        handler = type('TestHandler', (server.Handler,), {'database': self.base / 'inventory.sqlite', 'data_dir': self.base,
                                                        'log_message': lambda *args: None})
        self.httpd = ThreadingHTTPServer(('127.0.0.1', 0), handler)
        self.port = self.httpd.server_address[1]
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.tmp.cleanup()

    def request(self, method, path, body=None, headers=None):
        con = http.client.HTTPConnection('127.0.0.1', self.port, timeout=10)
        payload = json.dumps(body).encode() if body is not None else None
        con.request(method, path, payload, {'Content-Type': 'application/json', **(headers or {})})
        response = con.getresponse()
        data = response.read()
        con.close()
        return response.status, data

    def test_status_and_static_files(self):
        status, data = self.request('GET', '/api/status')
        self.assertEqual((status, json.loads(data)), (200, {'writable': True}))
        self.assertEqual(self.request('GET', '/index.html')[0], 200)
        self.assertEqual(self.request('GET', '/.git/config')[0], 404)

    def test_register_and_delete_movement(self):
        con = db.connect(self.base / 'inventory.sqlite', readonly=True)
        before = dict(con.execute("SELECT total, available FROM component_stock WHERE component_id = 'h7r3'").fetchone())
        con.close()
        body = {'component_id': 'h7r3', 'type_id': 'compra', 'quantity': 2, 'date': '2026-09-13', 'note': 'teste do servidor'}
        status, data = self.request('POST', '/api/movements', body)
        self.assertEqual(status, 200, data)
        h7 = next(c for c in json.loads(data)['catalog']['components'] if c['id'] == 'h7r3')
        self.assertEqual((h7['stock']['total'], h7['stock']['available']), (before['total'] + 2, before['available'] + 2))
        self.assertIn('teste do servidor', (self.base / 'catalog.js').read_text())
        self.assertIn('teste do servidor', (self.base / 'inventory.sql').read_text())
        status, data = self.request('POST', f"/api/movements/{h7['history'][-1]['id']}/delete", {})
        self.assertEqual(status, 200, data)
        self.assertNotIn('teste do servidor', (self.base / 'catalog.js').read_text())

    def test_rejects_invalid_and_foreign_requests(self):
        body = {'component_id': 'h7r3', 'type_id': 'descarte', 'quantity': 999, 'date': '2026-09-13'}
        status, data = self.request('POST', '/api/movements', body)
        self.assertEqual(status, 422)
        self.assertIn('disponíveis', json.loads(data)['error'])
        self.assertEqual(self.request('POST', '/api/movements', body, {'Origin': 'https://example.com'})[0], 403)
        self.assertEqual(self.request('POST', '/api/movements', body, {'Host': 'evil.test'})[0], 403)
        self.assertEqual(self.request('POST', '/api/movements', body, {'Content-Type': 'text/plain'})[0], 403)
        self.assertFalse((self.base / 'catalog.js').exists())


if __name__ == '__main__':
    unittest.main()

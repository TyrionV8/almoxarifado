"""Acesso compartilhado ao banco do almoxarifado.

Reúne o que exportação, servidor local, migrações e testes precisam:
conexão, estoque calculado a partir das movimentações, registro/remoção de
movimentações com validação e geração dos snapshots `catalog.js` e `inventory.sql`.
"""
from __future__ import annotations

import datetime
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
DATABASE = DATA / 'inventory.sqlite'
SOURCES = DATA / 'sources.json'
SCHEMA_VERSION = 15
MAX_MOVEMENT_QUANTITY = 1000
MAX_NOTE_LENGTH = 500


class InventoryError(ValueError):
    """Regra do acervo violada; a mensagem é exibida ao usuário."""


def connect(path: Path = DATABASE, readonly: bool = False) -> sqlite3.Connection:
    if readonly:
        con = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    else:
        con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.execute('PRAGMA foreign_keys = ON')
    return con


def rows(con: sqlite3.Connection, sql: str, *params) -> list[dict]:
    return [dict(row) for row in con.execute(sql, params)]


# ---------------------------------------------------------------- movimentações

def check_balances(con: sqlite3.Connection, component_id: str) -> None:
    """Percorre o histórico em ordem de data e falha se o saldo ficar negativo em algum momento."""
    total = in_use = 0
    history = con.execute(
        '''SELECT m.date, m.quantity, t.label, t.delta_total, t.delta_in_use
           FROM movements m JOIN movement_types t ON t.id = m.type_id
           WHERE m.component_id = ? ORDER BY m.date, m.id''',
        (component_id,),
    )
    for row in history:
        total += row['quantity'] * row['delta_total']
        in_use += row['quantity'] * row['delta_in_use']
        day = format_date(row['date'])
        if in_use < 0:
            raise InventoryError(f'Em {day}, “{row["label"]}” deixaria menos de zero unidades em uso.')
        if total - in_use < 0:
            raise InventoryError(f'Em {day}, “{row["label"]}” precisa de mais unidades disponíveis do que havia.')


def add_movement(con: sqlite3.Connection, component_id, type_id, quantity, date, note='') -> int:
    """Registra uma movimentação e confirma a transação somente se o histórico continuar válido."""
    if not con.execute('SELECT 1 FROM components WHERE id = ?', (component_id,)).fetchone():
        raise InventoryError('Componente desconhecido.')
    if not con.execute('SELECT 1 FROM movement_types WHERE id = ?', (type_id,)).fetchone():
        raise InventoryError('Tipo de movimentação desconhecido.')
    if isinstance(quantity, bool) or not isinstance(quantity, int) or not 1 <= quantity <= MAX_MOVEMENT_QUANTITY:
        raise InventoryError(f'Quantidade deve ser um número inteiro entre 1 e {MAX_MOVEMENT_QUANTITY}.')
    day = parse_date(date)
    note = str(note or '').strip()
    if len(note) > MAX_NOTE_LENGTH:
        raise InventoryError(f'Observação muito longa (máximo {MAX_NOTE_LENGTH} caracteres).')
    with con:
        cursor = con.execute(
            'INSERT INTO movements(component_id, type_id, quantity, date, note, created_at) VALUES (?, ?, ?, ?, ?, ?)',
            (component_id, type_id, quantity, day, note, now()),
        )
        check_balances(con, component_id)
    return cursor.lastrowid


def delete_movement(con: sqlite3.Connection, movement_id) -> None:
    row = con.execute('SELECT component_id FROM movements WHERE id = ?', (movement_id,)).fetchone()
    if not row:
        raise InventoryError('Registro não encontrado; recarregue a página.')
    with con:
        con.execute('DELETE FROM movements WHERE id = ?', (movement_id,))
        check_balances(con, row['component_id'])


def parse_date(value) -> str:
    try:
        day = datetime.date.fromisoformat(str(value))
    except ValueError:
        raise InventoryError('Data inválida; use o formato AAAA-MM-DD.') from None
    if day > datetime.date.today():
        raise InventoryError('A data não pode estar no futuro.')
    return day.isoformat()


def format_date(iso: str) -> str:
    return datetime.date.fromisoformat(iso).strftime('%d/%m/%Y')


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()


# ---------------------------------------------------------------- exportação

def build_catalog(con: sqlite3.Connection) -> dict:
    """Monta o objeto consumido pela página (window.CATALOG)."""
    stock = {row['component_id']: row for row in rows(con, 'SELECT * FROM component_stock')}
    history: dict[str, list] = {}
    for movement in rows(con, 'SELECT id, component_id, type_id, quantity, date, note FROM movements ORDER BY date, id'):
        history.setdefault(movement.pop('component_id'), []).append(movement)

    components = []
    for row in rows(con, 'SELECT * FROM components ORDER BY position'):
        item = {**row, **json.loads(row.pop('specs'))}
        del item['specs']
        counts = stock[item['id']]
        item['stock'] = {'total': counts['total'], 'in_use': counts['in_use'], 'available': counts['available']}
        item['history'] = history.get(item['id'], [])
        components.append(item)

    glossary_categories = rows(con, 'SELECT * FROM glossary_categories ORDER BY position')
    for category in glossary_categories:
        category['tips'] = json.loads(category['tips'])

    glossary = rows(con, 'SELECT * FROM glossary ORDER BY term')
    for term in glossary:
        term['aliases'] = json.loads(term['aliases'])

    return {
        'schema': SCHEMA_VERSION,
        'categories': rows(con, 'SELECT * FROM categories ORDER BY id'),
        'families': rows(con, 'SELECT * FROM families ORDER BY position'),
        'components': components,
        'movement_types': rows(con, 'SELECT * FROM movement_types ORDER BY position'),
        'spec_fields': rows(con, 'SELECT * FROM spec_fields ORDER BY position'),
        'column_groups': rows(con, 'SELECT * FROM column_groups ORDER BY position'),
        'table_columns': rows(con, 'SELECT * FROM table_columns ORDER BY position'),
        'processing_classes': rows(con, 'SELECT * FROM processing_classes ORDER BY rank'),
        'glossary_categories': glossary_categories,
        'glossary': glossary,
        'pin_guides': rows(con, 'SELECT * FROM pin_guides ORDER BY guide, position'),
        'tools': rows(con, 'SELECT * FROM tools ORDER BY rowid'),
        'sources': json.loads(SOURCES.read_text()),
    }


def catalog_script(con: sqlite3.Connection) -> str:
    return 'window.CATALOG = ' + json.dumps(build_catalog(con), ensure_ascii=False, sort_keys=True, indent=2) + ';\n'


def sql_dump(con: sqlite3.Connection) -> str:
    version = con.execute('PRAGMA user_version').fetchone()[0]
    return ('-- Gerado de inventory.sqlite; edite o banco e execute scripts/export.py.\n'
            + '\n'.join(con.iterdump()) + f'\nPRAGMA user_version={version};\n')


def snapshots(con: sqlite3.Connection, data_dir: Path = DATA) -> dict[Path, str]:
    assert con.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    return {data_dir / 'catalog.js': catalog_script(con), data_dir / 'inventory.sql': sql_dump(con)}


def write_snapshots(con: sqlite3.Connection, data_dir: Path = DATA) -> None:
    for path, content in snapshots(con, data_dir).items():
        path.write_text(content)

'use strict';
/* Página do catálogo: resumo, filtros, tabela configurável (tabela table_columns do banco) e seletor de colunas. */

const COLUMN_STORAGE_KEY = 'almoxarifado-column-preferences-v2';
const differentScale = '<span class="muted" title="Esta arquitetura usa outra escala de desempenho">Escala diferente</span>';

let columnOrder = [], visibleColumns = new Set();
const columnByKey = key => categoryColumns().find(c => c.key === key);
const groupById = id => C.column_groups.find(g => g.id === id);
const columnValue = (c, column) => c[column.field || column.key];

/* Como cada formato de coluna vira HTML. */
const cellRenderers = {
  component: c => `<button class="part-name" data-expand="${esc(c.id)}" aria-expanded="${state.expanded === c.id}" aria-controls="detail-${esc(c.id)}">
      <span class="chip-icon ${tone(familyTone(c))}">▦</span><span>${esc(c.name)}<small>${esc(c.subtitle)}</small></span></button>`,
  family: c => `<span class="badge ${tone(familyTone(c))}">${esc(c.family)}</span>`,
  stock: c => {
    const {available, in_use: inUse, total} = c.stock;
    const hint = !total ? 'sem unidades' : inUse ? `${inUse} em uso` : 'nenhuma em uso';
    const status = available ? '' : total ? 'is-busy' : 'is-empty';
    return `<button class="stock ${status}" data-open-history="${esc(c.id)}" title="Disponíveis / total · abrir histórico">
      <span class="stock-ratio"><b>${available}</b>/${total}${c.estimated ? '<sup>*</sup>' : ''}</span><small>${hint}</small></button>`;
  },
  class: (c, column) => `<span class="class-pill rank-${classRank.get(columnValue(c, column)) || 0}">${esc(columnValue(c, column))}</span>`,
  metric: (c, column) => {
    const value = columnValue(c, column);
    if (value === undefined) return differentScale;
    const note = c[`${column.key}_note`];
    return `${formatNumber(value, column.digits)}${column.unit ? `<span class="unit">${esc(column.unit)}</span>` : ''}${note ? `<span class="note-mark" title="${esc(note)}">*</span>` : ''}`;
  },
  annotated: (c, column) => annotate(columnValue(c, column)),
  text: (c, column) => esc(columnValue(c, column)),
  mhz: (c, column) => `${esc(columnValue(c, column))}<span class="unit">MHz</span>`,
  bytes: (c, column) => annotate(formatBytes(columnValue(c, column))),
};

function sortValue(c, column) {
  const value = columnValue(c, column);
  switch (column.format) {
    case 'component': return c.name;
    case 'family': return c.family;
    case 'stock': return c.stock.available * 1000 + c.stock.total;
    case 'class': return classRank.get(value) || 0;
    case 'metric': return value ?? -1;
    default: return value ?? '';
  }
}

/* ---------- preferências de colunas (localStorage) ---------- */

function loadColumnPreferences() {
  columnOrder = categoryColumns().map(c => c.key);
  visibleColumns = new Set(columnOrder);
  try {
    const saved = JSON.parse(window.localStorage.getItem(columnStorageKey()));
    if (!saved) return;
    const valid = saved.order.filter(columnByKey);
    columnOrder = [...valid, ...columnOrder.filter(key => !valid.includes(key))];
    visibleColumns = new Set(saved.visible.filter(columnByKey));
    if (!visibleColumns.size) visibleColumns.add('name');
  } catch { /* preferências ausentes ou inválidas: usa o padrão */ }
}

function saveColumnPreferences() {
  try {
    window.localStorage.setItem(columnStorageKey(), JSON.stringify({order: columnOrder, visible: [...visibleColumns]}));
  } catch { /* navegador sem armazenamento */ }
}

const columnStorageKey = () => state.category === 'microcontroladores' ? COLUMN_STORAGE_KEY : `${COLUMN_STORAGE_KEY}-${state.category}`;

function resetColumns() {
  columnOrder = categoryColumns().map(c => c.key);
  visibleColumns = new Set(columnOrder);
  saveColumnPreferences();
  renderColumnMenu();
  drawRows();
}

function toggleColumn(key, visible) {
  visible ? visibleColumns.add(key) : visibleColumns.delete(key);
  saveColumnPreferences();
  renderColumnMenu();
  drawRows();
}

function moveColumn(key, direction) {
  const from = columnOrder.indexOf(key), to = from + Number(direction);
  if (from < 0 || to < 0 || to >= columnOrder.length) return;
  [columnOrder[from], columnOrder[to]] = [columnOrder[to], columnOrder[from]];
  saveColumnPreferences();
  renderColumnMenu();
  drawRows();
}

const activeColumns = () => columnOrder.filter(key => visibleColumns.has(key)).map(columnByKey);

function renderColumnMenu() {
  const list = $('#column-picker-list');
  if (!list) return;
  $('#visible-column-count').textContent = `${visibleColumns.size}/${categoryColumns().length}`;
  list.innerHTML = columnOrder.map((key, i) => {
    const c = columnByKey(key), label = esc(c.label);
    return `<div class="column-option">
      <label><input type="checkbox" data-column-toggle="${esc(key)}" ${visibleColumns.has(key) ? 'checked' : ''}><span>${label}<small>${esc(groupById(c.group_id).label)}</small></span></label>
      <span>
        <button data-column-move="${esc(key)}" data-direction="-1" aria-label="Mover ${label} para a esquerda" ${i === 0 ? 'disabled' : ''}>↑</button>
        <button data-column-move="${esc(key)}" data-direction="1" aria-label="Mover ${label} para a direita" ${i === columnOrder.length - 1 ? 'disabled' : ''}>↓</button>
      </span>
    </div>`;
  }).join('');
}

/* ---------- página ---------- */

function catalogView() {
  const category = currentCategory(), components = sectorComponents();
  const estimatedFamilies = [...new Set(components.filter(c => c.estimated).map(c => c.family))];
  const estimatedUnits = components.filter(c => c.estimated).reduce((n, c) => n + c.stock.total, 0);
  const benchmarkNotes = C.table_columns
    .filter(column => column.format === 'metric')
    .flatMap(column => C.components.filter(c => c[`${column.key}_note`])
      .map(c => `<b>${esc(column.label)} da ${esc(c.name)} (*):</b> ${esc(c[`${column.key}_note`])}`));
  return `
    <nav class="sector-nav" aria-label="Setores do almoxarifado">
      ${C.categories.map(c => `<button data-category="${esc(c.id)}" class="${c.id === state.category ? 'active' : ''}" aria-pressed="${c.id === state.category}">${esc(c.name)} <span>${C.components.filter(p => p.category_id === c.id).length}</span></button>`).join('')}
    </nav>
    <div class="page-heading">
      <div><div class="eyebrow">DO COMPONENTE À IDEIA</div><h1>${esc(category.name)}</h1><p>Conheça o que você tem. Escolha o que seu projeto precisa.</p></div>
      <span class="edition">CATÁLOGO<br><b>${String(C.categories.indexOf(category) + 1).padStart(2, '0')} / ${esc(category.name.toUpperCase())}</b></span>
    </div>
    <section class="stats" aria-label="Resumo do acervo"></section>
    <div class="toolbar">
      <label class="search"><span>⌕</span><input id="search" type="search" placeholder="Buscar componente, recurso ou aplicação…" aria-label="Buscar componentes"></label>
      <select id="family" aria-label="Filtrar família">
        <option value="">Todas as famílias</option>
        ${C.families.filter(f => components.some(c => c.family === f.id)).map(f => `<option value="${esc(f.id)}">${esc(f.name)}</option>`).join('')}
      </select>
      <select id="kind" aria-label="Filtrar formato">
        <option value="">Chips e placas</option><option value="chip">Somente chips</option><option value="placa">Somente placas</option>
      </select>
      <details id="column-picker" class="column-picker">
        <summary>Colunas <span id="visible-column-count"></span></summary>
        <div class="column-menu">
          <div class="column-menu-head"><div><b>Escolher e ordenar</b><small>As setas mudam a posição na tabela.</small></div><button data-reset-columns>Restaurar</button></div>
          <div id="column-picker-list"></div>
        </div>
      </details>
    </div>
    <div class="table-caption"><span id="result-count"></span><span>Clique no nome para abrir a ficha · na quantidade para o histórico</span></div>
    <div class="table-wrap"><table id="inventory"><thead></thead><tbody id="rows"></tbody></table></div>
    ${estimatedUnits ? `<p class="footnote">* As ${estimatedUnits} unidades ${esc(estimatedFamilies.join(' e '))} são estimativas do inventário.</p>` : ''}
    ${category.id === 'microcontroladores' ? `<p id="performance-note" class="footnote"><b>Escalas de desempenho:</b> MIPS significa milhões de instruções por segundo e é apresentado para PIC e ATmega328P. DMIPS é o resultado normalizado do teste Dhrystone; CoreMark é outro teste padronizado. MIPS, DMIPS e CoreMark não devem ser comparados diretamente entre si. ${benchmarkNotes.join(' ')}</p>` : ''}
    <section class="bench-note">
      <span>↗</span>
      <div><b>Uma ficha técnica que você pode entender.</b><p>Passe o cursor sobre um termo sublinhado para uma explicação rápida. Clique para aprofundar.</p></div>
      <button data-view="glossario">Explorar documentação →</button>
    </section>`;
}

function renderStats() {
  const components = sectorComponents();
  const families = C.families.filter(f => components.some(c => c.family === f.id));
  const sum = key => components.reduce((n, c) => n + c.stock[key], 0);
  const estimated = components.some(c => c.estimated);
  $('.stats').innerHTML = `
    <div class="tone-green"><span>Modelos neste setor</span><strong>${components.length} <small>modelos</small></strong></div>
    <div class="tone-teal"><span>Disponíveis / total</span><strong>${sum('available')}/${sum('total')} <small>unidades${estimated ? '*' : ''}</small></strong></div>
    <div class="tone-blue"><span>Em uso agora</span><strong>${sum('in_use')} <small>unidades</small></strong></div>
    <div class="tone-orange"><span>Famílias</span><strong>${String(families.length).padStart(2, '0')} <small>${families.map(f => esc(f.name)).join(' · ')}</small></strong></div>`;
  $('#component-count').textContent = C.components.length;
}

function groupHeaders(columns) {
  const runs = [];
  for (const groupId of ['acervo', ...columns.map(c => c.group_id), 'detalhes']) {
    const last = runs.at(-1);
    last && last.id === groupId ? last.count++ : runs.push({id: groupId, count: 1});
  }
  return runs.map(run => {
    const group = groupById(run.id);
    return `<th colspan="${run.count}" class="${tone(group.tone)}">${esc(group.label)}</th>`;
  }).join('');
}

function columnHeader(column) {
  const group = groupById(column.group_id);
  return `<th class="${tone(group.tone)}" style="min-width:${column.width}px"${column.help ? ` title="${esc(column.help)}"` : ''}>
    <button data-sort="${esc(column.key)}">${esc(column.label)} <span aria-hidden="true">↕</span></button></th>`;
}

/* O detalhamento fica preso à área visível da tabela, que rola na horizontal. */
function fitDetailWidth() {
  const wrap = $('#main .table-wrap');
  if (wrap) wrap.style.setProperty('--detail-width', wrap.clientWidth + 'px');
}

function filteredComponents() {
  const query = $('#search').value.toLocaleLowerCase();
  const family = $('#family').value, kind = $('#kind').value;
  const items = sectorComponents().filter(c => JSON.stringify(c).toLocaleLowerCase().includes(query)
    && (!family || c.family === family) && (!kind || c.kind === kind));
  const column = columnByKey(state.sortKey);
  if (column) {
    items.sort((a, b) => {
      const av = sortValue(a, column), bv = sortValue(b, column);
      const order = typeof av === 'number' && typeof bv === 'number' ? av - bv : String(av).localeCompare(String(bv), 'pt-BR');
      return order * (state.ascending ? 1 : -1);
    });
  }
  return items;
}

function drawRows() {
  if (!$('#rows')) return;
  renderStats();
  renderColumnMenu();
  const columns = activeColumns(), span = columns.length + 2;
  $('#inventory').style.minWidth = (100 + columns.reduce((n, c) => n + c.width, 0)) + 'px';
  $('#inventory thead').innerHTML = `<tr class="column-groups">${groupHeaders(columns)}</tr>
    <tr><th class="tone-green"><span class="sr-only">Comparar</span></th>${columns.map(columnHeader).join('')}<th class="tone-slate"><span class="sr-only">Detalhes</span></th></tr>`;

  const items = filteredComponents();
  $('#result-count').textContent = plural(items.length, 'componente', 'componentes');
  $('#rows').innerHTML = items.map(c => {
    const open = state.expanded === c.id;
    const cells = columns.map(column => `<td class="cell-${esc(column.group_id)}" style="min-width:${column.width}px">${cellRenderers[column.format](c, column)}</td>`).join('');
    return `<tr class="${open ? 'is-open' : ''}">
        <td><input type="checkbox" data-select="${esc(c.id)}" aria-label="Comparar ${esc(c.name)}" ${state.selected.has(c.id) ? 'checked' : ''}></td>
        ${cells}
        <td><button class="expand" data-expand="${esc(c.id)}" aria-label="${open ? 'Recolher' : 'Expandir'} ${esc(c.name)}" aria-expanded="${open}">${open ? '−' : '+'}</button></td>
      </tr>${open ? `<tr id="detail-${esc(c.id)}"><td colspan="${span}" class="detail-cell">${detail(c)}</td></tr>` : ''}`;
  }).join('') || `<tr><td colspan="${span}" class="empty">Nenhum componente encontrado. Tente outro termo ou remova os filtros.</td></tr>`;
  syncSelection();
  fitDetailWidth();
  if (state.expanded) renderActiveTab();
}

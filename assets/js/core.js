'use strict';
/* Núcleo: utilitários, estado da página, índices do catálogo e acesso ao servidor local opcional.
   Todo o conteúdo vem de window.CATALOG (data/catalog.js), gerado a partir do SQLite. */

const $ = selector => document.querySelector(selector);
const $$ = selector => [...document.querySelectorAll(selector)];
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
const escapeRegExp = text => text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const plural = (n, one, many) => `${n} ${n === 1 ? one : many}`;
const tone = name => `tone-${esc(name || 'slate')}`;

const state = {
  view: 'catalogo',
  category: 'microcontroladores',
  expanded: null,       // id do componente com a ficha aberta
  tab: 'specs',         // aba ativa da ficha aberta
  sortKey: null,
  ascending: true,
  selected: new Set(),  // componentes marcados para comparar (não persiste)
  writable: false,      // true quando a página vem de scripts/server.py
  flash: null,          // mensagem exibida uma vez no histórico: {component, text, error}
};

// Índices recalculados sempre que o catálogo muda (carga inicial ou resposta do servidor).
let C, terms, termByLowerName, termPattern, componentById, familyById, movementTypeById, classRank, glossaryCategoryById, pinGuides;

function loadCatalog(catalog) {
  C = catalog;
  window.CATALOG = catalog;
  if (!C.categories.some(c => c.id === state.category)) state.category = C.categories[0].id;
  terms = new Map(C.glossary.map(t => [t.term, t]));
  // Sinônimos (aliases) apontam para o termo principal: "Quad-SPI" e "QUADSPI" abrem QSPI.
  termByLowerName = new Map(C.glossary.flatMap(t => [t.term, ...(t.aliases || [])].map(name => [name.toLowerCase(), t.term])));
  const names = [...termByLowerName.keys()].sort((a, b) => b.length - a.length);
  termPattern = new RegExp('(?<![\\w])(' + names.map(escapeRegExp).join('|') + ')(?![\\w])', 'gi');
  componentById = new Map(C.components.map(c => [c.id, c]));
  familyById = new Map(C.families.map(f => [f.id, f]));
  movementTypeById = new Map(C.movement_types.map(t => [t.id, t]));
  classRank = new Map(C.processing_classes.map(p => [p.name, p.rank]));
  glossaryCategoryById = new Map(C.glossary_categories.map(c => [c.id, {...c, terms: []}]));
  [...C.glossary].sort((a, b) => a.position - b.position).forEach(t => glossaryCategoryById.get(t.category_id).terms.push(t.term));
  pinGuides = new Map();
  C.pin_guides.forEach(pin => pinGuides.set(pin.guide, [...(pinGuides.get(pin.guide) || []), pin]));
}

const currentCategory = () => C.categories.find(c => c.id === state.category);
const sectorComponents = () => C.components.filter(c => c.category_id === state.category);
const categoryColumns = () => currentCategory().columns || C.table_columns;

/* Transforma os termos do glossário encontrados no texto em botões com explicação. */
function annotate(text) {
  const source = String(text ?? '');
  let result = '', position = 0;
  for (const match of source.matchAll(termPattern)) {
    const name = termByLowerName.get(match[0].toLowerCase());
    result += esc(source.slice(position, match.index))
      + `<button class="term" data-term="${esc(name)}" aria-label="Explicar ${esc(name)}">${esc(match[0])}</button>`;
    position = match.index + match[0].length;
  }
  return result + esc(source.slice(position));
}

/* ---------- formatação ---------- */

const formatBytes = n => n >= 1024 ? `${(n / 1024).toLocaleString('pt-BR')} KiB` : `${n} B`;
const formatNumber = (value, digits) => Number(value).toLocaleString('pt-BR',
  digits == null ? {maximumFractionDigits: 2} : {minimumFractionDigits: digits, maximumFractionDigits: digits});
const formatDate = iso => String(iso).split('-').reverse().join('/');

function today() {
  const d = new Date();
  return [d.getFullYear(), String(d.getMonth() + 1).padStart(2, '0'), String(d.getDate()).padStart(2, '0')].join('-');
}

/* Valor de um campo da ficha (tabela spec_fields) já com unidade. */
function fieldValue(component, field) {
  const value = component[field.key];
  if (value === undefined || value === null || value === '') return '—';
  if (field.format === 'mhz') return `${value} MHz`;
  if (field.format === 'bytes') return formatBytes(value);
  return value;
}

const familyTone = component => familyById.get(component.family)?.tone;

/* ---------- estoque ---------- */

const stockRatio = c => `${c.stock.available}/${c.stock.total}${c.estimated ? '*' : ''}`;

function stockSummary(c) {
  const {available, in_use: inUse, total} = c.stock;
  if (!total) return 'Nenhuma unidade no acervo';
  return `${plural(available, 'disponível', 'disponíveis')} · ${inUse} em uso · ${total} no total${c.estimated ? ' (estimado)' : ''}`;
}

/* Um tipo de movimentação é possível se não deixar saldo negativo (a mesma regra do servidor). */
function movementAllowed(c, type, quantity = 1) {
  const inUse = c.stock.in_use + type.delta_in_use * quantity;
  const available = c.stock.available + (type.delta_total - type.delta_in_use) * quantity;
  return inUse >= 0 && available >= 0;
}

/* ---------- servidor local (scripts/server.py) ---------- */

async function api(path, body) {
  const response = await fetch(path, body === undefined ? {} : {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body),
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || `O servidor respondeu ${response.status}.`);
  return data;
}

/* Por file:// não há servidor: a página fica só para consulta. */
async function detectServer() {
  if (!/^https?:$/.test(window.location?.protocol || '') || typeof fetch !== 'function') return false;
  try {
    return (await api('api/status')).writable === true;
  } catch {
    return false;
  }
}

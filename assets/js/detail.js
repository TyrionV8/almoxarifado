'use strict';
/* Ficha expandida de um componente: cabeçalho, abas e conteúdo de cada aba. */

const DETAIL_TABS = [
  ['specs', 'Especificações'],
  ['history', 'Histórico'],
  ['pins', 'Pinagem'],
  ['reader', 'Datasheet comentado'],
  ['pdf', 'Documento original ↗'],
];

function detail(c) {
  const tabs = DETAIL_TABS.filter(([id]) => !['reader', 'pdf'].includes(id) || c.datasheet).map(([id, label]) => {
    if (id === 'reader' && c.document_kind === 'esquema') label = 'Leitura do esquema';
    const active = state.tab === id;
    const count = id === 'history' ? ` <span class="tab-count">${c.history.length}</span>` : '';
    return `<button role="tab" aria-selected="${active}" class="${active ? 'active' : ''}" data-tab="${id}">${label}${count}</button>`;
  }).join('');
  return `<section class="detail ${tone(familyTone(c))}" data-component="${esc(c.id)}" aria-label="Ficha ${esc(c.name)}">
      <div class="detail-head">
        <div>
          <h2>${esc(c.name)} <span class="badge ${tone(familyTone(c))}">${esc(c.family)}</span> <span class="badge tone-slate">${c.kind === 'chip' ? 'CHIP AVULSO' : 'PLACA'}</span></h2>
          <p>${esc(c.subtitle)}</p>
        </div>
        <button class="stock-strip" data-tab-shortcut="history" title="Abrir histórico">
          <span class="tone-green"><b>${c.stock.available}</b> disponíve${c.stock.available === 1 ? 'l' : 'is'}</span>
          <span class="tone-blue"><b>${c.stock.in_use}</b> em uso</span>
          <span class="tone-slate"><b>${c.stock.total}</b> no total${c.estimated ? '*' : ''}</span>
        </button>
      </div>
      <div class="tabs" role="tablist" aria-label="Detalhes">${tabs}</div>
      <div class="tab-content" role="tabpanel"></div>
    </section>`;
}

function renderActiveTab() {
  const root = $('.detail');
  if (!root) return;
  const c = componentById.get(root.dataset.component), target = root.querySelector('.tab-content');
  switch (state.tab) {
    case 'history': target.innerHTML = historyPanel(c); break;
    case 'pins': target.innerHTML = pinsPanel(c); break;
    case 'reader': loadReader(c, target); break;
    case 'pdf': target.innerHTML = pdfPanel(c); break;
    default: target.innerHTML = specPanel(c);
  }
}

function setTab(tab) {
  state.tab = tab;
  $$('.detail [data-tab]').forEach(button => {
    button.classList.toggle('active', button.dataset.tab === tab);
    button.setAttribute('aria-selected', String(button.dataset.tab === tab));
  });
  renderActiveTab();
}

function specPanel(c) {
  const specs = C.spec_fields.filter(field => field.in_sheet && c[field.key] !== undefined && c[field.key] !== null);
  return `<div class="detail-grid">
      <div class="info-card">
        <h3>Ficha técnica</h3>
        <dl class="spec-list">${specs.map(field => `<dt>${annotate(field.label)}</dt><dd>${annotate(fieldValue(c, field))}</dd>`).join('')}</dl>
      </div>
      <div class="detail-side">
        <div class="info-card">
          <h3>Onde este componente faz sentido</h3><p>${annotate(c.use)}</p>
          <h3>Na sua bancada</h3><p>${annotate(c.notes)}</p>
          <h3>${c.category_id === 'perifericos' ? 'Como conectar' : 'Como programar'}</h3><p>${annotate(c.programmer)}</p>
        </div>
        <p class="source">Inventário: ${esc(c.origin)}.</p>
        ${c.category_id === 'microcontroladores' ? '<p class="source">Frequência máxima não é uma comparação direta de desempenho entre arquiteturas. Capacidades resumidas; limites completos no datasheet.</p>' : ''}
        ${c.evidence ? `<p class="source"><a href="${esc(c.evidence)}" target="_blank">Referência da variante adquirida ↗</a></p>` : ''}
        ${sourceLinks(c)}
      </div>
    </div>`;
}

function sourceLinks(c) {
  const source = C.sources.find(s => s.file.endsWith('/' + c.datasheet));
  const datasheet = source
    ? `<a href="${esc(source.url)}" target="_blank" rel="noreferrer">Fonte do ${c.document_kind === 'esquema' ? 'esquema' : 'datasheet'} ↗</a> · consultada em ${esc(formatDate(source.retrieved))}`
    : c.source_url ? `<a href="${esc(c.source_url)}" target="_blank" rel="noreferrer">Referência do fabricante ↗</a>` : 'Fonte técnica em preparação';
  return `<p class="source">${datasheet}${c.schematic ? ` · <a href="assets/documents/${esc(c.schematic)}" target="_blank">Esquema da placa ↗</a>` : ''}</p>`;
}

/* Várias folhas (campo pinouts) ficam empilhadas na largura total; uma só imagem usa pinout. */
function pinoutFigures(c) {
  return (c.pinouts || [{file: c.pinout}]).map(p => `
    ${p.title ? `<h3 class="pinout-title">${esc(p.title)}</h3>` : ''}
    ${p.notice ? `<div class="notice">${esc(p.notice)}</div>` : ''}
    <a href="assets/pinouts/${esc(p.file)}" target="_blank" aria-label="Ampliar pinagem${p.title ? ' ' + esc(p.title) : ''}">
      <img class="pinout-image${c.pinouts ? ' pinout-sheet' : ''}" src="assets/pinouts/${esc(p.file)}" alt="Mapa de pinagem ${esc(c.name)}${p.title ? ' · ' + esc(p.title) : ''}">
    </a>`).join('');
}

function pinsPanel(c) {
  const orientation = c.kind === 'chip'
    ? 'Vista superior. Entalhe indica a orientação do pino 1.'
    : 'Referência do fabricante; confira revisão e orientação dos conectores.';
  const pins = pinGuides.get(c.pin_guide) || [];
  return `<p>${annotate('Pinout')} · ${orientation}</p>
    ${c.pinout_notice ? `<div class="notice">${esc(c.pinout_notice)}</div>` : ''}
    ${pinoutFigures(c)}
    <p class="source">${c.pinout_credit ? esc(c.pinout_credit) + ' · ' : ''}${c.pinout_source ? `<a href="assets/documents/${esc(c.pinout_source)}" target="_blank">Documento completo de pinagem ↗</a> · ` : ''}Clique no desenho para ampliar. ${c.kind === 'chip' ? 'Funções alternativas completas estão no datasheet.' : 'As ligações da sua montagem podem ocupar pinos deste desenho.'}</p>
    <div class="pin-list">${pins.map(pin => `<button data-term="${esc(pin.term)}">${esc(pin.label)} ⓘ</button>`).join('')}</div>
    ${sourceLinks(c)}`;
}

function pdfPanel(c) {
  const file = `assets/documents/${esc(c.datasheet)}`;
  return `<p><a href="${file}" target="_blank">Abrir PDF em outra aba ↗</a></p>
    <p class="source">O PDF preserva a diagramação original. As explicações interativas estão na aba ${c.document_kind === 'esquema' ? 'Leitura do esquema' : 'Datasheet comentado'}.</p>
    <object class="pdf-frame" data="${file}" type="application/pdf"><p>Visualizador não disponível. Use o link acima ou a leitura comentada.</p></object>`;
}

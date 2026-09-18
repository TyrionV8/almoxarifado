'use strict';
/* Conteúdo de referência: glossário (dialog, tooltip e página Documentação) e ferramentas de gravação. */

const categoryFor = term => glossaryCategoryById.get(terms.get(term)?.category_id);

/* Vizinhos na ordem editorial da categoria (glossary.position). */
function relatedTerms(term) {
  const list = categoryFor(term).terms, at = list.indexOf(term), size = list.length;
  const neighbours = [-1, 1, -2, 2, -3, 3].map(offset => list[(at + offset + size) % size]);
  return [...new Set(neighbours)].filter(name => name && name !== term).slice(0, 5);
}

function termModal(name) {
  const t = terms.get(name);
  if (!t) return;
  const category = categoryFor(t.term);
  $('#tooltip').hidden = true;
  $('#term-content').innerHTML = `
    <div class="term-dialog-head">
      <span class="category-label">${esc(category.icon)} ${esc(category.name)}</span>
      <div class="eyebrow">DOCUMENTAÇÃO DE BANCADA</div>
      <h2>${esc(t.term)}</h2>
      ${t.aliases?.length ? `<p class="term-aliases">Também escrito: ${t.aliases.map(esc).join(' · ')}</p>` : ''}
      <p class="term-meaning">${esc(t.meaning)}</p>
    </div>
    <section class="term-lead"><h3>Em palavras simples</h3><p>${esc(t.short)}</p></section>
    ${t.figure ? `<figure class="term-figure"><a href="${esc(t.figure)}" target="_blank" title="Abrir a figura em tamanho real">
      <img src="${esc(t.figure)}" alt="${esc(t.figure_caption || t.term)}"></a>
      <figcaption>${esc(t.figure_caption || '')}</figcaption></figure>` : ''}
    <div class="term-detail-grid${t.detail.includes('\n\n') ? ' long' : ''}">
      <section><h3>Como funciona e como interpretar</h3>${t.detail.split(/\n\n+/).map(p => `<p>${esc(p)}</p>`).join('')}</section>
      <section class="term-example"><h3>Exemplo no seu acervo</h3><p>${esc(t.example)}</p></section>
    </div>
    <section class="term-reading"><h3>Checklist para usar esta informação</h3>
      <ul>${category.tips.map(tip => `<li>${esc(tip)}</li>`).join('')}</ul>
    </section>
    <section class="term-related"><h3>Termos relacionados</h3>
      <div>${relatedTerms(t.term).map(term => `<button data-term="${esc(term)}">${esc(term)} →</button>`).join('')}</div>
    </section>
    <p class="source"><b>Importante:</b> esta explicação ajuda a interpretar o termo. Para projetar uma ligação ou trabalhar perto de um limite elétrico, confirme valores, condições e pinos no datasheet da variante exata.</p>`;
  if (!$('#term-dialog').open) $('#term-dialog').showModal();
}

function showTip(element) {
  const t = terms.get(element.dataset.term);
  if (!t) return;
  const tip = $('#tooltip');
  tip.innerHTML = `<strong>${esc(t.term)}</strong><span>${esc(t.meaning)}</span><p>${esc(t.short)}</p><small>Clique para ver funcionamento, exemplo e cuidados.</small>`;
  tip.hidden = false;
  const rect = element.getBoundingClientRect();
  tip.style.left = Math.max(8, Math.min(rect.left, innerWidth - 335)) + 'px';
  tip.style.top = Math.max(8, Math.min(rect.bottom + 8, innerHeight - tip.offsetHeight - 10)) + 'px';
}

function documentationView() {
  return `
    <div class="eyebrow">ENTENDA · COMPARE · CONECTE</div>
    <h1>Documentação de bancada</h1>
    <p class="doc-intro">Um guia prático para entender as fichas, escolher um componente e evitar ligações erradas. As ${C.glossary.length} explicações começam em linguagem simples e avançam até cuidados de projeto.</p>
    <section class="doc-diagrams" aria-labelledby="doc-flow-title">
      <div class="doc-section-head">
        <div><span class="section-kicker">ESQUEMAS MENTAIS</span><h2 id="doc-flow-title">Como as partes trabalham juntas</h2></div>
        <p>Os blocos são clicáveis: abra qualquer termo para ver definição, funcionamento, exemplo e cuidados.</p>
      </div>
      <div class="diagram-grid">
        <article class="signal-diagram">
          <h3>Do sensor à ação</h3>
          <div class="flow-row">
            <button data-term="ADC"><b>ADC</b><small>tensão → número</small></button><i>→</i>
            <button data-term="DMA"><b>DMA</b><small>move os dados</small></button><i>→</i>
            <button data-term="SRAM"><b>SRAM</b><small>guarda amostras</small></button><i>→</i>
            <button data-term="CPU"><b>CPU</b><small>processa</small></button>
          </div>
          <div class="flow-branches"><span>resultado →</span>
            <button data-term="PWM">PWM · controla potência</button>
            <button data-term="DAC">DAC · produz tensão</button>
            <button data-term="UART">UART · envia dados</button>
          </div>
          <p>Exemplo: um sensor fornece uma tensão; o conversor analógico-digital (ADC) cria amostras, o acesso direto à memória (DMA) as coloca na memória estática de acesso aleatório (SRAM), e a unidade central de processamento (CPU) calcula a resposta.</p>
        </article>
        <article class="signal-diagram">
          <h3>Do computador ao firmware</h3>
          <div class="flow-row compact">
            <span class="flow-box"><b>Computador</b><small>arquivo do programa</small></span><i>→</i>
            <button data-term="SWD"><b>SWD</b><small>grava e depura</small></button><i>→</i>
            <button data-term="Flash"><b>Flash</b><small>guarda o firmware</small></button><i>→</i>
            <button data-term="Bootloader"><b>Bootloader</b><small>inicia a aplicação</small></button>
          </div>
          <p>A interface depende da família: Serial Wire Debug (SWD) é comum nos STM32; In-Circuit Serial Programming (ICSP) é usado nos PIC. Um bootloader pode permitir atualização sem um depurador dedicado.</p>
        </article>
      </div>
    </section>
    <section class="glossary-browser" aria-labelledby="glossary-title">
      <div class="doc-section-head">
        <div><span class="section-kicker">DICIONÁRIO INTERATIVO</span><h2 id="glossary-title">Todos os termos, com contexto</h2></div>
        <p id="glossary-count" aria-live="polite"></p>
      </div>
      <div class="glossary-toolbar">
        <label class="search"><span>⌕</span><input id="glossary-search" type="search" placeholder="Buscar sigla, significado, exemplo ou aplicação…" aria-label="Buscar documentação"></label>
        <select id="glossary-category" aria-label="Filtrar categoria">
          <option value="">Todas as categorias</option>
          ${C.glossary_categories.map(c => `<option value="${esc(c.id)}">${esc(c.name)}</option>`).join('')}
        </select>
      </div>
      <div id="glossary-items" class="glossary-grid"></div>
    </section>`;
}

function renderGlossary() {
  const category = $('#glossary-category')?.value || '';
  const needle = ($('#glossary-search')?.value || '').toLocaleLowerCase().trim();
  const items = C.glossary.filter(t => (!category || t.category_id === category) && JSON.stringify(t).toLocaleLowerCase().includes(needle));
  $('#glossary-count').textContent = `${items.length} de ${C.glossary.length} termos`;
  $('#glossary-items').innerHTML = items.map(t => {
    const c = categoryFor(t.term);
    return `<button class="glossary-card" data-term="${esc(t.term)}">
      <span class="category-label">${esc(c.icon)} ${esc(c.name)}</span>
      <b>${esc(t.term)}</b>
      <span class="glossary-meaning">${esc(t.meaning)}</span>
      <p>${esc(t.short)}</p>
      <span class="glossary-example"><strong>Exemplo:</strong> ${esc(t.example)}</span>
      <span class="glossary-more">Abrir explicação completa →</span>
    </button>`;
  }).join('') || '<p class="empty">Nenhum termo encontrado. Tente outra palavra ou escolha “Todas as categorias”.</p>';
}

function toolsView() {
  return `
    <div class="eyebrow">PREPARAR · CONECTAR · PROGRAMAR</div>
    <h1>Gravação e conexão</h1>
    <p>As ferramentas que acompanham seus microcontroladores.</p>
    <div class="tools-grid">${C.tools.map(t => `
      <article class="info-card">
        <span class="badge tone-violet">${esc(plural(t.quantity, 'UNIDADE', 'UNIDADES'))}</span>
        <h2>${esc(t.name)}</h2>
        <p>${annotate(t.description)}</p>
        <h3>Uso no acervo</h3>
        <p>${annotate(t.compatibility)}</p>
      </article>`).join('')}
    </div>`;
}

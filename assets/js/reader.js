'use strict';
/* Datasheet comentado: texto extraído do PDF (data/readers/*.js), carregado sob demanda por tag script. */

window.DATASHEETS = window.DATASHEETS || {};

function loadReader(c, target) {
  target.innerHTML = '<p>Carregando documento local…</p>';
  const show = () => {
    if (!target.isConnected) return;
    const pages = window.DATASHEETS[c.datasheet];
    if (!pages) {
      target.innerHTML = '<p>Texto não disponível. Abra o documento original.</p>';
      return;
    }
    target.innerHTML = `
      <div class="reader-controls">
        <button class="pill-button" data-page-step="-1" aria-label="Página anterior">←</button>
        <label>Página <input data-page type="number" value="1" min="1" max="${pages.length}" aria-label="Página do documento"></label>
        <span>de ${pages.length}</span>
        <button class="pill-button" data-page-step="1" aria-label="Próxima página">→</button>
        <input data-find-text type="search" placeholder="Localizar no documento…" aria-label="Buscar no documento">
        <button class="pill-button" data-find-next>Localizar próxima</button>
        <a href="assets/documents/${esc(c.datasheet)}" target="_blank">PDF original ↗</a>
      </div>
      <p class="source">Texto integral extraído; termos do glossário são interativos. Para desenhos, tabelas complexas e símbolos, confira o PDF original.</p>
      <p class="reader-status" aria-live="polite"></p>
      <div class="reader-text"></div>`;
    target.dataset.doc = c.datasheet;
    paintPage(target, 1);
  };
  if (window.DATASHEETS[c.datasheet]) return show();
  const script = document.createElement('script');
  script.src = 'data/readers/' + c.datasheet.replace('.pdf', '.js');
  script.onload = show;
  script.onerror = () => {
    target.innerHTML = `<p>Não foi possível carregar a leitura. <a target="_blank" href="assets/documents/${esc(c.datasheet)}">Abra o PDF local</a>.</p>`;
  };
  document.head.append(script);
}

function paintPage(target, number) {
  const pages = window.DATASHEETS[target.dataset.doc];
  const n = Math.max(1, Math.min(pages.length, Number(number) || 1));
  const text = target.querySelector('.reader-text');
  target.querySelector('[data-page]').value = n;
  text.innerHTML = annotate(pages[n - 1] || 'Página sem texto extraível. Consulte o PDF original.');
  text.scrollTop = 0;
  target.querySelector('[data-page-step="-1"]').disabled = n === 1;
  target.querySelector('[data-page-step="1"]').disabled = n === pages.length;
}

/* Busca circular a partir da página atual. */
function findNext(target) {
  const query = target.querySelector('[data-find-text]').value.toLowerCase().trim();
  const pages = window.DATASHEETS[target.dataset.doc];
  const start = Number(target.querySelector('[data-page]').value);
  let found = -1;
  if (query) {
    for (let i = 0; i < pages.length; i++) {
      const k = (start + i) % pages.length;
      if (pages[k].toLowerCase().includes(query)) { found = k; break; }
    }
  }
  target.querySelector('.reader-status').textContent = found >= 0 ? `Encontrado na página ${found + 1}.` : query ? 'Termo não encontrado.' : 'Digite um termo para buscar.';
  if (found >= 0) paintPage(target, found + 1);
}

'use strict';
/* Navegação, eventos delegados e inicialização. Carregado por último. */

const VIEW_TITLES = {comparar: 'Comparação', glossario: 'Documentação', ferramentas: 'Gravação e conexão'};

function navigate(view) {
  state.view = view;
  $('#tooltip').hidden = true;
  $$('nav [data-view]').forEach(button => button.classList.toggle('active', button.dataset.view === view));
  $('#breadcrumb').textContent = VIEW_TITLES[view] || currentCategory().name;
  if (view === 'catalogo') {
    $('#main').innerHTML = catalogView();
    drawRows();
  } else if (view === 'comparar') {
    renderCompare();
  } else if (view === 'glossario') {
    $('#main').innerHTML = documentationView();
    renderGlossary();
  } else if (view === 'ferramentas') {
    $('#main').innerHTML = toolsView();
  }
  syncSelection();
  window.scrollTo(0, 0);
}

/* Nome e "+" abrem/fecham a ficha; a quantidade abre direto no histórico (e só fecha se ele já estiver aberto). */
function toggleExpanded(id, tab) {
  const closing = state.expanded === id && (!tab || state.tab === tab);
  state.expanded = closing ? null : id;
  state.tab = tab || 'specs';
  drawRows();
}

function showMode() {
  $('#mode-badge').textContent = state.writable ? '● Registro ativo · servidor local' : '● Consulta offline';
  $('#mode-badge').classList.toggle('is-live', state.writable);
  $('#mode-label').textContent = state.writable ? 'Servidor local' : 'Acervo local';
  $('#mode-hint').textContent = state.writable ? 'Registros gravados no SQLite.' : 'Seu próximo projeto começa aqui.';
}

/* Cada botão declara sua ação em data-*; a ordem dos testes segue a especificidade. */
const clickActions = [
  ['data-category', b => { state.category = b.dataset.category; state.expanded = null; state.tab = 'specs'; state.sortKey = null; loadColumnPreferences(); navigate('catalogo'); }],
  ['data-column-move', b => moveColumn(b.dataset.columnMove, b.dataset.direction)],
  ['data-reset-columns', resetColumns],
  ['data-term', b => termModal(b.dataset.term)],
  ['data-view', b => navigate(b.dataset.view)],
  ['data-clear', () => { state.selected.clear(); state.view === 'catalogo' ? drawRows() : renderCompare(); syncSelection(); }],
  ['data-remove', b => { state.selected.delete(b.dataset.remove); renderCompare(); syncSelection(); }],
  ['data-open-history', b => toggleExpanded(b.dataset.openHistory, 'history')],
  ['data-expand', b => toggleExpanded(b.dataset.expand)],
  ['data-sort', b => { state.ascending = state.sortKey === b.dataset.sort ? !state.ascending : true; state.sortKey = b.dataset.sort; drawRows(); }],
  ['data-tab', b => setTab(b.dataset.tab)],
  ['data-tab-shortcut', b => setTab(b.dataset.tabShortcut)],
  ['data-delete-movement', deleteMovement],
  ['data-page-step', b => { const t = b.closest('.tab-content'); paintPage(t, Number(t.querySelector('[data-page]').value) + Number(b.dataset.pageStep)); }],
  ['data-find-next', b => findNext(b.closest('.tab-content'))],
];

document.addEventListener('click', event => {
  if (event.target.closest('.brand')) {
    event.preventDefault();
    return navigate('catalogo');
  }
  const button = event.target.closest('button');
  if (!button) return;
  if (button.classList.contains('close')) return $('#term-dialog').close();
  const action = clickActions.find(([attribute]) => button.hasAttribute(attribute));
  if (action) action[1](button);
});

document.addEventListener('change', event => {
  const target = event.target;
  if (target.dataset.columnToggle) return toggleColumn(target.dataset.columnToggle, target.checked);
  if (target.dataset.select) {
    target.checked ? state.selected.add(target.dataset.select) : state.selected.delete(target.dataset.select);
    return syncSelection();
  }
  if (target.id === 'family' || target.id === 'kind') return drawRows();
  if (target.id === 'glossary-category') return renderGlossary();
  if (target.hasAttribute('data-page')) return paintPage(target.closest('.tab-content'), target.value);
});

document.addEventListener('input', event => {
  if (event.target.id === 'search') drawRows();
  if (event.target.id === 'glossary-search') renderGlossary();
});

document.addEventListener('submit', event => {
  const form = event.target.closest('[data-movement-form]');
  if (!form) return;
  event.preventDefault();
  saveMovement(form);
});

document.addEventListener('keydown', event => {
  if (event.key === 'Escape') $('#tooltip').hidden = true;
  if (!event.target.matches('[role=tab]') || !['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
  event.preventDefault();
  const tabs = [...event.target.parentElement.querySelectorAll('[role=tab]')];
  const current = tabs.indexOf(event.target);
  const next = event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length - 1 : (current + (event.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
  setTab(tabs[next].dataset.tab);
  $$('.detail [role=tab]')[next].focus();
});

document.addEventListener('mouseover', event => { const el = event.target.closest('[data-term]'); if (el) showTip(el); });
document.addEventListener('mouseout', event => { if (event.target.closest('[data-term]')) $('#tooltip').hidden = true; });
document.addEventListener('focusin', event => { if (event.target.dataset.term) showTip(event.target); });
document.addEventListener('focusout', () => { $('#tooltip').hidden = true; });
window.addEventListener('scroll', () => { $('#tooltip').hidden = true; }, true);
window.addEventListener('resize', fitDetailWidth);

/* Clique no fundo escurecido fecha o dialog. */
$('#term-dialog').addEventListener('click', event => {
  const dialog = $('#term-dialog');
  if (event.target !== dialog) return;
  const r = dialog.getBoundingClientRect();
  if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close();
});

loadCatalog(window.CATALOG);
loadColumnPreferences();
navigate('catalogo');
detectServer().then(writable => {
  state.writable = writable;
  showMode();
  if (writable && state.view === 'catalogo') drawRows();
});

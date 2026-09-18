// Simulação de DOM (LinkeDOM): sem navegador, rede, layout ou renderização.
import {parseHTML} from './vendor/linkedom.mjs';
import {readFileSync, existsSync} from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import path from 'node:path';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const html = readFileSync(path.join(root, 'index.html'), 'utf8');
const {window} = parseHTML(html);
const {document} = window;
window.scrollTo = () => {};
const dialog = document.querySelector('dialog');
dialog.showModal = () => { dialog.open = true; };
dialog.close = () => { dialog.open = false; };

const ctx = vm.createContext({window, document, console, innerWidth: 1400, innerHeight: 1000});
// Mesmos scripts, na mesma ordem, que o index.html carrega.
const scripts = [...html.matchAll(/<script defer src="([^"]+)"/g)].map(m => m[1]);
assert.deepEqual(scripts.slice(0, 2), ['data/catalog.js', 'assets/js/core.js']);
for (const script of scripts) vm.runInContext(readFileSync(path.join(root, script), 'utf8'), ctx, {filename: script});
const run = code => vm.runInContext(code, ctx);
await new Promise(resolve => setTimeout(resolve, 0));  // detectServer() conclui: sem servidor, modo consulta
assert.equal(run('state.writable'), false);

const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
const fire = (el, type) => el.dispatchEvent(new window.Event(type, {bubbles: true}));
const click = s => { assert.ok($(s), 'Faltando ' + s); fire($(s), 'click'); };
const input = (s, v) => { $(s).value = v; fire($(s), 'input'); };
const choose = (s, v) => { Object.defineProperty($(s), 'value', {value: v, writable: true, configurable: true}); fire($(s), 'change'); };
const resetSelects = () => $$('select').forEach(node => Object.defineProperty(node, 'value', {value: '', writable: true, configurable: true}));
const count = () => $$('[data-select]').length;
const stockOf = id => $(`[data-open-history="${id}"] .stock-ratio`).textContent;
resetSelects();

// Tabela montada a partir do banco.
assert.equal(count(), 11);
assert.equal($$('#inventory thead tr:last-child th').length, 25);
assert.equal($$('[data-column-toggle]').length, 23);
assert.deepEqual($$('.column-groups th').map(th => th.textContent), ['Acervo', 'Desempenho e memória', 'Periféricos', 'Elétrica', 'Detalhes']);
assert.deepEqual($$('#family option').map(o => o.textContent), ['Todas as famílias', 'PIC', 'AVR', 'STM32']);
assert.match($('#rows').textContent, /Alto desempenho/);
assert.match($('#rows').textContent, /3\.196/);
assert.match($('#rows').textContent, /16MIPS/);
assert.match($('#rows').textContent, /Escala diferente/);
assert.match($('#rows').textContent, /CORDIC/);
assert.match($('#rows').textContent, /USART\/UART/);
assert.match($('#performance-note').textContent, /não devem ser comparados diretamente/);
assert.match($('#performance-note').textContent, /STM32F103RB/);

// Quantidade: disponíveis / total, calculada pelas movimentações.
const catalog = run('C');
const C_TERMS = catalog.glossary.length; // o número exato de termos é conferido em tests/test_inventory.py
for (const c of catalog.components) assert.equal(stockOf(c.id), `${c.stock.available}/${c.stock.total}${c.estimated ? '*' : ''}`);
const sum = key => catalog.components.reduce((n, c) => n + c.stock[key], 0);
assert.match($('.stats').textContent, new RegExp(`${sum('available')}/${sum('total')}`));
assert.equal($('#component-count').textContent, '11');

// Colunas configuráveis.
{
  const toggle = $('[data-column-toggle="accelerators"]');
  toggle.checked = false;
  fire(toggle, 'change');
  assert.equal($('#visible-column-count').textContent, '22/23');
  assert.equal($$('#inventory thead tr:last-child th').length, 24);
}
click('[data-column-move="family"][data-direction="-1"]');
assert.match($('#inventory thead tr:last-child th:nth-child(2)').textContent, /Família/);
click('[data-reset-columns]');
assert.equal($('#visible-column-count').textContent, '23/23');
assert.match($('#inventory thead tr:last-child th:nth-child(2)').textContent, /Componente/);
click('[data-sort="processing_class"]'); click('[data-sort="processing_class"]');
assert.equal($('[data-select]').dataset.select, 'h7r3');
click('[data-sort="dmips"]'); click('[data-sort="dmips"]');
assert.equal($('[data-select]').dataset.select, 'h7r3');

// Busca e filtros.
input('#search', 'PIC12F675'); assert.equal(count(), 1);
input('#search', 'nada-corresponde'); assert.equal(count(), 0); assert.match($('#rows').textContent, /Nenhum/);
input('#search', ''); assert.equal(count(), 11);
choose('#family', 'STM32'); assert.equal(count(), 5);
choose('#family', '');

// Ficha e abas.
click('[data-expand="blackpill"]');
assert.equal($('.detail-cell').getAttribute('colspan'), '25');
assert.match($('.tab-content').textContent, /STM32F411CEU6/);
assert.match($('.tab-content').textContent, /25 MHz/);
click('[data-tab="history"]');
assert.equal($$('.timeline li').length, catalog.components.find(c => c.id === 'blackpill').history.length);
assert.ok($('.read-only'), 'por file:// o histórico é só consulta');
assert.equal($$('.movement-form').length, 0);
assert.equal($$('[data-delete-movement]').length, 0);
click('[data-tab="pins"]');
assert.ok(existsSync(path.join(root, $('.pinout-image').getAttribute('src'))));
assert.ok($$('.pin-list [data-term="SWD"]').length);
click('[data-expand="g474"]'); click('[data-tab="pins"]');
assert.deepEqual($$('.pinout-image').map(i => i.getAttribute('src')), ['assets/pinouts/g474-long-pinout-simple.png', 'assets/pinouts/g474-long-pinout-full.png']);
click('[data-expand="h7r3"]'); click('[data-tab="pins"]');
assert.deepEqual($$('.pinout-image').map(i => i.getAttribute('src')), ['simple', 'full', 'simple-left', 'simple-right', 'full-left', 'full-right', 'full-extra'].map(n => `assets/pinouts/h7-pinout-${n}.png`));
click('[data-expand="h743"]');
assert.ok($('.tab-content [data-term="QSPI"]'), '"Flash QSPI" na ficha vira termo');
click('.tab-content [data-term="QSPI"]');
assert.equal(dialog.open, true);
assert.ok(existsSync(path.join(root, $('.term-figure img').getAttribute('src'))));
assert.match($('#term-content').textContent, /Quad-SPI/);
assert.ok($$('#term-content .term-detail-grid.long p').length >= 4);
click('.close');
click('[data-tab="pins"]');
assert.deepEqual($$('.pinout-image').map(i => i.getAttribute('src')), ['simple', 'full', 'simple-left', 'simple-right', 'full-left', 'full-right', 'full-extra'].map(n => `assets/pinouts/h743-pinout-${n}.png`));
click('[data-expand="bluepill"]'); click('[data-tab="pins"]');
assert.match($('.tab-content .notice').textContent, /micro-USB/);
click('[data-tab="pdf"]');
assert.ok(existsSync(path.join(root, $('object').getAttribute('data'))));
click('[data-expand="bluepill"]');
assert.equal($$('.detail').length, 0);

// Histórico com dados controlados (o banco real muda a cada registro do usuário): Uno com entrada e descarte.
const fixture = JSON.parse(JSON.stringify(catalog));
Object.assign(fixture.components.find(c => c.id === 'uno'), {
  history: [
    {id: 901, type_id: 'entrada', quantity: 1, date: '2026-09-12', note: 'Cadastro inicial.'},
    {id: 902, type_id: 'descarte', quantity: 1, date: '2026-09-13', note: 'Quebrou sem querer.'},
  ],
  stock: {total: 0, in_use: 0, available: 0},
});
ctx.fixture = fixture;
run('loadCatalog(fixture); drawRows()');

// A quantidade abre direto no histórico.
click('[data-open-history="uno"]');
assert.equal($('.detail').dataset.component, 'uno');
assert.equal($('[data-tab="history"]').getAttribute('aria-selected'), 'true');
assert.match($('.timeline').textContent, /Quebrou sem querer/);
assert.match($('.timeline li .timeline-balance').textContent, /^0\/0$/);

// Modo servidor: formulário, bloqueio de tipos impossíveis e atualização com o catálogo devolvido.
{
  const updated = JSON.parse(JSON.stringify(fixture));
  const uno = updated.components.find(c => c.id === 'uno');
  uno.history.push({id: 999, type_id: 'compra', quantity: 2, date: '2026-09-13', note: 'Reposição'});
  uno.stock = {total: 2, in_use: 0, available: 2};
  const calls = [];
  ctx.fetch = async (url, options) => { calls.push({url, body: JSON.parse(options.body)}); return {ok: true, json: async () => ({catalog: updated})}; };
  run('state.writable = true; drawRows()');
  assert.ok($('.movement-form'));
  assert.ok($('[name="type_id"][value="uso"]').hasAttribute('disabled'), 'sem unidades, não dá para colocar em uso');
  assert.ok(!$('[name="type_id"][value="compra"]').hasAttribute('disabled'));
  assert.ok($('[name="type_id"][value="compra"]').hasAttribute('checked'));
  $('[name="type_id"][value="compra"]').checked = true;  // LinkeDOM não reflete o atributo na propriedade
  $('[name="quantity"]').value = '2';
  $('[name="note"]').value = 'Reposição';
  fire($('.movement-form'), 'submit');
  await new Promise(resolve => setTimeout(resolve, 0));
  await new Promise(resolve => setTimeout(resolve, 0));
  assert.equal(calls[0].url, 'api/movements');
  assert.deepEqual({...calls[0].body, date: undefined}, {component_id: 'uno', type_id: 'compra', quantity: 2, note: 'Reposição', date: undefined});
  assert.equal(stockOf('uno'), '2/2');
  assert.match($('.form-flash').textContent, /Registrado/);
  assert.equal($$('.timeline li').length, 3);
  assert.equal($$('[data-delete-movement]').length, 3);
  ctx.originalCatalog = catalog;
  run('state.writable = false; state.expanded = null; loadCatalog(originalCatalog); drawRows()');
}

// Comparação.
for (const id of ['pic12f675', 'g474']) { const c = $(`[data-select="${id}"]`); c.checked = true; fire(c, 'change'); }
assert.equal($('#compare-count').textContent, '2');
click('nav [data-view="comparar"]');
assert.match($('#main').textContent, /PIC12F675/);
assert.match($('#main').textContent, /WeAct G474 Long/);
assert.match($('#main').textContent, /Disponível \/ total/);
assert.ok($$('.different').length > 5);
click('[data-remove="g474"]');
assert.match($('#main').textContent, /pelo menos dois/);

// Documentação (categorias e dicas vêm do banco).
click('nav [data-view="glossario"]');
assert.equal($$('.signal-diagram').length, 2);
assert.equal($$('.glossary-card').length, C_TERMS);
assert.match($('#glossary-count').textContent, new RegExp(`${C_TERMS} de ${C_TERMS}`));
assert.match($('.glossary-card').textContent, /Exemplo:/);
input('#glossary-search', 'analog-to-digital');
assert.equal($$('.glossary-card').length, 1);
click('.glossary-card');
assert.equal(dialog.open, true);
assert.match($('#term-content').textContent, /4096/);
assert.match($('#term-content').textContent, /Como funciona e como interpretar/);
assert.equal($$('.term-reading li').length, 3);
assert.ok($$('.term-related button').length >= 4);
click('.close');
assert.equal(dialog.open, false);
input('#glossary-search', '');
choose('#glossary-category', 'gravacao');
assert.equal($$('.glossary-card').length, 8);
assert.match($('#glossary-count').textContent, new RegExp(`8 de ${C_TERMS}`));

click('nav [data-view="ferramentas"]');
assert.equal($$('.tools-grid article').length, 3);

// Datasheet comentado.
click('nav [data-view="catalogo"]');
resetSelects();
click('[data-expand="pic12f683"]');
vm.runInContext(readFileSync(path.join(root, 'data/readers/pic12f683.js'), 'utf8'), ctx);
click('[data-tab="reader"]');
assert.match($('.reader-text').textContent, /PIC12F683/);
assert.ok($('.reader-text [data-term]'));
click('[data-page-step="1"]');
assert.equal(Number($('[data-page]').value), 2);
input('[data-find-text]', 'oscillator');
click('[data-find-next]');
assert.match($('.reader-status').textContent, /Encontrado/);
$('[data-page]').value = 99999;
fire($('[data-page]'), 'change');
assert.equal(Number($('[data-page]').value), 176);
assert.equal($('[data-page-step="1"]').disabled, true);
click('[data-tab="specs"]');
click('.tab-content [data-term="CPU"]');
assert.equal(dialog.open, true);

console.log('Interface: tabela do banco, quantidade X/X, histórico (consulta e registro), busca, filtros, fichas, pinagem, PDF, comparação, documentação, ferramentas e leitor passaram (DOM simulado).');

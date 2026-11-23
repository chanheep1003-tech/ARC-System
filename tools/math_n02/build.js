// ARC N° math workbook renderer (B/W, 4 items per page: 2 columns x 2 rows)
// KaTeX server-side strict render (any math error aborts) -> HTML -> Playwright PDF
// usage: node build2.js items.json out.pdf "SET 1"
const fs = require('fs');
const path = require('path');
const katex = require('katex');
const { chromium } = require('playwright');

const [,, inFile, outPdf, setName] = process.argv;
const items = JSON.parse(fs.readFileSync(inFile, 'utf8'));
const BOOK = 'ARC N°02';
const COURSE = '공통수학2 기말';
const errors = [];
let mathCount = 0;

function esc(s) { return s.replace(/&(?!(emsp|ensp|nbsp);)/g, '&amp;').replace(/<보기>/g, '\u0001').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\u0001/g, '<span class="nb">〈보기〉</span>'); }

function renderText(s, ctx) {
  const out = [];
  const re = /\$\$([\s\S]+?)\$\$|\$([^$]+?)\$/g;
  let last = 0, m;
  while ((m = re.exec(s))) {
    out.push(esc(s.slice(last, m.index)));
    const tex = m[1] !== undefined ? m[1] : m[2];
    const display = m[1] !== undefined;
    const tex1 = (!display && (tex.length < 64 || tex.includes('begin{cases}'))) ? '{' + tex + '}' : tex;   // short inline math never line-breaks
    const tex2 = tex1.replace(/\\begin\{cases\}/g, '{\\def\\arraystretch{1.5}\\begin{cases}')
                     .replace(/\\end\{cases\}/g, '\\end{cases}}').replace(/\\\\\[\d+pt\]/g, '\\\\');
    mathCount++;
    try {
      out.push(katex.renderToString(tex2, { displayMode: display, throwOnError: true, strict: 'error', output: 'html' }));
    } catch (e) {
      errors.push(`${ctx}: ${e.message} :: ${tex}`);
      out.push('<span class="err">[MATH ERROR]</span>');
    }
    last = re.lastIndex;
  }
  const tail = s.slice(last);
  if (tail.includes('$')) errors.push(`${ctx}: unmatched $ in "${tail}"`);
  out.push(esc(tail));
  return out.join('');
}

const circ = ['①', '②', '③', '④', '⑤'];
function choicesHtml(ch, ctx) {
  const parts = ch.map((c, i) => `<span class="ch"><span class="cn">${circ[i]}</span>&nbsp;${renderText(c.replace(/\\frac/g, '\\dfrac'), ctx)}</span>`);
  const long = ch.some(c => c.includes(',')) || ch.some(c => c.replace(/\$|\\[a-z]+|[{}]/g, '').length > 9);
  const long2 = ch.some(c => c.replace(/\$|\\[a-z]+|[{}]/g, '').length > 14);
  return `<div class="choices ${long2 ? 'long2' : long ? 'long' : ''}">${parts.join('')}</div>`;
}
function boxHtml(lines, titleTxt, ctx) {
  if (!lines) return '';
  const t = titleTxt ? `<div class="boxtitle"><span>${titleTxt}</span></div>` : '';
  const line = l => {
    const m = l.match(/^(\([가-라]\)|[ㄱ-ㅎ]\.|•)\s*([\s\S]*)$/);
    if (m) return `<div class="bl hang"><span class="lab">${m[1]}</span><span class="lbody">${renderText(m[2], ctx)}</span></div>`;
    if (/^&emsp;/.test(l)) return `<div class="bl hang"><span class="lab"></span><span class="lbody">${renderText(l.replace(/^(&emsp;|&nbsp;)+/, ''), ctx)}</span></div>`;
    return `<div class="bl">${renderText(l, ctx)}</div>`;
  };
  return `<div class="box ${titleTxt ? 'titled' : ''}">${t}${lines.map(line).join('')}</div>`;
}
const LV = { D3: 3, D4: 4, D5: 5 };
const LVNAME = { D3: '중상', D4: '상', D5: '최상' };
const stars = d => '★'.repeat(LV[d]) + '☆'.repeat(5 - LV[d]);

function itemHtml(it, n) {
  const ctx = `#${n} ${it.id}`;
  let h = `<div class="q">`;
  h += `<div class="qhead"><span class="qn">${String(n).padStart(2, '0')}</span>`
     + `<span class="meta"><span class="unit">${it.unit}</span><span class="lv">${stars(it.D)}</span></span></div>`;
  h += `<div class="stem">${renderText(it.stem, ctx)}</div>`;
  if (it.fig) {
    const svg = fs.readFileSync(path.join(__dirname, 'figs', it.fig + '.svg'), 'utf8').replace(/<\?xml[^>]*>/, '').replace(/ width="[\d.]+" height="[\d.]+"/, '');
    h += `<div class="fig">${svg}</div>`;
  }
  h += boxHtml(it.box, it.boxtitle, ctx);
  if (it.stem2) h += `<div class="stem">${renderText(it.stem2, ctx)}</div>`;
  if (it.box2) h += boxHtml(it.box2, '보기', ctx);
  if (it.choices) h += choicesHtml(it.choices, ctx);
  h += `<div class="src">${it.id} · ${esc(it.src)}</div></div>`;
  return h;
}

// compact answer key that fits in one cell: 5 columns x ceil(n/5) rows
const keyCols = 5, keyRowsN = Math.ceil(items.length / keyCols);
let keyBody = '';
for (let r = 0; r < keyRowsN; r++) {
  keyBody += '<tr>';
  for (let c = 0; c < keyCols; c++) {
    const i = c * keyRowsN + r;
    if (i < items.length) keyBody += `<td class="kn">${String(i + 1).padStart(2, '0')}</td><td class="ka">${renderText(items[i].ans.replace(/\\frac/g, '\\dfrac'), 'key ' + items[i].id)}</td>`;
    else keyBody += '<td class="kn"></td><td class="ka"></td>';
  }
  keyBody += '</tr>';
}

// slots: all items; then one blank page (skipped); then a full answer-key page
const slots = items.map((it, k) => `<div class="cell">${itemHtml(it, k + 1)}</div>`);
while (slots.length % 4) slots.push('<div class="cell"></div>');
const head = () => `<header><div class="hl"><span class="book">${BOOK}</span><span class="course">${COURSE}</span><span class="set">${setName}</span></div>
    <div class="hr">명제 · 함수 · 유리함수 · 무리함수</div></header>`;
const pages = [];
const pushPage = (body, cls = '') => {
  const pageNo = pages.length + 1;
  pages.push(`<section class="page ${pageNo % 2 ? 'odd' : 'even'} ${cls}">${head()}${body}<footer><span class="pn">${pageNo}</span></footer></section>`);
};
for (let p = 0; p < slots.length; p += 4) pushPage(`<div class="grid">${slots.slice(p, p + 4).join('')}</div>`);
pushPage('<div class="grid blank"></div>', 'blankpage');
pushPage(`<div class="keypage2"><div class="keyhead"><span class="qn">정답</span></div><table class="qkey big">${keyBody}</table></div>`);

const katexCss = path.join(__dirname, 'node_modules/katex/dist/katex.min.css');
const html = `<!doctype html><html lang="ko"><head><meta charset="utf-8">
<link rel="stylesheet" href="file://${katexCss}">
<style>
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #fff; color: #000; }
body { font-family: 'NanumMyeongjo', serif; font-size: 10.2pt; line-height: 1.72; -webkit-print-color-adjust: exact; }
.katex { font-size: 1.07em; }
.katex .text { font-family: KaTeX_Main, 'NanumMyeongjo', serif; }
.sans, header, footer, .qn, .meta, .cn, .src, .boxtitle, .short, .cover, table.key th { font-family: 'NanumSquare', 'NanumBarunGothic', sans-serif; }
.page { width: 210mm; height: 297mm; padding: 11mm 13mm 10mm; position: relative; page-break-after: always; overflow: hidden; display: flex; flex-direction: column; }
header { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2.2pt solid #000; padding-bottom: 2.2mm; }
header::after { content: ''; position: absolute; left: 13mm; right: 13mm; top: calc(11mm + 9.6mm); border-bottom: 0.5pt solid #000; }
.hl { display: flex; align-items: center; gap: 2.5mm; }
.book { background: #000; color: #fff; font-weight: 800; font-size: 9pt; padding: 0.6mm 2.4mm; letter-spacing: 0.3px; }
.course { font-weight: 800; font-size: 11pt; letter-spacing: -0.3px; }
.set { font-size: 9pt; border: 0.8pt solid #000; padding: 0 2mm; font-weight: 700; }
.hr { font-size: 8pt; color: #000; letter-spacing: 0.5px; }
.grid { flex: 1; display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; grid-auto-flow: column; margin-top: 5mm; position: relative; }
.grid::before { content: ''; position: absolute; left: 50%; top: 0; bottom: 0; border-left: 0.6pt solid #000; }
.cell { overflow: hidden; padding: 0 5mm 0 0; }
.cell:nth-child(n+3) { padding: 0 0 0 5mm; }
.cell:nth-child(2), .cell:nth-child(4) { padding-top: 4mm; }
.q { position: relative; }
.qhead { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 2mm; padding-bottom: 0.6mm; }
.qn { font-size: 19pt; font-weight: 800; line-height: 1; letter-spacing: -0.5px; }
.meta { display: flex; align-items: center; gap: 2mm; font-size: 7.6pt; }
.unit { border: 0.6pt solid #000; padding: 0 1.6mm; line-height: 1.55; }
.lv { letter-spacing: 0.4px; font-size: 8pt; }
.stem { text-align: left; word-break: keep-all; overflow-wrap: anywhere; }
.katex-display { margin: 0.4em 0; overflow: visible; }
.box { border: 0.6pt solid #000; padding: 1.6mm 2.6mm; margin: 2mm 0; word-break: keep-all; position: relative; }
.box.titled { margin-top: 3.6mm; padding-top: 2.6mm; }
.boxtitle { position: absolute; top: -2.3mm; left: 0; right: 0; text-align: center; line-height: 1; }
.boxtitle span { background: #fff; padding: 0 2mm; font-size: 8.4pt; font-weight: 700; letter-spacing: 1px; }
.bl { margin: 0.4mm 0; }
.nb { white-space: nowrap; }
.fig { display: flex; justify-content: center; margin: 2mm 0 1mm; }
.fig svg { width: 50mm; height: auto; }
.bl.hang { display: flex; align-items: baseline; }
.bl.hang .lab { flex: none; width: 7.4mm; }
.bl.hang .lbody { flex: 1; min-width: 0; }
.bl.hang .katex-display { margin: 0.1em 0; text-align: left; }
.bl.hang .katex-display > .katex { text-align: left; }
.choices { display: flex; flex-wrap: wrap; column-gap: 1mm; row-gap: 0.6mm; margin-top: 2.6mm; }
.choices .ch { width: calc(20% - 1mm); white-space: nowrap; }
.choices.long .ch { width: calc(33.3% - 1mm); }
.choices.long2 .ch { width: calc(50% - 1mm); }
.choices.long1 .ch { width: 100%; }
.choices .ch { overflow: hidden; }
.choices .katex { font-size: 1.12em; }
.cn { font-size: 10pt; }
.short { margin-top: 3mm; display: flex; justify-content: flex-end; }
.short span { border: 0.6pt solid #000; width: 28mm; height: 7mm; display: inline-flex; align-items: center; padding-left: 2mm; font-size: 8pt; }
.src { font-size: 6.4pt; color: #000; opacity: 0.55; text-align: right; margin-top: 1.4mm; letter-spacing: 0.2px; }
footer { height: 6mm; display: flex; align-items: flex-end; font-size: 8.5pt; font-weight: 700; }
.page.odd footer { justify-content: flex-end; } .page.even footer { justify-content: flex-start; }
.pn { border-top: 1.4pt solid #000; padding: 0.6mm 2mm 0; }
.err { color: #fff; background: #000; }
/* compact key */
.keyhead { margin-bottom: 3mm; }
table.qkey { border-collapse: collapse; width: 100%; font-size: 9pt; }
table.qkey td { border-top: 0.5pt solid #000; border-bottom: 0.5pt solid #000; padding: 1.2mm 0.6mm; text-align: center; height: 8.4mm; }
table.qkey td.kn { font-family: 'NanumSquare', sans-serif; font-weight: 800; font-size: 8pt; width: 6.5mm; }
table.qkey td.ka { width: 11mm; }
table.qkey td.ka .katex { font-size: 0.92em; }
table.qkey td.ka + td.kn { border-left: 0.5pt solid #000; }
/* full key page */
.grid.blank::before { display: none; }
.keypage2 { margin-top: 7mm; flex: 1; }
table.qkey.big { font-size: 10.5pt; }
table.qkey.big td { height: 13mm; padding: 1.5mm 1mm; }
table.qkey.big td.kn { font-size: 9.5pt; width: 12mm; }
table.qkey.big td.ka { width: 22mm; }
table.qkey.big td.ka .katex { font-size: 1.05em; }
/* cover */
.cover { justify-content: flex-start; padding: 34mm 22mm; }
.cv-top .book { font-size: 12pt; padding: 1mm 4mm; }
.cv-title { font-size: 34pt; font-weight: 800; line-height: 1.2; margin-top: 16mm; letter-spacing: -1px; }
.cv-title span { font-size: 22pt; font-weight: 400; letter-spacing: 0; }
.cv-set { display: inline-block; margin-top: 10mm; font-size: 16pt; font-weight: 800; border: 1.4pt solid #000; padding: 1mm 6mm; align-self: flex-start; }
.cv-line { border-top: 2.2pt solid #000; margin: 16mm 0 6mm; }
.cv-tab { border-collapse: collapse; font-size: 10.5pt; width: 100%; }
.cv-tab th { text-align: left; width: 26mm; padding: 2.4mm 0; border-bottom: 0.5pt solid #000; font-weight: 800; }
.cv-tab td { padding: 2.4mm 0; border-bottom: 0.5pt solid #000; }
.cv-foot { margin-top: auto; font-size: 10pt; }
.blank { display: inline-block; width: 46mm; border-bottom: 0.8pt solid #000; height: 5mm; vertical-align: bottom; }
.blank.s { width: 26mm; }
/* key */
.keywrap { display: flex; gap: 8mm; margin-top: 6mm; flex: 1; }
table.key { border-collapse: collapse; font-size: 9pt; flex: 1; align-self: flex-start; }
table.key th, table.key td { border-top: 0.5pt solid #000; border-bottom: 0.5pt solid #000; padding: 1.5mm 2mm; text-align: center; }
table.key thead th { border-top: 1.4pt solid #000; border-bottom: 1pt solid #000; font-weight: 800; }
table.key td.n { font-family: 'NanumSquare', sans-serif; font-weight: 800; }
table.key td.id { font-size: 7.5pt; }
table.key .ans { font-size: 10.5pt; }
</style></head><body>
${pages.join('\n')}
</body></html>`;

(async () => {
  const htmlFile = path.resolve(outPdf).replace(/\.pdf$/, '.html');
  fs.writeFileSync(htmlFile, html);
  console.log(`items: ${items.length}, math segments: ${mathCount}, errors: ${errors.length}`);
  if (errors.length) { errors.forEach(e => console.log('  ERR', e)); process.exit(2); }
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
  await page.emulateMedia({ media: 'print' });
  await page.goto('file://' + htmlFile);
  await page.evaluate(() => document.fonts.ready);
  // adaptive choice layout: 5 per row -> 3 per row -> 2 per row -> 1 per row, until nothing overflows
  await page.evaluate(() => {
    const fits = c => [...c.querySelectorAll('.ch')].every(ch => ch.scrollWidth <= ch.clientWidth + 0.5);
    document.querySelectorAll('.choices').forEach(c => {
      for (const cls of ['', 'long', 'long2', 'long1']) {
        c.classList.remove('long', 'long2', 'long1'); if (cls) c.classList.add(cls);
        if (fits(c)) break;
      }
    });
  });
  const over = await page.evaluate(() => {
    const bad = [];
    document.querySelectorAll('.cell').forEach((c, i) => {
      const q = c.querySelector('.q'); if (!q) return;
      const n = q.querySelector('.qn').textContent;
      const r = c.getBoundingClientRect();
      if (q.scrollHeight > c.clientHeight - (c.style.paddingTop ? 0 : 0) - 2) {
        const avail = c.clientHeight - parseFloat(getComputedStyle(c).paddingTop);
        if (q.getBoundingClientRect().height > avail) bad.push(`#${n} vertical ${Math.round(q.getBoundingClientRect().height)}>${Math.round(avail)}`);
      }
      const inner = { left: r.left + parseFloat(getComputedStyle(c).paddingLeft), right: r.right - parseFloat(getComputedStyle(c).paddingRight) };
      q.querySelectorAll('.katex .base, .ch, .bl, .stem, .box').forEach(k => {
        const b = k.getBoundingClientRect();
        if (b.right > inner.right + 1 || b.left < inner.left - 1) bad.push(`#${n} ${k.className} right=${Math.round(b.right)} col=${Math.round(inner.right)}`);
      });
    });
    document.querySelectorAll('.box').forEach(bx => {
      const br = bx.getBoundingClientRect();
      bx.querySelectorAll('.katex .base, .lbody').forEach(k => {
        const b = k.getBoundingClientRect();
        if (b.right > br.right - 3) bad.push(`box ${bx.closest('.q').querySelector('.qn').textContent} touches border right=${Math.round(b.right)} box=${Math.round(br.right)}`);
      });
    });
    // free solving space per cell (px) for report
    const free = [...document.querySelectorAll('.cell')].filter(c => c.querySelector('.q')).map(c => {
      const avail = c.clientHeight - parseFloat(getComputedStyle(c).paddingTop);
      return Math.round(avail - c.querySelector('.q').getBoundingClientRect().height);
    });
    const cells=[...document.querySelectorAll('.cell')].filter(c => c.querySelector('.q'));
    const mi=free.indexOf(Math.min(...free));
    return { bad, minFree: Math.min(...free) + ' (#' + cells[mi].querySelector('.qn').textContent + ')' };
  });
  console.log(`overflow: ${over.bad.length}, min free space in a cell: ${over.minFree}px`); over.bad.forEach(o => console.log('  OVF', o));
  await page.pdf({ path: outPdf, width: '210mm', height: '297mm', printBackground: true, preferCSSPageSize: true });
  await browser.close();
  process.exit(over.bad.length ? 3 : 0);
})();

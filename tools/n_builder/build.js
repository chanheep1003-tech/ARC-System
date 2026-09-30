'use strict';
// ARC_N builder: passages/*.txt + items/*.items -> 문제지 PDF + 답지 PDF (A4, Chromium print).
// Usage: node build.js [--no 03] [--ver 1.0] [--only 01,02] [--skip-answer]
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');
const { PDFDocument } = require('pdf-lib');
const P = require('./lib/parse');
const CSS = require('./lib/css');

const args = process.argv.slice(2);
const opt = (k, d) => {
  const i = args.indexOf('--' + k);
  return i >= 0 ? args[i + 1] : d;
};
const NO = opt('no', '03');
const VER = opt('ver', '1.0');
const ONLY = (opt('only', '') || '').split(',').filter(Boolean);
const ROOT = path.resolve(__dirname, '../../output');
const BUILD = path.join(ROOT, 'build');
const DIST = path.join(ROOT, 'dist');
fs.mkdirSync(BUILD, { recursive: true });
fs.mkdirSync(DIST, { recursive: true });

const SUBJECT = '공통국어2';
const SCHOOL = '동북고등학교';
const PERIOD = '2학기 중간고사 대비';
const YEAR = '2026';

const SECTIONS = [
  { id: '01', short: '제망매가', unit: '1단원', genre: '향가' },
  { id: '02', short: '속미인곡', unit: '1단원', genre: '가사' },
  { id: '03', short: '춘향전', unit: '1단원', genre: '고전 소설' },
  { id: '04', short: '수라', unit: '1단원', genre: '현대시' },
  { id: '05', short: '아홉 켤레의 구두로 남은 사내', unit: '1단원', genre: '현대 소설' },
  { id: '06', short: '반려견 보호자 자격시험을 의무화하자', unit: '2단원', genre: '논증하는 글' },
  { id: '07', short: '우리 학교 아래로 고속 철도가 지나간다고?', unit: '2단원', genre: '협상 대화' },
  { id: '08', short: '탄궁가', unit: '보충', genre: '가사' },
  { id: '09', short: '팔원', unit: '보충', genre: '현대시' },
  { id: '10', short: '기억할 만한 지나침', unit: '보충', genre: '현대시' },
  { id: '11', short: '칸트·헤겔의 자율성', unit: '보충', genre: '비문학' },
];
const PER = 10;
const rng = (i) => `${String(i * PER + 1).padStart(2, '0')}~${String((i + 1) * PER).padStart(2, '0')}`;

const doc = (body, extraCss = '') =>
  `<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>${CSS}${extraCss}</style></head><body>${body}</body></html>`;

const headerTpl = (right) =>
  `<div style="width:100%;padding:8.6mm 16.5mm 0;font-family:Pretendard,'Noto Sans KR',sans-serif;font-size:6.9pt;color:#666c74;-webkit-print-color-adjust:exact;">` +
  `<div style="display:flex;justify-content:space-between;align-items:flex-end;border-bottom:.45pt solid #d9dbde;padding-bottom:1.6mm;">` +
  `<span style="font-family:Inter,sans-serif;font-weight:700;letter-spacing:.07em;color:#1F2A44;">ARC N°${NO}</span><span>${right}</span></div></div>`;
const footerTpl =
  `<div style="width:100%;text-align:center;font-family:Inter,sans-serif;font-size:7pt;color:#687078;-webkit-print-color-adjust:exact;">` +
  `<span style="display:inline-block;width:2mm;height:.7mm;background:#7A2E35;margin-right:1.8mm;vertical-align:2px;"></span><span class="pageNumber"></span></div>`;

function load(idx) {
  const s = SECTIONS[idx];
  const pf = path.join(ROOT, 'passages', `${s.id}.txt`);
  const itf = path.join(ROOT, 'items', `${s.id}.items`);
  if (!fs.existsSync(pf) || !fs.existsSync(itf)) return null;
  const passage = P.parsePassage(pf);
  const items = P.parseItems(itf);
  const errs = P.validateItems(items, s.id);
  if (errs.length) throw new Error('ITEM VALIDATION FAILED:\n' + errs.join('\n'));
  if (items.length !== PER) throw new Error(`${s.id}: expected ${PER} items, got ${items.length}`);
  return { s, idx, passage, items };
}

function questionSectionHtml(d) {
  const start = d.idx * PER + 1;
  const band = `<div class="band"><span class="rng">[${rng(d.idx)}]</span>다음 글을 읽고 물음에 답하시오.</div>`;
  const qs = d.items.map((it, i) => P.itemHtml(it, start + i)).join('\n');
  return `<div class="sec">${band}${P.passageHtml(d.passage)}${qs}</div>`;
}

function coverHtml(kind, sections) {
  const sub = kind === 'answer' ? '정답 및 해설' : `지문 ${sections.length}개 · ${sections.length * PER}문항`;
  const cover =
    `<section class="page cover"><div class="kicker">ARC N°${NO}</div><div class="toprule"></div><div class="accent"></div>` +
    `<div class="covermain"><h1>${SUBJECT}</h1><div class="csub">${sub}</div>` +
    `<div class="covermeta"><strong>${SCHOOL}</strong><br>${PERIOD}</div></div>` +
    `<div class="year">${YEAR}</div><div class="series">ARC ACADEMIC SERIES</div></section>`;
  if (kind === 'answer') return cover;
  const rows = sections
    .map(
      (d) =>
        `<tr><td class="no">${String(d.idx + 1).padStart(2, '0')}</td><td>${P.esc(d.s.short)}</td><td class="gen">${d.s.unit} · ${d.s.genre}</td><td class="rng">${rng(d.idx)}</td></tr>`
    )
    .join('');
  const toc =
    `<section class="page tocpage"><div class="toctitle">차례</div><table class="toc">${rows}</table>` +
    `<div class="tocnote">지문별로 지문 전문과 5지선다 ${PER}문항이 이어집니다.</div></section>`;
  return cover + toc;
}

function answerBodyHtml(sections) {
  const tables = sections
    .map((d) => {
      const start = d.idx * PER + 1;
      const th = d.items.map((_, i) => `<th>${String(start + i).padStart(2, '0')}</th>`).join('');
      const td = d.items.map((it) => `<td class="a">${P.CIRC[it.answer - 1]}</td>`).join('');
      return `<table class="atable"><caption>[${rng(d.idx)}] ${P.esc(d.s.short)}</caption><tr>${th}</tr><tr>${td}</tr></table>`;
    })
    .join('');
  const bandTop = `<div class="band" style="column-span:all"><span class="rng">정답표</span></div>`;
  const first = `<div class="sec" style="column-count:1;margin-bottom:0">${bandTop}${tables}</div>`;
  const exp = sections
    .map((d) => {
      const start = d.idx * PER + 1;
      const band = `<div class="band"><span class="rng">[${rng(d.idx)}]</span>${P.esc(d.s.short)}<span class="sm">${d.s.unit} · ${d.s.genre}</span></div>`;
      const ex = d.items
        .map((it, i) => {
          const n = String(start + i).padStart(2, '0');
          const lines = it.expl
            .map(
              (e, k) =>
                `<div class="exl${k === it.answer - 1 ? ' c' : ''}"><span class="cn">${P.CIRC[k]}</span><span class="t">${P.inline(e)}</span></div>`
            )
            .join('');
          return `<div class="ex"><div class="exh">${n}<span class="ans">정답 ${P.CIRC[it.answer - 1]}</span><span class="meta">${P.esc(it.kind || '')}</span></div>${lines}</div>`;
        })
        .join('');
      return `<div class="sec">${band}${ex}</div>`;
    })
    .join('');
  return first + exp;
}

async function pdfOf(browser, html, name, { header, footer, margin, css } = {}) {
  const file = path.join(BUILD, name + '.html');
  fs.writeFileSync(file, html);
  const page = await browser.newPage();
  await page.goto('file://' + file);
  await page.evaluate(() => document.fonts.ready);
  const out = path.join(BUILD, name + '.pdf');
  const useHF = !!header;
  await page.pdf({
    path: out,
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: !useHF,
    displayHeaderFooter: useHF,
    headerTemplate: header || '<span></span>',
    footerTemplate: footer || '<span></span>',
    margin: useHF ? { top: '19mm', bottom: '15.5mm', left: '16.5mm', right: '16.5mm' } : { top: 0, bottom: 0, left: 0, right: 0 },
  });
  await page.close();
  return out;
}

const pageCount = async (f) => (await PDFDocument.load(fs.readFileSync(f))).getPageCount();

async function appendPages(dst, srcFile, from = 0) {
  const src = await PDFDocument.load(fs.readFileSync(srcFile));
  const idx = src.getPageIndices().slice(from);
  const pages = await dst.copyPages(src, idx);
  pages.forEach((p) => dst.addPage(p));
  return idx.length;
}

(async () => {
  const wanted = SECTIONS.map((_, i) => i).filter((i) => !ONLY.length || ONLY.includes(SECTIONS[i].id));
  const data = wanted.map(load).filter(Boolean);
  if (!data.length) throw new Error('no sections with both passage and items');
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
  try {
    // ---- 문제지 ----
    const sectionFiles = [];
    let offset = 0;
    for (const d of data) {
      const right = `${SUBJECT} · ${d.s.unit} ${P.esc(d.s.short.length > 26 ? d.s.short.slice(0, 26) + '…' : d.s.short)}`;
      const body = questionSectionHtml(d);
      const blank = (n) => '<div style="height:1px;break-after:page"></div>'.repeat(n);
      // pass 1: count pages
      const f1 = await pdfOf(browser, doc(body), `q_${d.s.id}_p1`, { header: headerTpl(right), footer: footerTpl });
      const n = await pageCount(f1);
      // pass 2: page numbers continue across sections (blank lead pages are dropped when merging)
      const f2 = await pdfOf(browser, doc(blank(offset) + body), `q_${d.s.id}_p2`, { header: headerTpl(right), footer: footerTpl });
      sectionFiles.push({ f: f2, skip: offset, n });
      console.log(`section ${d.s.id} ${d.s.short}: ${n} pages (start p.${offset + 1})`);
      offset += n;
    }
    const cover = await pdfOf(browser, doc(coverHtml('q', data)), 'q_cover');
    const qdoc = await PDFDocument.create();
    await appendPages(qdoc, cover);
    for (const s of sectionFiles) await appendPages(qdoc, s.f, s.skip);
    const qname = `ARC_N°${NO}_${SUBJECT}_지문${data.length}개_V${VER}.pdf`;
    fs.writeFileSync(path.join(DIST, qname), await qdoc.save());
    console.log('WROTE', qname, qdoc.getPageCount(), 'pages');

    // ---- 답지 ----
    if (!args.includes('--skip-answer')) {
      const acover = await pdfOf(browser, doc(coverHtml('answer', data)), 'a_cover');
      const abody = await pdfOf(browser, doc(answerBodyHtml(data)), 'a_body', {
        header: headerTpl(`${SUBJECT} · 정답 및 해설`),
        footer: footerTpl,
      });
      const adoc = await PDFDocument.create();
      await appendPages(adoc, acover);
      await appendPages(adoc, abody);
      const aname = `ARC_N°${NO}_${SUBJECT}_지문${data.length}개_답지_V${VER}.pdf`;
      fs.writeFileSync(path.join(DIST, aname), await adoc.save());
      console.log('WROTE', aname, adoc.getPageCount(), 'pages');
    }
  } finally {
    await browser.close();
  }
})().catch((e) => {
  console.error(e);
  process.exit(1);
});

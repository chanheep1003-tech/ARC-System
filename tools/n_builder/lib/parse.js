'use strict';
// Parsers for passage (.txt) and item (.items) source files. No passage text lives in this repo.
const fs = require('fs');

const CIRC = ['①', '②', '③', '④', '⑤'];

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const inline = (s) =>
  esc(s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>').replace(/\*(.+?)\*/g, '<i>$1</i>');

function parsePassage(file) {
  const raw = fs.readFileSync(file, 'utf8').replace(/\r/g, '');
  const [head, ...rest] = raw.split(/^---\s*$/m);
  const meta = {};
  head.split('\n').forEach((l) => {
    const m = l.match(/^(TITLE|SOURCE|KIND):\s*(.*)$/);
    if (m) meta[m[1]] = m[2].trim();
  });
  const bodyAll = rest.join('---');
  const notesM = bodyAll.split(/^---NOTES\s*$/m);
  let body = notesM[0];
  let notes = [];
  let extra = null;
  let tail = notesM[1] || '';
  const extraSplit = (notesM[0] + '\n' + tail).split(/^---EXTRA:(.*)$/m);
  if (extraSplit.length > 1) {
    // EXTRA may come after body (with or without NOTES)
    const idxBody = body.split(/^---EXTRA:(.*)$/m);
    body = idxBody[0];
    const title = idxBody[1] || extraSplit[1];
    const text = (idxBody[2] || extraSplit[2] || '').trim();
    extra = { title: title.trim(), text };
    tail = tail.split(/^---EXTRA:/m)[0];
  }
  notes = tail.split('\n').map((s) => s.trim()).filter(Boolean);
  return { meta, body: body.trim('\n'), notes, extra };
}

function blockHtml(block, kind) {
  const lines = block.split('\n').filter((l) => l.trim() !== '');
  if (!lines.length) return '';
  if (kind === 'poem') {
    return `<div class="stanza">${lines.map((l) => `<div class="pl">${inline(l)}</div>`).join('')}</div>`;
  }
  const first = lines[0];
  let m;
  if (/^\*\*\([가-힣]\)\*\*$/.test(first)) return `<div class="plabel">${inline(first.replace(/\*\*/g, ''))}</div>`;
  // A heading line may be directly followed by list/paragraph lines in the same block: emit both.
  if ((m = first.match(/^### (.*)$/)) || (m = first.match(/^## (.*)$/))) {
    const tag = first.startsWith('### ') ? '<h4 class="sub2">' : '<h3 class="sub">';
    const close = first.startsWith('### ') ? '</h4>' : '</h3>';
    const head = `${tag}${inline(m[1])}${close}`;
    const rest = lines.slice(1).join('\n');
    return rest ? head + blockHtml(rest, kind) : head;
  }
  if (lines.every((l) => /^- /.test(l))) {
    return `<ul class="bl">${lines.map((l) => `<li>${inline(l.slice(2))}</li>`).join('')}</ul>`;
  }
  if (lines.every((l) => /^\d+\. /.test(l))) {
    return `<div class="nl">${lines
      .map((l) => {
        const mm = l.match(/^(\d+\.) (.*)$/);
        return `<div><span class="n">${mm[1]}</span><span>${inline(mm[2])}</span></div>`;
      })
      .join('')}</div>`;
  }
  if (/^> /.test(first)) {
    const t = first.slice(2);
    const mm = t.match(/^((?:앞부분|중략 부분) 줄거리)\s*(.*)$/);
    return mm
      ? `<div class="summary"><b>${esc(mm[1])}</b> ${inline(mm[2])}</div>`
      : `<div class="summary">${inline(t)}</div>`;
  }
  const hasAnno = lines.some((l) => /^\*\(.*\)\*$/.test(l));
  if (hasAnno) {
    return `<p>${lines
      .map((l) => (/^\*\(.*\)\*$/.test(l) ? `<span class="anno">${esc(l.slice(1, -1))}</span>` : inline(l)))
      .join('<br>')}</p>`;
  }
  if (lines.length > 1) return `<p class="verse">${lines.map(inline).join('<br>')}</p>`;
  return `<p>${inline(first)}</p>`;
}

function passageHtml(p) {
  const kind = p.meta.KIND === 'poem' ? 'poem' : 'prose';
  const blocks = p.body.split(/\n\s*\n/);
  const bodyHtml = blocks.map((b) => blockHtml(b, kind)).join('\n');
  const src = (p.meta.SOURCE || '').replace(/\s*·\s*2025 기출/, '');
  const notes = p.notes.length
    ? `<div class="pnotes"><div class="pnh">주석</div>${p.notes.map((n) => `<div class="pn">${inline(n)}</div>`).join('')}</div>`
    : '';
  const extra = p.extra
    ? `<div class="pextra"><div class="pnh">${esc(p.extra.title)}</div><p>${inline(p.extra.text)}</p></div>`
    : '';
  return (
    `<div class="passage kind-${kind}">` +
    `<div class="ptitle">${inline(p.meta.TITLE)}</div>` +
    `<div class="psrc">출처: ${esc(src)}</div>` +
    `<div class="pbody">${bodyHtml}</div>${notes}${extra}</div>`
  );
}

function parseItems(file) {
  const txt = fs.readFileSync(file, 'utf8').replace(/\r/g, '');
  const chunks = txt.split(/^### Q\s*$/m).slice(1);
  return chunks.map((ch, idx) => {
    const it = { tag: '', stem: '', boxLabel: '', box: [], choices: [], answer: 0, expl: [] };
    for (const line of ch.split('\n')) {
      const m = line.match(/^(T|S|BOX|B|A|E[1-5]|[1-5]):\s?(.*)$/);
      if (!m) continue;
      const [, k, v] = m;
      if (k === 'T') it.tag = v;
      else if (k === 'S') it.stem = v;
      else if (k === 'BOX') it.boxLabel = v;
      else if (k === 'B') it.box.push(v);
      else if (k === 'A') it.answer = parseInt(v, 10);
      else if (k[0] === 'E') it.expl[parseInt(k[1], 10) - 1] = v;
      else it.choices[parseInt(k, 10) - 1] = v;
    }
    const [diff, kind, note] = it.tag.split('|').map((s) => s.trim());
    it.diff = diff;
    it.kind = kind;
    it.note = note;
    it.local = idx + 1;
    return it;
  });
}

function validateItems(items, label) {
  const errs = [];
  items.forEach((it) => {
    const w = `${label} Q${it.local}`;
    if (!it.stem) errs.push(`${w}: no stem`);
    if (it.choices.length !== 5 || it.choices.some((c) => !c)) errs.push(`${w}: choices != 5`);
    if (!(it.answer >= 1 && it.answer <= 5)) errs.push(`${w}: bad answer`);
    for (let i = 0; i < 5; i++) if (!it.expl[i]) errs.push(`${w}: missing E${i + 1}`);
    if (!/^D[3-5]$/.test(it.diff || '')) errs.push(`${w}: diff not D3-D5 (${it.diff})`);
    if (new Set(it.choices).size !== it.choices.length) errs.push(`${w}: duplicate choices`);
    if (it.expl[it.answer - 1] && !it.expl[it.answer - 1].startsWith('○')) errs.push(`${w}: answer expl must start with ○`);
    it.expl.forEach((e, i) => {
      if (i !== it.answer - 1 && e && !e.startsWith('×')) errs.push(`${w}: E${i + 1} must start with ×`);
    });
  });
  return errs;
}

function itemHtml(it, no) {
  const n = String(no).padStart(2, '0');
  const box = it.box.length
    ? `<div class="box">${it.boxLabel ? `<div class="boxlabel">${esc(it.boxLabel)}</div>` : ''}${it.box
        .map((b) => `<div class="bl2">${esc(b)}</div>`)
        .join('')}</div>`
    : '';
  const ch = it.choices
    .map((c, i) => `<div class="choice"><span class="cn">${CIRC[i]}</span><span>${esc(c)}</span></div>`)
    .join('');
  return `<article class="q"><div class="qnum">${n}</div><div class="stem">${esc(it.stem)}</div>${box}<div class="choices">${ch}</div></article>`;
}

module.exports = { parsePassage, passageHtml, parseItems, validateItems, itemHtml, esc, inline, CIRC };

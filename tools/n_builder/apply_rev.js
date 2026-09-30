'use strict';
// Apply revision overlays (output/items/rev/NN.rev) onto output/items/NN.items.
// A rev block "### Q<n>" replaces only the keys it lists (T,S,BOX,B*,1-5,A,E1-E5); any B: line replaces the whole box.
const fs = require('fs');
const path = require('path');
const P = require('./lib/parse');
const dir = path.resolve(__dirname, '../../output/items');
const id = process.argv[2];
if (!id) throw new Error('usage: node apply_rev.js NN');
const src = path.join(dir, `${id}.items`);
// NN.rev first, then NNb.rev, NNc.rev ... (later overlays win)
const revFiles = fs
  .readdirSync(path.join(dir, 'rev'))
  .filter((f) => new RegExp(`^${id}[a-z]?\\.rev$`).test(f))
  .sort()
  .map((f) => path.join(dir, 'rev', f));
if (!revFiles.length) throw new Error(`no rev files for ${id}`);
fs.mkdirSync(path.join(dir, 'orig'), { recursive: true });
const bak = path.join(dir, 'orig', `${id}.items`);
if (!fs.existsSync(bak)) fs.copyFileSync(src, bak);
const items = P.parseItems(bak); // always rebuild from the original + overlay
const txt = revFiles.map((f) => fs.readFileSync(f, 'utf8').replace(/\r/g, '')).join('\n\n');
txt.split(/^### Q(\d+)\s*$/m).slice(1).reduce((acc, v, i, arr) => {
  if (i % 2 === 0) acc.push([parseInt(v, 10), arr[i + 1]]);
  return acc;
}, []).forEach(([n, body]) => {
  const it = items[n - 1];
  if (!it) throw new Error(`rev Q${n} out of range`);
  let boxReset = false;
  for (const line of body.split('\n')) {
    const m = line.match(/^(T|S|BOX|B|A|E[1-5]|[1-5]):\s?(.*)$/);
    if (!m) continue;
    const [, k, v] = m;
    if (k === 'T') { it.tag = v; const [d, kd, nt] = v.split('|').map((s) => s.trim()); it.diff = d; it.kind = kd; it.note = nt; }
    else if (k === 'S') it.stem = v;
    else if (k === 'BOX') it.boxLabel = v;
    else if (k === 'B') { if (!boxReset) { it.box = []; boxReset = true; } it.box.push(v); }
    else if (k === 'A') it.answer = parseInt(v, 10);
    else if (k[0] === 'E') it.expl[parseInt(k[1], 10) - 1] = v;
    else it.choices[parseInt(k, 10) - 1] = v;
  }
});
const out = items.map((it) => {
  const L = ['### Q', `T: ${it.tag}`, `S: ${it.stem}`];
  if (it.box.length) { if (it.boxLabel) L.push(`BOX: ${it.boxLabel}`); it.box.forEach((b) => L.push(`B: ${b}`)); }
  it.choices.forEach((c, i) => L.push(`${i + 1}: ${c}`));
  L.push(`A: ${it.answer}`);
  it.expl.forEach((e, i) => L.push(`E${i + 1}: ${e}`));
  return L.join('\n');
}).join('\n\n') + '\n';
fs.writeFileSync(src, out);
const errs = P.validateItems(P.parseItems(src), id);
console.log(id, 'applied;', errs.length ? errs.join('\n') : 'valid');

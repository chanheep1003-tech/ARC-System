'use strict';
// Item-level QC over all output/items/*.items (numbering, answer spread, length bias, difficulty mix).
const fs = require('fs');
const path = require('path');
const P = require('./lib/parse');
const dir = path.resolve(__dirname, '../../output/items');
const files = fs.readdirSync(dir).filter((f) => f.endsWith('.items')).sort();
let all = [];
const errs = [];
files.forEach((f) => {
  const its = P.parseItems(path.join(dir, f));
  errs.push(...P.validateItems(its, f));
  its.forEach((it) => all.push({ f, ...it }));
});
const cnt = (arr, key) => arr.reduce((m, x) => ((m[key(x)] = (m[key(x)] || 0) + 1), m), {});
console.log('files', files.length, 'items', all.length, 'errors', errs.length);
errs.forEach((e) => console.log(' ', e));
console.log('answers', JSON.stringify(cnt(all, (x) => x.answer)));
console.log('diff', JSON.stringify(cnt(all, (x) => x.diff)));
console.log('per-file diff', JSON.stringify(Object.fromEntries(files.map((f) => [f, cnt(all.filter((x) => x.f === f), (x) => x.diff)]))));
// length bias: is the answer the longest choice?
let longest = 0, top2 = 0;
const biased = [];
all.forEach((x) => {
  const lens = x.choices.map((c) => c.length);
  const max = Math.max(...lens);
  const rank = [...lens].sort((a, b) => b - a).indexOf(lens[x.answer - 1]);
  if (lens[x.answer - 1] === max) { longest++; biased.push(`${x.f}#${x.local}`); }
  if (rank <= 1) top2++;
});
console.log(`answer is longest: ${longest}/${all.length}; in top2: ${top2}/${all.length}`);
console.log('longest-answer items:', biased.join(' '));
// stem type balance
const neg = all.filter((x) => /않은|않는|아닌|일치하지/.test(x.stem)).length;
console.log('negative-stem items', neg);
console.log('kinds', JSON.stringify(cnt(all, (x) => (x.kind || '').split('|')[0])));
// consecutive same answer
files.forEach((f) => {
  const a = all.filter((x) => x.f === f).map((x) => x.answer);
  for (let i = 2; i < a.length; i++) if (a[i] === a[i - 1] && a[i] === a[i - 2]) console.log('3-in-row', f, i);
});

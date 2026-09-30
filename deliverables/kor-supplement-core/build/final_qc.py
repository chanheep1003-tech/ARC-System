#!/usr/bin/env python3
"""최종 PDF 자동 검수. 실행 결과는 검수 메모에 그대로 옮긴다."""
import sys, os, re, collections, json
import pymupdf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B
pdf = sys.argv[1]
d = pymupdf.open(pdf)
res = {}
res['pages'] = len(d)
res['page_budget_ok'] = len(d) <= 40

# ---- fonts
fonts = collections.Counter(); bad_weight = []
for pg in d:
    for f in pg.get_fonts():
        n = f[3].split('+')[-1]; fonts[n] += 1
        if re.search(r'Thin|ExtraLight|Light', n): bad_weight.append(n)
res['fonts'] = dict(fonts); res['thin_or_light_fonts'] = bad_weight
res['type3_fonts'] = sum(1 for pg in d for f in pg.get_fonts() if f[2] == 'Type3')

# ---- sizes / fallback chars / overlap / margins
sizes = collections.Counter(); minsize = 99; fallback = collections.defaultdict(set)
overlap = []; margin = []
MM = 72/25.4
for i, pg in enumerate(d):
    words = pg.get_text('words')
    rects = [pymupdf.Rect(w[:4]) for w in words]
    for b in pg.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                if s['text'].strip():
                    sizes[round(s['size'], 1)] += len(s['text'])
                    minsize = min(minsize, s['size'])
                    if not re.search(r'Pretendard|NotoSansKR', s['font']):
                        for ch in s['text']:
                            if ch.strip(): fallback[s['font']].add(ch)
    # overlap of word boxes (ignoring tiny)
    for a in range(len(rects)):
        for b2 in range(a+1, len(rects)):
            inter = rects[a] & rects[b2]
            if not inter.is_empty and inter.width > 1.2 and inter.height > 1.2:
                overlap.append((i+1, words[a][4], words[b2][4]))
    for w in words:
        if w[2] > 210*MM - 17*MM + 1.5 or w[0] < 17*MM - 1.5 or w[3] > 297*MM - 6*MM: margin.append((i+1, w[4]))
res['body_size_mode_pt'] = sizes.most_common(3)
res['min_font_pt'] = round(minsize, 2)
res['fallback_fonts'] = {k: ''.join(sorted(v)) for k, v in fallback.items()}
res['overlaps'] = overlap[:5]; res['overlap_count'] = len(overlap)
res['margin_violations'] = margin[:5]; res['margin_violation_count'] = len(margin)

# ---- raw markup / metadata leaks
leak_tokens = ['⟦','⟧','¬',':::','**','__','<b>','</b>','<br','<span','&nbsp;','&amp;','&lt;','undefined','NaN','[object',
               'CONCEPT_ID','N_LINK','N°','FOUNDATION','APPLICATION','SOURCE_','BANK','QC_','DEPTH','TRAP_EVIDENCE','drive.google','file_id']
full = '\n'.join(pg.get_text() for pg in d)
res['leaks'] = [t for t in leak_tokens if t in full]

# ---- source text fidelity: every source line/paragraph must appear in the PDF in order
def norm(t): return re.sub(r'\s+', '', t)
fid = {}
for key, cfg in B.WORKS.items():
    s = B.SOURCES[key]
    ptxt = norm(full)
    ok = True; missing = []
    units = [s['lines'][n] for n in sorted(s['lines'])] if s['kind'] == 'poem' else s['paras']
    pos = 0
    for u in units:
        k = ptxt.find(norm(u), pos)
        if k < 0: ok = False; missing.append(u[:24])
        else: pos = k + len(norm(u))
    notes_ok = all(norm(n) in ptxt for n in s['notes'])
    fid[key] = dict(units=len(units), in_order=ok, missing=missing[:3], notes_present=notes_ok)
# exact whitespace check for poem lines: rebuild each PDF text line from its spans, drop the gutter number, compare exactly
pdf_lines = []
for pg in d:
    for b in pg.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            pdf_lines.append(''.join(s['text'] for s in l['spans']))
stripped = set(re.sub(r'^\d+ ', '', x) for x in pdf_lines)
for key in ('tan', 'pal', 'mem'):
    s = B.SOURCES[key]
    exact = sum(1 for n in s['lines'] if s['lines'][n] in stripped)
    fid[key]['exact_line_matches'] = f"{exact}/{len(s['lines'])}"
res['source_fidelity'] = fid
# 보충 해설문 verbatim
ex = B.SOURCES['kant']['extra'][0]
res['extra_commentary_present'] = norm(ex) in norm(full)

# ---- TOC page numbers vs real chapter headings
toc = d[1].get_text()
res['toc_text'] = [l for l in toc.split('\n') if re.search(r'\d\d$', l.strip())][:14]

json.dump(res, sys.stdout, ensure_ascii=False, indent=1)
print()

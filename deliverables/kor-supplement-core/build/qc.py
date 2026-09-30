#!/usr/bin/env python3
"""전 페이지 렌더 + 기본 QC(점유율, 유채색 픽셀, 폰트, raw markup, 원문 기호)."""
import sys, os, re, collections
import pymupdf
pdf = sys.argv[1]
outdir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(pdf), 'build', 'pages')
os.makedirs(outdir, exist_ok=True)
d = pymupdf.open(pdf)
MM = 72/25.4
top, bottom = 22*MM, (297-20)*MM
print('pages', len(d))
fonts = collections.Counter()
bad_tokens = ['⟦','⟧','¬',':::','**','__','<b>','</b>','<br','<span','&nbsp;','&amp;','&lt;','undefined','NaN','[object']
for i, pg in enumerate(d):
    pix = pg.get_pixmap(dpi=100)
    png = os.path.join(outdir, f'p{i+1:02d}.png'); pix.save(png)
    # occupancy of body area
    words = pg.get_text('words')
    body = [w for w in words if top-2 <= w[1] <= bottom+2]
    ys = [w[3] for w in body]
    for dr in pg.get_drawings():
        r = dr['rect']
        if top-2 <= r.y1 <= bottom+2 and r.y1 - r.y0 < 200*MM/10: ys.append(r.y1)   # rules/lines count as occupied
    occ = (max(ys)-top)/(bottom-top) if ys else 0
    # colored pixels
    s = pix.samples; n = pix.n; colored = 0
    for k in range(0, len(s), n*4):
        r, g, b = s[k], s[k+1], s[k+2]
        if max(r,g,b)-min(r,g,b) > 12: colored += 1
    txt = pg.get_text()
    leaks = [t for t in bad_tokens if t in txt]
    for f in pg.get_fonts(): fonts[f[3].split('+')[-1]] += 1
    # words beyond right/left margin
    over = [w for w in words if w[2] > (210-17)*MM+1.5 or w[0] < 17*MM-1.5]
    print(f'p{i+1:02d} occ={occ:4.0%} colored_px={colored:5d} words={len(words):4d} leaks={leaks} margin_overflow={len(over)}')
print('fonts:', dict(fonts))

"""Render a PDF to PNG previews for visual QC.  usage: qc_render.py file.pdf outdir [dpi]"""
import sys, os, pymupdf
pdf, out = sys.argv[1], sys.argv[2]
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 80
os.makedirs(out, exist_ok=True)
for f in os.listdir(out):
    if f.endswith('.png'): os.remove(os.path.join(out, f))
doc = pymupdf.open(pdf)
for i, page in enumerate(doc):
    page.get_pixmap(dpi=dpi).save(os.path.join(out, f'p{i:02d}.png'))
print(len(doc), 'pages ->', out)

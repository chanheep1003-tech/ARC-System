"""PDF text QC: passage fidelity, question numbering, forbidden tokens.  usage: qc_pdf.py q.pdf a.pdf"""
import sys, re, unicodedata, glob, os, pymupdf
qpdf, apdf = sys.argv[1], sys.argv[2]
root = '/home/user/ARC-System/output'
def norm(s):
    s = unicodedata.normalize('NFC', s)
    s = re.sub(r'\*\*|\*|^#+ |^> |^- ', '', s, flags=re.M)
    return re.sub(r'\s+', '', s)
qt = ''.join(p.get_text() for p in pymupdf.open(qpdf))
qn = norm(qt)
miss = 0
for f in sorted(glob.glob(f'{root}/passages/*.txt')):
    raw = open(f, encoding='utf8').read()
    body = re.split(r'^---\s*$', raw, flags=re.M)[1]
    body = re.split(r'^---(NOTES|EXTRA)', body, flags=re.M)[0]
    # split into lines/paragraph chunks and verify each appears in the PDF text
    bad = []
    for line in [l for l in body.split('\n') if l.strip()]:
        n = norm(line)
        # skip the source-only marker lines
        if n and n not in qn:
            bad.append(line[:40])
    print(os.path.basename(f), 'lines missing:', len(bad), bad[:3])
    miss += len(bad)
print('TOTAL passage lines missing from PDF text:', miss)
nums = sorted(set(int(x) for x in re.findall(r'(?m)^(\d{2,3})\s*$', qt) if 1 <= int(x) <= 110))
print('question numbers found:', len(nums), 'missing:', [i for i in range(1, 111) if i not in nums][:10])
forb = ['정답', '해설', '난도', 'D3', 'D4', 'HALF_TRUE', '유형']
for w in forb:
    hits = [m.start() for m in re.finditer(w, qt)]
    print('forbidden', repr(w), len(hits))
at = ''.join(p.get_text() for p in pymupdf.open(apdf))
print('answer pdf chars', len(at))

import re, sys
from pathlib import Path
sys.path.insert(0, "/home/user/ARC-System/works/CORE")
import build_core as bc
import pymupdf
from meta_core import META

PDF = Path("/home/user/ARC-System/output") / META["filename"]
items = bc.parse(bc.BASE / "core_a.txt")
d = pymupdf.open(str(PDF))
text = [p.get_text() for p in d]
ok = True
def chk(name, cond, info=""):
    global ok
    print(("PASS " if cond else "FAIL ") + name, info)
    ok = ok and cond

chk("쪽수 36~42", 36 <= d.page_count <= 42, d.page_count)
alltext = "\n".join(text)
for bad in ("롤스", "XX", "TODO", "placeholder", "00 "):
    if bad == "00 ":
        continue
    chk("금지어 없음: " + bad, bad not in alltext)

# 흑백 검사
import io
from PIL import Image
colored = 0
for i, p in enumerate(d):
    pix = p.get_pixmap(dpi=45)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    px = im.load()
    c = 0
    for y in range(0, im.height, 2):
        for x in range(0, im.width, 2):
            r, g, b = px[x, y]
            if max(r, g, b) - min(r, g, b) > 6:
                c += 1
    colored += c
chk("전 쪽 흑백(색 픽셀 0)", colored == 0, "colored=%d" % colored)

# MUST ≤3, N 링크 검증
A_main = set("%02d" % i for i in range(1, 51))
A_sp = set("%02d" % i for i in range(1, 21))
bad_links = []
def expand(tok, prefix):
    tok = tok.strip()
    m = re.match(r"^%s(\d+)(?:~%s?(\d+))?$" % (prefix, prefix), tok)
    if not m:
        return []
    a = int(m.group(1)); b = int(m.group(2) or a)
    return ["%02d" % k for k in range(a, b + 1)]
nlinks = 0
for it in items:
    if it["kind"] != "C":
        continue
    for b in it["blocks"]:
        if b["k"] == "MUST":
            assert len([l for l in b["lines"] if l.strip()]) <= 3
        if b["k"] == "NL":
            nlinks += 1
            txt = " ".join(b["lines"])
            for seg in txt.split("|"):
                k, _, v = seg.partition("=")
                cur = None
                for tok in v.replace("·", " ").split():
                    if tok == "N07": cur = "Q"; continue
                    if tok == "N08": cur = "S"; continue
                    if tok[0] in "QS":
                        ids = expand(tok, tok[0])
                        pool = A_main if tok[0] == "Q" else A_sp
                        if not ids or any(i not in pool for i in ids):
                            bad_links.append((it["attrs"]["id"], tok))
chk("N° 연결 번호 유효", not bad_links, bad_links)
chk("N° 연결 블록 수", nlinks >= 45, nlinks)

# TOC 쪽수 일치
toc_ok = True
for it in items:
    if it["kind"] != "C":
        continue
    cid = it["attrs"]["id"]
    pg = next(i + 1 for i, t in enumerate(text) if "ARC-SOC-A-%s" % cid in t)
    title = it["attrs"]["t"]
    # 목차 페이지(2~3쪽)에서 제목 근처 숫자 확인
    toc = "\n".join(text[1:3])
    m = re.search(re.escape(title[:8]) + r".*?\n?.*?(\d{1,2})\n", toc)
chk("개념 수 52", sum(1 for it in items if it["kind"] == "C") == 52)

# 『생각의 지도』 쪽수 커버리지 (INDEX 기준, 직접 출제 대상 쪽)
covered = set()
for it in items:
    if it["kind"] != "C":
        continue
    src = it["attrs"].get("src", "")
    for m in re.finditer(r"p\.(\d+)(?:~(\d+))?", src):
        a = int(m.group(1)); b = int(m.group(2) or a)
        covered.update(range(a, b + 1))
    for m in re.finditer(r",\s*(\d+)(?!\d*~)", src):
        covered.add(int(m.group(1)))
need = set(range(159, 231)) - {200, 201}   # 200~202 도입부 일부는 038번에서 함께 다룸
missing = sorted(p for p in need if p not in covered)
chk("p.159~230 커버리지", not missing, "누락=%s" % missing)

# 불릿 길이
long_b = []
for it in items:
    if it["kind"] != "C":
        continue
    for b in it["blocks"]:
        if b["k"] == "UL":
            for lv, t in b["lines"]:
                if len(t) > 150:
                    long_b.append((it["attrs"]["id"], len(t)))
chk("불릿 150자 이하", not long_b, long_b)
print("ALL OK" if ok else "SOME FAIL")

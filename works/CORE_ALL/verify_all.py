import re, sys, csv
from pathlib import Path
sys.path.insert(0, "/home/user/ARC-System/works/CORE")
sys.path.insert(0, "/home/user/ARC-System/works/CORE_ALL")
import build_core as bc
import build_all as ba
import pymupdf
from meta_all import META

PDF = Path("/home/user/ARC-System/output") / META["filename"]
items = bc.parse(ba.BASE / "core_all.txt")
d = pymupdf.open(str(PDF))
text = [p.get_text() for p in d]
alltext = "\n".join(text)
ok = True
def chk(name, cond, info=""):
    global ok
    print(("PASS " if cond else "FAIL ") + name, info)
    ok = ok and cond

chk("쪽수 18~23", 18 <= d.page_count <= 23, d.page_count)

# 파트별 쪽 분류 (개념 ID가 처음 나오는 쪽부터, 이어지는 쪽은 앞 쪽을 따른다)
part_of = {}
curk = None
for i, t in enumerate(text):
    if i < 2:
        continue
    m = re.search(r"ARC-SOC-ALL-([ABCZ])\d+", t)
    if m:
        curk = "C" if m.group(1) == "Z" else m.group(1)
    part_of[i + 1] = curk
a_pages = [p for p, k in part_of.items() if k == "A"]
c_pages = [p for p, k in part_of.items() if k == "C"]
chk("파트 분류됨", len(a_pages) >= 5 and len(c_pages) >= 4, "A=%s C=%s" % (a_pages, c_pages))

# 범위 금지어
a_text = "\n".join(text[p - 1] for p in a_pages)
for bad in ("롤스", "노직", "공동체주의", "자유주의"):
    chk("A 본문에 없음: " + bad, bad not in a_text)
for bad in ("거부권", "국정감사", "국정 감사", "탄핵", "사면", "규칙 심사", "임명 동의", "소로", "벤담", "밀(Mill"):
    chk("전체에 없음: " + bad, bad not in alltext)
for bad in ("TODO", "placeholder", "XX", "★"):
    chk("금지 문자열 없음: " + bad, bad not in alltext.replace("(★★★)", "").replace("(★★)", ""))
chk("롤스는 C와 범위표에만", all(("롤스" not in text[i]) or (i + 1 in c_pages) or i + 1 == 2 for i in range(d.page_count)))

# src 쪽수 범위
allowed = {"1": [(36, 43), (156, 233)], "2": [(98, 107), (124, 133)], "3": [(8, 23)]}
cur = None
for it in items:
    if it["kind"] == "PART":
        cur = it["attrs"]["no"]
    elif it["kind"] == "C" and cur in allowed:
        src = it["attrs"].get("src", "")
        for m in re.finditer(r"p\.(\d+)(?:~(\d+))?", src):
            lo = int(m.group(1)); hi = int(m.group(2) or lo)
            inside = any(a <= lo and hi <= b for a, b in allowed[cur])
            chk("src 범위 %s %s" % (it["attrs"]["id"], m.group(0)), inside, src)

# N° 연결 유효성 + 파트 일치
valid = {"N07": {"Q": 50}, "N08": {"S": 20}, "N09": {"Q": 50}, "N10": {"S": 20}, "N11": {"Q": 50}, "N12": {"S": 20}}
part_nums = {"1": ("N07", "N08"), "2": ("N09", "N10"), "3": ("N11", "N12")}
rows = []
cur = None
for it in items:
    if it["kind"] == "PART":
        cur = it["attrs"]["no"]
    elif it["kind"] == "C":
        for b in it["blocks"]:
            if b["k"] != "NL":
                continue
            lvl = None
            for part in " ".join(b["lines"]).split("|"):
                k, _, v = part.partition("=")
                book = None
                for tok in v.split():
                    if re.fullmatch(r"N\d\d", tok):
                        book = tok; continue
                    m = re.fullmatch(r"([QS])(\d\d)", tok)
                    if m and book:
                        kind, n = m.group(1), int(m.group(2))
                        good = (book in valid and kind in valid[book] and 1 <= n <= valid[book][kind])
                        if cur in part_nums:
                            good = good and book in part_nums[cur]
                        if not good:
                            chk("N° 유효 %s %s %s" % (it["attrs"]["id"], book, tok), False)
                        rows.append((it["attrs"]["id"], k.strip(), book, tok))
chk("N° 링크 전부 유효", True, "%d개" % len(rows))
with open(ba.BASE / "CORE_ALL_LINK_INDEX.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["concept", "level", "book", "item"]); w.writerows(rows)

# 목차 쪽수 일치
ids = [it["attrs"]["id"] for it in items if it["kind"] == "C"]
pages = ba.find_pages(PDF, ids)
front = text[1]
bad = []
for it in items:
    if it["kind"] != "C":
        continue
    cid = it["attrs"]["id"]
    chip = "정리" if cid.startswith("Z") else cid
    m = re.search(r"%s\n(.+?)\n(\d+)\n" % re.escape(chip), front, flags=re.S)
    if not m or m.group(2) != pages.get(cid):
        # 제목이 두 줄이면 정규식이 어긋날 수 있어 느슨하게 재검
        m2 = re.search(r"%s\n(?:.+\n){1,3}?(\d+)\n" % re.escape(chip), front)
        if not m2 or m2.group(1) != pages.get(cid):
            bad.append((cid, pages.get(cid)))
chk("목차 쪽수 일치", not bad, bad)
chk("개념 수 28", len(ids) == 28, len(ids))

# 불릿·MUST 길이
long_ = []
for it in items:
    if it["kind"] != "C":
        continue
    for b in it["blocks"]:
        if b["k"] == "UL":
            for lv, t in b["lines"]:
                if len(t) > 170:
                    long_.append((it["attrs"]["id"], len(t)))
        if b["k"] == "MUST":
            chk("MUST ≤3 %s" % it["attrs"]["id"], len([l for l in b["lines"] if l.strip()]) <= 3) if len(b["lines"]) > 3 else None
chk("불릿 170자 이하", not long_, long_)

# 흑백
from PIL import Image
colored = 0
for i, p in enumerate(d):
    pix = p.get_pixmap(dpi=45)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    px = im.load()
    for y in range(0, im.height, 2):
        for x in range(0, im.width, 2):
            r, g, b = px[x, y]
            if max(r, g, b) - min(r, g, b) > 6:
                colored += 1
chk("전 쪽 흑백(색 픽셀 0)", colored == 0, "colored=%d" % colored)

# 교과서 쪽 커버리지(표기된 쪽 합집합)
cov = set()
cur = None
for it in items:
    if it["kind"] == "PART":
        cur = it["attrs"]["no"]
    elif it["kind"] == "C":
        for m in re.finditer(r"p\.(\d+)(?:~(\d+))?", it["attrs"].get("src", "")):
            lo = int(m.group(1)); hi = int(m.group(2) or lo)
            for q in range(lo, hi + 1):
                cov.add((cur, q))
need = {"1": range(36, 44), "2": list(range(100, 108)) + list(range(126, 134)), "3": range(8, 24)}
miss = {k: [q for q in v if (k, q) not in cov] for k, v in need.items()}
print("교과서 쪽 표기 누락(참고):", {k: v for k, v in miss.items() if v})
print("ALL OK" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)

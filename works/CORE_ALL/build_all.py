"""전범위 직전 정리 CORE 빌더 — build_core의 파서·렌더러를 재사용하고 3부+정리 구성에 맞게 조판만 바꾼다."""
import re, sys
from pathlib import Path
sys.path.insert(0, "/home/user/ARC-System/works/CORE")
import build_core as bc

BASE = Path("/home/user/ARC-System/works/CORE_ALL")
PREFIX = "ARC-SOC-ALL-"
PARTS = {"1": "A  정의와 사고방식", "2": "B  세계화와 인구", "3": "C  인권과 헌법", "4": "시험장 체크"}


def head(right):
    return ('@top-left{content:"ARC CORE";font:700 6.6pt Inter;letter-spacing:.09em;color:#111;border-bottom:.45pt solid #bbb;width:100%%;padding-bottom:1.6mm;vertical-align:bottom}'
            '@top-right{content:"%s";font:6.6pt "Noto Sans KR";color:#666;border-bottom:.45pt solid #bbb;width:100%%;padding-bottom:1.6mm;vertical-align:bottom;text-align:right}'
            '@bottom-center{content:counter(page);font:7pt Inter;color:#555}') % right


def page_rules():
    r = ["@page{size:A4;margin:21mm 17mm 17mm 17mm}", "@page cover{margin:0}",
         "@page front{margin:21mm 17mm 17mm 17mm;%s}" % head("통합사회2 · 전범위 직전 정리")]
    for k, v in PARTS.items():
        r.append("@page p%s{%s}" % (k, head(v)))
    return "".join(r)


EXTRA = r"""
.cover .parts{grid-template-columns:1fr 1fr 1fr;gap:5mm}
.cover .parts div{font-size:8.6pt}
.rng{width:100%;border-collapse:collapse;margin:0 0 5mm;font-size:8.6pt}
.rng th,.rng td{border:.5pt solid #888;padding:1.5mm 2.4mm;text-align:left;vertical-align:top}
.rng th{background:#111;color:#fff;font-weight:700;width:26%}
.rng td{line-height:1.5}
.toc3{display:grid;grid-template-columns:1fr 1fr 1fr;column-gap:7mm;font-size:7.8pt}
.toc3 h4{margin:0 0 1.4mm;font-size:9pt;border-bottom:1.2pt solid #111;padding-bottom:1mm}
.toc3 .row{display:grid;grid-template-columns:6.2mm 1fr 6mm;gap:0 1.2mm;align-items:baseline;line-height:1.42;padding:.8mm 0;border-bottom:.35pt dotted #aaa}
.toc3 .row .n{font:700 7pt Inter}.toc3 .row .pg{font:7.4pt Inter;text-align:right}
.p1,.p2,.p3,.p4{page-break-before:always}
header.ch .no{min-width:8.4mm}

body{font-size:8.7pt;line-height:1.56}
section.c{margin:0 0 5mm;padding-top:2.2mm}
header.ch{margin-bottom:1.6mm}
header.ch h3{font-size:12.4pt}
header.ch .no{height:5.4mm;line-height:5.4mm;font-size:8.4pt}
.def{padding:1.5mm 3mm;margin:0 0 1.6mm}
.def p{font-size:8.9pt;line-height:1.5}
p.para{font-size:8.7pt;margin:1mm 0}
ul.pts{margin:.6mm 0 1mm}
ul.pts>li{margin:.9mm 0}
ul.pts>li:before{top:2mm}
.tbl{font-size:8.1pt;line-height:1.42;margin:1.6mm 0}
.tbl th,.tbl td{padding:1.05mm 1.9mm}
.tbl thead th{font-size:8pt}
.flow{margin:2.4mm 0 1.6mm}
.flow .fs{padding:1.3mm 1.6mm 1.2mm}
.flow .fs b{font-size:8.4pt}.flow .fs span{font-size:7.4pt}
.must{margin:2mm 0 1.2mm}
.must li{font-size:8.7pt;line-height:1.48}
.conf{margin:2.4mm 0 1.4mm;padding:2.4mm 3mm 1.1mm}
.conf .cr{font-size:8.3pt;line-height:1.45;margin:.4mm 0}
.ask{margin:2.2mm 0 1.2mm;padding:2.5mm 3mm 1.3mm}
.ask li{font-size:8.2pt;margin:.3mm 0;line-height:1.45}
.ask .steps{margin-top:1.1mm;padding-top:1mm;gap:.6mm 3.6mm;font-size:7.8pt}
.nl{margin-top:1.6mm;padding-top:1mm;font-size:7.3pt}
.partband{padding-top:2.2mm;margin-bottom:4mm}
.partband h2{font-size:19pt}
.partband .s{font-size:8.8pt;margin-bottom:2.2mm}
.partband li{font-size:7.8pt;padding-top:1.2mm}
figure{margin:1.4mm 0}
figure img{width:84%;margin:0 auto}
figcaption{font-size:7pt}
.note{font-size:7.2pt}
@page{margin:19mm 16mm 15mm 16mm}
@page front{margin:19mm 16mm 15mm 16mm}
"""


SHOW_ASK = False  # '이렇게 묻는다' 칸: V1.3부터 제외(원고의 ASK 줄은 복구용으로 유지)


def render_c(it, idx=0):
    a = it["attrs"]
    cid = PREFIX + a["id"]
    chip = "정리" if a["id"].startswith("Z") else a["id"]
    head_ = ("<header class='ch'><span class='no'>%s</span><h3>%s</h3><span class='meta'>%s<em>%s</em></span></header>" %
             (chip, bc.inline(a["t"]), ("<u>%s</u>" % bc.inline(a["src"])) if a.get("src") else "", cid))
    body = "".join(bc.r_block(b) for b in it["blocks"] if SHOW_ASK or b["k"] != "ASK")
    return "<section class='c' id='c%s'>%s%s</section>" % (a["id"], head_, body)


def build_html(items, meta, pages=None, extra_css=""):
    pages = pages or {}
    cover = ("<section class='cover'><div class='kick'>ARC CORE</div><div class='rule'></div><div class='main'>"
             "<h1>%(subject)s</h1><h2>%(sub)s</h2>"
             "<div class='parts'>%(parts)s</div>"
             "<div class='meta'>%(school)s<br>%(range)s</div></div>"
             "<div class='yr'>2026</div><div class='ser'>CONCEPT CORE</div></section>") % dict(
        subject=meta["subject"], sub=meta["sub"], parts=meta["cover_parts"], school=meta["school"], range=meta["range"])
    cols = {"1": [], "2": [], "3": [], "4": []}
    cur = None
    for it in items:
        if it["kind"] == "PART":
            cur = it["attrs"]["no"]
        elif it["kind"] == "C":
            cols[cur].append(it["attrs"])
    def rows(lst):
        return "".join("<div class='row'><span class='n'>%s</span><span class='t'>%s</span><span class='pg'>%s</span></div>" %
                       ("정리" if a["id"].startswith("Z") else a["id"], bc.inline(a["t"]), pages.get(a["id"], "00")) for a in lst)
    rng = "".join("<tr><th>%s</th><td>%s</td></tr>" % (a, b) for a, b in meta["range_rows"])
    front = ("<section class='front'>"
             "<h2 class='sec'>시험범위 <small style='font-size:8.4pt;font-weight:500;color:#555;margin-left:2mm'>통합사회2 · 24문항 · 100점</small></h2><table class='rng'>%s</table>"
             "<h2 class='sec'>이 책의 쓰임</h2><div class='use'>%s</div>"
             "<div class='note' style='margin:0 0 6mm'>%s</div>"
             "<h2 class='sec'>목차</h2><div class='toc3'>"
             "<div><h4>A  정의와 사고방식</h4>%s</div><div><h4>B  세계화와 인구</h4>%s</div>"
             "<div><h4>C  인권과 헌법</h4>%s%s</div></div></section>") % (
        rng, meta["use_html"], meta["note"], rows(cols["1"]), rows(cols["2"]), rows(cols["3"]), rows(cols["4"]))
    body, opened = [], False
    for it in items:
        if it["kind"] == "pb":
            body.append("<div class='pb'></div>")
        elif it["kind"] == "PART":
            if opened:
                body.append("</div>")
            body.append("<div class='p%s'>" % it["attrs"]["no"])
            opened = True
            body.append(bc.render_part(it))
        elif it["kind"] == "C":
            body.append(render_c(it))
    if opened:
        body.append("</div>")
    css = page_rules() + bc.CSS[bc.CSS.index("*{box-sizing"):] + EXTRA + extra_css
    return "<!doctype html><html lang='ko'><head><meta charset='utf-8'><style>%s</style></head><body>%s%s%s</body></html>" % (
        css, cover, front, "".join(body))


def find_pages(pdf_path, ids):
    import pymupdf
    d = pymupdf.open(str(pdf_path))
    res = {}
    texts = [p.get_text() for p in d]
    for cid in ids:
        pat = re.compile(re.escape(PREFIX + cid) + r"(?![0-9A-Za-z])")
        for i, t in enumerate(texts):
            if pat.search(t):
                res[cid] = str(i + 1)
                break
    return res


def build(ms_path, meta, out_pdf, extra_css=""):
    items = bc.parse(ms_path)
    work = BASE / "_tmp"
    work.mkdir(exist_ok=True)
    (work / "fig").mkdir(exist_ok=True)
    for f in (BASE / "fig").glob("*.svg"):
        (work / "fig" / f.name).write_bytes(f.read_bytes())
    ids = [it["attrs"]["id"] for it in items if it["kind"] == "C"]
    html1 = work / "core.html"
    html1.write_text(build_html(items, meta, {}, extra_css), encoding="utf-8")
    bc.to_pdf(html1, work / "pass1.pdf")
    pages = find_pages(work / "pass1.pdf", ids)
    html1.write_text(build_html(items, meta, pages, extra_css), encoding="utf-8")
    bc.to_pdf(html1, out_pdf)
    return pages, len(ids)


if __name__ == "__main__":
    sys.path.insert(0, str(BASE))
    from meta_all import META
    out = Path("/home/user/ARC-System/output") / META["filename"]
    pages, n = build(BASE / "core_all.txt", META, out)
    import pymupdf
    print(out, pymupdf.open(str(out)).page_count, "pages,", n, "concepts")

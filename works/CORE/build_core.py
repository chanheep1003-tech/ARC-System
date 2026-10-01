"""ARC CORE 빌더 (흑백 모드).

원고 문법 (core_a.txt)
  @PART no=1 title=... sub=... lead=...    파트 표지 띠
  @C id=001 t=제목 pr=R src=...            개념 시작  (pr: R/S/C)
  DEF: 한 줄 정리
  P: 짧은 문단
  - 일반 불릿 / -! 필수 불릿 / -~ 보충 불릿 / -- 하위 불릿
  FLOW: 라벨|보조 > 라벨|보조 > ...
  CMP: 항목 | 좌 | 우        (첫 줄=머리글, 이후 줄=행)
  TBL: 머리1 | 머리2 | ...   (일반 표)
  MAT: 좌상 | 우상 | 좌하 | 우하   + 머리글 줄 "MAT:" 아래 'ROW=…', 'COL=…'
  FIG: id | 캡션
  MUST: 줄마다 1개 (최대 3)
  CONF: × 틀린 진술 / ○ 바른 진술   (줄 단위)
  ASK: Q 발문 / → 푸는 순서
  SUP: 보충 박스
  NL: 기본=… | 적용=… | 고난도=…
  NOTE: 작은 주석
  @PB   쪽 나눔
"""
import re, sys, html as _html
from pathlib import Path

BASE = Path("/home/user/ARC-System/works/CORE")
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

KEYS = ("DEF", "P", "FLOW", "CMP", "TBL", "MAT", "FIG", "MUST", "CONF", "ASK", "SUP", "NL", "NOTE", "CAP")


def inline(s: str) -> str:
    s = _html.escape(s.strip(), quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"__(.+?)__", r"<u>\1</u>", s)
    s = re.sub(r"\^\^(.+?)\^\^", r"<span class='hl'>\1</span>", s)
    return s


def parse(path):
    items = []
    cur = None
    blk = None
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line.strip() or line.startswith("#"):
            continue
        if line.startswith("@PB"):
            items.append({"kind": "pb"}); cur = None; blk = None; continue
        m = re.match(r"^@(PART|C)\s+(.*)$", line)
        if m:
            kind, rest = m.groups()
            attrs = {}
            # key=value 쌍 (값에 공백 허용: 다음 key= 직전까지)
            for km in re.finditer(r"(\w+)=(.*?)(?=\s+\w+=|$)", rest):
                attrs[km.group(1)] = km.group(2).strip()
            cur = {"kind": kind, "attrs": attrs, "blocks": []}
            items.append(cur); blk = None
            continue
        if cur is None:
            continue
        mk = re.match(r"^(%s):\s*(.*)$" % "|".join(KEYS), line)
        if mk:
            k, v = mk.groups()
            blk = {"k": k, "lines": [v] if v else []}
            cur["blocks"].append(blk)
            continue
        if line.startswith("-"):
            mb = re.match(r"^(--|-!|-~|-)\s*(.*)$", line)
            lv, txt = mb.groups()
            if not (cur["blocks"] and cur["blocks"][-1]["k"] == "UL"):
                cur["blocks"].append({"k": "UL", "lines": []})
            cur["blocks"][-1]["lines"].append((lv, txt))
            blk = None
            continue
        if blk is not None:
            blk["lines"].append(line.strip())
    return items


# ----------------------------------------------------------------------------- 렌더
def r_ul(lines):
    out = ["<ul class='pts'>"]
    open_sub = False
    for lv, txt in lines:
        if lv == "--":
            if not open_sub:
                out.append("<ul class='sub'>"); open_sub = True
            out.append("<li>%s</li>" % inline(txt))
            continue
        if open_sub:
            out.append("</ul></li>"); open_sub = False
        else:
            if out[-1] != "<ul class='pts'>":
                out.append("</li>")
        cls = {"-": "", "-!": " class='must-li'", "-~": " class='sup-li'"}[lv]
        tag = {"-": "", "-!": "<i class='bd k'>필수</i>", "-~": "<i class='bd s'>보충</i>"}[lv]
        out.append("<li%s>%s%s" % (cls, tag, inline(txt)))
    if open_sub:
        out.append("</ul>")
    out.append("</li></ul>")
    return "".join(out)


def r_flow(lines):
    txt = " ".join(lines)
    steps = [s.strip() for s in txt.split(">")]
    cells = []
    for i, s in enumerate(steps):
        parts = [p.strip() for p in s.split("|")]
        sub = "<span>%s</span>" % inline(parts[1]) if len(parts) > 1 else ""
        cells.append("<div class='fs'><em>%d</em><b>%s</b>%s</div>" % (i + 1, inline(parts[0]), sub))
        if i < len(steps) - 1:
            cells.append("<div class='fa'>▶</div>")
    return "<div class='flow'>%s</div>" % "".join(cells)


def r_table(lines, cls="tbl", first_col_head=False):
    rows = [[c.strip() for c in l.split("|")] for l in lines if l.strip()]
    head, body = rows[0], rows[1:]
    t = ["<table class='%s'><thead><tr>%s</tr></thead><tbody>" % (cls, "".join("<th>%s</th>" % inline(c) for c in head))]
    for r in body:
        cells = []
        for j, c in enumerate(r):
            cells.append("<th class='rh'>%s</th>" % inline(c) if (j == 0 and first_col_head) else "<td>%s</td>" % inline(c))
        t.append("<tr>%s</tr>" % "".join(cells))
    t.append("</tbody></table>")
    return "".join(t)


def r_mat(lines):
    # 첫 줄: "열머리1 | 열머리2", 이후: "행머리 | 셀1 | 셀2"
    return r_table(lines, cls="tbl mat", first_col_head=True)


def r_conf(lines):
    rows = []
    for l in lines:
        l = l.strip()
        if not l:
            continue
        mark = l[0]
        cls = "x" if mark == "×" else "o"
        rows.append("<div class='cr %s'><i>%s</i><span>%s</span></div>" % (cls, mark, inline(l[1:])))
    return "<div class='conf'><div class='lab'>혼동 주의</div>%s</div>" % "".join(rows)


def r_ask(lines):
    qs, steps = [], []
    for l in lines:
        l = l.strip()
        if l.startswith("→"):
            steps.append(l[1:].strip())
        elif l.startswith("Q"):
            qs.append(l[1:].strip().lstrip(":").strip())
        else:
            qs.append(l)
    qh = "".join("<li>%s</li>" % inline(q) for q in qs)
    sh = ""
    if steps:
        sh = "<div class='steps'><b>푸는 순서</b>%s</div>" % "".join(
            "<span><em>%s</em>%s</span>" % ("①②③④⑤⑥"[i], inline(s)) for i, s in enumerate(steps))
    return "<div class='ask'><div class='lab'>이렇게 묻는다</div><ul>%s</ul>%s</div>" % (qh, sh)


def r_nl(lines):
    txt = " ".join(lines)
    parts = [p.strip() for p in txt.split("|")]
    spans = []
    for p in parts:
        k, _, v = p.partition("=")
        spans.append("<span><b>%s</b>%s</span>" % (inline(k), inline(v)))
    return "<div class='nl'><i>N° 연결</i>%s</div>" % "".join(spans)


def r_block(b, figdir="fig"):
    k, ls = b["k"], b["lines"]
    if k == "UL":
        return r_ul(ls)
    if k == "DEF":
        return "<div class='def'><i>한 줄 정리</i><p>%s</p></div>" % inline(" ".join(ls))
    if k == "P":
        return "<p class='para'>%s</p>" % inline(" ".join(ls))
    if k == "FLOW":
        return r_flow(ls)
    if k == "CMP":
        return r_table(ls, cls="tbl cmp", first_col_head=True)
    if k == "TBL":
        return r_table(ls)
    if k == "MAT":
        return r_mat(ls)
    if k == "FIG":
        fid, _, cap = " ".join(ls).partition("|")
        capl = "<figcaption>%s</figcaption>" % inline(cap) if cap.strip() else ""
        return "<figure><img src='%s/%s.svg'>%s</figure>" % (figdir, fid.strip(), capl)
    if k == "MUST":
        items = [l for l in ls if l.strip()]
        assert len(items) <= 3, ("MUST 3개 초과", items)
        return "<div class='must'><i>MUST</i><ol>%s</ol></div>" % "".join("<li>%s</li>" % inline(x) for x in items)
    if k == "CONF":
        return r_conf(ls)
    if k == "ASK":
        return r_ask(ls)
    if k == "SUP":
        return "<div class='sup'><div class='lab'>보충 <small>고2·3 윤리 연결 · 시험 답안의 근거로 쓰지 않는다</small></div>%s</div>" % \
            "".join("<p>%s</p>" % inline(x) for x in ls)
    if k == "NL":
        return r_nl(ls)
    if k == "NOTE":
        return "<div class='note'>%s</div>" % inline(" ".join(ls))
    if k == "CAP":
        return "<div class='cap'>%s</div>" % inline(" ".join(ls))
    raise ValueError(k)


def render_c(it, idx):
    a = it["attrs"]
    cid = "ARC-SOC-A-%s" % a["id"]
    pr = a.get("pr", "R")
    split = " split" if a.get("split") else ""
    head = ("<header class='ch'><span class='no'>%s</span><h3>%s</h3><span class='meta'>%s<em>%s</em></span></header>" %
            (a["id"][-2:], inline(a["t"]), ("<u>%s</u>" % inline(a["src"])) if a.get("src") else "", cid))
    body = "".join(r_block(b) for b in it["blocks"])
    return "<section class='c%s' id='c%s'>%s%s</section>" % (split, a["id"], head, body)


def render_part(it):
    a = it["attrs"]
    leads = [x.strip() for x in a.get("lead", "").split("/") if x.strip()]
    li = "".join("<li><b>%d</b><span>%s</span></li>" % (i + 1, inline(x)) for i, x in enumerate(leads))
    return ("<div class='partband p%s'><div class='k'>PART %s</div><h2>%s</h2><div class='s'>%s</div><ol>%s</ol></div>" %
            (a["no"], a["no"], inline(a["title"]), inline(a.get("sub", "")), li))


CSS = r"""
@page{size:A4;margin:21mm 17mm 17mm 17mm}
@page cover{margin:0}
@page front{margin:21mm 17mm 17mm 17mm;
  @top-left{content:"ARC CORE";font:700 6.6pt Inter;letter-spacing:.09em;color:#111;border-bottom:.45pt solid #bbb;width:100%;padding-bottom:1.6mm;vertical-align:bottom}
  @top-right{content:"통합사회2 · A파트";font:6.6pt "Noto Sans KR";color:#666;border-bottom:.45pt solid #bbb;width:100%;padding-bottom:1.6mm;vertical-align:bottom;text-align:right}
  @bottom-center{content:counter(page);font:7pt Inter;color:#555}}
@page p1{@top-left{content:"ARC CORE";font:700 6.6pt Inter;letter-spacing:.09em;color:#111;border-bottom:.45pt solid #bbb;width:100%;padding-bottom:1.6mm;vertical-align:bottom}
  @top-right{content:"1부  칸트와 베카리아";font:6.6pt "Noto Sans KR";color:#666;border-bottom:.45pt solid #bbb;width:100%;padding-bottom:1.6mm;vertical-align:bottom;text-align:right}
  @bottom-center{content:counter(page);font:7pt Inter;color:#555}}
@page p2{@top-left{content:"ARC CORE";font:700 6.6pt Inter;letter-spacing:.09em;color:#111;border-bottom:.45pt solid #bbb;width:100%;padding-bottom:1.6mm;vertical-align:bottom}
  @top-right{content:"2부  『생각의 지도』 p.156~233";font:6.6pt "Noto Sans KR";color:#666;border-bottom:.45pt solid #bbb;width:100%;padding-bottom:1.6mm;vertical-align:bottom;text-align:right}
  @bottom-center{content:counter(page);font:7pt Inter;color:#555}}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#fff;color:#111;font-family:"Noto Sans KR","Noto Sans",sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-size:9.3pt;line-height:1.7;letter-spacing:-.012em;word-break:keep-all}
.cover{page:cover;height:297mm;width:210mm;position:relative;padding:26mm 22mm;break-after:page}
.cover .kick{font:700 10pt Inter;letter-spacing:.14em}
.cover .rule{height:2.2pt;background:#111;margin-top:6mm}
.cover .main{margin-top:58mm}
.cover h1{font-size:34pt;line-height:1.15;letter-spacing:-.045em;margin:0 0 5mm;font-weight:700}
.cover h2{font-size:15pt;font-weight:500;margin:0 0 10mm;letter-spacing:-.03em;line-height:1.45}
.cover .parts{display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:14mm}
.cover .parts div{border-top:.9pt solid #111;padding-top:2.4mm;font-size:9pt;line-height:1.55}
.cover .parts b{display:block;font-size:10.4pt;margin-bottom:.6mm}
.cover .meta{margin-top:12mm;font-size:9pt;color:#444;line-height:1.9}
.cover .yr{position:absolute;left:22mm;bottom:22mm;font:9pt Inter;letter-spacing:.1em;color:#555}
.cover .ser{position:absolute;right:22mm;bottom:22mm;font:700 8pt Inter;letter-spacing:.1em}
.front{page:front}
.use-pg{break-after:page}
.p1{page:p1}.p2{page:p2}
h2.sec{font-size:15pt;margin:0 0 4mm;letter-spacing:-.035em}
.use{display:grid;grid-template-columns:1fr 1fr;gap:3.2mm 6mm;margin-bottom:6mm}
.use div{border-top:.7pt solid #111;padding-top:1.6mm;font-size:8.2pt;line-height:1.55;color:#222}
.use b{display:block;font-size:8.8pt;margin-bottom:.4mm}
.toc{display:grid;grid-template-columns:1fr 1fr;column-gap:9mm;font-size:8.2pt}
.toc h4{margin:0 0 1.6mm;font-size:9.4pt;border-bottom:1.2pt solid #111;padding-bottom:1mm}
.toc .row{display:grid;grid-template-columns:6.4mm 1fr 8mm;gap:0 1.5mm;align-items:baseline;line-height:1.5;padding:.9mm 0;border-bottom:.35pt dotted #aaa}
.toc .row .n{font:700 7.4pt Inter}
.toc .row .pg{font:7.8pt Inter;text-align:right}
.partband{border-top:3.4pt solid #111;padding-top:3mm;margin-bottom:6.5mm;break-inside:avoid}
.partband .k{font:700 8pt Inter;letter-spacing:.15em;color:#444}
.partband h2{font-size:22pt;letter-spacing:-.045em;margin:1.2mm 0 1mm;line-height:1.2}
.partband .s{font-size:9.6pt;color:#444;margin-bottom:3.4mm}
.partband ol{list-style:none;display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin:0;padding:0}
.partband li{display:flex;gap:2mm;font-size:8.2pt;line-height:1.5;border-top:.5pt solid #999;padding-top:1.6mm}
.partband li b{font:700 8.6pt Inter;flex:0 0 3.6mm}
section.c{break-inside:auto;margin:0 0 8.4mm;padding-top:3mm;border-top:1.2pt solid #111;orphans:3;widows:3}
ul.pts>li,.def,p.para{break-inside:avoid}
.def{break-after:avoid}
.nl{break-before:avoid}
header.ch+.def,header.ch+.flow,header.ch+.tbl{break-before:avoid}
header.ch{display:flex;align-items:center;gap:2.6mm;margin-bottom:2.2mm;break-after:avoid}
header.ch .no{background:#111;color:#fff;font:700 9pt Inter;min-width:7.6mm;height:6mm;line-height:6mm;text-align:center;border-radius:.9mm}
header.ch h3{font-size:13.6pt;margin:0;letter-spacing:-.035em;font-weight:700;line-height:1.25}
header.ch .meta{margin-left:auto;text-align:right;font:6.4pt Inter;color:#777;line-height:1.35;white-space:nowrap}
header.ch .meta u{display:block;text-decoration:none;font:6.8pt "Noto Sans KR";color:#555;margin-bottom:.2mm}
header.ch .meta em{font-style:normal;letter-spacing:.05em}
.def{display:flex;gap:3mm;align-items:baseline;background:#f0f0f0;border-left:2.4pt solid #111;padding:2mm 3.2mm;margin:0 0 2.2mm}
.def i{font-style:normal;font:700 6.8pt "Noto Sans KR";background:#111;color:#fff;padding:.4mm 1.8mm;border-radius:.8mm;flex:0 0 auto;white-space:nowrap}
.def p{margin:0;font-weight:500;font-size:9.5pt;line-height:1.6}
p.para{margin:1.4mm 0;font-size:9.3pt}
ul.pts{margin:1mm 0 1.6mm;padding:0;list-style:none}
ul.pts>li{position:relative;padding-left:3.8mm;margin:1.5mm 0}
ul.pts>li:before{content:"";position:absolute;left:.8mm;top:2.25mm;width:1.2mm;height:1.2mm;background:#333;border-radius:50%}
ul.pts>li.must-li:before{border-radius:0;background:#111;top:2.15mm}
ul.pts>li.must-li{font-weight:500}
ul.pts>li.sup-li{color:#555;font-size:8.7pt}
ul.pts>li.sup-li:before{background:#fff;border:.6pt solid #666}
ul.sub{list-style:none;margin:.4mm 0 .2mm;padding:0 0 0 .6mm}
ul.sub li{position:relative;padding-left:3mm;margin:.4mm 0;color:#333;font-size:8.8pt}
ul.sub li:before{content:"–";position:absolute;left:0;color:#777}
i.bd{font-style:normal;font:700 5.9pt "Noto Sans KR";padding:.15mm 1.1mm;border-radius:.6mm;margin-right:1.5mm;vertical-align:.2mm;letter-spacing:0}
i.bd.k{background:#111;color:#fff}
i.bd.s{border:.5pt dotted #555;color:#555}
.flow{display:flex;align-items:stretch;gap:0;margin:3mm 0 2.4mm;break-inside:avoid}
.flow .fs{flex:1 1 0;border:.9pt solid #111;padding:1.8mm 2mm 1.6mm;position:relative;background:#fff;text-align:left}
.flow .fs em{position:absolute;top:-2.2mm;left:1.6mm;background:#fff;font:700 6.8pt Inter;padding:0 1mm;font-style:normal}
.flow .fs b{display:block;font-size:9pt;line-height:1.4}
.flow .fs span{display:block;font-size:7.9pt;color:#555;line-height:1.45;margin-top:.6mm}
.flow .fa{flex:0 0 4.2mm;align-self:center;text-align:center;font-size:6pt;color:#111}
.tbl{width:100%;border-collapse:collapse;margin:2.4mm 0;font-size:8.8pt;line-height:1.5;break-inside:avoid}
.tbl th,.tbl td{border:.5pt solid #888;padding:1.6mm 2.2mm;vertical-align:top;text-align:left}
.tbl thead th{background:#111;color:#fff;border-color:#111;font-weight:700;font-size:8.6pt}
.tbl .rh{background:#ececec;font-weight:700;width:21%}
.tbl.cmp td{width:39.5%}
.tbl.mat td{text-align:center;vertical-align:middle;height:12mm}
.tbl.mat thead th{text-align:center}
figure{margin:2.2mm 0;text-align:center;break-inside:avoid}
figure img{width:100%;display:block}
figcaption{font-size:7.2pt;color:#555;margin-top:.8mm;text-align:center}
.must{display:flex;gap:3mm;align-items:flex-start;margin:3mm 0 2mm;break-inside:avoid}
.must i{font-style:normal;font:700 7pt Inter;background:#111;color:#fff;padding:.7mm 2.2mm;border-radius:.8mm;letter-spacing:.06em;flex:0 0 auto;margin-top:.4mm}
.must ol{margin:0;padding:0;list-style:none;flex:1}
.must li{font-weight:700;font-size:9.2pt;line-height:1.55;padding:.1mm 0;border-bottom:.4pt solid #ccc}
.must li:last-child{border-bottom:0}
.conf,.ask,.sup,.must{display:inline-block;width:100%;vertical-align:top;-webkit-column-break-inside:avoid;page-break-inside:avoid}
.must{display:flex}
.conf{border:1.15pt solid #111;margin:3mm 0 2.2mm;padding:3mm 3.4mm 2mm;position:relative;break-inside:avoid}
.lab{position:absolute;top:-2.3mm;left:3mm;background:#fff;padding:0 1.6mm;font:700 7.2pt "Noto Sans KR";letter-spacing:.01em}
.conf .cr{display:flex;gap:2mm;align-items:baseline;font-size:8.9pt;line-height:1.55;margin:.8mm 0}
.conf .cr i{font-style:normal;font:700 8pt "Noto Sans KR";flex:0 0 3.6mm;text-align:center;border-radius:50%;height:3.6mm;line-height:3.5mm;font-size:7.2pt}
.conf .cr.x i{background:#111;color:#fff}
.conf .cr.o i{border:.8pt solid #111}
.conf .cr.x span{color:#444;text-decoration:none}
.ask{border:.8pt dashed #444;margin:3mm 0 1.8mm;padding:3.2mm 3.4mm 2.2mm;position:relative;break-inside:avoid;background:#fafafa}
.ask ul{margin:0;padding:0;list-style:none}
.ask li{position:relative;padding-left:3.8mm;font-size:8.8pt;margin:.7mm 0;line-height:1.55}
.ask li:before{content:"Q";position:absolute;left:0;font:700 7.2pt Inter}
.ask .steps{display:flex;flex-wrap:wrap;gap:1.4mm 4.5mm;margin-top:1.8mm;padding-top:1.6mm;border-top:.4pt solid #bbb;font-size:8.3pt;align-items:baseline}
.ask .steps b{font-size:7pt;color:#555;font-weight:700}
.ask .steps span em{font-style:normal;font-weight:700;margin-right:.8mm}
.sup{border:.8pt dotted #555;margin:3mm 0 1.8mm;padding:3.2mm 3.4mm 1.4mm;position:relative;break-inside:avoid}
.sup .lab small{font-weight:400;font-size:6.6pt;color:#555;margin-left:1mm}
.sup p{margin:0 0 1.6mm;font-size:8.8pt;color:#333;line-height:1.6}
.nl{display:flex;flex-wrap:wrap;gap:1mm 4.8mm;align-items:baseline;margin-top:2.6mm;padding-top:1.5mm;border-top:.4pt solid #bbb;font-size:7.6pt;color:#444}
.nl i{font-style:normal;font-weight:700;color:#111;letter-spacing:.01em}
.nl span b{font-weight:700;color:#111;margin-right:1.2mm}
.note{font-size:7.4pt;color:#666;margin:1.2mm 0}
.cap{font-size:7.4pt;color:#555;margin:.6mm 0 1.6mm}
.hl{background:#e4e4e4;padding:0 .6mm}
.pb{break-after:page}
.fin{break-before:page}
.keep{break-inside:avoid}
"""


def build_html(items, meta, pages=None, figdir="fig"):
    pages = pages or {}
    cover = ("<section class='cover'><div class='kick'>ARC CORE</div><div class='rule'></div><div class='main'>"
             "<h1>%(subject)s</h1><h2>%(sub)s</h2>"
             "<div class='parts'>%(parts)s</div>"
             "<div class='meta'>%(school)s<br>%(range)s</div></div>"
             "<div class='yr'>2026</div><div class='ser'>CONCEPT CORE</div></section>") % dict(
        subject=meta["subject"], sub=meta["sub"], parts=meta["cover_parts"], school=meta["school"], range=meta["range"])
    # TOC
    toc_parts = {"1": [], "2": []}
    cur_part = None
    for it in items:
        if it["kind"] == "PART":
            cur_part = it["attrs"]["no"]
        elif it["kind"] == "C":
            a = it["attrs"]
            toc_parts[cur_part].append(a)
    def toc_rows(lst):
        return "".join("<div class='row'><span class='n'>%s</span><span class='t'>%s</span><span class='pg'>%s</span></div>" %
                       (a["id"][-2:], inline(a["t"]), pages.get(a["id"], "00")) for a in lst)
    front = ("<section class='front use-pg'><h2 class='sec'>이 책의 쓰임</h2><div class='use'>%s</div>"
             "<h2 class='sec' style='margin-top:8mm'>읽는 순서</h2>%s"
             "<div class='note' style='margin-top:6mm'>이 책의 표와 실험 결과는 모두 &lsquo;집단 평균의 경향&rsquo;이다. 개인이나 문화의 본질로 옮겨 말하는 선지는 오답이 되기 쉽다.</div></section>"
             "<section class='front'><h2 class='sec'>목차</h2><div class='toc'>"
             "<div><h4>1부  칸트와 베카리아</h4>%s</div><div><h4>2부  『생각의 지도』</h4>%s</div></div></section>") % (
        meta["use_html"], meta["order_html"], toc_rows(toc_parts["1"]), toc_rows(toc_parts["2"]))
    body = []
    cur = None
    opened = False
    for it in items:
        if it["kind"] == "pb":
            body.append("<div class='pb'></div>")
        elif it["kind"] == "PART":
            if opened:
                body.append("</div>")
            body.append("<div class='p%s' style='break-before:page'>" % it["attrs"]["no"])
            opened = True
            body.append(render_part(it))
        elif it["kind"] == "C":
            body.append(render_c(it, 0))
    if opened:
        body.append("</div>")
    return "<!doctype html><html lang='ko'><head><meta charset='utf-8'><style>%s</style></head><body>%s%s%s</body></html>" % (
        CSS, cover, front, "".join(body))


def to_pdf(html_path, pdf_path):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
        pg = b.new_page()
        pg.goto("file://" + str(Path(html_path).resolve()))
        pg.wait_for_timeout(700)
        pg.pdf(path=str(pdf_path), format="A4", print_background=True, prefer_css_page_size=True)
        b.close()


def find_pages(pdf_path, ids):
    import pymupdf
    d = pymupdf.open(str(pdf_path))
    res = {}
    for i, p in enumerate(d):
        t = p.get_text()
        for cid in ids:
            if cid not in res and ("ARC-SOC-A-%s" % cid) in t:
                res[cid] = str(i + 1)
    return res


def build(ms_path, meta, out_pdf):
    items = parse(ms_path)
    work = BASE / "_tmp"
    work.mkdir(exist_ok=True)
    (work / "fig").mkdir(exist_ok=True)
    for f in (BASE / "fig").glob("*.svg"):
        (work / "fig" / f.name).write_bytes(f.read_bytes())
    ids = [it["attrs"]["id"] for it in items if it["kind"] == "C"]
    html1 = work / "core.html"
    html1.write_text(build_html(items, meta, {}), encoding="utf-8")
    to_pdf(html1, work / "pass1.pdf")
    pages = find_pages(work / "pass1.pdf", ids)
    html1.write_text(build_html(items, meta, pages), encoding="utf-8")
    to_pdf(html1, out_pdf)
    return pages, len(ids)


if __name__ == "__main__":
    sys.path.insert(0, str(BASE))
    from meta_core import META
    out = Path("/home/user/ARC-System/output") / META["filename"]
    pages, n = build(BASE / "core_a.txt", META, out)
    import pymupdf
    print(out, pymupdf.open(str(out)).page_count, "pages,", n, "concepts")

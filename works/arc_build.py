#!/usr/bin/env python3
"""ARC N 제작 빌더: 원고(txt) -> A4 2단 HTML -> PDF (표지 + 문제지 + 정답지).

원고 형식(작성 규칙)은 works/README.md 참고.
"""
import html
import json
import re
import sys
from pathlib import Path

CIRC = "①②③④⑤"
TAG_OK = re.compile(r"<(?!/?(u|b|i|sub|sup|br|span|em|strong)\b)")


def esc(s: str) -> str:
    """허용 태그(u,b,i,sub,sup,br,span)만 남기고 나머지 '<'는 이스케이프."""
    s = s.replace("&", "&amp;")
    s = TAG_OK.sub("&lt;", s)
    s = re.sub(r"__(.+?)__", r"<u>\1</u>", s)
    return s


# ----------------------------------------------------------------------------
# 원고 파서
# ----------------------------------------------------------------------------
def parse(path):
    items = []          # 문항/번들 순서 리스트
    cur = None
    tag = None
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if line.startswith("#"):
            continue
        m = re.match(r"^@(Q|BUNDLE)\s*(.*)$", line)
        if m:
            kind, rest = m.groups()
            attrs = dict(re.findall(r"(\w+)=(\S+)", rest.replace("｜", " ")))
            # c=값에 공백이 들어갈 수 있으므로 c=는 '|' 이후 전체로 처리
            mc = re.search(r"c=(.*?)(?=\s+\w+=|$)", rest)
            if mc:
                attrs["c"] = mc.group(1).strip()
            cur = {"kind": kind, "attrs": attrs, "blocks": [], "ch": [], "chrow": None,
                   "why": "", "stem": ""}
            items.append(cur)
            tag = None
            continue
        if cur is None:
            continue
        mt = re.match(r"^(STEM|PASS|PLAIN|TABLE|BOX|FIG|CAP|CH|CHROW|WHY|TITLE|SRC|STEM2):\s*(.*)$", line)
        if mt:
            tag, val = mt.groups()
            if tag == "STEM":
                cur["stem"] = val
            elif tag in ("PASS", "PLAIN", "TABLE", "BOX", "TITLE", "SRC", "STEM2"):
                cur["blocks"].append([tag, [val] if val else []])
            elif tag == "FIG":
                cur["blocks"].append(["FIG", [val.strip()]])
            elif tag == "CAP":
                cur["blocks"].append(["CAP", [val]])
            elif tag == "CH":
                if val:
                    cur["ch"].append(val)
            elif tag == "CHROW":
                cur["chrow"] = [x.strip() for x in val.split("|")]
            elif tag == "WHY":
                cur["why"] = val
            continue
        if not line.strip():
            continue
        # 이어지는 줄
        if tag == "STEM":
            cur["stem"] += " " + line.strip()
        elif tag in ("PASS", "PLAIN", "TABLE", "BOX", "TITLE", "SRC", "STEM2", "CAP"):
            cur["blocks"][-1][1].append(line)
        elif tag == "CH":
            cur["ch"].append(line.strip())
        elif tag == "WHY":
            cur["why"] += " " + line.strip()
    return items


# ----------------------------------------------------------------------------
# 정답 번호 자동 배정 (ans 속성이 없는 문항만)
#   CHROW: 정답 조합 앞에 * 표시 -> 표준 순서로 정렬 후 정답 번호 계산
#   CH   : 정답 선지 앞에 ★ 표시 -> 세트 전체 정답 분포가 고르게 되도록 위치 배정
# ----------------------------------------------------------------------------
def _combo_key(c):
    order = "ㄱㄴㄷㄹㅁㅂ"
    parts = [p.strip() for p in c.split(",")]
    return (len(parts), [order.index(p) for p in parts])


def finalize(items, seed=11):
    import random
    from collections import Counter
    rnd = random.Random(seed)
    qs_all = [i for i in items if i["kind"] == "Q"]
    pend = [i for i in qs_all if "ans" not in i["attrs"]]
    counts = Counter(int(i["attrs"]["ans"]) for i in qs_all if "ans" in i["attrs"])
    for it in pend:
        if it["chrow"]:
            cs = it["chrow"]
            marked = [c for c in cs if c.startswith("*")]
            assert len(marked) == 1, ("CHROW 정답 표시 오류", it["attrs"]["id"])
            cc = marked[0].lstrip("*").strip()
            cs = sorted([c.lstrip("*").strip() for c in cs], key=_combo_key)
            assert len(set(cs)) == 5, ("CHROW 중복", it["attrs"]["id"])
            it["chrow"] = cs
            a = cs.index(cc) + 1
            it["attrs"]["ans"] = str(a)
            counts[a] += 1
    chs = [i for i in pend if not i["chrow"]]
    total = len(qs_all)
    want = {a: total // 5 for a in range(1, 6)}
    for a in rnd.sample(range(1, 6), total % 5):
        want[a] += 1
    targets = []
    for a in range(1, 6):
        targets += [a] * max(0, want[a] - counts[a])
    while len(targets) < len(chs):
        targets.append(rnd.randint(1, 5))
    targets = targets[:len(chs)]
    fixed = {id(i): int(i["attrs"]["ans"]) for i in qs_all if "ans" in i["attrs"]}

    def _seq(tg):
        m = dict(zip([id(i) for i in chs], tg))
        return [fixed.get(id(i), m.get(id(i))) for i in qs_all]

    def _ok(seq):
        return all(not (seq[k] == seq[k + 1] == seq[k + 2]) for k in range(len(seq) - 2))

    for _ in range(5000):
        rnd.shuffle(targets)
        if _ok(_seq(targets)):
            break
    for it, t in zip(chs, targets):
        raw = [re.sub(r"^[①②③④⑤]\s*", "", c.strip()) for c in it["ch"]]
        stars = [i for i, c in enumerate(raw) if c.startswith("★")]
        assert len(stars) == 1 and len(raw) == 5, ("CH 정답 표시 오류", it["attrs"]["id"])
        correct = raw[stars[0]].lstrip("★").strip()
        others = [c for i, c in enumerate(raw) if i != stars[0]]
        rnd.shuffle(others)
        new = others[:t - 1] + [correct] + others[t - 1:]
        it["ch"] = new
        it["attrs"]["ans"] = str(t)
    return items


# ----------------------------------------------------------------------------
# HTML 렌더
# ----------------------------------------------------------------------------
def render_blocks(blocks):
    out = []
    skip = False
    for bi, (tag, lines) in enumerate(blocks):
        if skip:
            skip = False
            continue
        if tag == "PASS":
            out.append('<div class="box"><div class="bodytxt">%s</div></div>' % "<br>".join(esc(l) for l in lines))
        elif tag == "PLAIN":
            out.append('<div class="plain">%s</div>' % "<br>".join(esc(l) for l in lines))
        elif tag == "STEM2":
            out.append('<div class="stem2">%s</div>' % " ".join(esc(l) for l in lines))
        elif tag == "SRC":
            out.append('<div class="source">%s</div>' % esc(" ".join(lines)))
        elif tag == "BOX":
            out.append('<div class="box bogi"><div class="bogi-t">&lt;보 기&gt;</div><div class="bodytxt">%s</div></div>'
                       % "<br>".join(esc(l) for l in lines))
        elif tag == "TABLE":
            rows = [l.split("|") for l in lines if l.strip()]
            title = ""
            if rows and len(rows[0]) == 1:
                title = '<div class="ttl">%s</div>' % esc(rows[0][0]); rows = rows[1:]
            t = ['<table class="table">']
            for i, r in enumerate(rows):
                cells = "".join(("<th>%s</th>" if i == 0 else "<td>%s</td>") % esc(c.strip()) for c in r)
                t.append("<tr>%s</tr>" % cells)
            t.append("</table>")
            out.append(title + "".join(t))
        elif tag == "FIG":
            cap = ""
            if bi + 1 < len(blocks) and blocks[bi + 1][0] == "CAP":
                cap = '<figcaption class="caption">%s</figcaption>' % esc(" ".join(blocks[bi + 1][1]))
                skip = True
            out.append('<figure class="fig"><img src="fig/%s.svg">%s</figure>' % (lines[0], cap))
        elif tag == "CAP":
            out.append('<div class="caption">%s</div>' % esc(" ".join(lines)))
        elif tag == "TITLE":
            out.append('<div class="bundle-title">%s</div>' % esc(" ".join(lines)))
    return "".join(out)


def render_choices(it):
    if it["chrow"]:
        cells = "".join('<div class="cr"><span class="cn">%s</span><span>%s</span></div>' % (CIRC[i], esc(c))
                        for i, c in enumerate(it["chrow"]))
        return '<div class="choices crow">%s</div>' % cells
    rows = []
    for i, c in enumerate(it["ch"]):
        c = re.sub(r"^[①②③④⑤]\s*", "", c)
        rows.append('<div class="choice"><span class="cn">%s</span><span>%s</span></div>' % (CIRC[i], esc(c)))
    return '<div class="choices">%s</div>' % "".join(rows)


def render_q(it, numfmt):
    a = it["attrs"]
    n = a["id"]
    num = numfmt(n)
    body = '<article class="q"><div class="qnum">%s</div>' % num
    body += '<div class="stem">%s</div>' % esc(it["stem"])
    body += render_blocks(it["blocks"])
    body += render_choices(it)
    body += "</article>"
    return body


def render_bundle(it):
    return '<div class="bundle"><div class="bundle-hd">%s</div>%s</div>' % ("", render_blocks(it["blocks"]))


CSS = r"""
:root{--navy:#1F2A44;--warm:#E9E7E1;--burg:#7A2E35;--ink:#17191d;--muted:#666c74;--rule:#d9dbde}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#fff;color:var(--ink);font-family:"Noto Sans KR","Noto Sans",sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.cols{column-count:2;column-gap:8.4mm;column-rule:.35pt solid #dfe0e2;column-fill:auto}
.q{break-inside:avoid;page-break-inside:avoid;margin:0 0 7mm}
.qnum{font-family:Inter,"Noto Sans KR",sans-serif;font-size:9.4pt;font-weight:700;color:var(--navy);margin-bottom:2.2mm}
.stem{font-size:8.9pt;line-height:1.58;font-weight:500;letter-spacing:-.018em;margin-bottom:3mm;word-break:keep-all}
.stem2{font-size:8.7pt;line-height:1.55;font-weight:500;letter-spacing:-.018em;margin:2.6mm 0 2.4mm;word-break:keep-all}
.bodytxt{font-size:8.45pt;line-height:1.62;letter-spacing:-.018em;color:#25292e;word-break:keep-all;text-align:justify}
.plain{font-size:8.45pt;line-height:1.62;letter-spacing:-.018em;color:#25292e;margin:2.4mm 0 3mm;word-break:keep-all}
.box{border:.5pt solid #b9bcc1;padding:3.4mm 3.8mm;margin:2.4mm 0 3.2mm}
.bogi{padding-top:2.6mm}.bogi-t{text-align:center;font-size:8pt;font-weight:700;margin-bottom:1.6mm;color:var(--navy)}
.source{text-align:right;font-size:6.6pt;color:#7b8086;margin:-1.6mm 0 3mm}
.ttl{font-size:7.6pt;font-weight:700;margin:2.4mm 0 1mm;color:#333}
.table{width:100%;border-collapse:collapse;font-size:7.7pt;margin:1.4mm 0 3.2mm;line-height:1.42}
.table th,.table td{border:.45pt solid #b5b8bd;padding:1.5mm 1.5mm;text-align:center;word-break:keep-all}
.table th{background:#f2f1ed;font-weight:600}
.fig{margin:2.2mm 0 2.4mm;text-align:center;break-inside:avoid}.fig img{width:100%;height:auto;display:block}
.caption{font-size:6.6pt;color:#7d8288;margin:0 0 3mm;text-align:center}
.choices{font-size:8.45pt;line-height:1.55;margin-top:2.6mm;word-break:keep-all;letter-spacing:-.015em}
.choice{display:grid;grid-template-columns:4.6mm 1fr;gap:.6mm;margin-bottom:1.15mm}
.cn{font-family:"Noto Sans KR";}
.crow{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1.1mm .4mm}
.cr{display:grid;grid-template-columns:4.4mm 1fr;white-space:nowrap}
.bundle{break-inside:avoid;margin:0 0 5mm;border-top:.55pt solid var(--navy);padding-top:2.2mm;break-after:avoid}
.bundle-title{font-size:8.5pt;font-weight:700;margin-bottom:2.2mm;color:var(--ink)}
.sec{column-span:all;margin:0 0 5mm;padding:2.2mm 0;border-top:1.1pt solid var(--navy);border-bottom:.4pt solid var(--rule);display:flex;justify-content:space-between;align-items:baseline}
.sec b{font-size:10.5pt;letter-spacing:-.02em;color:var(--navy)}.sec span{font-size:7.4pt;color:var(--muted)}
.secline{margin:1mm 0 5mm;padding:1.6mm 0;border-top:.9pt solid var(--navy);border-bottom:.35pt solid var(--rule);break-after:avoid}
.secline b{font-size:9.6pt;color:var(--navy);letter-spacing:-.02em}.secline span{font-size:7pt;color:var(--muted);margin-left:2.4mm}
/* cover */
.cover{width:210mm;height:297mm;position:relative;padding:24mm 20mm 18mm;page-break-after:always}
.kicker{font-family:Inter;font-size:10.5pt;font-weight:700;letter-spacing:.11em;color:var(--navy)}
.toprule{height:.7pt;background:var(--navy);margin-top:7mm}
.accent{position:absolute;left:20mm;top:82mm;width:12mm;height:1.2mm;background:var(--burg)}
.covermain{margin-top:53mm}.covermain h1{margin:0;font-size:31pt;line-height:1.15;letter-spacing:-.045em;color:var(--ink)}
.covermain h2{margin:5mm 0 0;font-size:15pt;font-weight:500;letter-spacing:-.03em;color:#33383f}
.covermeta{margin-top:12mm;font-size:10pt;line-height:1.9;color:#3d4248}
.year{position:absolute;left:20mm;bottom:24mm;font-family:Inter;font-size:10pt;color:var(--muted);letter-spacing:.08em}
.series{position:absolute;right:20mm;bottom:24mm;font-family:Inter;font-size:8pt;color:var(--navy);font-weight:700;letter-spacing:.05em}
/* answer */
.ans{font-size:8.2pt}
.ans h3{font-size:12pt;margin:0 0 2mm;color:var(--navy);letter-spacing:-.02em}
.ans .sub{font-size:7.6pt;color:var(--muted);margin-bottom:4mm}
.akey{display:grid;grid-template-columns:repeat(10,1fr);gap:1.2mm;margin:2mm 0 5mm}
.akey div{border:.45pt solid #c9cbcf;padding:1.4mm 0;text-align:center;font-size:8.3pt}
.akey div b{font-family:Inter;color:var(--navy);margin-right:1.2mm;font-size:7.4pt}
.atab{width:100%;border-collapse:collapse;font-size:7.8pt;line-height:1.5}
.atab th{background:#f2f1ed;border-top:.8pt solid var(--navy);border-bottom:.45pt solid #b5b8bd;padding:1.4mm 1.6mm;text-align:left;font-weight:600}
.atab td{border-bottom:.35pt solid #dcdee1;padding:1.5mm 1.6mm;vertical-align:top;word-break:keep-all}
.atab tr{break-inside:avoid}
.atab td.n{font-family:Inter;font-weight:700;color:var(--navy);width:9mm}
.atab td.a{font-weight:700;width:9mm;text-align:center}
.atab td.l{width:9mm;text-align:center;color:var(--burg);font-family:Inter;font-weight:600}
.atab td.c{width:34mm;color:#3d4248}
.figw{text-align:center;margin:2mm 0 4mm}.figw img{width:100%}
.pb{break-before:page}
"""


def html_doc(inner, extra=""):
    return '<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>%s%s</style></head><body>%s</body></html>' % (CSS, extra, inner)


def build_cover(meta):
    return html_doc('''<style>@page{size:A4;margin:0}</style><section class="cover"><div class="kicker">ARC N°%(no)s</div><div class="toprule"></div><div class="accent"></div>
<div class="covermain"><h1>통합사회2</h1><h2>%(title)s</h2><div class="covermeta"><strong>%(school)s</strong><br>%(range)s<br>객관식 %(count)d문항</div></div>
<div class="year">2026</div><div class="series">ARC ACADEMIC SERIES</div></section>''' % meta)


def build_body(items, meta, numfmt=lambda n: "%02d" % int(n)):
    parts = ['<main class="cols">']
    for it in items:
        if it["kind"] == "BUNDLE":
            parts.append(render_bundle(it))
        else:
            parts.append(render_q(it, numfmt))
    parts.append("</main>")
    return html_doc("".join(parts), "@page{size:A4;margin:17mm 16.5mm 14mm}")


def build_answers(items, meta, concept_fig=None):
    qs = [i for i in items if i["kind"] == "Q"]
    keys = "".join('<div><b>%s</b>%s</div>' % (q["attrs"]["id"], CIRC[int(q["attrs"]["ans"]) - 1]) for q in qs)
    rows = []
    for q in qs:
        a = q["attrs"]
        rows.append('<tr><td class="n">%s</td><td class="a">%s</td><td class="l">%s</td><td class="c">%s</td><td>%s</td></tr>'
                    % (a["id"], CIRC[int(a["ans"]) - 1], a["lv"], esc(a.get("c", "")), esc(q["why"])))
    fig = ""
    if concept_fig:
        cf = concept_fig if isinstance(concept_fig, (list, tuple)) else [concept_fig]
        fig = '<div class="pb"></div><h3>핵심 개념 지도</h3><div class="sub">%s</div>' % meta.get("concept_sub", "")
        for k, c in enumerate(cf):
            fig += ('<div class="pb"></div>' if k else "") + '<div class="figw"><img src="fig/%s.svg"></div>' % c
    inner = '''<div class="ans"><h3>정답</h3><div class="sub">%s</div><div class="akey">%s</div>
<h3 style="margin-top:6mm">정답 및 핵심 근거</h3><div class="sub">난도(D3~D5)와 출제 개념은 학습자용 참고 표기이며, 근거는 시험범위(학교 학습지·교과서·『생각의 지도』) 안의 내용만 사용했습니다.</div>
<table class="atab"><tr><th>번호</th><th>정답</th><th>난도</th><th>핵심 개념</th><th>핵심 근거</th></tr>%s</table>%s</div>''' % (
        meta["answer_sub"], keys, "".join(rows), fig)
    return html_doc(inner, "@page{size:A4;margin:17mm 16.5mm 14mm}")


def to_pdf(html_path, pdf_path, head, foot_prefix, margins, header=True):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args=['--no-sandbox'])
        pg = b.new_page()
        pg.goto("file://" + str(Path(html_path).resolve()))
        pg.wait_for_timeout(500)
        kw = dict(path=str(pdf_path), format="A4", print_background=True, prefer_css_page_size=True)
        if header:
            hl, hr = head
            kw["display_header_footer"] = True
            kw["header_template"] = (
                '<div style="width:100%%;font-family:\'Noto Sans KR\';font-size:6.9pt;color:#666c74;padding:0 16.5mm;'
                'display:flex;justify-content:space-between;border-bottom:.45pt solid #d9dbde;margin:0 0 0 0;height:9mm;align-items:flex-start;-webkit-print-color-adjust:exact">'
                '<span style="font-family:Inter;font-weight:700;letter-spacing:.07em;color:#1F2A44">%s</span><span>%s</span></div>' % (hl, hr))
            kw["footer_template"] = (
                '<div style="width:100%%;text-align:center;font-family:Inter;font-size:7pt;color:#687078">'
                '<span style="-webkit-print-color-adjust:exact;display:inline-block;width:2mm;height:.7mm;background:#7A2E35;margin-right:1.8mm;vertical-align:2px"></span>'
                '%s<span class="pageNumber"></span></div>' % foot_prefix)
        pg.pdf(**kw)
        b.close()


def build_all(work_dir, name, meta, main_txt, out_dir, concept_fig=None):
    import pymupdf
    work = Path(work_dir)
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    items = finalize(parse(work / main_txt))
    # 번들 아이템 제외 문항 수
    qs = [i for i in items if i["kind"] == "Q"]
    meta = dict(meta); meta["count"] = len(qs)
    tmp = work / "_tmp"; tmp.mkdir(exist_ok=True)
    (tmp / "fig").mkdir(exist_ok=True)
    src_fig = work / "fig"
    for f in src_fig.glob("*.svg"):
        (tmp / "fig" / f.name).write_bytes(f.read_bytes())
    (tmp / "cover.html").write_text(build_cover(meta), encoding="utf-8")
    (tmp / "body.html").write_text(build_body(items, meta), encoding="utf-8")
    (tmp / "ans.html").write_text(build_answers(items, meta, concept_fig), encoding="utf-8")
    head = ("ARC N°%s" % meta["no"], meta["head_right"])
    to_pdf(tmp / "cover.html", tmp / "cover.pdf", head, "", {"top": "0", "bottom": "0", "left": "0", "right": "0"}, header=False)
    to_pdf(tmp / "body.html", tmp / "body.pdf", head, "", {"top": "17mm", "bottom": "14mm", "left": "16.5mm", "right": "16.5mm"})
    to_pdf(tmp / "ans.html", tmp / "ans.pdf", ("ARC N°%s · 정답" % meta["no"], meta["head_right"]), "A-", {"top": "17mm", "bottom": "14mm", "left": "16.5mm", "right": "16.5mm"})
    doc = pymupdf.open()
    for f in ("cover.pdf", "body.pdf", "ans.pdf"):
        d = pymupdf.open(str(tmp / f)); doc.insert_pdf(d); d.close()
    outp = out / name
    doc.save(str(outp), deflate=True, garbage=3); doc.close()
    return outp, len(qs)


if __name__ == "__main__":
    print("import 해서 사용하세요")

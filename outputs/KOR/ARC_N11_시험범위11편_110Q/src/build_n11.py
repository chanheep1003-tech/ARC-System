# -*- coding: utf-8 -*-
import re, collections, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import items_a, items_b, items_c
from common import Q
from passages_n11 import SETS

OUT = pathlib.Path(__file__).parent
CIRC = "①②③④⑤"
SERIES = "ARC N°11"

def mark(s):
    return re.sub(r"\{(.)\|([^}]*)\}", r'<span class="mk">\1</span><u>\2</u>', s)


def _assign():
    import random
    rng = random.Random(20261011)
    quota = len(Q) // 5
    fixed = {i: q["c"] for i, q in enumerate(Q) if q["fixed"]}
    for _ in range(20000):
        pool = [k for k in range(5) for _ in range(quota)]
        for a in fixed.values(): pool.remove(a)
        rng.shuffle(pool)
        it = iter(pool)
        seq = [fixed[i] if i in fixed else next(it) for i in range(len(Q))]
        if all(not (seq[i] == seq[i+1] == seq[i+2]) for i in range(len(seq) - 2)):
            break
    for i, q in enumerate(Q):
        if not q["fixed"]: q["t"] = seq[i]
_assign()

# ── 정답 위치 확정
answers = []
for q in Q:
    ch = list(q["choices"]); c = q["c"]; t = q["t"]
    if t is not None and t != c:
        ch[c], ch[t] = ch[t], ch[c]; c = t
    q["final"] = ch; q["ans"] = c
    answers.append(c)
cnt = collections.Counter(answers)
print("dist", {CIRC[k]: cnt[k] for k in range(5)})
for i in range(len(answers) - 2):
    assert not (answers[i] == answers[i+1] == answers[i+2]), f"triple at {i+1}"

def poem_lines(lines):
    return "".join(f'<div class="ln"><span class="lt">{mark(l)}</span><span class="lno">{(n if n % 5 == 0 else "")}</span></div>' for n, l in enumerate(lines, 1))

def stanza_lines(sts):
    out, n = [], 0
    for k, st in enumerate(sts):
        if k: out.append('<div class="gap"></div>')
        for l in st:
            n += 1
            out.append(f'<div class="ln"><span class="lt">{mark(l)}</span><span class="lno">{(n if n % 5 == 0 else "")}</span></div>')
    return "".join(out)

def render_passage(s, sub=False):
    if s["kind"] == "multi":
        out = ['<div class="passage">']
        for part in s["parts"]:
            out.append(f'<div class="plabel">{part["label"]}</div>')
            out.append(render_passage(part, sub=True))
        out.append("</div>")
        return "\n".join(out)
    cls = "sub" if sub else "passage"
    nl = len(s.get("lines", [])) or sum(len(x) for x in s.get("stanzas", []))
    out = [f'<div class="{cls}{" keep" if (s["kind"] in ("poem", "stanzas") and nl <= 14) else ""}">']
    if s.get("pre"):
        out.append(f'<div class="pre">{s["pre"]}</div>')
    if s.get("head"):
        out.append(f'<div class="phead">{s["head"]}</div>')
    k = s["kind"]
    if k == "poem":
        out.append(poem_lines(s["lines"]))
    elif k == "stanzas":
        out.append(stanza_lines(s["stanzas"]))
    elif k in ("prose", "essay"):
        for p in s["paras"]:
            if p.startswith("@@SUM@@"): out.append(f'<div class="pre">{p[7:]}</div>')
            elif p.startswith("@@VERSE@@"): out.append('<div class="verse">' + "<br>".join(mark(x) for x in re.split(r"\|(?![^{}]*\})", p[9:])) + "</div>")
            elif p.startswith("@@LAB@@"): out.append(f'<div class="plabel">{p[7:]}</div>')
            else: out.append(f'<p class="para">{mark(p)}</p>')
    elif k == "dialog":
        cur = None
        for st, sp, tx in s["turns"]:
            if st != cur:
                out.append(f'<div class="stage">[{st}]</div>'); cur = st
            out.append(f'<p class="turn"><b class="sp">{sp} 위원회</b> {mark(tx)}</p>')
        title, items = s["deal"]
        out.append('<div class="deal keep"><div class="dt">수목구 고속 철도 공사 계획 합의안</div>'
                   '<div class="dp">추진 위원회와 반대 위원회는 다음 내용에 합의하고, 합의 사항을 충실히 이행할 것을 약속합니다.</div>'
                   + "".join(f'<div class="di">{i}. {a}</div>' for i, (a, b) in enumerate(items, 1)) + '</div>')
    if s.get("src"):
        out.append(f'<div class="src">— {s["src"]} —</div>')
    if s.get("notes"):
        out.append('<div class="notes">' + "".join(f"<div>* {n}</div>" for n in s["notes"]) + "</div>")
    out.append("</div>")
    return "\n".join(out)

def table_html(rows, cls="tbl"):
    t = [f'<table class="{cls}"><tr>' + "".join(f"<th>{c}</th>" for c in rows[0]) + "</tr>"]
    for r in rows[1:]:
        t.append("<tr>" + "".join(f'<td class="{"c0" if j == 0 else ""}">{mark(c)}</td>' for j, c in enumerate(r)) + "</tr>")
    t.append("</table>")
    return "".join(t)

def render_q(i, q):
    h = [f'<article class="q"><div class="stem"><span class="qn">{i:02d}</span><span>{q["stem"]} <span class="pts">({q["pts"]:.1f}점)</span></span></div>']
    if q.get("box"):
        body = q["box"]
        if q.get("boxleft"):
            body = "".join(f'<div class="hl">{x}</div>' for x in body.split("<br>"))
        pre = f'<div class="boxpre">{q["boxpre"]}</div>' if q.get("boxpre") else ""
        h.append(f'<div class="box"><div class="boxt">&lt;{q["boxtitle"]}&gt;</div><div class="boxb">{pre}{body}</div></div>')
    if q.get("table"):
        h.append(table_html(q["table"]))
    short = all(len(re.sub("<[^>]+>", "", c)) <= 12 for c in q["final"])
    if short:
        h.append('<div class="choices inline">' + "".join(f'<span class="ci">{CIRC[k]} {c}</span>' for k, c in enumerate(q["final"])) + "</div>")
    else:
        h.append('<div class="choices">' + "".join(f'<div class="choice"><span>{CIRC[k]}</span><span>{c}</span></div>' for k, c in enumerate(q["final"])) + "</div>")
    h.append("</article>")
    return "\n".join(h)

def render_subj(s):
    h = [f'<article class="sq"><div class="sstem"><span class="qn">서·논술형 {s["no"]}.</span> {mark(s["stem"])} <span class="pts">({s["pts"]}점)</span> <span class="ref">[{s["sets"]}]</span></div>']
    if s.get("box"):
        body = s["box"]
        if s.get("boxleft") or "조건" in body:
            body = "".join(f'<div class="hl">{x}</div>' for x in body.split("<br>"))
        h.append(f'<div class="box wide"><div class="boxb">{body}</div></div>')
    if s.get("table"):
        h.append(table_html(s["table"]))
    n = s.get("lines", 0)
    if s.get("blanks"):
        h.append('<div class="ans"><div class="al">답안</div>' + "".join(f'<div class="bl"><b>{b}</b><i></i></div>' for b in s["blanks"]) + "</div>")
    elif n:
        h.append('<div class="ans"><div class="al">답:</div>' + '<div class="rule"></div>' * n + "</div>")
    h.append("</article>")
    return "\n".join(h)

CSS = """
@page { size: A4; margin: 19mm 15mm 16mm 15mm;
  @top-left { content: "ARC N°11"; font-family: Inter, 'Noto Sans CJK KR', sans-serif; font-weight:700; font-size:7pt; letter-spacing:.07em; color:#1F2A44; vertical-align:bottom; padding-bottom:2.4mm; border-bottom:.45pt solid #d9dbde; }
  @top-right { content: "공통국어2 · 시험범위 11편 핵심 110문항"; font-family:'Noto Sans CJK KR', sans-serif; font-size:6.9pt; color:#666c74; vertical-align:bottom; padding-bottom:2.4mm; border-bottom:.45pt solid #d9dbde; }
  @bottom-center { content: "- " counter(page) " -"; font-family: Inter, sans-serif; font-size:7.2pt; color:#555; }
  @bottom-left { content: "이 문제지는 ARC 학습용 자료이며, 무단 전재와 복제를 금합니다."; font-family:'Noto Sans CJK KR', sans-serif; font-size:6pt; color:#8a8f96; }
}
@page cover { margin:0; @top-left{content:none;border:none} @top-right{content:none;border:none} @bottom-center{content:none} @bottom-left{content:none} }
@page blank { margin:0; @top-left{content:none;border:none} @top-right{content:none;border:none} @bottom-center{content:none} @bottom-left{content:none} }
:root{--navy:#1F2A44;--warm:#E9E7E1;--burg:#7A2E35;--ink:#17191d;--muted:#666c74;--rule:#d9dbde}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#fff;color:var(--ink);font-family:'Noto Sans CJK KR','Noto Sans KR',sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.cover{page:cover;width:210mm;height:297mm;position:relative;padding:24mm 20mm 18mm;break-after:page}
.blankpage{page:blank;height:297mm;break-after:page}
.kicker{font-family:Inter,Arial,sans-serif;font-size:10.5pt;font-weight:700;letter-spacing:.11em;color:var(--navy)}
.toprule{height:.7pt;background:var(--navy);margin-top:7mm}
.accent{position:absolute;left:20mm;top:82mm;width:12mm;height:1.2mm;background:var(--burg)}
.covermain{margin-top:53mm}.covermain h1{margin:0;font-size:30pt;line-height:1.15;letter-spacing:-.045em}
.covermeta{margin-top:12mm;font-size:10pt;line-height:1.85;color:#3d4248}
.works{margin-top:14mm;font-size:8.6pt;line-height:1.95;color:#4a4f56;border-left:.8pt solid var(--warm);padding-left:4mm}
.year{position:absolute;left:20mm;bottom:24mm;font-family:Inter,sans-serif;font-size:10pt;color:var(--muted);letter-spacing:.08em}
.series{position:absolute;right:20mm;bottom:24mm;font-family:Inter,sans-serif;font-size:8pt;color:var(--navy);font-weight:700;letter-spacing:.05em}
.exam{column-count:2;column-gap:8mm;column-rule:.4pt solid #cfd2d6;column-fill:auto}
.bundle-title{break-before:page}
.bundle-title.first{break-before:auto}
.examhead{column-span:all;text-align:center;border-bottom:.8pt solid #333;padding-bottom:3.6mm;margin-bottom:3.2mm}
.ex-sm{font-size:7.6pt;color:#555;margin-bottom:1.6mm}
.ex-title{font-size:17pt;font-weight:700;letter-spacing:-.035em}
.ex-sub{font-size:7.6pt;color:var(--navy);margin-top:1.4mm;letter-spacing:.02em}
.info{display:grid;grid-template-columns:1fr 46mm 46mm;border:.65pt solid #777;margin-top:3.6mm;height:9mm;font-size:7.8pt;text-align:left}
.info>div{display:flex;align-items:center;padding:0 4mm;border-right:.45pt solid #aaa}.info>div:last-child{border-right:0}
.notice{column-span:all;border:.5pt solid #999;padding:2mm 3.2mm;font-size:7.3pt;line-height:1.55;color:#333;margin-bottom:4mm}
.bundle-title{break-after:avoid;font-size:8.5pt;font-weight:700;border:.7pt solid #444;padding:1.6mm 2.4mm;margin:1mm 0 3mm}
.passage{font-size:8.4pt;line-height:1.7;letter-spacing:-.018em;color:#23272c;border-bottom:.45pt solid var(--rule);padding-bottom:3mm;margin-bottom:5mm}
.ln{display:flex;justify-content:space-between;gap:2mm;break-inside:avoid}
.lno{font-family:Inter,sans-serif;font-size:6.6pt;color:#8a8f96;min-width:4mm;text-align:right}
.gap{height:3mm}
.plabel{font-weight:700;color:#1F2A44;font-size:8.4pt;margin:2.2mm 0 1.2mm;break-after:avoid}
.sub{margin-bottom:2mm}
.pre{font-size:7.8pt;line-height:1.58;border:.5pt solid #cfd2d6;background:#f7f6f2;padding:2mm 2.6mm;margin:1.4mm 0 2.2mm;text-align:justify}
.phead{font-weight:700;text-align:center;font-size:9pt;margin:1mm 0 2mm}
.verse{margin:1.2mm 0 2mm 6mm;line-height:1.7}
.keep{break-inside:avoid}
.para{margin:0 0 1.5mm;text-indent:3mm;text-align:justify}
.turn{margin:0 0 1.6mm;text-align:justify}
.sp{color:var(--navy);margin-right:1mm}
.stage{font-weight:700;font-size:7.8pt;color:var(--burg);margin:2.4mm 0 1.2mm}
.deal{border:.6pt solid #666;padding:2.2mm 3mm;margin:2.4mm 0 1mm;font-size:8pt;line-height:1.6}
.deal .dt{text-align:center;font-weight:700;margin-bottom:1mm}.deal .dp{font-size:7.6pt;margin-bottom:1mm}
.deal .di{padding-left:3mm;text-indent:-3mm}
.mk{font-size:8pt;margin-right:.3mm}
u{text-underline-offset:1.6pt;text-decoration-thickness:.5pt}
.src{text-align:right;font-size:7.2pt;color:#555a60;margin-top:2mm}
.notes{break-inside:avoid;font-size:6.7pt;line-height:1.55;color:#6b7076;margin-top:1.8mm}
.q{break-inside:avoid;margin-bottom:5.6mm}
.stem{display:grid;grid-template-columns:6mm 1fr;font-size:8.8pt;line-height:1.56;font-weight:500;letter-spacing:-.018em;margin-bottom:2.3mm}
.qn{font-family:Inter,sans-serif;font-weight:700;color:var(--navy);font-size:9pt}
.pts{font-weight:400;font-size:7.4pt;color:#6b7076;white-space:nowrap}
.box{border:.5pt solid #9aa0a6;padding:3.4mm 3.4mm 2.8mm;margin:2.8mm 0 2.6mm;font-size:8.05pt;line-height:1.62;letter-spacing:-.02em;text-align:justify}
.box.wide{margin:2mm 0 3mm}
.hl{padding-left:3.4mm;text-indent:-3.4mm}
.boxpre{text-align:justify;padding-bottom:2mm;margin-bottom:2mm;border-bottom:.4pt dashed #9aa0a6}
.boxt{text-align:center;font-size:7.6pt;margin:-5.2mm auto 1.4mm;background:#fff;width:15mm}
.tbl{width:100%;border-collapse:collapse;font-size:7.6pt;line-height:1.5;margin:2.4mm 0 2.8mm}
.tbl th,.tbl td{border:.45pt solid #9aa0a6;padding:1.5mm 1.8mm;vertical-align:middle}
.tbl th{background:#f1f0ec;font-weight:600;text-align:center}
.tbl td.c0{text-align:center;white-space:nowrap;font-weight:600}
.choices{font-size:8.4pt;line-height:1.6;letter-spacing:-.02em}
.choice{display:grid;grid-template-columns:4.6mm 1fr;gap:.5mm;margin-bottom:.8mm}
.choices.inline{display:flex;flex-wrap:wrap;gap:1mm 5mm}
.subj{break-before:page}
.pts{color:#7a7f86}
.sec-title{font-size:10.5pt;font-weight:700;border-bottom:.8pt solid #333;padding-bottom:2mm;margin-bottom:4mm}
.sec-note{font-size:7.6pt;color:#555;margin-bottom:4mm;line-height:1.6}
.sq{break-inside:avoid;margin-bottom:6mm}
.sstem{font-size:9pt;line-height:1.62;font-weight:500;margin-bottom:2mm}
.ref{font-size:7pt;color:#7a7f86;font-weight:400}
.ans{border:.6pt solid #666;padding:2mm 3mm 3mm;margin-top:2.4mm}
.al{font-size:7.6pt;color:#555;margin-bottom:.5mm}
.rule{border-bottom:.4pt dotted #8a8f96;height:8.2mm}
.bl{display:flex;align-items:flex-end;gap:2mm;height:8mm}.bl b{font-weight:600;font-size:8.6pt;width:5mm}.bl i{flex:1;border-bottom:.4pt dotted #8a8f96;height:5.4mm}
.end{text-align:center;font-size:8pt;color:#666;margin-top:4mm}
"""


def dlv(p): return "D2" if p <= 3.5 else "D4" if p >= 4.0 else "D3"
lv_cnt = collections.Counter(dlv(q["pts"]) for q in Q)
print("level", dict(lv_cnt), "sum_pts", round(sum(q["pts"] for q in Q), 1))

def student_html():
    p = [f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>{SERIES} 공통국어2</title><style>{CSS}</style></head><body>"]
    p.append("""<section class="cover"><div class="kicker">ARC N°11</div><div class="toprule"></div><div class="accent"></div>
<div class="covermain"><h1>공통국어2</h1><div class="covermeta"><strong>동북고등학교</strong><br>2학기 중간고사 파이널 · 시험 범위 11편 핵심 110문항</div>
<div class="works">교과서 1단원 — 「제망매가」 · 「속미인곡」 · 「춘향전」 · 「수라」 · 「아홉 켤레의 구두로 남은 사내」<br>교과서 2단원 — 논증하는 글 쓰기 · 지혜롭게 협상하기<br>보충 프린트 — 「탄궁가」 · 「팔원」 · 「기억할 만한 지나침」 · 칸트와 헤겔의 자유</div></div>
<div class="year">2026</div><div class="series">ARC ACADEMIC SERIES</div></section>""")
    p.append('<section class="blankpage"></section>')
    p.append('<section class="exam">')
    for k, st in enumerate(SETS):
        a, b = st["rng"]
        p.append(f'<div class="bundle-title{" first" if k == 0 else ""}">[{a:02d}~{b:02d}] 다음 글을 읽고 물음에 답하시오.</div>')
        p.append(render_passage(st))
        for i in range(a, b + 1):
            p.append(render_q(i, Q[i - 1]))
    p.append("</section></body></html>")
    return "\n".join(p)

def key_html():
    rows = []
    for st in SETS:
        a, b = st["rng"]
        cells = "".join(f"<td><span class='kn'>{i:02d}</span> {CIRC[Q[i-1]['ans']]}</td>" for i in range(a, b + 1))
        rows.append(f"<tr><th>{st['name']}</th>{cells}</tr>")
    css = CSS + """
body{font-size:8.6pt}
.kt{width:100%;border-collapse:collapse;font-size:8.6pt;margin-top:4mm}
.kt th,.kt td{border:.45pt solid #c9ccd0;padding:2.2mm 1.2mm;text-align:center}
.kt th{background:#f3f2ee;font-weight:600;width:30mm;font-size:7.8pt}
.kn{font-family:Inter,sans-serif;font-weight:700;color:#1F2A44;font-size:7.4pt}
h2{font-size:12pt;margin:0 0 1mm}.sub2{font-size:8pt;color:#666c74}.dist{font-size:7.6pt;color:#555a60;margin-top:3mm}
"""
    dist = " · ".join(f"{CIRC[k]} {cnt[k]}" for k in range(5))
    lv = " · ".join(f"{k} {lv_cnt[k]}문항" for k in ("D2", "D3", "D4"))
    return (f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>{SERIES} 정답</title><style>{css}</style></head><body>"
            f"<h2>{SERIES} 공통국어2 — 정답표</h2><div class='sub2'>시험 범위 11편 × 10문항 · 편집·검증용 (학생용 문제지에 포함하지 않음)</div>"
            f"<table class='kt'>{''.join(rows)}</table><div class='dist'>정답 분포: {dist} &nbsp;|&nbsp; 난이도 분포(내부 추정): {lv}</div></body></html>")

def explain_html():
    css = CSS + """
body{font-size:8.6pt}
h2{font-size:12pt;margin:0 0 1mm}.sub2{font-size:8pt;color:#666c74;margin-bottom:3mm}
.gt{font-weight:700;font-size:9.4pt;margin:5mm 0 1.6mm;border-bottom:.6pt solid #333;padding-bottom:1mm;break-after:avoid}
.ex{display:grid;grid-template-columns:9mm 8mm 1fr;gap:1mm 2mm;padding:1.3mm 0;border-bottom:.35pt dashed #d0d3d6;break-inside:avoid;line-height:1.55}
.en{font-family:Inter,sans-serif;font-weight:700;color:#1F2A44}.ea{font-weight:700;color:#7A2E35}.et{color:#2b2f34}
.el{font-size:6.6pt;color:#7a7f86}
"""
    out = [f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>{SERIES} 해설</title><style>{css}</style></head><body>",
           f"<h2>{SERIES} 공통국어2 — 간단 해설</h2><div class='sub2'>정답과 핵심 근거만 간단히 정리했습니다. (난이도는 내부 추정 D2~D4)</div>"]
    for st in SETS:
        a, b = st["rng"]
        out.append(f"<div class='gt'>[{a:02d}~{b:02d}] {st['name']}</div>")
        for i in range(a, b + 1):
            q = Q[i - 1]
            out.append(f"<div class='ex'><span class='en'>{i:02d}</span><span class='ea'>{CIRC[q['ans']]}</span><span class='et'>{q['e']} <span class='el'>[{dlv(q['pts'])}]</span></span></div>")
    out.append("</body></html>")
    return "\n".join(out)

(OUT / "student.html").write_text(student_html(), encoding="utf-8")
(OUT / "key.html").write_text(key_html(), encoding="utf-8")
(OUT / "explain.html").write_text(explain_html(), encoding="utf-8")
print("answers", "".join(CIRC[a] for a in answers))

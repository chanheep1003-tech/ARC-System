# -*- coding: utf-8 -*-
import re, html, collections, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from content import Q, SETS

OUT = pathlib.Path(__file__).parent
CIRC = "①②③④⑤"
SERIES = "ARC N°09"
UNIT = "공통국어2 · 보충자료 4편"

def mark(s):
    return re.sub(r"\{(.)\|([^}]*)\}", r'<span class="mk">\1</span><u>\2</u>', s)

# ── finalize answer positions
answers = []
for i, q in enumerate(Q, 1):
    ch = list(q["choices"]); c = q["c"]; t = q["t"]
    if t is not None and t != c:
        ch[c], ch[t] = ch[t], ch[c]; c = t
    q["final"] = ch; q["ans"] = c
    answers.append(c)
assert len(Q) == 40, len(Q)
cnt = collections.Counter(answers)
print("dist", {CIRC[k]: cnt[k] for k in range(5)})
for i in range(len(answers) - 2):
    assert not (answers[i] == answers[i+1] == answers[i+2]), f"triple at {i+1}"

def render_passage(s):
    keep = s["kind"] != "prose"
    out = [f'<div class="passage{" keep" if keep else ""}">']
    if s["kind"] == "poem":
        for n, ln in enumerate(s["lines"], 1):
            no = n if n % 5 == 0 else ""
            out.append(f'<div class="ln"><span class="lt">{mark(ln)}</span><span class="lno">{no}</span></div>')
    elif s["kind"] == "stanzas":
        n = 0
        for k, st in enumerate(s["stanzas"]):
            if k: out.append('<div class="gap"></div>')
            for ln in st:
                n += 1
                no = n if n % 5 == 0 else ""
                out.append(f'<div class="ln"><span class="lt">{mark(ln)}</span><span class="lno">{no}</span></div>')
    else:
        for p in s["paras"]:
            out.append(f'<p class="para">{mark(p)}</p>')
    out.append(f'<div class="src">— {s["src"]} —</div>')
    if s["notes"]:
        out.append('<div class="notes">' + "".join(f"<div>* {n}</div>" for n in s["notes"]) + "</div>")
    out.append("</div>")
    return "\n".join(out)

def render_q(i, q):
    h = [f'<article class="q"><div class="stem"><span class="qn">{i:02d}</span><span>{q["stem"]} <span class="pts">[{q["pts"]:.1f}점]</span></span></div>']
    if q.get("box"):
        body = q["box"]
        if q.get("boxleft"):
            body = "".join('<div class="hr"></div>' if x == "@@HR@@" else f'<div class="hl">{x}</div>' for x in body.split("<br>"))
        h.append(f'<div class="box"><div class="boxt">&lt;보 기&gt;</div><div class="boxb">{body}</div></div>')
    if q.get("table"):
        rows = q["table"]
        t = ['<table class="tbl"><tr>' + "".join(f"<th>{c}</th>" for c in rows[0]) + "</tr>"]
        for r in rows[1:]:
            t.append("<tr>" + "".join(f'<td class="{"c0" if j==0 else ""}">{c}</td>' for j, c in enumerate(r)) + "</tr>")
        t.append("</table>")
        h.append("".join(t))
    short = all(len(re.sub("<[^>]+>", "", c)) <= 12 for c in q["final"])
    if short:
        h.append('<div class="choices inline">' + "".join(f'<span class="ci"><b>{CIRC[k]}</b> {c}</span>' for k, c in enumerate(q["final"])) + "</div>")
    else:
        h.append('<div class="choices">' + "".join(f'<div class="choice"><span>{CIRC[k]}</span><span>{c}</span></div>' for k, c in enumerate(q["final"])) + "</div>")
    h.append("</article>")
    return "\n".join(h)

CSS = """
@page { size: A4; margin: 21mm 16.5mm 17mm 16.5mm;
  @top-left { content: "ARC N°09"; font-family: Inter, 'Noto Sans CJK KR', sans-serif; font-weight:700; font-size:7pt; letter-spacing:.07em; color:#1F2A44; vertical-align:bottom; padding-bottom:2.5mm; border-bottom:.45pt solid #d9dbde; }
  @top-right { content: "공통국어2 · 보충자료 4편"; font-family:'Noto Sans CJK KR', sans-serif; font-size:6.9pt; color:#666c74; vertical-align:bottom; padding-bottom:2.5mm; border-bottom:.45pt solid #d9dbde; }
  @bottom-center { content: counter(page, decimal-leading-zero); font-family: Inter, sans-serif; font-size:7pt; color:#687078; }
}
@page blank { margin:0; @top-left{content:none; border:none} @top-right{content:none; border:none} @bottom-center{content:none} }
@page cover { margin:0; @top-left{content:none; border:none} @top-right{content:none; border:none} @bottom-center{content:none} }
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
.set{column-count:2;column-gap:8.4mm;column-rule:.35pt solid #e4e5e7;column-fill:auto;break-before:page}
.set:first-of-type{break-before:auto}
.bundle-title{break-after:avoid;font-size:8.4pt;font-weight:700;border-top:.55pt solid var(--navy);padding-top:3mm;margin-bottom:3mm}
.passage{font-size:8.55pt;line-height:1.72;letter-spacing:-.018em;color:#23272c;border-bottom:.45pt solid var(--rule);padding-bottom:3.5mm;margin-bottom:6mm}
.ln{display:flex;justify-content:space-between;gap:2mm;break-inside:avoid}
.lno{font-family:Inter,sans-serif;font-size:6.6pt;color:#8a8f96;min-width:4mm;text-align:right}
.gap{height:3.2mm}
.passage.keep{break-inside:avoid}
.para{margin:0 0 1.6mm;text-indent:3mm;text-align:justify}
.mk{font-size:8pt;margin-right:.3mm}
u{text-underline-offset:1.6pt;text-decoration-thickness:.5pt}
.src{text-align:right;font-size:7.2pt;color:#555a60;margin-top:2.2mm}
.notes{break-inside:avoid;font-size:6.8pt;line-height:1.55;color:#6b7076;margin-top:2mm}
.q{break-inside:avoid;margin-bottom:6.2mm}
.stem{display:grid;grid-template-columns:6.4mm 1fr;font-size:8.95pt;line-height:1.58;font-weight:500;letter-spacing:-.018em;margin-bottom:2.6mm}
.qn{font-family:Inter,sans-serif;font-weight:700;color:var(--navy);font-size:9.3pt}
.pts{font-weight:400;font-size:7.6pt;color:#6b7076;white-space:nowrap}
.box{border:.5pt solid #bfc3c8;padding:3.6mm 3.8mm 3.2mm;margin:2.6mm 0 3mm;font-size:8.2pt;line-height:1.66;letter-spacing:-.02em;text-align:justify}
.hr{border-top:.4pt dashed #bfc3c8;margin:2.2mm 0 1.8mm}
.hl{padding-left:3.6mm;text-indent:-3.6mm}
.boxt{text-align:center;font-size:7.8pt;margin:-5.6mm auto 1.6mm;background:#fff;width:14mm}
.bsrc{text-align:right;font-size:7pt;color:#555a60;margin-top:1.4mm}
.bnote{font-size:6.6pt;color:#6b7076;margin-top:1.4mm;line-height:1.5}
.tbl{width:100%;border-collapse:collapse;font-size:7.7pt;line-height:1.5;margin:2.6mm 0 3mm}
.tbl th,.tbl td{border:.45pt solid #c9ccd0;padding:1.6mm 1.8mm;vertical-align:middle}
.tbl th{background:#f3f2ee;font-weight:600;text-align:center}
.tbl td.c0{text-align:center;white-space:nowrap}
.choices{font-size:8.5pt;line-height:1.62;letter-spacing:-.02em}
.choice{display:grid;grid-template-columns:4.7mm 1fr;gap:.6mm;margin-bottom:.9mm}
.choices.inline{display:flex;flex-wrap:wrap;gap:1mm 5mm}
.ci b{font-weight:400}
.key{page:auto}
"""

def student_html():
    parts = [f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>{SERIES} 공통국어2</title><style>{CSS}</style></head><body>"]
    parts.append("""<section class="cover"><div class="kicker">ARC N°09</div><div class="toprule"></div><div class="accent"></div>
<div class="covermain"><h1>공통국어2</h1><div class="covermeta"><strong>동북고등학교</strong><br>2학기 중간고사 대비 · 보충자료 4편 40문항</div>
<div class="works">정훈, 「탄궁가」<br>백석, 「팔원 - 서행시초3」<br>기형도, 「기억할 만한 지나침」<br>이행남, 「칸트의 도덕적 자율성으로부터 헤겔의 인륜적 자율성으로」</div></div>
<div class="year">2026</div><div class="series">ARC ACADEMIC SERIES</div></section>""")
    parts.append('<section class="blankpage"></section>')
    parts.append('<section class="set">')
    for s in SETS:
        a, b = s["rng"]
        parts.append(f'<div class="bundle-title">[{a:02d}~{b:02d}] 다음 글을 읽고 물음에 답하시오.</div>')
        parts.append(render_passage(s))
        for i in range(a, b + 1):
            parts.append(render_q(i, Q[i - 1]))
    parts.append("</section>")
    parts.append("</body></html>")
    return "\n".join(parts)

def key_html():
    rows = []
    for s in SETS:
        a, b = s["rng"]
        cells = "".join(f"<td><span class='kn'>{i:02d}</span> {CIRC[Q[i-1]['ans']]}</td>" for i in range(a, b + 1))
        rows.append(f"<tr><th>{s['title']}</th>{cells}</tr>")
    css = CSS + """
.kt{width:100%;border-collapse:collapse;font-size:8.6pt;margin-top:6mm}
.kt th,.kt td{border:.45pt solid #c9ccd0;padding:2.4mm 1.4mm;text-align:center}
.kt th{background:#f3f2ee;font-weight:600;width:30mm;font-size:7.8pt}
.kn{font-family:Inter,sans-serif;font-weight:700;color:#1F2A44;font-size:7.4pt}
h2{font-size:12pt;margin:0 0 1mm;letter-spacing:-.02em}
.sub{font-size:8pt;color:#666c74}
.dist{font-size:7.6pt;color:#555a60;margin-top:4mm}
"""
    dist = " · ".join(f"{CIRC[k]} {cnt[k]}" for k in range(5))
    return (f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>{SERIES} 정답</title><style>{css}</style></head><body>"
            f"<h2>{SERIES} 공통국어2 — 정답표</h2><div class='sub'>동북고등학교 2학기 중간고사 대비 · 보충자료 4편 40문항 · 편집·검증용 (학생용 문제지에 포함하지 않음)</div>"
            f"<table class='kt'>{''.join(rows)}</table><div class='dist'>정답 분포: {dist}</div></body></html>")

(OUT / "student.html").write_text(student_html(), encoding="utf-8")
(OUT / "key.html").write_text(key_html(), encoding="utf-8")
print("answers", "".join(CIRC[a] for a in answers))

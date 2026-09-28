"""Build the ARC N° PDF: cover, blank, two-column problems, blank, answer key.

usage: python3 build.py [--png OUTDIR]
Requires: Pretendard installed as a system font, Node + Playwright (Chromium).
"""
import os
import re
import subprocess
import sys

from items import ITEMS, BOGI_SETS

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "ARC_N_SCI_통합과학2_전자기유도_방향고난도20_V1.0"
HEAD_RIGHT = "통합과학2 · 전자기 유도 · 방향"
CIRCLED = "①②③④⑤"


def h(s):
    s = re.sub(r"\^\{([^}]*)\}", r"<sup>\1</sup>", s)
    s = re.sub(r"_\{([^}]*)\}", r"<sub>\1</sub>", s)
    s = s.replace("∼", "~")  # U+223C is missing from Pretendard
    for ch, j in zip("㉠㉡㉢㉣", "ㄱㄴㄷㄹ"):
        s = s.replace(ch, f'<span class="cj">{j}</span>')
    return s


def render_choices(item):
    if "choice_figs" in item:
        cells = "".join(f'<div class="cf"><span>{CIRCLED[i]}</span>{f}</div>' for i, f in enumerate(item["choice_figs"]))
        return f'<div class="choices figs">{cells}</div>'
    ch = item["choices"]
    if isinstance(ch, str):
        ch = BOGI_SETS[ch]
    if "choice_head" in item:
        head = "".join(f"<th>{c}</th>" for c in item["choice_head"])
        rows = "".join(
            f'<tr><td class="cn">{CIRCLED[i]}</td>' + "".join(f"<td>{h(c)}</td>" for c in r) + "</tr>"
            for i, r in enumerate(ch))
        return f'<table class="mtab"><tr><th></th>{head}</tr>{rows}</table>'
    short = item.get("choice_style") == "row" or all(len(c) <= 9 for c in ch)
    if short:
        cells = "".join(f'<span class="c"><b>{CIRCLED[i]}</b> {h(c)}</span>' for i, c in enumerate(ch))
        return f'<div class="choices row">{cells}</div>'
    cells = "".join(f'<div class="choice"><span>{CIRCLED[i]}</span><span>{h(c)}</span></div>'
                    for i, c in enumerate(ch))
    return f'<div class="choices">{cells}</div>'


def render_item(no, item):
    parts = [f'<article class="q"><div class="qnum">{no:02d}</div>',
             f'<div class="stem">{h(item["stem"])}</div>']
    for blk in item.get("blocks", []):
        parts.append(f'<div class="blk">{h(blk) if not blk.startswith("<svg") else blk}</div>')
    parts.append(f'<div class="ask">{h(item["q"])}</div>')
    if item.get("bogi"):
        lines = "".join(f'<div class="hang"><span>{"ㄱㄴㄷㄹ"[i]}.</span><span>{h(s)}</span></div>'
                        for i, s in enumerate(item["bogi"]))
        parts.append(f'<div class="bogi"><div class="bogi-t">보 기</div>{lines}</div>')
    parts.append(render_choices(item))
    parts.append("</article>")
    return "".join(parts)


CSS = r"""
:root{--navy:#1F2A44;--warm:#E9E7E1;--burg:#7A2E35;--ink:#17191d;--muted:#666c74;--rule:#d9dbde}
*{box-sizing:border-box}
@page{size:A4;margin:0}
html,body{margin:0;padding:0;background:#fff;color:var(--ink);
  font-family:Pretendard,"Noto Sans KR",sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:297mm;position:relative;background:#fff;page-break-after:always;overflow:hidden}
.page:last-child,.page.key{page-break-after:auto}
.cover{padding:24mm 20mm 18mm}
.kicker{font-size:10.5pt;font-weight:700;letter-spacing:.11em;color:var(--navy)}
.toprule{height:.7pt;background:var(--navy);margin-top:7mm}
.accent{position:absolute;left:20mm;top:82mm;width:12mm;height:1.2mm;background:var(--burg)}
.covermain{margin-top:53mm}
.covermain h1{margin:0;font-size:30pt;line-height:1.15;letter-spacing:-.045em;font-weight:700}
.covermain .sub{margin-top:5mm;font-size:13pt;font-weight:500;color:#2c3240;letter-spacing:-.02em}
.covermeta{margin-top:12mm;font-size:10pt;line-height:1.85;color:#3d4248}
.year{position:absolute;left:20mm;bottom:24mm;font-size:10pt;color:var(--muted);letter-spacing:.08em}
.series{position:absolute;right:20mm;bottom:24mm;font-size:8pt;color:var(--navy);font-weight:700;letter-spacing:.05em}
.body{padding:12.5mm 16.5mm 14mm}
.head{height:9mm;display:flex;justify-content:space-between;align-items:flex-start;border-bottom:.45pt solid var(--rule);
  font-size:6.9pt;color:var(--muted)}
.brand{font-weight:700;letter-spacing:.07em;color:var(--navy)}
.content{padding-top:6mm;height:252mm;display:grid;grid-template-columns:1fr 1fr}
.col{min-width:0}
.col.l{padding-right:4.2mm;border-right:.35pt solid #e4e5e7}
.col.r{padding-left:4.2mm}
.foot{position:absolute;left:16.5mm;right:16.5mm;bottom:8mm;border-top:.45pt solid var(--rule);padding-top:2mm;
  text-align:center;font-size:7pt;color:#687078}
.foot:before{content:"";display:inline-block;width:2mm;height:.7mm;background:var(--burg);margin-right:1.8mm;vertical-align:2px}
.q{margin-bottom:8.5mm}
.qnum{font-size:9.3pt;font-weight:700;color:var(--navy);margin-bottom:2.2mm;letter-spacing:.02em}
.stem,.ask{font-size:8.9pt;line-height:1.62;letter-spacing:-.02em;text-align:justify;word-break:keep-all}
.ask{margin-top:2.8mm}
.blk{margin-top:2.6mm;font-size:8.5pt;line-height:1.6;letter-spacing:-.02em}
.blk svg.fig{display:block;margin:1mm auto 0;height:auto}
sup,sub{font-size:68%;line-height:0}
sup{vertical-align:.45em}
sub{vertical-align:-.25em}
.cj{display:inline-block;width:1.15em;height:1.15em;line-height:1.05em;border:.6pt solid currentColor;border-radius:50%;
  text-align:center;font-size:.82em;vertical-align:.05em;margin:0 .06em}
.bogi{position:relative;border:.6pt solid #3a3d42;padding:4.2mm 3.6mm 2.6mm;margin-top:4.2mm}
.bogi-t{position:absolute;top:-1.85mm;left:50%;transform:translateX(-50%);background:#fff;padding:0 2.4mm;
  font-size:8pt;letter-spacing:.35em;font-weight:600}
.hang{display:grid;grid-template-columns:auto 1fr;column-gap:1.4mm;font-size:8.6pt;line-height:1.6;
  letter-spacing:-.02em;margin-bottom:1.1mm;text-align:left;word-break:keep-all}
.hang>span:first-child{white-space:nowrap}
.choices{margin-top:3.2mm;font-size:8.6pt;line-height:1.6;letter-spacing:-.02em}
.choices.row{display:flex;justify-content:space-between;flex-wrap:wrap;column-gap:2mm}
.choices.row .c b{font-weight:400}
.choices.figs{display:grid;grid-template-columns:1fr 1fr;gap:1.5mm 4mm}
.cf{display:grid;grid-template-columns:4mm 1fr;align-items:start}
.cf svg{width:100%;height:auto}
.choice{display:grid;grid-template-columns:4.6mm 1fr;margin-bottom:1mm;word-break:keep-all}
.eqtab{border-collapse:collapse;width:100%;font-size:8.2pt;border-top:.6pt solid #333;border-bottom:.6pt solid #333}
.eqtab td{padding:1.05mm 1.5mm;border-bottom:.3pt solid #ddd}
.eqtab tr:last-child td{border-bottom:none}
.eqk{white-space:nowrap;color:#222;width:1%}
.eqline{text-align:center;font-size:9pt;border:.5pt solid #bbb;padding:1.8mm 0;margin:0 6mm}
.eqline.small{border:none;padding:.6mm 0 1.4mm;font-size:8.6pt}
.dtab{border-collapse:collapse;width:100%;font-size:8.1pt;line-height:1.45;margin:0 auto}
.dtab th,.dtab td{border:.45pt solid #9a9da2;padding:1.3mm 1.2mm;text-align:center;word-break:keep-all}
.dtab th{background:#f3f2ee;font-weight:600}
.dtab.lefttd td:nth-child(2){text-align:left}
.mtab{border-collapse:collapse;margin-top:3mm;width:100%;font-size:8.6pt}
.mtab th{font-weight:500;border-bottom:.6pt solid #333;padding:.8mm 1mm;text-align:center}
.mtab td{padding:.8mm 1mm;text-align:center}
.mtab td.cn{width:6mm}
.note{font-size:7.6pt;color:#333;text-align:right;margin-top:.8mm}
.note.left{text-align:left}
.sublabel{font-size:8.5pt;margin-top:1mm}
.exp{font-size:8.6pt;line-height:1.6}
.exph{font-weight:600;margin-bottom:.6mm}
.srcbox,.talk{border:.5pt solid #9a9da2;padding:2.6mm 3mm 1.6mm}
.frac{display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle;font-size:7.6pt;line-height:1.25}
.frac span:first-child{border-bottom:.5pt solid #333;padding:0 .8mm}
.frac.n{font-size:8.4pt}
#measure{position:absolute;left:-9999px;top:0;width:calc((177mm - 8.4mm)/2)}
.keytab{border-collapse:collapse;width:100%;margin-top:8mm;font-size:10pt}
.keytab td{border:.5pt solid #9a9da2;text-align:center;padding:2.4mm 0;line-height:1.6}
.keyh{font-size:13pt;font-weight:700;margin-top:4mm}
"""

PAGINATE = r"""
<script>
(async () => {
  await document.fonts.ready;
  const mm = v => v * 96 / 25.4;
  const src = [...document.querySelectorAll('#source .q')];
  const measure = document.getElementById('measure');
  const colH = mm(252) - mm(6);
  const pages = document.getElementById('pages');
  let page = null, cols = [], ci = 0, used = 0, pno = 0;
  function newPage() {
    pno += 1;
    page = document.createElement('section');
    page.className = 'page body';
    page.innerHTML = `<header class="head"><div class="brand">ARC N°</div><div class="unit">__HEAD__</div></header>
      <main class="content"><div class="col l"></div><div class="col r"></div></main><footer class="foot">${pno}</footer>`;
    pages.appendChild(page);
    cols = [...page.querySelectorAll('.col')]; ci = 0; used = 0;
  }
  newPage();
  for (const q of src) {
    measure.appendChild(q);
    const hgt = q.getBoundingClientRect().height + mm(8.5);
    if (used > 0 && used + hgt - mm(8.5) > colH) {
      ci += 1; used = 0;
      if (ci > 1) newPage();
    }
    cols[ci].appendChild(q);
    used += hgt;
  }
  document.body.setAttribute('data-ready', '1');
})();
</script>
"""


def build_html():
    items = "".join(render_item(i + 1, it) for i, it in enumerate(ITEMS))
    cover = ('<section class="page cover"><div class="kicker">ARC N°</div><div class="toprule"></div>'
             '<div class="accent"></div><div class="covermain"><h1>통합과학2</h1>'
             '<div class="sub">전자기 유도 · 유도 전류와 자기장의 방향 · 고난도 20제</div>'
             '<div class="covermeta"><strong>동북고등학교</strong><br>2학기 중간고사 대비</div></div>'
             '<div class="year">2026</div><div class="series">ARC ACADEMIC SERIES</div></section>')
    blank = '<section class="page blank"></section>'
    return (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{NAME}</title>'
            f'<style>{CSS}</style></head><body>{cover}{blank}<div id="pages"></div>{blank}{key_section()}'
            f'<div id="measure"></div><div id="source" style="display:none">{items}</div>'
            f'{PAGINATE.replace("__HEAD__", HEAD_RIGHT)}</body></html>')


RENDER_JS = r"""
const { chromium } = require(process.env.PW_MODULE || 'playwright');
(async () => {
  const [,, html, pdf] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + html);
  await p.waitForSelector('body[data-ready="1"]');
  await p.pdf({ path: pdf, preferCSSPageSize: true, printBackground: true });
  await b.close();
})();
"""


KEY = [3, 1, 4, 4, 1, 3, 3, 2, 5, 3, 2, 2, 5, 2, 4, 4, 1, 5, 5, 1]


def key_section():
    cells = "".join(f'<td><b>{i + 1:02d}</b><br>{CIRCLED[k - 1]}</td>' + ("</tr><tr>" if i % 10 == 9 else "")
                    for i, k in enumerate(KEY))
    return (f'<section class="page body key"><header class="head"><div class="brand">ARC N°</div>'
            f'<div class="unit">{HEAD_RIGHT} · 정답</div></header>'
            f'<div class="keyh">정답</div><table class="keytab"><tr>{cells}</tr></table></section>')


def main():
    html_path = os.path.join(HERE, NAME + ".html")
    pdf_path = os.path.join(HERE, NAME + ".pdf")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(build_html())
    js = os.path.join(HERE, ".render.js")
    with open(js, "w") as f:
        f.write(RENDER_JS)
    env = dict(os.environ)
    env.setdefault("PW_MODULE", "/opt/node22/lib/node_modules/playwright")
    try:
        subprocess.run(["node", js, html_path, pdf_path], check=True, env=env)
    finally:
        os.remove(js)
    print(pdf_path)
    if "--png" in sys.argv:
        import pymupdf
        out = sys.argv[sys.argv.index("--png") + 1]
        os.makedirs(out, exist_ok=True)
        doc = pymupdf.open(pdf_path)
        for i, pg in enumerate(doc):
            pg.get_pixmap(dpi=110).save(os.path.join(out, f"p{i + 1:02d}.png"))
        print(f"{len(doc)} pages")


if __name__ == "__main__":
    main()

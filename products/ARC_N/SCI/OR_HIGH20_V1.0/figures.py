"""SVG figures for ARC N° 통합과학2 산화와 환원 고난도 20제.

All figures are plain line drawings (black/gray only) so they survive
black-and-white printing. viewBox width 400 maps to one column (~84 mm).
"""
import re

INK = "#1b1b1b"
GRAY = "#bdbdbd"
LIGHT = "#ececec"
FONT = "Pretendard, 'Noto Sans KR', sans-serif"

DEFS = f"""
<defs>
  <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="{INK}"/>
  </marker>
  <pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <line x1="0" y1="0" x2="0" y2="6" stroke="#777" stroke-width="1"/>
  </pattern>
  <pattern id="dots" width="7" height="7" patternUnits="userSpaceOnUse">
    <rect width="7" height="7" fill="{LIGHT}"/>
    <circle cx="2" cy="2" r="0.9" fill="#666"/>
    <circle cx="5.5" cy="5.5" r="0.9" fill="#666"/>
  </pattern>
</defs>"""


def chem(s, size):
    """Convert ^{..}/_{..} markup to tspans (superscript / subscript)."""
    small = round(size * 0.68, 1)
    out = []
    pos = 0
    for m in re.finditer(r"([\^_])\{([^}]*)\}", s):
        out.append(s[pos:m.start()])
        if m.group(1) == "^":
            out.append(f'<tspan dy="{-size*0.38:.1f}" font-size="{small}">{m.group(2)}</tspan>'
                       f'<tspan dy="{size*0.38:.1f}">​</tspan>')
        else:
            out.append(f'<tspan dy="{size*0.25:.1f}" font-size="{small}">{m.group(2)}</tspan>'
                       f'<tspan dy="{-size*0.25:.1f}">​</tspan>')
        pos = m.end()
    out.append(s[pos:])
    return "".join(out)


def t(x, y, s, size=13, anchor="middle", weight=400, fill=INK, extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" '
            f'font-weight="{weight}" fill="{fill}" font-family="{FONT}" {extra}>{chem(s, size)}</text>')


def circ_jamo(x, y, jamo, r=7.5, size=10):
    """Circled hangul (㉠ etc.) drawn by hand; the body font lacks those glyphs."""
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="1"/>'
            f'<text x="{x}" y="{y + size*0.36:.1f}" font-size="{size}" text-anchor="middle" '
            f'fill="{INK}" font-family="{FONT}">{jamo}</text>')


def svg(w, h, body, maxw="100%"):
    return (f'<svg class="fig" viewBox="0 0 {w} {h}" style="width:{maxw}" '
            f'xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>')


def box(x, y, w, h, fill="#fff", rx=2, sw=1.2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{INK}" stroke-width="{sw}"/>'


def line(x1, y1, x2, y2, sw=1.2, dash=None, arrow=False, color=INK):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    a = ' marker-end="url(#ah)"' if arrow else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d}{a}/>'


def path(d, sw=1.2, fill="none", arrow=False, dash=None, color=INK):
    a = ' marker-end="url(#ah)"' if arrow else ""
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{sw}"{a}{ds}/>'


# ---------------------------------------------------------------- 01
def fig01():
    b = []
    b.append(box(18, 64, 92, 34) + t(64, 86, "포도당"))
    b.append(box(160, 64, 80, 34) + t(200, 86, "CO_{2}", weight=600))
    b.append(box(300, 64, 82, 34) + t(341, 86, "CO"))
    b.append(box(160, 152, 80, 32) + t(200, 173, "메테인"))
    b.append(path("M184,64 C176,24 88,24 72,62", arrow=True))
    b.append(t(128, 26, "(가)", 12))
    b.append(path("M58,98 C70,142 164,142 178,100", arrow=True))
    b.append(t(116, 148, "(나)", 12))
    b.append(line(200, 152, 200, 100, arrow=True))
    b.append(t(214, 131, "(다)", 12, anchor="start"))
    b.append(line(240, 81, 298, 81, arrow=True))
    b.append(t(269, 72, "(라)", 12))
    return svg(400, 192, "".join(b), "88%")


# ---------------------------------------------------------------- 02
def fig02():
    ox, oy = 58, 190
    b = [line(ox, oy, 380, oy), line(ox, oy, ox, 18)]
    ys = {1: 140, 2: 90, 3: 40}
    for n, y in ys.items():
        b.append(line(ox - 4, y, ox, y))
        b.append(t(ox - 8, y + 4, f"{'' if n == 1 else n}N", 12, anchor="end"))
    b.append(t(ox - 8, oy + 4, "0", 12, anchor="end"))
    b.append(line(ox, 40, 196, 40, sw=0.8, dash="3,3"))
    b.append(line(ox, 90, 268, 90, sw=0.8, dash="3,3"))
    b.append(path(f"M{ox},{oy} C88,70 126,40 196,40 L372,40", sw=1.6))
    b.append(path(f"M{ox},{oy} C118,118 176,90 268,90 L372,90", sw=1.6))
    b.append(t(376, 36, "B", 13, anchor="end", weight=600))
    b.append(t(376, 84, "A", 13, anchor="end", weight=600))
    b.append(t(380, 210, "시간", 12, anchor="end"))
    b.append(t(ox - 4, 12, "발생한 H_{2} 분자 수", 12, anchor="start"))
    return svg(400, 216, "".join(b), "86%")


# ---------------------------------------------------------------- 04
def _beaker(x, y, w, h):
    return (path(f"M{x - 4},{y} L{x},{y + 4} L{x},{y + h} L{x + w},{y + h} L{x + w},{y + 4} L{x + w + 4},{y}", sw=1.3)
            + line(x, y + 16, x + w, y + 16, sw=0.8, dash="4,3"))


def _ion(x, y, label, kind):
    fill = {"X": "#fff", "Y": GRAY, "M": "#4a4a4a"}[kind]
    tc = "#fff" if kind == "M" else INK
    return (f'<circle cx="{x}" cy="{y}" r="11" fill="{fill}" stroke="{INK}" stroke-width="1.1"/>'
            f'<text x="{x}" y="{y + 4.3}" font-size="12" text-anchor="middle" fill="{tc}" '
            f'font-family="{FONT}" font-weight="600">{label}</text>')


def _fill_ions(x, y, w, h, kinds):
    cols = 4
    out = []
    gx = w / (cols + 0.4)
    for i, k in enumerate(kinds):
        r, c = divmod(i, cols)
        cx = x + gx * (c + 0.7)
        cy = y + h - 16 - r * 27
        out.append(_ion(round(cx, 1), cy, k, k))
    return "".join(out)


def fig04():
    b = []
    rows = [("Ⅰ", ["X"] * 8, ["X", "X", "M", "M", "M"], 8),
            ("Ⅱ", ["Y"] * 4, ["Y", "Y", "M", "M", "M"], 136)]
    for label, before, after, y0 in rows:
        b.append(t(14, y0 + 52, label, 14, weight=600))
        b.append(_beaker(38, y0 + 8, 128, 84))
        b.append(_fill_ions(38, y0 + 8, 128, 84, before))
        b.append(line(180, y0 + 52, 226, y0 + 52, arrow=True))
        b.append(t(203, y0 + 44, "M 3N개", 11))
        b.append(_beaker(242, y0 + 8, 128, 84))
        b.append(_fill_ions(242, y0 + 8, 128, 84, after))
        b.append(t(102, y0 + 110, "반응 전", 12))
        b.append(t(306, y0 + 110, "반응 후", 12))
    return svg(400, 256, "".join(b), "92%")


# ---------------------------------------------------------------- 05
def _tube_path(cx, top=34, bot=160, r=17):
    return f"M{cx - r},{top} L{cx - r},{bot} A{r},{r} 0 0 0 {cx + r},{bot} L{cx + r},{top}"


def _liquid(cx, level, fill, top=34, bot=160, r=17):
    d = (f"M{cx - r + 1},{level} L{cx - r + 1},{bot} A{r - 1},{r - 1} 0 0 0 {cx + r - 1},{bot} "
         f"L{cx + r - 1},{level} Z")
    return f'<path d="{d}" fill="{fill}" stroke="none"/>' + line(cx - r, level, cx + r, level, sw=0.9)


def _nail(cx, y1, y2):
    return (line(cx, y1, cx, y2 - 6, sw=3.2, color="#555")
            + f'<path d="M{cx - 1.6},{y2 - 6} L{cx},{y2} L{cx + 1.6},{y2 - 6} Z" fill="#555"/>'
            + line(cx - 6, y1, cx + 6, y1, sw=2.6, color="#555"))


def fig05():
    b = []
    xs = [52, 150, 250, 348]
    # (가) water
    b.append(_liquid(xs[0], 128, LIGHT))
    b.append(_nail(xs[0], 44, 172))
    # (나) boiled water + oil layer
    b.append(_liquid(xs[1], 52, LIGHT))
    b.append(f'<rect x="{xs[1] - 16}" y="44" width="32" height="8" fill="url(#hatch)" stroke="none"/>')
    b.append(line(xs[1] - 17, 44, xs[1] + 17, 44, sw=0.9))
    b.append(_nail(xs[1], 66, 172))
    # (다) calcium chloride + cotton + stopper
    for i, (gx, gy) in enumerate([(-9, 166), (-2, 170), (6, 166), (11, 160), (-11, 158), (0, 160), (8, 172), (-6, 173), (3, 153), (-3, 150)]):
        b.append(f'<circle cx="{xs[2] + gx}" cy="{gy}" r="3" fill="#fff" stroke="{INK}" stroke-width="0.8"/>')
    b.append(path(f"M{xs[2] - 16},142 q4,-4 8,0 q4,4 8,0 q4,-4 8,0 q4,4 8,0", sw=0.9))
    b.append(_nail(xs[2], 60, 138))
    b.append(f'<rect x="{xs[2] - 20}" y="22" width="40" height="16" rx="2" fill="#3a3a3a"/>')
    # (라) salt water
    b.append(_liquid(xs[3], 128, "url(#dots)"))
    b.append(_nail(xs[3], 44, 172))
    for i, cx in enumerate(xs):
        b.append(path(_tube_path(cx), sw=1.3))
        b.append(t(cx, 202, ["(가)", "(나)", "(다)", "(라)"][i], 13))
    labels = [["물"], ["끓여 식힌 물", "+ 식용유"], ["염화 칼슘", "+ 마개"], ["소금물"]]
    for cx, ls in zip(xs, labels):
        for j, s in enumerate(ls):
            b.append(t(cx, 219 + j * 15, s, 11.5))
    return svg(400, 252, "".join(b), "96%")


# ---------------------------------------------------------------- 06
def fig06():
    b = [line(24, 34, 384, 34, sw=1.4, arrow=True)]
    for x, s in [(66, "금, 구리"), (156, "청동"), (240, "철"), (326, "알루미늄")]:
        b.append(f'<circle cx="{x}" cy="34" r="3.2" fill="{INK}"/>')
        b.append(t(x, 22, s, 12.5))
    b.append(t(24, 56, "과거", 11.5, anchor="start", fill="#444"))
    b.append(t(384, 56, "현재", 11.5, anchor="end", fill="#444"))
    return svg(400, 64, "".join(b), "92%")


# ---------------------------------------------------------------- 08
def fig08():
    b = []
    b.append(t(8, 16, "(가)", 12.5, anchor="start"))
    # heated tube
    b.append(path(_tube_path(64, top=44, bot=132, r=13), sw=1.3))
    b.append(f'<rect x="49" y="36" width="30" height="12" rx="2" fill="#3a3a3a"/>')
    b.append(f'<path d="M52,122 L52,132 A12,12 0 0 0 76,132 L76,122 Z" fill="url(#dots)" stroke="none"/>')
    b.append(line(51, 122, 77, 122, sw=0.8))
    # delivery tube
    b.append(path("M64,36 L64,20 L170,20 L170,112", sw=1.6))
    # limewater tube
    b.append(path(_tube_path(170, top=58, bot=140, r=14), sw=1.3))
    b.append(_liquid(170, 96, LIGHT, top=58, bot=140, r=14))
    b.append(line(170, 20, 170, 124, sw=1.6))
    for by in (112, 104):
        b.append(f'<circle cx="{173 if by == 112 else 167}" cy="{by}" r="2.2" fill="#fff" stroke="{INK}" stroke-width="0.7"/>')
    # burner
    b.append(path("M50,178 L56,160 L72,160 L78,178 Z", sw=1.2))
    b.append(line(64, 160, 64, 154, sw=1.2))
    b.append(path("M64,153 C58,148 60,142 64,136 C68,142 70,148 64,153 Z", sw=1.0, fill="#fff"))
    b.append(line(79, 128, 96, 168, sw=0.8))
    b.append(t(98, 180, "산화 구리(Ⅱ)", 11.5, anchor="start"))
    b.append(t(98, 195, "+ 탄소", 11.5, anchor="start"))
    b.append(line(186, 118, 204, 124, sw=0.8))
    b.append(t(206, 130, "석회수", 11.5, anchor="start"))
    # (나)
    b.append(t(262, 16, "(나)", 12.5, anchor="start"))
    b.append(f'<path d="M281,96 L281,176 L381,176 L381,96 Z" fill="{LIGHT}" stroke="none"/>')
    b.append(line(281, 96, 381, 96, sw=0.9))
    b.append(path("M277,56 L281,60 L281,176 L381,176 L381,60 L385,56", sw=1.3))
    b.append(f'<rect x="324" y="34" width="14" height="128" fill="#fff" stroke="{INK}" stroke-width="1.2"/>')
    b.append(line(338, 46, 356, 38, sw=0.8))
    b.append(t(358, 40, "아연판", 11.5, anchor="start"))
    b.append(t(331, 196, "황산 구리(Ⅱ) 수용액", 11.5))
    return svg(400, 204, "".join(b), "96%")


# ---------------------------------------------------------------- 09
def fig09():
    b = []
    # (가): decreasing to -3
    ox, oy = 52, 40
    b.append(line(ox, 18, ox, 172))
    b.append(line(ox, oy, 190, oy))
    for v in range(0, 4):
        y = oy + v * 38
        b.append(line(ox - 4, y, ox, y))
        b.append(t(ox - 8, y + 4, "0" if v == 0 else f"-{v}", 12, anchor="end"))
    b.append(line(ox, oy + 114, 118, oy + 114, sw=0.8, dash="3,3"))
    b.append(path(f"M{ox},{oy} C74,120 92,154 118,154 L186,154", sw=1.6))
    b.append(t(190, 34, "시간", 11.5, anchor="end"))
    b.append(t(120, 194, "(가)", 12.5))
    # (나): increasing to 82
    ox2, oy2 = 256, 160
    b.append(line(ox2, 18, ox2, oy2))
    b.append(line(ox2, oy2, 394, oy2))
    for v, y in [(0, 160), (41, 100), (82, 40)]:
        b.append(line(ox2 - 4, y, ox2, y))
        b.append(t(ox2 - 8, y + 4, str(v), 12, anchor="end"))
    b.append(line(ox2, 40, 330, 40, sw=0.8, dash="3,3"))
    b.append(path(f"M{ox2},{oy2} C280,70 300,40 330,40 L390,40", sw=1.6))
    b.append(t(394, 178, "시간", 11.5, anchor="end"))
    b.append(t(326, 194, "(나)", 12.5))
    b.append(t(ox - 40, 12, "판의 질량 변화량(상댓값)", 11, anchor="start"))
    b.append(t(ox2 - 40, 12, "판의 질량 변화량(상댓값)", 11, anchor="start"))
    return svg(400, 200, "".join(b))


# ---------------------------------------------------------------- 11
def fig11():
    ox, oy = 56, 212
    sx, sy = 38, 22.5
    X = lambda n: ox + n * sx
    Y = lambda n: oy - n * sy
    b = [line(ox, oy, 386, oy), line(ox, oy, ox, 16)]
    for n in range(0, 9):
        b.append(line(X(n), oy, X(n), oy + 4))
    for n in (0, 3, 6, 8):
        b.append(t(X(n), oy + 18, str(n), 12))
    for n in (5, 6, 8):
        b.append(line(ox - 4, Y(n), ox, Y(n)))
        b.append(t(ox - 8, Y(n) + 4, str(n), 12, anchor="end"))
    b.append(t(ox - 8, oy + 4, "0", 12, anchor="end"))
    b.append(line(ox, Y(5), X(3), Y(5), sw=0.8, dash="3,3"))
    b.append(line(X(3), Y(5), X(3), oy, sw=0.8, dash="3,3"))
    b.append(line(ox, Y(6), X(6), Y(6), sw=0.8, dash="3,3"))
    b.append(line(X(6), Y(6), X(6), oy, sw=0.8, dash="3,3"))
    b.append(path(f"M{X(0)},{Y(8)} L{X(3)},{Y(5)} L{X(6)},{Y(6)} L{X(8)},{Y(6)}", sw=1.7))
    b.append(t(ox - 4, 10, "양이온 수(N)", 12, anchor="start"))
    b.append(t(388, oy + 34, "넣어 준 C 원자 수(N)", 12, anchor="end"))
    return svg(400, 252, "".join(b), "86%")


# ---------------------------------------------------------------- 12
def _plate(x0, coat):
    b = []
    b.append(f'<rect x="{x0}" y="44" width="164" height="46" fill="url(#hatch)" stroke="{INK}" stroke-width="1.2"/>')
    b.append(f'<rect x="{x0}" y="32" width="164" height="12" fill="#fff" stroke="{INK}" stroke-width="1.2"/>')
    cx = x0 + 82
    b.append(f'<path d="M{cx - 13},31 L{cx},56 L{cx + 13},31 Z" fill="#fff" stroke="none"/>')
    b.append(path(f"M{cx - 13},32 L{cx - 7},44 L{cx},56 L{cx + 7},44 L{cx + 13},32", sw=1.2))
    b.append(line(cx + 20, 22, cx + 7, 38, sw=0.8))
    b.append(t(cx + 22, 20, "긁힌 부분", 11, anchor="start"))
    b.append(line(x0 + 30, 38, x0 + 14, 18, sw=0.8))
    b.append(t(x0 + 12, 15, coat, 12.5, anchor="middle", weight=600))
    b.append(t(x0 + 36, 74, "철", 12.5, extra='paint-order="stroke" stroke="#fff" stroke-width="4"'))
    return "".join(b)


def fig12():
    b = [_plate(14, "X"), _plate(222, "Y")]
    b.append(t(96, 110, "(가)", 12.5))
    b.append(t(304, 110, "(나)", 12.5))
    return svg(400, 116, "".join(b))


# ---------------------------------------------------------------- 16
def fig16():
    b = []
    b.append(box(8, 8, 156, 30) + t(86, 28, "A, B, C 가루 각 3N개", 12))
    b.append(box(214, 8, 178, 30) + t(303, 28, "D^{2+} 8N개가 든 수용액", 12))
    b.append(line(86, 38, 172, 70, arrow=True))
    b.append(line(303, 38, 226, 70, arrow=True))
    b.append(box(118, 72, 164, 28, fill="#f4f4f4") + t(200, 91, "섞어 충분히 반응 → 거름", 12))
    b.append(t(106, 64, "(가)", 12, anchor="end"))
    b.append(line(170, 100, 86, 128, arrow=True))
    b.append(line(232, 100, 300, 128, arrow=True))
    b.append(box(26, 130, 120, 30) + t(78, 150, "고체", 12.5) + circ_jamo(108, 145, "ㄱ"))
    b.append(box(196, 130, 198, 50))
    b.append(t(268, 149, "용액", 12.5) + circ_jamo(298, 145, "ㄴ"))
    b.append(t(295, 170, "A^{2+} 3N개, B^{2+} 3N개, D^{2+} 2N개", 11.5))
    b.append(line(295, 180, 295, 214, arrow=True))
    b.append(t(305, 202, "A를 충분히 넣음", 11.5, anchor="start"))
    b.append(t(285, 202, "(나)", 12, anchor="end"))
    b.append(box(196, 216, 198, 30) + t(295, 236, "금속 양이온: A^{2+}뿐", 12))
    return svg(400, 250, "".join(b))


# ---------------------------------------------------------------- 17
def fig17():
    ox, oy = 52, 176
    s = 34
    b = [line(ox, oy, 388, oy), line(ox, oy, ox, 22)]
    for n in range(1, 5):
        y = oy - n * s
        b.append(line(ox - 4, y, ox, y))
        b.append(t(ox - 8, y + 4, str(n), 12, anchor="end"))
        b.append(line(ox, y, 388, y, sw=0.5, dash="2,3", color="#999"))
    b.append(t(ox - 8, oy + 4, "0", 12, anchor="end"))

    def bar(x, n, style):
        h = n * s
        fill = {"X": "#fff", "Y": "#9e9e9e", "Z": "url(#hatch)"}[style]
        return f'<rect x="{x}" y="{oy - h}" width="30" height="{h}" fill="{fill}" stroke="{INK}" stroke-width="1.1"/>'

    groups = [("반응 전", [("X", 3), ("Y", 4)], 88), ("반응 후", [("X", 0), ("Y", 4), ("Z", 2)], 234)]
    for gname, bars, gx in groups:
        for i, (k, n) in enumerate(bars):
            x = gx + i * 42
            if n:
                b.append(bar(x, n, k))
            b.append(t(x + 15, oy + 16, k, 12, weight=600))
        width = len(bars) * 42 - 12
        b.append(t(gx + width / 2, oy + 36, gname, 12.5))
    b.append(t(ox - 4, 14, "이온 수(N)", 12, anchor="start"))
    return svg(400, 218, "".join(b), "88%")


# ---------------------------------------------------------------- 18
def fig18():
    b = []
    xs = [30, 72, 114, 156, 198, 240, 282, 324, 366]
    labels = ["Mg", "ㄱ", "Zn", "ㄴ", "Fe", "ㄷ", "Cu", "ㄹ", "Ag"]
    for x, s in zip(xs, labels):
        if s in "ㄱㄴㄷㄹ":
            b.append(circ_jamo(x, 22, s, r=8.5, size=11))
        else:
            b.append(t(x, 27, s, 14, weight=600))
    b.append(line(366, 48, 30, 48, sw=1.2, arrow=True))
    b.append(t(30, 66, "반응성이 크다", 11.5, anchor="start"))
    b.append(t(366, 66, "반응성이 작다", 11.5, anchor="end"))
    return svg(400, 72, "".join(b), "92%")


# ---------------------------------------------------------------- 20
def fig20():
    b = []
    ox, oy = 52, 150
    b.append(line(ox, oy, 190, oy) + line(ox, oy, ox, 18))
    y6, y4 = 44, 80
    for lab, y in [("6N", y6), ("4N", y4)]:
        b.append(line(ox - 4, y, ox, y))
        b.append(t(ox - 8, y + 4, lab, 12, anchor="end"))
    b.append(t(ox - 8, oy + 4, "0", 12, anchor="end"))
    tx = 128
    b.append(line(tx, y4, tx, oy, sw=0.8, dash="3,3"))
    b.append(line(ox, y4, tx, y4, sw=0.8, dash="3,3"))
    b.append(path(f"M{ox},{y6} C84,58 104,80 {tx},{y4} L186,{y4}", sw=1.6))
    b.append(t(tx, oy + 16, "t", 12, extra='font-style="italic"'))
    b.append(t(190, oy + 16, "시간", 11.5, anchor="end"))
    b.append(t(ox - 4, 12, "양이온 수", 11.5, anchor="start"))
    b.append(t(120, 188, "(가)", 12.5))

    ox2 = 256
    b.append(line(ox2, oy, 394, oy) + line(ox2, oy, ox2, 18))
    yw = 70
    b.append(line(ox2 - 4, yw, ox2, yw))
    b.append(t(ox2 - 8, yw + 4, "w_{0}", 12, anchor="end", extra='font-style="italic"'))
    b.append(t(ox2 - 8, oy + 4, "0", 12, anchor="end"))
    b.append(line(ox2 + 76, yw, ox2 + 76, oy, sw=0.8, dash="3,3"))
    b.append(line(ox2, yw, 390, yw, sw=1.6))
    b.append(t(ox2 + 76, oy + 16, "t", 12, extra='font-style="italic"'))
    b.append(t(394, oy + 16, "시간", 11.5, anchor="end"))
    b.append(t(ox2 - 4, 12, "판 A의 질량", 11.5, anchor="start"))
    b.append(t(326, 188, "(나)", 12.5))
    return svg(400, 196, "".join(b))

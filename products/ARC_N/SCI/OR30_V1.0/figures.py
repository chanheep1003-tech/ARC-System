"""SVG figures for ARC N° 통합과학2 산화와 환원 30제.

Particle models show metal cations only (one circle = N ions unless the
stem says otherwise). viewBox width 400 = one column (~84 mm).
"""
from figparts import (GRAY, INK, LIGHT, MID, axes, circle, line, path, rect, svg, t, ti, tick_x,
                      tick_y)

DARK = "#4a4a4a"


# ------------------------------------------------------------------ parts
def beaker(x, y, w, h, level=18, fill=LIGHT):
    liq = f'<rect x="{x}" y="{y + level}" width="{w}" height="{h - level}" fill="{fill}" stroke="none"/>'
    return (liq + line(x, y + level, x + w, y + level, sw=0.8)
            + path(f"M{x - 5},{y} L{x},{y + 5} L{x},{y + h} L{x + w},{y + h} L{x + w},{y + 5} L{x + w + 5},{y}",
                   sw=1.3))


def ion(x, y, label, fill="#fff", r=12.5, size=10.5):
    tc = "#fff" if fill == DARK else INK
    return (circle(x, y, r, fill=fill, sw=1.1)
            + t(x, y + size * 0.36, label, size, weight=600, fill=tc))


def spots(x, y, w, h, n, level=18, cols=3, skip_mid=None):
    """n evenly spread particle centres inside the liquid of beaker(x, y, w, h)."""
    rows = (n + cols - 1) // cols
    top, bot = y + level + 16, y + h - 15
    out = []
    xs = [x + w * (c + 0.5) / cols for c in range(cols)]
    if skip_mid is not None:
        xs = [x + 18, x + w * 0.33, x + w * 0.67, x + w - 18][:cols]
    for i in range(n):
        r, c = divmod(i, cols)
        cy = top if rows == 1 else top + (bot - top) * r / (rows - 1)
        dx = 7 if r % 2 else -7
        out.append((xs[c] + (dx if cols > 2 else 0), cy))
    return out


def fill_of(k):
    return {"A": "#fff", "B": GRAY, "C": DARK, "X": "#fff", "Y": GRAY, "Z": DARK}.get(k[0], "#fff")


def particles(x, y, w, h, kinds, cols=3):
    return "".join(ion(px, py, k, fill_of(k)) for (px, py), k in zip(spots(x, y, w, h, len(kinds), cols=cols), kinds))


def plate(x, y, w, h, fill="#fff", label=""):
    out = rect(x, y, w, h, fill=fill, sw=1.1)
    if label:
        out += t(x + w / 2, y + 14, label, 11, weight=600)
    return out


def deposit(x, y1, y2, side=1):
    """Small bumps of deposited metal along a vertical plate edge x."""
    out = []
    yy = y1
    while yy < y2:
        out.append(f'<circle cx="{x + side * 2.2:.1f}" cy="{yy:.1f}" r="2.6" fill="{MID}" stroke="none"/>')
        yy += 7
    return "".join(out)


# ---------------------------------------------------------------- 02
def fig02():
    b = []
    for k, (x0, lab, kinds) in enumerate([(22, "(가) 반응 전", ["Ag^{+}"] * 6),
                                         (232, "(나) 반응 후", ["Ag^{+}", "Cu^{2+}", "Ag^{+}", "Cu^{2+}"])]):
        w, h = 146, 118
        b.append(beaker(x0, 26, w, h))
        cx = x0 + w / 2
        b.append(line(cx, 8, cx, 132, sw=3.4, color="#6a6a6a"))
        if k:
            b.append(deposit(cx - 2, 52, 130, -1) + deposit(cx + 2, 56, 130, 1))
        pos = [(x0 + 30, 66), (x0 + 30, 118), (x0 + 50, 92), (x0 + w - 30, 66), (x0 + w - 30, 118), (x0 + w - 50, 92)]
        if k:
            pos = [(x0 + 34, 70), (x0 + 36, 116), (x0 + w - 34, 70), (x0 + w - 36, 116)]
        for (px, py), s in zip(pos, kinds):
            b.append(ion(px, py, s, GRAY if s.startswith("Cu") else "#fff", r=13.5, size=10))
        b.append(t(cx, 164, lab, 12))
    b.append(line(99, 14, 112, 9, sw=0.7) + t(114, 12, "구리 선", 10.5, anchor="start"))
    return svg(400, 172, "".join(b), "94%")


# ---------------------------------------------------------------- 04
def _dip(x0, plate_lab, sol_lab, tag, dep=True):
    w, h = 120, 104
    out = [beaker(x0, 30, w, h)]
    px = x0 + w / 2 - 9
    out.append(plate(px, 10, 18, 112, fill="#fff"))
    out.append(t(px + 9, 26, plate_lab, 11.5, weight=600))
    if dep:
        out.append(deposit(px, 62, 120, -1) + deposit(px + 18, 62, 120, 1))
    out.append(t(x0 + w / 2, 152, sol_lab, 11))
    out.append(t(x0 + w / 2, 170, tag, 12))
    return "".join(out)


def fig04():
    b = [_dip(38, "X", "Y(NO_{3})_{2} 수용액", "(가)"), _dip(242, "Y", "ZNO_{3} 수용액", "(나)")]
    return svg(400, 176, "".join(b), "88%")


# ---------------------------------------------------------------- 06
def _tube(cx, top, bot, r):
    return f"M{cx - r},{top} L{cx - r},{bot} A{r},{r} 0 0 0 {cx + r},{bot} L{cx + r},{top}"


def fig06():
    b = []
    b.append(path(_tube(64, 44, 132, 13), sw=1.3))
    b.append(rect(49, 36, 30, 12, fill="#3a3a3a", sw=0.8, rx=2))
    b.append('<path d="M52,122 L52,132 A12,12 0 0 0 76,132 L76,122 Z" fill="url(#dots)" stroke="none"/>')
    b.append(line(51, 122, 77, 122, sw=0.8))
    b.append(path("M64,36 L64,20 L190,20 L190,112", sw=1.6))
    b.append(f'<path d="M177,96 L177,140 A13,13 0 0 0 203,140 L203,96 Z" fill="{LIGHT}" stroke="none"/>')
    b.append(line(176, 96, 204, 96, sw=0.9))
    b.append(path(_tube(190, 58, 140, 14), sw=1.3))
    for cx, cy in ((193, 118), (187, 108)):
        b.append(circle(cx, cy, 2.2, sw=0.7))
    b.append(path("M50,178 L56,160 L72,160 L78,178 Z", sw=1.2))
    b.append(line(64, 160, 64, 154, sw=1.2))
    b.append(path("M64,153 C58,148 60,142 64,136 C68,142 70,148 64,153 Z", sw=1.0, fill="#fff"))
    b.append(line(79, 128, 94, 164, sw=0.8))
    b.append(t(96, 174, "산화 구리(Ⅱ) + 탄소 가루", 11, anchor="start"))
    b.append(line(206, 120, 222, 126, sw=0.8))
    b.append(t(224, 130, "석회수", 11, anchor="start"))
    return svg(290, 184, "".join(b), "72%")


# ---------------------------------------------------------------- 07
def fig07():
    b = []
    panels = [(8, "(가)", ["X"] * 6), (142, "(나)", ["X", "Y", "X", "Y"]), (276, "(다)", ["Z"] * 3)]
    for x0, lab, kinds in panels:
        w, h = 116, 108
        b.append(beaker(x0, 10, w, h))
        if len(kinds) == 6:
            pos = [(x0 + 26, 50), (x0 + 58, 50), (x0 + 90, 50), (x0 + 26, 94), (x0 + 58, 94), (x0 + 90, 94)]
        elif len(kinds) == 4:
            pos = [(x0 + 34, 52), (x0 + 82, 52), (x0 + 82, 94), (x0 + 34, 94)]
        else:
            pos = [(x0 + 34, 56), (x0 + 82, 56), (x0 + 58, 96)]
        for (px, py), k in zip(pos, kinds):
            b.append(ion(px, py, k, fill_of(k)))
        b.append(t(x0 + w / 2, 138, lab, 12))
    b.append(line(126, 64, 138, 64, sw=1.1, arrow=True) + line(260, 64, 272, 64, sw=1.1, arrow=True))
    return svg(400, 146, "".join(b), "96%")


# ---------------------------------------------------------------- 08
def fig08():
    b = [beaker(30, 34, 150, 112)]
    b.append(path("M106,10 L106,40 Q104,70 110,96 Q116,120 108,138", sw=3.0, color="#6a6a6a"))
    b.append(line(114, 20, 150, 14, sw=0.7) + t(154, 17, "마그네슘 리본", 12, anchor="start"))
    b.append(t(105, 168, "황산 구리(Ⅱ) 수용액", 12))
    return svg(250, 174, "".join(b), "56%")


# ---------------------------------------------------------------- 09
def fig09():
    ox, oy = 56, 176
    sx, sy = 36, 15
    X = lambda v: ox + v * sx
    Y = lambda v: oy - v * sy
    b = [axes(ox, oy, 378, 12), t(378, oy + 32, "금속의 질량(g)", 11.5, anchor="end")]
    b.append(t(ox - 4, 8, "생성된 산화물의 질량(g)", 11.5, anchor="start"))
    for v in (3, 4, 6, 8):
        b.append(tick_x(X(v), oy, str(v)))
    for v in (5, 10):
        b.append(tick_y(ox, Y(v), str(v)))
        b.append(line(ox, Y(v), 372, Y(v), sw=0.5, dash="2,3", color="#999"))
    b.append(t(ox - 7, oy + 4, "0", 11.5, anchor="end"))
    for v in (3, 4, 6, 8):
        b.append(line(X(v), oy, X(v), Y(10 if v in (6, 8) else 5), sw=0.5, dash="2,3", color="#999"))
    b.append(line(ox, oy, X(8), Y(10), sw=1.6) + line(ox, oy, X(6), Y(10), sw=1.6))
    b.append(circle(X(4), Y(5), 2.6, fill=INK, sw=0.5) + circle(X(8), Y(10), 2.6, fill=INK, sw=0.5))
    b.append(circle(X(3), Y(5), 2.6, fill=INK, sw=0.5) + circle(X(6), Y(10), 2.6, fill=INK, sw=0.5))
    b.append(t(X(6) - 6, Y(10) - 8, "마그네슘", 11, anchor="end"))
    b.append(t(X(8) + 4, Y(10) - 8, "구리", 11, anchor="middle"))
    return svg(400, 214, "".join(b), "86%")


# ---------------------------------------------------------------- 12
def _lamp(cx, plate_y, tag):
    out = []
    out.append(path(f"M{cx - 34},172 L{cx - 26},128 Q{cx},118 {cx + 26},128 L{cx + 34},172 Z", sw=1.3, fill="#fff"))
    out.append(f'<path d="M{cx - 31},172 L{cx - 25},146 L{cx + 25},146 L{cx + 31},172 Z" fill="{LIGHT}" stroke="none"/>')
    out.append(rect(cx - 7, 112, 14, 10, fill="#fff", sw=1.1))
    out.append(line(cx, 112, cx, 104, sw=1.6))
    out.append(path(f"M{cx},104 C{cx - 20},90 {cx - 16},56 {cx},20 C{cx + 16},56 {cx + 20},90 {cx},104 Z",
                    sw=1.1, fill="#fff"))
    out.append(path(f"M{cx},102 C{cx - 9},94 {cx - 8},78 {cx},64 C{cx + 8},78 {cx + 9},94 {cx},102 Z",
                    sw=0.9, fill="url(#dots)"))
    # copper plate held horizontally by tongs
    out.append(rect(cx - 30, plate_y - 3, 60, 6, fill=GRAY, sw=1.0))
    out.append(line(cx + 30, plate_y, cx + 74, plate_y - 10, sw=1.4) + line(cx + 30, plate_y + 1, cx + 74, plate_y + 8, sw=1.4))
    out.append(t(cx, 192, tag, 12))
    return "".join(out)


def fig12():
    b = [_lamp(92, 44, "(가)"), _lamp(292, 86, "(나)")]
    b.append(line(104, 80, 148, 92, sw=0.7) + t(150, 96, "겉불꽃", 10.5, anchor="start"))
    b.append(line(296, 98, 330, 122, sw=0.7) + t(332, 127, "속불꽃", 10.5, anchor="start"))
    b.append(t(12, 16, "구리판", 10.5, anchor="start") + line(40, 20, 66, 41, sw=0.7))
    return svg(400, 198, "".join(b), "88%")


# ---------------------------------------------------------------- 13
def fig13():
    ox, oy = 52, 170
    sx, sy = 64, 23
    X = lambda v: ox + v * sx
    Y = lambda v: oy - v * sy
    b = [axes(ox, oy, 370, 12), t(370, oy + 32, "넣어 준 B 원자 수", 11.5, anchor="end")]
    b.append(t(ox - 4, 8, "수용액 속 이온 수", 11.5, anchor="start"))
    for v in (1, 2, 3, 4):
        b.append(tick_x(X(v), oy, f"{'' if v == 1 else v}N"))
    for v in (3, 6):
        b.append(tick_y(ox, Y(v), f"{v}N"))
    b.append(t(ox - 7, oy + 4, "0", 11.5, anchor="end"))
    b.append(line(X(3), Y(3), X(3), oy, sw=0.6, dash="3,3"))
    b.append(line(ox, Y(3), X(3), Y(3), sw=0.6, dash="3,3"))
    b.append(line(ox, Y(6), 360, Y(6), sw=1.6))
    b.append(path(f"M{X(0)},{Y(6) + 0.1} L{X(3)},{Y(3)} L360,{Y(3)}", sw=1.6))
    b.append(t(356, Y(6) - 7, "음이온", 11, anchor="end"))
    b.append(t(356, Y(3) - 7, "양이온", 11, anchor="end"))
    return svg(400, 208, "".join(b), "86%")


# ---------------------------------------------------------------- 15
def fig15():
    b = []
    w, h = 136, 112
    b.append(beaker(30, 12, w, h))
    pos = [(58, 54), (98, 54), (138, 54), (58, 98), (98, 98), (138, 98)]
    for (px, py), k in zip(pos, ["A", "B", "A", "A", "B", "A"]):
        b.append(ion(px, py, k, fill_of(k)))
    b.append(t(98, 142, "반응 전", 12))
    b.append(line(180, 68, 222, 68, sw=1.2, arrow=True) + t(201, 60, "C", 11.5, weight=600))
    b.append(beaker(236, 12, w, h))
    for (px, py), k in zip([(270, 54), (338, 54), (270, 98), (338, 98)], ["B", "C", "C", "B"]):
        b.append(ion(px, py, k, fill_of(k)))
    b.append(t(304, 142, "반응 후", 12))
    return svg(400, 150, "".join(b), "88%")


# ---------------------------------------------------------------- 18
def _al(x0, y0, w, h, letters, coat=False):
    out = []
    out.append(rect(x0, y0, w, h, fill="url(#hatch)" if coat else "#fff", sw=1.2))
    for i, ch in enumerate(letters):
        cx = x0 + w * (i + 1) / (len(letters) + 1)
        out.append(rect(cx - 13, y0 + h / 2 - 14, 26, 28, fill="#fff" if coat else GRAY, sw=0.6 if coat else 0.9,
                        color=MID if coat else INK))
        out.append(t(cx, y0 + h / 2 + 5, ch, 14, weight=700))
    return "".join(out)


def fig18():
    b = [_al(10, 34, 104, 60, "과학")]
    b.append(t(62, 22, "스티커", 10.5))
    b.append(t(62, 150, "(가)", 12))
    b.append(beaker(146, 16, 108, 112))
    b.append(rect(186, 6, 28, 110, fill="#fff", sw=1.1))
    b.append(t(200, 150, "(나)", 12))
    b.append(_al(286, 34, 104, 60, "과학", coat=True))
    b.append(t(338, 150, "(다)", 12))
    return svg(400, 156, "".join(b), "94%")


# ---------------------------------------------------------------- 22
def _qbox(cx, y, w, lines_):
    h = 14 + 14 * len(lines_)
    out = rect(cx - w / 2, y, w, h, fill="#fff", sw=1.1, rx=4)
    for i, s in enumerate(lines_):
        out += t(cx, y + 17 + 14 * i, s, 10.5)
    return out, y + h


def fig22():
    b = []
    top, tb = _qbox(200, 4, 120, ["Mg, Fe, Cu, Ag"])
    b.append(top)
    q1, q1b = _qbox(200, 34, 236, ["묽은 염산에 넣으면 기체가 발생하는가?"])
    b.append(line(200, tb, 200, 34, arrow=True))
    b.append(q1)
    q2, q2b = _qbox(102, 88, 188, ["황산 아연 수용액에 넣으면", "아연이 석출되는가?"])
    q3, q3b = _qbox(298, 88, 188, ["질산 은 수용액에 넣으면", "은이 석출되는가?"])
    b.append(path(f"M160,{q1b} L102,{q1b} L102,88", arrow=True) + t(128, q1b + 13, "예", 10.5))
    b.append(path(f"M240,{q1b} L298,{q1b} L298,88", arrow=True) + t(272, q1b + 13, "아니요", 10.5))
    b.append(q2 + q3)
    for cx, lab in ((54, "A"), (150, "B"), (250, "C"), (346, "D")):
        b.append(circle(cx, q2b + 36, 12, sw=1.1) + t(cx, q2b + 40.5, lab, 12, weight=700))
    for x0, x1, x2 in ((102, 54, 150), (298, 250, 346)):
        b.append(line(x0, q2b, x0, q2b + 10, sw=1.1))
        b.append(path(f"M{x0},{q2b + 10} L{x1},{q2b + 10} L{x1},{q2b + 22}", arrow=True))
        b.append(path(f"M{x0},{q2b + 10} L{x2},{q2b + 10} L{x2},{q2b + 22}", arrow=True))
        b.append(t(x1 - 12, q2b + 20, "예", 10, anchor="end") + t(x2 + 12, q2b + 20, "아니요", 10, anchor="start"))
    return svg(400, q2b + 54, "".join(b), "92%")


def series():
    syms = ["K", "Ca", "Na", "Mg", "Al", "Zn", "Fe", "Ni", "Sn", "Pb", "(H)", "Cu", "Hg", "Ag", "Pt", "Au"]
    b = []
    for i, s in enumerate(syms):
        b.append(t(18 + i * 24.4, 18, s, 11.5, weight=600 if s != "(H)" else 400))
    b.append(line(386, 32, 14, 32, sw=1.1, arrow=True))
    b.append(t(14, 48, "반응성이 크다", 10.5, anchor="start") + t(386, 48, "반응성이 작다", 10.5, anchor="end"))
    return svg(400, 54, "".join(b), "94%")


# ---------------------------------------------------------------- 23
def fig23():
    ox, oy = 56, 176
    sx, sy = 92, 17
    X = lambda v: ox + v * sx
    Y = lambda v: oy - v * sy
    b = [axes(ox, oy, 372, 12), t(372, oy + 32, "반응한 B 원자 수", 11.5, anchor="end")]
    b.append(t(ox - 4, 8, "수용액 속 금속 양이온 수", 11.5, anchor="start"))
    for v in (1, 2, 3):
        b.append(tick_x(X(v), oy, f"{'' if v == 1 else v}N"))
    for v in (3, 6, 9):
        b.append(tick_y(ox, Y(v), f"{v}N"))
        b.append(line(ox, Y(v), X(3), Y(v), sw=0.5, dash="2,3", color="#999"))
    b.append(t(ox - 7, oy + 4, "0", 11.5, anchor="end"))
    for v in (1, 2, 3):
        b.append(line(X(v), oy, X(v), Y(9), sw=0.5, dash="2,3", color="#999"))
    b.append(line(X(0), Y(9), X(3), Y(0), sw=1.7))
    b.append(line(X(0), Y(0), X(3), Y(3), sw=1.7, dash="6,3"))
    b.append(t(X(1.0) + 4, Y(7.3), "A 이온", 11, anchor="start", extra='paint-order="stroke" stroke="#fff" stroke-width="4"'))
    b.append(t(X(3) + 5, Y(3) + 4, "B 이온", 11, anchor="start"))
    return svg(400, 212, "".join(b), "86%")


# ---------------------------------------------------------------- 27
def fig27():
    ox, oy = 52, 172
    sx = 50
    X = lambda v: ox + v * sx
    Y = lambda v: oy - 22 - (v - 4) * 36
    b = [axes(ox, oy, 376, 12), t(376, oy + 32, "넣어 준 C 원자 수(N)", 11.5, anchor="end")]
    b.append(rect(ox - 6, oy - 16, 12, 6, fill="#fff", sw=0, color="#fff"))
    b.append(line(ox - 6, oy - 11, ox + 6, oy - 15, sw=1.0) + line(ox - 6, oy - 7, ox + 6, oy - 11, sw=1.0))
    b.append(t(ox - 4, 8, "수용액 속 양이온 수(N)", 11.5, anchor="start"))
    for v in range(1, 7):
        b.append(tick_x(X(v), oy, str(v)))
    for v in (5, 6, 7):
        b.append(tick_y(ox, Y(v), str(v)))
        b.append(line(ox, Y(v), X(6.4), Y(v), sw=0.5, dash="2,3", color="#999"))
    b.append(t(ox - 7, oy + 4, "0", 11.5, anchor="end"))
    for v in (3, 5):
        b.append(line(X(v), oy, X(v), Y(7 if v == 3 else 5), sw=0.6, dash="3,3"))
    b.append(path(f"M{X(0)},{Y(6)} L{X(3)},{Y(7)} L{X(5)},{Y(5)} L{X(6.4)},{Y(5)}", sw=1.7))
    return svg(400, 208, "".join(b), "86%")


# ---------------------------------------------------------------- 30
def fig30():
    b = []
    ox, oy = 44, 150
    b.append(axes(ox, oy, 190, 18, "", ""))
    b.append(t(ox - 4, 12, "수용액 속 양이온 수", 11, anchor="start"))
    y6, y4 = 44, 88
    b.append(tick_y(ox, y6, "6N") + tick_y(ox, y4, "4N"))
    b.append(t(ox - 7, oy + 4, "0", 11.5, anchor="end"))
    t1, t2 = 104, 158
    b.append(path(f"M{ox},{y6} C66,60 84,{y4} {t1},{y4} L184,{y4}", sw=1.6))
    b.append(line(t1, y4, t1, oy, sw=0.6, dash="3,3") + line(t2, y4, t2, oy, sw=0.6, dash="3,3"))
    b.append(ti(t1, oy + 15, "t_{1}", 12) + ti(t2, oy + 15, "t_{2}", 12))
    b.append(t(116, 188, "(가)", 12))

    ox2 = 250
    b.append(axes(ox2, oy, 396, 18, "", ""))
    b.append(t(ox2 - 4, 12, "금속판의 질량 변화(상댓값)", 11, anchor="start"))
    ya, yb = 40, 60
    b.append(tick_y(ox2, ya, "302") + tick_y(ox2, yb, "300"))
    b.append(t(ox2 - 7, oy + 4, "0", 11.5, anchor="end"))
    u1, u2 = ox2 + (t1 - ox), ox2 + (t2 - ox)
    b.append(path(f"M{ox2},{oy} C{ox2 + 22},80 {u1 - 22},{ya} {u1},{ya} L{u2},{yb} L390,{yb}", sw=1.6))
    b.append(line(ox2, ya, u1, ya, sw=0.5, dash="2,3", color="#999") + line(ox2, yb, u2, yb, sw=0.5, dash="2,3", color="#999"))
    b.append(line(u1, ya, u1, oy, sw=0.6, dash="3,3") + line(u2, yb, u2, oy, sw=0.6, dash="3,3"))
    b.append(ti(u1, oy + 15, "t_{1}", 12) + ti(u2, oy + 15, "t_{2}", 12))
    b.append(t(322, 188, "(나)", 12))
    b.append(t(196, oy + 15, "시간", 10.5, anchor="end") + t(398, oy + 15, "시간", 10.5, anchor="end"))
    return svg(400, 194, "".join(b))

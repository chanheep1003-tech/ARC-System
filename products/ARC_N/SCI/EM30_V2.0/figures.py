"""SVG figures for ARC N° 통합과학2 전자기 유도와 발전 30제 N°2.

Primitives live in figparts.py (shared conventions with EM30 V1.0):
coil_h front strands "/" -> current entering the LEFT lead makes the field
inside point LEFT; coil_h(reverse=True) is the opposite winding.
"""
import math

from figparts import *  # noqa: F401,F403


def _sine_graph(ox, oy, W, A, f, ticks=(), ylab="", xlab="시간", yticks=(), sw=1.6, top=12, bottom=None):
    b = [line(ox, oy, ox + W + 6, oy), line(ox, top, ox, bottom or oy + A + 14)]
    b.append(t(ox + W + 8, oy + 4, xlab, 10.5, anchor="start"))
    if ylab:
        b.append(t(ox + 4, top - 2, ylab, 10.5, anchor="start"))
    for v, lab in yticks:
        b.append(tick_y(ox, oy - v * A, lab, 10.5))
    b.append(poly(curve(lambda x: oy - A * f((x - ox) / W), ox, ox + W, 200), sw=sw))
    for u, lab, above in ticks:
        x = ox + u * W
        b.append(line(x, oy - 3, x, oy + 3))
        b.append(ti(x, oy - 6 if above else oy + 15, lab, 10.5))
    return "".join(b)


# ------------------------------------------------------------------ 02
def fig02():
    b = []
    for i, (th, lab) in enumerate([(90, "(가)"), (45, "(나)"), (0, "(다)")]):
        cx = 66 + i * 134
        b.append(gen_top(cx, 52, th, W=124, H=76, pole_w=14))
        b.append(t(cx, 108, lab, 12))
    return svg(400, 114, "".join(b))


# ------------------------------------------------------------------ 03
def fig03():
    b = []
    cx = 150
    b.append(magnet_v(cx - 9, 10, 18, 44, top="S", bottom="N", size=10))
    b.append(line(cx, 54, cx, 196, sw=0.6, dash="2,3", color=MID))
    b.append(line(206, 10, 206, 102, sw=0.8, both=True) + ti(214, 60, "h", 12, anchor="start"))
    b.append(dot(cx, 80, 2.6) + ti(cx - 10, 84, "p", 12, anchor="end"))
    b.append(coil_v(cx, 104, turns=6, w=60, pitch=9))
    (lx, ly), (rx, ry) = coil_v_leads(cx, 104, 6, 60, 9)
    b.append(poly([(lx, ly), (lx - 24, ly), (lx - 24, 180), (cx + 60, 180)]))
    b.append(poly([(rx, ry), (rx + 40, ry), (rx + 40, 170)]))
    b.append(galv(rx + 40, 180, 11))
    b.append(dot(cx, 174, 2.6) + ti(cx - 10, 178, "q", 12, anchor="end"))
    b.append(t(cx - 50, 130, "코일", 10.5, anchor="end"))
    return svg(400, 200, "".join(b), "72%")


# ------------------------------------------------------------------ 05
def fig05():
    ox, oy, W, A = 50, 58, 300, 40
    f = lambda u: math.sin(2 * math.pi * u)
    b = [_sine_graph(ox, oy, W, A, f, ticks=[(0.5, "T/2", True), (1, "T", True)], ylab="전류",
                     yticks=[(1, "I_{0}"), (-1, "-I_{0}")], top=12)]
    b.append(t(ox - 7, oy + 4, "0", 10.5, anchor="end"))
    return svg(400, 116, "".join(b), "80%")


# ------------------------------------------------------------------ 06
def fig06():
    b = []
    b.append(line(60, 8, 60, 20, sw=0.8) + line(30, 8, 90, 8, sw=2))
    b.append(magnet_v(51, 20, 18, 40, top="S", bottom="N", size=10))
    b.append(t(80, 30, "실", 10, anchor="start", fill="#555"))
    b.append(rect(46, 70, 28, 118, fill="none", sw=0.9, color="#888"))
    b.append(t(40, 100, "유리관", 10, anchor="end", fill="#555"))
    b.append(coil_v(60, 146, turns=5, w=52, pitch=8))
    (lx, ly), (rx, ry) = coil_v_leads(60, 146, 5, 52, 8)
    b.append(poly([(rx, ry), (130, ry), (130, 160)]))
    b.append(poly([(lx, ly), (20, ly), (20, 196), (130, 196), (130, 184)]))
    b.append(rect(112, 160, 36, 24, rx=3) + t(130, 176, "센서", 9.5))
    b.append(line(100, 60, 100, 146, sw=0.8, both=True) + ti(106, 106, "h", 12, anchor="start"))
    return svg(200, 204, "".join(b), "44%")


# ------------------------------------------------------------------ 07
def fig07():
    b = [rect(250, 96, 60, 10, fill="#e9e9e9", sw=1), line(280, 96, 280, 70, sw=3, color="#777")]
    b.append(f'<ellipse cx="280" cy="48" rx="9" ry="26" fill="none" stroke="#555" stroke-width="3.2"/>')
    b.append(t(300, 50, "알루미늄 고리", 10.5, anchor="start"))
    b.append(t(280, 120, "절연체 받침대", 10.5))
    b.append(magnet_h(70, 39, 100, 18))
    b.append(arrow_v(104, 28, 150, 28))
    b.append(line(40, 48, 380, 48, sw=0.5, dash="2,3", color=MID))
    return svg(400, 126, "".join(b), "86%")


# ------------------------------------------------------------------ 08
def fig08():
    b = []
    b.append(path("M8,20 L96,96 L392,96", sw=1.6))
    b.append(rect(384, 40, 8, 56, fill="url(#hatch)", sw=1) + t(380, 34, "벽", 10.5, anchor="end"))
    b.append(f'<g transform="rotate(40.8 36 44)">' + magnet_h(14, 36, 44, 14, size=9) + "</g>")
    cx = 250
    b.append(f'<ellipse cx="{cx}" cy="80" rx="9" ry="26" fill="none" stroke="{INK}" stroke-width="3"/>')
    b.append(poly([(cx, 54), (cx, 30), (cx + 34, 30)]))
    b.append(poly([(cx, 106), (cx, 114), (cx + 60, 114), (cx + 60, 30), (cx + 50, 30)]))
    b.append(galv(cx + 42, 30, 8))
    b.append(t(cx - 16, 40, "코일", 10.5, anchor="end"))
    for x, lab in [(cx - 70, "a"), (cx + 70, "b")]:
        b.append(dot(x, 96, 2.6) + ti(x, 112, lab, 12))
    b.append(line(cx - 70, 124, cx, 124, sw=0.6, both=True) + line(cx, 124, cx + 70, 124, sw=0.6, both=True))
    b.append(ti(cx - 35, 134, "L", 11) + ti(cx + 35, 134, "L", 11))
    return svg(400, 140, "".join(b), "94%")


# ------------------------------------------------------------------ 09
def fig09():
    b = [gen_top(74, 56, 120, W=136, H=80, pole_w=14)]
    a0, a1 = math.radians(90), math.radians(120)
    b.append(line(74, 56, 74, 22, sw=0.7, dash="2,2", color=MID))
    b.append(path(f"M{74 + 22 * math.cos(a0):.1f},{56 - 22 * math.sin(a0):.1f} A22,22 0 0 0 "
                  f"{74 + 22 * math.cos(a1):.1f},{56 - 22 * math.sin(a1):.1f}", sw=0.9))
    b.append(ti(74 + 30 * math.cos(math.radians(106)), 56 - 30 * math.sin(math.radians(106)), "θ", 12))
    b.append(t(74, 112, "(가)", 11.5))
    ox, oy, W, A = 170, 58, 200, 40
    b.append(line(ox, oy, ox + W + 6, oy) + line(ox, 10, ox, 104))
    b.append(ti(ox + W + 10, oy + 4, "θ", 11.5, anchor="start"))
    b.append(t(ox + 4, 8, "전류", 10.5, anchor="start"))
    for v, lab in [(1, "I_{0}"), (0.5, "I_{0}/2"), (-0.5, "-I_{0}/2"), (-1, "-I_{0}")]:
        b.append(tick_y(ox, oy - v * A, lab, 9.5))
        if abs(v) == 0.5:
            b.append(line(ox, oy - v * A, ox + W, oy - v * A, sw=0.5, dash="2,3", color=MID))
    b.append(poly(curve(lambda x: oy - A * math.sin(2 * math.pi * (x - ox) / W), ox, ox + W, 200), sw=1.6))
    for k in range(1, 13):
        x = ox + W * k / 12
        b.append(line(x, oy - 2, x, oy + 2, sw=0.8))
    for k, lab in [(3, "90°"), (6, "180°"), (9, "270°"), (12, "360°")]:
        x = ox + W * k / 12
        b.append(t(x - (6 if k == 12 else 0), oy + (-6 if k == 9 else 14), lab, 9.5))
    b.append(t(ox + 100, 118, "(나)", 11.5))
    return svg(400, 124, "".join(b))


# ------------------------------------------------------------------ 10
def fig10():
    b = [line(10, 76, 390, 76, sw=1.6), line(10, 81, 390, 81, sw=0.8)]
    b.append(magnet_h(40, 48, 80, 22) + t(80, 42, "고정", 10.5))
    b.append(rect(222, 60, 96, 12, rx=2, fill="#f2f2f2", sw=1))
    b.append(circle(236, 74, 4.5) + circle(304, 74, 4.5))
    b.append(coil_h(236, 22, turns=7, pitch=10, h=34))
    (lx, ly), (rx, ry) = coil_leads(236, 22, 7, 10, 34)
    b.append(poly([(lx, ly), (lx - 8, ly), (lx - 8, 12), (272, 12)]))
    b.append(poly([(rx, ly), (rx + 8, ly), (rx + 8, 12), (292, 12)]))
    b.append(galv(282, 12, 8))
    b.append(arrow_v(250, 98, 206, 98, "v", ly=10))
    b.append(t(330, 100, "코일과 검류계가 함께 이동", 10, fill="#444"))
    return svg(400, 114, "".join(b), "90%")


# ------------------------------------------------------------------ 11
def fig11():
    b = []
    for x0, lab, turns, rev in [(8, "A", 5, False), (208, "B", 10, True)]:
        b.append(magnet_h(x0, 40, 54, 16, size=10))
        b.append(arrow_v(x0 + 10, 32, x0 + 42, 32, "v", ly=-3, size=11))
        cx = x0 + 70
        pitch = 11 if turns == 5 else 6.4
        b.append(coil_h(cx, 30, turns=turns, pitch=pitch, h=36, reverse=rev))
        (lx, ly), (rx, ry) = coil_leads(cx, 30, turns, pitch, 36)
        b.append(poly([(lx, ly), (lx, 88), (cx + 12, 88)]))
        b.append(poly([(rx, ry), (rx, 88), (cx + 52, 88)]))
        b.append(resistor_h(cx + 12, cx + 52, 88))
        b.append(t(cx + 12, 104, "p", 11, extra='font-style="italic"') + t(cx + 52, 104, "q", 11, extra='font-style="italic"'))
        b.append(t(cx + turns * pitch / 2, 20, lab, 13, weight=700))
    return svg(400, 112, "".join(b))


# ------------------------------------------------------------------ 12
def _flux_graph():
    ox, oy, W, A = 40, 52, 300, 36
    b = [_sine_graph(ox, oy, W, A, lambda u: math.cos(2 * math.pi * u),
                     ticks=[(0.25, "T/4", False), (0.5, "T/2", True), (0.75, "3T/4", False), (1, "T", True)],
                     ylab="코일면을 통과하는 자기력선의 수", xlab="시간", top=10)]
    b.append(t(ox - 6, oy + 4, "0", 10.5, anchor="end"))
    return svg(400, 104, "".join(b), "86%")


def _small_graph(f, label_t=True):
    ox, oy, W, A = 12, 38, 118, 26
    b = [line(ox, oy, ox + W + 4, oy), line(ox, 6, ox, 70)]
    b.append(poly(curve(lambda x: oy - A * f((x - ox) / W), ox, ox + W, 160), sw=1.4))
    for u, lab in [(0.5, "T/2"), (1, "T")]:
        x = ox + u * W
        b.append(line(x, oy - 2, x, oy + 2, sw=0.8) + ti(x, oy + 13, lab, 9))
    b.append(ti(ox + 3, 8, "I", 9.5, anchor="start"))
    return svg(140, 74, "".join(b), "100%")


def fig12_choices():
    fs = [lambda u: math.sin(2 * math.pi * u), lambda u: math.cos(2 * math.pi * u),
          lambda u: -math.sin(2 * math.pi * u), lambda u: abs(math.sin(2 * math.pi * u)),
          lambda u: math.sin(4 * math.pi * u)]
    return [_small_graph(f) for f in fs]


# ------------------------------------------------------------------ 14
def fig14():
    ox, oy, W = 30, 64, 340
    b = [line(ox, oy, ox + W + 6, oy), line(ox + W / 2, 12, ox + W / 2, 116)]
    b.append(t(ox + W + 8, oy + 4, "x", 11.5, anchor="start", extra='font-style="italic"'))
    b.append(t(ox + W / 2 + 4, 10, "유도 전류", 10.5, anchor="start"))

    def f(x):
        u = (x - ox - W / 2) / 60
        return oy - 40 * (-u * math.exp(-u * u / 1.2)) * 1.6
    b.append(poly(curve(f, ox, ox + W, 240), sw=1.6))
    for k, lab in [(-2, "-2d"), (-1, "-d"), (1, "d"), (2, "2d")]:
        x = ox + W / 2 + k * 60
        b.append(line(x, oy - 3, x, oy + 3) + ti(x, oy + (15 if k < 0 else -7), lab, 10.5))
    b.append(t(ox + W / 2 - 6, oy + 15, "0", 10.5, anchor="end"))
    return svg(400, 122, "".join(b), "86%")


# ------------------------------------------------------------------ 16
def fig16():
    b = []
    cx, cy, n, p, hh = 180, 44, 9, 11, 40
    # induced field lines: through the coil to the LEFT, looping back outside
    for dy, w in [(8, 1.0), (32, 1.0)]:
        b.append(line(cx + n * p + 16, cy + dy, cx - 20, cy + dy, sw=w, color=MID))
        b.append(f'<path d="M{cx - 10},{cy + dy - 3.5} L{cx - 18},{cy + dy} L{cx - 10},{cy + dy + 3.5}" fill="none" stroke="{MID}" stroke-width="1.2"/>')
    b.append(path(f"M{cx - 20},{cy + 8} C{cx - 60},{cy - 30} {cx + n * p + 56},{cy - 30} {cx + n * p + 16},{cy + 8}", sw=1.0, color=MID, dash="4,3"))
    b.append(path(f"M{cx - 20},{cy + 32} C{cx - 60},{cy + 70} {cx + n * p + 56},{cy + 70} {cx + n * p + 16},{cy + 32}", sw=1.0, color=MID, dash="4,3"))
    b.append(coil_h(cx, cy, turns=n, pitch=p, h=hh))
    (lx, ly), (rx, ry) = coil_leads(cx, cy, n, p, hh)
    b.append(poly([(lx, ly), (lx, 122), (cx + 36, 122)]))
    b.append(poly([(rx, ry), (rx, 122), (cx + 64, 122)]))
    b.append(galv(cx + 50, 122, 11))
    b.append(t(cx + 30, 116, "A", 11, weight=600) + t(cx + 70, 116, "B", 11, weight=600))
    b.append(rect(34, 55, 34, 18, fill="#fff", sw=1.1) + rect(68, 55, 34, 18, fill="#bdbdbd", sw=1.1))
    b.append(t(85, 68, "P", 11.5, weight=700))
    b.append(arrow_v(52, 46, 94, 46))
    b.append(t(cx + n * p / 2, 20, "유도 전류에 의한 자기장", 10, fill="#555"))
    return svg(400, 136, "".join(b), "90%")


# ------------------------------------------------------------------ 18
def fig18():
    b = []
    cx = 150
    b.append(f'<ellipse cx="{cx}" cy="96" rx="52" ry="11" fill="none" stroke="{INK}" stroke-width="2.6"/>')
    b.append(t(cx + 60, 100, "원형 고리 (고정)", 10.5, anchor="start"))
    b.append(line(cx, 16, cx, 186, sw=0.6, dash="2,3", color=MID))
    b.append(magnet_v(cx - 8, 150, 16, 36, top="N", bottom="S", size=9.5))
    b.append(line(cx + 22, 180, cx + 22, 150, sw=1.2, arrow=True) + t(cx + 30, 168, "위로 던짐", 10, anchor="start"))
    for y, lab in [(132, "p"), (60, "q")]:
        b.append(dot(cx, y, 2.6) + ti(cx - 10, y + 4, lab, 12, anchor="end"))
    b.append(line(cx - 70, 60, cx - 70, 96, sw=0.6, both=True) + line(cx - 70, 96, cx - 70, 132, sw=0.6, both=True))
    b.append(ti(cx - 78, 82, "d", 11, anchor="end") + ti(cx - 78, 118, "d", 11, anchor="end"))
    return svg(400, 192, "".join(b), "76%")


# ------------------------------------------------------------------ 19
def fig19():
    b = []
    b.append(path("M14,34 L60,22 L60,112 L14,124 Z", sw=1.2, fill="#5a5a5a"))
    b.append(t(37, 78, "N", 14, weight=700, fill="#fff"))
    b.append(path("M214,22 L260,34 L260,124 L214,112 Z", sw=1.2, fill="#fff"))
    b.append(t(237, 78, "S", 14, weight=700))
    for dy in (44, 70, 96):
        b.append(line(64, dy, 208, dy, sw=0.6, dash="3,3", color=MID))
    # coil (tilted rectangle) between the poles
    b.append(path("M112,34 L166,44 L166,104 L112,94 Z", sw=2.6, color="#333"))
    b.append(t(139, 24, "코일", 10.5))
    # axle toward the viewer (lower right), slip rings and brushes
    b.append(line(139, 69, 300, 146, sw=1.6))
    for k, (x, y) in enumerate([(262, 128), (282, 138)]):
        b.append(f'<ellipse cx="{x}" cy="{y}" rx="4.5" ry="11" transform="rotate(-25 {x} {y})" fill="#fff" stroke="{INK}" stroke-width="1.3"/>')
        b.append(rect(x - 5, y + 10, 10, 10, fill="#999", sw=0.8))
    b.append(path("M166,74 C200,96 236,112 262,120", sw=0.9) + path("M150,100 C190,120 250,140 282,130", sw=0.9))
    b.append(poly([(257, 148), (257, 158), (330, 158)]) + poly([(277, 158), (277, 152), (372, 152), (372, 170), (360, 170)]))
    b.append(circle(350, 170, 10) + line(343, 163, 357, 177, sw=1) + line(357, 163, 343, 177, sw=1))
    b.append(t(350, 194, "전구", 10.5) + t(236, 176, "브러시", 10))
    b.append(t(314, 140, "회전축", 10, anchor="start"))
    b.append(path("M300,112 A12,12 0 1 1 318,128", sw=0.9, arrow=True, color=MID))
    return svg(400, 200, "".join(b), "90%")


# ------------------------------------------------------------------ 21
def fig21_setup():
    b = []
    cx = 60
    b.append(magnet_v(cx - 8, 8, 16, 34, top="S", bottom="N", size=9.5))
    b.append(line(cx, 42, cx, 150, sw=0.6, dash="2,3", color=MID))
    b.append(coil_v(cx, 88, turns=5, w=52, pitch=8))
    (lx, ly), (rx, ry) = coil_v_leads(cx, 88, 5, 52, 8)
    b.append(poly([(rx, ry), (120, ry), (120, 110)]) + poly([(lx, ly), (14, ly), (14, 140), (120, 140), (120, 132)]))
    b.append(galv(120, 121, 10))
    return svg(160, 154, "".join(b), "36%")


def _fall_graph(a1, w1, a2, w2, sign2=-1, gap=0.18):
    ox, oy, W = 12, 40, 124
    b = [line(ox, oy, ox + W + 4, oy), line(ox, 6, ox, 74)]
    b.append(ti(ox + W + 2, oy + 12, "t", 9.5) + ti(ox + 3, 8, "I", 9.5, anchor="start"))
    s1 = 0.10
    e1 = s1 + w1
    s2 = e1 + gap
    e2 = s2 + w2

    def f(x):
        u = (x - ox) / W
        if s1 <= u <= e1:
            return oy - 26 * a1 * math.sin(math.pi * (u - s1) / w1)
        if s2 <= u <= e2:
            return oy - sign2 * 26 * a2 * math.sin(math.pi * (u - s2) / w2)
        return oy
    b.append(poly(curve(f, ox, ox + W, 240), sw=1.4))
    return svg(140, 78, "".join(b), "100%")


def fig21_choices():
    return [_fall_graph(0.8, 0.28, 0.8, 0.28), _fall_graph(0.7, 0.30, 1.0, 0.20),
            _fall_graph(1.0, 0.20, 0.7, 0.30), _fall_graph(0.7, 0.30, 1.0, 0.20, sign2=1),
            _fall_graph(1.0, 0.30, 0.7, 0.20)]


# ------------------------------------------------------------------ 22
def fig22():
    b = [gen_top(100, 52, 0, W=160, H=80), gen_top2(300, 52, 0, cw=True, W=160, H=80)]
    b.append(t(100, 108, "A (시계 반대 방향 회전)", 10.5) + t(300, 108, "B (시계 방향 회전)", 10.5))
    return svg(400, 114, "".join(b))


# ------------------------------------------------------------------ 23
def fig23():
    b = []
    for i, (lab, n) in enumerate([("A", 1), ("B", 2), ("C", 3)]):
        x = 40 + i * 70
        for k in range(n):
            b.append(magnet_v(x + k * 14 - (n - 1) * 7 - 7, 20, 14, 40, top="S", bottom="N", size=8.5))
        b.append(t(x, 76, lab, 12, weight=700))
    b.append(t(110, 96, "같은 자석을 1개, 2개, 3개씩 묶음", 10, fill="#444"))
    cx = 320
    b.append(line(cx, 12, cx, 110, sw=0.6, dash="2,3", color=MID))
    b.append(rect(cx - 7, 12, 14, 20, fill="#ddd", sw=0.8) + t(cx + 12, 26, "?", 11, anchor="start", fill="#555"))
    b.append(line(cx + 40, 22, cx + 40, 66, sw=0.8, both=True) + ti(cx + 46, 48, "h", 11.5, anchor="start"))
    b.append(coil_v(cx, 70, turns=4, w=48, pitch=7))
    (lx, ly), (rx, ry) = coil_v_leads(cx, 70, 4, 48, 7)
    b.append(poly([(rx, ry), (cx + 44, ry), (cx + 44, 94)]) + rect(cx + 32, 94, 24, 16, rx=2) + t(cx + 44, 106, "센서", 8.5))
    b.append(poly([(lx, ly), (cx - 38, ly), (cx - 38, 118), (cx + 44, 118), (cx + 44, 110)]))
    return svg(400, 124, "".join(b), "92%")


# ------------------------------------------------------------------ 24
def fig24():
    b = [path("M10,20 C40,20 60,104 110,110 L290,110 C340,104 360,30 392,24", sw=1.6)]
    b.append(f'<g transform="rotate(38 30 28)">' + magnet_h(14, 16, 40, 13, size=8.5) + "</g>")
    b.append(dot(24, 26, 2.6) + ti(12, 18, "p", 12))
    b.append(line(6, 26, 6, 110, sw=0.6, dash="2,3", color=MID) + ti(0, 70, "h", 11.5, anchor="start"))
    cx = 200
    b.append(f'<ellipse cx="{cx}" cy="96" rx="8" ry="22" fill="none" stroke="{INK}" stroke-width="2.8"/>')
    b.append(t(cx, 64, "원형 도선 A", 10.5))
    b.append(dot(372, 36, 2.6) + ti(380, 32, "q", 12, anchor="start"))
    b.append(line(10, 116, 390, 116, sw=0.5, color="#aaa"))
    return svg(400, 124, "".join(b), "94%")


# ------------------------------------------------------------------ 25
def fig25():
    ox, oy, W, A = 40, 58, 320, 22
    b = [line(ox, oy, ox + W + 6, oy), line(ox, 8, ox, 108)]
    b.append(t(ox + W + 8, oy + 4, "시간", 10.5, anchor="start") + t(ox + 4, 8, "전류", 10.5, anchor="start"))
    b.append(tick_y(ox, oy - A, "I_{0}", 10) + tick_y(ox, oy - 2 * A, "2I_{0}", 10))
    b.append(tick_y(ox, oy + A, "-I_{0}", 10) + tick_y(ox, oy + 2 * A, "-2I_{0}", 10))
    b.append(poly(curve(lambda x: oy - A * math.cos(2 * math.pi * (x - ox) / (W / 2)), ox, ox + W, 240), sw=1.3, color="#555"))
    b.append(f'<g stroke-dasharray="5,3">' + poly(curve(lambda x: oy - 2 * A * math.cos(2 * math.pi * (x - ox) / (W / 2)), ox, ox + W, 240), sw=1.5) + "</g>")
    for u, lab in [(0.5, "T"), (1, "2T")]:
        x = ox + u * W
        b.append(line(x, oy - 3, x, oy + 3) + ti(x, oy + 15, lab, 10.5))
    b.append(line(250, 118, 280, 118, sw=1.3, color="#555") + t(284, 122, "A", 11, anchor="start", weight=600))
    b.append(f'<line x1="316" y1="118" x2="346" y2="118" stroke="{INK}" stroke-width="1.5" stroke-dasharray="5,3"/>'
             + t(350, 122, "B", 11, anchor="start", weight=600))
    return svg(400, 128, "".join(b), "88%")


# ------------------------------------------------------------------ 26
def fig26():
    b = []
    b.append(coil_h(60, 30, turns=7, pitch=10, h=34) + t(95, 22, "A", 13, weight=700))
    (lx, ly), (rx, ry) = coil_leads(60, 30, 7, 10, 34)
    b.append(poly([(lx, ly), (lx, 104), (72, 104)]))
    b.append(line(72, 96, 72, 112, sw=1.6) + line(78, 99, 78, 109, sw=3))
    b.append(t(75, 124, "전지", 10))
    b.append(line(78, 104, 90, 104))
    b.append(switch_h(90, 110, 104, closed=False) + t(100, 124, "스위치", 10))
    b.append(resistor_h(110, 150, 104))
    b.append(line(142, 96, 122, 114, sw=0.9, arrow=True))
    b.append(t(136, 90, "가변 저항", 10))
    b.append(poly([(150, 104), (rx, 104), (rx, ry)]))
    b.append(coil_h(220, 30, turns=7, pitch=10, h=34) + t(255, 22, "B", 13, weight=700))
    (lx2, ly2), (rx2, ry2) = coil_leads(220, 30, 7, 10, 34)
    b.append(poly([(lx2, ly2), (lx2, 104), (244, 104)]) + poly([(rx2, ry2), (rx2, 104), (266, 104)]))
    b.append(galv(255, 104, 11))
    b.append(line(40, 47, 320, 47, sw=0.5, dash="2,3", color=MID))
    return svg(340, 132, "".join(b), "84%")


# ------------------------------------------------------------------ 27
def fig27():
    b = [meter(100, 40, 88, 54, needle=0.62), t(100, 94, "기준 실험의 결과", 10.5),
         meter(300, 40, 88, 54, needle=-0.3), t(300, 94, "(다)의 결과", 10.5)]
    return svg(400, 100, "".join(b), "80%")


# ------------------------------------------------------------------ 28
def fig28():
    b = [rect(132, 8, 36, 196, fill="none", sw=0.9, color="#888")]
    b.append(magnet_v(142, 14, 16, 34, top="S", bottom="N", size=9.5))
    for y, lab, g in [(70, "A", "G_{1}"), (150, "B", "G_{2}")]:
        b.append(coil_v(150, y, turns=5, w=54, pitch=7))
        (lx, ly), (rx, ry) = coil_v_leads(150, y, 5, 54, 7)
        b.append(poly([(rx, ry), (220, ry), (220, y + 4)]) + galv(220, y + 16, 10, label=""))
        b.append(t(220, y + 20, g, 9.5, weight=600))
        b.append(poly([(lx, ly), (110, ly), (110, y + 40), (220, y + 40), (220, y + 26)]))
        b.append(t(100, y + 18, lab, 13, weight=700, anchor="end"))
    b.append(t(250, 110, "(A와 B는 감은 수와", 10, anchor="start", fill="#444"))
    b.append(t(250, 124, " 감은 방향이 같다.)", 10, anchor="start", fill="#444"))
    return svg(400, 212, "".join(b), "72%")


# ------------------------------------------------------------------ 29
def fig29():
    ox, oy, W, A = 30, 46, 330, 32
    b = [line(ox, oy, ox + W + 6, oy), line(ox, 8, ox, 86)]
    b.append(t(ox + W + 8, oy + 4, "시간", 10, anchor="start") + t(ox + 4, 8, "전류", 10, anchor="start"))
    b.append(poly(curve(lambda x: oy - A * math.sin(2 * math.pi * (x - ox) / W), ox, ox + W, 240), sw=1.5))
    for u, lab in [(1 / 8, "P"), (2 / 8, "Q"), (3 / 8, "R"), (4 / 8, "S")]:
        x = ox + u * W
        y = oy - A * math.sin(2 * math.pi * u)
        b.append(dot(x, y, 2.8) + t(x + (0 if u < 0.5 else 8), y - 7 if u < 0.5 else y + 14, lab, 11, weight=700))
        b.append(line(x, oy, x, y, sw=0.5, dash="2,2", color=MID))
    b.append(t(ox + W, oy + 14, "T", 10.5, extra='font-style="italic"'))
    top = svg(400, 92, "".join(b), "86%")
    views = []
    for th, lab in [(180, "(가)"), (225, "(나)"), (135, "(다)"), (270, "(라)")]:
        views.append(gen_top(50, 44, th, W=88, H=64, pole_w=11, rot=True, coil_len=19))
        views[-1] = f'<g transform="translate({len(views) * 100 - 100 + 0},0)">{views[-1]}' + t(50, 94, lab, 11) + "</g>"
    bottom = svg(400, 100, "".join(views))
    return top + bottom


# ------------------------------------------------------------------ 30
def fig30():
    ox, oy = 40, 90
    b = [line(ox, oy, 370, oy), line(ox, 12, ox, oy)]
    b.append(t(372, oy + 4, "시간(s)", 10, anchor="start"))
    b.append(t(ox + 4, 10, "코일을 지나는 자기장의 세기", 10, anchor="start"))
    sx = 60
    pts = [(ox, oy), (ox + 2 * sx, 34), (ox + 4 * sx, 34), (ox + 5 * sx, oy)]
    b.append(poly(pts, sw=1.6))
    for k in range(1, 6):
        b.append(tick_x(ox + k * sx, oy, str(k), size=10))
    b.append(tick_y(ox, 34, "B_{0}", 10))
    b.append(line(ox, 34, ox + 2 * sx, 34, sw=0.5, dash="2,3", color=MID))
    b.append(t(ox - 6, oy + 4, "0", 10, anchor="end"))
    return svg(400, 104, "".join(b), "86%")


def _step_graph(segs):
    """segs: list of (t0, t1, value) with value in current units."""
    ox, oy, sx, sy = 12, 42, 23, 11
    b = [line(ox, oy, ox + 5 * sx + 8, oy), line(ox, 6, ox, 72)]
    b.append(ti(ox + 3, 8, "I", 9.5, anchor="start") + t(ox + 5 * sx + 8, oy + 12, "t", 9.5, extra='font-style="italic"'))
    pts = [(ox, oy)]
    for t0, t1, v in segs:
        pts += [(ox + t0 * sx, oy - v * sy), (ox + t1 * sx, oy - v * sy)]
    pts.append((ox + 5 * sx, oy))
    b.append(poly(pts, sw=1.4))
    for k in (2, 4, 5):
        b.append(line(ox + k * sx, oy - 2, ox + k * sx, oy + 2, sw=0.8) + t(ox + k * sx, oy + 2 * sy + 12, str(k), 8.5))
    for v in (1, 2):
        b.append(line(ox - 2, oy - v * sy, ox, oy - v * sy, sw=0.6) + line(ox - 2, oy + v * sy, ox, oy + v * sy, sw=0.6))
    b.append(t(ox - 3, oy - sy + 3, "I_{0}", 7.5, anchor="end") if False else "")
    return svg(140, 80, "".join(b), "100%")


def fig30_choices():
    return [_step_graph([(0, 2, 1), (2, 4, 0), (4, 5, -1)]),
            _step_graph([(0, 2, 1), (2, 4, 0), (4, 5, -2)]),
            _step_graph([(0, 2, 1), (2, 4, 1), (4, 5, -2)]),
            _step_graph([(0, 2, -1), (2, 4, 0), (4, 5, 2)]),
            _step_graph([(0, 2, 0.5), (2, 4, 2), (4, 5, 1)])]

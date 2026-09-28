"""SVG figures for ARC N° 통합과학2 전자기 유도 · 방향 고난도 20제.

Conventions (checked by verify.py):
  * coil_h: front strands "/" -> current entering the LEFT lead makes the
    field inside the coil point LEFT (coil_h(reverse=True) is the opposite).
  * battery: long thin plate = (+), short thick plate = (−).
  * horizontal ring drawn as an ellipse: the lower half is the near side.
    An arrow on the near side pointing RIGHT = counter-clockwise seen from
    above = induced field pointing UP.
Figures 07, 12, 16, 19 are reprinted from EM30 V2.0 (items 16, 18, 24, 28).
"""
import math

from figparts import *  # noqa: F401,F403


def battery(x, y, plus_left=True):
    """Battery on a horizontal wire at y, plates at x and x+6."""
    xl, xs = (x, x + 6) if plus_left else (x + 6, x)
    out = [line(xl, y - 9, xl, y + 9, sw=1.4), line(xs, y - 5, xs, y + 5, sw=3.2)]
    out.append(t(xl + (-5 if plus_left else 5), y - 11, "+", 10, anchor="end" if plus_left else "start"))
    return "".join(out)


def ring_h(cx, cy, rx=40, ry=9, sw=2.6):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{INK}" stroke-width="{sw}"/>'


def ring_arrow(cx, cy, ry, right=True):
    s = 1 if right else -1
    return line(cx - 11 * s, cy + ry + 0.4, cx + 11 * s, cy + ry + 0.4, sw=1.6, arrow=True)


def res_circuit(x1, x2, y_lead, y, lab1, lab2):
    """Resistor hanging below two coil leads, with end labels."""
    xm1, xm2 = x1 + (x2 - x1) * 0.28, x2 - (x2 - x1) * 0.28
    out = [poly([(x1, y_lead), (x1, y), (xm1, y)]), poly([(x2, y_lead), (x2, y), (xm2, y)]),
           resistor_h(xm1, xm2, y)]
    out.append(ti(xm1, y + 16, lab1, 11.5) + ti(xm2, y + 16, lab2, 11.5))
    return "".join(out)


# ------------------------------------------------------------------ 02
def fig02():
    b = [line(20, 47, 380, 47, sw=0.5, dash="2,3", color=MID)]
    x0, n, p, hh = 70, 8, 10, 34
    b.append(coil_h(x0, 30, turns=n, pitch=p, h=hh))
    (lx, ly), (rx, ry) = coil_leads(x0, 30, n, p, hh)
    b.append(res_circuit(lx, rx, ly, 100, "a", "b"))
    b.append(magnet_h(206, 38, 84, 18, left="S", right="N"))
    b.append(arrow_v(300, 47, 346, 47, "v", ly=-8))
    b.append(t(x0 + n * p / 2, 22, "코일", 10.5))
    return svg(400, 124, "".join(b), "86%")


# ------------------------------------------------------------------ 04
def fig04():
    b = [line(10, 47, 390, 47, sw=0.5, dash="2,3", color=MID)]
    b.append(magnet_h(20, 38, 84, 18, left="S", right="N"))
    x0, n, p, hh = 170, 8, 10, 34
    b.append(coil_h(x0, 30, turns=n, pitch=p, h=hh))
    (lx, ly), (rx, ry) = coil_leads(x0, 30, n, p, hh)
    cx = (lx + rx) / 2
    for y, fwd, lab in [(96, True, "P"), (128, False, "Q")]:
        b.append(line(lx, y, cx - 8, y) + line(cx + 8, y, rx, y))
        b.append(led_h(cx, y, forward=fwd))
        b.append(t(cx + 24, y + 4, lab, 12, weight=700, anchor="start"))
    b.append(line(lx, ly, lx, 128) + line(rx, ly, rx, 128))
    b.append(dot(lx, 96, 2.2) + dot(rx, 96, 2.2))
    return svg(400, 140, "".join(b), "86%")


# ------------------------------------------------------------------ 05
def fig05():
    b = []
    cx = 150
    b.append(rect(cx - 8, 14, 16, 150, fill="url(#hatch)", sw=1.1))
    b.append(t(cx + 14, 84, "철심", 10.5, anchor="start"))
    b.append(ring_h(cx, 42, rx=24, ry=6, sw=3))
    b.append(line(cx - 44, 42, cx - 26, 42, sw=0.7) + t(cx - 48, 46, "금속 고리", 10.5, anchor="end"))
    b.append(line(cx + 34, 44, cx + 34, 14, sw=1.1, dash="3,2", arrow=True))
    b.append(coil_v(cx, 104, turns=6, w=62, pitch=9))
    b.append(t(cx + 40, 128, "코일", 10.5, anchor="start"))
    (lx, ly), (rx, ry) = coil_v_leads(cx, 104, 6, 62, 9)
    b.append(poly([(lx, ly), (60, ly), (60, 184), (100, 184)]))
    b.append(battery(100, 184))
    b.append(line(106, 184, 150, 184) + switch_h(150, 176, 184, closed=False))
    b.append(poly([(176, 184), (236, 184), (236, ry), (rx, ry)]))
    b.append(t(103, 206, "전지", 10) + t(163, 206, "스위치", 10))
    return svg(300, 212, "".join(b), "70%")


# ------------------------------------------------------------------ 06
def fig06():
    b = [line(20, 60, 390, 60, sw=0.5, dash="2,3", color=MID)]
    b.append(magnet_h(40, 51, 90, 18, left="S", right="N"))
    b.append(circle(85, 60, 2.6, fill="#fff", sw=1))
    r = 56
    b.append(path(f"M{85 + r * math.cos(math.radians(30)):.1f},{60 - r * math.sin(math.radians(30)):.1f} "
                  f"A{r},{r} 0 0 0 {85 + r * math.cos(math.radians(70)):.1f},{60 - r * math.sin(math.radians(70)):.1f}",
                  sw=1.0, arrow=True, color=MID))
    b.append(t(85, 96, "회전축", 10.5))
    x0, n, p, hh = 200, 8, 10, 34
    b.append(coil_h(x0, 43, turns=n, pitch=p, h=hh))
    (lx, ly), (rx, ry) = coil_leads(x0, 43, n, p, hh)
    b.append(poly([(lx, ly), (lx, 104), (x0 + 28, 104)]) + poly([(rx, ry), (rx, 104), (x0 + 52, 104)]))
    b.append(galv(x0 + 40, 104, 11))
    b.append(t(x0 + n * p / 2, 36, "코일", 10.5))
    return svg(400, 122, "".join(b), "86%")


# ------------------------------------------------------------------ 07 (reprint)
def fig07():
    b = []
    cx, cy, n, p, hh = 180, 44, 9, 11, 40
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


# ------------------------------------------------------------------ 08
def fig08():
    b = []
    for x0, lab in [(30, "A"), (170, "B")]:
        b.append(coil_h(x0, 26, turns=7, pitch=10, h=34) + t(x0 + 35, 18, lab, 13, weight=700))
    (lx, ly), (rx, ry) = coil_leads(30, 26, 7, 10, 34)
    b.append(poly([(lx, ly), (lx, 92), (40, 92)]) + poly([(rx, ry), (rx, 92), (90, 92)]))
    b.append(rect(40, 82, 50, 20, rx=2) + t(65, 96, "전원 장치", 9.5))
    (lx, ly), (rx, ry) = coil_leads(170, 26, 7, 10, 34)
    b.append(poly([(lx, ly), (lx, 92), (194, 92)]) + poly([(rx, ry), (rx, 92), (216, 92)]))
    b.append(galv(205, 92, 11))
    b.append(line(14, 43, 256, 43, sw=0.5, dash="2,3", color=MID))
    b.append(t(135, 122, "(가)", 12))
    # (나) current graph
    ox, oy, sx = 282, 92, 20
    b.append(axes(ox, oy, ox + 112, 12))
    b.append(t(ox - 4, 8, "A의 전류", 10, anchor="start"))
    y2 = 40
    b.append(line(ox - 4, y2, ox, y2) + t(ox - 6, y2 + 4, "2<tspan font-style=\"italic\">I</tspan>_{0}", 10, anchor="end"))
    b.append(t(ox - 6, oy + 4, "0", 10, anchor="end"))
    for k in range(1, 6):
        b.append(line(ox + k * sx, oy, ox + k * sx, oy + 3) + t(ox + k * sx, oy + 14, str(k), 10))
    b.append(poly([(ox, oy), (ox + 2 * sx, y2), (ox + 4 * sx, y2), (ox + 5 * sx, oy), (ox + 5.5 * sx, oy)], sw=1.6))
    b.append(line(ox, y2, ox + 2 * sx, y2, sw=0.5, dash="2,3", color=MID))
    b.append(t(ox + 112, oy + 26, "시간(s)", 10, anchor="end"))
    b.append(t(ox + 56, 122, "(나)", 12))
    return svg(400, 128, "".join(b))


# ------------------------------------------------------------------ 09
def fig09():
    b = []
    cx = 150
    b.append(line(cx, 10, cx, 178, sw=0.6, dash="2,3", color=MID))
    b.append(magnet_v(cx - 9, 12, 18, 46, top="S", bottom="N", size=10))
    b.append(line(cx + 26, 20, cx + 26, 56, sw=1.2, arrow=True) + t(cx + 32, 42, "낙하", 10, anchor="start"))
    b.append(ring_h(cx, 110, rx=52, ry=11))
    b.append(t(cx + 60, 114, "원형 고리 (고정)", 10.5, anchor="start"))
    return svg(300, 150, "".join(b), "64%")


# ------------------------------------------------------------------ 10
def fig10():
    ox, oy, W = 40, 70, 330
    b = [line(ox, oy, ox + W, oy), line(ox, 10, ox, 126)]
    b.append(ti(ox + W + 4, oy + 4, "t", 11.5, anchor="start") + ti(ox + 6, 12, "I", 11.5, anchor="start"))
    b.append(t(ox - 6, oy + 4, "0", 10.5, anchor="end"))
    b.append(t(ox - 6, 26, "(+)", 10, anchor="end") + t(ox - 6, 118, "(−)", 10, anchor="end"))

    def f(x):
        u = (x - ox) / W
        if 0.08 <= u <= 0.40:
            return oy + 28 * math.sin(math.pi * (u - 0.08) / 0.32)
        if 0.52 <= u <= 0.70:
            return oy - 50 * math.sin(math.pi * (u - 0.52) / 0.18)
        return oy
    b.append(poly(curve(f, ox, ox + W, 300), sw=1.6))
    return svg(400, 132, "".join(b), "84%")


# ------------------------------------------------------------------ 11
def fig11():
    b = [line(8, 47, 392, 47, sw=0.5, dash="2,3", color=MID)]
    for x0, lab, l1, l2 in [(20, "P", "a", "b"), (300, "Q", "c", "d")]:
        b.append(coil_h(x0, 30, turns=8, pitch=10, h=34) + t(x0 + 40, 22, lab, 13, weight=700))
        (lx, ly), (rx, ry) = coil_leads(x0, 30, 8, 10, 34)
        b.append(res_circuit(lx, rx, ly, 98, l1, l2))
    b.append(magnet_h(150, 38, 84, 18, left="S", right="N"))
    b.append(arrow_v(170, 26, 216, 26, "v", ly=-3))
    return svg(400, 122, "".join(b))


# ------------------------------------------------------------------ 12 (reprint)
def fig12():
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


# ------------------------------------------------------------------ 13
def fig13():
    b = []
    px, py, L = 200, 10, 120
    b.append(rect(150, 4, 100, 6, fill="url(#hatch)", sw=0.9))
    for ang in (-32, 32):
        a = math.radians(ang)
        mx, my = px + L * math.sin(a), py + L * math.cos(a)
        b.append(line(px, py, mx, my - 18, sw=0.8, dash="3,3" if ang > 0 else None, color=MID if ang > 0 else INK))
        g = magnet_v(mx - 7, my - 18, 14, 30, top="S", bottom="N", size=8.5)
        b.append(g if ang < 0 else f'<g opacity="0.45">{g}</g>')
    b.append(path(f"M{px + (L + 16) * math.sin(math.radians(-32)):.1f},{py + (L + 16) * math.cos(math.radians(-32)):.1f} "
                  f"A{L + 16},{L + 16} 0 0 0 {px + (L + 16) * math.sin(math.radians(32)):.1f},{py + (L + 16) * math.cos(math.radians(32)):.1f}",
                  sw=0.8, dash="3,3", color=MID))
    b.append(coil_v(px, 164, turns=4, w=60, pitch=8))
    (lx, ly), (rx, ry) = coil_v_leads(px, 164, 4, 60, 8)
    b.append(poly([(rx, ry), (300, ry), (300, 176)]) + galv(300, 188, 11) + poly([(300, 200), (300, 206), (140, 206), (140, ly), (lx, ly)]))
    b.append(t(px - 34, 158, "코일", 10.5, anchor="end"))
    return svg(400, 212, "".join(b), "80%")


# ------------------------------------------------------------------ 14
def _panel(cx, pole_down, mag_above, v_down, arrow_right, tag):
    b = [ring_h(cx, 90, rx=38, ry=9, sw=2.4), ring_arrow(cx, 90, 9, arrow_right)]
    my = 18 if mag_above else 118
    top, bot = ("S", "N") if pole_down == "N" else ("N", "S")
    b.append(magnet_v(cx - 8, my, 16, 36, top=top, bottom=bot, size=9))
    y1, y2 = (my + 4, my + 32) if v_down else (my + 32, my + 4)
    b.append(line(cx + 22, y1, cx + 22, y2, sw=1.2, arrow=True))
    b.append(t(cx, 172, tag, 12))
    return "".join(b)


def fig14():
    b = [_panel(66, "N", True, True, False, "(가)"), _panel(200, "N", True, False, True, "(나)"),
         _panel(334, "S", False, True, True, "(다)")]
    return svg(400, 178, "".join(b), "96%")


# ------------------------------------------------------------------ 15
def fig15():
    b = []
    b.append(coil_h(60, 30, turns=7, pitch=10, h=34) + t(95, 22, "A", 13, weight=700))
    (lx, ly), (rx, ry) = coil_leads(60, 30, 7, 10, 34)
    b.append(poly([(lx, ly), (lx, 104), (84, 104)]))
    b.append(battery(84, 104, plus_left=True))
    b.append(line(90, 104, 104, 104) + switch_h(104, 126, 104, closed=False))
    b.append(poly([(126, 104), (rx, 104), (rx, ry)]))
    b.append(t(87, 126, "전지", 10) + t(115, 126, "스위치", 10))
    b.append(coil_h(210, 30, turns=7, pitch=10, h=34) + t(245, 22, "B", 13, weight=700))
    (lx2, ly2), (rx2, ry2) = coil_leads(210, 30, 7, 10, 34)
    b.append(res_circuit(lx2, rx2, ly2, 104, "c", "d"))
    b.append(line(40, 47, 300, 47, sw=0.5, dash="2,3", color=MID))
    return svg(320, 132, "".join(b), "80%")


# ------------------------------------------------------------------ 16 (reprint)
def fig16():
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


# ------------------------------------------------------------------ 17
def fig17():
    b = []
    cx = 150
    b.append(rect(cx - 26, 8, 52, 196, fill="#f1f1f1", sw=1.2))
    b.append(rect(cx - 20, 8, 40, 196, fill="#fff", sw=0.8))
    b.append(magnet_v(cx - 9, 86, 18, 44, top="S", bottom="N", size=10))
    b.append(line(cx + 44, 94, cx + 44, 124, sw=1.2, arrow=True) + t(cx + 50, 114, "낙하", 10, anchor="start"))
    for y, lab in [(66, "P"), (150, "Q")]:
        b.append(f'<ellipse cx="{cx}" cy="{y}" rx="26" ry="6" fill="none" stroke="{INK}" stroke-width="1.1" stroke-dasharray="4,3"/>')
        b.append(t(cx - 34, y + 4, lab, 12.5, weight=700, anchor="end"))
    b.append(t(cx + 34, 26, "구리관", 10.5, anchor="start"))
    return svg(300, 212, "".join(b), "62%")


# ------------------------------------------------------------------ 18
def fig18():
    b = []
    for y0, tag, right_left_pole in [(20, "(가)", "N"), (104, "(나)", "S")]:
        cy = y0 + 22
        b.append(line(8, cy, 392, cy, sw=0.5, dash="2,3", color=MID))
        b.append(magnet_h(16, cy - 9, 80, 18, left="S", right="N"))
        b.append(arrow_v(40, cy - 16, 80, cy - 16))
        b.append(coil_h(160, cy - 17, turns=8, pitch=10, h=34))
        (lx, ly), (rx, ry) = coil_leads(160, cy - 17, 8, 10, 34)
        b.append(poly([(lx, ly), (lx, cy + 30), (186, cy + 30)]) + poly([(rx, ry), (rx, cy + 30), (214, cy + 30)]))
        b.append(galv(200, cy + 30, 10))
        other = "S" if right_left_pole == "N" else "N"
        b.append(magnet_h(304, cy - 9, 80, 18, left=right_left_pole, right=other))
        b.append(arrow_v(360, cy - 16, 320, cy - 16))
        b.append(t(200, cy - 24, tag, 12))
    return svg(400, 184, "".join(b))


# ------------------------------------------------------------------ 19 (reprint)
def fig19():
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


# ------------------------------------------------------------------ 20
def fig20():
    b = [line(6, 47, 394, 47, sw=0.5, dash="2,3", color=MID)]
    b.append(rect(22, 84, 104, 10, rx=2, fill="#f2f2f2", sw=1) + circle(36, 98, 4.5) + circle(112, 98, 4.5))
    b.append(line(8, 103, 250, 103, sw=1.2))
    b.append(coil_h(34, 30, turns=8, pitch=10, h=34) + t(74, 22, "A", 13, weight=700))
    (lx, ly), (rx, ry) = coil_leads(34, 30, 8, 10, 34)
    b.append(poly([(lx, ly), (lx, 76), (68, 76)]))
    b.append(battery(68, 76, plus_left=False))
    b.append(poly([(74, 76), (rx, 76), (rx, ry)]))
    b.append(arrow_v(140, 30, 186, 30, "v", ly=-3))
    b.append(coil_h(236, 30, turns=8, pitch=10, h=34) + t(276, 22, "B", 13, weight=700))
    (lx2, ly2), (rx2, ry2) = coil_leads(236, 30, 8, 10, 34)
    b.append(res_circuit(lx2, rx2, ly2, 98, "c", "d"))
    b.append(t(74, 120, "A와 전지는 수레에 고정", 9.5, fill="#444"))
    return svg(400, 126, "".join(b))

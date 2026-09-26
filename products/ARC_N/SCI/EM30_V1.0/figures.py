"""SVG figures for ARC N° 통합과학2 전자기 유도와 발전 30제.

Plain line drawings (black/gray) that survive B/W printing.
viewBox width 400 = one column (~84 mm).

Coil convention (used by verify.py): a side-view solenoid is drawn with
front strands "/" (solid) and back strands "\\" (light). Traversing the wire
from its left lead to its right lead, current on the front strands runs
upward, which makes the field inside the coil point to the LEFT.
"""
import math
import re

INK = "#1b1b1b"
GRAY = "#bdbdbd"
MID = "#8a8a8a"
LIGHT = "#ececec"
FONT = "Pretendard, 'Noto Sans KR', sans-serif"

DEFS = f"""
<defs>
  <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="{INK}"/>
  </marker>
  <marker id="ahs" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="{MID}"/>
  </marker>
  <pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <line x1="0" y1="0" x2="0" y2="6" stroke="#888" stroke-width="1"/>
  </pattern>
  <pattern id="dots" width="7" height="7" patternUnits="userSpaceOnUse">
    <rect width="7" height="7" fill="{LIGHT}"/><circle cx="2" cy="2" r="0.9" fill="#666"/>
    <circle cx="5.5" cy="5.5" r="0.9" fill="#666"/>
  </pattern>
</defs>"""


def chem(s, size):
    small = round(size * 0.68, 1)
    out, pos = [], 0
    for m in re.finditer(r"([\^_])\{([^}]*)\}", s):
        out.append(s[pos:m.start()])
        d = -size * 0.38 if m.group(1) == "^" else size * 0.25
        out.append(f'<tspan dy="{d:.1f}" font-size="{small}">{m.group(2)}</tspan><tspan dy="{-d:.1f}">​</tspan>')
        pos = m.end()
    out.append(s[pos:])
    return "".join(out)


def t(x, y, s, size=13, anchor="middle", weight=400, fill=INK, extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" '
            f'fill="{fill}" font-family="{FONT}" {extra}>{chem(s, size)}</text>')


def ti(x, y, s, size=13, anchor="middle"):
    """Italic symbol (t, v, θ, T ...)."""
    return t(x, y, s, size, anchor, extra='font-style="italic"')


def svg(w, h, body, maxw="100%"):
    return (f'<svg class="fig" viewBox="0 0 {w} {h}" style="width:{maxw}" '
            f'xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>')


def line(x1, y1, x2, y2, sw=1.2, dash=None, arrow=False, color=INK, both=False):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    a = ' marker-end="url(#ah)"' if arrow else ""
    if both:
        a += ' marker-start="url(#ah)"'
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{sw}"{d}{a}/>'


def path(d, sw=1.2, fill="none", arrow=False, dash=None, color=INK):
    a = ' marker-end="url(#ah)"' if arrow else ""
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{sw}"{a}{ds}/>'


def rect(x, y, w, h, fill="#fff", sw=1.2, rx=0, color=INK):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{color}" stroke-width="{sw}"/>'


def circle(cx, cy, r, fill="#fff", sw=1.2):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="{sw}"/>'


def dot(cx, cy, r=2.4, fill=INK):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}"/>'


def poly(pts, sw=1.2, color=INK):
    return f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{color}" stroke-width="{sw}"/>'


# ------------------------------------------------------------------ parts
def magnet_h(x, y, w=64, h=18, left="S", right="N", size=12):
    """Horizontal bar magnet; the N half is shaded."""
    half = w / 2
    out = []
    for i, pole in enumerate((left, right)):
        dark = pole == "N"
        out.append(rect(x + i * half, y, half, h, fill="#5a5a5a" if dark else "#fff", sw=1.1))
        out.append(t(x + i * half + half / 2, y + h / 2 + size * 0.36, pole, size, weight=700,
                     fill="#fff" if dark else INK))
    return "".join(out)


def magnet_v(x, y, w=18, h=56, top="S", bottom="N", size=12):
    half = h / 2
    out = []
    for i, pole in enumerate((top, bottom)):
        dark = pole == "N"
        out.append(rect(x, y + i * half, w, half, fill="#5a5a5a" if dark else "#fff", sw=1.1))
        out.append(t(x + w / 2, y + i * half + half / 2 + size * 0.36, pole, size, weight=700,
                     fill="#fff" if dark else INK))
    return "".join(out)


def coil_h(x, y, turns=7, pitch=9, h=34, reverse=False):
    """Side view solenoid, axis horizontal. Leads leave from the bottom-left
    (x, y+h) and bottom-right (x+turns*pitch, y+h).
    reverse=True draws the opposite winding (front strands "\\")."""
    out = [f'<rect x="{x - 3:.1f}" y="{y:.1f}" width="{turns * pitch + 6:.1f}" height="{h}" rx="4" fill="#f6f6f6" stroke="none"/>']
    for k in range(turns):
        x0 = x + k * pitch
        if not reverse:
            out.append(line(x0 + pitch / 2, y, x0 + pitch, y + h, sw=0.9, color=GRAY))      # back "\"
            out.append(line(x0, y + h, x0 + pitch / 2, y, sw=1.5))                          # front "/"
        else:
            out.append(line(x0, y + h, x0 + pitch / 2, y, sw=0.9, color=GRAY))
            out.append(line(x0 + pitch / 2, y, x0 + pitch, y + h, sw=1.5))
    for ex in (x, x + turns * pitch):
        out.append(f'<ellipse cx="{ex:.1f}" cy="{y + h / 2:.1f}" rx="3.2" ry="{h / 2:.1f}" fill="none" '
                   f'stroke="{MID}" stroke-width="0.8"/>')
    return "".join(out)


def coil_leads(x, y, turns=7, pitch=9, h=34):
    return (x, y + h), (x + turns * pitch, y + h)


def galv(cx, cy, r=13, label="G"):
    return (circle(cx, cy, r) + t(cx, cy + 4.6, label, 12.5, weight=600))


def meter(cx, cy, w=46, h=34, needle=0.0):
    """Galvanometer with a centre-zero scale; needle in [-1, 1]."""
    x, y = cx - w / 2, cy - h / 2
    out = [rect(x, y, w, h, rx=3)]
    r = h * 0.72
    ax, ay = cx, y + h - 5
    out.append(path(f"M{ax - r * 0.8:.1f},{ay - r * 0.6:.1f} A{r},{r} 0 0 1 {ax + r * 0.8:.1f},{ay - r * 0.6:.1f}", sw=0.9))
    for k in (-0.8, -0.4, 0, 0.4, 0.8):
        a = math.asin(k)
        out.append(line(ax + r * math.sin(a), ay - r * math.cos(a), ax + (r - 4) * math.sin(a), ay - (r - 4) * math.cos(a), sw=0.8))
    a = math.asin(max(-0.9, min(0.9, needle)))
    out.append(line(ax, ay, ax + (r - 2) * math.sin(a), ay - (r - 2) * math.cos(a), sw=1.3))
    out.append(dot(ax, ay, 1.8))
    out.append(t(cx, y - 3, "0", 9))
    return "".join(out)


def resistor_h(x1, x2, y, amp=5):
    n = 6
    w = (x2 - x1) * 0.6
    s = x1 + (x2 - x1 - w) / 2
    pts = [(x1, y), (s, y)]
    for i in range(n):
        pts.append((s + w * (i + 0.5) / n, y + (amp if i % 2 == 0 else -amp)))
    pts += [(s + w, y), (x2, y)]
    return poly(pts, sw=1.2)


def switch_h(x1, x2, y, closed=True):
    out = [dot(x1, y, 2.2), dot(x2, y, 2.2)]
    if closed:
        out.append(line(x1, y, x2, y, sw=1.4))
    else:
        out.append(line(x1, y, x2 - 3, y - (x2 - x1) * 0.45, sw=1.4))
    return "".join(out)


def led_h(x, y, forward=True, label=""):
    """LED on a horizontal wire centred at x; forward=True conducts left→right."""
    s = 1 if forward else -1
    tri = f"M{x - 7 * s:.1f},{y - 7} L{x - 7 * s:.1f},{y + 7} L{x + 6 * s:.1f},{y} Z"
    out = [f'<path d="{tri}" fill="#fff" stroke="{INK}" stroke-width="1.2"/>',
           line(x + 6 * s, y - 7, x + 6 * s, y + 7, sw=1.4)]
    for dx in (-2, 4):
        out.append(line(x + dx, y - 9, x + dx + 5, y - 16, sw=0.8, arrow=True))
    if label:
        out.append(t(x, y + 22, label, 11.5, weight=600))
    return "".join(out)


def arrow_v(x1, y1, x2, y2, label="", lx=0, ly=-6, size=12):
    out = [line(x1, y1, x2, y2, sw=1.3, arrow=True)]
    if label:
        out.append(ti((x1 + x2) / 2 + lx, (y1 + y2) / 2 + ly, label, size))
    return "".join(out)


def axes(ox, oy, x2, y2, xl="", yl="", xl_anchor="end"):
    out = [line(ox, oy, x2, oy), line(ox, oy, ox, y2)]
    if xl:
        out.append(t(x2, oy + 16, xl, 11.5, anchor=xl_anchor))
    if yl:
        out.append(t(ox - 4, y2 - 6, yl, 11.5, anchor="start"))
    return "".join(out)


def tick_x(x, oy, label, italic=False, size=11.5):
    lab = ti(x, oy + 15, label, size) if italic else t(x, oy + 15, label, size)
    return line(x, oy, x, oy + 4) + lab


def tick_y(ox, y, label, size=11.5):
    return line(ox - 4, y, ox, y) + t(ox - 7, y + 4, label, size, anchor="end")


def curve(f, x0, x1, n=120):
    pts = [(x0 + (x1 - x0) * i / n, None) for i in range(n + 1)]
    return [(x, f(x)) for x, _ in pts]


# ----------------------------------------------------------- generator view
def gen_top(cx, cy, theta, W=118, H=84, pole_w=16, show_axis=True, p_label="p", rot=True, coil_len=None,
            extra_coil=None):
    """Top view: N pole at left, S pole at right, uniform field left→right.
    theta = angle (deg) between the coil plane and the field, measured
    counter-clockwise; the coil edge is drawn as a thick segment whose end
    at +theta is side p (filled dot)."""
    out = []
    x0, x1 = cx - W / 2, cx + W / 2
    out.append(rect(x0, cy - H / 2, pole_w, H, fill="#5a5a5a", sw=1))
    out.append(t(x0 + pole_w / 2, cy + 4.5, "N", 12, weight=700, fill="#fff"))
    out.append(rect(x1 - pole_w, cy - H / 2, pole_w, H, sw=1))
    out.append(t(x1 - pole_w / 2, cy + 4.5, "S", 12, weight=700))
    for dy in (-H * 0.36, H * 0.36):
        out.append(line(x0 + pole_w + 3, cy + dy, x1 - pole_w - 4, cy + dy, sw=0.7, dash="3,3", color=MID))
        out.append(f'<path d="M{cx + 6:.1f},{cy + dy - 3:.1f} L{cx + 12:.1f},{cy + dy:.1f} L{cx + 6:.1f},{cy + dy + 3:.1f}" fill="none" stroke="{MID}" stroke-width="0.9"/>')
    L = coil_len or (W - 2 * pole_w) * 0.34

    def seg(th, lab, filled=True):
        a = math.radians(th)
        dx, dy = L * math.cos(a), -L * math.sin(a)
        s = [line(cx - dx, cy - dy, cx + dx, cy + dy, sw=3.2, color="#333")]
        s.append(dot(cx + dx, cy + dy, 3.4, INK if filled else "#fff"))
        if not filled:
            s.append(circle(cx + dx, cy + dy, 3.4, sw=1.1))
        if lab:
            lx, ly = cx + (L + 11) * math.cos(a), cy - (L + 11) * math.sin(a)
            s.append(t(lx, ly + 4, lab, 11.5, weight=600))
        return "".join(s)

    out.append(seg(theta, p_label))
    if extra_coil is not None:
        th2, lab2 = extra_coil
        out.append(seg(th2, lab2, filled=False))
    if show_axis:
        out.append(circle(cx, cy, 2.6, fill="#fff", sw=1))
    if rot:
        r = L + 4
        out.append(path(f"M{cx + r * math.cos(math.radians(-60)):.1f},{cy - r * math.sin(math.radians(-60)):.1f} "
                        f"A{r},{r} 0 0 0 {cx + r * math.cos(math.radians(-15)):.1f},{cy - r * math.sin(math.radians(-15)):.1f}",
                        sw=0.9, arrow=True, color=MID))
    return "".join(out)


# ================================================================== items
def fig01():
    b = [line(8, 92, 392, 92, sw=1.6), line(8, 97, 392, 97, sw=0.8)]
    b.append(magnet_h(60, 64, 76, 22))
    cx, cy = 232, 58
    b.append(coil_h(cx, cy, turns=8, pitch=10, h=34))
    (lx, ly), (rx, ry) = coil_leads(cx, cy, 8, 10, 34)
    b.append(poly([(lx, ly), (lx, 118), (292, 118)]))
    b.append(poly([(rx, ry), (rx, 118), (332, 118)]))
    b.append(meter(312, 124, 40, 26))
    b.append(t(98, 56, "자석", 11.5))
    b.append(t(272, 50, "코일", 11.5))
    b.append(t(352, 128, "검류계", 11.5, anchor="start"))
    b.append(t(200, 150, "레일", 11, fill="#555"))
    b.append(line(200, 140, 200, 99, sw=0.6, color="#777"))
    return svg(400, 156, "".join(b), "80%")


def fig03():
    b = []
    for i, (th, lab) in enumerate([(0, "(가)"), (45, "(나)"), (90, "(다)"), (180, "(라)")]):
        cx = 100 + (i % 2) * 200
        cy = 62 + (i // 2) * 130
        b.append(gen_top(cx, cy, th, W=150, H=80))
        b.append(t(cx, cy + 58, lab, 12.5))
    return svg(400, 256, "".join(b), "74%")


def _dir_panel(x0, y0, mag_side, pole_face, move, coil_move=None, label=""):
    """Small panel: coil fixed at centre with galvanometer; magnet on the
    left or right of the coil, `pole_face` toward the coil, moving
    'toward' / 'away' (or fixed when coil_move is given)."""
    b = []
    cx, cy = x0 + 70, y0 + 12
    b.append(coil_h(cx, cy, turns=5, pitch=9, h=26))
    (lx, ly), (rx, ry) = coil_leads(cx, cy, 5, 9, 26)
    b.append(poly([(lx, ly), (lx, y0 + 50), (cx + 12, y0 + 50)]))
    b.append(poly([(rx, ry), (rx, y0 + 50), (cx + 33, y0 + 50)]))
    b.append(galv(cx + 22.5, y0 + 50, 9))
    my = cy + 4
    other = "S" if pole_face == "N" else "N"
    if mag_side == "L":
        mx = x0 + 6
        b.append(magnet_h(mx, my, 50, 18, left=other, right=pole_face, size=11))
        tip = mx + 50
        if move == "toward":
            b.append(arrow_v(mx + 10, my - 6, mx + 38, my - 6))
        elif move == "away":
            b.append(arrow_v(mx + 38, my - 6, mx + 10, my - 6))
        else:
            b.append(t(mx + 25, my - 5, "고정", 10))
    else:
        mx = x0 + 128
        b.append(magnet_h(mx, my, 50, 18, left=pole_face, right=other, size=11))
        if move == "toward":
            b.append(arrow_v(mx + 40, my - 6, mx + 12, my - 6))
        elif move == "away":
            b.append(arrow_v(mx + 12, my - 6, mx + 40, my - 6))
        else:
            b.append(t(mx + 25, my - 5, "고정", 10))
    if coil_move:
        b.append(arrow_v(cx + 34, cy - 6, cx + 8, cy - 6))
        b.append(t(cx + 22, cy - 13, "코일 이동", 9.5))
    if label:
        b.append(t(x0 + 94, y0 + 80, label, 12))
    return "".join(b)


def fig04():
    b = []
    b.append(rect(2, 4, 196, 90, fill="#fafafa", sw=0.6, color="#999"))
    b.append(_dir_panel(4, 16, "L", "N", "toward"))
    b.append(t(100, 88, "기준: 바늘이 오른쪽으로 움직임", 10.5))
    panels = [("L", "S", "toward", None, "(가)"), ("L", "N", "away", None, "(나)"),
              ("R", "S", "toward", None, "(다)"), ("L", "N", "fixed", True, "(라)")]
    pos = [(204, 12), (4, 110), (204, 110), (4, 208)]
    for (side, face, mv, cm, lab), (x0, y0) in zip(panels, pos):
        b.append(_dir_panel(x0, y0, side, face, mv, cm, lab))
    return svg(400, 296, "".join(b))


def fig06():
    b = []
    for i, (phi, lab) in enumerate([(0, "(가)"), (90, "(나)"), (180, "(다)")]):
        x0 = i * 134
        mx, my = x0 + 40, 58
        a = math.radians(phi)
        L = 26
        nx, ny = mx + L * math.cos(a), my - L * math.sin(a)
        sx, sy = mx - L * math.cos(a), my + L * math.sin(a)
        # magnet as two thick halves
        b.append(line(mx, my, nx, ny, sw=11, color="#5a5a5a"))
        b.append(line(mx, my, sx, sy, sw=11, color="#fff"))
        b.append(line(mx, my, sx, sy, sw=11, color="#fff"))
        b.append(f'<g transform="rotate({-phi} {mx} {my})">'
                 f'<rect x="{mx - L}" y="{my - 5.5}" width="{2 * L}" height="11" fill="none" stroke="{INK}" stroke-width="1.1"/>'
                 f'<line x1="{mx}" y1="{my - 5.5}" x2="{mx}" y2="{my + 5.5}" stroke="{INK}" stroke-width="1"/></g>')
        b.append(t(nx + (9 * math.cos(a)) , ny - 9 * math.sin(a) + 4, "N", 11, weight=700))
        b.append(t(sx - 9 * math.cos(a), sy + 9 * math.sin(a) + 4, "S", 11, weight=700))
        b.append(circle(mx, my, 2.2, sw=0.9))
        # coil to the right, axis horizontal
        cxx = x0 + 82
        b.append(coil_h(cxx, my - 15, turns=4, pitch=8, h=30))
        (lx, ly), (rx, ry) = coil_leads(cxx, my - 15, 4, 8, 30)
        b.append(poly([(lx, ly), (lx, my + 30), (cxx + 8, my + 30)]))
        b.append(poly([(rx, ry), (rx, my + 30), (cxx + 24, my + 30)]))
        b.append(galv(cxx + 16, my + 30, 7.5))
        b.append(line(mx - 34, my, cxx + 40, my, sw=0.6, dash="2,3", color=MID))
        b.append(t(x0 + 62, 118, lab, 12))
    b.append(path("M28,20 A30,30 0 0 1 58,22", sw=0.9, arrow=True, color=MID))
    b.append(t(8, 14, "회전", 10, anchor="start", fill="#555"))
    return svg(400, 124, "".join(b))


def fig07():
    b = [line(150, 10, 390, 10, sw=2.4)]
    for cx, lab, gap in [(200, "P", False), (330, "Q", True)]:
        b.append(line(cx, 10, cx, 52, sw=0.8))
        rx, ry = 7, 26
        if gap:
            # draw ring as ellipse with small gap at the bottom
            b.append(path(f"M{cx - 3.6},{102.6} A{rx},{ry} 0 1 1 {cx + 3.6},{102.6}", sw=3, color="#666"))
        else:
            b.append(f'<ellipse cx="{cx}" cy="{78}" rx="{rx}" ry="{ry}" fill="none" stroke="#666" stroke-width="3"/>')
        b.append(t(cx + 20, 82, lab, 13, weight=700))
    b.append(t(349, 124, "끊어진 부분", 10.5))
    b.append(line(333, 114, 331, 106, sw=0.6))
    b.append(magnet_h(40, 69, 90, 18, left="S", right="N"))
    b.append(arrow_v(76, 60, 118, 60))
    return svg(400, 130, "".join(b), "86%")


def fig08():
    b = []
    # setup strip
    b.append(line(20, 40, 380, 40, sw=0.7, dash="2,3", color=MID))
    b.append(magnet_h(22, 31, 48, 18))
    b.append(coil_h(280, 23, turns=6, pitch=9, h=34))
    (lx, ly), (rx, ry) = coil_leads(280, 23, 6, 9, 34)
    b.append(poly([(lx, ly), (lx, 84), (318, 84)]))
    b.append(poly([(rx, ry), (rx, 84), (336, 84)]))
    b.append(galv(327, 84, 8))
    for x, lab in [(70, "0"), (140, "d"), (210, "2d"), (280, "3d")]:
        b.append(line(x, 58, x, 64, sw=0.9))
        b.append(ti(x, 76, "x=" + lab if lab != "0" else "x=0", 11))
    b.append(t(200, 108, "(가)", 12))
    # x-t graph
    ox, oy = 60, 250
    sx, sy = 70, 42
    b.append(axes(ox, oy, 380, 128, "", "N극의 위치 x"))
    b.append(t(386, oy + 4, "시간(s)", 11, anchor="start") if False else t(380, oy + 30, "시간(s)", 11, anchor="end"))
    for k in range(1, 5):
        b.append(tick_x(ox + k * sx, oy, str(k)))
    b.append(t(ox - 7, oy + 4, "0", 11.5, anchor="end"))
    for k, lab in [(1, "d"), (2, "2d")]:
        b.append(line(ox - 4, oy - k * sy, ox, oy - k * sy) + ti(ox - 8, oy - k * sy + 4, lab, 11.5, anchor="end"))
    b.append(line(ox, oy - 2 * sy, ox + 3 * sx, oy - 2 * sy, sw=0.6, dash="3,3", color=MID))
    for k in (2, 3):
        b.append(line(ox + k * sx, oy, ox + k * sx, oy - 2 * sy, sw=0.6, dash="3,3", color=MID))
    b.append(poly([(ox, oy), (ox + 2 * sx, oy - 2 * sy), (ox + 3 * sx, oy - 2 * sy), (ox + 4 * sx, oy)], sw=1.7))
    b.append(t(200, 294, "(나)", 12))
    return svg(400, 300, "".join(b), "92%")


def fig09():
    b = [gen_top(92, 64, 90, W=150, H=84)]
    b.append(t(92, 128, "(가)", 11.5))
    ox, oy, W, A = 200, 70, 180, 44
    b.append(line(ox, oy, ox + W, oy) + line(ox, 16, ox, 124))
    b.append(t(ox + W, oy - 6, "시간", 11, anchor="end"))
    b.append(t(ox + 4, 12, "전류", 11, anchor="start"))
    b.append(tick_y(ox, oy - A, "I_{0}"))
    b.append(tick_y(ox, oy + A, "-I_{0}"))
    b.append(t(ox - 7, oy + 4, "0", 11, anchor="end"))
    pts = curve(lambda x: oy - A * math.sin(2 * math.pi * (x - ox) / (W - 20)), ox, ox + W - 20)
    b.append(poly(pts, sw=1.6))
    for k, lab in [(1, "T/4"), (2, "T/2"), (3, "3T/4"), (4, "T")]:
        x = ox + (W - 20) * k / 4
        b.append(line(x, oy - 3, x, oy + 3))
        b.append(ti(x, oy - 7 if k == 3 else oy + 16, lab, 10.5))
    b.append(line(ox + (W - 20) / 4, oy - A, ox + (W - 20) / 4, oy, sw=0.6, dash="3,3", color=MID))
    b.append(line(ox, oy - A, ox + (W - 20) / 4, oy - A, sw=0.6, dash="3,3", color=MID))
    b.append(t(290, 142, "(나)", 11.5))
    return svg(400, 148, "".join(b))


def fig10():
    b = []
    boxes = [(8, "물의 위치 에너지", "100"), (146, "수차의 운동 에너지", "85"), (284, "전기 에너지", "76")]
    for x, name, val in boxes:
        b.append(rect(x, 14, 108, 44, rx=3))
        b.append(t(x + 54, 32, name, 11))
        b.append(t(x + 54, 50, val, 12.5, weight=600))
    b.append(line(116, 36, 144, 36, arrow=True) + t(130, 29, "수차", 9.5, fill="#444"))
    b.append(line(254, 36, 282, 36, arrow=True) + t(268, 29, "발전기", 9.5, fill="#444"))
    for x, v in [(130, "15"), (268, "9")]:
        b.append(line(x, 40, x, 78, sw=1.0, arrow=True, color=MID))
        b.append(t(x, 92, f"열, 소리 에너지 등 {v}", 10.5))
    return svg(400, 100, "".join(b))


def fig11():
    b = []
    cx, cy, n, p, hh = 170, 58, 9, 11, 40
    b.append(coil_h(cx, cy, turns=n, pitch=p, h=hh))
    (lx, ly), (rx, ry) = coil_leads(cx, cy, n, p, hh)
    # leads go down, around, up to resistor above
    b.append(poly([(lx, ly), (lx, ly + 16), (150, ly + 16), (150, 26), (200, 26)]))
    b.append(poly([(rx, ry), (rx, ly + 16), (290, ly + 16), (290, 26), (240, 26)]))
    b.append(resistor_h(200, 240, 26))
    b.append(dot(200, 26) + t(200, 16, "a", 12, weight=600))
    b.append(dot(240, 26) + t(240, 16, "b", 12, weight=600))
    b.append(t(220, 48, "저항", 10.5))
    b.append(magnet_h(30, 69, 80, 18))
    b.append(arrow_v(56, 60, 98, 60))
    b.append(t(210, 130, "코일", 11))
    return svg(400, 136, "".join(b), "90%")


def fig12():
    b = [line(10, 92, 390, 92, sw=1.6)]
    # coil around the track (drawn as a ring cross-section)
    b.append(f'<ellipse cx="200" cy="70" rx="10" ry="34" fill="none" stroke="{INK}" stroke-width="3"/>')
    b.append(poly([(200, 36), (200, 20), (228, 20)]))
    b.append(poly([(200, 104), (200, 112), (248, 112), (248, 20), (244, 20)]))
    b.append(galv(236, 20, 8))
    b.append(t(182, 26, "코일", 11, anchor="end"))
    # cart with magnet
    b.append(rect(58, 70, 70, 16, rx=2))
    b.append(circle(72, 88, 4.5) + circle(114, 88, 4.5))
    b.append(magnet_h(62, 52, 62, 16, size=11))
    b.append(arrow_v(70, 42, 116, 42))
    # spring + wall
    b.append(rect(376, 40, 10, 52, fill="url(#hatch)", sw=1))
    pts = [(376, 72)]
    for i in range(10):
        pts.append((372 - i * 5 - 2.5, 64 if i % 2 == 0 else 80))
    pts.append((318, 72))
    b.append(poly(pts, sw=1.1))
    b.append(line(318, 64, 318, 80, sw=2))
    for x, lab in [(150, "p"), (274, "q")]:
        b.append(dot(x, 92, 2.8) + t(x, 108, lab, 12, extra='font-style="italic"'))
    b.append(t(348, 110, "용수철", 10.5))
    return svg(400, 118, "".join(b), "94%")


def fig14():
    b = [gen_top(88, 58, 30, W=150, H=84, rot=True)]
    a = math.radians(30)
    L = (150 - 32) * 0.34
    b.append(path(f"M{88 + 26:.1f},58 A26,26 0 0 0 {88 + 26 * math.cos(a):.1f},{58 - 26 * math.sin(a):.1f}", sw=0.9))
    b.append(ti(88 + 34, 52, "θ", 12))
    b.append(t(88, 118, "(가)", 11.5))
    ox, oy, W, A = 196, 62, 172, 40
    b.append(line(ox, oy, ox + W + 8, oy) + line(ox, 12, ox, 112))
    b.append(t(ox + W + 12, oy + 4, "θ", 11.5, anchor="start", extra='font-style="italic"'))
    b.append(t(ox + 4, 10, "전류", 11, anchor="start"))
    b.append(tick_y(ox, oy - A, "I_{0}") + tick_y(ox, oy + A, "-I_{0}"))
    pts = curve(lambda x: oy - A * math.cos(2 * math.pi * (x - ox) / W), ox, ox + W)
    b.append(poly(pts, sw=1.6))
    for k, lab in [(1, "90°"), (2, "180°"), (3, "270°"), (4, "360°")]:
        x = ox + W * k / 4
        b.append(line(x, oy - 3, x, oy + 3))
        b.append(t(x - (8 if k == 4 else 0), oy - 6 if k == 2 else oy + 14, lab, 10))
    b.append(t(ox - 7, oy + 4, "0", 11, anchor="end"))
    b.append(t(290, 124, "(나)", 11.5))
    return svg(400, 130, "".join(b))


def fig15():
    b = []
    for i, (lab, closed) in enumerate([("(가)", False), ("(나)", True)]):
        x0 = i * 200
        b.append(line(x0 + 30, 8, x0 + 100, 8, sw=2.2))
        b.append(line(x0 + 64, 8, x0 + 64, 64, sw=0.8))
        b.append(magnet_h(x0 + 38, 64, 52, 16, left="S", right="N", size=10))
        b.append(path(f"M{x0 + 30},{94} Q{x0 + 64},{104} {x0 + 98},{94}", sw=0.8, dash="2,2", color=MID, arrow=True))
        b.append(path(f"M{x0 + 98},{94} Q{x0 + 64},{104} {x0 + 30},{94}", sw=0, color="none"))
        b.append(coil_h(x0 + 116, 57, turns=5, pitch=9, h=30))
        (lx, ly), (rx, ry) = coil_leads(x0 + 116, 57, 5, 9, 30)
        b.append(poly([(lx, ly), (lx, 110), (x0 + 124, 110)]))
        b.append(poly([(rx, ry), (rx, 110), (x0 + 150, 110)]))
        b.append(switch_h(x0 + 124, x0 + 150, 110, closed))
        b.append(t(x0 + 137, 128, "스위치 " + ("닫힘" if closed else "열림"), 10.5))
        b.append(t(x0 + 100, 150, lab, 12))
    ox, oy = 60, 262
    b.append(axes(ox, oy, 370, 180, "시간", "자석의 진폭"))
    b.append(line(ox, 204, 356, 204, sw=1.6))
    b.append(t(362, 208, "(가)", 11, anchor="start"))
    b.append(poly(curve(lambda x: 204 + 50 * (1 - math.exp(-(x - ox) / 110)), ox, 356), sw=1.6))
    b.append(t(362, 252, "(나)", 11, anchor="start"))
    b.append(t(ox - 7, oy + 4, "0", 11, anchor="end"))
    return svg(400, 286, "".join(b), "92%")


def _pass_graph(amp=1.0, width=1.0, W=150, H=80, flip=False, label=None):
    """Induced current while a magnet passes through a coil (+ then -)."""
    ox, oy = 14, H / 2 + 6
    out = [line(ox, oy, ox + W - 10, oy) + line(ox, 8, ox, H + 4)]
    out.append(t(ox + W - 10, oy + 13, "t", 10.5, anchor="end", extra='font-style="italic"'))
    out.append(t(ox + 2, 8, "I", 10.5, anchor="start", extra='font-style="italic"'))
    span = (W - 30) * 0.8 * width
    A = (H / 2 - 12) * 0.62 * amp
    s = -1 if flip else 1

    def f(x):
        u = (x - ox - 6) / span
        if u < 0 or u > 1:
            return oy
        return oy - s * A * math.sin(2 * math.pi * u) * (1 - 0.15 * math.cos(2 * math.pi * u))
    out.append(poly(curve(f, ox, ox + W - 12, 200), sw=1.5))
    ref = (W - 30) * 0.8
    out.append(line(ox + 6 + ref, oy - 3, ox + 6 + ref, oy + 3, sw=1))
    out.append(ti(ox + 6 + ref, oy + 14, "t_{0}", 9.5))
    Aref = (H / 2 - 12) * 0.62
    out.append(line(ox - 3, oy - Aref, ox + W - 12, oy - Aref, sw=0.5, dash="2,3", color=MID))
    if label:
        out.append(t(ox + (W - 10) / 2, H + 22, label, 11.5))
    return out


def fig16_base():
    return svg(160, 96, "".join(_pass_graph(label=None)), "44%")


def fig16_choice(amp, width, flip=False):
    return svg(160, 92, "".join(_pass_graph(amp, width, flip=flip)), "100%")


def fig17():
    b = []
    b.append(line(20, 30, 380, 30, sw=1.3))
    b.append(path("M110,30 Q200,14 290,30", sw=0.8, dash="3,2", color=MID))
    b.append(path("M110,30 Q200,46 290,30", sw=0.8, dash="3,2", color=MID))
    b.append(t(372, 22, "금속 줄", 10.5, anchor="end"))
    # vertical magnet (N up) with a coil wound around it
    mx, my = 190, 46
    b.append(magnet_v(mx, my, 20, 88, top="N", bottom="S", size=10))
    for k in range(4):
        y = my + 34 + k * 6
        b.append(path(f"M{mx - 7},{y} Q{mx + 10},{y + 6} {mx + 27},{y}", sw=1.5))
        b.append(path(f"M{mx - 7},{y} Q{mx + 10},{y - 4} {mx + 27},{y}", sw=0.8, color=GRAY))
    b.append(poly([(mx - 7, my + 34), (mx - 30, my + 34), (mx - 30, 148), (296, 148)]))
    b.append(poly([(mx + 27, my + 52), (mx + 40, my + 52), (mx + 40, 138), (296, 138)]))
    b.append(rect(296, 128, 64, 30, rx=3) + t(328, 147, "앰프", 11))
    b.append(t(mx - 36, my + 48, "코일", 10.5, anchor="end"))
    b.append(t(mx + 30, my + 16, "자석", 10.5, anchor="start"))
    b.append(t(120, 124, "픽업", 11))
    return svg(400, 164, "".join(b), "86%")


def fig18():
    b = [line(10, 50, 390, 50, sw=0.6, dash="2,3", color=MID)]
    for x0, lab, g in [(40, "A", "G_{1}"), (270, "B", "G_{2}")]:
        b.append(coil_h(x0, 33, turns=7, pitch=11, h=34))
        (lx, ly), (rx, ry) = coil_leads(x0, 33, 7, 11, 34)
        b.append(poly([(lx, ly), (lx, 96), (x0 + 28, 96)]))
        b.append(poly([(rx, ry), (rx, 96), (x0 + 50, 96)]))
        b.append(galv(x0 + 39, 96, 11, label=""))
        b.append(t(x0 + 39, 100.5, g, 11, weight=600))
        b.append(t(x0 + 38, 24, lab, 13, weight=700))
    b.append(magnet_h(160, 41, 76, 18))
    b.append(arrow_v(176, 30, 222, 30, "v", ly=-5))
    return svg(400, 118, "".join(b), "94%")


def fig20():
    b = []
    for x, lab, obj in [(60, "A (알루미늄 관)", "자석"), (200, "B (플라스틱 관)", "자석"), (340, "A (알루미늄 관)", "쇠구슬")]:
        b.append(rect(x - 14, 20, 28, 120, fill="#f4f4f4" if "플라" in lab else "url(#hatch)", sw=1.1))
        b.append(rect(x - 9, 20, 18, 120, fill="#fff", sw=0.6, color="#777"))
        if obj == "자석":
            b.append(magnet_v(x - 7, 28, 14, 28, top="S", bottom="N", size=8.5))
        else:
            b.append(circle(x, 36, 7, fill="#9c9c9c", sw=1))
        b.append(line(x + 20, 40, x + 20, 90, arrow=True, sw=1))
        b.append(t(x, 158, lab, 10.5))
        b.append(t(x, 174, obj, 10.5, fill="#444"))
    return svg(400, 180, "".join(b))


def fig21():
    b = []
    cx, cy, n, p, hh = 170, 84, 8, 11, 36
    b.append(coil_h(cx, cy, turns=n, pitch=p, h=hh))
    (lx, ly), (rx, ry) = coil_leads(cx, cy, n, p, hh)
    nl, nr = 150, 280                     # left / right nodes of the LED pair
    b.append(poly([(lx, ly), (lx, 136), (nl, 136), (nl, 44)]))
    b.append(poly([(rx, ry), (rx, 136), (nr, 136), (nr, 44)]))
    mid = (nl + nr) / 2
    for y, fwd, lab in [(14, False, "P"), (44, True, "Q")]:
        b.append(poly([(nl, 44), (nl, y), (mid - 8, y)]) if y != 44 else line(nl, 44, mid - 8, 44))
        b.append(poly([(mid + 8, y), (nr, y), (nr, 44)]) if y != 44 else line(mid + 8, 44, nr, 44))
        b.append(led_h(mid, y, forward=fwd))
        b.append(t(mid + 18, y + 16, lab, 12, weight=700, anchor="start"))
    b.append(dot(nl, 44) + dot(nr, 44))
    b.append(magnet_h(30, 93, 80, 18))
    b.append(t(214, 150, "코일", 10.5))
    return svg(400, 156, "".join(b), "80%")


def fig22():
    b = [gen_top(100, 56, 30, W=160, H=84), gen_top(300, 56, 90, W=160, H=84)]
    b.append(t(100, 116, "A", 12.5, weight=700) + t(300, 116, "B", 12.5, weight=700))
    a = math.radians(30)
    b.append(path(f"M{100 + 24},56 A24,24 0 0 0 {100 + 24 * math.cos(a):.1f},{56 - 24 * math.sin(a):.1f}", sw=0.9))
    b.append(t(100 + 38, 52, "30°", 10))
    return svg(400, 122, "".join(b))


def fig23():
    b = []
    b.append(f'<rect x="120" y="14" width="160" height="104" rx="30" fill="none" stroke="#777" stroke-width="12"/>')
    b.append(t(200, 70, "철심", 11, fill="#555"))
    for x0 in (106, 266):
        for k in range(5):
            y = 36 + k * 11
            b.append(path(f"M{x0},{y} q14,5 28,0", sw=1.5))
    b.append(t(98, 30, "A", 13, weight=700, anchor="end"))
    b.append(t(302, 30, "B", 13, weight=700, anchor="start"))
    # A circuit: battery + switch
    b.append(poly([(106, 36), (60, 36), (60, 58)]))
    b.append(line(52, 58, 68, 58, sw=1.6) + line(55, 64, 65, 64, sw=3))
    b.append(t(46, 66, "전지", 10, anchor="end"))
    b.append(poly([(60, 64), (60, 90)]))
    b.append(switch_h(60, 84, 90, closed=False) if False else "")
    b.append(dot(60, 90, 2) + dot(60, 112, 2) + line(60, 90, 72, 110, sw=1.4))
    b.append(t(48, 104, "S", 11, anchor="end", weight=600))
    b.append(poly([(60, 112), (60, 124), (106, 124), (106, 80)]))
    # B circuit: galvanometer
    b.append(poly([(294, 36), (340, 36), (340, 64)]))
    b.append(galv(340, 78, 13))
    b.append(poly([(340, 92), (340, 124), (294, 124), (294, 80)]))
    return svg(400, 132, "".join(b), "86%")


def fig24():
    b = []
    cx = 90
    b.append(coil_h(60, 150, turns=6, pitch=10, h=26).replace("<rect", "<rect", 1))
    b.append(t(46, 168, "코일", 10.5, anchor="end"))
    (lx, ly), (rx, ry) = coil_leads(60, 150, 6, 10, 26)
    b.append(poly([(lx, ly), (lx, 196), (80, 196)]) + poly([(rx, ry), (rx, 196), (100, 196)]))
    b.append(galv(90, 196, 9))
    b.append(magnet_v(cx - 8, 20, 16, 34, top="S", bottom="N", size=10))
    b.append(line(cx, 150, cx, 60, sw=0.6, dash="2,3", color=MID))
    b.append(line(130, 54, 130, 150, sw=0.8, both=True))
    b.append(ti(142, 106, "4h", 12, anchor="start"))
    b.append(t(cx, 226, "(가)", 12))
    b.append(t(60 + 200, 226, "(나)", 12))
    b.append(coil_h(260, 150, turns=6, pitch=10, h=26))
    (lx, ly), (rx, ry) = coil_leads(260, 150, 6, 10, 26)
    b.append(poly([(lx, ly), (lx, 196), (280, 196)]) + poly([(rx, ry), (rx, 196), (300, 196)]))
    b.append(galv(290, 196, 9))
    b.append(magnet_v(282, 94, 16, 34, top="S", bottom="N", size=10))
    b.append(line(290, 150, 290, 128, sw=0.6, dash="2,3", color=MID))
    b.append(line(330, 128, 330, 150, sw=0.8, both=True))
    b.append(ti(342, 144, "h", 12, anchor="start"))
    return svg(400, 232, "".join(b), "80%")


def fig25():
    ox, oy = 50, 70
    sx = 80
    b = [line(ox, oy, 380, oy) + line(ox, 10, ox, 130)]
    b.append(t(380, oy + 16, "시간(s)", 11, anchor="end") + t(ox + 4, 10, "전류", 11, anchor="start"))
    b.append(t(ox - 7, oy + 4, "0", 11, anchor="end"))
    b.append(t(ox - 7, 28, "+", 12, anchor="end") + t(ox - 7, 116, "−", 12, anchor="end"))
    for k in range(1, 4):
        b.append(tick_x(ox + k * sx, oy, str(k)))

    def f(x):
        u = (x - ox) / sx
        if 0 <= u <= 1:
            return oy - 34 * math.sin(math.pi * u) ** 1.2
        if 2 <= u <= 3:
            return oy + 46 * math.sin(math.pi * (u - 2)) ** 1.2
        return oy
    b.append(poly(curve(f, ox, ox + 3.6 * sx, 300), sw=1.6))
    return svg(400, 136, "".join(b), "88%")


def fig27():
    b = []
    for i, (lab, closed) in enumerate([("(가)", False), ("(나)", True)]):
        x0 = i * 200
        b.append(rect(x0 + 20, 30, 70, 50, rx=4, fill="#f7f7f7"))
        b.append(t(x0 + 55, 60, "발전기", 11))
        b.append(circle(x0 + 20, 55, 9) + line(x0 + 20, 55, x0 + 4, 40, sw=2) + dot(x0 + 4, 40, 3))
        b.append(t(x0 + 10, 100, "손잡이", 10))
        b.append(poly([(x0 + 90, 40), (x0 + 150, 40), (x0 + 150, 48)]))
        b.append(circle(x0 + 150, 60, 11) + line(x0 + 143, 53, x0 + 157, 67, sw=1) + line(x0 + 157, 53, x0 + 143, 67, sw=1))
        b.append(t(x0 + 170, 64, "전구", 10, anchor="start"))
        b.append(poly([(x0 + 150, 72), (x0 + 150, 96), (x0 + 128, 96)]))
        b.append(switch_h(x0 + 108, x0 + 128, 96, closed))
        b.append(poly([(x0 + 108, 96), (x0 + 90, 96), (x0 + 90, 72)]))
        b.append(t(x0 + 118, 114, "스위치 " + ("닫힘" if closed else "열림"), 10))
        b.append(t(x0 + 95, 136, lab, 12))
    return svg(400, 142, "".join(b))


def fig28():
    b = [rect(10, 70, 380, 50, fill="#f5f5f5", sw=0.8), line(10, 70, 390, 70, sw=1.4)]
    b.append(f'<ellipse cx="200" cy="96" rx="58" ry="12" fill="none" stroke="{INK}" stroke-width="2.4"/>')
    b.append(t(200, 136, "지면 아래에 수평으로 묻은 코일", 10.5))
    b.append(poly([(258, 96), (300, 96), (300, 104)]) + galv(300, 108, 0) if False else "")
    b.append(poly([(256, 99), (318, 99)]) + poly([(252, 93), (318, 93), (318, 88)]))
    b.append(galv(318, 76, 0) if False else "")
    b.append(rect(330, 82, 44, 26, rx=3) + t(352, 99, "G", 12, weight=600))
    b.append(line(318, 88, 330, 88) + line(318, 99, 330, 99))
    # car with magnet (N down)
    b.append(rect(52, 22, 76, 22, rx=5))
    b.append(circle(66, 48, 5) + circle(114, 48, 5))
    b.append(magnet_v(82, 36, 16, 26, top="S", bottom="N", size=9))
    b.append(arrow_v(66, 12, 116, 12, "v", ly=-3))
    b.append(line(90, 62, 90, 70, sw=0.5, dash="2,2", color=MID))
    return svg(400, 142, "".join(b), "92%")


def fig29():
    ox, oy = 50, 164
    b = [axes(ox, oy, 380, 30, "시간", "속력")]
    b.append(t(ox - 7, oy + 4, "0", 11, anchor="end"))
    k = 0.42

    def vA(x):
        return oy - k * (x - ox)

    # B: slowed while entering (t1..t2) and leaving (t3..t4) the coil
    t1, t2, t3, t4 = 130, 180, 230, 290

    def vB(x):
        v = 0.0
        for a, bb, s in [(ox, t1, k), (t1, t2, k * 0.25), (t2, t3, k), (t3, t4, k * 0.2), (t4, 380, k)]:
            if x > a:
                v += (min(x, bb) - a) * s
        return oy - v
    b.append(poly(curve(vA, ox, 360), sw=1.6))
    b.append(poly(curve(vB, ox, 372), sw=1.6))
    b.append(t(360, vA(360) - 6, "A", 12, weight=700))
    b.append(t(376, vB(372) + 4, "B", 12, weight=700, anchor="start"))
    for x, lab in [(t1, "t_{1}"), (t2, "t_{2}"), (t3, "t_{3}"), (t4, "t_{4}")]:
        b.append(line(x, oy, x, vB(x), sw=0.6, dash="3,3", color=MID))
        b.append(ti(x, oy + 15, lab, 11))
    return svg(400, 186, "".join(b), "88%")


def fig30():
    b = [gen_top(200, 68, 0, W=240, H=112, p_label="P", extra_coil=(90, "Q"), coil_len=42)]
    b.append(t(200, 144, "●: P의 한 변,  ○: Q의 한 변", 10.5, fill="#444"))
    return svg(400, 150, "".join(b), "80%")

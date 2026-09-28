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




def coil_v(cx, y, turns=6, w=56, pitch=9, ry=5):
    """Coil with a vertical axis seen slightly from above: each turn is an
    ellipse; the front (lower) half is solid, the back (upper) half light.
    Returns svg; leads leave at the top-left and bottom-right."""
    out = [f'<rect x="{cx - w / 2 - 2:.1f}" y="{y - ry:.1f}" width="{w + 4:.1f}" height="{turns * pitch + 2 * ry:.1f}" rx="5" fill="#f6f6f6" stroke="none"/>']
    for k in range(turns):
        yy = y + k * pitch
        out.append(path(f"M{cx - w / 2:.1f},{yy:.1f} A{w / 2:.1f},{ry} 0 0 1 {cx + w / 2:.1f},{yy:.1f}", sw=0.9, color=GRAY))
        out.append(path(f"M{cx - w / 2:.1f},{yy:.1f} A{w / 2:.1f},{ry} 0 0 0 {cx + w / 2:.1f},{yy:.1f}", sw=1.5))
    return "".join(out)


def coil_v_leads(cx, y, turns=6, w=56, pitch=9):
    return (cx - w / 2, y), (cx + w / 2, y + (turns - 1) * pitch)


def gen_top2(cx, cy, theta, cw=False, **kw):
    """gen_top with an optional clockwise rotation arrow."""
    s = gen_top(cx, cy, theta, rot=not cw, **kw)
    if cw:
        L = kw.get("coil_len") or (kw.get("W", 118) - 2 * kw.get("pole_w", 16)) * 0.34
        r = L + 4
        a1, a2 = math.radians(-15), math.radians(-60)
        s += path(f"M{cx + r * math.cos(a1):.1f},{cy - r * math.sin(a1):.1f} "
                  f"A{r},{r} 0 0 1 {cx + r * math.cos(a2):.1f},{cy - r * math.sin(a2):.1f}",
                  sw=0.9, arrow=True, color=MID)
    return s

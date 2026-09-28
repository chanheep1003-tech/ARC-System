"""SVG drawing primitives for ARC N° 통합과학2 산화와 환원 30제.

Plain line drawings (black/gray) that survive B/W printing.
viewBox width 400 = one column (~84 mm).
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

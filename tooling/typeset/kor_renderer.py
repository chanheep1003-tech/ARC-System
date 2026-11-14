#!/usr/bin/env python3
"""Production renderer for ARC_N / ARC_FINAL problem sets (KOR, SOC, SCI share this one layout).

Korean-language typesetting: registry passages (KOR), bundle material sets, standalone
items, tables, <보기> boxes and hash-bound figures (SOC/SCI) all use the same page model.

ARC_N:     cover, blank verso, two-column problem pages, blank separator, answer key.
ARC_FINAL: cover, blank verso, two-column problem pages (no key); the answer key
           is written to a separate PDF so the problem sheet never exposes answers.

Question blocks are never split across columns. Passage paragraphs may flow
line by line. Content is rendered exactly as given; this module never edits it.
"""
from __future__ import annotations

import hashlib
import html
import os
import re
from pathlib import Path
from typing import Any

import fitz

A4_W, A4_H = 595.276, 841.890
ML, MR, MT, MB = 46.0, 46.0, 64.0, 58.0
GUT = 20.0
COL_W = (A4_W - ML - MR - GUT) / 2
_ACTIVE_SUBJECT: str | None = None
_MIDDLE_KOREAN_RE = re.compile(r"[\u1100-\u11ff\u302e\u302f\u3165-\u318e\ua960-\ua97c\ud7b0-\ud7fb\ue000-\uf8ff]")
_SHAPED_JAMO_RE = re.compile(r"[\u1100-\u11ff\u302e\u302f\ua960-\ua97c\ud7b0-\ud7fb]")
_OPTIONAL_CENTERED_DOT: dict[str, Path] = {}


def _first_existing(candidates: list[Path]) -> Path:
    return next((p for p in candidates if p.is_file()), candidates[0])


def _resolve_font_files(subject: str | None = None) -> dict[str, Path]:
    subj = (subject if subject is not None else _ACTIVE_SUBJECT or "").upper()
    hancom_reg = [
        Path("C:/Windows/Fonts/HANDotum.ttf"),
        Path("C:/Program Files/Hancom/Office 2022/HOffice120/Shared/Fonts/Truetype/HANDotum.ttf"),
        Path("/usr/share/fonts/truetype/hancom/HANDotum.ttf"),
        Path.home() / ".local/share/fonts/hancom/HANDotum.ttf",
    ]
    hancom_bold = [
        Path("C:/Windows/Fonts/HANDotumB.ttf"),
        Path("C:/Program Files/Hancom/Office 2022/HOffice120/Shared/Fonts/Truetype/HANDotumB.ttf"),
        Path("/usr/share/fonts/truetype/hancom/HANDotumB.ttf"),
        Path.home() / ".local/share/fonts/hancom/HANDotumB.ttf",
    ]
    santteut_reg = [
        Path("C:/Windows/Fonts/HanSantteutDotum-Regular.ttf"),
        Path("C:/Program Files/Hancom/Office 2022/HOffice120/Shared/Fonts/Truetype/HanSantteutDotum-Regular.ttf"),
    ]
    santteut_bold = [
        Path("C:/Windows/Fonts/HanSantteutDotum-Bold.ttf"),
        Path("C:/Program Files/Hancom/Office 2022/HOffice120/Shared/Fonts/Truetype/HanSantteutDotum-Bold.ttf"),
    ]
    linux_reg = [
        Path("/usr/share/fonts/truetype/nanum/NanumGothic.ttf"),
        Path.home() / ".local/share/fonts/nanum/NanumGothic.ttf",
        Path("C:/Windows/Fonts/malgun.ttf"),
    ]
    linux_bold = [
        Path("/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"),
        Path.home() / ".local/share/fonts/nanum/NanumGothicBold.ttf",
        Path("C:/Windows/Fonts/malgunbd.ttf"),
    ]
    # KOR uses HCR Dotum (HANDotum R/B) so modern Korean and Middle Korean (옛한글·방점) share one typeface.
    if subj == "KOR":
        reg_candidates = [*hancom_reg, *santteut_reg, *linux_reg]
        bold_candidates = [*hancom_bold, *santteut_bold, *linux_bold]
    else:
        reg_candidates = [*santteut_reg, *linux_reg]
        bold_candidates = [*santteut_bold, *linux_bold]
    gb_candidates = [
        Path("C:/Windows/Fonts/KoPub Dotum Bold.ttf"),
        *bold_candidates,
    ]
    _OPTIONAL_CENTERED_DOT.clear()
    for dot_key, dot_cands in (("C", santteut_reg), ("CB", santteut_bold)):
        hit = next((p for p in dot_cands if p.is_file()), None)
        if hit is not None:
            _OPTIONAL_CENTERED_DOT[dot_key] = hit
    return {
        "R": _first_existing(reg_candidates),
        "B": _first_existing(bold_candidates),
        "G": _first_existing(reg_candidates),
        "GB": _first_existing(gb_candidates),
    }


FONT_FILES = _resolve_font_files()
# Hanja (漢字) and glyphs absent from body Gothic fall back to a CJK font; first existing file wins.
FALLBACK_FILES = [
    Path("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"),
    Path("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"),
    Path("/usr/share/fonts/truetype/arc-fallback/NotoSerifKR.ttf"),
    Path.home() / ".local/share/fonts/arc-fallback/NotoSerifKR.ttf",
    Path("C:/Windows/Fonts/HANDotum.ttf"),
    Path("C:/Program Files/Hancom/Office 2022/HOffice120/Shared/Fonts/Truetype/HANDotum.ttf"),
    Path("C:/Windows/Fonts/HANBatang.ttf"),
    Path("C:/Windows/Fonts/malgun.ttf"),
]
SIZE = 9.8   # default body size; a bundle `layout` key overrides it per render (see render())
LH = SIZE * 1.62
NAVY = (0.08, 0.16, 0.30)
BLACK = (0.0, 0.0, 0.0)
CIRC = "①②③④⑤"


class RenderError(RuntimeError):
    pass


def fallback_file() -> Path | None:
    return next((p for p in FALLBACK_FILES if p.is_file()), None)


def fonts() -> dict[str, fitz.Font]:
    global FONT_FILES
    FONT_FILES = _resolve_font_files()
    missing = [f"{k}:{p}" for k, p in FONT_FILES.items() if not p.is_file()]
    if missing:
        raise RenderError("KOREAN_FONT_MISSING: " + ", ".join(missing) + " (install fonts-nanum or Korean Gothic fonts)")
    out = {k: fitz.Font(fontfile=str(v)) for k, v in FONT_FILES.items()}
    for dk, dp in _OPTIONAL_CENTERED_DOT.items():
        out[dk] = fitz.Font(fontfile=str(dp))
    fb = fallback_file()
    if fb:
        out["H"] = fitz.Font(fontfile=str(fb))
    return out


_FONTS: dict[str, fitz.Font] | None = None

# Unicode super/subscripts (ion charges, formulas: A²⁺, CO₂) are drawn as small raised/lowered
# ordinary glyphs so they come from the body font instead of a wide CJK fallback.
SUPERSCRIPTS = dict(zip("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻", "0123456789+-"))
SUBSCRIPTS = dict(zip("₀₁₂₃₄₅₆₇₈₉₊₋", "0123456789+-"))
SCRIPT_SCALE = 0.62
SCRIPT_SHIFT = {"^": -0.36, "_": 0.14}  # baseline shift as a share of the font size
# ⟦…⟧ marks an underlined span (English exam underlines: ①⟦word⟧). Markers take no width and are never printed.
UL_OPEN, UL_CLOSE = "\u27e6", "\u27e7"


def base_key(key: str) -> str:
    return key.rstrip("^_~")


def run_size(key: str, size: float) -> float:
    return size * SCRIPT_SCALE if key[-1] in "^_" else size


def runs(text: str, key: str) -> list[tuple[str, str]]:
    """Split text into (font key, run) so every glyph comes from a font that has it.
    A glyph missing from both the Korean font and the CJK fallback is a hard error, never a tofu box."""
    global _FONTS
    if _FONTS is None:
        _FONTS = fonts()
    # Keep headings/tokens containing Middle Korean in one unified bold face (B) instead of mixing KoPub + HANDotum.
    if key == "GB" and _MIDDLE_KOREAN_RE.search(text):
        if all(c.isspace() or c in SUPERSCRIPTS or c in SUBSCRIPTS or c in (UL_OPEN, UL_CLOSE) or _FONTS["B"].has_glyph(ord(c)) for c in text):
            key = "B"
    out: list[tuple[str, str]] = []
    ul = ""
    for ch in text:
        if ch in (UL_OPEN, UL_CLOSE):
            ul = "~" if ch == UL_OPEN else ""
            continue
        k = key + ul
        if ch in SUPERSCRIPTS:
            ch, k = SUPERSCRIPTS[ch], key + ul + "^"
        elif ch in SUBSCRIPTS:
            ch, k = SUBSCRIPTS[ch], key + ul + "_"
        elif ch == "\u318d":
            ck = "CB" if key in ("B", "GB") else "C"
            if ck in _FONTS and _FONTS[ck].has_glyph(0x318D):
                k = ck + ul
        elif not ch.isspace() and not _FONTS[key].has_glyph(ord(ch)):
            if key in ("GB", "B") and "B" in _FONTS and _FONTS["B"].has_glyph(ord(ch)):
                k = "B" + ul
            elif "H" in _FONTS and _FONTS["H"].has_glyph(ord(ch)):
                k = "H" + ul
            else:
                raise RenderError(f"GLYPH_MISSING: U+{ord(ch):04X} {ch!r} (install fonts-noto-cjk or fonts-wqy-zenhei)")
        if out and out[-1][0] == k:
            out[-1] = (k, out[-1][1] + ch)
        else:
            out.append((k, ch))
    return out


def _insert_shaped_run(page: fitz.Page, x: float, y: float, text: str, font_path: Path, size: float, color) -> None:
    rgb = "rgb(0,0,0)" if color is None else f"rgb({int(round(color[0]*255))},{int(round(color[1]*255))},{int(round(color[2]*255))})"
    css = (
        f'@font-face{{font-family:ArcMK;src:url("{font_path.as_posix()}");}}'
        f"body{{font-family:ArcMK;font-size:{size}pt;line-height:1;margin:0;padding:0;color:{rgb};white-space:pre;}}"
    )
    rect = fitz.Rect(x, y - 0.80 * size, x + 800.0, y + 0.60 * size)
    page.insert_htmlbox(rect, f"<span>{html.escape(text)}</span>", css=css)


def put(page: fitz.Page, pos, text: str, fontname: str = "R", fontsize: float | None = None, color=None) -> None:
    fontsize = SIZE if fontsize is None else fontsize
    x, y = pos
    for rk, t in runs(text, fontname):
        k, size = base_key(rk), run_size(rk, fontsize)
        fp = FONT_FILES.get(k) or _OPTIONAL_CENTERED_DOT.get(k) or fallback_file()
        dy = SCRIPT_SHIFT.get(rk[-1], 0.0) * fontsize
        if _SHAPED_JAMO_RE.search(t) and fp is not None:
            _insert_shaped_run(page, x, y + dy, t, fp, size, color)
        else:
            if k not in {f[4] for f in page.get_fonts()}:  # embed only fonts a page actually uses (unused fonts are not subset)
                page.insert_font(fontname=k, fontfile=str(fp))
            kw = {"color": color} if color is not None else {}
            page.insert_text((x, y + dy), t, fontname=k, fontsize=size, **kw)
        adv = _FONTS[k].text_length(t, fontsize=size)
        if "~" in rk:
            page.draw_line((x, y + 1.6), (x + adv, y + 1.6), width=0.55)
        x += adv


class Layout:
    def __init__(self) -> None:
        self.f = fonts()

    def width(self, text: str, key: str = "R", size: float | None = None) -> float:
        size = SIZE if size is None else size
        return sum(self.f[base_key(k)].text_length(t, fontsize=run_size(k, size)) for k, t in runs(text, key))

    def wrap(self, text: str, w: float, key: str = "R", size: float | None = None, first: float = 0.0, rest: float = 0.0):
        size = SIZE if size is None else size
        """Greedy wrap on spaces (어절); char break only for tokens wider than the line."""
        lines, cur, indent = [], "", first
        text = re.sub(r"\( (\S{1,3}) \)", "(\u00a0\\1\u00a0)", text).replace("( )", "(\u00a0)")  # keep blanks on one line
        for word in text.split(" "):
            trial = word if not cur else cur + " " + word
            if self.width(trial, key, size) <= w - indent:
                cur = trial
                continue
            if cur:
                lines.append((indent, cur))
                indent, cur = rest, ""
            while self.width(word, key, size) > w - indent:
                cut = len(word)
                while cut > 1 and self.width(word[:cut], key, size) > w - indent:
                    cut -= 1
                lines.append((indent, word[:cut]))
                indent, word = rest, word[cut:]
            cur = word
        if cur:
            lines.append((indent, cur))
        out, carry = [], False  # an underline span that crosses a line break is closed and reopened
        for i, t in lines:
            t = (UL_OPEN if carry else "") + t.replace("\u00a0", " ")
            carry = t.rfind(UL_OPEN) > t.rfind(UL_CLOSE)
            out.append((i, t + (UL_CLOSE if carry else "")))
        return out


class Block:
    def __init__(self, splittable: bool = False) -> None:
        self.ops: list[tuple] = []
        self.h = 0.0
        self.splittable = splittable

    def text(self, lines, key="R", size=None, lh=None, dx=0.0):
        size = SIZE if size is None else size
        lh = LH if lh is None else lh
        for indent, t in lines:
            self.ops.append(("text", dx + indent, self.h + size, t, key, size))
            self.h += lh


def set_blocks(L: Layout, bundle: dict[str, Any], src: dict[str, Any], labels: dict[str, str], set_header) -> list[Block]:
    blocks: list[Block] = []
    head = Block()
    head.text(L.wrap(set_header(bundle, src["id"], labels), COL_W, "B"), key="B")
    head.h += 6
    blocks.append(head)
    if src.get("lead"):  # e.g. [앞부분의 줄거리] printed before the passage
        lb = Block()
        for line in src["lead"]:
            lb.text(L.wrap(line, COL_W, size=SIZE - 0.8, first=0, rest=0), size=SIZE - 0.8, lh=(SIZE - 0.8) * 1.55)
        lb.h += 8
        blocks.append(lb)
    for w in src["works"]:
        if w.get("label"):
            lab = Block()
            lab.text([(0, w["label"])], key="B")
            blocks.append(lab)
        if w["form"] == "VERSE":
            every = w.get("line_numbers") or 0
            num_w = L.width("00", size=SIZE - 2) + 6 if every else 0
            n = 0
            for unit in w["display"]:
                b = Block(splittable=True)
                if unit.strip():
                    n += 1
                    if every and n % every == 0:
                        t = str(n)
                        b.ops.append(("text", COL_W - L.width(t, size=SIZE - 2), SIZE, t, "R", SIZE - 2))
                    b.text(L.wrap(unit, COL_W - num_w, first=0, rest=SIZE * 1.5))
                else:
                    b.h += LH * 0.6
                blocks.append(b)
        else:
            for para in w["display"]:
                b = Block(splittable=True)
                b.text(L.wrap(para, COL_W, first=SIZE))
                b.h += 2
                blocks.append(b)
        if w.get("table") or w.get("figure"):  # material sets (SOC/SCI): shared table / figure
            mb = Block()
            if w.get("table"):
                table(L, mb, w["table"])
            if w.get("figure"):
                figure(L, mb, w["figure"])
            blocks.append(mb)
        if w.get("title"):
            src_b = Block()
            small = SIZE - 0.6
            for _, t in L.wrap(f"― {w['title']} ―", COL_W, size=small):
                src_b.ops.append(("text", COL_W - L.width(t, size=small), src_b.h + SIZE, t, "R", small))
                src_b.h += LH
            src_b.h += 8
            blocks.append(src_b)
        else:
            gap = Block()
            gap.h = 8
            blocks.append(gap)
    if src.get("notes"):
        nb = Block()
        for note in src["notes"]:
            nb.text(L.wrap(note, COL_W, size=SIZE - 1.2, rest=SIZE), size=SIZE - 1.2, lh=(SIZE - 1.2) * 1.5)
        nb.h += 10
        blocks.append(nb)
    return blocks


def build_blocks(L: Layout, bundle: dict[str, Any], sources: list[dict[str, Any]], labels: dict[str, str], set_header) -> list[Block]:
    """Bundle item order; a set's passage/material is printed once, before its first item."""
    by_id = {s["id"]: s for s in sources}
    blocks: list[Block] = []
    seen: set[str] = set()
    for it in bundle["items"]:
        sid = it.get("set")
        if sid is None:
            blocks.append(question_block(L, it, labels[it["item_id"]], bundle["product_mode"]))
        elif sid not in seen:
            seen.add(sid)
            blocks += set_blocks(L, bundle, by_id[sid], labels, set_header)
            for x in [x for x in bundle["items"] if x.get("set") == sid]:
                blocks.append(question_block(L, x, labels[x["item_id"]], bundle["product_mode"]))
    return blocks


def _diff_badge(it: dict[str, Any]) -> str:
    """Format difficulty badge without triggering STUDENT_METADATA_LEAK ('D1'..'D5')."""
    d = str(it.get("difficulty", "")).strip().upper()
    if d.startswith("D") and d[1:].isdigit():
        return f" [{d[1:]}]"
    return ""


def question_block(L: Layout, it: dict[str, Any], label: str, product: str = "ARC_N") -> Block:
    b = Block()
    pts = f" ({it['points']}점)" if it.get("points") else ""
    badge = _diff_badge(it)
    if it.get("format") == "CR":
        num = f"[{label}] "
    elif product == "ARC_FINAL":
        num = f"{label}. "
    else:
        num = f"{int(label):02d} "
    nw = L.width(num, "B")
    tag = f"[{it['source_label']}] " if it.get("source_label") else ""  # 어느 지문의 문제인지
    stem = L.wrap(tag + it["stem"] + pts + badge, COL_W, "B", first=nw, rest=nw)
    stem[0] = (0, num + stem[0][1])
    b.text(stem, key="B")
    b.h += 4
    for para in it.get("passage", []):  # item-own passage (English variants: each item reworks the text)
        b.text(L.wrap(para, COL_W, first=SIZE))
        b.h += 2
    if it.get("passage"):
        b.h += 4
    if it.get("figure"):
        figure(L, b, it["figure"])
    if it.get("table"):
        table(L, b, it["table"])
    if it.get("view"):
        view(L, b, it["view"], label=it.get("view_label", "<보 기>"))
    if it.get("format") == "CR":
        view(L, b, it["conditions"], label="<조 건>")
        top = b.h
        b.h += LH * 3.2
        b.ops.append(("text", 2, top + SIZE + 2, "답:", "GB", SIZE - 0.6))
        for k in (1.1, 2.1, 3.1):
            ry = top + LH * k
            b.ops.append(("line", 0, ry, COL_W, ry, 0.45))
        b.h += 20
        return b
    labels_ = [o if o == CIRC[i] else f"{CIRC[i]} {o}" for i, o in enumerate(it["options"])]  # bare ①~⑤ for underline items
    widest = max(L.width(t) for t in labels_)
    if widest <= COL_W / 5 - 4:
        for i, t in enumerate(labels_):
            b.ops.append(("text", i * COL_W / 5, b.h + SIZE, t, "R", SIZE))
        b.h += LH
    elif widest <= COL_W / 3 - 4:
        for i, t in enumerate(labels_):
            if i == 3:
                b.h += LH
            b.ops.append(("text", (i % 3) * COL_W / 3, b.h + SIZE, t, "R", SIZE))
        b.h += LH
    else:
        hang = L.width("① ")
        for t in labels_:
            b.text(L.wrap(t, COL_W, rest=hang))
            b.h += 1.5
    b.h += 22
    return b


def figure(L: Layout, b: Block, fig: dict[str, Any]) -> None:
    """Place a hash-bound image at column width (or `width` share of it), keeping its aspect ratio."""
    path = fig.get("abs_path") or fig["path"]
    pix = fitz.Pixmap(str(path))
    share = min(1.0, max(0.3, float(fig.get("width", 0.9))))
    w = COL_W * share
    h = w * pix.height / pix.width
    x0 = (COL_W - w) / 2
    b.h += 2
    b.ops.append(("image", x0, b.h, x0 + w, b.h + h, str(path)))
    b.h += h + 6


def view(L: Layout, b: Block, lines: list[str], label: str = "<보 기>") -> None:
    pad, top = 7.0, b.h
    b.h += pad + 3
    for s in lines:
        hang = L.width("ㄱ. ") if len(s) > 2 and s[1] == "." else 0.0
        if s.startswith("|") and s.endswith("|"):
            s = "  ".join(c.strip() for c in s.strip("|").split("|"))
        b.text(L.wrap(s, COL_W - 2 * pad, rest=hang), dx=pad)
        b.h += 1
    b.h += pad - 2
    b.ops.append(("rect", 0, top + 4, COL_W, b.h))
    if label:  # an unlabelled box (English given sentence / summary) keeps its border closed
        lw = L.width(label, "B")
        b.ops.append(("label", COL_W / 2 - lw / 2, top + 4, label, lw))
    b.h += 6


def table(L: Layout, b: Block, tbl: dict[str, Any]) -> None:
    ncol = len(tbl["header"])
    weights = tbl.get("weights") or ([0.28, 0.33, 0.39] if ncol == 3 else [1 / ncol] * ncol)
    cw = [COL_W * w for w in weights]
    pad, size = 3.0, SIZE - 0.8
    lh = size * 1.45
    rows = [tbl["header"]] + tbl["rows"]
    y = b.h + 2
    b.ops.append(("line", 0, y, COL_W, y, 1.1))
    for ri, row in enumerate(rows):
        key = "GB" if ri == 0 else "R"
        wrapped = [L.wrap(cell, cw[i] - 2 * pad, key, size) for i, cell in enumerate(row)]
        rh = max(len(w) for w in wrapped) * lh + 2 * pad
        if ri == 0:
            b.ops.append(("fill_rect", 0, y, COL_W, y + rh, (0.90, 0.90, 0.90)))
        x = 0.0
        for i, w in enumerate(wrapped):
            yy = y + pad
            for _, t in w:
                b.ops.append(("text", x + pad, yy + size, t, key, size))
                yy += lh
            x += cw[i]
        y += rh
        b.ops.append(("line", 0, y, COL_W, y, 0.7 if ri in (0, len(rows) - 1) else 0.4))
    x = 0.0
    for i in range(1, ncol):
        x += cw[i - 1]
        b.ops.append(("line", x, b.h + 2, x, y, 0.4))
    b.h = y + 8


def paint(page: fitz.Page, ops, x: float, y: float) -> None:
    labels = []
    for op in ops:
        kind = op[0]
        if kind == "fill_rect":
            _, x0, y0, x1, y1, fill_c = op
            page.draw_rect(fitz.Rect(x + x0, y + y0, x + x1, y + y1), color=None, fill=fill_c)
        elif kind == "text":
            _, dx, dy, t, key, size = op
            put(page, (x + dx, y + dy), t, fontname=key, fontsize=size)
        elif kind == "rect":
            _, x0, y0, x1, y1 = op
            page.draw_rect(fitz.Rect(x + x0, y + y0, x + x1, y + y1), color=(0.13, 0.13, 0.13), width=0.55)
        elif kind == "line":
            _, x0, y0, x1, y1, w = op
            lc = (0.65, 0.65, 0.65) if w <= 0.45 else (0.10, 0.10, 0.10)
            page.draw_line((x + x0, y + y0), (x + x1, y + y1), color=lc, width=w)
        elif kind == "image":
            _, x0, y0, x1, y1, path = op
            page.insert_image(fitz.Rect(x + x0, y + y0, x + x1, y + y1), filename=path, keep_proportion=True)
        elif kind == "label":
            labels.append(op)
    for _, lx, ly, t, lw in labels:  # Canva solid black pill tab centered on top border
        pill_rect = fitz.Rect(x + lx - 8, y + ly - 6.0, x + lx + lw + 8, y + ly + 5.5)
        page.draw_rect(pill_rect, color=BLACK, fill=BLACK)
        put(page, (x + lx + 1.0, y + ly + 3.0), t, fontname="GB", fontsize=SIZE - 0.4, color=(1, 1, 1))


def new_page(doc: fitz.Document) -> fitz.Page:
    return doc.new_page(width=A4_W, height=A4_H)  # fonts are embedded by put() only where used


def problem_page(doc, L: Layout, header: str, number: int, product: str = "ARC_N",
                 meta: dict[str, Any] | None = None) -> tuple[fitz.Page, float]:
    page = new_page(doc)
    top_y = MT
    if product == "ARC_FINAL" and number == 3 and meta:
        # Authentic Dongbuk High School exam header block inside the top header band (y < 58pt)
        school_hdr = f"2026학년도 2학기 기말고사  |  동북고등학교  |  {meta.get('course', '')}"
        put(page, (ML, 30), school_hdr, fontname="GB", fontsize=10.5, color=BLACK)
        right_hdr = f"{meta.get('set_label', 'ARC FINAL')} · 배점 문항별 표시"
        put(page, (A4_W - MR - L.width(right_hdr, "G", 8.4), 30), right_hdr, fontname="G", fontsize=8.4, color=BLACK)
        box = fitz.Rect(ML, 36, A4_W - MR, 52)
        page.draw_rect(box, color=BLACK, width=0.8)
        mid_x = A4_W / 2
        page.draw_line((mid_x, 36), (mid_x, 52), color=BLACK, width=0.6)
        put(page, (ML + 8, 47), "대상: 동북고등학교 1학년", fontname="G", fontsize=8.2, color=BLACK)
        put(page, (mid_x + 8, 47), f"범위: {str(meta.get('scope', ''))[:26]}", fontname="G", fontsize=8.2, color=BLACK)
        page.draw_line((ML, 55), (A4_W - MR, 55), color=BLACK, width=1.1)
        top_y = MT + 6.0
    else:
        put(page, (ML, 38), header, fontname="GB", fontsize=8.5, color=BLACK)
        code = str((meta or {}).get("batch_id", ""))
        if code:
            cw = L.width(code, "G", 7.8)
            put(page, (A4_W - MR - cw, 38), code, fontname="G", fontsize=7.8, color=(0.40, 0.40, 0.40))
        page.draw_line((ML, 46), (A4_W - MR, 46), color=BLACK, width=0.7)
    mid = ML + COL_W + GUT / 2
    page.draw_line((mid, top_y - 4), (mid, A4_H - MB + 6), color=(0.76, 0.76, 0.76), width=0.55)
    page.draw_line((ML, A4_H - MB + 12), (A4_W - MR, A4_H - MB + 12), color=(0.72, 0.72, 0.72), width=0.55)
    s = f"- {number} -" if product == "ARC_FINAL" else str(number)
    if product == "ARC_FINAL":
        put(page, (A4_W / 2 - L.width(s, "GB", 8.8) / 2, A4_H - 28), s, fontname="GB", fontsize=8.8, color=BLACK)
    else:
        put(page, (ML, A4_H - 28), "ARC-System Editorial Division", fontname="G", fontsize=7.6, color=(0.35, 0.35, 0.35))
        sw = L.width(s, "GB", 8.8)
        put(page, (A4_W - MR - sw, A4_H - 28), s, fontname="GB", fontsize=8.8, color=BLACK)
    return page, top_y


def cover(doc, meta: dict[str, Any], logo: dict[str, Any] | None) -> str:
    page = new_page(doc)
    product = meta.get("product_mode", "ARC_N")
    school = str(meta.get("school_line") or "동북고등학교")
    if "동북고" not in school:
        school = f"동북고등학교  |  {school}"

    # Top editorial accent rule & kicker
    page.draw_line((ML, 52), (A4_W - MR, 52), color=BLACK, width=2.0)
    put(page, (ML, 72), f"ARC SYSTEM  ·  {school}", fontname="GB", fontsize=9.0, color=BLACK)

    brand = "BRAND_ASSET_MISSING"
    top = 104.0
    if logo and Path(logo["path"]).is_file():
        data = Path(logo["path"]).read_bytes()
        if hashlib.sha256(data).hexdigest() != logo["sha256"]:
            raise RenderError("BRAND_HASH_MISMATCH")
        w, h = logo["pixels"]
        box_w = 155.0
        img_h = box_w * h / w
        page.insert_image(fitz.Rect(ML, 84, ML + box_w, 84 + img_h), stream=data, keep_proportion=True)
        brand, top = "PASS", 84 + img_h + 28

    # Canva Editorial Modern Gothic Hero Block (4.2pt left accent bar + 3-line Gothic typography)
    page.draw_rect(fitz.Rect(ML, top, ML + 4.2, top + 92), color=None, fill=BLACK)
    put(page, (ML + 16, top + 24), str(meta.get("set_label", "")), fontname="GB", fontsize=26, color=BLACK)
    put(page, (ML + 16, top + 56), str(meta.get("course", "")), fontname="GB", fontsize=19, color=BLACK)
    if meta.get("cover_subtitle"):
        put(page, (ML + 16, top + 82), str(meta["cover_subtitle"]), fontname="G", fontsize=11.5, color=(0.20, 0.20, 0.20))

    # Pills Row (minimalist: no passage titles or cover_lines leaked onto ARC_N cover)
    py = top + 108
    mode_lbl = "ARC N° SERIES" if product == "ARC_N" else "ARC FINAL"
    page.draw_rect(fitz.Rect(ML, py, ML + 112, py + 20), color=None, fill=BLACK)
    put(page, (ML + 12, py + 13), mode_lbl, fontname="GB", fontsize=8.2, color=(1, 1, 1))
    item_cnt = len(meta.get("items", []))
    page.draw_rect(fitz.Rect(ML + 120, py, ML + 260, py + 20), color=BLACK, width=0.8)
    put(page, (ML + 132, py + 13), f"문항 수: {item_cnt}문항", fontname="GB", fontsize=8.2, color=BLACK)

    # Borderless soft-gray editorial notice card (static boilerplate only; no curriculum topics)
    cy = py + 38
    page.draw_rect(fitz.Rect(ML, cy, A4_W - MR, cy + 118), color=None, fill=(0.945, 0.945, 0.945))
    put(page, (ML + 16, cy + 22), "일러두기", fontname="GB", fontsize=9.8, color=BLACK)
    page.draw_line((ML + 16, cy + 30), (A4_W - MR - 16, cy + 30), color=(0.80, 0.80, 0.80), width=0.5)
    notices = (
        "문항을 순서대로 풀고 OMR 또는 답안 표기란에 정답을 정확히 기입하십시오.",
        "서답형 문항은 <조건>을 확인한 뒤 핵심 근거를 빠짐없이 서술하십시오.",
        "풀이 후 뒷면의 빠른 정답표 및 별도 해설지로 오답을 점검하십시오.",
    )
    for ni, note in enumerate(notices):
        ny = cy + 48 + ni * 22
        page.draw_rect(fitz.Rect(ML + 16, ny - 5.5, ML + 19.5, ny - 2.0), color=None, fill=BLACK)
        put(page, (ML + 26, ny), note, fontname="R", fontsize=8.5, color=BLACK)

    # Bottom 3-cell Editorial Metadata Grid
    fy0, fy1 = 736.0, 782.0
    page.draw_line((ML, fy0), (A4_W - MR, fy0), color=BLACK, width=1.4)
    page.draw_line((ML, fy1), (A4_W - MR, fy1), color=BLACK, width=0.7)
    gw = A4_W - ML - MR
    cols = [
        ("DOCUMENT CODE", str(meta.get("batch_id", "ARC"))[:22]),
        ("INSTITUTION", school[:24]),
        ("EDITION MODE", "ARC N° STANDARD" if product == "ARC_N" else "ARC FINAL EXAM"),
    ]
    cw = gw / len(cols)
    for ci, (k_lbl, v_lbl) in enumerate(cols):
        cx0 = ML + ci * cw
        if ci > 0:
            page.draw_line((cx0, fy0), (cx0, fy1), color=(0.80, 0.80, 0.80), width=0.5)
        put(page, (cx0 + 8, fy0 + 16), k_lbl, fontname="G", fontsize=7.5, color=(0.38, 0.38, 0.38))
        put(page, (cx0 + 8, fy0 + 34), v_lbl, fontname="GB", fontsize=8.8, color=BLACK)
    return brand


def answer_page(doc, items: list[dict[str, Any]], labels: dict[str, str] | None = None, product: str = "ARC_N") -> None:
    L = Layout()
    key = new_page(doc)
    put(key, (ML, 76), "정답  ANSWER KEY", fontname="GB", fontsize=18, color=BLACK)
    key.draw_line((ML, 92), (A4_W - MR, 92), color=BLACK, width=1.5)
    mcq = [it for it in items if it.get("format", "MCQ") == "MCQ"]
    per_col, col_w, row_h = (10 if len(mcq) <= 30 else 15), 130, 28
    fsize = 12.5
    if len(mcq) > 60:  # long workbooks (e.g. 140-item passage sets): narrower columns, one page up to 7 x 27
        col_w, row_h, fsize = 72, 24, 10.5
        cols = int((A4_W - ML - MR - 20) // col_w)
        per_col = -(-len(mcq) // cols)
        if per_col > 27:
            raise RenderError(f"ANSWER_KEY_TOO_LONG: {len(mcq)} items")
    if mcq:
        num_cols = max(1, (len(mcq) + per_col - 1) // per_col)
        grid_right = min(A4_W - MR, ML + num_cols * col_w + 10)
        for r in range(per_col):
            ry = 114 + r * row_h
            if r % 2 == 0 and len(mcq) <= 60:
                key.draw_rect(fitz.Rect(ML, ry, grid_right, ry + row_h), color=None, fill=(0.955, 0.955, 0.955))
            key.draw_line((ML, ry + row_h), (grid_right, ry + row_h), color=(0.82, 0.82, 0.82), width=0.4)
        key.draw_line((ML, 114), (grid_right, 114), color=BLACK, width=1.1)
        key.draw_line((ML, 114 + per_col * row_h), (grid_right, 114 + per_col * row_h), color=BLACK, width=1.2)
    for i, it in enumerate(mcq):
        x = ML + 14 + (i // per_col) * col_w
        y = 132 + (i % per_col) * row_h
        num = f"{i + 1:02d}" if product == "ARC_N" else f"{i + 1}"
        put(key, (x, y), f"{num}  {CIRC[it['answer'] - 1]}", fontname="GB", fontsize=fsize, color=BLACK)
    crs = [it for it in items if it.get("format") == "CR"]
    if not crs:
        return
    y = 132 + per_col * row_h + 22
    page = key
    width = A4_W - ML - MR
    for it in crs:
        chunks = [("GB", f"[{labels[it['item_id']] if labels else it['item_id']}] 모범답안 ({it.get('points', '')}점)")]
        chunks += [("R", "답: " + it["model_answer"])]
        chunks += [("G", "채점 기준: " + r) for r in it.get("rubric", [])]
        if it.get("accepted_variants"):
            chunks.append(("G", "유사 정답: " + " / ".join(it["accepted_variants"])))
        wrapped: list[tuple[str, str]] = []
        for key_font, text in chunks:
            for _, line in L.wrap(text, width - 22, key_font, 10.0):
                wrapped.append((key_font, line))
        card_h = len(wrapped) * 15.0 + 16
        if y + card_h > A4_H - MB and y > 130:
            page = new_page(doc)
            y = 72
        page.draw_rect(fitz.Rect(ML, y, A4_W - MR, y + card_h), color=None, fill=(0.955, 0.955, 0.955))
        page.draw_rect(fitz.Rect(ML, y, ML + 3.0, y + card_h), color=None, fill=BLACK)
        cy = y + 18
        for key_font, line in wrapped:
            if cy > A4_H - MB:
                page = new_page(doc)
                cy = 72
            put(page, (ML + 12, cy), line, fontname=key_font, fontsize=10.0, color=BLACK)
            cy += 15.0
        y += card_h + 10


def render_solutions(bundle: dict[str, Any], labels: dict[str, str], out_pdf: Path) -> dict[str, Any]:
    """Render a dedicated B&W 2-column Canva Modern Gothic solutions booklet PDF (*_SOLUTIONS.pdf)."""
    global _ACTIVE_SUBJECT, _FONTS
    saved_subj = _ACTIVE_SUBJECT
    subj = (bundle.get("subject") or "").upper() or None
    if subj != _ACTIVE_SUBJECT:
        _ACTIVE_SUBJECT = subj
        _FONTS = None
    try:
        return _render_solutions_inner(bundle, labels, out_pdf)
    finally:
        if _ACTIVE_SUBJECT != saved_subj:
            _ACTIVE_SUBJECT = saved_subj
            _FONTS = None


def _render_solutions_inner(bundle: dict[str, Any], labels: dict[str, str], out_pdf: Path) -> dict[str, Any]:
    L = Layout()
    doc = fitz.open()
    sol_col_w = COL_W
    sol_top_first = 98.0
    sol_top_next = MT
    sol_bottom = A4_H - MB
    pno = 1

    def open_sol_page(first: bool = False) -> tuple[fitz.Page, float]:
        nonlocal pno
        p = new_page(doc)
        if first:
            put(p, (ML, 54), f"{bundle.get('set_label', '')}  {bundle.get('course', '')} — 정답 및 상세 해설", fontname="GB", fontsize=15.0, color=BLACK)
            put(p, (ML, 72), f"동북고등학교  |  범위: {bundle.get('scope', '')}", fontname="G", fontsize=9.0, color=(0.25, 0.25, 0.25))
            p.draw_line((ML, 82), (A4_W - MR, 82), color=BLACK, width=1.1)
            y0 = sol_top_first
        else:
            put(p, (ML, 38), f"{bundle.get('set_label', '')}  정답 및 상세 해설", fontname="GB", fontsize=8.5, color=BLACK)
            rw = L.width("DETAILED SOLUTIONS", "G", 7.8)
            put(p, (A4_W - MR - rw, 38), "DETAILED SOLUTIONS", fontname="G", fontsize=7.8, color=(0.40, 0.40, 0.40))
            p.draw_line((ML, 46), (A4_W - MR, 46), color=BLACK, width=0.7)
            y0 = sol_top_next
        mid = ML + sol_col_w + GUT / 2
        p.draw_line((mid, y0 - 4), (mid, A4_H - MB + 6), color=(0.76, 0.76, 0.76), width=0.55)
        p.draw_line((ML, A4_H - MB + 12), (A4_W - MR, A4_H - MB + 12), color=(0.72, 0.72, 0.72), width=0.55)
        put(p, (ML, A4_H - 28), "ARC-System Editorial Division", fontname="G", fontsize=7.6, color=(0.35, 0.35, 0.35))
        s = str(pno)
        put(p, (A4_W - MR - L.width(s, "GB", 8.8), A4_H - 28), s, fontname="GB", fontsize=8.8, color=BLACK)
        pno += 1
        return p, y0

    page, col_top = open_sol_page(first=True)
    col, y = 0, col_top

    def advance_col() -> None:
        nonlocal page, col_top, col, y
        if col == 0:
            col, y = 1, col_top
        else:
            page, col_top = open_sol_page(first=False)
            col, y = 0, col_top

    for it in bundle["items"]:
        lbl = labels.get(it["item_id"], it["item_id"])
        diff = it.get("difficulty", "")
        arch = it.get("archetype") or it.get("family", "")
        if it.get("format") == "CR":
            header_line = f"[{lbl}]  서답형 해설  ({it.get('points', '')}점)" + (f"  [{diff}]" if diff else "")
            lines_to_draw: list[tuple[str, float, str]] = [("GB", 9.8, header_line)]
            lines_to_draw.append(("R", 8.8, f"발문: {it['stem']}"))
            lines_to_draw.append(("GB", 8.8, f"모범 답안: {it.get('model_answer', '')}"))
            for r in it.get("rubric", []):
                lines_to_draw.append(("G", 8.5, f"• 채점 기준: {r}"))
        else:
            ans = int(it["answer"])
            sb = int(it.get("second_best", 0) or 0)
            header_line = f"{int(lbl):02d}번  정답 {CIRC[ans - 1]}   [{diff} · {arch}]"
            lines_to_draw = [("GB", 9.8, header_line)]
            for idx, (opt, j) in enumerate(zip(it.get("options", []), it.get("judgments", [])), 1):
                tag = " [정답]" if idx == ans else (" [2순위]" if idx == sb else "")
                verdict = j.get("v", "")
                why = j.get("why", "")
                font_k = "B" if idx == ans else "R"
                lines_to_draw.append((font_k, 8.7, f"{CIRC[idx - 1]} {opt}{tag} ({verdict}) — {why}"))

        wrapped_rows: list[tuple[str, float, float, str, bool]] = []
        for li, (fk, fsz, raw_line) in enumerate(lines_to_draw):
            hang = L.width("① ", fk, fsz) if raw_line[:1] in CIRC else 0.0
            avail = sol_col_w - (10.0 if li == 0 else 0.0)
            for indent, wline in L.wrap(raw_line, avail, fk, fsz, first=0.0, rest=hang):
                wrapped_rows.append((fk, fsz, indent + (7.0 if li == 0 else 0.0), wline, li == 0))

        row_step = 13.4
        hdr_rows = sum(1 for r in wrapped_rows if r[4])
        block_h = len(wrapped_rows) * row_step + 14.0
        if y + block_h > sol_bottom and y > col_top + 8:
            advance_col()

        x_col = ML + col * (sol_col_w + GUT)
        if hdr_rows:
            page.draw_rect(fitz.Rect(x_col, y, x_col + sol_col_w, y + hdr_rows * row_step + 4), color=None, fill=(0.935, 0.935, 0.935))
            page.draw_rect(fitz.Rect(x_col, y, x_col + 2.5, y + hdr_rows * row_step + 4), color=None, fill=BLACK)
            y += 2.0

        for ri, (fk, fsz, indent, wline, is_hdr) in enumerate(wrapped_rows):
            if y + row_step > sol_bottom:
                advance_col()
                x_col = ML + col * (sol_col_w + GUT)
            put(page, (x_col + indent, y + fsz + 1), wline, fontname=fk, fontsize=fsz, color=BLACK)
            y += row_step
            if is_hdr and (ri + 1 == len(wrapped_rows) or not wrapped_rows[ri + 1][4]):
                y += 4.0
        page.draw_line((x_col, y + 2), (x_col + sol_col_w, y + 2), color=(0.82, 0.82, 0.82), width=0.4)
        y += 9.0

    doc.subset_fonts()
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_pdf, garbage=4, deflate=True)
    pages = len(doc)
    doc.close()
    return {"status": "PASS", "pages": pages, "pdf": str(out_pdf)}


def render(bundle: dict[str, Any], sources: list[dict[str, Any]], labels: dict[str, str], set_header,
           out_pdf: Path, key_pdf: Path | None = None, logo: dict[str, Any] | None = None,
           solutions_pdf: Path | None = None) -> dict[str, Any]:
    global SIZE, LH, _ACTIVE_SUBJECT, _FONTS
    saved = (SIZE, LH)
    saved_subj = _ACTIVE_SUBJECT
    subj = (bundle.get("subject") or "").upper() or None
    if subj != _ACTIVE_SUBJECT:
        _ACTIVE_SUBJECT = subj
        _FONTS = None
    lay = bundle.get("layout") or {}
    if lay.get("body_pt"):  # per-bundle body size / line height (English passage workbooks)
        SIZE = float(lay["body_pt"])
        LH = SIZE * float(lay.get("line_height_ratio", 1.62))
    try:
        return _render(bundle, sources, labels, set_header, out_pdf, key_pdf, logo, solutions_pdf)
    finally:
        SIZE, LH = saved
        if _ACTIVE_SUBJECT != saved_subj:
            _ACTIVE_SUBJECT = saved_subj
            _FONTS = None


def _render(bundle: dict[str, Any], sources: list[dict[str, Any]], labels: dict[str, str], set_header,
            out_pdf: Path, key_pdf: Path | None = None, logo: dict[str, Any] | None = None,
            solutions_pdf: Path | None = None) -> dict[str, Any]:
    product = bundle["product_mode"]
    items = bundle["items"]
    L = Layout()
    doc = fitz.open()
    titles = list(bundle.get("cover_lines") or [w["title"] for src in sources for w in src["works"] if w.get("title")])
    meta = dict(bundle, passage_titles=titles)
    brand = cover(doc, meta, logo)
    doc.new_page(width=A4_W, height=A4_H)  # blank verso
    header = f"{bundle['set_label']}  {bundle['course']}"
    pno = 3
    page, col_top = problem_page(doc, L, header, pno, product=product, meta=meta)
    col, y, bottom = 0, col_top, A4_H - MB
    col_q_count = 0

    def advance():
        nonlocal col, y, page, pno, col_top, col_q_count
        if col == 0:
            col, y, col_q_count = 1, col_top, 0
        else:
            pno += 1
            page, col_top = problem_page(doc, L, header, pno, product=product, meta=meta)
            col, y, col_q_count = 0, col_top, 0

    for b in build_blocks(L, bundle, sources, labels, set_header):
        is_question = not b.splittable and any(
            op[0] == "text" and op[4] == "B" and (op[3][:2].isdigit() or op[3].startswith("[") or (len(op[3]) > 1 and op[3][0].isdigit() and op[3][1] in "0123456789."))
            for op in b.ops[:1]
        )
        # Target 2 standalone questions per column (4 per page) on ARC_N when no shared passage precedes
        if product == "ARC_N" and is_question and col_q_count >= 2 and not bundle.get("sets"):
            advance()
        if b.splittable and y + b.h > bottom:
            rows: dict[float, list[tuple]] = {}
            for op in b.ops:  # ops sharing a baseline (a verse line and its margin number) stay on one row
                rows.setdefault(op[2], []).append(op)
            for row in rows.values():
                if y + LH > bottom:
                    advance()
                x = ML + col * (COL_W + GUT)
                base = y + max(op[5] for op in row)
                for op in row:
                    put(page, (x + op[1], base), op[3], fontname=op[4], fontsize=op[5])
                y += LH
            y += 2
            continue
        if y + b.h > bottom:
            advance()
            if b.h > bottom - col_top:
                raise RenderError(f"QUESTION_BLOCK_TALLER_THAN_COLUMN: {b.h:.1f}pt")
        paint(page, b.ops, ML + col * (COL_W + GUT), y)
        y += b.h
        if is_question:
            col_q_count += 1

    if product == "ARC_N":
        doc.new_page(width=A4_W, height=A4_H)  # blank separator
        answer_page(doc, items, labels, product)
    elif key_pdf is not None:
        kdoc = fitz.open()
        answer_page(kdoc, items, labels, product)
        kdoc.subset_fonts()
        kdoc.save(key_pdf, garbage=4, deflate=True)
        kdoc.close()
    if solutions_pdf is not None:
        render_solutions(bundle, labels, solutions_pdf)
    doc.subset_fonts()
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_pdf, garbage=4, deflate=True)
    pages = len(doc)
    doc.close()
    return {"status": "PASS", "pages": pages, "brand": brand, "product": product,
            "solutions_pdf": str(solutions_pdf) if solutions_pdf else None}

#!/usr/bin/env python3
"""Korean production renderer for ARC_N / ARC_FINAL problem sets.

ARC_N:     cover, blank verso, two-column problem pages, blank separator, answer key.
ARC_FINAL: cover, blank verso, two-column problem pages (no key); the answer key
           is written to a separate PDF so the problem sheet never exposes answers.

Question blocks are never split across columns. Passage paragraphs may flow
line by line. Content is rendered exactly as given; this module never edits it.
"""
from __future__ import annotations

import hashlib
import math
import re
from pathlib import Path
from typing import Any

import fitz

A4_W, A4_H = 595.276, 841.890
ML, MR, MT, MB = 46.0, 46.0, 64.0, 58.0
GUT = 20.0
COL_W = (A4_W - ML - MR - GUT) / 2
FONT_DIR = Path("/usr/share/fonts/truetype/nanum")
FONT_FILES = {
    "R": FONT_DIR / "NanumMyeongjo.ttf",
    "B": FONT_DIR / "NanumMyeongjoBold.ttf",
    "G": FONT_DIR / "NanumGothic.ttf",
    "GB": FONT_DIR / "NanumGothicBold.ttf",
}
# Hanja (漢字) and other glyphs Nanum lacks fall back to a CJK font; first existing file wins.
FALLBACK_FILES = [Path("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"),
                  Path("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc")]
# Math/linguistic symbols (e.g. U+2205 empty set used for zero morphemes) that neither Nanum nor the CJK fallback carries.
SYMBOL_FILES = [Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
                Path("/usr/share/fonts/truetype/freefont/FreeSerif.ttf")]
SIZE = 9.8
LH = SIZE * 1.62
NAVY = (0.08, 0.16, 0.30)
CIRC = "①②③④⑤"


class RenderError(RuntimeError):
    pass


# Middle Korean (옛한글) is written as conjoining jamo (U+1100-11FF, A960-A97F, D7B0-D7FF) that only compose into
# syllables through OpenType shaping. insert_text does not shape, so such clusters are drawn through MuPDF's HTML box
# (HarfBuzz) with Noto Serif CJK, which carries the old-Hangul composition tables. One composed syllable = 1 em.
OLD_HANGUL_FONT = Path("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc")
_JAMO = "\u1100-\u11ff\ua960-\ua97f\ud7b0-\ud7ff"
OLD_CLUSTER = re.compile(f"(?:[\u1100-\u115f\ua960-\ua97f]+[\u1160-\u11a7\ud7b0-\ud7c6]+[\u11a8-\u11ff\ud7cb-\ud7fb]*"
                         f"|[\uac00-\ud7a3][\u11a8-\u11ff\ud7cb-\ud7fb]+)")


def old_hangul_syllables(t: str) -> int:
    return len(OLD_CLUSTER.findall(t))


def fallback_file() -> Path | None:
    return next((p for p in FALLBACK_FILES if p.is_file()), None)


def symbol_file() -> Path | None:
    return next((p for p in SYMBOL_FILES if p.is_file()), None)


def fonts() -> dict[str, fitz.Font]:
    missing = [str(p) for p in FONT_FILES.values() if not p.is_file()]
    if missing:
        raise RenderError("KOREAN_FONT_MISSING: " + ", ".join(missing) + " (install fonts-nanum)")
    out = {k: fitz.Font(fontfile=str(v)) for k, v in FONT_FILES.items()}
    fb = fallback_file()
    if fb:
        out["H"] = fitz.Font(fontfile=str(fb))
    sf = symbol_file()
    if sf:
        out["S"] = fitz.Font(fontfile=str(sf))
    return out


_FONTS: dict[str, fitz.Font] | None = None


def runs(text: str, key: str) -> list[tuple[str, str]]:
    """Split text into (font key, run) so every glyph comes from a font that has it.
    A glyph missing from both the Korean font and the CJK fallback is a hard error, never a tofu box."""
    global _FONTS
    if _FONTS is None:
        _FONTS = fonts()
    out: list[tuple[str, str]] = []
    pos = 0
    for m in OLD_CLUSTER.finditer(text):
        if m.start() > pos:
            out += runs(text[pos:m.start()], key) if OLD_CLUSTER.search(text[pos:m.start()]) is None else []
        if out and out[-1][0] == "OH":
            out[-1] = ("OH", out[-1][1] + m.group())
        else:
            out.append(("OH", m.group()))
        pos = m.end()
    if pos:
        return out + (runs(text[pos:], key) if pos < len(text) else [])
    for ch in text:
        k = key
        if not ch.isspace() and not _FONTS[key].has_glyph(ord(ch)):
            if "H" in _FONTS and _FONTS["H"].has_glyph(ord(ch)):
                k = "H"
            elif "S" in _FONTS and _FONTS["S"].has_glyph(ord(ch)):
                k = "S"
            else:
                raise RenderError(f"GLYPH_MISSING: U+{ord(ch):04X} {ch!r} (install fonts-noto-cjk or fonts-wqy-zenhei)")
        if out and out[-1][0] == k:
            out[-1] = (k, out[-1][1] + ch)
        else:
            out.append((k, ch))
    return out


def put(page: fitz.Page, pos, text: str, fontname: str = "R", fontsize: float = SIZE, color=None) -> None:
    x, y = pos
    for k, t in runs(text, fontname):
        if k == "OH":
            w = old_hangul_syllables(t) * fontsize
            page.insert_htmlbox(fitz.Rect(x, y - fontsize * 1.02, x + w + fontsize, y + fontsize * 0.6),
                                f"<p>{t}</p>", archive=fitz.Archive(str(OLD_HANGUL_FONT.parent)),
                                css=f"@font-face{{font-family:OH;src:url({OLD_HANGUL_FONT.name});}}"
                                    f"p{{font-family:OH;font-size:{fontsize}pt;margin:0;line-height:1.2}}")
            x += w
            continue
        if k not in {f[4] for f in page.get_fonts()}:  # embed only fonts a page actually uses (unused fonts are not subset)
            page.insert_font(fontname=k, fontfile=str(FONT_FILES.get(k) or (symbol_file() if k == "S" else fallback_file())))
        kw = {"color": color} if color is not None else {}
        page.insert_text((x, y), t, fontname=k, fontsize=fontsize, **kw)
        x += _FONTS[k].text_length(t, fontsize=fontsize)


class Layout:
    def __init__(self) -> None:
        self.f = fonts()

    def width(self, text: str, key: str = "R", size: float = SIZE) -> float:
        return sum(old_hangul_syllables(t) * size if k == "OH" else self.f[k].text_length(t, fontsize=size)
                   for k, t in runs(text, key))

    def wrap(self, text: str, w: float, key: str = "R", size: float = SIZE, first: float = 0.0, rest: float = 0.0):
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
        return [(i, t.replace("\u00a0", " ")) for i, t in lines]


class Block:
    def __init__(self, splittable: bool = False) -> None:
        self.ops: list[tuple] = []
        self.h = 0.0
        self.splittable = splittable

    def text(self, lines, key="R", size=SIZE, lh=LH, dx=0.0):
        for indent, t in lines:
            self.ops.append(("text", dx + indent, self.h + size, t, key, size))
            self.h += lh


def build_blocks(L: Layout, bundle: dict[str, Any], sources: list[dict[str, Any]], labels: dict[str, str], set_header) -> list[Block]:
    blocks: list[Block] = []
    for src in sources:
        hdr = set_header(bundle, src["id"], labels)
        if hdr:  # sets with item-supplied material only have no shared passage header
            head = Block()
            head.text(L.wrap(hdr, COL_W, "B"), key="B")
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
            src_b = Block()
            small = SIZE - 0.6
            for _, t in L.wrap(f"― {w['title']} ―", COL_W, size=small):
                src_b.ops.append(("text", COL_W - L.width(t, size=small), src_b.h + SIZE, t, "R", small))
                src_b.h += LH
            src_b.h += 8
            blocks.append(src_b)
        if src.get("notes"):
            nb = Block()
            for note in src["notes"]:
                nb.text(L.wrap(note, COL_W, size=SIZE - 1.2, rest=SIZE), size=SIZE - 1.2, lh=(SIZE - 1.2) * 1.5)
            nb.h += 10
            blocks.append(nb)
        for it in [x for x in bundle["items"] if x["set"] == src["id"]]:
            blocks.append(question_block(L, it, labels[it["item_id"]], bundle["product_mode"]))
    return blocks


def question_block(L: Layout, it: dict[str, Any], label: str, product: str = "ARC_N") -> Block:
    b = Block()
    if product == "ARC_N" and re.fullmatch(r"D[1-5]", str(it.get("difficulty", ""))):
        # Metadata strip (user decision 2026-11-08): the internal grade D1-D5 is shown here only,
        # never in the stem/choices, never in ARC_FINAL, and never invented when absent.
        top = b.h
        b.h += 13
        b.ops.append(("rect", 0, top, COL_W, b.h))
        b.ops.append(("text", 5, top + 9.4, f"난이도 {it['difficulty']}", "B", 7.3))
        b.h += 5
    pts = f" ({it['points']}점)" if it.get("points") else ""
    if it.get("format") == "CR":
        num = f"[{label}] "
    elif product == "ARC_FINAL":
        num = f"{label}. "
    else:
        num = f"{int(label):02d} "
    nw = L.width(num, "B")
    stem = L.wrap(it["stem"] + pts, COL_W, "B", first=nw, rest=nw)
    stem[0] = (0, num + stem[0][1])
    b.text(stem, key="B")
    b.h += 4
    if it.get("table"):
        table(L, b, it["table"])
    if it.get("view"):
        view(L, b, it["view"])
    if it.get("format") == "CR":
        view(L, b, it["conditions"], label="<조 건>")
        top = b.h
        b.h += LH * 3.2
        b.ops.append(("rect", 0, top, COL_W, b.h))
        b.ops.append(("text", 5, top + SIZE + 3, "답:", "G", SIZE - 0.8))
        b.h += 16
        return b
    labels_ = [f"{CIRC[i]} {o}" for i, o in enumerate(it["options"])]
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
    b.h += 16
    return b


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
    b.ops.append(("line", 0, y, COL_W, y, 0.8))
    for ri, row in enumerate(rows):
        key = "GB" if ri == 0 else "R"
        wrapped = [L.wrap(cell, cw[i] - 2 * pad, key, size) for i, cell in enumerate(row)]
        rh = max(len(w) for w in wrapped) * lh + 2 * pad
        x = 0.0
        for i, w in enumerate(wrapped):
            yy = y + pad
            for _, t in w:
                b.ops.append(("text", x + pad, yy + size, t, key, size))
                yy += lh
            x += cw[i]
        y += rh
        b.ops.append(("line", 0, y, COL_W, y, 0.8 if ri in (0, len(rows) - 1) else 0.4))
    x = 0.0
    for i in range(1, ncol):
        x += cw[i - 1]
        b.ops.append(("line", x, b.h + 2, x, y, 0.4))
    b.h = y + 8


def paint(page: fitz.Page, ops, x: float, y: float) -> None:
    labels = []
    for op in ops:
        kind = op[0]
        if kind == "text":
            _, dx, dy, t, key, size = op
            put(page, (x + dx, y + dy), t, fontname=key, fontsize=size)
        elif kind == "rect":
            _, x0, y0, x1, y1 = op
            page.draw_rect(fitz.Rect(x + x0, y + y0, x + x1, y + y1), color=(0.25, 0.25, 0.25), width=0.6)
        elif kind == "line":
            _, x0, y0, x1, y1, w = op
            page.draw_line((x + x0, y + y0), (x + x1, y + y1), color=(0.25, 0.25, 0.25), width=w)
        elif kind == "label":
            labels.append(op)
    for _, lx, ly, t, lw in labels:  # knock the label out of the box border
        page.draw_rect(fitz.Rect(x + lx - 4, y + ly - 5.5, x + lx + lw + 4, y + ly + 5.5), color=None, fill=(1, 1, 1))
        put(page, (x + lx, y + ly + 3.4), t, fontname="B", fontsize=SIZE)


def new_page(doc: fitz.Document) -> fitz.Page:
    return doc.new_page(width=A4_W, height=A4_H)  # fonts are embedded by put() only where used


def problem_page(doc, L: Layout, header: str, number: int) -> fitz.Page:
    page = new_page(doc)
    put(page, (ML, 38), header, fontname="G", fontsize=8.4, color=NAVY)
    page.draw_line((ML, 46), (A4_W - MR, 46), color=(0.45, 0.55, 0.68), width=0.7)
    mid = ML + COL_W + GUT / 2
    page.draw_line((mid, MT - 4), (mid, A4_H - MB + 6), color=(0.7, 0.7, 0.7), width=0.4)
    s = str(number)
    put(page, (A4_W / 2 - L.width(s, "G", 9) / 2, A4_H - 28), s, fontname="G", fontsize=9)
    return page


def cover(doc, meta: dict[str, Any], logo: dict[str, Any] | None) -> str:
    page = new_page(doc)
    brand = "BRAND_ASSET_MISSING"
    top = 150
    if logo and Path(logo["path"]).is_file():
        data = Path(logo["path"]).read_bytes()
        if hashlib.sha256(data).hexdigest() != logo["sha256"]:
            raise RenderError("BRAND_HASH_MISMATCH")
        w, h = logo["pixels"]
        box_w = 170.0
        page.insert_image(fitz.Rect(64, 70, 64 + box_w, 70 + box_w * h / w), stream=data, keep_proportion=True)
        brand, top = "PASS", 70 + box_w * h / w + 50
    put(page, (64, top), meta["set_label"], fontname="GB", fontsize=30, color=NAVY)
    put(page, (64, top + 40), meta["course"], fontname="GB", fontsize=20)
    put(page, (64, top + 72), meta["cover_subtitle"], fontname="G", fontsize=12.5)
    y = top + 96
    for p in meta["passage_titles"]:
        put(page, (64, y), p, fontname="G", fontsize=10)
        y += 18
    page.draw_line((64, y + 4), (A4_W - 64, y + 4), color=(0.45, 0.55, 0.68), width=0.8)
    put(page, (64, 770), meta["school_line"], fontname="G", fontsize=10)
    return brand


def answer_page(doc, items: list[dict[str, Any]], labels: dict[str, str] | None = None, product: str = "ARC_N") -> None:
    L = Layout()
    key = new_page(doc)
    put(key, (ML, 80), "정답  ANSWER KEY", fontname="GB", fontsize=18, color=NAVY)
    key.draw_line((ML, 94), (A4_W - MR, 94), color=(0.45, 0.55, 0.68), width=0.8)
    mcq = [it for it in items if it.get("format", "MCQ") == "MCQ"]
    per_col = 10 if len(mcq) <= 30 else 15
    for i, it in enumerate(mcq):
        x = ML + 20 + (i // per_col) * 130
        y = 132 + (i % per_col) * 28
        num = f"{i + 1:02d}" if product == "ARC_N" else f"{i + 1}"
        put(key, (x, y), f"{num}  {CIRC[it['answer'] - 1]}", fontname="G", fontsize=12.5)
    crs = [it for it in items if it.get("format") == "CR"]
    if not crs:
        return
    y = 132 + per_col * 28 + 20
    page = key
    width = A4_W - ML - MR
    for it in crs:
        chunks = [("GB", f"[{labels[it['item_id']] if labels else it['item_id']}] 모범답안 ({it.get('points', '')}점)")]
        chunks += [("R", "답: " + it["model_answer"])]
        chunks += [("G", "채점 기준: " + r) for r in it.get("rubric", [])]
        if it.get("accepted_variants"):
            chunks.append(("G", "유사 정답: " + " / ".join(it["accepted_variants"])))
        for key_font, text in chunks:
            for _, line in L.wrap(text, width, key_font, 10.2):
                if y > A4_H - MB:
                    page = new_page(doc)
                    y = 80
                put(page, (ML, y), line, fontname=key_font, fontsize=10.2)
                y += 15.5
        y += 10


def render(bundle: dict[str, Any], sources: list[dict[str, Any]], labels: dict[str, str], set_header,
           out_pdf: Path, key_pdf: Path | None = None, logo: dict[str, Any] | None = None) -> dict[str, Any]:
    product = bundle["product_mode"]
    items = bundle["items"]
    L = Layout()
    doc = fitz.open()
    titles = list(dict.fromkeys(w["title"] for src in sources for w in src["works"]))  # short per-item excerpts repeat a source: list it once
    meta = dict(bundle, passage_titles=titles)
    brand = cover(doc, meta, logo)
    doc.new_page(width=A4_W, height=A4_H)  # blank verso
    header = f"{bundle['set_label']}  {bundle['course']}"
    pno = 3
    page = problem_page(doc, L, header, pno)
    col, y, bottom = 0, MT, A4_H - MB

    def advance():
        nonlocal col, y, page, pno
        if col == 0:
            col, y = 1, MT
        else:
            pno += 1
            page = problem_page(doc, L, header, pno)
            col, y = 0, MT

    for b in build_blocks(L, bundle, sources, labels, set_header):
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
            if b.h > bottom - MT:
                raise RenderError(f"QUESTION_BLOCK_TALLER_THAN_COLUMN: {b.h:.1f}pt")
        paint(page, b.ops, ML + col * (COL_W + GUT), y)
        y += b.h

    if product == "ARC_N":
        doc.new_page(width=A4_W, height=A4_H)  # blank separator
        answer_page(doc, items, labels, product)
    elif key_pdf is not None:
        kdoc = fitz.open()
        answer_page(kdoc, items, labels, product)
        kdoc.subset_fonts()
        kdoc.save(key_pdf, garbage=4, deflate=True)
        kdoc.close()
    doc.subset_fonts()
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_pdf, garbage=4, deflate=True)
    pages = len(doc)
    doc.close()
    return {"status": "PASS", "pages": pages, "brand": brand, "product": product}

def pack_order(items: list[dict[str, Any]], product: str = "ARC_N", window: int = 5, ok=None, section=None) -> list[int]:
    """Order for item-supplied-material questions that fills column gaps (school papers rarely leave half columns empty).
    Greedy two-column fill: keep the original order while the next question fits; when it does not, pull the
    largest question that still fits from the next `window` questions of the same section. `ok(placed, cand)`
    may veto a choice (e.g. three same answer positions in a row). Returns indices into `items`."""
    L = Layout()
    h = [question_block(L, it, "00", product).h for it in items]
    col_h = (A4_H - MB) - MT
    left = list(range(len(items)))
    out: list[int] = []
    y = 0.0
    sec = section or (lambda i: 0)
    while left:
        head_sec = sec(left[0])
        win = [i for i in left if sec(i) == head_sec][:window]
        allowed = [i for i in win if ok is None or ok([items[j] for j in out], items[i])] or win
        fits = [i for i in allowed if y + h[i] <= col_h]
        if fits:
            pick = fits[0] if fits[0] == left[0] or y == 0 else max(fits, key=lambda i: h[i])
            out.append(pick)
            left.remove(pick)
            y += h[pick]
        else:
            y = 0.0  # next column
            pick = allowed[0]
            out.append(pick)
            left.remove(pick)
            y += h[pick]
    return out

def pack_columns(items: list[dict[str, Any]], sections: list[int], product: str = "ARC_N", ok=None) -> list[int]:
    """Balanced packing of whole questions (user 2026-11-10: no page with one lonely question, no half-empty
    columns). Each section gets the fewest columns into which LPT (largest question first, into the emptiest
    column) fits; if the total is odd, one more column goes to the fullest section so every page has two filled
    columns. Inside a column questions keep authoring order; columns follow their earliest question.
    `ok(prev2, cand)` vetoes sequences (e.g. three equal answer positions) and is repaired by nearby swaps."""
    L = Layout()
    h = [question_block(L, it, "00", product).h for it in items]
    cap = (A4_H - MB) - MT

    def lpt(idx: list[int], n: int) -> list[list[int]]:
        bins: list[list[int]] = [[] for _ in range(n)]
        for i in sorted(idx, key=lambda i: -h[i]):
            min(bins, key=lambda bn: sum(h[j] for j in bn)).append(i)
        return bins

    secs = sorted(set(sections))
    members = {sec: [i for i in range(len(items)) if sections[i] == sec] for sec in secs}
    count = {}
    for sec in secs:
        n = max(1, math.ceil(sum(h[i] for i in members[sec]) / cap))
        while max(sum(h[j] for j in bn) for bn in lpt(members[sec], n)) > cap:
            n += 1
        count[sec] = n
    if sum(count.values()) % 2:
        fullest = max(secs, key=lambda sec: sum(h[i] for i in members[sec]) / count[sec])
        count[fullest] += 1
    order: list[int] = []
    for sec in secs:
        cols = [sorted(bn) for bn in lpt(members[sec], count[sec]) if bn]
        for c in sorted(cols, key=min):
            order += c
    if ok is not None:
        for _ in range(3):
            for k in range(2, len(order)):
                if not ok([items[j] for j in order[k - 2:k]], items[order[k]]):
                    for m in range(k + 1, min(k + 4, len(order))):
                        if sections[order[m]] == sections[order[k]] and ok([items[j] for j in order[k - 2:k]], items[order[m]]):
                            order[k], order[m] = order[m], order[k]
                            break
    return order

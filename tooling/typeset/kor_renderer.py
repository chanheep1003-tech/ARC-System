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
SIZE = 9.8
LH = SIZE * 1.62
NAVY = (0.08, 0.16, 0.30)
CIRC = "①②③④⑤"


class RenderError(RuntimeError):
    pass


def fonts() -> dict[str, fitz.Font]:
    missing = [str(p) for p in FONT_FILES.values() if not p.is_file()]
    if missing:
        raise RenderError("KOREAN_FONT_MISSING: " + ", ".join(missing) + " (install fonts-nanum)")
    return {k: fitz.Font(fontfile=str(v)) for k, v in FONT_FILES.items()}


class Layout:
    def __init__(self) -> None:
        self.f = fonts()

    def width(self, text: str, key: str = "R", size: float = SIZE) -> float:
        return self.f[key].text_length(text, fontsize=size)

    def wrap(self, text: str, w: float, key: str = "R", size: float = SIZE, first: float = 0.0, rest: float = 0.0):
        """Greedy wrap on spaces (어절); char break only for tokens wider than the line."""
        lines, cur, indent = [], "", first
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
        return lines


class Block:
    def __init__(self, splittable: bool = False) -> None:
        self.ops: list[tuple] = []
        self.h = 0.0
        self.splittable = splittable

    def text(self, lines, key="R", size=SIZE, lh=LH, dx=0.0):
        for indent, t in lines:
            self.ops.append(("text", dx + indent, self.h + size, t, key, size))
            self.h += lh


def build_blocks(L: Layout, passages: list[dict[str, Any]], items: list[dict[str, Any]]) -> list[Block]:
    blocks: list[Block] = []
    number = 1
    for passage in passages:
        own = [it for it in items if it["passage"] == passage["id"]]
        if not own:
            continue
        first, last = number, number + len(own) - 1
        head = Block()
        head.text(L.wrap(f"[{first}~{last}] 다음 글을 읽고 물음에 답하시오.", COL_W, "B"), key="B")
        head.h += 6
        blocks.append(head)
        for para in passage["paragraphs"]:
            b = Block(splittable=True)
            b.text(L.wrap(para, COL_W, first=SIZE))
            b.h += 2
            blocks.append(b)
        src = Block()
        small = SIZE - 0.6
        for _, t in L.wrap(f"― {passage['title']} ―", COL_W, size=small):
            src.ops.append(("text", COL_W - L.width(t, size=small), src.h + SIZE, t, "R", small))
            src.h += LH
        src.h += 10
        blocks.append(src)
        for it in own:
            blocks.append(question_block(L, it, number))
            number += 1
    return blocks


def question_block(L: Layout, it: dict[str, Any], number: int) -> Block:
    b = Block()
    num = f"{number:02d} "
    stem = L.wrap(it["stem"], COL_W, "B", rest=L.width(num, "B"))
    stem[0] = (0, num + stem[0][1])
    b.text(stem, key="B")
    b.h += 4
    if it.get("table"):
        table(L, b, it["table"])
    if it.get("view"):
        view(L, b, it["view"])
    labels = [f"{CIRC[i]} {o}" for i, o in enumerate(it["options"])]
    widest = max(L.width(t) for t in labels)
    if widest <= COL_W / 5 - 4:
        for i, t in enumerate(labels):
            b.ops.append(("text", i * COL_W / 5, b.h + SIZE, t, "R", SIZE))
        b.h += LH
    elif widest <= COL_W / 3 - 4:
        for i, t in enumerate(labels):
            if i == 3:
                b.h += LH
            b.ops.append(("text", (i % 3) * COL_W / 3, b.h + SIZE, t, "R", SIZE))
        b.h += LH
    else:
        hang = L.width("① ")
        for t in labels:
            b.text(L.wrap(t, COL_W, rest=hang))
            b.h += 1.5
    b.h += 16
    return b


def view(L: Layout, b: Block, lines: list[str]) -> None:
    pad, top = 7.0, b.h
    b.h += pad + 3
    for s in lines:
        hang = L.width("ㄱ. ") if len(s) > 2 and s[1] == "." else 0.0
        b.text(L.wrap(s, COL_W - 2 * pad, rest=hang), dx=pad)
        b.h += 1
    b.h += pad - 2
    b.ops.append(("rect", 0, top + 4, COL_W, b.h))
    label = "<보 기>"
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
            page.insert_text((x + dx, y + dy), t, fontname=key, fontsize=size)
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
        page.insert_text((x + lx, y + ly + 3.4), t, fontname="B", fontsize=SIZE)


def new_page(doc: fitz.Document) -> fitz.Page:
    page = doc.new_page(width=A4_W, height=A4_H)
    for k, f in FONT_FILES.items():
        page.insert_font(fontname=k, fontfile=str(f))
    return page


def problem_page(doc, L: Layout, header: str, number: int) -> fitz.Page:
    page = new_page(doc)
    page.insert_text((ML, 38), header, fontname="G", fontsize=8.4, color=NAVY)
    page.draw_line((ML, 46), (A4_W - MR, 46), color=(0.45, 0.55, 0.68), width=0.7)
    mid = ML + COL_W + GUT / 2
    page.draw_line((mid, MT - 4), (mid, A4_H - MB + 6), color=(0.7, 0.7, 0.7), width=0.4)
    s = str(number)
    page.insert_text((A4_W / 2 - L.width(s, "G", 9) / 2, A4_H - 28), s, fontname="G", fontsize=9)
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
    page.insert_text((64, top), meta["set_label"], fontname="GB", fontsize=30, color=NAVY)
    page.insert_text((64, top + 40), meta["course"], fontname="GB", fontsize=20)
    page.insert_text((64, top + 72), meta["cover_subtitle"], fontname="G", fontsize=12.5)
    y = top + 96
    for p in meta["passage_titles"]:
        page.insert_text((64, y), p, fontname="G", fontsize=10)
        y += 18
    page.draw_line((64, y + 4), (A4_W - 64, y + 4), color=(0.45, 0.55, 0.68), width=0.8)
    page.insert_text((64, 770), meta["school_line"], fontname="G", fontsize=10)
    return brand


def answer_page(doc, items: list[dict[str, Any]]) -> None:
    key = new_page(doc)
    key.insert_text((ML, 80), "정답  ANSWER KEY", fontname="GB", fontsize=18, color=NAVY)
    key.draw_line((ML, 94), (A4_W - MR, 94), color=(0.45, 0.55, 0.68), width=0.8)
    per_col = 10
    for i, it in enumerate(items):
        x = ML + 20 + (i // per_col) * 130
        y = 132 + (i % per_col) * 30
        key.insert_text((x, y), f"{i + 1:02d}  {CIRC[it['answer'] - 1]}", fontname="G", fontsize=13)


def render(bundle: dict[str, Any], passages: list[dict[str, Any]], out_pdf: Path,
           key_pdf: Path | None = None, logo: dict[str, Any] | None = None) -> dict[str, Any]:
    product = bundle["product_mode"]
    items = bundle["items"]
    L = Layout()
    doc = fitz.open()
    meta = dict(bundle, passage_titles=[p["title"] for p in passages])
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

    for b in build_blocks(L, passages, items):
        if b.splittable and y + b.h > bottom:
            for op in b.ops:
                if y + LH > bottom:
                    advance()
                x = ML + col * (COL_W + GUT)
                page.insert_text((x + op[1], y + op[5]), op[3], fontname=op[4], fontsize=op[5])
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
        answer_page(doc, items)
    elif key_pdf is not None:
        kdoc = fitz.open()
        answer_page(kdoc, items)
        kdoc.subset_fonts()
        kdoc.save(key_pdf, garbage=4, deflate=True)
        kdoc.close()
    doc.subset_fonts()
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_pdf, garbage=4, deflate=True)
    pages = len(doc)
    doc.close()
    return {"status": "PASS", "pages": pages, "brand": brand, "product": product}

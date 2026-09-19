#!/usr/bin/env python3
"""Behavioral smoke tests for ARC PDF preflight V1.2."""
from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("arc_pdf_preflight", ROOT / "tooling/pdf_qc/pdf_preflight.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


def new_doc() -> fitz.Document:
    doc = fitz.open()
    cover = doc.new_page(width=mod.A4_W, height=mod.A4_H)
    cover.insert_text((72, 110), "ARC CORE", fontsize=22)
    return doc


def paragraph() -> str:
    return (
        "A stable learning document needs readable typography, semantic pagination, "
        "clear hierarchy, and enough following text to keep headings attached to content. "
        "This paragraph is deliberately long enough to behave like body prose in detection. "
    )


def add_one_column_page(doc: fitz.Document) -> None:
    p = doc.new_page(width=mod.A4_W, height=mod.A4_H)
    y = 64
    for i in range(9):
        r = fitz.Rect(58, y, mod.A4_W - 58, y + 70)
        remaining = p.insert_textbox(r, paragraph(), fontsize=10.0, lineheight=1.20)
        assert remaining >= 0, remaining
        y += 78


def add_two_column_page(doc: fitz.Document) -> None:
    p = doc.new_page(width=mod.A4_W, height=mod.A4_H)
    left = fitz.Rect(45, 70, mod.A4_W / 2 - 16, 300)
    right = fitz.Rect(mod.A4_W / 2 + 16, 70, mod.A4_W - 45, 300)
    left2 = fitz.Rect(45, 330, mod.A4_W / 2 - 16, 610)
    right2 = fitz.Rect(mod.A4_W / 2 + 16, 330, mod.A4_W - 45, 610)
    body = paragraph() * 2
    for r in (left, right, left2, right2):
        remaining = p.insert_textbox(r, body, fontsize=10.0, lineheight=1.20)
        assert remaining >= 0, remaining


def flag_types(result: dict) -> set[str]:
    return {flag["type"] for page in result["pages"] for flag in page["flags"]}


def run() -> None:
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)

        doc = new_doc()
        add_one_column_page(doc)
        path = td / "one.pdf"
        doc.save(path)
        doc.close()
        result = mod.analyze_pdf(path, "ARC_CORE")
        assert "CORE_TWO_COLUMN_FLOW" not in flag_types(result), result

        doc = new_doc()
        add_two_column_page(doc)
        path = td / "two.pdf"
        doc.save(path)
        doc.close()
        result = mod.analyze_pdf(path, "ARC_CORE")
        assert "CORE_TWO_COLUMN_FLOW" in flag_types(result), result

        doc = new_doc()
        p = doc.new_page(width=mod.A4_W, height=mod.A4_H)
        p.insert_textbox(fitz.Rect(55, 70, mod.A4_W - 55, 700), (paragraph() * 12) + " <br> ", fontsize=10.0)
        path = td / "markup.pdf"
        doc.save(path)
        doc.close()
        result = mod.analyze_pdf(path, "ARC_CORE")
        assert "RAW_MARKUP_LEAK" in flag_types(result), result

        doc = new_doc()
        p = doc.new_page(width=mod.A4_W, height=mod.A4_H)
        p.insert_text((70, 90), "Only one carry-over line.", fontsize=10.0)
        path = td / "sparse.pdf"
        doc.save(path)
        doc.close()
        result = mod.analyze_pdf(path, "ARC_CORE")
        assert "CORE_NEAR_EMPTY_PAGE" in flag_types(result), result

        doc = new_doc()
        p = doc.new_page(width=mod.A4_W, height=mod.A4_H)
        remaining = p.insert_textbox(
            fitz.Rect(55, 70, mod.A4_W - 55, 720),
            paragraph() * 10,
            fontsize=8.5,
            lineheight=1.25,
        )
        assert remaining >= 0, remaining
        path = td / "smallfont.pdf"
        doc.save(path)
        doc.close()
        result = mod.analyze_pdf(path, "ARC_CORE")
        assert "CORE_BODY_FONT_TOO_SMALL" in flag_types(result), result

        doc = new_doc()
        p = doc.new_page(width=mod.A4_W, height=mod.A4_H)
        remaining = p.insert_textbox(
            fitz.Rect(55, 70, mod.A4_W - 55, 560),
            paragraph() * 7,
            fontsize=10.0,
            lineheight=1.22,
        )
        assert remaining >= 0, remaining
        p.insert_text((60, 650), "Section heading should move", fontsize=13.0, fontname="helv")
        path = td / "orphan.pdf"
        doc.save(path)
        doc.close()
        result = mod.analyze_pdf(path, "ARC_CORE")
        assert "HEADING_ORPHAN_CANDIDATE" in flag_types(result), result

        doc = new_doc()
        p = doc.new_page(width=mod.A4_W, height=mod.A4_H)
        p.insert_text((65, 520), "PART A - Social Justice", fontsize=18.0, fontname="helv")
        p.insert_textbox(
            fitz.Rect(65, 555, mod.A4_W - 65, 720),
            paragraph() * 2,
            fontsize=10.0,
            lineheight=1.2,
        )
        path = td / "late-part.pdf"
        doc.save(path)
        doc.close()
        result = mod.analyze_pdf(path, "ARC_CORE")
        assert "CORE_MAJOR_BOUNDARY_NOT_PAGE_START" in flag_types(result), result

    print("ARC PDF PREFLIGHT SMOKE: PASS")


if __name__ == "__main__":
    run()

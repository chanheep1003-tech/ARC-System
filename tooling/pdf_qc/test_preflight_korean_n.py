#!/usr/bin/env python3
"""ARC_N preflight must count Korean production markers ("01 ..." stems, "01 ③" key lines)
and still block missing questions, missing answers and a missing separator page."""
from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("arc_pdf_preflight", ROOT / "tooling/pdf_qc/pdf_preflight.py")
preflight = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(preflight)

A4_W, A4_H = 595.276, 841.890
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
CIRCLED = "①②③④⑤"


def build(path: Path, question_numbers, answer_numbers, separator=True, gutter_crossing=False, key_symbols=CIRCLED) -> None:
    doc = fitz.open()
    cover = doc.new_page(width=A4_W, height=A4_H)
    cover.insert_font(fontname="F", fontfile=FONT)
    cover.insert_text((72, 150), "ARC N 04", fontname="F", fontsize=24)
    doc.new_page(width=A4_W, height=A4_H)
    page = doc.new_page(width=A4_W, height=A4_H)
    page.insert_font(fontname="F", fontfile=FONT)
    y = 80
    for n in question_numbers:
        page.insert_text((60, y), f"{n:02d} Which statement is best supported?", fontname="F", fontsize=10)
        page.insert_text((60, y + 16), "① a  ② b  ③ c  ④ d  ⑤ e", fontname="F", fontsize=10)
        y += 44
    if gutter_crossing:
        page.insert_text((60, 600), "11 This stem line runs straight across the column gutter into the right column", fontname="F", fontsize=10)
    page.insert_text((290, 812), "3", fontname="F", fontsize=9)
    if separator:
        doc.new_page(width=A4_W, height=A4_H)
    key = doc.new_page(width=A4_W, height=A4_H)
    key.insert_font(fontname="F", fontfile=FONT)
    key.insert_text((60, 80), "ANSWER KEY", fontname="F", fontsize=18)
    for i, n in enumerate(answer_numbers):
        key.insert_text((80, 130 + i * 30), f"{n:02d}  {key_symbols[n % 5]}", fontname="F", fontsize=12)
    doc.save(path)
    doc.close()


def flag_types(result) -> set[str]:
    return {f["type"] for p in result["pages"] for f in p["flags"] if f["severity"] == "FAIL"}


def main() -> int:
    ids = list(range(1, 11))
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        cases = {
            "valid": (ids, ids, True, set()),
            "dingbat_valid": (ids, ids, True, set()),
            "dingbat_missing": (ids, ids[:-1], True, {"ARC_N_ANSWER_COUNT_MISMATCH"}),
            "gutter_crossing": (ids, ids, True, {"COLUMN_GUTTER_CROSSING"}),
            "question_missing": ([n for n in ids if n != 7], ids, True, {"ARC_N_QUESTION_COUNT_MISMATCH"}),
            "answer_missing": (ids, ids[:-1], True, {"ARC_N_ANSWER_COUNT_MISMATCH"}),
            "separator_missing": (ids, ids, False, {"ARC_N_SEPARATOR_NOT_BLANK"}),
        }
        for name, (questions, answers, separator, expected) in cases.items():
            pdf = tmp / f"{name}.pdf"
            build(pdf, questions, answers, separator, gutter_crossing=(name == "gutter_crossing"),
                  key_symbols="➀➁➂➃➄" if name.startswith("dingbat") else CIRCLED)
            result = preflight.analyze_pdf(pdf, "ARC_N", expected_item_count=10)
            fails = flag_types(result)
            if expected:
                assert expected <= fails, (name, fails)
            else:
                assert result["status"] in {"PASS", "WARN"} and not fails, (name, fails)
        assert not preflight.ANSWER_LINE_RE.findall("01 ➅\n02 ⑥\n"), "out-of-range answers accepted"
    print("ARC PREFLIGHT KOREAN N MARKERS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

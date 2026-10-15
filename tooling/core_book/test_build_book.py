#!/usr/bin/env python3
"""Smoke for the ARC CORE BOOK builder helpers and BOOK style invariants (no browser needed)."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("arc_build_book", ROOT / "tooling/core_book/build_book.py")
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


def run() -> None:
    assert mod.non_gray_colors("a{color:#111;background:#e4e4e4;border:1px solid #000}") == []
    assert mod.non_gray_colors("a{color:#1F2A44}") == ["#1f2a44"]
    assert mod.non_gray_colors("a{color:#7A2E35;b:#fff}") == ["#7a2e35"]

    css = mod.CSS.read_text(encoding="utf-8")
    assert mod.non_gray_colors(css) == [], "BOOK style must be grayscale-only"
    for rule in (".s{break-inside:avoid", "table.t tr{break-inside:avoid", ".cp{break-before:page", "column-count:auto!important"):
        assert rule in css, rule
    assert "column-count:1" not in css, "column-count:1 on a flow wrapper breaks page breaks"

    parts = [ROOT / "templates/core/ARC_CORE_BOOK_master_v0.4.html"]
    html = mod.assemble(
        parts,
        css,
        {k: "x" for k in ("COVER_KICKER", "COVER_TITLE", "COVER_SUBTITLE", "COVER_SCOPE", "COVER_SCHOOL_EXAM", "COVER_YEAR")},
        {"A": 7},
        "t",
    )
    assert 'data-core-profile="BOOK"' in html
    try:
        mod.assemble([ROOT / "templates/core/ARC_CORE_BOOK_master_v0.4.html"], css, {}, None, "t")
    except SystemExit as exc:
        assert "unresolved placeholders" in str(exc)
    else:
        raise AssertionError("unresolved placeholders must stop the build")
    print("ARC CORE BOOK BUILDER SMOKE: PASS")


if __name__ == "__main__":
    run()

"""Embedded Latin fonts for synthetic PDF pipeline fixtures only.

These fonts do not certify Korean glyph coverage. Production Korean PDFs must
use a separately verified Korean Regular/Bold font and visual QA.
"""
from __future__ import annotations

from pathlib import Path


def _first_existing(candidates: list[Path]) -> Path:
    return next((p for p in candidates if p.is_file()), candidates[0])


REGULAR_NAME = "ArcCanaryRegular"
BOLD_NAME = "ArcCanaryBold"
REGULAR_FILE = _first_existing([
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    Path("C:/Windows/Fonts/HANDotum.ttf"),
    Path("C:/Windows/Fonts/malgun.ttf"),
    Path("C:/Windows/Fonts/arial.ttf"),
])
BOLD_FILE = _first_existing([
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    Path("C:/Windows/Fonts/HANDotumB.ttf"),
    Path("C:/Windows/Fonts/malgunbd.ttf"),
    Path("C:/Windows/Fonts/arialbd.ttf"),
])
ALLOWED_FONT_TOKENS = ("dejavu sans", "hcr dotum", "malgun gothic", "arial")


def embed(page) -> None:
    if not REGULAR_FILE.is_file() or not BOLD_FILE.is_file():
        raise RuntimeError("CANARY_FONT_MISSING: embedded regular and bold fonts are required")
    page.insert_font(fontname=REGULAR_NAME, fontfile=str(REGULAR_FILE))
    page.insert_font(fontname=BOLD_NAME, fontfile=str(BOLD_FILE))


def assert_embedded_fonts(document) -> None:
    """Reject accidental return to non-embedded Base14 student text."""
    for number, page in enumerate(document, start=1):
        if not page.get_text().strip():
            continue
        for xref, _ext, _type, name, _alias, _encoding in page.get_fonts():
            if not any(tok in name.lower() for tok in ALLOWED_FONT_TOKENS):
                raise RuntimeError(f"CANARY_NON_EMBEDDED_FONT page {number}: {name}")
            _font_name, extension, _kind, binary = document.extract_font(xref)
            if extension not in {"ttf", "otf"} or not binary:
                raise RuntimeError(f"CANARY_FONT_NOT_EMBEDDED page {number}: {name}")

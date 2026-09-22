"""Embedded Latin fonts for synthetic PDF pipeline fixtures only.

These fonts do not certify Korean glyph coverage. Production Korean PDFs must
use a separately verified Korean Regular/Bold font and visual QA.
"""
from __future__ import annotations

from pathlib import Path


REGULAR_NAME = "ArcCanaryRegular"
BOLD_NAME = "ArcCanaryBold"
REGULAR_FILE = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
BOLD_FILE = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")


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
            if "dejavu sans" not in name.lower():
                raise RuntimeError(f"CANARY_NON_EMBEDDED_FONT page {number}: {name}")
            _font_name, extension, _kind, binary = document.extract_font(xref)
            if extension not in {"ttf", "otf"} or not binary:
                raise RuntimeError(f"CANARY_FONT_NOT_EMBEDDED page {number}: {name}")

#!/usr/bin/env python3
import tempfile
from pathlib import Path

import cv2
import fitz
import numpy as np

from xmark_detect import raster_candidates


def make_pdf(path: Path, with_x: bool) -> None:
    image = np.full((900, 700, 3), 255, dtype=np.uint8)
    if with_x:
        cv2.line(image, (120, 120), (580, 780), (0, 0, 0), 18)
        cv2.line(image, (580, 120), (120, 780), (0, 0, 0), 18)
    ok, encoded = cv2.imencode(".png", image)
    assert ok
    doc = fitz.open()
    page = doc.new_page(width=595.276, height=841.89)
    page.insert_image(page.rect, stream=encoded.tobytes())
    doc.save(path)


def main() -> None:
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        x_pdf = td / "x.pdf"
        blank_pdf = td / "blank.pdf"
        make_pdf(x_pdf, True)
        make_pdf(blank_pdf, False)

        x_doc = fitz.open(x_pdf)
        blank_doc = fitz.open(blank_pdf)
        assert raster_candidates(x_doc[0], dpi=150), "raster X must produce a HUMAN_CHECK candidate"
        assert raster_candidates(blank_doc[0], dpi=150) == [], "blank raster must not produce a candidate"
    print("ARC XMARK DETECTOR SMOKE: PASS")


if __name__ == "__main__":
    main()

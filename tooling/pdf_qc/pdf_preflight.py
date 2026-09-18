#!/usr/bin/env python3
import argparse
import json
import math
import shutil
import subprocess
from pathlib import Path

import fitz

BROKEN_GLYPHS = {"�", "□", "■"}

def rect_outside(inner, outer, tol=0.5):
    return inner.x0 < outer.x0 - tol or inner.y0 < outer.y0 - tol or inner.x1 > outer.x1 + tol or inner.y1 > outer.y1 + tol

def overlap_ratio(a, b):
    inter = a & b
    if inter.is_empty:
        return 0.0
    ia = max(0.0, inter.width) * max(0.0, inter.height)
    ma = max(1e-6, min(a.width * a.height, b.width * b.height))
    return ia / ma

def page_report(page, margin_pt, overlap_threshold):
    page_rect = page.rect
    safe = fitz.Rect(
        page_rect.x0 + margin_pt,
        page_rect.y0 + margin_pt,
        page_rect.x1 - margin_pt,
        page_rect.y1 - margin_pt,
    )
    flags = []

    words = page.get_text("words")
    text = page.get_text("text")
    blocks = page.get_text("blocks")

    if not text.strip() and not page.get_images(full=True) and not page.get_drawings():
        flags.append({"severity": "WARN", "type": "EMPTY_PAGE"})

    if any(g in text for g in BROKEN_GLYPHS):
        flags.append({"severity": "FAIL", "type": "BROKEN_GLYPH_CANDIDATE"})

    word_rects = []
    for w in words:
        r = fitz.Rect(w[:4])
        token = str(w[4])
        if rect_outside(r, page_rect):
            flags.append({"severity": "FAIL", "type": "TEXT_OUTSIDE_PAGE", "token": token, "bbox": list(r)})
        elif rect_outside(r, safe):
            flags.append({"severity": "WARN", "type": "TEXT_IN_MARGIN", "token": token, "bbox": list(r)})
        word_rects.append((r, token, int(w[5]), int(w[6]), int(w[7])))

    # Suspicious word overlap. Ignore words from the same text line.
    for i in range(len(word_rects)):
        a, ta, ba, la, wa = word_rects[i]
        for j in range(i + 1, len(word_rects)):
            b, tb, bb, lb, wb = word_rects[j]
            if ba == bb and la == lb:
                continue
            ratio = overlap_ratio(a, b)
            if ratio >= overlap_threshold:
                flags.append({
                    "severity": "WARN",
                    "type": "TEXT_TEXT_OVERLAP",
                    "a": ta,
                    "b": tb,
                    "ratio": round(ratio, 3),
                    "bbox_a": list(a),
                    "bbox_b": list(b),
                })

    for img in page.get_images(full=True):
        xref = img[0]
        for r in page.get_image_rects(xref):
            if rect_outside(r, page_rect):
                flags.append({"severity": "FAIL", "type": "IMAGE_OUTSIDE_PAGE", "xref": xref, "bbox": list(r)})

    for d in page.get_drawings():
        r = d.get("rect")
        if r and rect_outside(r, page_rect):
            flags.append({"severity": "FAIL", "type": "DRAWING_OUTSIDE_PAGE", "bbox": list(r)})

    return {
        "page": page.number + 1,
        "page_size_pt": [page_rect.width, page_rect.height],
        "word_count": len(words),
        "block_count": len(blocks),
        "flags": flags,
    }

def render_pdf(pdf_path, outdir, dpi=150):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    pdftoppm = shutil.which("pdftoppm")
    if pdftoppm:
        prefix = outdir / "page"
        proc = subprocess.run(
            [pdftoppm, "-png", "-r", str(dpi), str(pdf_path), str(prefix)],
            capture_output=True,
            text=True,
        )
        return {"renderer": "pdftoppm", "ok": proc.returncode == 0, "stderr": proc.stderr[-1000:]}
    doc = fitz.open(pdf_path)
    zoom = dpi / 72.0
    for page in doc:
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        pix.save(outdir / f"page-{page.number + 1:03d}.png")
    return {"renderer": "pymupdf", "ok": True}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--margin-pt", type=float, default=18.0)
    ap.add_argument("--overlap-threshold", type=float, default=0.30)
    ap.add_argument("--report", default=None)
    ap.add_argument("--render-dir", default=None)
    ap.add_argument("--dpi", type=int, default=150)
    args = ap.parse_args()

    doc = fitz.open(args.pdf)
    pages = [page_report(p, args.margin_pt, args.overlap_threshold) for p in doc]
    fail_count = sum(1 for p in pages for f in p["flags"] if f["severity"] == "FAIL")
    warn_count = sum(1 for p in pages for f in p["flags"] if f["severity"] == "WARN")
    status = "FAIL" if fail_count else ("WARN" if warn_count else "PASS")

    render = None
    if args.render_dir:
        render = render_pdf(args.pdf, args.render_dir, args.dpi)
        if not render.get("ok"):
            status = "FAIL"
            fail_count += 1

    result = {
        "tool": "ARC_PDF_PREFLIGHT_V1.0",
        "pdf": str(args.pdf),
        "status": status,
        "page_count": len(pages),
        "fail_count": fail_count,
        "warn_count": warn_count,
        "render": render,
        "pages": pages,
    }

    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        Path(args.report).write_text(text, encoding="utf-8")
    print(text)
    raise SystemExit(1 if status == "FAIL" else 0)

if __name__ == "__main__":
    main()

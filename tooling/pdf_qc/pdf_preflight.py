#!/usr/bin/env python3
"""ARC PDF deterministic preflight V1.2.

Focuses on rendered-PDF invariants. It does not replace source-level HTML
overflow checks or human visual review.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Iterable

import fitz

A4_W = 595.276
A4_H = 841.890
PAGE_TOLERANCE_PT = 2.0
BROKEN_GLYPHS = {"�"}
RAW_MARKUP_RE = re.compile(r"<\s*/?\s*(?:br|b|i|span)\b[^>]*>", re.I)
METADATA_RE = re.compile(
    r"(?:CONTENT_LOCK|HANDOFF_STATUS|CONTENT_QA_STATUS|BATCH_ID|SOURCE_ID|"
    r"DRIVE[_ ]?(?:ID|STATUS)|READY_FOR_TYPESET|PDF_QC_STATUS|"
    r"TYPESET_STATUS|STUDENT_METADATA_LEAK)",
    re.I,
)
LIGHT_FONT_RE = re.compile(r"(?:thin|extralight|ultralight|light|wght[-_ ]?(?:100|200|300))", re.I)
BOLD_FONT_RE = re.compile(r"(?:bold|semibold|demibold|medium)", re.I)


def rect_outside(inner: fitz.Rect, outer: fitz.Rect, tol: float = 0.5) -> bool:
    return (
        inner.x0 < outer.x0 - tol
        or inner.y0 < outer.y0 - tol
        or inner.x1 > outer.x1 + tol
        or inner.y1 > outer.y1 + tol
    )


def overlap_ratio(a: fitz.Rect, b: fitz.Rect) -> float:
    inter = a & b
    if inter.is_empty:
        return 0.0
    ia = max(0.0, inter.width) * max(0.0, inter.height)
    ma = max(1e-6, min(a.width * a.height, b.width * b.height))
    return ia / ma


def merge_intervals(intervals: Iterable[tuple[float, float]]) -> list[tuple[float, float]]:
    rows = sorted((float(a), float(b)) for a, b in intervals if b > a)
    merged: list[list[float]] = []
    for a, b in rows:
        if not merged or a > merged[-1][1] + 0.5:
            merged.append([a, b])
        else:
            merged[-1][1] = max(merged[-1][1], b)
    return [(a, b) for a, b in merged]


def interval_union_length(intervals: Iterable[tuple[float, float]]) -> float:
    return sum(b - a for a, b in merge_intervals(intervals))


def text_blocks(page: fitz.Page) -> list[dict]:
    """Return normalized text blocks from PyMuPDF dict output."""
    out: list[dict] = []
    data = page.get_text("dict")
    for block in data.get("blocks", []):
        if block.get("type") != 0:
            continue
        spans = []
        text_parts = []
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span.get("text", "")
                if text:
                    text_parts.append(text)
                    spans.append(
                        {
                            "text": text,
                            "font": str(span.get("font", "")),
                            "size": float(span.get("size", 0.0)),
                            "bbox": list(span.get("bbox", (0, 0, 0, 0))),
                        }
                    )
        text = "".join(text_parts).strip()
        if not text:
            continue
        out.append({"bbox": list(block.get("bbox", (0, 0, 0, 0))), "text": text, "spans": spans})
    return out


def body_typography(blocks: list[dict], page_height: float) -> dict:
    total_chars = 0
    weighted_size = 0.0
    light_chars = 0
    font_chars: dict[str, int] = {}
    for block in blocks:
        x0, y0, x1, y1 = block["bbox"]
        if y1 < page_height * 0.07 or y0 > page_height * 0.94:
            continue
        for span in block["spans"]:
            size = span["size"]
            text = span["text"].strip()
            chars = len(text)
            if chars == 0 or not (7.0 <= size <= 12.8):
                continue
            total_chars += chars
            weighted_size += size * chars
            font = span["font"]
            font_chars[font] = font_chars.get(font, 0) + chars
            if LIGHT_FONT_RE.search(font):
                light_chars += chars
    avg_size = weighted_size / total_chars if total_chars else None
    light_ratio = light_chars / total_chars if total_chars else 0.0
    top_fonts = sorted(font_chars.items(), key=lambda kv: kv[1], reverse=True)[:8]
    return {
        "body_chars": total_chars,
        "body_font_avg_pt": round(avg_size, 3) if avg_size is not None else None,
        "light_body_ratio": round(light_ratio, 4),
        "body_fonts": top_fonts,
    }


def occupancy_ratio(blocks: list[dict], page_height: float, top: float, bottom: float) -> float:
    intervals: list[tuple[float, float]] = []
    for block in blocks:
        _x0, y0, _x1, y1 = block["bbox"]
        a = max(top, y0)
        b = min(bottom, y1)
        if b > a:
            intervals.append((a, b))
    usable = max(1.0, bottom - top)
    return min(1.0, interval_union_length(intervals) / usable)


def column_signal(blocks: list[dict], page_rect: fitz.Rect) -> dict:
    """Conservative two-lane body detector, designed to ignore ordinary table cells."""
    mid = page_rect.width / 2.0
    lane_limit = page_rect.width * 0.49
    gutter = page_rect.width * 0.035
    body_top = page_rect.height * 0.08
    body_bottom = page_rect.height * 0.92

    left: list[dict] = []
    right: list[dict] = []
    for block in blocks:
        text = re.sub(r"\s+", " ", block["text"]).strip()
        x0, y0, x1, y1 = block["bbox"]
        width = x1 - x0
        if len(text) < 90 or width <= 0 or width > lane_limit:
            continue
        if y1 < body_top or y0 > body_bottom:
            continue
        item = {"bbox": block["bbox"], "chars": len(text)}
        if x1 <= mid + gutter:
            left.append(item)
        elif x0 >= mid - gutter:
            right.append(item)

    left_chars = sum(x["chars"] for x in left)
    right_chars = sum(x["chars"] for x in right)
    left_y = [(x["bbox"][1], x["bbox"][3]) for x in left]
    right_y = [(x["bbox"][1], x["bbox"][3]) for x in right]

    overlap_y = 0.0
    for la, lb in merge_intervals(left_y):
        for ra, rb in merge_intervals(right_y):
            overlap_y += max(0.0, min(lb, rb) - max(la, ra))
    usable = max(1.0, body_bottom - body_top)
    overlap_ratio_y = overlap_y / usable

    detected = (
        len(left) >= 2
        and len(right) >= 2
        and left_chars >= 220
        and right_chars >= 220
        and overlap_ratio_y >= 0.18
    )
    return {
        "detected": detected,
        "left_blocks": len(left),
        "right_blocks": len(right),
        "left_chars": left_chars,
        "right_chars": right_chars,
        "vertical_overlap_ratio": round(overlap_ratio_y, 4),
    }


def heading_orphan_flags(blocks: list[dict], page_rect: fitz.Rect, body_avg: float | None) -> list[dict]:
    flags: list[dict] = []
    if not blocks:
        return flags
    size_base = body_avg or 9.9
    threshold_y = page_rect.height * 0.78
    footer_cut = page_rect.height * 0.94
    for block in blocks:
        text = re.sub(r"\s+", " ", block["text"]).strip()
        x0, y0, x1, y1 = block["bbox"]
        if y0 < threshold_y or y0 > footer_cut or len(text) > 110:
            continue
        max_size = max((span["size"] for span in block["spans"]), default=0)
        boldish = any(BOLD_FONT_RE.search(span["font"]) for span in block["spans"])
        heading_like = max_size >= size_base + 1.2 or (boldish and max_size >= size_base + 0.3)
        if not heading_like:
            continue
        following_chars = 0
        for other in blocks:
            ox0, oy0, ox1, oy1 = other["bbox"]
            if oy0 >= y1 + 0.5 and oy0 < footer_cut:
                following_chars += len(other["text"].strip())
        if following_chars < 90:
            severity = "FAIL" if y0 >= page_rect.height * 0.84 and following_chars < 45 else "WARN"
            flags.append(
                {
                    "severity": severity,
                    "type": "HEADING_ORPHAN_CANDIDATE",
                    "text": text[:120],
                    "bbox": [x0, y0, x1, y1],
                    "following_chars": following_chars,
                }
            )
    return flags


def page_report(
    page: fitz.Page,
    product: str,
    margin_pt: float,
    overlap_threshold: float,
) -> dict:
    page_rect = page.rect
    safe = fitz.Rect(
        page_rect.x0 + margin_pt,
        page_rect.y0 + margin_pt,
        page_rect.x1 - margin_pt,
        page_rect.y1 - margin_pt,
    )
    flags: list[dict] = []

    words = page.get_text("words")
    text = page.get_text("text")
    blocks = text_blocks(page)

    if abs(page_rect.width - A4_W) > PAGE_TOLERANCE_PT or abs(page_rect.height - A4_H) > PAGE_TOLERANCE_PT:
        flags.append(
            {
                "severity": "FAIL",
                "type": "UNEXPECTED_PAGE_SIZE",
                "actual_pt": [round(page_rect.width, 2), round(page_rect.height, 2)],
                "expected_pt": [A4_W, A4_H],
            }
        )

    if not text.strip() and not page.get_images(full=True) and not page.get_drawings():
        flags.append({"severity": "WARN", "type": "EMPTY_PAGE"})

    if any(g in text for g in BROKEN_GLYPHS):
        flags.append({"severity": "FAIL", "type": "BROKEN_GLYPH_CANDIDATE"})

    if RAW_MARKUP_RE.search(text):
        flags.append({"severity": "FAIL", "type": "RAW_MARKUP_LEAK"})

    if METADATA_RE.search(text):
        flags.append({"severity": "FAIL", "type": "STUDENT_METADATA_LEAK"})

    word_rects = []
    for w in words:
        r = fitz.Rect(w[:4])
        token = str(w[4])
        if rect_outside(r, page_rect):
            flags.append({"severity": "FAIL", "type": "TEXT_OUTSIDE_PAGE", "token": token, "bbox": list(r)})
        elif rect_outside(r, safe):
            flags.append({"severity": "WARN", "type": "TEXT_IN_MARGIN", "token": token, "bbox": list(r)})
        word_rects.append((r, token, int(w[5]), int(w[6])))

    # Suspicious word overlap. Ignore words from the same text line.
    # Cap comparison count to avoid quadratic explosions on exceptionally dense pages.
    capped = word_rects[:2200]
    for i in range(len(capped)):
        a, ta, ba, la = capped[i]
        for j in range(i + 1, len(capped)):
            b, tb, bb, lb = capped[j]
            if ba == bb and la == lb:
                continue
            ratio = overlap_ratio(a, b)
            if ratio >= overlap_threshold:
                flags.append(
                    {
                        "severity": "WARN",
                        "type": "TEXT_TEXT_OVERLAP",
                        "a": ta,
                        "b": tb,
                        "ratio": round(ratio, 3),
                        "bbox_a": list(a),
                        "bbox_b": list(b),
                    }
                )
                if sum(1 for x in flags if x["type"] == "TEXT_TEXT_OVERLAP") >= 100:
                    break
        if sum(1 for x in flags if x["type"] == "TEXT_TEXT_OVERLAP") >= 100:
            break

    for img in page.get_images(full=True):
        xref = img[0]
        for r in page.get_image_rects(xref):
            if rect_outside(r, page_rect):
                flags.append({"severity": "FAIL", "type": "IMAGE_OUTSIDE_PAGE", "xref": xref, "bbox": list(r)})

    for drawing in page.get_drawings():
        r = drawing.get("rect")
        if r and rect_outside(r, page_rect):
            flags.append({"severity": "FAIL", "type": "DRAWING_OUTSIDE_PAGE", "bbox": list(r)})

    typo = body_typography(blocks, page_rect.height)
    top = max(margin_pt, page_rect.height * 0.07)
    bottom = min(page_rect.height - margin_pt, page_rect.height * 0.93)
    occ = occupancy_ratio(blocks, page_rect.height, top, bottom)
    cols = column_signal(blocks, page_rect)

    if product == "ARC_CORE" and page.number > 0:
        if occ < 0.25:
            flags.append({"severity": "FAIL", "type": "CORE_NEAR_EMPTY_PAGE", "occupancy_ratio": round(occ, 4)})
        elif occ < 0.45:
            flags.append({"severity": "WARN", "type": "CORE_SPARSE_PAGE_REFLOW", "occupancy_ratio": round(occ, 4)})

        if cols["detected"]:
            flags.append({"severity": "FAIL", "type": "CORE_TWO_COLUMN_FLOW", "details": cols})

        avg = typo["body_font_avg_pt"]
        if typo["body_chars"] >= 180 and avg is not None and avg < 9.2:
            flags.append({"severity": "FAIL", "type": "CORE_BODY_FONT_TOO_SMALL", "avg_pt": avg})
        if typo["body_chars"] >= 180 and typo["light_body_ratio"] > 0.15:
            flags.append(
                {
                    "severity": "FAIL",
                    "type": "CORE_LIGHT_BODY_FONT",
                    "light_body_ratio": typo["light_body_ratio"],
                    "fonts": typo["body_fonts"],
                }
            )

        flags.extend(heading_orphan_flags(blocks, page_rect, typo["body_font_avg_pt"]))

    return {
        "page": page.number + 1,
        "page_size_pt": [round(page_rect.width, 3), round(page_rect.height, 3)],
        "word_count": len(words),
        "block_count": len(blocks),
        "occupancy_ratio": round(occ, 4),
        "typography": typo,
        "column_signal": cols,
        "flags": flags,
    }


def render_pdf(pdf_path: str | Path, outdir: str | Path, dpi: int = 300) -> dict:
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


def analyze_pdf(
    pdf_path: str | Path,
    product: str,
    margin_pt: float = 18.0,
    overlap_threshold: float = 0.30,
    render_dir: str | Path | None = None,
    dpi: int = 300,
) -> dict:
    doc = fitz.open(pdf_path)
    pages = [page_report(p, product, margin_pt, overlap_threshold) for p in doc]
    fail_count = sum(1 for p in pages for f in p["flags"] if f["severity"] == "FAIL")
    warn_count = sum(1 for p in pages for f in p["flags"] if f["severity"] == "WARN")
    status = "FAIL" if fail_count else ("WARN" if warn_count else "PASS")

    render = None
    if render_dir:
        render = render_pdf(pdf_path, render_dir, dpi)
        if not render.get("ok"):
            status = "FAIL"
            fail_count += 1

    return {
        "tool": "ARC_PDF_PREFLIGHT_V1.2",
        "pdf": str(pdf_path),
        "product": product,
        "status": status,
        "page_count": len(pages),
        "fail_count": fail_count,
        "warn_count": warn_count,
        "render": render,
        "pages": pages,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--product", required=True, choices=["ARC_CORE", "ARC_N", "ARC_FINAL"])
    ap.add_argument("--margin-pt", type=float, default=18.0)
    ap.add_argument("--overlap-threshold", type=float, default=0.30)
    ap.add_argument("--report", default=None)
    ap.add_argument("--render-dir", default=None)
    ap.add_argument("--dpi", type=int, default=300)
    args = ap.parse_args()

    result = analyze_pdf(
        args.pdf,
        product=args.product,
        margin_pt=args.margin_pt,
        overlap_threshold=args.overlap_threshold,
        render_dir=args.render_dir,
        dpi=args.dpi,
    )
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        Path(args.report).write_text(output, encoding="utf-8")
    print(output)
    raise SystemExit(1 if result["status"] == "FAIL" else 0)


if __name__ == "__main__":
    main()

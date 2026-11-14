#!/usr/bin/env python3
"""Production renderer for ARC_CORE Pure B&W Open Editorial study books (KOR, SOC, SCI).

Implements `templates/core/ARC_CORE_BW_OPEN_EDITORIAL_V1.0.md`:
- Wide 1-column layout (`ONE_COLUMN`, `CORE_TWO_COLUMN_FLOW = 0`), generous 52pt margins
- Pure black & white monochrome aesthetic matching ARC N° and ARC FINAL
- Zero 4-sided card boxes; uses left accent bars, Booktabs horizontal-rule tables,
  compact borderless A-vs-B contrast micro-grids, and numbered option verification rows
- Typography floor >= 9.2pt (9.9pt body, 1.62 line-height) with strict orphan prevention
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
from typing import Any

import fitz

ROOT = Path(__file__).resolve().parents[2]
_kor_spec = importlib.util.spec_from_file_location("arc_kor_renderer", ROOT / "tooling/typeset/kor_renderer.py")
kor = importlib.util.module_from_spec(_kor_spec)
assert _kor_spec and _kor_spec.loader
_kor_spec.loader.exec_module(kor)

A4_W, A4_H = kor.A4_W, kor.A4_H
ML, MR = 52.0, 52.0
BODY_W = A4_W - ML - MR
CONTENT_TOP = 64.0
CONTENT_BOTTOM = A4_H - 54.0
BLACK = (0.0, 0.0, 0.0)
BODY_INK = (0.10, 0.10, 0.10)
MUTED = (0.38, 0.38, 0.38)
TINT = (0.96, 0.96, 0.96)
HAIR = (0.78, 0.78, 0.78)


class CoreRenderError(RuntimeError):
    pass


class CoreLayout(kor.Layout):
    pass


def wrap_paragraphs(L: CoreLayout, text: str, width: float, font_key: str, size: float, first_indent: float = 0.0, rest_indent: float = 0.0) -> list[tuple[float, str]]:
    lines: list[tuple[float, str]] = []
    paras = str(text or "").split("\n")
    for p_idx, para in enumerate(paras):
        clean = " ".join(para.split())
        if not clean:
            if p_idx > 0 and p_idx < len(paras) - 1:
                lines.append((first_indent, ""))
            continue
        lines.extend(L.wrap(clean, width, font_key, size, first=first_indent, rest=rest_indent))
    return lines


def _render_cover(doc: fitz.Document, meta: dict[str, Any], logo: dict[str, Any] | None = None) -> str:
    page = kor.new_page(doc)
    brand = "BRAND_ASSET_MISSING"
    top = 186.0
    if logo and Path(logo["path"]).is_file():
        data = Path(logo["path"]).read_bytes()
        if hashlib.sha256(data).hexdigest() != logo["sha256"]:
            raise CoreRenderError("BRAND_HASH_MISMATCH")
        w, h = logo["pixels"]
        box_w = 165.0
        page.insert_image(fitz.Rect(64, 72, 64 + box_w, 72 + box_w * h / w), stream=data, keep_proportion=True)
        brand, top = "PASS", 72 + box_w * h / w + 56
    else:
        kor.put(page, (64, 76), "ARC SYSTEM  ·  DONGBUK HIGH SCHOOL", fontname="GB", fontsize=10.0, color=BLACK)
        page.draw_line((64, 86), (A4_W - 64, 86), color=BLACK, width=1.0)
        page.draw_rect(fitz.Rect(64, 112, 164, 136), color=BLACK, width=0.9)
        kor.put(page, (78, 128), "ARC CORE", fontname="GB", fontsize=9.4, color=BLACK)

    set_label = str(meta.get("set_label") or "ARC CORE")
    course = str(meta.get("course") or "")
    sub = str(meta.get("cover_subtitle") or meta.get("scope") or "")
    kor.put(page, (64, top), set_label, fontname="GB", fontsize=28, color=BLACK)
    if course:
        kor.put(page, (64, top + 40), course, fontname="GB", fontsize=20, color=BLACK)
    if sub:
        kor.put(page, (64, top + 72), sub, fontname="G", fontsize=12.0, color=MUTED)
    rule_y = top + 96
    page.draw_line((64, rule_y), (A4_W - 64, rule_y), color=BLACK, width=0.9)
    school = str(meta.get("school_line") or "동북고등학교")
    if "동북고" not in school:
        school = f"동북고등학교  |  {school}"
    kor.put(page, (64, 768), school, fontname="GB", fontsize=10.5, color=BLACK)
    return brand


def _new_body_page(doc: fitz.Document, L: CoreLayout, header_right: str, page_num: int) -> tuple[fitz.Page, float]:
    page = kor.new_page(doc)
    kor.put(page, (ML, 38), "ARC CORE", fontname="GB", fontsize=9.0, color=BLACK)
    rw = L.width(header_right, "G", 8.0)
    kor.put(page, (A4_W - MR - rw, 38), header_right, fontname="G", fontsize=8.0, color=MUTED)
    page.draw_line((ML, 46), (A4_W - MR, 46), color=BLACK, width=0.65)

    page.draw_line((ML, A4_H - 42), (A4_W - MR, A4_H - 42), color=HAIR, width=0.4)
    kor.put(page, (ML, A4_H - 28), "ARC CORE  ·  PURE B&W OPEN EDITORIAL", fontname="G", fontsize=7.6, color=MUTED)
    pstr = f"{page_num:02d}"
    pw = L.width(pstr, "GB", 8.8)
    kor.put(page, (A4_W - MR - pw, A4_H - 28), pstr, fontname="GB", fontsize=8.8, color=BLACK)
    return page, CONTENT_TOP


def render_core(bundle: dict[str, Any], out_pdf: Path, logo: dict[str, Any] | None = None) -> dict[str, Any]:
    """Render an ARC_CORE Pure B&W Open Editorial PDF from normalized core bundle YAML."""
    L = CoreLayout()
    doc = fitz.open()
    brand = _render_cover(doc, bundle, logo)
    # Minimalist B&W cover keeps verso page count consistent if desired or starts unit 1 directly on page 2.
    # Keep unit 1 cleanly on physical page 2 (cover_verso_blank is False for ARC_CORE in typesetter_gateway).
    units = bundle.get("units") or []
    if not units and bundle.get("sections"):
        units = [{
            "unit_kicker": bundle.get("unit_kicker", "CORE UNIT 01"),
            "title": bundle.get("title") or bundle.get("scope", ""),
            "sections": bundle["sections"],
        }]
    if not units:
        raise CoreRenderError("ARC_CORE bundle needs at least one unit or sections list")

    pno = 1
    course = str(bundle.get("course") or "")
    school = str(bundle.get("school_line") or "동북고등학교")

    def ensure_space(need_h: float, page: fitz.Page, y: float, hdr_r: str) -> tuple[fitz.Page, float]:
        nonlocal pno
        if y + need_h <= CONTENT_BOTTOM:
            return page, y
        pno += 1
        return _new_body_page(doc, L, hdr_r, pno)

    for u_idx, unit in enumerate(units):
        unit_title = str(unit.get("title") or "")
        kicker = str(unit.get("unit_kicker") or f"UNIT {u_idx + 1:02d}")
        hdr_r = f"{school}  |  {course} · {unit_title}" if course else f"{school}  |  {unit_title}"
        if L.width(hdr_r, "G", 8.0) > BODY_W - 95:
            hdr_r = hdr_r[:42] + "…"
        if u_idx > 0 or True:
            page, y = _new_body_page(doc, L, hdr_r, pno)
            pno += 1

        # Open Chapter Header (no closed 4-sided box)
        kor.put(page, (ML, y + 8), kicker, fontname="GB", fontsize=8.4, color=MUTED)
        y += 14.0
        title_lines = wrap_paragraphs(L, unit_title, BODY_W, "GB", 15.8)
        for indent, line in title_lines:
            kor.put(page, (ML + indent, y + 15.8), line, fontname="GB", fontsize=15.8, color=BLACK)
            y += 22.0
        page.draw_line((ML, y + 4), (A4_W - MR, y + 4), color=BLACK, width=1.4)
        y += 22.0

        # Adjust pno tracker since _new_body_page received pno before increment
        def next_pg() -> tuple[fitz.Page, float]:
            nonlocal pno
            pg, ny = _new_body_page(doc, L, hdr_r, pno)
            pno += 1
            return pg, ny

        for s_idx, sec in enumerate(unit.get("sections", []), start=1):
            sec_no = str(sec.get("no") or f"{s_idx:02d}")
            thesis = str(sec.get("heading") or sec.get("thesis") or "").strip()
            prose = str(sec.get("prose") or sec.get("explanation") or "").strip()

            # Keep section heading + first few prose lines together (orphan prevention)
            head_lines = wrap_paragraphs(L, thesis, BODY_W - 26, "GB", 11.0) if thesis else []
            prose_lines = wrap_paragraphs(L, prose, BODY_W - 26, "R", 9.9) if prose else []
            first_chunk_h = len(head_lines) * 16.5 + min(len(prose_lines), 3) * 16.0 + 18.0
            if y + first_chunk_h > CONTENT_BOTTOM and y > CONTENT_TOP + 20:
                page, y = next_pg()

            if thesis:
                kor.put(page, (ML, y + 11.0), sec_no, fontname="GB", fontsize=11.0, color=BLACK)
                for indent, line in head_lines:
                    kor.put(page, (ML + 26 + indent, y + 11.0), line, fontname="GB", fontsize=11.0, color=BLACK)
                    y += 16.0
                y += 3.0

            if prose_lines:
                for indent, line in prose_lines:
                    if y + 15.2 > CONTENT_BOTTOM:
                        page, y = next_pg()
                    if line:
                        kor.put(page, (ML + 26 + indent, y + 9.9), line, fontname="R", fontsize=9.9, color=BODY_INK)
                    y += 15.2
                y += 6.0

            # Optional Left-Bar Callout (.callout-bar)
            for callout in sec.get("callouts", []):
                c_title = str(callout.get("label") or "").strip()
                c_body = str(callout.get("text") or "").strip()
                inner_w = BODY_W - 26 - 24
                c_lines: list[tuple[str, float, str]] = []
                if c_title:
                    for _, l in wrap_paragraphs(L, c_title, inner_w, "GB", 9.6):
                        c_lines.append(("GB", 9.6, l))
                if c_body:
                    for _, l in wrap_paragraphs(L, c_body, inner_w, "R", 9.5):
                        c_lines.append(("R", 9.5, l))
                ch = len(c_lines) * 14.6 + 14.0
                if y + ch > CONTENT_BOTTOM and y > CONTENT_TOP + 20:
                    page, y = next_pg()
                page.draw_rect(fitz.Rect(ML + 26, y, A4_W - MR, y + ch), color=None, fill=TINT, width=0)
                page.draw_line((ML + 26, y), (ML + 26, y + ch), color=BLACK, width=2.5)
                cy = y + 8.0
                for fk, fsz, l in c_lines:
                    kor.put(page, (ML + 38, cy + fsz), l, fontname=fk, fontsize=fsz, color=BLACK if fk == "GB" else BODY_INK)
                    cy += 14.6
                y += ch + 11.0

            # Optional Booktabs Open Table (zero vertical lines)
            for tbl in sec.get("tables", []):
                cols = tbl.get("headers") or []
                rows = tbl.get("rows") or []
                if not cols:
                    continue
                tx = ML + 26
                tw = BODY_W - 26
                ncols = len(cols)
                weights = tbl.get("weights") or [1.0] * ncols
                wsum = sum(weights)
                cws = [tw * w / wsum for w in weights]
                # Precompute heights
                row_heights: list[float] = []
                wrapped_rows: list[list[list[str]]] = []
                for row in rows:
                    cell_lines: list[list[str]] = []
                    max_l = 1
                    for ci, cell in enumerate(row):
                        fk = "GB" if ci == 0 else "R"
                        ls = [l for _, l in wrap_paragraphs(L, str(cell), cws[ci] - 12, fk, 9.3)] or [""]
                        cell_lines.append(ls)
                        max_l = max(max_l, len(ls))
                    wrapped_rows.append(cell_lines)
                    row_heights.append(max_l * 13.8 + 8.0)
                total_th = 22.0 + sum(row_heights) + 6.0
                if y + total_th > CONTENT_BOTTOM and y > CONTENT_TOP + 20:
                    page, y = next_pg()
                page.draw_line((tx, y), (tx + tw, y), color=BLACK, width=1.1)
                cx = tx
                for ci, h in enumerate(cols):
                    kor.put(page, (cx + 4, y + 14.5), str(h), fontname="GB", fontsize=9.2, color=BLACK)
                    cx += cws[ci]
                y += 20.0
                page.draw_line((tx, y), (tx + tw, y), color=BLACK, width=0.65)
                for r_idx, (cell_lines, rh) in enumerate(zip(wrapped_rows, row_heights)):
                    cx = tx
                    for ci, ls in enumerate(cell_lines):
                        fk = "GB" if ci == 0 else "R"
                        for li, line in enumerate(ls):
                            kor.put(page, (cx + 4, y + 13.5 + li * 13.8), line, fontname=fk, fontsize=9.3, color=BLACK if ci == 0 else BODY_INK)
                        cx += cws[ci]
                    y += rh
                    if r_idx < len(wrapped_rows) - 1:
                        page.draw_line((tx, y), (tx + tw, y), color=HAIR, width=0.4)
                page.draw_line((tx, y), (tx + tw, y), color=BLACK, width=0.95)
                y += 12.0

            # Optional Compact Contrast Micro-Grid (A vs B, <= 6 lines per side to keep CORE_TWO_COLUMN_FLOW=0)
            for contrast in sec.get("contrasts", []):
                left_t = str(contrast.get("left_title") or "")
                left_b = str(contrast.get("left_body") or "")
                right_t = str(contrast.get("right_title") or "")
                right_b = str(contrast.get("right_body") or "")
                col_w = (BODY_W - 26 - 24) / 2
                ll = wrap_paragraphs(L, left_b, col_w, "R", 9.3)[:6]
                rl = wrap_paragraphs(L, right_b, col_w, "R", 9.3)[:6]
                ch = max(len(ll), len(rl), 1) * 14.0 + 28.0
                if y + ch > CONTENT_BOTTOM and y > CONTENT_TOP + 20:
                    page, y = next_pg()
                x0 = ML + 26
                mid_x = x0 + col_w + 12
                page.draw_line((x0, y), (A4_W - MR, y), color=BLACK, width=1.0)
                page.draw_line((mid_x, y + 5), (mid_x, y + ch - 5), color=HAIR, width=0.5)
                kor.put(page, (x0 + 4, y + 16), left_t, fontname="GB", fontsize=9.8, color=BLACK)
                kor.put(page, (mid_x + 10, y + 16), right_t, fontname="GB", fontsize=9.8, color=BLACK)
                for li, (_, line) in enumerate(ll):
                    kor.put(page, (x0 + 4, y + 32 + li * 14.0), line, fontname="R", fontsize=9.3, color=BODY_INK)
                for li, (_, line) in enumerate(rl):
                    kor.put(page, (mid_x + 10, y + 32 + li * 14.0), line, fontname="R", fontsize=9.3, color=BODY_INK)
                y += ch
                page.draw_line((x0, y), (A4_W - MR, y), color=BLACK, width=0.8)
                y += 12.0

            # Optional Discrimination Callout Points (.core-disc)
            for disc in sec.get("discriminations", []):
                d_title = str(disc.get("title") or "")
                d_body = str(disc.get("body") or "")
                d_t_lines = wrap_paragraphs(L, d_title, BODY_W - 38, "GB", 9.6)
                d_b_lines = wrap_paragraphs(L, d_body, BODY_W - 38, "R", 9.5)
                dh = len(d_t_lines) * 14.4 + len(d_b_lines) * 14.6 + 6.0
                if y + dh > CONTENT_BOTTOM and y > CONTENT_TOP + 20:
                    page, y = next_pg()
                start_y = y
                for _, line in d_t_lines:
                    kor.put(page, (ML + 38, y + 10.5), line, fontname="GB", fontsize=9.6, color=BLACK)
                    y += 14.4
                for _, line in d_b_lines:
                    kor.put(page, (ML + 38, y + 9.5), line, fontname="R", fontsize=9.5, color=BODY_INK)
                    y += 14.6
                page.draw_line((ML + 26, start_y + 1), (ML + 26, y - 2), color=BLACK, width=2.0)
                y += 8.0

            # Optional Proposition Verification Rows (.core-check)
            checks = sec.get("option_checks") or []
            if checks:
                if y + 32.0 > CONTENT_BOTTOM and y > CONTENT_TOP + 20:
                    page, y = next_pg()
                page.draw_line((ML + 26, y), (A4_W - MR, y), color=BLACK, width=0.85)
                y += 6.0
                for ci, chk in enumerate(checks):
                    stmt = str(chk.get("statement") or "")
                    why = str(chk.get("why") or "")
                    s_lines = wrap_paragraphs(L, stmt, BODY_W - 32, "GB", 9.5)
                    w_lines = wrap_paragraphs(L, why, BODY_W - 32, "R", 9.3)
                    ch = len(s_lines) * 14.2 + len(w_lines) * 14.2 + 8.0
                    if y + ch > CONTENT_BOTTOM and y > CONTENT_TOP + 20:
                        page, y = next_pg()
                    for _, line in s_lines:
                        kor.put(page, (ML + 30, y + 9.5), line, fontname="GB", fontsize=9.5, color=BLACK)
                        y += 14.2
                    for _, line in w_lines:
                        kor.put(page, (ML + 30, y + 9.3), line, fontname="R", fontsize=9.3, color=MUTED)
                        y += 14.2
                    y += 3.0
                    if ci < len(checks) - 1:
                        page.draw_line((ML + 26, y), (A4_W - MR, y), color=HAIR, width=0.4)
                    y += 6.0

    doc.subset_fonts()
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_pdf, garbage=4, deflate=True)
    pages = len(doc)
    doc.close()
    return {"status": "PASS", "pages": pages, "brand": brand, "product": "ARC_CORE", "pdf": str(out_pdf)}

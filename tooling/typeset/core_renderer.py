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



BULLETS = ("· ", "- ", "• ", "① ", "② ", "③ ", "④ ", "⑤ ", "⑥ ", "⑦ ", "1단계", "2단계", "3단계", "[")


def _bullet_lines(L: "CoreLayout", text: str, width: float, font_key: str, size: float) -> list[tuple[float, str]]:
    """Wrap text; lines that start with a bullet/step marker get a hanging indent."""
    out: list[tuple[float, str]] = []
    for para in str(text or "").split("\n"):
        clean = " ".join(para.split())
        if not clean:
            continue
        hang = 0.0
        for b in BULLETS:
            if clean.startswith(b) and b != "[":
                hang = L.width(b.split(" ")[0] + " ", font_key, size) if " " in b else L.width(b + " ", font_key, size)
                break
        out.extend(L.wrap(clean, width, font_key, size, first=0.0, rest=hang))
    return out


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

        def _draw_block(blk: dict[str, Any], page: fitz.Page, y: float, next_pg) -> tuple[fitz.Page, float]:
            kind = blk.get("type")
            x0 = ML + 26
            if kind == "prose":
                for indent, line in _bullet_lines(L, str(blk.get("text") or ""), BODY_W - 26, "R", 9.9):
                    if y + 15.2 > CONTENT_BOTTOM:
                        page, y = next_pg()
                    kor.put(page, (x0 + indent, y + 9.9), line, fontname="R", fontsize=9.9, color=BODY_INK)
                    y += 15.2
                return page, y + 6.0
            if kind in ("callout", "key"):
                style = "key" if kind == "key" else str(blk.get("style") or "tint")
                c_title = str(blk.get("label") or "").strip()
                inner_w = BODY_W - 26 - 24
                body = _bullet_lines(L, str(blk.get("text") or ""), inner_w, "R", 9.5)
                tab_h = 20.0 if (style == "key" and c_title) else 0.0
                t_lines = [] if tab_h else [l for _, l in wrap_paragraphs(L, c_title, inner_w, "GB", 9.6)] if c_title else []
                rows = [("GB", 9.6, 0.0, l) for l in t_lines] + [("R", 9.5, ind, l) for ind, l in body]
                min_h = tab_h + min(len(rows), 4) * 14.6 + 14.0
                if y + min_h > CONTENT_BOTTOM and y > CONTENT_TOP + 20:
                    page, y = next_pg()
                idx = 0
                first = True
                while True:
                    avail = CONTENT_BOTTOM - y - (tab_h if first else 0.0) - 14.0
                    n = max(1, int(avail // 14.6))
                    chunk = rows[idx: idx + n]
                    ch = len(chunk) * 14.6 + 14.0
                    top = y
                    if first and tab_h:
                        tw = L.width(c_title, "GB", 9.4) + 20
                        page.draw_rect(fitz.Rect(x0, y, x0 + tw, y + tab_h), color=None, fill=BLACK, width=0)
                        kor.put(page, (x0 + 10, y + 14.0), c_title, fontname="GB", fontsize=9.4, color=(1, 1, 1))
                        page.draw_line((x0, y + tab_h), (A4_W - MR, y + tab_h), color=BLACK, width=1.2)
                        top = y + tab_h
                    page.draw_rect(fitz.Rect(x0, top, A4_W - MR, top + ch), color=None, fill=TINT, width=0)
                    page.draw_line((x0, top), (x0, top + ch), color=BLACK, width=2.5)
                    cy = top + 8.0
                    for fk, fsz, ind, l in chunk:
                        kor.put(page, (x0 + 12 + ind, cy + fsz), l, fontname=fk, fontsize=fsz, color=BLACK if fk == "GB" else BODY_INK)
                        cy += 14.6
                    y = top + ch
                    idx += len(chunk)
                    first = False
                    if idx >= len(rows):
                        break
                    page, y = next_pg()
                return page, y + 11.0
            if kind == "steps":
                label = str(blk.get("label") or "")
                steps = blk.get("items") or []
                total = (18.0 if label else 0.0) + sum(
                    24.0 + len(wrap_paragraphs(L, str(st.get("body") or ""), BODY_W - 26 - 34, "R", 9.4)) * 14.2 for st in steps) + 4.0
                if y + total + 46.0 > CONTENT_BOTTOM and total <= CONTENT_BOTTOM - CONTENT_TOP - 46.0 and y > CONTENT_TOP + 20:
                    page, y = next_pg()
                if label:
                    if y + 50 > CONTENT_BOTTOM:
                        page, y = next_pg()
                    kor.put(page, (x0, y + 10.0), label, fontname="GB", fontsize=9.8, color=BLACK)
                    y += 18.0
                for i, st in enumerate(steps, 1):
                    head = str(st.get("title") or "")
                    lines = wrap_paragraphs(L, str(st.get("body") or ""), BODY_W - 26 - 34, "R", 9.4)
                    h = 16.0 + len(lines) * 14.2 + 8.0
                    if y + h > CONTENT_BOTTOM and y > CONTENT_TOP + 20:
                        page, y = next_pg()
                    page.draw_circle((x0 + 10, y + 8), 9.0, color=BLACK, fill=BLACK, width=0)
                    num = str(st.get("mark") or i)
                    kor.put(page, (x0 + 10 - L.width(num, "GB", 9.0) / 2, y + 11.2), num, fontname="GB", fontsize=9.0, color=(1, 1, 1))
                    kor.put(page, (x0 + 26, y + 11.5), head, fontname="GB", fontsize=9.9, color=BLACK)
                    yy = y + 16.0
                    for _, l in lines:
                        kor.put(page, (x0 + 26, yy + 9.4), l, fontname="R", fontsize=9.4, color=BODY_INK)
                        yy += 14.2
                    if i < len(steps):
                        page.draw_line((x0 + 10, y + 18), (x0 + 10, yy + 4), color=HAIR, width=0.8)
                    y = yy + 8.0
                return page, y + 4.0
            if kind == "table":
                cols = blk.get("headers") or []
                rows = blk.get("rows") or []
                cap = str(blk.get("caption") or "")
                tw = BODY_W - 26
                ncols = len(cols)
                weights = blk.get("weights") or [1.0] * ncols
                cws = [tw * w / sum(weights) for w in weights]
                wrapped, heights = [], []
                for row in rows:
                    cl = []
                    for ci, cell in enumerate(row):
                        fk = "GB" if ci == 0 else "R"
                        cl.append([l for _, l in wrap_paragraphs(L, str(cell), cws[ci] - 12, fk, 9.3)] or [""])
                    wrapped.append(cl)
                    heights.append(max(len(c) for c in cl) * 13.8 + 8.0)
                need = (18.0 if cap else 0.0) + 22.0 + sum(heights[:3]) + 6.0
                if y + need > CONTENT_BOTTOM and y > CONTENT_TOP + 20:
                    page, y = next_pg()
                if cap:
                    kor.put(page, (x0, y + 10.0), cap, fontname="GB", fontsize=9.6, color=BLACK)
                    y += 16.0

                def header(pg, yy):
                    pg.draw_rect(fitz.Rect(x0, yy, x0 + tw, yy + 20), color=None, fill=TINT, width=0)
                    pg.draw_line((x0, yy), (x0 + tw, yy), color=BLACK, width=1.1)
                    cx = x0
                    for ci, h in enumerate(cols):
                        kor.put(pg, (cx + 4, yy + 14.5), str(h), fontname="GB", fontsize=9.2, color=BLACK)
                        cx += cws[ci]
                    pg.draw_line((x0, yy + 20), (x0 + tw, yy + 20), color=BLACK, width=0.65)
                    return yy + 20.0
                y = header(page, y)
                for r_idx, (cl, rh) in enumerate(zip(wrapped, heights)):
                    if y + rh > CONTENT_BOTTOM:
                        page.draw_line((x0, y), (x0 + tw, y), color=BLACK, width=0.95)
                        page, y = next_pg()
                        y = header(page, y)
                    cx = x0
                    for ci, ls in enumerate(cl):
                        fk = "GB" if ci == 0 else "R"
                        for li, line in enumerate(ls):
                            kor.put(page, (cx + 4, y + 13.5 + li * 13.8), line, fontname=fk, fontsize=9.3, color=BLACK if ci == 0 else BODY_INK)
                        cx += cws[ci]
                    y += rh
                    if r_idx < len(wrapped) - 1:
                        page.draw_line((x0, y), (x0 + tw, y), color=HAIR, width=0.4)
                page.draw_line((x0, y), (x0 + tw, y), color=BLACK, width=0.95)
                return page, y + 12.0
            if kind == "contrast":
                col_w = (BODY_W - 26 - 24) / 2
                ll = wrap_paragraphs(L, str(blk.get("left_body") or ""), col_w, "R", 9.3)[:8]
                rl = wrap_paragraphs(L, str(blk.get("right_body") or ""), col_w, "R", 9.3)[:8]
                ch = max(len(ll), len(rl), 1) * 14.0 + 30.0
                if y + ch > CONTENT_BOTTOM and y > CONTENT_TOP + 20:
                    page, y = next_pg()
                mid_x = x0 + col_w + 12
                page.draw_rect(fitz.Rect(x0, y, A4_W - MR, y + 22), color=None, fill=TINT, width=0)
                page.draw_line((x0, y), (A4_W - MR, y), color=BLACK, width=1.0)
                page.draw_line((mid_x, y + 3), (mid_x, y + ch - 3), color=HAIR, width=0.5)
                kor.put(page, (x0 + 6, y + 15.5), str(blk.get("left_title") or ""), fontname="GB", fontsize=9.8, color=BLACK)
                kor.put(page, (mid_x + 10, y + 15.5), str(blk.get("right_title") or ""), fontname="GB", fontsize=9.8, color=BLACK)
                for li, (_, line) in enumerate(ll):
                    kor.put(page, (x0 + 6, y + 36 + li * 14.0), line, fontname="R", fontsize=9.3, color=BODY_INK)
                for li, (_, line) in enumerate(rl):
                    kor.put(page, (mid_x + 10, y + 36 + li * 14.0), line, fontname="R", fontsize=9.3, color=BODY_INK)
                y += ch
                page.draw_line((x0, y), (A4_W - MR, y), color=BLACK, width=0.8)
                return page, y + 12.0
            if kind == "disc":
                d_t = wrap_paragraphs(L, str(blk.get("title") or ""), BODY_W - 38, "GB", 9.6)
                d_b = _bullet_lines(L, str(blk.get("body") or ""), BODY_W - 38, "R", 9.5)
                dh = len(d_t) * 14.4 + len(d_b) * 14.6 + 6.0
                if y + min(dh, 120) > CONTENT_BOTTOM and y > CONTENT_TOP + 20:
                    page, y = next_pg()
                start_y = y
                for _, line in d_t:
                    kor.put(page, (ML + 38, y + 10.5), line, fontname="GB", fontsize=9.6, color=BLACK)
                    y += 14.4
                for ind, line in d_b:
                    if y + 14.6 > CONTENT_BOTTOM:
                        page.draw_line((ML + 26, start_y + 1), (ML + 26, y - 2), color=BLACK, width=2.0)
                        page, y = next_pg()
                        start_y = y
                    kor.put(page, (ML + 38 + ind, y + 9.5), line, fontname="R", fontsize=9.5, color=BODY_INK)
                    y += 14.6
                page.draw_line((ML + 26, start_y + 1), (ML + 26, y - 2), color=BLACK, width=2.0)
                return page, y + 8.0
            if kind == "checks":
                checks = blk.get("items") or []
                if y + 32.0 > CONTENT_BOTTOM and y > CONTENT_TOP + 20:
                    page, y = next_pg()
                page.draw_line((x0, y), (A4_W - MR, y), color=BLACK, width=0.85)
                y += 6.0
                for ci, chk in enumerate(checks):
                    s_lines = wrap_paragraphs(L, str(chk.get("statement") or ""), BODY_W - 32, "GB", 9.5)
                    w_lines = wrap_paragraphs(L, str(chk.get("why") or ""), BODY_W - 32, "R", 9.3)
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
                        page.draw_line((x0, y), (A4_W - MR, y), color=HAIR, width=0.4)
                    y += 6.0
                return page, y
            raise CoreRenderError(f"UNKNOWN_CORE_BLOCK:{kind}")

        for s_idx, sec in enumerate(unit.get("sections", []), start=1):
            sec_no = str(sec.get("no") or f"{s_idx:02d}")
            thesis = str(sec.get("heading") or sec.get("thesis") or "").strip()
            blocks = sec.get("blocks")
            if blocks is None:
                blocks = []
                if sec.get("prose") or sec.get("explanation"):
                    blocks.append({"type": "prose", "text": sec.get("prose") or sec.get("explanation")})
                blocks += [dict(c, type="callout") for c in sec.get("callouts", [])]
                blocks += [dict(t, type="table") for t in sec.get("tables", [])]
                blocks += [dict(c, type="contrast") for c in sec.get("contrasts", [])]
                blocks += [dict(d, type="disc") for d in sec.get("discriminations", [])]
                if sec.get("option_checks"):
                    blocks.append({"type": "checks", "items": sec["option_checks"]})

            head_lines = wrap_paragraphs(L, thesis, BODY_W - 26, "GB", 11.0) if thesis else []
            first = blocks[0] if blocks else {}
            if first.get("type") == "steps":
                first_h = 46.0 + (18.0 if first.get("label") else 0.0) + sum(
                    24.0 + len(wrap_paragraphs(L, str(st.get("body") or ""), BODY_W - 26 - 34, "R", 9.4)) * 14.2
                    for st in (first.get("items") or []))
            else:
                first_h = 60.0 if first.get("type") != "prose" else min(len(wrap_paragraphs(L, str(first.get("text") or ""), BODY_W - 26, "R", 9.9)), 3) * 16.0 + (50.0 if len(blocks) > 1 else 0.0)
            if y + len(head_lines) * 16.5 + first_h + 18.0 > CONTENT_BOTTOM and y > CONTENT_TOP + 20:
                page, y = next_pg()
            if thesis:
                kor.put(page, (ML, y + 11.0), sec_no, fontname="GB", fontsize=11.0, color=BLACK)
                for indent, line in head_lines:
                    kor.put(page, (ML + 26 + indent, y + 11.0), line, fontname="GB", fontsize=11.0, color=BLACK)
                    y += 16.0
                y += 3.0
            for blk in blocks:
                page, y = _draw_block(blk, page, y, next_pg)

    doc.subset_fonts()
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_pdf, garbage=4, deflate=True)
    pages = len(doc)
    doc.close()
    return {"status": "PASS", "pages": pages, "brand": brand, "product": "ARC_CORE", "pdf": str(out_pdf)}

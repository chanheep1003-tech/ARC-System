"""Subject-specific Pure B&W ARC N° sample payloads and vector diagram drawers.

Provides self-contained, curriculum-aligned 6-page sample specifications for:
  - KOR (공통국어2)
  - SOC (통합사회2)
  - SCI (통합과학2)
  - ENG (공통영어1)
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

import fitz

BLACK = (0.0, 0.0, 0.0)
DARK = (0.12, 0.12, 0.12)
MID_GRAY = (0.45, 0.45, 0.45)
RULE_GRAY = (0.72, 0.72, 0.72)
BG_TINT = (0.955, 0.955, 0.955)
BG_TH = (0.92, 0.92, 0.92)
WHITE = (1.0, 1.0, 1.0)


def _draw_kor_freedom_diagram(page: fitz.Page, fk: Any, x0: float, y0: float, x1: float) -> float:
    """Pure B&W conceptual hierarchy comparing Kant and Hegel freedom models."""
    h = 122.0
    page.draw_rect(fitz.Rect(x0, y0, x1, y0 + h), color=BLACK, fill=WHITE, width=0.6)
    w = x1 - x0

    # Top lane: Kant
    fk.put(page, x0 + 7.0, y0 + 13.0, "[칸트] 자유의 이원 구조", key="G_B", fontsize=7.2, color=BLACK)
    k_y = y0 + 20.0
    k_bh = 26.0
    k_w1, k_w2, k_w3 = 72.0, 76.0, 62.0
    k_x1 = x0 + 7.0
    k_x2 = k_x1 + k_w1 + 11.0
    k_x3 = k_x2 + k_w2 + 11.0

    # 현상계 (dashed)
    page.draw_rect(fitz.Rect(k_x1, k_y, k_x1 + k_w1, k_y + k_bh), color=DARK, fill=BG_TINT, width=0.6, dashes="[2 2]")
    fk.put(page, k_x1 + 5.0, k_y + 11.0, "현상계 (타율)", key="G_B", fontsize=6.7, color=DARK)
    fk.put(page, k_x1 + 5.0, k_y + 21.0, "감각 욕구 규정", key="B_R", fontsize=6.4, color=MID_GRAY)

    # Dashed divider "구분"
    fk.put(page, k_x1 + k_w1 + 2.5, k_y + 15.0, "vs", key="G_B", fontsize=6.5, color=MID_GRAY)

    # 예지계 (solid)
    page.draw_rect(fitz.Rect(k_x2, k_y, k_x2 + k_w2, k_y + k_bh), color=BLACK, fill=WHITE, width=0.8)
    fk.put(page, k_x2 + 5.0, k_y + 11.0, "예지계 (자기입법)", key="G_B", fontsize=6.7, color=BLACK)
    fk.put(page, k_x2 + 5.0, k_y + 21.0, "보편적 준칙 검토", key="B_R", fontsize=6.4, color=DARK)

    # Arrow -> 도덕 법칙
    ax0 = k_x2 + k_w2
    ax1 = k_x3
    ay = k_y + k_bh / 2.0
    page.draw_line(fitz.Point(ax0, ay), fitz.Point(ax1 - 3.0, ay), color=BLACK, width=0.85)
    page.draw_polyline([fitz.Point(ax1 - 4.0, ay - 2.5), fitz.Point(ax1, ay), fitz.Point(ax1 - 4.0, ay + 2.5)], color=BLACK, fill=BLACK)

    page.draw_rect(fitz.Rect(k_x3, k_y, k_x3 + k_w3, k_y + k_bh), color=BLACK, fill=BLACK)
    fk.put(page, k_x3 + 6.0, k_y + 11.0, "도덕 법칙", key="G_B", fontsize=6.8, color=WHITE)
    fk.put(page, k_x3 + 6.0, k_y + 21.0, "자유의 의식", key="B_R", fontsize=6.4, color=WHITE)

    # Horizontal dashed separator
    mid_y = y0 + 55.0
    page.draw_line(fitz.Point(x0 + 7.0, mid_y), fitz.Point(x1 - 7.0, mid_y), color=RULE_GRAY, width=0.5, dashes="[3 2]")

    # Bottom lane: Hegel
    fk.put(page, x0 + 7.0, mid_y + 13.0, "[헤겔] 관계망 속 구체적 자유의 전개", key="G_B", fontsize=7.2, color=BLACK)
    h_y = mid_y + 20.0
    h_bh = 25.0
    bw = 72.0
    gap = (w - 14.0 - 3 * bw) / 2.0
    boxes = [
        ("가족", "사랑 · 제도 약", WHITE, BLACK, False),
        ("시민 사회", "권리 · 이해 충돌", WHITE, BLACK, False),
        ("국가 (완성)", "법·제도 · 구체적 자유", BLACK, WHITE, True),
    ]
    for i, (t, sub, bg, fg, is_blk) in enumerate(boxes):
        bx = x0 + 7.0 + i * (bw + gap)
        page.draw_rect(fitz.Rect(bx, h_y, bx + bw, h_y + h_bh), color=BLACK, fill=bg, width=0.75)
        fk.put(page, bx + 5.0, h_y + 10.5, t, key="G_B", fontsize=6.6, color=fg)
        fk.put(page, bx + 5.0, h_y + 20.5, sub, key="B_R", fontsize=5.8, color=fg if is_blk else DARK)
        if i < 2:
            arr_x0 = bx + bw
            arr_x1 = bx + bw + gap
            arr_y = h_y + h_bh / 2.0
            page.draw_line(fitz.Point(arr_x0, arr_y), fitz.Point(arr_x1 - 3.0, arr_y), color=BLACK, width=0.85)
            page.draw_polyline([fitz.Point(arr_x1 - 4.0, arr_y - 2.3), fitz.Point(arr_x1, arr_y), fitz.Point(arr_x1 - 4.0, arr_y + 2.3)], color=BLACK, fill=BLACK)

    fk.put(page, x0 + 7.0, y0 + h - 6.0, "※ 추상적 자유(법·제도 부정) → 공동체 질서 파괴 우려", key="B_R", fontsize=6.6, color=MID_GRAY)
    return y0 + h


def _draw_soc_remedy_diagram(page: fitz.Page, fk: Any, x0: float, y0: float, x1: float) -> float:
    """Pure B&W SOC-INSTITUTION flowchart: 국민 → 헌법재판소 → 구제 / 법원 제청."""
    h = 116.0
    page.draw_rect(fitz.Rect(x0, y0, x1, y0 + h), color=BLACK, fill=WHITE, width=0.6)
    fk.put(page, x0 + 7.0, y0 + 13.0, "[헌법재판을 통한 권리 구제 절차]", key="G_B", fontsize=7.2, color=BLACK)

    # Top flow boxes: [국민] -> [헌법재판소] -> [공권력 취소/위헌]
    ry1 = y0 + 23.0
    bh1 = 30.0
    b1_w, b2_w, b3_w = 56.0, 74.0, 62.0
    b1_x = x0 + 8.0
    b2_x = b1_x + b1_w + 21.0
    b3_x = b2_x + b2_w + 21.0

    # Box 1: 국민
    page.draw_rect(fitz.Rect(b1_x, ry1, b1_x + b1_w, ry1 + bh1), color=BLACK, fill=BG_TINT, width=0.7)
    fk.put(page, b1_x + (b1_w - fk.width("국민", "G_B", 7.1)) / 2.0, ry1 + 12.5, "국민", key="G_B", fontsize=7.1, color=BLACK)
    fk.put(page, b1_x + (b1_w - fk.width("기본권 침해", "B_R", 6.3)) / 2.0, ry1 + 23.0, "기본권 침해", key="B_R", fontsize=6.3, color=DARK)

    # Arrow 1 -> 2
    ay1 = ry1 + bh1 / 2.0
    page.draw_line(fitz.Point(b1_x + b1_w, ay1), fitz.Point(b2_x - 3.0, ay1), color=BLACK, width=0.9)
    page.draw_polyline([fitz.Point(b2_x - 4.5, ay1 - 2.5), fitz.Point(b2_x, ay1), fitz.Point(b2_x - 4.5, ay1 + 2.5)], color=BLACK, fill=BLACK)
    fk.put(page, b1_x + b1_w + 2.0, ay1 - 5.5, "헌법", key="G_B", fontsize=5.8, color=DARK)
    fk.put(page, b1_x + b1_w + 2.0, ay1 + 8.0, "소원", key="G_B", fontsize=5.8, color=DARK)

    # Box 2: 헌법재판소 (inverted highlight)
    page.draw_rect(fitz.Rect(b2_x, ry1, b2_x + b2_w, ry1 + bh1), color=BLACK, fill=BLACK)
    fk.put(page, b2_x + (b2_w - fk.width("헌법재판소", "G_B", 7.1)) / 2.0, ry1 + 12.5, "헌법재판소", key="G_B", fontsize=7.1, color=WHITE)
    fk.put(page, b2_x + (b2_w - fk.width("심판 · 위헌 결정", "B_R", 6.1)) / 2.0, ry1 + 23.0, "심판 · 위헌 결정", key="B_R", fontsize=6.1, color=WHITE)

    # Arrow 2 -> 3
    page.draw_line(fitz.Point(b2_x + b2_w, ay1), fitz.Point(b3_x - 3.0, ay1), color=BLACK, width=0.9)
    page.draw_polyline([fitz.Point(b3_x - 4.5, ay1 - 2.5), fitz.Point(b3_x, ay1), fitz.Point(b3_x - 4.5, ay1 + 2.5)], color=BLACK, fill=BLACK)
    fk.put(page, b2_x + b2_w + 2.0, ay1 - 5.5, "인용", key="G_B", fontsize=5.8, color=DARK)
    fk.put(page, b2_x + b2_w + 2.0, ay1 + 8.0, "결정", key="G_B", fontsize=5.8, color=DARK)

    # Box 3: 구제 효과
    page.draw_rect(fitz.Rect(b3_x, ry1, b3_x + b3_w, ry1 + bh1), color=BLACK, fill=WHITE, width=0.8)
    fk.put(page, b3_x + (b3_w - fk.width("공권력 취소", "G_B", 7.0)) / 2.0, ry1 + 12.5, "공권력 취소", key="G_B", fontsize=7.0, color=BLACK)
    fk.put(page, b3_x + (b3_w - fk.width("기본권 구제", "B_R", 6.3)) / 2.0, ry1 + 23.0, "기본권 구제", key="B_R", fontsize=6.3, color=DARK)

    # Bottom branch: [일반 법원] --(위헌법률심판 제청)--> [헌법재판소]
    ry2 = y0 + 70.0
    bh2 = 26.0
    f_w = 88.0
    f_x = b1_x + 12.0
    page.draw_rect(fitz.Rect(f_x, ry2, f_x + f_w, ry2 + bh2), color=DARK, fill=WHITE, width=0.7, dashes="[3 2]")
    fk.put(page, f_x + 10.0, ry2 + 11.0, "일반 법원 (재판)", key="G_B", fontsize=6.8, color=BLACK)
    fk.put(page, f_x + 10.0, ry2 + 21.0, "법률 위헌 여부 의문", key="B_R", fontsize=6.1, color=DARK)

    # Orthogonal dashed arrow from 법원 right to bottom of 헌법재판소
    lx = f_x + f_w
    ly = ry2 + bh2 / 2.0
    tx = b2_x + b2_w / 2.0
    ty_bot = ry1 + bh1
    page.draw_line(fitz.Point(lx, ly), fitz.Point(tx, ly), color=DARK, width=0.8, dashes="[3 2]")
    page.draw_line(fitz.Point(tx, ly), fitz.Point(tx, ty_bot + 3.0), color=DARK, width=0.8, dashes="[3 2]")
    page.draw_polyline([fitz.Point(tx - 2.5, ty_bot + 4.5), fitz.Point(tx, ty_bot), fitz.Point(tx + 2.5, ty_bot + 4.5)], color=BLACK, fill=BLACK)
    fk.put(page, lx + 8.0, ly + 11.0, "위헌법률심판 제청", key="G_B", fontsize=6.4, color=DARK)

    return y0 + h


def _draw_sci_ion_graph(page: fitz.Page, fk: Any, x0: float, y0: float, x1: float) -> float:
    """Pure B&W dual curve graph: A atoms added vs ion counts (total cations & A^2+)."""
    h = 126.0
    page.draw_rect(fitz.Rect(x0, y0, x1, y0 + h), color=BLACK, fill=WHITE, width=0.6)

    ox = x0 + 34.0
    oy = y0 + h - 27.0
    ax_x1 = x1 - 14.0
    ax_y0 = y0 + 18.0
    page.draw_line(fitz.Point(ox, oy), fitz.Point(ax_x1, oy), color=BLACK, width=0.9)
    page.draw_line(fitz.Point(ox, oy), fitz.Point(ox, ax_y0), color=BLACK, width=0.9)

    fk.put(page, ox - 27.0, ax_y0 + 3.0, "이온 수", key="G_B", fontsize=6.8, color=BLACK)
    lbl_x = "넣어 준 금속 A 원자 수"
    fk.put(page, x1 - 10.0 - fk.width(lbl_x, "G_B", 6.5), y0 + h - 6.0, lbl_x, key="G_B", fontsize=6.5, color=BLACK)

    # Y ticks: 0, 3N, 6N
    pw = ax_x1 - ox - 16.0
    ph = oy - ax_y0 - 12.0
    def pt(x_val: float, y_val: float) -> tuple[float, float]:
        # x_val in [0, 4.5], y_val in [0, 6]
        return ox + (x_val / 4.5) * pw, oy - (y_val / 6.0) * ph

    for yv, lbl in [(0.0, "0"), (3.0, "3N"), (6.0, "6N")]:
        _, py = pt(0.0, yv)
        if yv > 0:
            page.draw_line(fitz.Point(ox - 3.0, py), fitz.Point(ox, py), color=BLACK, width=0.7)
            page.draw_line(fitz.Point(ox, py), fitz.Point(ax_x1 - 10.0, py), color=RULE_GRAY, width=0.4, dashes="[2 2]")
        fk.put(page, ox - 18.0, py + 2.5, lbl, key="B_R", fontsize=6.7, color=DARK)

    for xv, lbl in [(1.5, "1.5N"), (3.0, "3N"), (4.5, "4.5N")]:
        px, _ = pt(xv, 0.0)
        page.draw_line(fitz.Point(px, oy), fitz.Point(px, oy + 3.0), color=BLACK, width=0.7)
        if xv == 3.0:
            page.draw_line(fitz.Point(px, oy), fitz.Point(px, pt(3.0, 3.0)[1]), color=RULE_GRAY, width=0.45, dashes="[2 2]")
        fk.put(page, px - fk.width(lbl, "B_R", 6.6) / 2.0, oy + 9.5, lbl, key="B_R", fontsize=6.6, color=DARK)

    # Solid line: Total cations (0,6N)->(1.5N,4.5N)->(3N,3N)->(4.5N,3N)
    p_tot = [pt(0.0, 6.0), pt(1.5, 4.5), pt(3.0, 3.0), pt(4.5, 3.0)]
    for i in range(len(p_tot) - 1):
        page.draw_line(fitz.Point(*p_tot[i]), fitz.Point(*p_tot[i + 1]), color=BLACK, width=1.2)
    for px, py in p_tot:
        page.draw_circle(fitz.Point(px, py), 2.3, color=BLACK, fill=BLACK)

    # Dashed line: A^2+ produced (0,0)->(1.5N,1.5N)->(3N,3N)->(4.5N,3N)
    p_a2 = [pt(0.0, 0.0), pt(1.5, 1.5), pt(3.0, 3.0), pt(4.5, 3.0)]
    for i in range(len(p_a2) - 1):
        page.draw_line(fitz.Point(*p_a2[i]), fitz.Point(*p_a2[i + 1]), color=DARK, width=1.0, dashes="[3 2]")
    for idx, (px, py) in enumerate(p_a2):
        dy = 3.5 if idx >= 2 else 0.0
        page.draw_rect(fitz.Rect(px - 2.1, py + dy - 2.1, px + 2.1, py + dy + 2.1), color=BLACK, fill=WHITE, width=0.8)

    fk.put(page, x1 - 88.0, y0 + 13.0, "● 실선: 전체 양이온 수", key="G_B", fontsize=6.6, color=BLACK)
    fk.put(page, x1 - 88.0, y0 + 23.0, "□ 점선: 생성된 A²⁺ 수", key="G_B", fontsize=6.6, color=DARK)
    return y0 + h


def _draw_sci_beaker_diagram(page: fitz.Page, fk: Any, x0: float, y0: float, x1: float) -> float:
    """Pure B&W dual beaker particle model for SCI Item 06."""
    h = 94.0
    page.draw_rect(fitz.Rect(x0, y0, x1, y0 + h), color=BLACK, fill=WHITE, width=0.6)
    fk.put(page, x0 + 7.0, y0 + 11.5, "○: B⁺   ▲: A²⁺   □: NO₃⁻   ●: 석출 금속 B", key="G_B", fontsize=6.6, color=DARK)

    # Two beakers
    bw, bh = 68.0, 50.0
    bx1 = x0 + 18.0
    bx2 = x1 - 18.0 - bw
    by0 = y0 + 21.0
    liq_y = by0 + 10.0

    for bx, cap in [(bx1, "(가) 반응 전"), (bx2, "(나) 반응 후")]:
        page.draw_rect(fitz.Rect(bx, liq_y, bx + bw, by0 + bh), color=None, fill=BG_TINT)
        page.draw_line(fitz.Point(bx, liq_y), fitz.Point(bx + bw, liq_y), color=RULE_GRAY, width=0.6, dashes="[2 2]")
        page.draw_line(fitz.Point(bx, by0), fitz.Point(bx, by0 + bh), color=BLACK, width=0.9)
        page.draw_line(fitz.Point(bx, by0 + bh), fitz.Point(bx + bw, by0 + bh), color=BLACK, width=0.9)
        page.draw_line(fitz.Point(bx + bw, by0), fitz.Point(bx + bw, by0 + bh), color=BLACK, width=0.9)
        fk.put(page, bx + (bw - fk.width(cap, "G_B", 6.8)) / 2.0, by0 + bh + 12.0, cap, key="G_B", fontsize=6.8, color=BLACK)

    # Particles inside (가): 4 B⁺ (○), 4 NO₃⁻ (□)
    for px, py in [(bx1 + 14, liq_y + 11), (bx1 + 38, liq_y + 10), (bx1 + 22, liq_y + 27), (bx1 + 50, liq_y + 24)]:
        page.draw_circle(fitz.Point(px, py), 3.0, color=BLACK, fill=WHITE, width=0.85)
    for px, py in [(bx1 + 26, liq_y + 12), (bx1 + 52, liq_y + 12), (bx1 + 12, liq_y + 28), (bx1 + 37, liq_y + 28)]:
        page.draw_rect(fitz.Rect(px - 2.7, py - 2.7, px + 2.7, py + 2.7), color=BLACK, fill=WHITE, width=0.8)

    # Arrow between beakers
    arr_x0 = bx1 + bw + 8.0
    arr_x1 = bx2 - 8.0
    arr_y = by0 + bh / 2.0 + 2.0
    page.draw_line(fitz.Point(arr_x0, arr_y), fitz.Point(arr_x1 - 3.0, arr_y), color=BLACK, width=0.95)
    page.draw_polyline([fitz.Point(arr_x1 - 4.5, arr_y - 2.5), fitz.Point(arr_x1, arr_y), fitz.Point(arr_x1 - 4.5, arr_y + 2.5)], color=BLACK, fill=BLACK)
    fk.put(page, arr_x0 + 4.0, arr_y - 7.0, "금속 A", key="G_B", fontsize=6.4, color=BLACK)
    fk.put(page, arr_x0 + 6.0, arr_y + 10.0, "투입", key="G_B", fontsize=6.4, color=BLACK)

    # Particles inside (나): 2 A²⁺ (▲), 4 NO₃⁻ (□), 4 B precipitate (● sitting clearly near bottom)
    for px, py in [(bx2 + 18, liq_y + 11), (bx2 + 46, liq_y + 13)]:
        page.draw_polyline(
            [fitz.Point(px, py - 3.3), fitz.Point(px - 3.2, py + 2.8), fitz.Point(px + 3.2, py + 2.8)],
            color=BLACK,
            fill=BLACK,
        )
    for px, py in [(bx2 + 32, liq_y + 10), (bx2 + 13, liq_y + 23), (bx2 + 36, liq_y + 23), (bx2 + 54, liq_y + 22)]:
        page.draw_rect(fitz.Rect(px - 2.7, py - 2.7, px + 2.7, py + 2.7), color=BLACK, fill=WHITE, width=0.8)
    for px in [bx2 + 16, bx2 + 27, bx2 + 39, bx2 + 50]:
        page.draw_circle(fitz.Point(px, by0 + bh - 4.5), 2.5, color=BLACK, fill=BLACK)

    return y0 + h


def _draw_eng_hours_graph(page: fitz.Page, fk: Any, x0: float, y0: float, x1: float) -> float:
    """Pure B&W dual-line graph: Weekly Study Hours (Printed Mock Sets vs Video Only, 2021-2025)."""
    h = 122.0
    page.draw_rect(fitz.Rect(x0, y0, x1, y0 + h), color=BLACK, fill=WHITE, width=0.6)
    fk.put(page, x0 + 8.0, y0 + 12.0, "Weekly Study Hours", key="G_B", fontsize=6.8, color=BLACK)

    # Legend in upper-right clean box zone
    fk.put(page, x1 - 102.0, y0 + 12.0, "● Solid: Printed Sets", key="G_B", fontsize=6.5, color=BLACK)
    fk.put(page, x1 - 102.0, y0 + 22.0, "□ Dashed: Video Only", key="G_B", fontsize=6.5, color=DARK)

    ox = x0 + 30.0
    oy = y0 + h - 22.0
    ax_x1 = x1 - 14.0
    ax_y0 = y0 + 30.0
    page.draw_line(fitz.Point(ox, oy), fitz.Point(ax_x1, oy), color=BLACK, width=0.9)
    page.draw_line(fitz.Point(ox, oy), fitz.Point(ox, ax_y0), color=BLACK, width=0.9)

    pw = ax_x1 - ox - 18.0
    ph = oy - ax_y0 - 6.0

    def pt(yr_idx: int, hrs: float) -> tuple[float, float]:
        return ox + 10.0 + (yr_idx / 4.0) * pw, oy - (hrs / 12.0) * ph

    for yv, ylbl in [(0, "0h"), (4, "4h"), (8, "8h"), (12, "12h")]:
        _, py = pt(0, yv)
        if yv > 0:
            page.draw_line(fitz.Point(ox - 2.5, py), fitz.Point(ox, py), color=BLACK, width=0.6)
            page.draw_line(fitz.Point(ox, py), fitz.Point(ax_x1 - 8.0, py), color=RULE_GRAY, width=0.4, dashes="[2 2]")
        fk.put(page, ox - 4.0 - fk.width(ylbl, "B_R", 6.6), py + 2.5, ylbl, key="B_R", fontsize=6.6, color=DARK)

    years = ["2021", "2022", "2023", "2024", "2025"]
    for idx, yr in enumerate(years):
        px, _ = pt(idx, 0)
        page.draw_line(fitz.Point(px, oy), fitz.Point(px, oy + 2.5), color=BLACK, width=0.6)
        fk.put(page, px - fk.width(yr, "B_R", 6.6) / 2.0, oy + 10.5, yr, key="B_R", fontsize=6.6, color=DARK)

    p_print = [pt(i, v) for i, v in enumerate([5.0, 6.0, 8.0, 9.0, 11.0])]
    p_video = [pt(i, v) for i, v in enumerate([9.0, 8.0, 7.0, 6.0, 5.0])]

    for i in range(4):
        page.draw_line(fitz.Point(*p_print[i]), fitz.Point(*p_print[i + 1]), color=BLACK, width=1.2)
    for px, py in p_print:
        page.draw_circle(fitz.Point(px, py), 2.3, color=BLACK, fill=BLACK)

    for i in range(4):
        page.draw_line(fitz.Point(*p_video[i]), fitz.Point(*p_video[i + 1]), color=DARK, width=1.0, dashes="[3 2]")
    for px, py in p_video:
        page.draw_rect(fitz.Rect(px - 2.1, py - 2.1, px + 2.1, py + 2.1), color=BLACK, fill=WHITE, width=0.8)

    return y0 + h


def _load_palwon_lines() -> list[str]:
    txt_path = Path(__file__).resolve().parents[2] / "quality" / "source" / "text" / "KOR_SUPP_2026_LIT_PALWON_V1.0.txt"
    return [ln.strip() for ln in txt_path.read_text(encoding="utf-8").splitlines() if ln.strip()]


SUBJECT_SAMPLES: dict[str, dict[str, Any]] = {
    "KOR": {
        "code": "KOR",
        "pdf_name": "ARC_N_SAMPLE_KOR_V1.0.pdf",
        "png_prefix": "kor_sample",
        "cover": {
            "brand_right": "KOREAN LANGUAGE · KOR V1.0",
            "edition": "SUBJECT SAMPLE · V1.0",
            "pill1": "2022 개정 교육과정 · 공통국어2",
            "pill2": "Pure B&W 국어 N° 표준 조판",
            "title1": "ARC N° 국어 조판 샘플",
            "title2": "고교 내신 · 수능형",
            "badge": "V1.0",
            "subtitle": "현대시 원문 연계 · <보기> 외재적 감상 · 중세국어(옛한글·방점) · 비문학 도식 · 서답형",
            "band": "문학·비문학 지문 (1~2단 확장)   |   중세국어·문법 Booktabs 표   |   빠른 정답·채점 기준",
            "notes": [
                "• 운문·산문·중세국어는 1.5pt 상단 실선 프레임과 함초롬돋움 단일 고딕으로 옛한글·방점을 일관 조판합니다.",
                "• <보 기>·<조 건> 박스는 상단 탭·풀바 검은 헤더 프레임으로 시각 초점을 고정하며 불필요한 색채를 배제합니다.",
                "• 중세국어(방점·옛자모) 비교표와 비문학 개념 도식(칸트 vs 헤겔)은 순수 흑백 Booktabs·벡터로 조판합니다.",
            ],
            "rows": [
                ("01", "현대시 원문 프레임(백석 「팔원」) + 화자 태도·표현", "01", "3쪽 좌단"),
                ("02~03", "<보 기> 외재적 감상 + 3열 그리드 단독 합답형", "02 ~ 03", "3쪽 우단"),
                ("04", "중세국어(옛한글·방점·옛자모) Booktabs 비교표", "04", "4쪽 좌상"),
                ("05", "비문학(칸트·헤겔 자유론) 흑백 개념 계층 도식", "05", "4쪽 좌하"),
                ("06·서답", "사례 판별 <보 기> + 조건형 서술 및 5문항 정답표", "06 · 서답1", "4·6쪽"),
            ],
            "specs": [
                ("교과 / 과목", "고교 공통국어2 (KOR)"),
                ("서체 규격", "함초롬돋움 R/B · KoPub 돋움B"),
                ("컬러 · 인쇄", "100% Pure B&W (무채색)"),
            ],
            "footer": "ARC N° · 공통국어2 고정 마스터 조판 샘플 V1.0",
        },
        "body1": {
            "header_left": "ARC N° | 공통국어2 마스터 샘플 (현대시 · 보기형)",
            "header_right": "01~03",
            "footer_left": "ARC N° · 공통국어2 Pure B&W 규격",
            "passage": {
                "title": "[01~02] 다음 시를 읽고 물음에 답하시오.",
                "mode": "lines",
                "lines": _load_palwon_lines(),
                "source": "― 백석, 「팔원(八院) - 서행시초 3」 ―",
            },
            "q1": {
                "pill": "현대시 · 표현",
                "label": "화자의 시선과 시적 상황",
                "no": "01",
                "stem": "윗글의 표현상 특징과 시적 상황에 대한 이해로 가장 적절한 것은?",
                "choices": [
                    "계절적 배경을 나타내는 시어와 감각적 이미지를 통해 대상이 처한 고달픈 현실을 부각하고 있다.",
                    "화자는 승합자동차 안에서 벌어진 갈등을 직접 중재하며 현실 극복의 낙관적 전망을 노래한다.",
                    "계집아이와 어른들이 나누는 격렬한 대화를 인용하여 사건의 전개 속도를 급격히 높이고 있다.",
                    "역설적 진술을 반복해 어린 화자가 성인의 고뇌를 스스로 조롱하는 냉소적 태도를 드러낸다.",
                    "수미상관 구조를 취해 고향 상실에 대한 화자의 죄책감이 점차 해소되는 과정을 보여 준다.",
                ],
                "mode": "stack",
            },
            "q2": {
                "pill": "<보 기> 감상",
                "label": "외재적 준거 적용",
                "no": "02",
                "stem": "윗글을 바탕으로 <보기>를 참고하여 감상한 내용으로 적절하지 않은 것은?",
                "box_label": "<보 기>",
                "box_paras": [
                    "「팔원」은 일제 강점기 북방의 삭막한 현실 속에서 고단하게 살아가는 민중의 모습을 담담한 시선으로 포착한 작품이다. 시인은 어린아이가 가혹한 노동에 내몰린 현실과 이를 바라보는 타인의 연민을 과장 없이 제시해 삶의 비애를 형상화한다.",
                ],
                "choices": [
                    "'차디찬 아침'과 '텅 하니 비어' 있는 차 안은 북방의 삭막한 배경을 감각적으로 환기하는군.",
                    "'밭고랑처럼 몹시도 터'진 손잔등은 어린 나이에 겪었을 고된 노동을 시각적으로 압축하는군.",
                    "차 안 한구석에서 '눈을 씻'는 인물은 아이의 슬픔에 조용히 공감하는 연민의 시선을 보여 주는군.",
                    "'주재소장 집에서 / 밥을 짓고 걸레를 치'던 과거는 식민지 하층민 아동의 삶의 조건을 짐작게 하는군.",
                    "'진진초록 새 저고리'는 아이가 장차 도회지 상급 학교로 진학할 경제적 풍요를 상징하는군.",
                ],
                "mode": "stack",
            },
            "q3": {
                "pill": "단독 합답형",
                "label": "시적 공간 · 3열 선지",
                "no": "03",
                "stem": "윗글의 시상 전개 및 공간 구성에 대해 옳은 것만을 <보기>에서 있는 대로 고른 것은?",
                "box_label": "<보 기>",
                "box_paras": [
                    "ㄱ. '승합자동차 안'과 '유리창 밖'을 경계로 아이의 고립감과 쓸쓸함이 대비된다.",
                    "ㄴ. 마지막 연의 '것이다'라는 추측 표현은 아이가 겪었을 고초를 헤아리는 시선을 드러낸다.",
                    "ㄷ. 묘향산으로 떠나는 여정은 식민지 현실을 거부하는 적극적 무장 투쟁의 선언을 뜻한다.",
                ],
                "choices": ["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
                "mode": "grid3",
            },
        },
        "body2": {
            "header_left": "ARC N° | 공통국어2 마스터 샘플 (문법 · 비문학 · 서답형)",
            "header_right": "04~06 · 서답형 1",
            "footer_left": "ARC N° · 공통국어2 Pure B&W 규격",
            "q4": {
                "pill": "문법 · 중세국어",
                "label": "중세국어 옛한글·방점 Booktabs 표",
                "no": "04",
                "stem": "표는 15세기 중세국어 자료(《훈민정음》 언해)의 표기와 음운·방점 특징을 정리한 것이다. 이에 대한 설명으로 적절하지 않은 것은?",
                "headers": ["표기 용례", "음운 · 옛자모", "표기 · 성조", "해석 원리"],
                "widths": [0.25, 0.25, 0.24, 0.26],
                "rows": [
                    ["나랏말\u110a\u119e미", "각자병서 ㅆ·ㆍ", "이어적기(연철)", "체언+조사 결합"],
                    ["\u1120\u1173들·\u1121\u1173메", "합용병서 ㅳ·ㅄ", "초성 자음군", "어두 자음 실현"],
                    ["마\u1140\u119e\u11af·\u1112\u119e\u11af\u11f9", "반치음 ㅿ·여린 ㆆ", "현대 소실 음운", "관형형·마찰음"],
                    ["랏\u302e / 말\u302f / 미", "방점 1·2·무점", "거성·상성·평성", "소리 높낮이 변별"],
                ],
                "choices": [
                    "'나랏말\u110a\u119e미'는 체언과 주격 조사가 이어적기되어 형태소 원형을 밝혀 적지 않았다.",
                    "'\u1120\u1173들'의 'ㅳ'은 어두 자음군 표기이고, '마\u1140\u119e\u11af'의 'ㅿ'은 현대 국어에서 소실된 음운이다.",
                    "' 랏\u302e'의 방점 1개는 높은 소리(거성), ' 말\u302f'의 방점 2개는 낮았다 높아지는 소리(상성)를 뜻한다.",
                    "'말\u110a\u119e미'와 '마\u1140\u119e\u11af'의 'ㆍ'는 모두 현대 국어의 장모음 'ㅓ'를 표기하기 위한 부호였다.",
                    "방점 없는 '미'는 낮은 소리인 평성이며, 성조 변별을 위한 방점 표기는 16세기 이후 사라졌다.",
                ],
            },
            "q5": {
                "pill": "비문학 · 도식",
                "label": "칸트 · 헤겔 자유론 도식",
                "no": "05",
                "stem": "그림은 칸트와 헤겔의 자유론을 구조화한 것이다. 위 도식에 대한 이해로 가장 적절한 것은?",
                "draw_diagram": _draw_kor_freedom_diagram,
                "choices": [
                    "칸트는 감각 욕구에 따라 행위할 때 예지계의 자기 입법이 실현된다고 본다.",
                    "칸트의 도덕 법칙은 주관적 준칙이 모순 없이 보편성을 확보할 때 성립한다.",
                    "헤겔은 시민 사회 단계에서 이해 충돌 없이 자유가 완전히 고정된다고 본다.",
                    "헤겔은 국가의 법과 제도를 자유를 억압하는 추상적 자유의 원천으로 비판한다.",
                    "두 철학자 모두 공동체의 법적 구속을 부정할수록 진정한 자유가 커진다고 본다.",
                ],
            },
            "q6": {
                "pill": "사례 판별",
                "label": "비문학 <보 기> 적용",
                "no": "06",
                "stem": "<보기>의 (가), (나)를 칸트와 헤겔의 관점에서 평가한 내용으로 가장 적절한 것은?",
                "box_label": "<보 기>",
                "box_paras": [
                    "(가) 갑은 배고픔의 욕구를 이기고, 타인의 생존 위기를 외면해서는 안 된다는 보편적 법칙에 따라 음식을 양보했다.",
                    "(나) 을은 국가의 모든 법과 제도를 개인의 선택을 가로막는 외적 구속으로 간주해 전면 거부하였다.",
                ],
                "choices": [
                    "칸트는 (가)를 쾌락 추구가 원인이 된 현상계의 타율적 행위로 규정할 것이다.",
                    "헤겔은 (가)를 공동체의 법적 보호를 해치는 파괴적 행위로 비판할 것이다.",
                    "칸트는 (가)에서 이성이 규정한 자유를 확인하고, 헤겔은 (나)를 추상적 자유로 비판할 것이다.",
                    "헤겔은 (나)를 국가 단계의 구체적 자유를 가장 모범적으로 구현한 사례로 평가할 것이다.",
                    "칸트와 헤겔 모두 (나)의 태도가 공동체 질서와 타인의 자유를 지켜 준다고 볼 것이다.",
                ],
            },
            "cr": {
                "pill": "서답형 문항",
                "label": "<조 건> 및 답안 프레임",
                "no": "[서답형 1]",
                "stem": "헤겔의 관점에서 '국가의 법과 제도'가 지니는 의의를 '추상적 자유'와 대비하여 서술하시오.",
                "box_label": "<조 건>",
                "box_paras": [
                    "1. 국가 단계에서 법과 제도가 수행하는 기능을 구체적으로 명시할 것.",
                    "2. 추상적 자유의 파괴적 한계와 대비하여 한 문장으로 작성할 것.",
                ],
            },
        },
        "answer": {
            "header_left": "ARC N° | 공통국어2 빠른 정답 · 모범답안",
            "header_right": "01~06 · 서답형 1",
            "footer_left": "ARC N° · 공통국어2 Pure B&W 규격",
            "answers": [(1, 1), (2, 5), (3, 3), (4, 4), (5, 2), (6, 3)],
            "cr_title": "[서답형 1] 모범답안 및 채점 기준",
            "cr_model": "예시 답안: 법과 제도를 외적 구속으로만 부정해 공동체 질서를 해치는 추상적 자유와 달리, 국가의 법과 제도는 법적 보호와 이해관계 조정을 통해 개인의 자유와 공동체 질서가 조화되는 구체적 자유를 실현한다.",
            "cr_rubric": [
                "• 채점 기준 ①: 국가의 법과 제도가 수행하는 법적 보호 및 이해관계 조정 기능 제시 (50%)",
                "• 채점 기준 ②: 법·제도를 부정하는 추상적 자유의 파괴적 한계와 대비해 완결된 문장으로 서술 (50%)",
            ],
        },
    },
    "SOC": {
        "code": "SOC",
        "pdf_name": "ARC_N_SAMPLE_SOC_V1.0.pdf",
        "png_prefix": "soc_sample",
        "cover": {
            "brand_right": "SOCIAL STUDIES · SOC V1.0",
            "edition": "SUBJECT SAMPLE · V1.0",
            "pill1": "2022 개정 교육과정 · 통합사회2",
            "pill2": "Pure B&W 사회 N° 표준 조판",
            "title1": "ARC N° 사회 조판 샘플",
            "title2": "제시문 · 통계 · 제도 도식",
            "badge": "V1.0",
            "subtitle": "사상가 대비 지문 · 사례 <보기> · Booktabs 통계표 · 권리구제 도식 · 서답형",
            "band": "정의·사상가 (가)/(나) 대비   |   통계·헌재 구제 도식   |   권리충돌 조건형 서답",
            "notes": [
                "• 복수 사상가 제시문은 (가)/(나) 대조 구조를 명료하게 가르고 <보 기> 사례 적용 문항으로 심화 변별합니다.",
                "• 통계 비교표는 표본 수·기준 연도·단위(%)를 명시해 비율과 절대수 혼동, 개인 일반화 오류를 점검합니다.",
                "• 권리구제·헌법재판 흐름도는 유채색 없이 실선·점선·방향 화살표만으로 기관 간 권한 경로를 엄밀히 구분합니다.",
            ],
            "rows": [
                ("01", "복수 사상가 프레임(아리스토텔레스 vs 롤스 정의관)", "01", "3쪽 좌단"),
                ("02~03", "분배 사례 적용 <보 기> + 실질 기준 3열 합답형", "02 ~ 03", "3쪽 우단"),
                ("04", "집단 인식 경향(표본·단위 명시) Booktabs 통계표", "04", "4쪽 좌상"),
                ("05", "헌법소원 · 위헌법률심판 제청 흑백 절차 흐름도", "05", "4쪽 좌하"),
                ("06·서답", "다국적 기업 공간적 분업 <보 기> + 기본권 충돌 서답", "06 · 서답1", "4·6쪽"),
            ],
            "specs": [
                ("교과 / 과목", "고교 통합사회2 (SOC)"),
                ("도식 규격", "SOC-DATA · SOC-INSTITUTION"),
                ("컬러 · 인쇄", "100% Pure B&W (무채색)"),
            ],
            "footer": "ARC N° · 통합사회2 고정 마스터 조판 샘플 V1.0",
        },
        "body1": {
            "header_left": "ARC N° | 통합사회2 마스터 샘플 (사상가 · 정의 기준)",
            "header_right": "01~03",
            "footer_left": "ARC N° · 통합사회2 Pure B&W 규격",
            "passage": {
                "title": "[01~02] 다음 (가), (나) 사상가의 입장을 읽고 물음에 답하시오.",
                "mode": "paras",
                "paras": [
                    "(가) 아리스토텔레스는 재화와 명예를 나누는 분배적 정의에서는 각 사람이 지닌 가치(덕·능력·공적)에 비례해 배분하는 기하학적 비례 평등이 적용되어야 한다고 보았다. 반면 거래나 피해로 인한 부당한 불균형을 바로잡는 교정적 정의에서는 당사자의 지위와 무관하게 손익을 산술적으로 균등 복구해야 한다고 주장하였다.",
                    "(나) 롤스는 공정으로서의 정의를 제시하며 원초적 입장의 무지의 베일 아래에서 정의의 원칙이 합의된다고 보았다. 제1원칙으로 평등한 기본적 자유가 우선 보장되어야 하며, 제2원칙에 따라 사회적·경제적 불평등은 공정한 기회균등이 열린 조건에서 최소 수혜자에게 최대 이익이 될 때만 정당화된다.",
                ],
                "source": "― 통합사회2 정의의 의미와 원칙 핵심 대비 ―",
            },
            "q1": {
                "pill": "정의관 대비",
                "label": "(가), (나) 사상가 입장",
                "no": "01",
                "stem": "(가), (나) 입장에 대한 설명으로 가장 적절한 것은?",
                "choices": [
                    "(가)는 재화 분배 시 개인의 공적 차이를 배제하고 언제나 산술적 균등 분배만 적용한다.",
                    "(가)는 분배적 정의에서 각자의 가치 차이를 반영한 비례적 배분을 정당하다고 본다.",
                    "(나)는 무지의 베일 속 당사자들이 자신의 계층과 재능을 정확히 안 채 합의한다고 본다.",
                    "(나)는 최소 수혜자 이익보다 사회 전체 총효용 극대화를 제1원칙으로 삼는다.",
                    "(가)와 (나) 모두 사회적·경제적 불평등은 어떤 조건에서도 일절 정당화할 수 없다고 본다.",
                ],
                "mode": "stack",
            },
            "q2": {
                "pill": "<보 기> 적용",
                "label": "분배 사례 분석",
                "no": "02",
                "stem": "<보기>의 분배 정책에 대해 (가), (나) 입장에서 내릴 평가로 적절하지 않은 것은?",
                "box_label": "<보 기>",
                "box_paras": [
                    "S시는 2026년 예산 배분에서 학업 성취와 연구 성과가 우수한 학생에게는 장학금을 차등 지급하고, 재난 피해를 입은 저소득 가구에는 기본 생계 지원금을 우선 배정하기로 결정하였다.",
                ],
                "choices": [
                    "(가)는 성과에 따른 장학금 차등 지급이 분배적 정의의 비례 원칙에 부합한다고 볼 것이다.",
                    "(나)는 저소득 피해 가구 우선 지원이 최소 수혜자의 처지를 개선한다면 정당화할 것이다.",
                    "(가)는 부당한 재산 침해로 발생한 가구의 손실 복구 문제를 교정적 정의와 연결할 것이다.",
                    "(나)는 기회균등을 배제한 채 특정 신분에게만 장학 응시 자격을 독점시키는 제도를 지지할 것이다.",
                    "(가)와 (나) 모두 정당한 분배 기준이 공동체의 공정성과 신뢰 유지에 기여한다고 볼 것이다.",
                ],
                "mode": "stack",
            },
            "q3": {
                "pill": "단독 합답형",
                "label": "실질적 기준 · 3열 선지",
                "no": "03",
                "stem": "분배의 실질적 기준(능력, 업적, 필요)에 대한 옳은 설명만을 <보기>에서 고른 것은?",
                "box_label": "<보 기>",
                "box_paras": [
                    "ㄱ. 업적 기준은 객관적 성과 측정이 비교적 용이해 성취 동기를 높이는 데 유리하다.",
                    "ㄴ. 필요 기준은 인간다운 삶을 보장하는 데 기여하지만 근로 의욕 저하 우려가 있다.",
                    "ㄷ. 능력 기준은 선천적 자질과 우연한 환경의 영향을 배제하므로 불평등을 완전히 없앤다.",
                ],
                "choices": ["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
                "mode": "grid3",
            },
        },
        "body2": {
            "header_left": "ARC N° | 통합사회2 마스터 샘플 (통계 · 권리구제 · 서답형)",
            "header_right": "04~06 · 서답형 1",
            "footer_left": "ARC N° · 통합사회2 Pure B&W 규격",
            "q4": {
                "pill": "통계 · 자료",
                "label": "SOC-DATA 비교표",
                "no": "04",
                "stem": "표는 2025년 두 집단 X, Y(각 200명)의 사물 분류 기준 응답 비율(%)을 조사한 결과이다. 가장 적절한 해석은?",
                "headers": ["집단", "속성 중심(%)", "관계 중심(%)", "응답자(명)"],
                "widths": [0.20, 0.28, 0.28, 0.24],
                "rows": [
                    ["집단 X", "72.0", "28.0", "200"],
                    ["집단 Y", "39.0", "61.0", "200"],
                ],
                "choices": [
                    "집단 수준에서는 X가 속성 중심, Y가 관계 중심 응답 비율이 높지만 개인별 예외도 존재한다.",
                    "집단 X에 속한 모든 개인은 어떤 상황에서도 예외 없이 개별 속성만으로 사물을 분류한다.",
                    "집단 Y는 집단 X보다 관계 중심 응답 비율이 낮아 전체 조사 대상 인원 수도 더 적다.",
                    "집단 Y의 분류 방식은 논리적 분석 능력이 결여된 결과라고 단정할 수 있다.",
                    "위 표만으로 두 집단의 인식 차이를 결정한 단일 유전적 요인을 확정할 수 있다.",
                ],
            },
            "q5": {
                "pill": "제도 · 흐름도",
                "label": "SOC-INSTITUTION 도식",
                "no": "05",
                "stem": "그림은 헌법재판을 통한 권리 구제 절차의 일부이다. 이에 대한 설명으로 옳은 것은?",
                "draw_diagram": _draw_soc_remedy_diagram,
                "choices": [
                    "헌법소원의 인용 결정은 청구인인 국민이 직접 내려 공권력 행사를 취소시킨다.",
                    "일반 법원은 재판 중인 사건과 관련된 법률의 위헌 여부를 스스로 최종 확정해 폐기한다.",
                    "일반 법원이 헌법소원을 청구하면 국회가 위헌법률심판 제청권을 대신 행사한다.",
                    "헌법재판소의 위헌 결정이 내려져도 침해된 공권력 행사의 효력은 그대로 유지된다.",
                    "국민은 기본권 침해 시 헌법재판소에 권리구제형 헌법소원을 청구해 구제받을 수 있다.",
                ],
            },
            "q6": {
                "pill": "세계화 · 분업",
                "label": "공간적 분업 <보 기>",
                "no": "06",
                "stem": "<보기>의 다국적 기업 K사 사례에서 추론할 수 있는 내용으로 가장 적절한 것은?",
                "box_label": "<보 기>",
                "box_paras": [
                    "다국적 기업 K사는 본국 대도시에 연구·설계 센터를 유지하고, 정밀 부품은 복수의 공업국에서 조달하며, 단순 조립 공장은 임금 수준이 낮은 개발 도상국으로 이전해 가동하고 있다.",
                ],
                "choices": [
                    "생산 요소와 입지 조건의 차이를 고려해 생산 기능이 여러 국가에 배치되는 공간적 분업이 진행되고 있다.",
                    "핵심 연구·설계 기능까지 저임금 조립 지역으로 완전 이전하여 본국 본사의 역할을 폐지하였다.",
                    "조립 공장이 들어선 개발 도상국 지역은 모두 자동적으로 최상위 세계도시 계층으로 승격된다.",
                    "기업의 공간적 분업 확대는 국가 간 교역과 경제적 상호 의존 관계를 전면 차단한다.",
                    "이 같은 생산 거점 분산만으로 세계 모든 국가 간 소득 격차가 일률적으로 소멸한다.",
                ],
            },
            "cr": {
                "pill": "서답형 문항",
                "label": "기본권 충돌 · <조 건>",
                "no": "[서답형 1]",
                "stem": "공익 목적의 언론 보도 활동과 개인의 사생활 보호가 충돌할 때 이루어지는 헌법적 조정 원리를 서술하시오.",
                "box_label": "<조 건>",
                "box_paras": [
                    "1. 충돌하는 두 기본권의 명칭을 명확히 밝혀 적을 것.",
                    "2. 비례성 원칙(이익 형량)에 따른 해결 방향을 한 문장으로 서술할 것.",
                ],
            },
        },
        "answer": {
            "header_left": "ARC N° | 통합사회2 빠른 정답 · 모범답안",
            "header_right": "01~06 · 서답형 1",
            "footer_left": "ARC N° · 통합사회2 Pure B&W 규격",
            "answers": [(1, 2), (2, 4), (3, 3), (4, 1), (5, 5), (6, 1)],
            "cr_title": "[서답형 1] 모범답안 및 채점 기준",
            "cr_model": "예시 답안: 표현의 자유(언론·출판의 자유)와 사생활의 비밀과 자유가 충돌할 때에는 보도의 공익성과 사생활 침해 정도를 비례성 원리에 따라 형량하여 두 기본권이 조화롭게 실현되도록 조정한다.",
            "cr_rubric": [
                "• 채점 기준 ①: 충돌하는 두 기본권(표현의 자유, 사생활의 비밀과 자유) 정확히 명시 (40%)",
                "• 채점 기준 ②: 공익과 침해 법익의 이익 형량 및 비례성 원칙에 따른 조화로운 제한 설명 (60%)",
            ],
        },
    },
    "SCI": {
        "code": "SCI",
        "pdf_name": "ARC_N_SAMPLE_SCI_V1.0.pdf",
        "png_prefix": "sci_sample",
        "cover": {
            "brand_right": "INTEGRATED SCIENCE · SCI V1.0",
            "edition": "SUBJECT SAMPLE · V1.0",
            "pill1": "2022 개정 교육과정 · 통합과학2",
            "pill2": "Pure B&W 과학 N° 표준 조판",
            "title1": "ARC N° 과학 조판 샘플",
            "title2": "실험 · 입자 모형 · 그래프",
            "badge": "V1.0",
            "subtitle": "산화·환원 실험 지문 · 전자기 유도 표 · 정량 그래프 · 비커 입자 모형",
            "band": "실험 전후 조건 제시문   |   정량 곡선 & 입자 모형 도식   |   전하 보존 조건 서답",
            "notes": [
                "• 이온식(A²⁺, B⁺, NO₃⁻)과 아래첨자·위첨자는 고딕 본문 + 정밀 첨자 폴백 매핑으로 깨짐 없이 출력합니다.",
                "• 반응 곡선 그래프는 실선(●)과 점선(□)의 선종·마커 이중 구분으로 흑백 인쇄 시 데이터 혼선을 원천 차단합니다.",
                "• 수용액 입자 모형 비커 도식은 반응 전·후 양이온/구경꾼 이온/석출 고체를 기호로 명확히 분리해 표기합니다.",
            ],
            "rows": [
                ("01", "금속-이온 수용액 산화·환원 실험 프레임 + 전자 이동", "01", "3쪽 좌단"),
                ("02~03", "양이온 수 변화 <보 기> + 반응성 서열 3열 합답형", "02 ~ 03", "3쪽 우단"),
                ("04", "전자기 유도 변인 통제(속력·감은 수) Booktabs 표", "04", "4쪽 좌상"),
                ("05", "금속 A 투입량에 따른 이온 수 변화 흑백 벡터 그래프", "05", "4쪽 좌하"),
                ("06·서답", "반응 전후 비커 입자 모형 + 전하량 보존 서답", "06 · 서답1", "4·6쪽"),
            ],
            "specs": [
                ("교과 / 과목", "고교 통합과학2 (SCI)"),
                ("정량 · 도식", "그래프 · 입자 모형 · 실험표"),
                ("컬러 · 인쇄", "100% Pure B&W (무채색)"),
            ],
            "footer": "ARC N° · 통합과학2 고정 마스터 조판 샘플 V1.0",
        },
        "body1": {
            "header_left": "ARC N° | 통합과학2 마스터 샘플 (산화·환원 · 반응성)",
            "header_right": "01~03",
            "footer_left": "ARC N° · 통합과학2 Pure B&W 규격",
            "passage": {
                "title": "[01~02] 다음은 금속과 금속 이온 수용액의 산화·환원 반응 실험이다.",
                "mode": "paras",
                "paras": [
                    "• 비커에 양이온 B⁺ 6N개와 구경꾼 이온 NO₃⁻ 6N개가 녹아 있는 수용액을 준비하였다.",
                    "• 이 수용액에 금속 A를 넣어 반응시켰더니 금속 A는 A²⁺ 이온으로 산화되고, 수용액 속 B⁺ 이온 6N개는 모두 전자를 얻어 금속 B로 석출되어 반응이 완결되었다.",
                    "• 반응 과정에서 물은 참여하지 않으며, 금속 A와 B의 반응 전후 전하량은 보존된다.",
                ],
                "source": "― 통합과학2 전자 이동에 의한 산화·환원 정량 탐구 ―",
            },
            "q1": {
                "pill": "산화 · 환원",
                "label": "전자 이동 원리",
                "no": "01",
                "stem": "위 실험의 산화·환원 반응에 대한 설명으로 옳은 것은?",
                "choices": [
                    "금속 A는 전자를 얻어 수용액 속에서 A²⁺ 이온으로 환원된다.",
                    "B⁺ 이온은 각각 전자 1개를 얻어 금속 B로 환원된다.",
                    "구경꾼 이온 NO₃⁻는 반응이 진행되면서 전자를 잃고 산화된다.",
                    "금속 B는 금속 A보다 전자를 잃고 양이온이 되려는 성질이 크다.",
                    "산화된 물질이 잃은 총 전자 수는 환원된 물질이 얻은 전자 수의 절반이다.",
                ],
                "mode": "stack",
            },
            "q2": {
                "pill": "<보 기> 정량",
                "label": "이온 수 변화 판별",
                "no": "02",
                "stem": "위 반응이 완결될 때까지 수용액 속 입자 수 변화에 대한 <보기>의 판단 중 옳은 것은?",
                "box_label": "<보 기>",
                "box_paras": [
                    "초기 수용액에는 B⁺ 6N개와 NO₃⁻ 6N개가 들어 있었으며, 반응 완결 시까지 A는 A²⁺ 상태로만 녹아 들어간다.",
                ],
                "choices": [
                    "반응 후 수용액 속 NO₃⁻ 이온 수는 초기의 절반인 3N개로 줄어든다.",
                    "반응이 완결되었을 때 생성된 A²⁺ 이온 수는 6N개로 초기 B⁺ 수와 같다.",
                    "B⁺ 이온 2개가 석출될 때마다 A 원자 2개가 산화되어 전체 양이온 수가 일정하다.",
                    "반응 전후 수용액 속 전체 양이온 수는 6N개에서 3N개로 감소한다.",
                    "수용액 속 양이온 수가 줄어들므로 용액 전체 전하량은 음(-)전하로 바뀐다.",
                ],
                "mode": "stack",
            },
            "q3": {
                "pill": "단독 합답형",
                "label": "반응성 서열 · 3열 선지",
                "no": "03",
                "stem": "금속 X, Y, Z의 반응 실험 결과를 토대로 내린 결론 중 옳은 것만을 <보기>에서 고른 것은?",
                "box_label": "<보 기>",
                "box_paras": [
                    "[실험] X를 Y²⁺ 용액에 넣으면 Y가 석출되고, Y를 Z²⁺ 용액에 넣으면 Z가 석출되었다. Z를 X²⁺ 용액에 넣었을 때는 변화가 없었다.",
                    "ㄱ. 금속의 반응성 크기는 X > Y > Z 순이다.",
                    "ㄴ. Z를 Y²⁺ 수용액에 넣어도 산화·환원 반응이 일어나지 않는다.",
                    "ㄷ. X를 Z²⁺ 수용액에 넣으면 X가 산화되며 Z가 석출된다.",
                ],
                "choices": ["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
                "mode": "grid3",
            },
        },
        "body2": {
            "header_left": "ARC N° | 통합과학2 마스터 샘플 (전자기 · 그래프 · 모형)",
            "header_right": "04~06 · 서답형 1",
            "footer_left": "ARC N° · 통합과학2 Pure B&W 규격",
            "q4": {
                "pill": "실험 · 데이터",
                "label": "전자기 유도 Booktabs 표",
                "no": "04",
                "stem": "표는 같은 막대자석과 코일로 세 조건 I~III에서 유도 전류를 측정한 결과이다. 옳은 설명은?",
                "headers": ["실험", "자석 운동", "속력", "감은 수", "바늘 편향"],
                "widths": [0.13, 0.28, 0.16, 0.17, 0.26],
                "rows": [
                    ["I", "N극 접근", "v", "N", "오른쪽, θ₁"],
                    ["II", "N극 접근", "2v", "N", "오른쪽, θ₂"],
                    ["III", "N극 멀어짐", "2v", "2N", "왼쪽, θ₃"],
                ],
                "choices": [
                    "I과 II는 자석의 이동 방향이 같아 전류 방향이 같고, 속력이 큰 II의 세기가 더 크다(θ₂ > θ₁).",
                    "II와 III은 자석 이동 속력이 2v로 같으므로 검류계 바늘의 편향 방향도 동일하다.",
                    "III은 코일 감은 수가 2N이므로 자석을 멀어지게 해도 II와 같은 방향으로 흐른다.",
                    "자석이 코일 내부에 정지해 있어도 감은 수가 2N이면 유도 전류가 계속 발생한다.",
                    "코일의 감은 수와 자석 속력은 코일에 유도되는 전류의 세기와 전혀 무관하다.",
                ],
            },
            "q5": {
                "pill": "정량 · 그래프",
                "label": "벡터 곡선 (선종 · 마커 구분)",
                "no": "05",
                "stem": "그림은 B⁺ 6N개가 녹아 있는 수용액에 금속 A를 넣을 때 이온 수 변화를 나타낸 것이다. 옳은 것은?",
                "draw_diagram": _draw_sci_ion_graph,
                "choices": [
                    "넣어 준 A 원자 수가 1.5N개일 때 수용액에 남아 있는 B⁺ 수는 4.5N개이다.",
                    "넣어 준 A 원자 수가 1.5N개일 때 수용액 속 A²⁺와 B⁺의 수 비는 1 : 1이다.",
                    "넣어 준 A 원자 수가 3N개인 지점에서 초기 B⁺가 모두 환원되어 반응이 완결된다.",
                    "A를 3N개보다 더 많이 넣으면 생성되는 A²⁺ 수는 3N개를 넘어 계속 증가한다.",
                    "반응이 완결된 이후 전체 양이온 수는 초기 6N개의 두 배인 12N개가 된다.",
                ],
            },
            "q6": {
                "pill": "입자 · 모형",
                "label": "수용액 비커 전후 도식",
                "no": "06",
                "stem": "그림 (가) 수용액에 금속 A를 충분히 반응시켜 (나)가 되었다. 이에 대한 해석으로 옳은 것은?",
                "draw_diagram": _draw_sci_beaker_diagram,
                "choices": [
                    "(가)에서 (나)로 될 때 구경꾼 이온(□) 수는 반응에 소모되어 절반으로 줄어든다.",
                    "반응 과정에서 ○ 4개가 전자를 얻어 금속 B로 석출되고 ▲ 2개가 새로 생성되었다.",
                    "(나) 수용액에 들어 있는 전체 양전하의 합은 전체 음전하의 합보다 크다.",
                    "금속 B가 금속 A보다 전자를 잃기 쉬워 자발적 산화·환원 반응이 일어난 것이다.",
                    "반응 후 전체 양이온 수가 절반으로 감소했으므로 전하량 보존 법칙에 위배된다.",
                ],
            },
            "cr": {
                "pill": "서답형 문항",
                "label": "전하량 보존 · <조 건>",
                "no": "[서답형 1]",
                "stem": "그림 (가)→(나) 반응에서 수용액 속 전체 양이온 수가 감소하는 까닭을 서술하시오.",
                "box_label": "<조 건>",
                "box_paras": [
                    "1. 반응에 참여하는 두 양이온(B⁺, A²⁺)의 전하량 비와 이동 전자 수를 명시할 것.",
                    "2. 구경꾼 이온(NO₃⁻) 수 유지와 전기적 중성 조건을 포함해 서술할 것.",
                ],
            },
        },
        "answer": {
            "header_left": "ARC N° | 통합과학2 빠른 정답 · 모범답안",
            "header_right": "01~06 · 서답형 1",
            "footer_left": "ARC N° · 통합과학2 Pure B&W 규격",
            "answers": [(1, 2), (2, 4), (3, 5), (4, 1), (5, 3), (6, 2)],
            "cr_title": "[서답형 1] 모범답안 및 채점 기준",
            "cr_model": "예시 답안: 반응에 참여하지 않는 구경꾼 이온(NO₃⁻) 수가 일정해 전체 음전하가 유지되는 상태에서, 전하량이 +1인 B⁺ 2개가 전자 2개를 얻어 환원될 때마다 전하량이 +2인 A²⁺ 1개만 생성되므로 전체 양이온 수는 감소한다.",
            "cr_rubric": [
                "• 채점 기준 ①: +1가 B⁺ 2개 환원 시 +2가 A²⁺ 1개 생성되는 전하량·전자 수 관계 서술 (60%)",
                "• 채점 기준 ②: 구경꾼 이온(NO₃⁻) 수 일정 유지 및 수용액 전체의 전기적 중성 유지 언급 (40%)",
            ],
        },
    },
    "ENG": {
        "code": "ENG",
        "pdf_name": "ARC_N_SAMPLE_ENG_V1.0.pdf",
        "png_prefix": "eng_sample",
        "cover": {
            "brand_right": "ENGLISH READING & WRITING · ENG V1.0",
            "edition": "SUBJECT SAMPLE · V1.0",
            "pill1": "2022 개정 교육과정 · 공통영어1",
            "pill2": "Pure B&W 영어 N° 표준 조판",
            "title1": "ARC N° 영어 조판 샘플",
            "title2": "지문 · 순서 · 도표 · 조건 영작",
            "badge": "V1.0",
            "subtitle": "어절 보존 영문 래핑 · 빈칸 추론 · (A)(B)(C) 순서 3열 · 도표/그래프 · 서답",
            "band": "장문 빈칸·어법 독해   |   Booktabs 도표 & 흑백 그래프   |   요약문 · 조건 영작",
            "notes": [
                "• 영문 지문과 선택지는 단어 중간 끊김을 방지하는 어절 보존 래핑(word-safe wrap)으로 수능·모평 가독성을 유지합니다.",
                "• 글의 순서((A)-(B)-(C))와 요약문((A)/(B)) 박스는 상단 풀바/라인 라벨과 3열 알파벳 순 배열 규격을 준수합니다.",
                "• 통계 표·시계열 선그래프·조건 영작 프레임까지 100% Pure B&W 무채색으로 조판해 인쇄 선명도를 극대화합니다.",
            ],
            "rows": [
                ("01", "영문 독해 지문 프레임 + 빈칸 추론 (Parallel Phrases)", "01", "3쪽 좌단"),
                ("02~03", "Summary <보 기> 내용 일치 + (A)(B)(C) 글의 순서 3열", "02 ~ 03", "3쪽 우단"),
                ("04", "학년별 학습 매체 비중 Booktabs 영문 비교표", "04", "4쪽 좌상"),
                ("05", "연도별 학습 시간 추이 흑백 벡터 선그래프(실선/점선)", "05", "4쪽 좌하"),
                ("06·서답", "요약문 <요 약 문> 완성 + 'not only ~ but also' 영작", "06 · 서답1", "4·6쪽"),
            ],
            "specs": [
                ("교과 / 과목", "고교 공통영어1 (ENG)"),
                ("래핑 · 배열", "어절 보존 · CSAT 3열 순서"),
                ("컬러 · 인쇄", "100% Pure B&W (무채색)"),
            ],
            "footer": "ARC N° · 공통영어1 고정 마스터 조판 샘플 V1.0",
        },
        "body1": {
            "header_left": "ARC N° | 공통영어1 마스터 샘플 (독해 · 빈칸 · 순서)",
            "header_right": "01~03",
            "footer_left": "ARC N° · 공통영어1 Pure B&W 규격",
            "passage": {
                "title": "[01~02] Read the following passage and answer the questions.",
                "mode": "paras",
                "paras": [
                    "When readers move rapidly across digital screens, they often scan headings and skip subtle logical transitions. Because scrolling feels effortless, the brain mistakes visual fluency for complete understanding, even while core claims remain untested.",
                    "By contrast, working with structured print layouts introduces productive friction. Clear typographic hierarchy, fixed column boundaries, and deliberate white space slow the eye just enough to invite active verification. In trials with high-school learners, students who annotated two-column print passages recalled causal links more accurately than peers reading identical texts on scrollable feeds. Far from slowing thought, visual discipline creates the mental pause required for __________________________.",
                ],
                "source": "* productive friction: 생산적 인지 마찰",
            },
            "q1": {
                "pill": "빈칸 추론",
                "label": "어휘 · 문맥 논리",
                "no": "01",
                "stem": "다음 글의 빈칸에 들어갈 말로 가장 적절한 것은?",
                "choices": [
                    "skipping complex evidence without careful checking",
                    "deep comprehension rather than passive skimming",
                    "relying strictly on unverified screen impressions",
                    "removing fixed boundaries between distinct sections",
                    "increasing scrolling speed at the cost of precision",
                ],
                "mode": "stack",
            },
            "q2": {
                "pill": "<보 기> 일치",
                "label": "Reading Note 대조",
                "no": "02",
                "stem": "윗글과 <보기>의 독해 요점을 바탕으로 판단할 때, 글의 내용과 일치하지 않는 것은?",
                "box_label": "<보 기>",
                "box_paras": [
                    "• Note 1: Effortless scrolling can create a false sense of mastery.",
                    "• Note 2: Fixed print layout promotes active verification via pause.",
                    "• Note 3: Two-column print annotation improved causal recall.",
                ],
                "choices": [
                    "Fluent scrolling may cause screen readers to overlook key arguments.",
                    "Fixed column structure offers helpful friction for careful verification.",
                    "Students annotating printed passages recalled causal links better.",
                    "Deliberate white space regulates reading pace instead of harming focus.",
                    "Using scrollable feeds removes any need for clear typographic hierarchy.",
                ],
                "mode": "stack",
            },
            "q3": {
                "pill": "글의 순서",
                "label": "(A)-(B)-(C) · 3열 배열",
                "no": "03",
                "stem": "주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?",
                "box_label": "<보 기>",
                "box_paras": [
                    "City planners increasingly rely on pocket parks to cool dense neighborhoods during summer heat waves.",
                    "(A) However, without steady maintenance, shaded benches degrade quickly and lose daily visitors.",
                    "(B) First, clusters of native trees lower surface heat by blocking direct sunlight over asphalt streets.",
                    "(C) These cooler walkways, in turn, invite pedestrians to stay outdoors longer and gather in shared plazas.",
                ],
                "choices": ["(A)-(C)-(B)", "(B)-(A)-(C)", "(B)-(C)-(A)", "(C)-(A)-(B)", "(C)-(B)-(A)"],
                "mode": "grid3",
            },
        },
        "body2": {
            "header_left": "ARC N° | 공통영어1 마스터 샘플 (도표 · 요약 · 조건 영작)",
            "header_right": "04~06 · 서답형 1",
            "footer_left": "ARC N° · 공통영어1 Pure B&W 규격",
            "q4": {
                "pill": "실용 · 도표",
                "label": "Booktabs 영문 비교표",
                "no": "04",
                "stem": "다음 표(Primary Study Mode by Grade, 2025, Unit: %)의 내용과 일치하지 않는 것은?",
                "headers": ["Study Mode", "Grade 1", "Grade 2", "Grade 3"],
                "widths": [0.34, 0.22, 0.22, 0.22],
                "rows": [
                    ["Print Workbook", "52%", "46%", "64%"],
                    ["Tablet / PDF", "31%", "38%", "24%"],
                    ["Hybrid Notes", "17%", "16%", "12%"],
                ],
                "choices": [
                    "Print workbook usage reached its highest share in Grade 3 at 64%.",
                    "Tablet / PDF share peaked in Grade 2 among the three surveyed grades.",
                    "In every grade, print workbooks exceeded tablet / PDF in share.",
                    "Hybrid notes accounted for more than one quarter of Grade 1 responses.",
                    "Grade 3 showed the smallest proportion for hybrid notes at 12%.",
                ],
            },
            "q5": {
                "pill": "그래프 · 일치",
                "label": "시계열 흑백 선그래프",
                "no": "05",
                "stem": "다음 그래프(Weekly Study Hours, 2021~2025)의 내용과 일치하는 것은?",
                "draw_diagram": _draw_eng_hours_graph,
                "choices": [
                    "Weekly hours spent on printed sets rose steadily from 2021 to 2025.",
                    "Video-only hours remained higher than printed sets in 2025.",
                    "In 2022, both study formats recorded the exact same weekly hours.",
                    "Printed set hours fell sharply between 2023 and 2025.",
                    "Video-only study hours exceeded 10 hours per week in every year.",
                ],
            },
            "q6": {
                "pill": "요약문 완성",
                "label": "문단 요약 · <요 약 문>",
                "no": "06",
                "stem": "다음 글을 한 문장으로 요약할 때, 빈칸 (A), (B)에 들어갈 말로 가장 적절한 것은?",
                "pre_box_para": "Immediate feedback allows learners to catch minor errors before flawed habits settle into routine. Regular self-checks turn every small correction into lasting mastery.",
                "box_label": "<요 약 문>",
                "box_paras": [
                    "Prompt feedback helps learners ___(A)___ early mistakes before bad habits form, thereby ___(B)___ durable understanding.",
                ],
                "choices": [
                    "ignore  —  blocking",
                    "repeat  —  weakening",
                    "conceal  —  delaying",
                    "detect  —  building",
                    "avoid  —  forgetting",
                ],
            },
            "cr": {
                "pill": "서답형 문항",
                "label": "조건 영작 · <조 건>",
                "no": "[서답형 1]",
                "stem": "우리말 뜻에 맞도록 <조건>을 충족하여 완전한 영어 문장으로 쓰시오.",
                "box_label": "<조 건>",
                "box_paras": [
                    "뜻: 명확한 구조는 가독성을 높일 뿐 아니라 이해도 깊게 한다.",
                    "1. [clear, structure, improve, legibility, deepen, comprehension]을 모두 사용(어형 변화 가능).",
                    "2. 'not only A but also B' 상관접속사 구문을 활용할 것.",
                ],
            },
        },
        "answer": {
            "header_left": "ARC N° | 공통영어1 빠른 정답 · 모범답안",
            "header_right": "01~06 · 서답형 1",
            "footer_left": "ARC N° · 공통영어1 Pure B&W 규격",
            "answers": [(1, 2), (2, 5), (3, 3), (4, 4), (5, 1), (6, 4)],
            "cr_title": "[서답형 1] 모범답안 및 채점 기준",
            "cr_model": "Model Answer: Clear structure not only improves legibility but also deepens comprehension.",
            "cr_rubric": [
                "• 채점 기준 ①: 'not only A but also B' 상관구문 및 3인칭 단수 시제 일치(improves / deepens) 정확히 적용 (60%)",
                "• 채점 기준 ②: 제시된 6개 어휘 모두 포함 및 완전한 단일 문장 구성 (40%)",
            ],
        },
    },
}

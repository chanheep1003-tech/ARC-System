#!/usr/bin/env python3
"""Build the fixed Pure B&W Shidae-Injae-grade ARC N° All-in-One Master Sample PDF & PNGs.

Physical PDF sequence (6 pages):
  Page 1: Swiss architectural Pure B&W cover (with monochrome ARC_N_LOCKUP_MASTER)
  Page 2: Blank cover verso (0 objects)
  Page 3: 2-column body 1 — common passage (prose + verse), <보 기> knockout box, 3-col choices
  Page 4: 2-column body 2 — Booktabs table, monochrome vector diagram, ㄱ·ㄴ·ㄷ <보 기>, [서답형 1]
  Page 5: Blank separator before answer key (0 objects)
  Page 6: 5-item-unit Booktabs quick answer key + [서답형 1] model answer & rubric
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any

import fitz

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tooling" / "typeset"))
from subject_sample_specs import SUBJECT_SAMPLES  # noqa: E402

A4_W, A4_H = 595.276, 841.890
BLACK = (0.0, 0.0, 0.0)
DARK = (0.12, 0.12, 0.12)
MID_GRAY = (0.45, 0.45, 0.45)
RULE_GRAY = (0.72, 0.72, 0.72)
BG_STRIPE = (0.965, 0.965, 0.965)
WHITE = (1.0, 1.0, 1.0)
CIRC = ["①", "②", "③", "④", "⑤"]
COL_X = [(36.3, 286.6), (308.7, 559.0)]
COL_W = 250.3
CANVA_BG_NOTICE = (0.945, 0.945, 0.945)
CANVA_BG_TH = (0.895, 0.895, 0.895)
CANVA_GRID_GRAY = (0.76, 0.76, 0.76)
EXPECTED_LOCKUP_SHA256 = "a61269f152a79343b91f37e75f987f0b5a82d53dc7d9d3a4d067c9830df3bde4"


def resolve_lockup_logo(logo_path: Path | None = None) -> Path | None:
    candidates = [logo_path] if logo_path is not None else []
    candidates.append(ROOT / "templates" / "brand" / "assets" / "ARC_N_LOCKUP_MASTER.png")
    for c in candidates:
        if c.is_file():
            digest = hashlib.sha256(c.read_bytes()).hexdigest()
            if digest != EXPECTED_LOCKUP_SHA256:
                raise RuntimeError(f"BRAND_HASH_MISMATCH: {c} has sha256 {digest}")
            return c
    return None


def _logo_to_bw_png_bytes(logo_path: Path) -> bytes:
    pix = fitz.Pixmap(str(logo_path))
    return fitz.Pixmap(fitz.csGRAY, pix).tobytes("png")


class CanvaFontKit:
    """Modern Korean Gothic font kit matching Canva DAHaz5b2kK0 editorial tone."""

    _MK_RE = re.compile(r"[\u1100-\u11ff\u302e\u302f\u3165-\u318e\ua960-\ua97c\ud7b0-\ud7fb\ue000-\uf8ff]")

    FONT_NAMES = {
        "B_R": "CanvaSansReg",
        "B_B": "CanvaSansBold",
        "G_B": "CanvaKoPubBold",
        "G_R": "CanvaDotumFallback",
    }

    def __init__(self, profile: str = "DEFAULT") -> None:
        self.profile = profile.upper()
        env_dir = os.environ.get("ARC_N_FONT_DIR")
        dirs = ([Path(env_dir)] if env_dir else []) + [
            ROOT / "templates" / "fonts",
            Path(r"C:\Windows\Fonts"),
            Path(r"C:\Program Files\Hancom\Office 2022\HOffice120\Shared\Fonts\Truetype"),
            Path("/usr/share/fonts/truetype/nanum"),
            Path.home() / ".local/share/fonts/nanum",
            Path("/usr/share/fonts"),
        ]
        # KOR unifies modern + Middle Korean (옛한글·방점) on HCR Dotum (HANDotum R/B).
        if self.profile == "KOR":
            names = {
                "B_R": ["HANDotum.ttf", "HanSantteutDotum-Regular.ttf", "NanumGothic.ttf"],
                "B_B": ["HANDotumB.ttf", "HanSantteutDotum-Bold.ttf", "NanumGothicBold.ttf"],
                "G_B": ["KoPub Dotum Bold.ttf", "KoPubDotumBold.ttf", "HANDotumB.ttf", "NanumGothicBold.ttf"],
                "G_R": ["HANDotum.ttf", "malgun.ttf", "NanumGothic.ttf"],
            }
        else:
            names = {
                "B_R": ["HanSantteutDotum-Regular.ttf", "HANDotum.ttf", "NanumGothic.ttf"],
                "B_B": ["HanSantteutDotum-Bold.ttf", "HANDotumB.ttf", "NanumGothicBold.ttf"],
                "G_B": ["KoPub Dotum Bold.ttf", "KoPubDotumBold.ttf", "HANDotumB.ttf", "NanumGothicBold.ttf"],
                "G_R": ["HANDotum.ttf", "malgun.ttf", "NanumGothic.ttf"],
            }
        self.paths: dict[str, Path] = {}
        self.fonts: dict[str, fitz.Font] = {}
        for key, cands in names.items():
            for d in dirs:
                if not d.is_dir():
                    continue
                for n in cands:
                    p = d / n
                    if p.is_file():
                        self.paths[key] = p
                        self.fonts[key] = fitz.Font(fontfile=str(p))
                        break
                if key in self.paths:
                    break
            if key not in self.paths:
                raise RuntimeError(f"REQUIRED_FONT_MISSING ({key}): tried {cands}")

    def register(self, page: fitz.Page) -> None:
        return  # Lazy-registered in put() so unused fallback fonts are not embedded whole

    def runs(self, text: str, key: str) -> list[tuple[str, str]]:
        # Keep headings/strings containing Middle Korean in one unified bold face (B_B) instead of splitting syllables across KoPub + HANDotum.
        if key == "G_B" and self._MK_RE.search(text):
            if all(c.isspace() or self.fonts["B_B"].has_glyph(ord(c)) for c in text):
                key = "B_B"
        primary = self.fonts[key]
        fallback_order = [k for k in ("B_B" if key == "G_B" else "B_R", "G_R", "B_R") if k != key]
        out: list[tuple[str, str]] = []
        for ch in text:
            use_k = key
            if not ch.isspace() and not primary.has_glyph(ord(ch)):
                for fk in fallback_order:
                    if self.fonts[fk].has_glyph(ord(ch)):
                        use_k = fk
                        break
            if out and out[-1][0] == use_k:
                out[-1] = (use_k, out[-1][1] + ch)
            else:
                out.append((use_k, ch))
        return out

    def width(self, text: str, key: str, fontsize: float) -> float:
        return sum(self.fonts[k].text_length(t, fontsize=fontsize) for k, t in self.runs(text, key))

    def put(
        self,
        page: fitz.Page,
        x: float,
        y: float,
        text: str,
        key: str = "B_R",
        fontsize: float = 9.0,
        color: tuple[float, float, float] = BLACK,
    ) -> float:
        existing = {f[4] for f in page.get_fonts()}
        for rk, _ in self.runs(text, key):
            fname = self.FONT_NAMES[rk]
            if fname not in existing:
                page.insert_font(fontname=fname, fontfile=str(self.paths[rk]))
                existing.add(fname)
        cur_x = x
        for rk, rtxt in self.runs(text, key):
            page.insert_text(fitz.Point(cur_x, y), rtxt, fontname=self.FONT_NAMES[rk], fontsize=fontsize, color=color)
            cur_x += self.fonts[rk].text_length(rtxt, fontsize=fontsize)
        return cur_x


FontKit = CanvaFontKit


def _draw_canva_chrome(
    page: fitz.Page,
    fk: FontKit,
    header_left: str,
    header_right: str,
    footer_left: str,
    page_num: int,
) -> None:
    fk.put(page, 36.3, 38.5, header_left, key="G_B", fontsize=8.4, color=DARK)
    fk.put(page, 559.0 - fk.width(header_right, "G_B", 8.4), 38.5, header_right, key="G_B", fontsize=8.4, color=DARK)
    page.draw_line(fitz.Point(36.3, 46.5), fitz.Point(559.0, 46.5), color=BLACK, width=0.7)
    page.draw_line(fitz.Point(36.3, 792.0), fitz.Point(559.0, 792.0), color=RULE_GRAY, width=0.55)
    fk.put(page, 36.3, 807.5, footer_left, key="B_R", fontsize=7.8, color=MID_GRAY)
    pg_str = str(page_num)
    fk.put(page, (A4_W - fk.width(pg_str, "B_R", 8.2)) / 2.0, 807.5, pg_str, key="B_R", fontsize=8.2, color=DARK)


def _draw_fullbar_box(
    page: fitz.Page,
    fk: FontKit,
    x0: float,
    x1: float,
    top: float,
    label: str,
    paragraphs: list[str],
    fs: float = 8.05,
    lh: float = 11.7,
) -> float:
    bar_h = 16.0
    wrapped: list[str] = []
    for para in paragraphs:
        wrapped.extend(_wrap_word_safe(fk, para, "B_R", fs, (x1 - x0) - 19.0))
    pad_top = 8.5
    pad_bot = 8.0
    body_h = pad_top + len(wrapped) * lh + pad_bot
    bottom = top + bar_h + body_h
    page.draw_rect(fitz.Rect(x0, top, x1, bottom), color=BLACK, fill=WHITE, width=0.65)
    page.draw_rect(fitz.Rect(x0, top, x1, top + bar_h), color=BLACK, fill=BLACK)
    lw = fk.width(label, "G_B", 8.0)
    fk.put(page, x0 + (x1 - x0 - lw) / 2.0, top + 11.2, label, key="G_B", fontsize=8.0, color=WHITE)
    by = top + bar_h + pad_top + fs - 1.5
    for ln in wrapped:
        fk.put(page, x0 + 9.5, by, ln, key="B_R", fontsize=fs, color=DARK)
        by += lh
    return bottom


def _draw_pilltab_box(
    page: fitz.Page,
    fk: FontKit,
    x0: float,
    x1: float,
    top: float,
    label: str,
    paragraphs: list[str],
    fs: float = 8.05,
    lh: float = 11.7,
) -> float:
    tab_h = 13.5
    wrapped: list[str] = []
    for para in paragraphs:
        wrapped.extend(_wrap_word_safe(fk, para, "B_R", fs, (x1 - x0) - 19.0))
    pad_top = 12.5
    pad_bot = 7.5
    box_top = top + tab_h / 2.0
    bottom = box_top + pad_top + len(wrapped) * lh + pad_bot
    page.draw_rect(fitz.Rect(x0, box_top, x1, bottom), color=BLACK, fill=WHITE, width=0.65)
    lw = fk.width(label, "G_B", 7.6)
    tab_w = lw + 26.0
    tx0 = x0 + (x1 - x0 - tab_w) / 2.0
    page.draw_rect(fitz.Rect(tx0, top, tx0 + tab_w, top + tab_h), color=BLACK, fill=BLACK)
    fk.put(page, tx0 + 13.0, top + 9.6, label, key="G_B", fontsize=7.6, color=WHITE)
    by = box_top + pad_top + fs - 1.5
    for ln in wrapped:
        fk.put(page, x0 + 9.5, by, ln, key="B_R", fontsize=fs, color=DARK)
        by += lh
    return bottom


def _draw_canva_q_hanging(
    page: fitz.Page,
    fk: FontKit,
    x0: float,
    y: float,
    no_str: str,
    stem_text: str,
    no_fs: float = 13.2,
    stem_fs: float = 8.8,
    lh: float = 12.4,
) -> float:
    fk.put(page, x0, y + 11.5, no_str, key="G_B", fontsize=no_fs, color=BLACK)
    indent = 23.0
    lines = _wrap_word_safe(fk, stem_text, "B_B", stem_fs, COL_W - indent)
    sy = y + 9.5
    for ln in lines:
        fk.put(page, x0 + indent, sy, ln, key="B_B", fontsize=stem_fs, color=BLACK)
        sy += lh
    return max(y + 15.0, sy - lh + 4.5)


def _draw_canva_q_stacked(
    page: fitz.Page,
    fk: FontKit,
    x0: float,
    y: float,
    no_str: str,
    stem_text: str,
    no_fs: float = 13.2,
    stem_fs: float = 8.7,
    lh: float = 12.2,
) -> float:
    fk.put(page, x0, y + 11.5, no_str, key="G_B", fontsize=no_fs, color=BLACK)
    sy = y + 25.5
    lines = _wrap_word_safe(fk, stem_text, "B_R", stem_fs, COL_W)
    for ln in lines:
        fk.put(page, x0, sy, ln, key="B_R", fontsize=stem_fs, color=DARK)
        sy += lh
    return sy - lh + 4.5


def _wrap_word_safe(
    fk: FontKit,
    text: str,
    key: str,
    fontsize: float,
    max_width: float,
    first_width: float | None = None,
) -> list[str]:
    """Wrap Korean/English prose cleanly without splitting ASCII words mid-token."""
    if first_width is None:
        first_width = max_width
    lines: list[str] = []
    for para_idx, raw_para in enumerate(text.split("\n")):
        limit = first_width if para_idx == 0 and not lines else max_width
        if not raw_para.strip():
            lines.append("")
            continue
        tokens: list[str] = []
        buf = ""
        for ch in raw_para:
            if ch == " ":
                if buf:
                    tokens.append(buf)
                    buf = ""
                tokens.append(" ")
            elif ord(ch) < 128 and not ch.isspace():
                buf += ch
            else:
                if buf:
                    tokens.append(buf)
                    buf = ""
                tokens.append(ch)
        if buf:
            tokens.append(buf)

        cur = ""
        for tok in tokens:
            if not cur and tok == " ":
                continue
            cand = cur + tok
            if fk.width(cand, key, fontsize) <= limit or not cur:
                if fk.width(cand, key, fontsize) > limit and tok != " ":
                    for sub in fk.wrap(tok, key, fontsize, limit):
                        if cur:
                            lines.append(cur.rstrip())
                        cur = sub
                        limit = max_width
                else:
                    cur = cand
            else:
                if tok in ".,)]}’”〉》!?:;·" and len(cur.rstrip()) > 1:
                    lines.append(cur[:-1].rstrip())
                    cur = cur[-1] + tok
                else:
                    lines.append(cur.rstrip())
                    cur = "" if tok == " " else tok
                limit = max_width
        if cur:
            lines.append(cur.rstrip())
    return lines or [""]


def _draw_knockout_box(
    page: fitz.Page,
    fk: FontKit,
    x0: float,
    x1: float,
    top: float,
    label: str,
    paragraphs: list[str],
    fs: float = 8.0,
    lh: float = 11.2,
) -> float:
    wrapped: list[str] = []
    for p in paragraphs:
        wrapped.extend(_wrap_word_safe(fk, p, "B_R", fs, (x1 - x0) - 15.0))
    pad_top = 10.0
    pad_bot = 5.0
    box_h = pad_top + len(wrapped) * lh + pad_bot
    bottom = top + box_h
    page.draw_rect(fitz.Rect(x0, top, x1, bottom), color=BLACK, fill=WHITE, width=0.65)
    lw = fk.width(label, "B_B", 7.8)
    lx0 = x0 + (x1 - x0) / 2.0 - lw / 2.0
    page.draw_rect(fitz.Rect(lx0 - 5.0, top - 4.5, lx0 + lw + 5.0, top + 4.5), color=None, fill=WHITE)
    fk.put(page, lx0, top + 2.6, label, key="B_B", fontsize=7.8, color=BLACK)
    by = top + 9.2 + fs
    for ln in wrapped:
        fk.put(page, x0 + 7.5, by, ln, key="B_R", fontsize=fs, color=DARK)
        by += lh
    return bottom


def _draw_choices(
    page: fitz.Page,
    fk: FontKit,
    x0: float,
    y_start: float,
    choices: list[str],
    mode: str = "stack",
    fs: float = 8.15,
    lh: float = 11.1,
) -> float:
    cy = y_start + fs
    if mode == "grid3":
        for i, body in enumerate(choices):
            if i == 3:
                cy += lh + 2.0
            cx = x0 + (i % 3) * (COL_W / 3.0)
            fk.put(page, cx, cy, f"{CIRC[i]} {body}", key="B_R", fontsize=fs, color=BLACK)
        return cy + 6.0
    for i, body in enumerate(choices):
        lines = _wrap_word_safe(fk, body, "B_R", fs, COL_W - 13.0)
        fk.put(page, x0, cy, CIRC[i], key="B_R", fontsize=fs, color=BLACK)
        for li, ln in enumerate(lines):
            if li > 0:
                cy += lh
            fk.put(page, x0 + 11.5, cy, ln, key="B_R", fontsize=fs, color=BLACK)
        cy += lh + 2.0
    return cy + 2.0


def _draw_master_q5_diagram(p: fitz.Page, fk: FontKit, x0: float, gy0: float, x1: float) -> float:
    gh = 110.0
    p.draw_rect(fitz.Rect(x0, gy0, x1, gy0 + gh), color=BLACK, fill=WHITE, width=0.6)
    ox, oy = x0 + 34.0, gy0 + gh - 20.0
    ax_x1, ax_y0 = x1 - 16.0, gy0 + 14.0
    p.draw_line(fitz.Point(ox, oy), fitz.Point(ax_x1, oy), color=BLACK, width=0.9)
    p.draw_line(fitz.Point(ox, oy), fitz.Point(ox, ax_y0), color=BLACK, width=0.9)
    fk.put(p, ox - 24.0, ax_y0 + 5.0, "반응률", key="G_B", fontsize=7.0, color=BLACK)
    fk.put(p, ax_x1 - 16.0, oy + 11.0, "시간(t)", key="G_B", fontsize=7.0, color=BLACK)
    pts_x = [(ox + 15, oy - 10), (ox + 65, oy - 28), (ox + 120, oy - 44), (ox + 175, oy - 50)]
    for i in range(len(pts_x) - 1):
        p.draw_line(fitz.Point(*pts_x[i]), fitz.Point(*pts_x[i + 1]), color=BLACK, width=1.2)
    for px, py in pts_x:
        p.draw_circle(fitz.Point(px, py), 2.3, color=BLACK, fill=BLACK)
    pts_y = [(ox + 15, oy - 50), (ox + 65, oy - 40), (ox + 120, oy - 26), (ox + 175, oy - 14)]
    for i in range(len(pts_y) - 1):
        p.draw_line(fitz.Point(*pts_y[i]), fitz.Point(*pts_y[i + 1]), color=DARK, width=1.0, dashes="[3 2]")
    for px, py in pts_y:
        p.draw_rect(fitz.Rect(px - 2.2, py - 2.2, px + 2.2, py + 2.2), color=BLACK, fill=WHITE, width=0.8)
    fk.put(p, x1 - 74.0, gy0 + 13.0, "● 실선: 조건 X", key="G_B", fontsize=6.9, color=BLACK)
    fk.put(p, x1 - 74.0, gy0 + 23.0, "□ 점선: 조건 Y", key="G_B", fontsize=6.9, color=DARK)
    return gy0 + gh


MASTER_SPEC: dict[str, Any] = {
    "code": "MASTER",
    "pdf_name": "ARC_N_ALL_IN_ONE_MASTER_SAMPLE_V1.0.pdf",
    "png_prefix": "master_sample",
    "cover": {
        "brand_right": "HIGH-SCHOOL ACADEMIC SERIES",
        "edition": "EDITION V1.0 · ALL-IN-ONE MASTER",
        "title1": "ARC N° 표준 조판 마스터",
        "title2": "전 유형 올인원 샘플",
        "badge": "V1.0",
        "pill1": "2022 개정 교육과정 · 고등학교 공통",
        "pill2": "Pure B&W 고정 마스터 규격",
        "notes": [
            "• 표지·러닝헤드·문항 번호·<보기> 바는 고딕 Bold(KoPub), 발문·지문·선지는 한산뜻돋움 Regular로 통일합니다.",
            "• 문항 번호는 13.2pt([서답형 1] 11.6pt)로 절제하고, 불필요한 태그 배지를 제거한 여백 중심 2단 조판을 적용합니다.",
            "• 전 페이지는 100% Pure B&W(무채색)로 조판하며, 표지 뒷면(2쪽)과 정답표 앞면(5쪽)은 인쇄용 완전 백지를 유지합니다.",
        ],
        "table_header": "수록 컴포넌트 및 검증 규격",
        "rows": [
            ("A", "공통 지문 프레임(상단 1.6pt · 산문+운문 복합) + 연계 발문", "01 ~ 02", "3쪽 좌·우단"),
            ("B", "필탭(Pill-tab) / 녹아웃 <보 기> 박스 + 짧은 선지 3열 그리드", "02 ~ 03", "3쪽 우단"),
            ("C", "캔바 스타일 데이터 비교표 + 흑백 벡터 조건 곡선 도식", "04 ~ 05", "4쪽 좌단"),
            ("D", "고난도 풀바(Full-bar) <보 기> + [서답형 1] 줄노트 답안란", "06 · 서답형1", "4쪽 우단"),
            ("KEY", "5문항 단위 Booktabs 교차 채점표 + 서답형 모범답안", "01 ~ 06", "6쪽 정답표"),
        ],
        "subtitle": "문제편 (지문 · 보기 · 표 · 도식 · 서답형)   |   빠른 정답표 (5문항 단위 교차 채점표)",
        "footer": "ARC N° · Pure B&W 고딕 에디토리얼 고정 마스터 디자인 샘플 V1.0",
    },
    "body1": {
        "header_left": "ARC N° | 마스터 조판 샘플 V1.0 (지문 · 보기형)",
        "header_right": "01~03",
        "footer_left": "ARC N° · Pure B&W 고정 마스터 규격",
        "passage": {
            "title": "[01~02] 다음 글을 읽고 물음에 답하시오.",
            "mode": "prose_verse",
            "paras": [
                "(가) 시험지 조판의 품격은 불필요한 장식 태그를 걷어낸 여백과 정보 위계에서 나온다. "
                "발문·지문·선지에는 판독성이 뛰어난 모던 고딕(한산뜻돋움)을, 문항 번호와 <보 기> 라벨에는 "
                "시선을 고정하는 고딕 Bold를 배치하면 수험생의 탐색 리듬이 흐트러지지 않는다."
            ],
            "verse_lines": [
                "(나) 갈바람 불어오는 능선 위로",
                "     먹빛 구름 한 줄기 스쳐 지나니",
                "     묵묵히 선 바위만 제 자리를 지키네.",
            ],
            "source": "― (가) 편집 규범 예시 / (나) 운문 조판 예시 ―",
        },
        "q1": {
            "no": "01",
            "stem": "(가)와 (나)의 조판 원칙을 설명한 내용으로 가장 적절한 것은?",
            "choices": [
                "(가)는 산문 문단 순서를 유지하며 모던 고딕 서체로 조판한다.",
                "(나)는 운문의 행갈이를 제거하고 산문과 한 줄로 이어 붙인다.",
                "지문 프레임은 유채색 그라데이션과 그림자로 시각 강조를 둔다.",
                "선지가 두 줄 이상일 때 둘째 줄은 번호 왼쪽 바깥으로 당긴다.",
                "공통 지문은 연계된 문항마다 본문 전체를 반복 복제해 싣는다.",
            ],
            "mode": "stack",
        },
        "q2": {
            "no": "02",
            "stem": "윗글을 바탕으로 <보기>의 조판 규격을 판단한 것으로 적절하지 않은 것은?",
            "box_label": "< 보 기 >",
            "box_paras": [
                "ARC N° 고정 마스터는 상단 검정 필탭(Pill-tab) 또는 풀바(Full-bar) 라벨로 <보 기>를 구획해 수험생의 시선 집중도를 높인다."
            ],
            "choices": [
                "문항 상단의 불필요한 검정 태그 배지를 제거해 여백을 확보한다.",
                "표지의 공식 로고 역시 무채색 그레이스케일로 톤을 통일한다.",
                "박스 내부 텍스트 길이를 줄이기 위해 본문을 6.5pt로 축소한다.",
                "선택지는 번호 아래로 말려 들어가지 않도록 내어쓰기를 유지한다.",
                "정답표는 문제지와 별개의 물리 페이지로 분리해 배치한다.",
            ],
            "mode": "stack",
        },
        "q3": {
            "no": "03",
            "stem": "ARC N° 물리 페이지 배치 원칙으로 옳은 것만을 <보기>에서 있는 대로 고른 것은?",
            "box_label": "< 보 기 >",
            "box_paras": [
                "ㄱ. 표지 뒷면(2쪽)은 양면 인쇄를 위해 완전 백지로 둔다.",
                "ㄴ. 마지막 문제와 정답표 사이에는 빈 페이지 1장을 둔다.",
                "ㄷ. 모든 문항 상단에 검정 태그 배지를 중복 배치해 밀도를 높인다.",
            ],
            "choices": ["ㄱ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
            "mode": "grid3",
        },
    },
    "body2": {
        "header_left": "ARC N° | 마스터 조판 샘플 V1.0 (표 · 도식 · 서답형)",
        "header_right": "04~06 · 서답형 1",
        "footer_left": "ARC N° · Pure B&W 고정 마스터 규격",
        "q4": {
            "no": "04",
            "stem": "표는 세 구간 A~C의 지표 변화를 정리한 것이다. 이에 대한 해석으로 옳은 것은?",
            "widths": [0.22, 0.26, 0.26, 0.26],
            "headers": ["구분", "집단 A", "집단 B", "집단 C"],
            "rows": [
                ["1차 지표", "12.4", "18.0", "24.5"],
                ["2차 지표", "16.8", "18.0", "19.2"],
                ["판정 결과", "적합", "보류", "초과"],
            ],
            "choices": [
                "집단 A는 1차 대비 2차 지표가 감소하였다.",
                "집단 B는 두 시점의 수치가 동일하게 유지되었다.",
                "집단 C의 2차 지표는 집단 A보다 항상 낮다.",
                "1차 지표가 가장 작은 집단이 판정에서 초과되었다.",
                "세 집단 모두 2차 지표가 1차 지표보다 크다.",
            ],
        },
        "q5": {
            "no": "05",
            "stem": "그림은 조건 X와 Y의 시간에 따른 변화 곡선이다. 이에 대한 설명으로 옳은 것은?",
            "draw_diagram": _draw_master_q5_diagram,
            "choices": [
                "조건 X는 시간이 지날수록 반응률이 감소한다.",
                "조건 Y는 초기 구간에서 조건 X보다 값이 작다.",
                "두 조건의 반응률 역전은 중간 구간에서 한 번 일어난다.",
                "흑백 인쇄 시 두 곡선은 색상 차이로만 구별할 수 있다.",
                "마지막 시점에서도 조건 Y가 조건 X보다 높다.",
            ],
        },
        "q6": {
            "no": "06",
            "stem": "다음 판정 원리를 <보기>의 사례에 적용한 결과로 가장 적절한 것은?",
            "box_label": "< 보 기 >",
            "box_paras": [
                "사례 (가): 형태소 경계에서 음운 변동이 일어나도 본뜻이 유지되면 원형을 밝혀 적는다.",
                "사례 (나): 본뜻에서 멀어져 의미가 분화된 파생어는 소리대로 적는 것을 원칙으로 한다.",
            ],
            "choices": [
                "(가)는 발음 형태를 그대로 표기해 형태소 경계를 지운다.",
                "(나)는 어근의 원형을 반드시 유지해야 하는 예외 조항이다.",
                "(가)는 표의주의 원칙, (나)는 표음주의 원칙이 우선 적용된다.",
                "음운 변동이 일어나지 않는 단어는 모두 (나)에 해당한다.",
                "표기 원리와 무관하게 모든 파생어는 동일한 방식으로 적는다.",
            ],
        },
        "cr": {
            "no": "[서답형 1]",
            "stem": "윗자료의 조판 원칙을 근거로 2단 고정 레이아웃이 갖는 장점을 서술하시오.",
            "box_label": "< 조 건 >",
            "box_paras": [
                "1. 시선 이동 폭과 단 구분선의 역할을 반드시 포함할 것.",
                "2. 한 문장 이상의 완결된 국어 문장으로 작성할 것.",
            ],
        },
    },
    "answer": {
        "header_left": "ARC N° | 빠른 정답 · 모범답안",
        "header_right": "01~06 · 서답형 1",
        "footer_left": "ARC N° · Pure B&W 고정 마스터 규격",
        "answers": [(1, 1), (2, 3), (3, 3), (4, 2), (5, 3), (6, 3)],
        "cr_title": "[서답형 1] 모범답안 및 채점 기준",
        "cr_model": "예시 답안: 2단 고정 레이아웃은 한 줄의 시선 이동 폭을 줄여 가독성을 높이고, 중앙 구분선이 좌·우열의 읽기 흐름을 명확히 분리한다.",
        "cr_rubric": [
            "• 채점 기준 ①: 시선 이동 폭 축소에 따른 가독성 향상 언급 (50%)",
            "• 채점 기준 ②: 중앙 구분선의 좌·우열 분리 기능 및 완결된 문장 구성 (50%)",
        ],
    },
}


def build_cover(doc: fitz.Document, fk: FontKit) -> None:
    build_subject_cover(doc, fk, MASTER_SPEC["cover"])


def build_body_page_1(doc: fitz.Document, fk: FontKit) -> None:
    build_subject_body_1(doc, fk, MASTER_SPEC)


def build_body_page_2(doc: fitz.Document, fk: FontKit) -> None:
    build_subject_body_2(doc, fk, MASTER_SPEC)


def build_answer_page(doc: fitz.Document, fk: FontKit) -> None:
    build_subject_answer(doc, fk, MASTER_SPEC)


def build_subject_cover(doc: fitz.Document, fk: FontKit, cfg: dict[str, Any]) -> None:
    p = doc.new_page(width=A4_W, height=A4_H)
    fk.register(p)

    # Top Swiss metadata bar (Canva DAHaz5b2kK0 cover style)
    fk.put(p, 48.0, 38.0, f"ARC N°  |  {cfg['brand_right']}", key="G_B", fontsize=8.8, color=DARK)
    ed = cfg["edition"]
    fk.put(p, 547.28 - fk.width(ed, "G_B", 8.2), 38.0, ed, key="G_B", fontsize=8.2, color=MID_GRAY)
    p.draw_line(fitz.Point(48.0, 46.5), fitz.Point(547.28, 46.5), color=BLACK, width=0.75)

    # Left vertical bar + monumental 3-line Gothic hero title + pills below title
    p.draw_rect(fitz.Rect(48.0, 74.0, 52.5, 214.0), color=BLACK, fill=BLACK)
    fk.put(p, 66.0, 99.0, "ARC N°", key="G_B", fontsize=23.5, color=BLACK)
    raw_t1 = cfg["title1"]
    clean_t1 = raw_t1[len("ARC N° "):] if raw_t1.startswith("ARC N° ") else raw_t1
    fk.put(p, 66.0, 130.0, clean_t1, key="G_B", fontsize=23.5, color=BLACK)
    fk.put(p, 66.0, 161.0, f"{cfg['title2']} {cfg['badge']}", key="G_B", fontsize=21.5, color=BLACK)

    pill1 = cfg["pill1"]
    p1_w = fk.width(pill1, "G_B", 8.5) + 20.0
    p.draw_rect(fitz.Rect(66.0, 184.0, 66.0 + p1_w, 207.0), color=BLACK, fill=BLACK)
    fk.put(p, 76.0, 198.8, pill1, key="G_B", fontsize=8.5, color=WHITE)

    pill2 = cfg["pill2"]
    p2_x = 66.0 + p1_w + 8.0
    p2_w = fk.width(pill2, "G_B", 8.3) + 18.0
    p.draw_rect(fitz.Rect(p2_x, 184.0, p2_x + p2_w, 207.0), color=BLACK, width=0.8)
    fk.put(p, p2_x + 9.0, 198.8, pill2, key="G_B", fontsize=8.3, color=BLACK)

    # Borderless light-gray editorial notice box ("일러두기 | ...")
    notice_y = 236.0
    wrapped_notes: list[str] = []
    for ln in cfg["notes"]:
        wrapped_notes.extend(_wrap_word_safe(fk, ln, "B_R", 7.8, 408.0))
    notice_h = max(68.0, 20.0 + len(wrapped_notes) * 12.6 + 10.0)
    p.draw_rect(fitz.Rect(48.0, notice_y, 547.28, notice_y + notice_h), color=None, fill=CANVA_BG_NOTICE)
    fk.put(p, 64.0, notice_y + notice_h / 2.0 + 3.0, "일러두기", key="G_B", fontsize=9.8, color=BLACK)
    p.draw_line(fitz.Point(114.0, notice_y + 13.0), fitz.Point(114.0, notice_y + notice_h - 13.0), color=RULE_GRAY, width=0.55)
    ny = notice_y + 21.0
    for sub in wrapped_notes:
        fk.put(p, 126.0, ny, sub, key="B_R", fontsize=7.8, color=DARK)
        ny += 12.6

    # Clean Booktabs grid table (white header, crisp horizontal dividers)
    tbl_top, th_h, row_h = notice_y + notice_h + 26.0, 27.0, 34.0
    cols_x = [48.0, 102.0, 386.0, 466.0, 547.28]
    p.draw_line(fitz.Point(cols_x[0], tbl_top), fitz.Point(cols_x[-1], tbl_top), color=BLACK, width=1.15)
    p.draw_line(fitz.Point(cols_x[0], tbl_top + th_h), fitz.Point(cols_x[-1], tbl_top + th_h), color=BLACK, width=0.75)

    headers = ["유형", cfg.get("table_header", "과목 특화 조판 요소 및 검증 내용"), "문항 번호", "수록 면"]
    for ci, h_txt in enumerate(headers):
        cw = cols_x[ci + 1] - cols_x[ci]
        hw = fk.width(h_txt, "G_B", 8.6)
        hx = cols_x[ci] + (10.0 if ci == 1 else (cw - hw) / 2.0)
        fk.put(p, hx, tbl_top + 17.5, h_txt, key="G_B", fontsize=8.6, color=BLACK)

    ry = tbl_top + th_h
    for ri, (c0, c1, c2, c3) in enumerate(cfg["rows"]):
        fk.put(p, cols_x[0] + (cols_x[1] - cols_x[0] - fk.width(c0, "G_B", 8.8)) / 2.0, ry + 20.5, c0, key="G_B", fontsize=8.8, color=BLACK)
        fk.put(p, cols_x[1] + 10.0, ry + 20.5, c1, key="B_R", fontsize=8.2, color=DARK)
        fk.put(p, cols_x[2] + (cols_x[3] - cols_x[2] - fk.width(c2, "B_B", 8.2)) / 2.0, ry + 20.5, c2, key="B_B", fontsize=8.2, color=BLACK)
        fk.put(p, cols_x[3] + (cols_x[4] - cols_x[3] - fk.width(c3, "B_R", 8.1)) / 2.0, ry + 20.5, c3, key="B_R", fontsize=8.1, color=DARK)
        ry += row_h
        is_last = ri == len(cfg["rows"]) - 1
        p.draw_line(fitz.Point(cols_x[0], ry), fitz.Point(cols_x[-1], ry), color=BLACK if is_last else RULE_GRAY, width=1.15 if is_last else 0.45)

    # Subtitle strip directly under table
    fk.put(p, 48.0, ry + 22.0, cfg["subtitle"], key="B_R", fontsize=8.6, color=MID_GRAY)

    # Bottom 4-column architectural footer grid (matching Canva p1)
    fg_top = 674.0
    fg_bot = 740.0
    seg_w = (547.28 - 48.0) / 4.0
    for si in range(1, 4):
        sx = 48.0 + si * seg_w
        p.draw_line(fitz.Point(sx, fg_top + 6.0), fitz.Point(sx, fg_bot - 6.0), color=RULE_GRAY, width=0.55)

    blocks = [
        ("A4", "PORTRAIT"),
        ("01-06", "+ 서답형 1"),
        ("VERSION", "1.0"),
    ]
    for si, (top_txt, bot_txt) in enumerate(blocks):
        cx = 48.0 + si * seg_w + seg_w / 2.0
        if si < 2:
            fk.put(p, cx - fk.width(top_txt, "G_B", 15.0) / 2.0, fg_top + 31.0, top_txt, key="G_B", fontsize=15.0, color=BLACK)
            fk.put(p, cx - fk.width(bot_txt, "B_R", 7.6) / 2.0, fg_top + 46.0, bot_txt, key="B_R", fontsize=7.6, color=MID_GRAY)
        else:
            fk.put(p, cx - fk.width(top_txt, "B_R", 7.4) / 2.0, fg_top + 23.0, top_txt, key="B_R", fontsize=7.4, color=MID_GRAY)
            fk.put(p, cx - fk.width(bot_txt, "G_B", 16.5) / 2.0, fg_top + 45.0, bot_txt, key="G_B", fontsize=16.5, color=DARK)

    logo = resolve_lockup_logo()
    col3_cx = 48.0 + 3.5 * seg_w
    if logo is not None:
        lw_pt = 82.0
        lh_pt = lw_pt * 380.0 / 565.0
        lx0 = col3_cx - lw_pt / 2.0
        ly0 = fg_top + (fg_bot - fg_top - lh_pt) / 2.0
        p.insert_image(fitz.Rect(lx0, ly0, lx0 + lw_pt, ly0 + lh_pt), stream=_logo_to_bw_png_bytes(logo))
    else:
        fk.put(p, col3_cx - fk.width("ARC N°", "G_B", 15.0) / 2.0, fg_top + 39.0, "ARC N°", key="G_B", fontsize=15.0, color=BLACK)

    p.draw_line(fitz.Point(48.0, 774.0), fitz.Point(547.28, 774.0), color=RULE_GRAY, width=0.55)
    fk.put(p, 48.0, 791.0, cfg["footer"], key="B_R", fontsize=8.0, color=MID_GRAY)


def build_subject_body_1(doc: fitz.Document, fk: FontKit, spec: dict[str, Any]) -> None:
    b1 = spec["body1"]
    p = doc.new_page(width=A4_W, height=A4_H)
    fk.register(p)
    _draw_canva_chrome(p, fk, header_left=b1["header_left"], header_right=b1["header_right"], footer_left=b1["footer_left"], page_num=3)
    p.draw_line(fitz.Point(297.638, 60.0), fitz.Point(297.638, 782.0), color=CANVA_GRID_GRAY, width=0.55)

    # Left Col: Title outside frame + top-bar passage box + Q1 (Canva p2 style, zero tag badge)
    x0, x1 = COL_X[0]
    y = 60.0
    psg = b1["passage"]
    title_lines = _wrap_word_safe(fk, psg["title"], "B_B", 8.8, COL_W)
    ty = y + 9.0
    for tl in title_lines:
        fk.put(p, x0, ty, tl, key="B_B", fontsize=8.8, color=BLACK)
        ty += 12.0

    box_top = ty - 2.0
    p.draw_line(fitz.Point(x0, box_top), fitz.Point(x1, box_top), color=BLACK, width=1.6)
    py = box_top + 18.0
    if psg["mode"] == "lines":
        for ln in psg["lines"]:
            fk.put(p, x0 + 11.0, py, ln, key="B_R", fontsize=8.1, color=DARK)
            py += 11.7
    else:
        for pi, para in enumerate(psg.get("paras", [])):
            for ln in _wrap_word_safe(fk, para, "B_R", 8.0, COL_W - 22.0):
                fk.put(p, x0 + 11.0, py, ln, key="B_R", fontsize=8.0, color=DARK)
                py += 11.5
            if pi < len(psg.get("paras", [])) - 1 or psg.get("verse_lines"):
                py += 5.0
        for ln in psg.get("verse_lines", []):
            fk.put(p, x0 + 11.0, py, ln, key="B_R", fontsize=8.05, color=DARK)
            py += 11.7

    src_txt = psg["source"]
    fk.put(p, x1 - 11.0 - fk.width(src_txt, "B_R", 7.4), py + 4.0, src_txt, key="B_R", fontsize=7.4, color=MID_GRAY)
    box_bot = py + 14.0
    p.draw_line(fitz.Point(x0, box_top), fitz.Point(x0, box_bot), color=BLACK, width=0.5)
    p.draw_line(fitz.Point(x1, box_top), fitz.Point(x1, box_bot), color=BLACK, width=0.5)
    p.draw_line(fitz.Point(x0, box_bot), fitz.Point(x1, box_bot), color=BLACK, width=0.5)

    q1 = b1["q1"]
    y1 = box_bot + 16.0
    y1 = _draw_canva_q_hanging(p, fk, x0, y1, q1["no"], q1["stem"])
    _draw_choices(p, fk, x0, y1 + 3.0, q1["choices"], mode=q1["mode"], fs=8.15, lh=11.4)

    # Right Col: Q2 (pill-tab <보 기>) + rule + Q3 (knockout <보 기> + grid3)
    rx0, rx1 = COL_X[1]
    ry = 60.0
    q2 = b1["q2"]
    ry = _draw_canva_q_hanging(p, fk, rx0, ry, q2["no"], q2["stem"])
    ry = _draw_pilltab_box(p, fk, rx0, rx1, ry + 7.0, q2["box_label"], q2["box_paras"], fs=8.0, lh=11.6)
    ry = _draw_choices(p, fk, rx0, ry + 7.0, q2["choices"], mode=q2["mode"], fs=8.15, lh=11.4)

    div_y = max(ry + 8.0, 404.0)
    p.draw_line(fitz.Point(rx0, div_y), fitz.Point(rx1, div_y), color=RULE_GRAY, width=0.55)

    q3 = b1["q3"]
    ry = div_y + 14.0
    ry = _draw_canva_q_hanging(p, fk, rx0, ry, q3["no"], q3["stem"])
    ry = _draw_knockout_box(p, fk, rx0, rx1, ry + 8.0, q3["box_label"], q3["box_paras"], fs=8.0, lh=11.5)
    _draw_choices(p, fk, rx0, ry + 7.0, q3["choices"], mode=q3["mode"], fs=7.95 if spec["code"] == "ENG" else 8.15, lh=11.5)


def build_subject_body_2(doc: fitz.Document, fk: FontKit, spec: dict[str, Any]) -> None:
    b2 = spec["body2"]
    p = doc.new_page(width=A4_W, height=A4_H)
    fk.register(p)
    _draw_canva_chrome(p, fk, header_left=b2["header_left"], header_right=b2["header_right"], footer_left=b2["footer_left"], page_num=4)
    p.draw_line(fitz.Point(297.638, 60.0), fitz.Point(297.638, 782.0), color=CANVA_GRID_GRAY, width=0.55)

    # Left Top: Q4 Canva table style (stacked smaller number + gray header + full light cell rules)
    x0, x1 = COL_X[0]
    y = 60.0
    q4 = b2["q4"]
    y = _draw_canva_q_stacked(p, fk, x0, y, q4["no"], q4["stem"])

    tbl_y = y + 4.0
    cw = [COL_W * w for w in q4["widths"]]
    th_h, rh = 20.5, 18.0
    tbl_bot = tbl_y + th_h + len(q4["rows"]) * rh
    p.draw_rect(fitz.Rect(x0, tbl_y, x1, tbl_y + th_h), color=None, fill=CANVA_BG_TH)
    p.draw_line(fitz.Point(x0, tbl_y), fitz.Point(x1, tbl_y), color=BLACK, width=1.0)
    p.draw_line(fitz.Point(x0, tbl_y + th_h), fitz.Point(x1, tbl_y + th_h), color=BLACK, width=0.6)
    cx = x0
    for i, h in enumerate(q4["headers"]):
        fk.put(p, cx + (cw[i] - fk.width(h, "G_B", 7.4)) / 2.0, tbl_y + 13.0, h, key="G_B", fontsize=7.4, color=BLACK)
        if i > 0:
            p.draw_line(fitz.Point(cx, tbl_y), fitz.Point(cx, tbl_bot), color=RULE_GRAY, width=0.4)
        cx += cw[i]
    ry = tbl_y + th_h
    for ri, row in enumerate(q4["rows"]):
        cx = x0
        for i, cell in enumerate(row):
            fk.put(p, cx + (cw[i] - fk.width(cell, "B_R", 7.4)) / 2.0, ry + 12.0, cell, key="B_R", fontsize=7.4, color=DARK)
            cx += cw[i]
        ry += rh
        is_last = ri == len(q4["rows"]) - 1
        p.draw_line(fitz.Point(x0, ry), fitz.Point(x1, ry), color=BLACK if is_last else RULE_GRAY, width=1.0 if is_last else 0.4)

    y = _draw_choices(p, fk, x0, ry + 7.0, q4["choices"], mode="stack", fs=8.05, lh=11.3)

    # Left Bottom: Rule + Q5 Diagram
    div_l = max(y + 8.0, 404.0)
    p.draw_line(fitz.Point(x0, div_l), fitz.Point(x1, div_l), color=RULE_GRAY, width=0.55)
    q5 = b2["q5"]
    y = div_l + 12.0
    y = _draw_canva_q_stacked(p, fk, x0, y, q5["no"], q5["stem"])
    fig_bot = q5["draw_diagram"](p, fk, x0, y + 4.0, x1)
    _draw_choices(p, fk, x0, fig_bot + 7.0, q5["choices"], mode="stack", fs=8.0, lh=11.1)

    # Right Top: Q6 (full-bar <보 기> / diagram)
    rx0, rx1 = COL_X[1]
    ry = 60.0
    q6 = b2["q6"]
    ry = _draw_canva_q_stacked(p, fk, rx0, ry, q6["no"], q6["stem"])
    if q6.get("pre_box_para"):
        ry += 2.0
        p_lines = _wrap_word_safe(fk, q6["pre_box_para"], "B_R", 8.0, COL_W - 6.0)
        py = ry + 9.0
        for ln in p_lines:
            fk.put(p, rx0 + 3.0, py, ln, key="B_R", fontsize=8.0, color=DARK)
            py += 11.4
        ry = py - 5.0
    if q6.get("draw_diagram"):
        ry = q6["draw_diagram"](p, fk, rx0, ry + 4.0, rx1)
    if q6.get("box_label"):
        ry = _draw_fullbar_box(p, fk, rx0, rx1, ry + 6.0, q6["box_label"], q6["box_paras"], fs=8.0, lh=11.5)
    ry = _draw_choices(p, fk, rx0, ry + 7.0, q6["choices"], mode="stack", fs=8.05, lh=11.2)

    # Right Bottom: Rule + [서답형 1] (full-bar <조 건> + open ruled lines)
    div_r = max(ry + 8.0, 404.0)
    p.draw_line(fitz.Point(rx0, div_r), fitz.Point(rx1, div_r), color=RULE_GRAY, width=0.55)
    cr = b2["cr"]
    ry = div_r + 12.0
    ry = _draw_canva_q_stacked(p, fk, rx0, ry, cr["no"], cr["stem"], no_fs=11.6)
    ry = _draw_fullbar_box(p, fk, rx0, rx1, ry + 6.0, cr["box_label"], cr["box_paras"], fs=8.0, lh=11.5)

    ans_y = ry + 18.0
    fk.put(p, rx0, ans_y, "답:", key="G_B", fontsize=8.5, color=BLACK)
    line_y = ans_y + 15.0
    while line_y <= 772.0:
        p.draw_line(fitz.Point(rx0, line_y), fitz.Point(rx1, line_y), color=CANVA_GRID_GRAY, width=0.5)
        line_y += 16.5


def build_subject_answer(doc: fitz.Document, fk: FontKit, spec: dict[str, Any]) -> None:
    ans_cfg = spec["answer"]
    p = doc.new_page(width=A4_W, height=A4_H)
    fk.register(p)
    _draw_canva_chrome(p, fk, header_left=ans_cfg["header_left"], header_right=ans_cfg["header_right"], footer_left=ans_cfg["footer_left"], page_num=6)

    fk.put(p, 36.3, 81.0, "정답", key="G_B", fontsize=16.5, color=BLACK)
    fk.put(p, 76.0, 81.0, "QUICK ANSWER KEY · 01~06", key="G_B", fontsize=9.0, color=MID_GRAY)

    grid_x0 = 36.3
    grid_y0 = 104.0
    grid_w = 558.98 - grid_x0
    num_cols = 5
    cell_w = grid_w / num_cols
    th_grid = 22.0
    cell_h = 30.0
    rows_per_col = 5

    p.draw_rect(fitz.Rect(grid_x0, grid_y0, grid_x0 + grid_w, grid_y0 + th_grid), color=None, fill=CANVA_BG_TH)
    for r in range(rows_per_col):
        ry = grid_y0 + th_grid + r * cell_h
        if r % 2 == 1:
            p.draw_rect(fitz.Rect(grid_x0, ry, grid_x0 + grid_w, ry + cell_h), color=None, fill=BG_STRIPE)
        p.draw_line(
            fitz.Point(grid_x0, ry + cell_h),
            fitz.Point(grid_x0 + grid_w, ry + cell_h),
            color=BLACK if r == rows_per_col - 1 else RULE_GRAY,
            width=1.2 if r == rows_per_col - 1 else 0.4,
        )
    p.draw_line(fitz.Point(grid_x0, grid_y0), fitz.Point(grid_x0 + grid_w, grid_y0), color=BLACK, width=1.2)
    p.draw_line(fitz.Point(grid_x0, grid_y0 + th_grid), fitz.Point(grid_x0 + grid_w, grid_y0 + th_grid), color=BLACK, width=0.75)
    for c in range(1, num_cols):
        vx = grid_x0 + c * cell_w
        p.draw_line(fitz.Point(vx, grid_y0), fitz.Point(vx, grid_y0 + th_grid + rows_per_col * cell_h), color=RULE_GRAY, width=0.45)

    for c, hdr in enumerate(["01 ~ 05", "06 ~ 10", "11 ~ 15", "16 ~ 20", "21 ~ 25"]):
        hw = fk.width(hdr, "G_B", 8.5)
        fk.put(p, grid_x0 + c * cell_w + (cell_w - hw) / 2.0, grid_y0 + 14.5, hdr, key="G_B", fontsize=8.5, color=BLACK)

    for idx, (qno, ans_i) in enumerate(ans_cfg["answers"]):
        col_i = idx // rows_per_col
        row_i = idx % rows_per_col
        cx = grid_x0 + col_i * cell_w
        cy = grid_y0 + th_grid + row_i * cell_h
        ans_line = f"{qno:02d}  {CIRC[ans_i - 1]}"
        aw = fk.width(ans_line, "B_B", 10.2)
        fk.put(p, cx + (cell_w - aw) / 2.0, cy + 19.0, ans_line, key="B_B", fontsize=10.2, color=BLACK)

    cr_y = grid_y0 + th_grid + rows_per_col * cell_h + 28.0
    box_w = 558.98 - grid_x0 - 20.0
    model_lines = _wrap_word_safe(fk, ans_cfg["cr_model"], "B_R", 8.5, box_w)
    rubric_lines: list[str] = []
    for rb in ans_cfg["cr_rubric"]:
        rubric_lines.extend(_wrap_word_safe(fk, rb, "B_R", 8.2, box_w))
    cr_h = 38.0 + len(model_lines) * 13.0 + 8.0 + len(rubric_lines) * 13.0 + 12.0

    p.draw_rect(fitz.Rect(grid_x0, cr_y, 558.98, cr_y + cr_h), color=None, fill=CANVA_BG_NOTICE)
    p.draw_rect(fitz.Rect(grid_x0, cr_y, grid_x0 + 3.0, cr_y + cr_h), color=BLACK, fill=BLACK)
    fk.put(p, grid_x0 + 12.0, cr_y + 18.0, ans_cfg["cr_title"], key="G_B", fontsize=9.2, color=BLACK)
    ty = cr_y + 38.0
    for ml in model_lines:
        fk.put(p, grid_x0 + 12.0, ty, ml, key="B_R", fontsize=8.5, color=DARK)
        ty += 13.0
    ty += 6.0
    for rl in rubric_lines:
        fk.put(p, grid_x0 + 12.0, ty, rl, key="B_R", fontsize=8.2, color=DARK)
        ty += 13.0


def render_subject_sample(fk: FontKit, spec: dict[str, Any], out_dir: Path, artifact_dir: Path | None) -> tuple[Path, list[Path]]:
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / spec["pdf_name"]

    doc = fitz.open()
    build_subject_cover(doc, fk, spec["cover"])
    doc.new_page(width=A4_W, height=A4_H)
    build_subject_body_1(doc, fk, spec)
    build_subject_body_2(doc, fk, spec)
    doc.new_page(width=A4_W, height=A4_H)
    build_subject_answer(doc, fk, spec)
    doc.subset_fonts()
    doc.save(str(pdf_path), garbage=2, deflate=True)

    pref = spec["png_prefix"]
    page_map = {
        0: f"{pref}_p1_cover.png",
        2: f"{pref}_p2_body_1.png",
        3: f"{pref}_p3_body_2.png",
        5: f"{pref}_p4_answer_key.png",
    }
    saved_pngs: list[Path] = []
    for pidx, fname in page_map.items():
        png_path = out_dir / fname
        doc[pidx].get_pixmap(dpi=216, alpha=False).save(str(png_path))
        saved_pngs.append(png_path)
        if artifact_dir is not None:
            artifact_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(png_path, artifact_dir / fname)
    doc.close()
    return pdf_path, saved_pngs


MASTER_SOLUTIONS_ITEMS: list[dict[str, Any]] = [
    {
        "no": "01",
        "col": 0,
        "ans": "정답 ①",
        "meta": "문학 · 과정과 태도의 대비 [핵심]",
        "summary": "(가)는 여정의 목적지보다 걸어가는 과정을 강조하고, (나)는 바람·어둠 속에서 삶을 버티며 촛불을 켜겠다는 화자의 태도를 드러낸다.",
        "options": [
            "① [정답] (가)는 과정의 의미를 부각하고, (나)는 현실을 이겨 내려는 다짐을 제시한다.",
            "② [오답] (가)는 삶의 유한함을 다루지만, (나)가 결과 중심의 효율성을 옹호한다는 진술은 어긋난다.",
            "③ [오답] (나)의 화자는 지난날을 애도하는 데 머무르지 않고 앞으로 나아가려는 의지를 보인다.",
            "④ [오답] 두 글 모두 현실 도피나 체념이 아닌 주체적 응전을 보여 준다.",
            "⑤ [오답] 감각적 경험의 배제나 운명 순응은 두 글의 중심 정서와 배치된다.",
        ],
    },
    {
        "no": "02",
        "col": 0,
        "ans": "정답 ③",
        "meta": "문학 · <보기> 감상 적용 [심화]",
        "summary": "ㄱ은 두 작품의 핵심 정서 대응이 정확하고, ㄷ은 <보기>의 '현재에 충실한 삶의 태도'와 직접 연결된다.",
        "options": [
            "ㄱ [적절] (가)의 과정 중심 성찰과 (나)의 결의가 대비·대응을 이룬다.",
            "ㄴ [오답] '바람'은 내적 갈등의 원인이 아니라 시련·외부 역경을 뜻한다.",
            "ㄷ [적절] 결과에 매몰되지 않고 현재의 빛을 밝히려는 태도와 일치한다.",
            "ㄹ [오답] '등불'은 타인의 희생이 아니라 화자 자신의 내면 의지를 뜻한다.",
        ],
    },
    {
        "no": "03",
        "col": 0,
        "ans": "정답 ③",
        "meta": "비문학/문학 · 핵심 개념 연결 [표준]",
        "summary": "(가)에서 여정의 본질로 강조한 핵심 개념은 '과정'(A)이며, (나)에서 화자가 어둠 속에서 택한 행동은 스스로를 '밝혀야 한다'(B)이다.",
        "options": [
            "A [과정] '목적지에 도달하는 순간보다 그 과정'에서 직접 확인된다.",
            "B [밝혀야 한다] '등불 하나 / 내가 더 환히 밝혀야겠다'와 일치한다.",
            "오답 [①·②·④·⑤] '결과·참고·기다림' 등은 본문의 대조를 뒤집었다.",
        ],
    },
    {
        "no": "04",
        "col": 1,
        "ans": "정답 ②",
        "meta": "자료 해석 · 복합 표 분석 [핵심]",
        "summary": "연구개발비 합계는 5,640억 원(평균 1,128억 원), 특허 출원 수 최다 기업은 C(110건, 매출 14,920억 원)이다.",
        "options": [
            "ㄱ [적절] 5개 기업 연구개발비 평균은 5,640 ÷ 5 = 1,128억 원이다.",
            "ㄴ [오답] C의 매출액은 14,920억 원으로 15,000억 원을 넘지 않는다.",
            "ㄷ [적절] 매출액 10,000억 원 미만은 D(7,860억 원)뿐이다.",
            "ㄹ [오답] 특허/개발비 비율 최대는 C(110/1,560 ≈ 0.0705)이다.",
        ],
    },
    {
        "no": "05",
        "col": 1,
        "ans": "정답 ③",
        "meta": "시각 자료 · 시계열 추이 판독 [표준]",
        "summary": "2023년 매출 증가 기업 수와 5년간 단조 증가 여부(B·C)를 그래프의 표식으로 구분해 판정한다.",
        "options": [
            "ㄱ [적절] 2022년 대비 2023년 매출 증가 기업은 A·B·C·D 4개다.",
            "ㄴ [오답] 5년 누적 증가 폭은 C가 최대가 맞지만 A와의 비교 수치 확인이 필요하다.",
            "ㄷ [오답] A와 C 외에도 B가 전 구간 완만한 상승세를 유지한다.",
        ],
    },
    {
        "no": "06",
        "col": 1,
        "ans": "정답 ③",
        "meta": "수식 추론 · 효율성 지수(E) 비교 [고난도]",
        "summary": "효율성 지수 E = 특허 출원 수 / 연구개발비를 04번 표 자료에 대입해 최대·최소 격차와 변화율을 계산한다.",
        "options": [
            "ㄱ [오답] 최대 C(0.0705)와 최소 E(0.0643)의 차이는 약 0.0062로 0.02 미만이다.",
            "ㄴ [적절] 전체 평균 E(≈0.0681)를 웃도는 기업은 C(0.0705)·A(0.0688) 등이다.",
            "ㄷ [적절] B(0.0653)와 D(0.0658)의 백분율 차이는 기준치 범위 내다.",
        ],
    },
    {
        "no": "[서답형 1]",
        "col": 1,
        "ans": "예시 답안 · 10점",
        "meta": "조판 원리 · 채점 기준",
        "is_cr": True,
        "summary": "모범답안: 2단 고정 레이아웃은 한 줄의 시선 이동 폭을 줄여 가독성을 높이고, 중앙 구분선이 좌·우열의 읽기 흐름을 명확히 분리한다.",
        "options": [
            "채점 기준 ① (5점): 시선 이동 폭 축소에 따른 가독성 향상 명시",
            "채점 기준 ② (5점): 중앙 구분선의 열 분리 및 완결 문장 서술",
        ],
    },
]


def build_master_solutions_sample(
    fk: FontKit,
    out_dir: Path,
    artifact_dir: Path | None = None,
) -> tuple[Path, Path]:
    """Generate canonical 2-column Canva Modern Gothic detailed solutions sample (PDF + 216dpi PNG)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / "ARC_N_ALL_IN_ONE_SOLUTIONS_SAMPLE_V1.0.pdf"
    doc = fitz.open()
    p = doc.new_page(width=A4_W, height=A4_H)
    fk.register(p)

    _draw_canva_chrome(
        p,
        fk,
        header_left="ARC N° | 정답 및 상세 해설",
        header_right="DETAILED SOLUTIONS · 01~06",
        footer_left="ARC N° · Pure B&W 2단 해설 마스터 규격",
        page_num=1,
    )
    p.draw_line(fitz.Point(297.638, 60.0), fitz.Point(297.638, 782.0), color=CANVA_GRID_GRAY, width=0.55)

    col_ys = [60.0, 60.0]
    for item in MASTER_SOLUTIONS_ITEMS:
        ci = item["col"]
        x0, x1 = COL_X[ci]
        col_w = x1 - x0
        y = col_ys[ci]

        # Highlight strip + left black bar + black capsule pill
        hdr_h = 20.0
        p.draw_rect(fitz.Rect(x0, y, x1, y + hdr_h), color=None, fill=CANVA_BG_NOTICE)
        p.draw_rect(fitz.Rect(x0, y, x0 + 2.8, y + hdr_h), color=BLACK, fill=BLACK)
        pill_txt = item["no"]
        pw = fk.width(pill_txt, "G_B", 8.2) + 12.0
        p.draw_rect(fitz.Rect(x0 + 7.0, y + 3.0, x0 + 7.0 + pw, y + hdr_h - 3.0), color=BLACK, fill=BLACK)
        fk.put(p, x0 + 13.0, y + 13.2, pill_txt, key="G_B", fontsize=8.2, color=WHITE)
        fk.put(p, x0 + 7.0 + pw + 7.0, y + 13.2, item["ans"], key="G_B", fontsize=8.6, color=BLACK)
        mw = fk.width(item["meta"], "B_R", 7.4)
        fk.put(p, x1 - 6.0 - mw, y + 13.0, item["meta"], key="B_R", fontsize=7.4, color=MID_GRAY)
        y += hdr_h + 11.0

        # Core rationale
        for ln in _wrap_word_safe(fk, item["summary"], "B_B" if item.get("is_cr") else "B_R", 8.0, col_w - 6.0):
            fk.put(p, x0 + 3.0, y, ln, key="B_B" if item.get("is_cr") else "B_R", fontsize=8.0, color=BLACK if item.get("is_cr") else DARK)
            y += 11.4
        y += 2.0

        # Option judgments / rubric bullets
        for opt_line in item["options"]:
            prefix_end = opt_line.find("] ")
            hang = fk.width(opt_line[:2] + " ", "B_R", 7.7) if opt_line[:1] in CIRC else 10.0
            for li, ln in enumerate(_wrap_word_safe(fk, opt_line, "B_R", 7.7, col_w - 8.0 - (hang if len(opt_line) > 20 else 0.0))):
                fk.put(p, x0 + 5.0 + (hang if li > 0 else 0.0), y, ln, key="B_B" if "[정답]" in opt_line and prefix_end > 0 else "B_R", fontsize=7.7, color=DARK)
                y += 10.8
            y += 1.2

        p.draw_line(fitz.Point(x0, y + 2.0), fitz.Point(x1, y + 2.0), color=RULE_GRAY, width=0.45)
        col_ys[ci] = y + 11.0

    doc.subset_fonts()
    doc.save(str(pdf_path), garbage=2, deflate=True)
    png_name = "master_sample_p5_solutions.png"
    png_path = out_dir / png_name
    doc[0].get_pixmap(dpi=216, alpha=False).save(str(png_path))
    doc.close()
    if artifact_dir is not None:
        artifact_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(png_path, artifact_dir / png_name)
    return pdf_path, png_path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", default="MASTER", choices=["MASTER", "KOR", "SOC", "SCI", "ENG", "SUBJECTS", "ALL"])
    ap.add_argument("--out-dir", type=Path, default=ROOT / "templates" / "gold" / "samples")
    ap.add_argument("--artifact-dir", type=Path, default=None)
    args = ap.parse_args()

    canva_fk = CanvaFontKit()
    if args.subject in {"MASTER", "ALL"}:
        out_dir = args.out_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        pdf_path = out_dir / "ARC_N_ALL_IN_ONE_MASTER_SAMPLE_V1.0.pdf"

        doc = fitz.open()
        build_cover(doc, canva_fk)
        doc.new_page(width=A4_W, height=A4_H)  # Page 2: blank verso
        build_body_page_1(doc, canva_fk)     # Page 3: body 1
        build_body_page_2(doc, canva_fk)     # Page 4: body 2
        doc.new_page(width=A4_W, height=A4_H)  # Page 5: blank separator
        build_answer_page(doc, canva_fk)     # Page 6: answer key
        doc.subset_fonts()
        doc.save(str(pdf_path), garbage=2, deflate=True)

        page_map = {
            0: "master_sample_p1_cover.png",
            2: "master_sample_p2_body_passage.png",
            3: "master_sample_p3_body_data_cr.png",
            5: "master_sample_p4_answer_key.png",
        }
        saved_pngs: list[Path] = []
        for pidx, fname in page_map.items():
            png_path = out_dir / fname
            doc[pidx].get_pixmap(dpi=216, alpha=False).save(str(png_path))
            saved_pngs.append(png_path)
            if args.artifact_dir is not None:
                args.artifact_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(png_path, args.artifact_dir / fname)
        doc.close()
        print(f"GENERATED: {pdf_path}")
        for sp in saved_pngs:
            print(f"PNG: {sp}")
        sol_pdf, sol_png = build_master_solutions_sample(canva_fk, out_dir, args.artifact_dir)
        print(f"GENERATED[SOLUTIONS]: {sol_pdf}")
        print(f"PNG[SOLUTIONS]: {sol_png}")

    targets = ["KOR", "SOC", "SCI", "ENG"] if args.subject in {"SUBJECTS", "ALL"} else ([args.subject] if args.subject in SUBJECT_SAMPLES else [])
    if targets:
        subj_dir = args.out_dir / "subjects" if args.out_dir == ROOT / "templates" / "gold" / "samples" else args.out_dir
        kor_fk = CanvaFontKit(profile="KOR") if "KOR" in targets else None
        for code in targets:
            fk = kor_fk if code == "KOR" and kor_fk is not None else canva_fk
            pdf_path, pngs = render_subject_sample(fk, SUBJECT_SAMPLES[code], subj_dir, args.artifact_dir)
            print(f"GENERATED[{code}]: {pdf_path}")
            for sp in pngs:
                print(f"PNG[{code}]: {sp}")


if __name__ == "__main__":
    main()

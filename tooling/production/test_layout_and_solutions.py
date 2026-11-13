#!/usr/bin/env python3
"""TDD test for ARC unified layout design & separate solutions PDF booklet."""
from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[2]
SCI = ROOT / "quality/production/SCI_N_REDOX_SAMPLE_20261110"
SOC = ROOT / "quality/production/SOC_FINAL_SAMPLE_20261110"
KOR = ROOT / "quality/production/KOR_V6_DONGBUK_STYLE_SAMPLE_20261111"

spec_pipe = importlib.util.spec_from_file_location("arc_production_pipeline", ROOT / "tooling/production/production_pipeline.py")
pipeline = importlib.util.module_from_spec(spec_pipe)
assert spec_pipe and spec_pipe.loader
spec_pipe.loader.exec_module(pipeline)

spec_draft = importlib.util.spec_from_file_location("arc_draft_preview", ROOT / "tooling/production/draft_preview.py")
draft_preview = importlib.util.module_from_spec(spec_draft)
assert spec_draft and spec_draft.loader
spec_draft.loader.exec_module(draft_preview)


def page_text(page: fitz.Page) -> str:
    return page.get_text().replace("\u00a0", " ").translate({0x2780 + i: 0x2460 + i for i in range(5)})


def main() -> int:
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)

        # 1. Draft preview on KOR V6 sample must emit both DRAFT_PREVIEW.pdf and SOLUTIONS.pdf
        d_out = tmp / "kor_draft"
        d_rep = draft_preview.run(KOR, d_out)
        assert "solutions_pdf" in d_rep and d_rep["solutions_pdf"], "draft_preview must emit solutions_pdf"
        sol_pdf = Path(d_rep["solutions_pdf"])
        assert sol_pdf.is_file(), "solutions_pdf file must exist"
        with fitz.open(sol_pdf) as sdoc:
            stext = "\n".join(page_text(p) for p in sdoc)
            assert "정답 및 상세 해설" in stext, "solutions PDF must have Korean title header"
            assert "정답" in stext and "①" in stext and "②" in stext, "solutions PDF must include option explanations"

        # 2. ARC_N cover is simple (title + school + logo) without passage/cover_lines list clutter,
        #    and problem items show [D#] difficulty badge.
        sci_out = tmp / "sci_n"
        sci_rep = pipeline.run(SCI, sci_out, archived_replay=True)
        assert sci_rep.get("solutions_pdf") and Path(sci_rep["solutions_pdf"]).is_file()
        with fitz.open(sci_rep["pdf"]) as ndoc:
            cover_txt = page_text(ndoc[0])
            assert "동북고등학교" in cover_txt
            # Cover should not print the bulleted cover_lines list on ARC_N
            assert "산화·환원 반응의 산소·전자 이동 정의" not in cover_txt, "ARC_N cover must stay minimalist (title + school + logo only)"
            prob_txt = "\n".join(page_text(p) for p in ndoc[2:-2])
            assert "[3]" in prob_txt or "[4]" in prob_txt, "Question stems must display difficulty badge"

        # 3. ARC_FINAL first problem page has authentic Dongbuk High School exam banner
        soc_out = tmp / "soc_final"
        soc_rep = pipeline.run(SOC, soc_out, archived_replay=True)
        assert soc_rep.get("solutions_pdf") and Path(soc_rep["solutions_pdf"]).is_file()
        with fitz.open(soc_rep["pdf"]) as fdoc:
            p3_txt = page_text(fdoc[2])
            assert "동북고등학교" in p3_txt and ("고사" in p3_txt or "시험" in p3_txt), (
                "ARC_FINAL first problem page must render the Dongbuk High School exam header banner"
            )

    print("LAYOUT AND SOLUTIONS TEST: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

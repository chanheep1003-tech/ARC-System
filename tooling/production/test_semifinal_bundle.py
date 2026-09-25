#!/usr/bin/env python3
"""Regression on the KOR semi-final bundle: multi-work sets, verse line numbers, constructed
response items, points, Hanja glyph fallback, and the honest blocks (draft literature sources,
FINAL difficulty floor) that must stay blocked until their inputs change."""
from __future__ import annotations

import copy
import importlib.util
import tempfile
from pathlib import Path

import fitz
import yaml

ROOT = Path(__file__).resolve().parents[2]
BUNDLE = ROOT / "quality/production/KOR_SEMIFINAL_20260925"
LOGO = {"path": str(ROOT / "templates/brand/assets/ARC_FINAL_LOCKUP_MASTER.png"),
        "sha256": "e1a5e62f125592f258dfc3fd7224155da5a6c9ef4f92dc164994dd1dcc832b9e", "pixels": (580, 380)}


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


pipeline = _load("arc_production_pipeline", "tooling/production/production_pipeline.py")
renderer = _load("arc_kor_renderer", "tooling/typeset/kor_renderer.py")

MUST_PASS = ["BLIND_INDEPENDENT_SOLVE", "KOR_EXAM_REALISM_GATE", "KOR_AI_STYLE_LEAK_GATE", "ANSWER_LENGTH_AUDIT",
             "ATTRACTIVE_DISTRACTOR_GATE", "CONSTRUCTED_RESPONSE_GATE", "POINTS_GATE", "STEM_FORM_GATE",
             "ANSWER_POSITION_GATE", "HANDOFF", "TYPESET", "BRAND"]


def load(name: str):
    return yaml.safe_load((BUNDLE / name).read_text(encoding="utf-8"))


def run_variant(tmp: Path, name: str, items=None, blind=None):
    work = tmp / name
    work.mkdir()
    (work / "items.yaml").write_text(yaml.safe_dump(items or load("items.yaml"), allow_unicode=True, sort_keys=False), encoding="utf-8")
    (work / "blind_review.yaml").write_text(yaml.safe_dump(blind or load("blind_review.yaml"), allow_unicode=True, sort_keys=False), encoding="utf-8")
    return pipeline.run(work, work / "out", LOGO)


def fails(report) -> set[str]:
    return {f["code"] for f in report["findings"] if f["severity"] == "FAIL"}


def main() -> int:
    # Hanja must come from the CJK fallback, and an unknown glyph must stop rendering instead of printing a box.
    assert [k for k, _ in renderer.runs("안표(顔瓢)", "R")] == ["R", "H", "R"]
    try:
        renderer.runs("\U0010fffd", "R")
    except renderer.RenderError as exc:
        assert "GLYPH_MISSING" in str(exc)
    else:
        raise AssertionError("missing glyph was not blocked")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        base = run_variant(tmp, "baseline")
        for gate in MUST_PASS:
            assert base["gates"][gate] == "PASS", (gate, base["gates"][gate], fails(base))
        m = base["metrics"]
        assert m["mcq_count"] == 22 and m["cr_count"] == 4 and abs(m["total_points"] - 100) < 1e-6
        # Draft literature sources keep content QA and typesetter admission closed.
        assert base["gates"]["CONTENT_QA"] == "FAIL"
        assert "KOR_SOURCE_NOT_EXACT" in base["gates"]["TYPESETTER_ADMISSION"]
        # The FINAL floor is judged on blind difficulty, so a set rated D1-D3 must not pass it.
        blind = load("blind_review.yaml")
        mcq_blind = [b for b in blind["items"] if "difficulty" in b]
        if sum(b["difficulty"] in {"D4", "D5"} for b in mcq_blind) / len(mcq_blind) < 0.30:
            assert base["gates"]["FINAL_DIFFICULTY"] == "FAIL"
        assert base["governance"] == {"FINAL_USER_APPROVAL": "PENDING", "DRIVE_SAVE": "BLOCKED"}

        with fitz.open(base["pdf"]) as doc:
            text = "".join(page.get_text() for page in doc).replace("\xa0", " ")
        assert "顔瓢" in text and "[서술형 4]" in text and "ANSWER KEY" not in text
        with fitz.open(base["answer_key_pdf"]) as doc:
            key_text = "".join(page.get_text() for page in doc).replace("\xa0", " ")
        assert "모범답안" in key_text and "채점 기준" in key_text
        manuscript = (Path(base["pdf"]).parent / "student_manuscript.md").read_text(encoding="utf-8")
        assert "〔40〕" in manuscript, "verse margin numbers missing from the student manuscript"

        items = load("items.yaml")
        off = copy.deepcopy(blind)
        next(b for b in off["items"] if b["item_id"] == "SF-CR4")["meets_rubric"] = False
        r = run_variant(tmp, "cr_off_rubric", blind=off)
        assert "CR_BLIND_ANSWER_OFF_RUBRIC" in fails(r) and r["gates"]["CONSTRUCTED_RESPONSE_GATE"] == "FAIL"

        pts = copy.deepcopy(items)
        next(i for i in pts["items"] if i["item_id"] == "SF-CR1")["points"] = 7
        r = run_variant(tmp, "points", items=pts)
        assert "POINT_TOTAL_NOT_100" in fails(r) and r["gates"]["POINTS_GATE"] == "FAIL"

        ref = copy.deepcopy(items)
        next(i for i in ref["items"] if i["item_id"] == "SF-07")["judgments"][0]["ev"] = ["W2.L15"]
        assert "EVIDENCE_REF_OUT_OF_SOURCE" in fails(run_variant(tmp, "verse_ref", items=ref))

    print("ARC SEMI-FINAL BUNDLE REGRESSION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

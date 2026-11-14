#!/usr/bin/env python3
"""Regression on the KOR semi-final bundle: multi-work sets, verse line numbers, constructed
response items, points, Hanja glyph fallback, the one-round blind policy and the 동북고
school-anchor FINAL difficulty gate (neither easier nor harder than the real exam)."""
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
    return pipeline.run(work, work / "out", LOGO, archived_replay=True)


def fails(report) -> set[str]:
    return {f["code"] for f in report["findings"] if f["severity"] == "FAIL"}


def main() -> int:
    # Hanja must come either natively from the body font (Windows HanSantteutDotum/HANDotum) or CJK fallback (Linux NanumGothic -> H);
    # an unknown glyph must stop rendering instead of printing a box.
    assert [k for k, _ in renderer.runs("안표(顔瓢)", "R")] in (["R", "H", "R"], ["R"])
    if renderer._resolve_font_files("KOR")["R"].name == "HANDotum.ttf":
        saved_subj, saved_fonts = renderer._ACTIVE_SUBJECT, renderer._FONTS
        try:
            renderer._ACTIVE_SUBJECT, renderer._FONTS = "KOR", None
            mk_sample = "나랏말\u110a\u119e미 \u1120\u1173들 마\u1140\u119e\u11af 랏\u302e 말\u302f ㅿ ㆁ ㆆ"
            assert [k for k, _ in renderer.runs(mk_sample, "R")] == ["R"], "KOR Middle Korean must stay single HANDotum run"
            assert [k for k, _ in renderer.runs("ㆍ", "R")] in (["C"], ["R"]), "standalone 아래아 routes to centered dot C when present"
            assert [k for k, _ in renderer.runs("랏\u302e 말\u302f", "GB")] == ["B"], "GB Middle Korean tokens must stay intact in B (HANDotumB)"
        finally:
            renderer._ACTIVE_SUBJECT, renderer._FONTS = saved_subj, saved_fonts
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
        # Literature sources are user-confirmed EXACT, so content QA and admission are open.
        assert base["gates"]["CONTENT_QA"] == "PASS" and base["gates"]["TYPESETTER_ADMISSION"] == "PASS"
        # FINAL difficulty is judged against the 동북고 anchor: this set (blind 1/13/8/0) is easier.
        blind = load("blind_review.yaml")
        assert base["gates"]["FINAL_DIFFICULTY"] == "FAIL"
        assert "FINAL_SCHOOL_ANCHOR_EASIER" in {f["code"] for f in base["final_quality"]["findings"]}
        assert base["final_quality"]["difficulty_profile"]["MODE"] == "SCHOOL_MULTI_EXAM_ANCHOR"
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
        mcq_ids = [b["item_id"] for b in blind["items"] if "difficulty" in b]

        def with_levels(levels):
            forged = copy.deepcopy(blind)
            by_id = {b["item_id"]: b for b in forged["items"]}
            for iid, level in zip(mcq_ids, levels):
                by_id[iid]["difficulty"] = level
            return forged

        # A profile shaped like the anchor passes the FINAL difficulty gate; an all-D4 set is too hard.
        # Multi-exam KOR anchor center is approximately D12 .343 / D3 .400 / D45 .257, mean 2.89.
        # This 22-item profile is D1=1, D2=6, D3=9, D4=6 -> .318/.409/.273, mean 2.91.
        like_anchor = [
            "D1", "D2", "D3", "D3", "D2", "D3", "D4", "D2", "D3", "D4", "D3",
            "D2", "D3", "D4", "D3", "D2", "D4", "D3", "D2", "D3", "D4", "D4"
        ]
        anchor_report = run_variant(tmp, "anchor_like", blind=with_levels(like_anchor))
        assert anchor_report["gates"]["FINAL_DIFFICULTY"] == "PASS", anchor_report["final_quality"]
        assert anchor_report["final_quality"]["difficulty_profile"]["MODE"] == "SCHOOL_MULTI_EXAM_ANCHOR"
        r = run_variant(tmp, "too_hard", blind=with_levels(["D4"] * 22))
        assert "FINAL_SCHOOL_ANCHOR_HARDER" in {f["code"] for f in r["final_quality"]["findings"]}

        # One blind round is policy; a second round without a legacy exemption is blocked.
        twice = copy.deepcopy(blind)
        twice["rounds"] = 2
        twice.pop("round_policy_exemption", None)
        r = run_variant(tmp, "two_rounds", blind=twice)
        assert "BLIND_ROUND_POLICY_VIOLATION" in fails(r) and r["gates"]["BLIND_INDEPENDENT_SOLVE"] == "FAIL"

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

    # Final semi-final (textbook units 1-2 + supplements): one blind round, every gate but the
    # 동북고 difficulty anchor passes; the blind profile (D2 13 / D3 9) is easier than the anchor.
    final_dir = ROOT / "quality/production/KOR_SEMIFINAL_FINAL_20260925"
    with tempfile.TemporaryDirectory() as tmp:
        r = pipeline.run(final_dir, Path(tmp) / "out", LOGO, archived_replay=True)
        assert yaml.safe_load((final_dir / "blind_review.yaml").read_text(encoding="utf-8"))["rounds"] == 1
        for gate in MUST_PASS + ["CONTENT_QA", "TYPESETTER_ADMISSION"]:
            assert r["gates"][gate] == "PASS", (gate, r["gates"][gate])
        assert r["gates"]["FINAL_DIFFICULTY"] == "FAIL"
        assert r["metrics"]["mcq_count"] == 22 and r["metrics"]["cr_count"] == 4
    print("ARC SEMI-FINAL BUNDLE REGRESSION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

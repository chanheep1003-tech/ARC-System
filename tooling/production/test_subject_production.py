#!/usr/bin/env python3
"""SOC/SCI production regression: the same pipeline and renderer as KOR.

Fixtures are synthetic (authored for layout/gate regression, blind review derived
from the key) and run as archived replay, so they can never become release eligible.
Covers: standalone items, bundle material sets, tables, <보기> boxes, a hash-bound
figure, ion super/subscripts, ARC_N inline key and ARC_FINAL separate key PDF."""
from __future__ import annotations

import copy
import importlib.util
import shutil
import tempfile
from pathlib import Path

import fitz
import yaml

ROOT = Path(__file__).resolve().parents[2]
SCI = ROOT / "quality/production/SCI_N_REDOX_SAMPLE_20261110"
SOC = ROOT / "quality/production/SOC_FINAL_SAMPLE_20261110"
KOR = ROOT / "quality/production/KOR_N04_KANTHEGEL_20260925"
spec = importlib.util.spec_from_file_location("arc_production_pipeline", ROOT / "tooling/production/production_pipeline.py")
pipeline = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(pipeline)


def load(bundle: Path, name: str):
    return yaml.safe_load((bundle / name).read_text(encoding="utf-8"))


def run_variant(tmp: Path, name: str, bundle: Path, items=None, blind=None):
    work = tmp / name
    shutil.copytree(bundle, work)
    if items is not None:
        (work / "items.yaml").write_text(yaml.safe_dump(items, allow_unicode=True, sort_keys=False), encoding="utf-8")
    if blind is not None:
        (work / "blind_review.yaml").write_text(yaml.safe_dump(blind, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return pipeline.run(work, work / "out", archived_replay=True)


def page_text(page) -> str:
    # Some Nanum builds map the circled-digit glyphs to the dingbat code points (U+2780..) on extraction.
    return page.get_text().replace("\u00a0", " ").translate({0x2780 + i: 0x2460 + i for i in range(5)})


def fail_codes(report) -> set[str]:
    return {f["code"] for f in report["findings"] if f["severity"] == "FAIL"}


def assert_clean(report, subject: str, product: str) -> None:
    # Archived replay is the only allowed blocker for a synthetic fixture.
    assert report["blocking_gates"] == ["EXAM_SCOPE"], report["blocking_gates"]
    assert report["gates"]["EXAM_SCOPE"] == "ARCHIVED_REPLAY"
    assert not fail_codes(report), fail_codes(report)
    for gate in (f"{subject}_EXAM_REALISM_GATE", f"{subject}_AI_STYLE_LEAK_GATE", f"{subject}_SCHOOL_TASK_FAMILY_GATE",
                 "CONTENT_QA", "BLIND_INDEPENDENT_SOLVE", "ANSWER_LENGTH_AUDIT", "ATTRACTIVE_DISTRACTOR_GATE",
                 "STEM_FORM_GATE", "ANSWER_POSITION_GATE", "DIFFICULTY_BALANCE_GATE", "HANDOFF",
                 "TYPESETTER_ADMISSION", "TYPESET"):
        assert report["gates"][gate] == "PASS", (gate, report["gates"][gate])
    # ARC_FINAL has a blank cover verso, which preflight reports as a WARN for KOR as well.
    assert report["gates"]["PDF_QC"] == ("PASS" if product == "ARC_N" else "WARN"), report["gates"]["PDF_QC"]
    assert not any(k.startswith("KOR_") for k in report["gates"]), "KOR gate names leaked into another subject"
    assert report["product"] == product


def main() -> int:
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)

        # --- SCI ARC_N: material set, table, view, figure, ion notation, inline answer key ---
        sci = run_variant(tmp, "sci", SCI)
        assert_clean(sci, "SCI", "ARC_N")
        doc = fitz.open(sci["pdf"])
        text = "\n".join(page_text(page) for page in doc)
        assert len(doc) == 6, len(doc)                       # cover, verso, 2 problem pages, separator, key
        assert sum(len(page.get_images(full=True)) for page in doc) == 1, "figure must be embedded exactly once"
        assert "[5~6] 다음은 금속의 반응성에 대한 실험이다." in text
        assert "A2+" in text and "B3+" in text, "ion charges must come from the body font"
        assert "ANSWER KEY" in page_text(doc[-1]) and "03  ④" in page_text(doc[-1])
        manuscript = (tmp / "sci/out/student_manuscript.md").read_text(encoding="utf-8")
        assert "〔그림〕" in manuscript and "| 금속 |" in manuscript
        qa = yaml.safe_load(next((tmp / "sci/out").glob("ARC_QA_EVIDENCE_*.yaml")).read_text(encoding="utf-8"))
        assert qa["uses_source_text"] is False and qa["source_text_locks"] == []
        assert qa["generated_material"][0]["origin"] == "GENERATED"
        assert all(item["pass_b"]["scope_trace"]["source_refs"] for item in qa["items"])

        # --- SOC ARC_FINAL: points, FINAL gate with the SOC anchor, separate key PDF ---
        soc = run_variant(tmp, "soc", SOC)
        assert_clean(soc, "SOC", "ARC_FINAL")
        assert soc["gates"]["FINAL_DIFFICULTY"] == "PASS" and soc["gates"]["FINAL_ITEM_QUALITY"] == "PASS"
        assert soc["metrics"]["total_points"] == 100
        problem = "\n".join(page_text(page) for page in fitz.open(soc["pdf"]))
        assert "ANSWER KEY" not in problem, "FINAL problem sheet must not expose the key"
        assert "(선택형 8~9번)" in problem
        assert "ANSWER KEY" in page_text(fitz.open(soc["answer_key_pdf"])[0])

        # --- fault injection ---
        # 1. KOR must keep registry-locked raw text: bundle-authored material is refused.
        kor_items = load(KOR, "items.yaml")
        kor_bad = copy.deepcopy(kor_items)
        kor_bad.pop("passages")
        kor_bad["sets"] = [{"id": "P1", "works": [{"material": {"origin": "GENERATED", "paragraphs": ["임의로 쓴 지문."]}}]}]
        try:
            run_variant(tmp, "kor_material", KOR, items=kor_bad)
            raise AssertionError("KOR material set must be refused")
        except pipeline.PipelineError as exc:
            assert "MATERIAL_FORBIDDEN_FOR_SUBJECT" in str(exc), exc

        sci_items = load(SCI, "items.yaml")
        # 2. A figure whose bytes differ from the registered hash never reaches the page.
        bad = copy.deepcopy(sci_items)
        next(i for i in bad["items"] if i.get("figure"))["figure"]["sha256"] = "0" * 64
        try:
            run_variant(tmp, "sci_figure", SCI, items=bad)
            raise AssertionError("tampered figure must be refused")
        except pipeline.PipelineError as exc:
            assert "FIGURE_CHECKSUM_MISMATCH" in str(exc), exc

        # 3. Non-registry subjects must say where each item sits in the range.
        bad = copy.deepcopy(sci_items)
        bad.pop("scope_refs")
        report = run_variant(tmp, "sci_scope", SCI, items=bad)
        assert "SCOPE_REF_MISSING" in fail_codes(report)
        assert report["gates"]["CONTENT_QA"] != "PASS"

        # 4. An option with no evidence reference is not auditable.
        bad = copy.deepcopy(sci_items)
        bad["items"][0]["judgments"][0]["ev"] = []
        assert "EVIDENCE_REF_MISSING" in fail_codes(run_variant(tmp, "sci_ev", SCI, items=bad))

        # 5. A passage reference on a standalone item points at nothing.
        bad = copy.deepcopy(sci_items)
        bad["items"][0]["judgments"][0]["ev"] = ["P1S1"]
        assert "EVIDENCE_REF_OUT_OF_SOURCE" in fail_codes(run_variant(tmp, "sci_ref", SCI, items=bad))

        # 6. Key/blind disagreement blocks exactly as it does for KOR.
        blind = load(SCI, "blind_review.yaml")
        blind["items"][2]["answer"] = 1
        report = run_variant(tmp, "sci_blind", SCI, blind=blind)
        assert "BLIND_ANSWER_MISMATCH" in fail_codes(report)
        assert report["gates"]["BLIND_INDEPENDENT_SOLVE"] == "FAIL"

        # 7. ADVANCED share outside the universal 20-30% target fails the N balance gate.
        bad = copy.deepcopy(sci_items)
        for it in bad["items"]:
            it["balance"] = "CORE_EXAM_POINT"
        assert "BALANCE_ADVANCED_OUT_OF_RANGE" in fail_codes(run_variant(tmp, "sci_balance", SCI, items=bad))

        # 8. Material that claims a school/public origin needs a source reference.
        bad = copy.deepcopy(sci_items)
        bad["sets"][0]["works"][0]["material"]["origin"] = "SCHOOL_SOURCE"
        try:
            run_variant(tmp, "sci_origin", SCI, items=bad)
            raise AssertionError("school-origin material without a source_ref must be refused")
        except pipeline.PipelineError as exc:
            assert "MATERIAL_SOURCE_REF_MISSING" in str(exc), exc

    print("subject production regression: SCI ARC_N + SOC ARC_FINAL PASS, 8 faults blocked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

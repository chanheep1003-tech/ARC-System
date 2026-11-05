#!/usr/bin/env python3
"""Production pipeline regression on the real KOR N04 bundle plus fault injection.

The bundle's measured verdicts must follow from its own data (no self-reported
metrics), and every injected fault must be blocked by the named gate."""
from __future__ import annotations

import copy
import importlib.util
import shutil
import tempfile
from pathlib import Path

import fitz
import yaml

ROOT = Path(__file__).resolve().parents[2]
BUNDLE = ROOT / "quality/production/KOR_N04_KANTHEGEL_20260925"
spec = importlib.util.spec_from_file_location("arc_production_pipeline", ROOT / "tooling/production/production_pipeline.py")
pipeline = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(pipeline)

INTEGRITY_GATES = ["BLIND_INDEPENDENT_SOLVE", "KOR_EXAM_REALISM_GATE", "KOR_AI_STYLE_LEAK_GATE", "KOR_SCHOOL_TASK_FAMILY_GATE",
                   "ANSWER_LENGTH_AUDIT", "ATTRACTIVE_DISTRACTOR_GATE", "STEM_FORM_GATE", "ANSWER_POSITION_GATE",
                   "HANDOFF", "TYPESET", "PDF_QC"]


def load(name: str):
    return yaml.safe_load((BUNDLE / name).read_text(encoding="utf-8"))


def run_variant(tmp: Path, name: str, items=None, blind=None):
    work = tmp / name
    work.mkdir()
    (work / "items.yaml").write_text(yaml.safe_dump(items or load("items.yaml"), allow_unicode=True, sort_keys=False), encoding="utf-8")
    (work / "blind_review.yaml").write_text(yaml.safe_dump(blind or load("blind_review.yaml"), allow_unicode=True, sort_keys=False), encoding="utf-8")
    return pipeline.run(work, work / "out", archived_replay=True)


def codes(report) -> set[str]:
    return {f["code"] for f in report["findings"] if f["severity"] == "FAIL"}


def main() -> int:
    # Regression: six exception-stem items in the real 2026 semifinal fixture
    # require one FALSE answer; do not infer polarity from family alone.
    semifinal = yaml.safe_load((
        ROOT / "quality/production/KOR_SEMIFINAL_FINAL_20260925/items.yaml"
    ).read_text(encoding="utf-8"))
    semiconductor_items = pipeline.mcq_items(semifinal)
    negative_ids = {
        item["item_id"] for item in semiconductor_items
        if pipeline.korean_stem_polarity(item) == "NEGATIVE"
    }
    assert negative_ids == {"FS-03", "FS-08", "FS-13", "FS-18", "FS-19", "FS-21"}, negative_ids
    for item in semiconductor_items:
        polarity = pipeline.korean_stem_polarity(item)
        truth = [judgment["v"] for judgment in item["judgments"]]
        answer_index = int(item["answer"]) - 1
        expected = "FALSE" if polarity == "NEGATIVE" else "TRUE"
        assert truth[answer_index] == expected, (item["item_id"], polarity)
        assert truth.count(expected) == 1, (item["item_id"], truth)

    # Explicit contradictory metadata must never override the question itself.
    conflict = dict(semiconductor_items[0])
    conflict["stem_polarity"] = "NEGATIVE"
    try:
        pipeline.korean_stem_polarity(conflict)
    except ValueError:
        pass
    else:
        raise AssertionError("contradictory stem polarity was accepted")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        base = run_variant(tmp, "baseline")
        for gate in INTEGRITY_GATES:
            assert base["gates"][gate] == "PASS", (gate, base["gates"][gate], base["findings"])
        assert base["governance"] == {"FINAL_USER_APPROVAL": "PENDING", "DRIVE_SAVE": "BLOCKED"}

        # Balance verdict must be derived from the blind difficulties, not declared.
        blind = load("blind_review.yaml")
        n = len(blind["items"])
        d45 = sum(1 for b in blind["items"] if b["difficulty"] in {"D4", "D5"}) / n
        assert abs(base["metrics"]["balance"]["D45"] - d45) < 1e-9
        expected_fail = not 0.15 <= d45 <= 0.35
        assert (base["gates"]["DIFFICULTY_BALANCE_GATE"] == "FAIL") == (expected_fail or "BALANCE_D1_OUT_OF_RANGE" in codes(base))

        items = load("items.yaml")

        cue = copy.deepcopy(items)
        target = cue["items"][0]
        target["options"][target["answer"] - 1] += " 이는 윗글의 여러 문단에 걸쳐 제시된 설명을 종합하여 확인할 수 있는 내용이다."
        assert "CORRECT_LENGTH_CUE" in codes(run_variant(tmp, "length_cue", items=cue))

        leak = copy.deepcopy(items)
        leak["items"][1]["stem"] = "판단축을 고려할 때 " + leak["items"][1]["stem"]
        r = run_variant(tmp, "leak", items=leak)
        assert "STUDENT_METADATA_LEAK" in codes(r) and r["gates"]["KOR_AI_STYLE_LEAK_GATE"] == "FAIL"

        mismatch = copy.deepcopy(blind)
        first = mismatch["items"][0]
        first["answer"] = 1 if first["answer"] != 1 else 2
        r = run_variant(tmp, "blind_mismatch", blind=mismatch)
        assert "BLIND_ANSWER_MISMATCH" in codes(r) and r["gates"]["BLIND_INDEPENDENT_SOLVE"] == "FAIL"
        assert r["gates"]["CONTENT_QA"] == "FAIL"

        multi = copy.deepcopy(blind)
        multi["items"][3]["flags"] = ["a"]
        assert "BLIND_MULTIPLE_ANSWERS" in codes(run_variant(tmp, "blind_multi", blind=multi))

        run3 = copy.deepcopy(items)
        run3["items"][6]["stem"] = "윗글의 헤겔의 관점에서 칸트에게 던질 물음으로 가장 적절한 것은?"
        assert "STEM_SKELETON_RUN" in codes(run_variant(tmp, "stem_run", items=run3))

        tamper = copy.deepcopy(items)
        tamper["passages"][0]["marks"] = [{"find": "파괴적 성향을 띨 수 있다고", "replace": "파괴적 경향을 ⓐ띨 수 있다고"}]
        try:
            run_variant(tmp, "source_tamper", items=tamper)
        except pipeline.PipelineError as exc:
            assert "SOURCE_MARK_CHANGES_WORDS" in str(exc)
        else:
            raise AssertionError("source wording change was not blocked")

        final = copy.deepcopy(items)
        final["product_mode"] = "ARC_FINAL"
        r = run_variant(tmp, "final_mode", items=final)
        assert r["final_quality"] is not None and r["gates"]["FINAL_DIFFICULTY"] in {"PASS", "FAIL"}
        assert r["gates"]["FINAL_DIFFICULTY"] == "FAIL", "KOR N04 converted to FINAL must fail the Dongbuk multi-exam anchor"
        assert "FINAL_SCHOOL_ANCHOR_EASIER" in {f["code"] for f in r["final_quality"]["findings"]}
        assert r["final_quality"]["difficulty_profile"]["MODE"] == "SCHOOL_MULTI_EXAM_ANCHOR"
        assert r["answer_key_pdf"] and Path(r["answer_key_pdf"]).is_file()
        with fitz.open(r["pdf"]) as doc:
            assert not any("ANSWER KEY" in page.get_text() for page in doc), "FINAL problem sheet exposes the key"

    print("ARC PRODUCTION PIPELINE REGRESSION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

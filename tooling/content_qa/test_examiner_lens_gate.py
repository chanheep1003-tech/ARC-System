#!/usr/bin/env python3
"""Examiner-lens gate regression: school-style sample passes; masked-spacing set and injected faults fail."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("arc_examiner_lens_gate", ROOT / "tooling/content_qa/examiner_lens_gate.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def load(name: str) -> dict:
    return yaml.safe_load((ROOT / "quality/production" / name / "items.yaml").read_text(encoding="utf-8"))


def codes(report: dict) -> set[str]:
    return {f["code"] for f in report["findings"]}


def lens_item(**over) -> dict:
    item = {
        "item_id": "T-001",
        "stem": "<보기>를 참고하여 ㉠~㉤의 띄어쓰기를 설명한 내용으로 가장 적절한 것은?",
        "options": ["가", "나", "다", "라", "마"],
        "answer": 2,
        "blueprint": {"unit": "3-2", "behavior": "적용", "difficulty": "D3"},
        "teaching_anchor": "교과서 p.118 학습활동 2",
        "distractor_misconceptions": {1: "a", 3: "b", 4: "c", 5: "d"},
        "appeal_check": "PASS",
    }
    item.update(over)
    return item


def main() -> int:
    # Pronunciation brackets ([꼬치]) and A3 <보기 2> target marks are allowed.
    assert gate.analyze(load("KOR_V6_DONGBUK_STYLE_SAMPLE_20261111"))["status"] == "PASS"
    # Masked spacing (년[만]에) is not a school exam-sheet convention.
    assert "NON_SCHOOL_MARKUP" in codes(gate.analyze(load("KOR_V6_ORTHO_A_20261111")))

    ok = {"examiner_lens": "V1.0", "items": [lens_item()]}
    assert gate.analyze(ok)["status"] == "PASS", gate.analyze(ok)

    clone = copy.deepcopy(ok)
    clone["items"][0]["distractor_misconceptions"] = {1: "a", 3: "a", 4: "c", 5: "d"}
    assert "CLONE_DISTRACTORS" in codes(gate.analyze(clone))

    for field, code in (("teaching_anchor", "NOT_TAUGHT"), ("blueprint", "MISSING_BLUEPRINT"),
                        ("appeal_check", "MISSING_APPEAL_CHECK")):
        broken = copy.deepcopy(ok)
        broken["items"][0].pop(field)
        assert code in codes(gate.analyze(broken)), code

    gap = copy.deepcopy(ok)
    gap["items"][0]["distractor_misconceptions"] = {1: "a", 3: "b", 4: "c"}
    assert "MISSING_MISCONCEPTION" in codes(gate.analyze(gap))

    leak = {"items": [lens_item(stem="정답 후보를 판단축에 따라 고른 것은?")]}
    assert "META_LANGUAGE_LEAK" in codes(gate.analyze(leak))

    skew = {"items": [lens_item(item_id=f"S-{i}", answer=3) for i in range(20)]}
    report = gate.analyze(skew)
    assert "ANSWER_POSITION_SKEW" in codes(report) and report["status"] == "WARN"

    longest = {"items": [lens_item(item_id=f"L-{i}", options=["가", "나나나나", "다", "라", "마"]) for i in range(10)]}
    assert "LONGEST_ANSWER_CUE" in codes(gate.analyze(longest))

    # V1.1 discrimination lens: transfer levels, novel material, set mix.
    def v11_item(i: int, level: str, novel: dict | None = None) -> dict:
        item = lens_item(item_id=f"V-{i}", answer=(i % 5) + 1, transfer_level=level,
                         distractor_misconceptions={k: f"m{k}" for k in range(1, 6) if k != (i % 5) + 1})
        if novel:
            item["novel_material"] = novel
        return item

    new = {"kind": "NEW_EXAMPLE", "source": "AUTHORED"}
    clause = {"kind": "NEW_CLAUSE", "source": "한글 맞춤법 제57항"}
    good_mix = ["RECALL", "RECALL", "APPLY", "APPLY", "APPLY", "INFER", "INFER", "EXTEND", "APPLY", "INFER"]
    good = {"examiner_lens": "V1.1", "product_mode": "ARC_N",
            "items": [v11_item(i, lv, clause if lv == "EXTEND" else (new if lv != "RECALL" else None))
                      for i, lv in enumerate(good_mix)]}
    assert gate.analyze(good)["status"] == "PASS", gate.analyze(good)

    recall_heavy = copy.deepcopy(good)
    for it in recall_heavy["items"][:8]:
        it["transfer_level"] = "RECALL"
    assert {"RECALL_OVERUSE", "TRANSFER_SHORT"} <= codes(gate.analyze(recall_heavy))

    no_novel = copy.deepcopy(good)
    no_novel["items"][5].pop("novel_material")
    assert "NOVEL_MATERIAL_MISSING" in codes(gate.analyze(no_novel))

    weak_extend = copy.deepcopy(good)
    weak_extend["items"][7]["novel_material"] = new
    assert "EXTEND_WITHOUT_NEW_CONDITION" in codes(gate.analyze(weak_extend))

    unlabeled = copy.deepcopy(good)
    unlabeled["items"][0].pop("transfer_level")
    assert "MISSING_TRANSFER_LEVEL" in codes(gate.analyze(unlabeled))

    # The 2026-11-14 draft set is all RECALL/APPLY: under V1.1 it must be flagged.
    draft = load("KOR_N_MKO10_20261114")
    draft["examiner_lens"] = "V1.1"
    for it in draft["items"]:
        it["transfer_level"] = "APPLY"
    assert "TRANSFER_SHORT" in codes(gate.analyze(draft))

    # V1.2 (2026-11-14 user review): one-cell grid capped at D3; new clauses/data need student support.
    trial = load("KOR_N_MKV11_20261114")
    trial["examiner_lens"] = "V1.2"
    found = {(f["code"], f["item_id"]) for f in gate.analyze(trial)["findings"]}
    assert ("GRID_ONE_CELL_D4", "KOR-MKV-03") in found, found
    assert ("STUDENT_SUPPORT_MISSING", "KOR-MKV-09") in found, found
    assert gate.analyze(load("KOR_N_MKV12_20261114"))["status"] == "PASS"

    # V1.3 (2026-11-14 user directive): harder items must be INFER/EXTEND; no fixed mix.
    v13 = load("KOR_N_MKV12_20261114")
    v13["examiner_lens"] = "V1.3"
    found = {(f["code"], f["item_id"]) for f in gate.analyze(v13)["findings"]}
    assert ("DIFFICULTY_TRANSFER_MISMATCH", "KOR-MKW-04") in found, found   # RECALL labelled D4
    assert not any(c == "TRANSFER_SHORT" for c, _ in found)
    basic = {"examiner_lens": "V1.3", "product_mode": "ARC_N",
             "items": [v11_item(i, "RECALL" if i < 6 else "APPLY") for i in range(10)]}
    for it in basic["items"]:
        it["difficulty"] = "D2"
    assert gate.analyze(basic)["status"] == "PASS", gate.analyze(basic)   # a basic set may be mostly RECALL
    hard = copy.deepcopy(basic)
    hard["items"][0]["difficulty"] = "D5"
    hard["items"][0]["transfer_level"] = "INFER"
    hard["items"][0]["novel_material"] = new
    assert "DIFFICULTY_TRANSFER_MISMATCH" in codes(gate.analyze(hard))

    print("examiner lens gate regression: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

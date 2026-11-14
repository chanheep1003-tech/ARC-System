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

    print("examiner lens gate regression: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

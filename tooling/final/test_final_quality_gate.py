#!/usr/bin/env python3
"""Behavioral smoke for ARC FINAL quality gate."""
from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("final_quality_gate", ROOT / "tooling/final/final_quality_gate.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)

def item(i, d, correct=2, lengths=None):
    return {
        "item_id": f"F-{i:03d}",
        "actual_difficulty": d,
        "reasoning_steps": 3 if d == "D5" else (2 if d in {"D3", "D4"} else 1),
        "evidence_count": 2 if d == "D5" else 1,
        "strong_distractor_count": 2,
        "effective_choice_count": 5 if d in {"D4", "D5"} else 4,
        "first_pass_plausible_candidates": 3,
        "immediate_elimination_count": 1 if d == "D5" else 2,
        "correct_option": correct,
        "second_best_option": 3 if correct != 3 else 4,
        "second_best_refutation": "Fails one limiting condition.",
        "option_lengths_chars": lengths or [32, 34, 31, 35, 33],
        "correct_detail_outlier": False,
        "length_justified": False,
        "school_relative": "ABOVE_SCHOOL" if d == "D5" else ("SCHOOL_UPPER" if d == "D4" else "SCHOOL_STANDARD"),
        "expected_time_class": "LONG" if d == "D5" else "STANDARD",
    }

diffs=["D2","D3","D3","D3","D3","D3","D4","D4","D4","D5"]
good={"product_mode":"ARC_FINAL","item_count":10,"items":[item(i+1,d) for i,d in enumerate(diffs)]}
assert mod.analyze(good)["status"] == "PASS"

multi_anchor = {
    "anchor_id": "TEST_MULTI_EXAM",
    "mode": "MULTI_EXAM_ENSEMBLE",
    "source_exam_count": 4,
    "corpus": "quality/anchors/DONGBUK_ACTUAL_EXAM_DIFFICULTY_CORPUS_V1.0.yaml",
    "confidence": "HIGH",
    "profile": {
        "shares": {"D12": 0.10, "D3": 0.50, "D45": 0.40},
        "mean_level": 3.40,
    },
    "tolerance": {"share": 0.001, "mean_level": 0.01, "late_section_d45_min": 1},
}
anchored = dict(good)
anchored["difficulty_anchor_required"] = True
anchored["difficulty_anchor"] = multi_anchor
assert mod.analyze(anchored)["status"] == "PASS"
assert mod.analyze(anchored)["difficulty_profile"]["MODE"] == "SCHOOL_MULTI_EXAM_ANCHOR"

missing = dict(good)
missing["difficulty_anchor_required"] = True
assert "FINAL_SCHOOL_ANCHOR_MISSING" in {x["code"] for x in mod.analyze(missing)["findings"]}

bad_provenance = dict(anchored)
bad_provenance["difficulty_anchor"] = dict(multi_anchor)
bad_provenance["difficulty_anchor"]["source_exam_count"] = 1
assert "FINAL_ANCHOR_PROVENANCE_INVALID" in {x["code"] for x in mod.analyze(bad_provenance)["findings"]}

weak={"product_mode":"ARC_FINAL","item_count":10,"items":[dict(x) for x in good["items"]]}
weak["items"][2]["strong_distractor_count"]=0
assert "WEAK_DISTRACTOR_HARD_FAIL" in {x["code"] for x in mod.analyze(weak)["findings"]}

length={"product_mode":"ARC_FINAL","item_count":10,"items":[dict(x) for x in good["items"]]}
length["items"][1]["correct_option"]=5
length["items"][1]["option_lengths_chars"]=[20,21,19,22,40]
assert "CORRECT_OPTION_LENGTH_BIAS" in {x["code"] for x in mod.analyze(length)["findings"]}

fake={"product_mode":"ARC_FINAL","item_count":10,"items":[dict(x) for x in good["items"]]}
fake["items"][7]["reasoning_steps"]=1
assert "FAKE_D4" in {x["code"] for x in mod.analyze(fake)["findings"]}

easy={"product_mode":"ARC_FINAL","item_count":10,"items":[item(i+1,"D2") for i in range(10)]}
codes={x["code"] for x in mod.analyze(easy)["findings"]}
assert "FINAL_TOO_EASY_DISTRIBUTION" in codes
assert "FINAL_HIGH_DIFFICULTY_FLOOR_MISSED" in codes
print("ARC FINAL QUALITY GATE SMOKE: PASS")

# --- SCI final anchor (school ensemble + provisional offset) ---
import yaml
sci_anchor = yaml.safe_load((ROOT / "quality/anchors/SCI_DONGBUK_MULTI_EXAM_DIFFICULTY_ANCHOR_V1.0.yaml").read_text(encoding="utf-8"))
assert sci_anchor["mode"] == "MULTI_EXAM_ENSEMBLE" and sci_anchor["source_exam_count"] == 4
assert abs(sci_anchor["profile"]["mean_level"] - (sci_anchor["school_baseline"]["mean_level"] + sci_anchor["final_offset"]["center"])) < 1e-9
assert abs(sum(sci_anchor["profile"]["shares"].values()) - 1.0) < 1e-9

def sci_set(counts):
    seq = [d for d in ("D1", "D2", "D3", "D4", "D5") for _ in range(counts.get(d, 0))]
    return {"product_mode": "ARC_FINAL", "item_count": len(seq), "difficulty_anchor_required": True,
            "difficulty_anchor": sci_anchor, "items": [item(i + 1, d) for i, d in enumerate(seq)]}

ANCHOR_CODES = {"FINAL_SCHOOL_ANCHOR_EASIER", "FINAL_SCHOOL_ANCHOR_HARDER", "FINAL_SCHOOL_ANCHOR_SHARE_OFF"}
on_target = mod.analyze(sci_set({"D1": 1, "D2": 9, "D3": 9, "D4": 5}))
assert not ANCHOR_CODES & {x["code"] for x in on_target["findings"]}, on_target["findings"]
school_level = mod.analyze(sci_set({"D1": 3, "D2": 10, "D3": 8, "D4": 3}))  # mean 2.46: at or below the school's own average
assert "FINAL_SCHOOL_ANCHOR_EASIER" in {x["code"] for x in school_level["findings"]}
too_hard = mod.analyze(sci_set({"D2": 4, "D3": 8, "D4": 8, "D5": 4}))
assert "FINAL_SCHOOL_ANCHOR_HARDER" in {x["code"] for x in too_hard["findings"]}
print("SCI anchor gate checks OK")

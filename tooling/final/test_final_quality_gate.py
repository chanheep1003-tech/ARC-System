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

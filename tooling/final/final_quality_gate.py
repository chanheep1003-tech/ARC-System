#!/usr/bin/env python3
"""Deterministic ARC FINAL difficulty / item-quality profile gate."""
from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path
from typing import Any

import yaml

DIFFICULTIES = {"D1", "D2", "D3", "D4", "D5"}
TIME_CLASSES = {"SHORT", "STANDARD", "LONG"}


def load_payload(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    data = json.loads(text) if path.suffix.lower() == ".json" else yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError("FINAL quality profile must be a mapping")
    return data


def fail(code: str, message: str, item_id: str | None = None) -> dict[str, Any]:
    out: dict[str, Any] = {"severity": "FAIL", "code": code, "message": message}
    if item_id:
        out["item_id"] = item_id
    return out


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    if str(data.get("product_mode", "")).upper() != "ARC_FINAL":
        findings.append(fail("PRODUCT_MODE_INVALID", "product_mode must be ARC_FINAL"))

    items = data.get("items")
    item_count = data.get("item_count")
    if not isinstance(items, list) or not isinstance(item_count, int) or item_count != len(items):
        findings.append(fail("ITEM_COUNT_MISMATCH", "item_count must equal len(items)"))
        items = items if isinstance(items, list) else []
        item_count = len(items)

    difficulty_counts = {level: 0 for level in sorted(DIFFICULTIES)}
    longest_key = 0
    long_run = 0
    max_long_run = 0

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            findings.append(fail("ITEM_INVALID", "each item must be a mapping"))
            continue
        item_id = str(item.get("item_id", "")).strip() or f"ITEM-{index}"
        difficulty = str(item.get("actual_difficulty", "")).upper()
        if difficulty not in DIFFICULTIES:
            findings.append(fail("DIFFICULTY_INVALID", "actual_difficulty must be D1-D5", item_id))
        else:
            difficulty_counts[difficulty] += 1

        strong = item.get("strong_distractor_count")
        effective = item.get("effective_choice_count")
        plausible = item.get("first_pass_plausible_candidates")
        reasoning = item.get("reasoning_steps")
        immediate = item.get("immediate_elimination_count")
        evidence_count = item.get("evidence_count", 1)

        for field, value in (
            ("strong_distractor_count", strong),
            ("effective_choice_count", effective),
            ("first_pass_plausible_candidates", plausible),
            ("reasoning_steps", reasoning),
            ("immediate_elimination_count", immediate),
            ("evidence_count", evidence_count),
        ):
            if not isinstance(value, int) or value < 0:
                findings.append(fail("METRIC_INVALID", f"{field} must be non-negative int", item_id))

        if difficulty in {"D3", "D4", "D5"}:
            if isinstance(strong, int) and strong < 2:
                findings.append(fail("WEAK_DISTRACTOR_HARD_FAIL", "D3+ requires >=2 strong distractors", item_id))
            if isinstance(plausible, int) and plausible < 3:
                findings.append(fail("OBVIOUS_KEY_HARD_FAIL", "D3+ requires >=3 first-pass plausible candidates", item_id))
        if difficulty in {"D4", "D5"} and isinstance(effective, int) and effective < 4:
            findings.append(fail("EFFECTIVE_CHOICE_COUNT_LOW", "D4/D5 requires effective_choice_count >=4", item_id))
        if difficulty == "D4" and isinstance(reasoning, int) and reasoning < 2:
            findings.append(fail("FAKE_D4", "D4 requires at least two reasoning steps", item_id))
        if difficulty == "D5":
            if isinstance(reasoning, int) and reasoning < 3:
                findings.append(fail("FAKE_D5", "D5 requires at least three reasoning steps", item_id))
            if isinstance(evidence_count, int) and evidence_count < 2:
                findings.append(fail("D5_EVIDENCE_SHORT", "D5 requires evidence_count >=2", item_id))
            if isinstance(immediate, int) and immediate > 1:
                findings.append(fail("D5_TOO_MANY_IMMEDIATE_ELIMINATIONS", "D5 requires <=1 immediate elimination", item_id))

        second_best = int(item.get("second_best_option", 0) or 0)
        correct = int(item.get("correct_option", 0) or 0)
        if second_best not in range(1, 6) or correct not in range(1, 6) or second_best == correct:
            findings.append(fail("SECOND_BEST_INVALID", "correct/second_best must be distinct options 1-5", item_id))
        if not str(item.get("second_best_refutation", "")).strip():
            findings.append(fail("SECOND_BEST_REFUTATION_MISSING", "second_best_refutation is required", item_id))

        lengths = item.get("option_lengths_chars")
        if not isinstance(lengths, list) or len(lengths) != 5 or not all(isinstance(v, int) and v > 0 for v in lengths):
            findings.append(fail("OPTION_LENGTHS_INVALID", "option_lengths_chars must be five positive ints", item_id))
        elif correct in range(1, 6):
            c_len = lengths[correct - 1]
            maximum = max(lengths)
            median = float(statistics.median(lengths))
            unique_longest = c_len == maximum and lengths.count(maximum) == 1
            if unique_longest:
                longest_key += 1
            ratio = c_len / median if median else 999.0
            justified = item.get("length_justified") is True
            detail_outlier = item.get("correct_detail_outlier") is True
            if unique_longest and ratio >= 1.25 and not justified:
                findings.append(fail("CORRECT_OPTION_LENGTH_BIAS", f"unique longest correct option ratio={ratio:.2f}", item_id))
            if detail_outlier and not justified:
                findings.append(fail("CORRECT_DETAIL_OUTLIER", "correct option is uniquely more detailed without structural need", item_id))

        school_relative = str(item.get("school_relative", "")).upper()
        if school_relative == "BELOW_SCHOOL":
            findings.append(fail("BELOW_SCHOOL_FINAL_ITEM", "FINAL may not include unjustified BELOW_SCHOOL items", item_id))

        time_class = str(item.get("expected_time_class", "")).upper()
        if time_class not in TIME_CLASSES:
            findings.append(fail("EXPECTED_TIME_CLASS_INVALID", "expected_time_class must be SHORT/STANDARD/LONG", item_id))
        if time_class == "LONG":
            long_run += 1
            max_long_run = max(max_long_run, long_run)
        else:
            long_run = 0

    n = max(1, item_count)
    d12 = difficulty_counts["D1"] + difficulty_counts["D2"]
    d45 = difficulty_counts["D4"] + difficulty_counts["D5"]
    d12_rate = d12 / n
    d45_rate = d45 / n
    longest_rate = longest_key / n

    anchor = data.get("difficulty_anchor")
    mean_level = sum(int(k[1]) * v for k, v in difficulty_counts.items()) / n
    anchor_view = None
    if item_count >= 10 and isinstance(anchor, dict):
        # SCHOOL_ANCHOR mode: the set must match the school's real exam, neither easier nor harder.
        prof, tol = anchor["profile"], anchor["tolerance"]
        d3_rate = difficulty_counts["D3"] / n
        for name, got in (("D12", d12_rate), ("D3", d3_rate), ("D45", d45_rate)):
            want = float(prof["shares"][name])
            if abs(got - want) > float(tol["share"]):
                code = "FINAL_SCHOOL_ANCHOR_EASIER" if (name == "D45" and got < want) or (name == "D12" and got > want) else "FINAL_SCHOOL_ANCHOR_SHARE_OFF"
                findings.append(fail(code, f"{name} share {got:.2f} vs anchor {want:.2f} (±{float(tol['share']):.2f})"))
        if abs(mean_level - float(prof["mean_level"])) > float(tol["mean_level"]):
            code = "FINAL_SCHOOL_ANCHOR_EASIER" if mean_level < float(prof["mean_level"]) else "FINAL_SCHOOL_ANCHOR_HARDER"
            findings.append(fail(code, f"mean level {mean_level:.2f} vs anchor {float(prof['mean_level']):.2f} (±{float(tol['mean_level']):.2f})"))
        if longest_rate > 0.30:
            findings.append(fail("LONGEST_OPTION_IS_KEY_RATE", f"rate {longest_rate:.2f} exceeds 0.30"))
        late_start = math.floor(item_count * 0.70)
        late_d4_plus = sum(1 for item in items[late_start:] if isinstance(item, dict) and str(item.get("actual_difficulty", "")).upper() in {"D4", "D5"})
        late_required = int(tol.get("late_section_d45_min", 1))
        if late_d4_plus < late_required:
            findings.append(fail("LATE_SECTION_DISCRIMINATION_SHORT", f"late D4+ {late_d4_plus} < {late_required}"))
        anchor_view = {"anchor_id": anchor.get("anchor_id"), "anchor_shares": prof["shares"], "anchor_mean_level": prof["mean_level"],
                       "D3_RATE": round(d3_rate, 4), "MEAN_LEVEL": round(mean_level, 2)}
    elif item_count >= 10:
        if d12_rate > 0.25:
            findings.append(fail("FINAL_TOO_EASY_DISTRIBUTION", f"D1+D2 rate {d12_rate:.2f} exceeds 0.25"))
        if d45_rate < 0.30:
            findings.append(fail("FINAL_HIGH_DIFFICULTY_FLOOR_MISSED", f"D4+D5 rate {d45_rate:.2f} below 0.30"))
        if longest_rate > 0.30:
            findings.append(fail("LONGEST_OPTION_IS_KEY_RATE", f"rate {longest_rate:.2f} exceeds 0.30"))

        late_start = math.floor(item_count * 0.70)
        late_items = items[late_start:]
        late_d4_plus = sum(1 for item in late_items if isinstance(item, dict) and str(item.get("actual_difficulty", "")).upper() in {"D4", "D5"})
        late_required = 2 if item_count >= 20 else 1
        if late_d4_plus < late_required:
            findings.append(fail("LATE_SECTION_DISCRIMINATION_SHORT", f"late D4+ {late_d4_plus} < {late_required}"))
    else:
        late_d4_plus = None

    if max_long_run >= 3:
        findings.append(fail("TIME_PRESSURE_LONG_RUN", "three or more LONG items are consecutive"))

    status = "FAIL" if findings else "PASS"
    return {
        "tool": "ARC_FINAL_QUALITY_GATE_V1.0_EXEC",
        "status": status,
        "item_count": item_count,
        "fail_count": len(findings),
        "difficulty_profile": {
            **difficulty_counts,
            "D1_D2_RATE": round(d12_rate, 4),
            "D4_D5_RATE": round(d45_rate, 4),
            "LATE_SECTION_D4_PLUS": late_d4_plus,
            "MODE": "SCHOOL_ANCHOR" if anchor_view else "FIXED_PROFILE",
            **({"SCHOOL_ANCHOR": anchor_view} if anchor_view else {}),
        },
        "item_quality_profile": {
            "LONGEST_OPTION_IS_KEY_RATE": round(longest_rate, 4),
            "MAX_CONSECUTIVE_LONG_ITEMS": max_long_run,
        },
        "FINAL_DIFFICULTY": "PASS" if not any(f["code"] in {"FINAL_SCHOOL_ANCHOR_EASIER", "FINAL_SCHOOL_ANCHOR_HARDER", "FINAL_SCHOOL_ANCHOR_SHARE_OFF", "FINAL_TOO_EASY_DISTRIBUTION", "FINAL_HIGH_DIFFICULTY_FLOOR_MISSED", "LATE_SECTION_DISCRIMINATION_SHORT", "FAKE_D4", "FAKE_D5", "D5_EVIDENCE_SHORT"} for f in findings) else "FAIL",
        "FINAL_ITEM_QUALITY": "PASS" if not any(f["code"] in {"WEAK_DISTRACTOR_HARD_FAIL", "OBVIOUS_KEY_HARD_FAIL", "EFFECTIVE_CHOICE_COUNT_LOW", "CORRECT_OPTION_LENGTH_BIAS", "CORRECT_DETAIL_OUTLIER", "LONGEST_OPTION_IS_KEY_RATE", "SECOND_BEST_INVALID", "SECOND_BEST_REFUTATION_MISSING"} for f in findings) else "FAIL",
        "FINAL_RELEASE": "PASS" if status == "PASS" else "BLOCKED",
        "findings": findings,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("profile", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    result = analyze(load_payload(args.profile))
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

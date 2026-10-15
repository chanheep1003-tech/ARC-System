#!/usr/bin/env python3
"""Allowlisted ARC PDF preflight auto-fix planner and loop guard.

Only layout-profile values owned by Typesetter may be changed automatically.
Answer, item-count, source fidelity, broken-glyph and unknown defects return to
the owning stage or HOLD instead of mutating locked content.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


AUTO_ACTIONS = {
    "CORE_TWO_COLUMN_FLOW": "FORCE_CORE_ONE_COLUMN",
    "CORE_BODY_FONT_TOO_SMALL": "RESTORE_CORE_BODY_9_9PT",
    "CORE_LIGHT_BODY_FONT": "RESTORE_BODY_WEIGHT_400",
    "CORE_SPARSE_PAGE_REFLOW": "REFLOW_WITHIN_MAJOR_SECTION",
    "HEADING_ORPHAN_CANDIDATE": "KEEP_HEADING_WITH_FOLLOWING_BODY",
    "ARC_N_COVER_VERSO_NOT_BLANK": "REBUILD_COVER_VERSO_BLANK",
    "ARC_N_SEPARATOR_NOT_BLANK": "REBUILD_ANSWER_SEPARATOR_BLANK",
    "UNEXPECTED_PAGE_SIZE": "RESTORE_A4_PAGE_SIZE",
    "TEXT_IN_MARGIN": "REFLOW_TO_SAFE_MARGIN",
    "TEXT_TEXT_OVERLAP": "REFLOW_OVERLAPPING_BLOCKS",
}
CONTENT_RETURN_CODES = {
    "ARC_N_ANSWER_KEY_MISSING",
    "ARC_N_QUESTION_COUNT_MISMATCH",
    "ARC_N_ANSWER_COUNT_MISMATCH",
    "BROKEN_GLYPH_CANDIDATE",
    "RAW_MARKUP_LEAK",
    "STUDENT_METADATA_LEAK",
}
N_ONLY_CODES = {code for code in (set(AUTO_ACTIONS) | CONTENT_RETURN_CODES) if code.startswith("ARC_N_")}


def collect_findings(report: dict[str, Any]) -> list[dict[str, Any]]:
    return [flag for page in report.get("pages", []) for flag in page.get("flags", []) if flag.get("severity") in {"FAIL", "WARN"}]


def fingerprint(report: dict[str, Any]) -> str:
    tokens = []
    for page in report.get("pages", []):
        for flag in page.get("flags", []):
            if flag.get("severity") in {"FAIL", "WARN"}:
                tokens.append(f"{page.get('page')}:{flag.get('type')}:{flag.get('severity')}")
    return hashlib.sha256("|".join(sorted(tokens)).encode("utf-8")).hexdigest()


def build_plan(report: dict[str, Any], product: str, attempt: int = 0, previous_fingerprint: str | None = None, max_attempts: int = 2) -> dict[str, Any]:
    findings = collect_findings(report)
    current_fingerprint = fingerprint(report)
    codes = sorted({str(flag.get("type", "")) for flag in findings})
    if not findings:
        return {"decision": "PASS", "actions": [], "fingerprint": current_fingerprint, "attempt": attempt}
    if attempt >= max_attempts or (previous_fingerprint and previous_fingerprint == current_fingerprint):
        return {"decision": "HOLD", "reason": "AUTO_FIX_NO_PROGRESS", "actions": [], "fingerprint": current_fingerprint, "attempt": attempt}
    if product != "ARC_N" and any(code in N_ONLY_CODES for code in codes):
        return {"decision": "HOLD", "reason": "PRODUCT_RULE_LEAK", "actions": [], "fingerprint": current_fingerprint, "attempt": attempt}
    content_codes = sorted(set(codes) & CONTENT_RETURN_CODES)
    if content_codes:
        return {"decision": "CONTENT_RETURN", "reason": "LOCKED_CONTENT_OR_COUNT_DEFECT", "codes": content_codes, "actions": [], "fingerprint": current_fingerprint, "attempt": attempt}
    unknown = sorted(code for code in codes if code not in AUTO_ACTIONS)
    if unknown:
        return {"decision": "HOLD", "reason": "UNALLOWLISTED_DEFECT", "codes": unknown, "actions": [], "fingerprint": current_fingerprint, "attempt": attempt}
    actions = sorted({AUTO_ACTIONS[code] for code in codes})
    return {"decision": "AUTO_FIX", "actions": actions, "fingerprint": current_fingerprint, "attempt": attempt}


def apply_profile_fixes(profile: dict[str, Any], plan: dict[str, Any]) -> dict[str, Any]:
    if plan.get("decision") != "AUTO_FIX":
        raise ValueError("only AUTO_FIX plans may mutate a Typesetter profile")
    fixed = dict(profile)
    for action in plan.get("actions", []):
        if action == "FORCE_CORE_ONE_COLUMN": fixed["columns"] = 1
        elif action == "RESTORE_CORE_BODY_9_9PT": fixed["body_size"] = 9.9
        elif action == "RESTORE_BODY_WEIGHT_400": fixed["body_weight"] = 400
        elif action == "REFLOW_WITHIN_MAJOR_SECTION": fixed["semantic_reflow"] = True
        elif action == "KEEP_HEADING_WITH_FOLLOWING_BODY": fixed["keep_heading_with_body"] = True
        elif action == "REBUILD_COVER_VERSO_BLANK": fixed["cover_verso_blank"] = True
        elif action == "REBUILD_ANSWER_SEPARATOR_BLANK": fixed["answer_separator_blank"] = True
        elif action == "RESTORE_A4_PAGE_SIZE": fixed["page_size"] = "A4"
        elif action == "REFLOW_TO_SAFE_MARGIN": fixed["safe_margin"] = True
        elif action == "REFLOW_OVERLAPPING_BLOCKS": fixed["avoid_overlap"] = True
    return fixed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--product", required=True, choices=["ARC_CORE", "ARC_N", "ARC_FINAL"])
    parser.add_argument("--attempt", type=int, default=0)
    parser.add_argument("--previous-fingerprint")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    result = build_plan(report, args.product, args.attempt, args.previous_fingerprint)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output: args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0 if result["decision"] in {"PASS", "AUTO_FIX"} else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate the 70/30 source mix and auditable original-item provenance.

This checks records, not the truth of the underlying exam or a student's answer.
Source content, scope and independent solving still require their own reviews.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

POLICY_VERSION = "ARC-SOURCE-MIX-V1.0"
PAST_MODES = {"SELECT_ORIGINAL", "PRESERVE_CORE", "VERIFIED_VARIANT"}
PAST_KINDS = {"SCHOOL_EXAM", "NATIONAL_MOCK", "KICE_EXAM", "CSAT"}
# Per-subject profiles (user decision 2026-11-08, quality/ARC_GENERATION_SOURCE_POLICY_V1.0.md section 10).
PROFILES = {"PAST_70_AI_30", "STRUCTURE_REFERENCE_ONLY"}
COMPOSITION_MODES = {None, "ORIGINAL_TRIAL"}


def targets(count: int) -> tuple[int, int]:
    if type(count) is not int or count < 1:
        raise ValueError("item_count must be a positive integer")
    past = (count * 7 + 5) // 10  # nearest integer; half goes to past exams
    return past, count - past


def item_rows(bundle: dict[str, Any]) -> list[Any]:
    # Production's sets describe shared works; questions live in flat items.
    if isinstance(bundle.get("items"), list):
        return bundle["items"]
    if isinstance(bundle.get("sets"), list):
        return [it for group in bundle["sets"] if isinstance(group, dict)
                for it in (group.get("items") if isinstance(group.get("items"), list) else [])]
    return []


def analyze(bundle: dict[str, Any]) -> dict[str, Any]:
    rows = item_rows(bundle)
    findings = []
    def fail(code: str, message: str, iid: str | None = None, severity: str = "FAIL"):
        row = {"severity": severity, "code": code, "message": message}
        if iid is not None:
            row["item_id"] = iid
        findings.append(row)

    meta = bundle.get("source_composition")
    if not isinstance(meta, dict) or meta.get("policy_version") != POLICY_VERSION:
        fail("SOURCE_POLICY_MISSING", f"source_composition.policy_version must be {POLICY_VERSION}")
    meta_d = meta if isinstance(meta, dict) else {}
    profile = meta_d.get("profile", "PAST_70_AI_30")
    comp_mode = meta_d.get("mode")
    if profile not in PROFILES:
        fail("SOURCE_PROFILE_INVALID", f"source_composition.profile must be one of {sorted(PROFILES)}")
        profile = "PAST_70_AI_30"
    if comp_mode not in COMPOSITION_MODES:
        fail("SOURCE_COMPOSITION_MODE_INVALID", "source_composition.mode may only be ORIGINAL_TRIAL when present")
    if comp_mode == "ORIGINAL_TRIAL":
        for field in ("authorized_by", "shortage_reason"):
            if not isinstance(meta_d.get(field), str) or not meta_d[field].strip():
                fail("ORIGINAL_TRIAL_UNAUTHORIZED", f"ORIGINAL_TRIAL requires an explicit source_composition.{field}")
    if "profile" not in meta_d and str(bundle.get("subject", "")).upper() == "KOR":
        fail("SOURCE_PROFILE_UNDECLARED", "KOR bundles should declare profile STRUCTURE_REFERENCE_ONLY", severity="WARN")
    no_past = profile == "STRUCTURE_REFERENCE_ONLY" or comp_mode == "ORIGINAL_TRIAL"
    count = len(rows)
    if not count:
        fail("SOURCE_ITEMS_EMPTY", "Source mix requires at least one item")
    declared = bundle.get("item_count", count)
    if type(declared) is not int or declared != count:
        fail("SOURCE_ITEM_COUNT_MISMATCH", "Declared count must include every MCQ and constructed-response item")
    seen = set()
    families = set()
    past = creative = 0
    for it in rows:
        if not isinstance(it, dict):
            fail("SOURCE_ITEM_INVALID", "Every item must be a mapping")
            continue
        iid = str(it.get("item_id", "")).strip()
        if not iid or iid in seen:
            fail("SOURCE_ITEM_ID_INVALID", "Item IDs must be nonempty and unique", iid)
        seen.add(iid)
        p = it.get("provenance")
        if not isinstance(p, dict):
            fail("SOURCE_PROVENANCE_MISSING", "Every item requires provenance", iid)
            continue
        mode = p.get("mode")
        if mode in PAST_MODES:
            past += 1
            if no_past:
                fail("PAST_ITEM_NOT_ALLOWED", "This profile/mode allows only AI_ORIGINAL items (no past-exam items)", iid)
            if p.get("source_kind") not in PAST_KINDS:
                fail("NOT_ACTUAL_PAST_EXAM", "Publisher exercises, official samples and prior AI items are not actual past exams", iid)
            for field in ("source_id", "source_item_number", "source_locator", "source_answer_ref", "origin_family_id", "core_preserved"):
                if not isinstance(p.get(field), str) or not p[field].strip():
                    fail("SOURCE_REFERENCE_MISSING", f"provenance.{field} is required", iid)
            if p.get("source_review_status") != "CONTENT_VERIFIED":
                fail("SOURCE_UNVERIFIED", "Keyword matches and header-only checks cannot certify an original item", iid)
            if mode != "SELECT_ORIGINAL" and not p.get("modification_log"):
                fail("SOURCE_CHANGE_LOG_MISSING", "Edited/variant items require a modification log", iid)
            fam = str(p.get("origin_family_id", "")).strip()
            if fam and fam in families:
                fail("ORIGINAL_FAMILY_REPEATED", "Numeric or wording variants of the same original cannot inflate set diversity", iid)
            families.add(fam)
        elif mode == "AI_ORIGINAL":
            creative += 1
            refs = p.get("school_scope_refs")
            if not isinstance(refs, list) or not refs or not all(isinstance(ref, str) and ref.strip() for ref in refs):
                fail("CREATIVE_SCOPE_EVIDENCE_MISSING", "Creative items require current school/textbook scope references", iid)
            if not isinstance(p.get("design_purpose"), str) or not p["design_purpose"].strip():
                fail("CREATIVE_PURPOSE_MISSING", "Creative item must record what current-scope task it evaluates", iid)
        else:
            fail("SOURCE_MODE_INVALID", "Use an original/edited/variant past exam or AI_ORIGINAL", iid)
    expected = ((0, count) if no_past else targets(count)) if count else (0, 0)
    if (past, creative) != expected:
        fail("SOURCE_MIX_MISMATCH", f"Expected past/creative {expected[0]}/{expected[1]}, got {past}/{creative}")
    failed = any(f["severity"] == "FAIL" for f in findings)
    return {"tool": POLICY_VERSION, "status": "FAIL" if failed else "PASS",
            "profile": profile, "composition_mode": comp_mode or "STANDARD",
            "meets_70_30": (not no_past) and not failed,
            "item_count": count, "past_exam_count": past, "ai_original_count": creative,
            "target_past_exam_count": expected[0], "target_ai_original_count": expected[1],
            "findings": findings, "semantic_source_truth_verified_by_runner": False}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = yaml.safe_load(args.bundle.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("bundle must be a mapping")
    result = analyze(data)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

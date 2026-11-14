#!/usr/bin/env python3
"""Deterministic completeness gate for ARC independent-solve QA evidence.

This runner cannot decide whether a literary interpretation or factual claim is
true. It makes the evidence-producing review auditable and blocks CONTENT_LOCK
when the required blind solve, option map, source trace, or difficulty evidence
is absent or internally inconsistent.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
SUBJECTS = {"KOR", "ENG", "SOC", "SCI", "HIS", "AI"}
VERDICTS = {"TRUE", "FALSE", "HALF_TRUE", "UNSUPPORTED"}
COMPETITIVENESS = {"STRONG", "MEDIUM", "WEAK", "CORRECT"}
DIFFICULTIES = {"D1", "D2", "D3", "D4", "D5"}
CONFIDENCE_LEVELS = {"HIGH", "MEDIUM", "LOW"}
SECOND_BEST_RISKS = {"HIGH", "MEDIUM", "LOW", "NONE"}
REQUIRED_EXCLUDED_INPUTS = {"ANSWER_KEY", "PASS_A", "AUTHOR_INTENT", "TARGET_DIFFICULTY"}
ITEM_GATES = {
    "FACTUAL_ACCURACY_REVIEW",
    "OPTION_SEMANTIC_DUPLICATION_REVIEW",
    "ANSWER_EVIDENCE_TRACE",
    "SCOPE_EVIDENCE_TRACE",
    "ALL_OPTION_AUDIT",
    "UNIQUE_ANSWER",
    "DIFFICULTY_MATCH",
}
SET_GATES = {
    "STRUCTURE",
    "ANSWER_COUNT_MATCH",
    "MANUSCRIPT_CONTAMINATION",
    "TOO_EASY",
    "MID_GAP",
    "STRUCTURE_BIAS",
    "D4_SHORT",
    "PASSAGE_TRUNCATION",
}
KOR_ALLOWED_ORIGINS = {
    "USER_UPLOAD",
    "USER_PROVIDED_SCHOOL_SUPPLEMENT",
    "USER_PROVIDED_TEXTBOOK",
    "CONNECTED_DRIVE_RAW_SCHOOL_SOURCE",
}
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def load_payload(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    data = json.loads(text) if path.suffix.lower() == ".json" else yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError("QA evidence root must be a mapping")
    return data


def finding(code: str, message: str, item_id: str | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"severity": "FAIL", "code": code, "message": message}
    if item_id:
        result["item_id"] = item_id
    return result


def nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0 and all(str(v).strip() for v in value)


def gate_failures(gates: Any, required: set[str], prefix: str, item_id: str | None = None) -> list[dict[str, Any]]:
    if not isinstance(gates, dict):
        return [finding(f"{prefix}_GATES_MISSING", f"{prefix} gates must be a mapping", item_id)]
    failures = []
    for name in sorted(required):
        if str(gates.get(name, "")).upper() != "PASS":
            failures.append(finding(f"{prefix}_{name}_NOT_PASS", f"{name} must equal PASS", item_id))
    return failures


def analyze_item(item: Any, item_format: str, subject: str = "") -> list[dict[str, Any]]:
    if not isinstance(item, dict):
        return [finding("ITEM_NOT_MAPPING", "Each item must be a mapping")]
    item_id = str(item.get("item_id", "")).strip() or "<missing>"
    findings: list[dict[str, Any]] = []
    pass_a = item.get("pass_a")
    pass_b = item.get("pass_b")
    if not isinstance(pass_a, dict) or not isinstance(pass_b, dict):
        return [finding("PASS_AB_MISSING", "pass_a and pass_b mappings are required", item_id)]

    answer_a = str(pass_a.get("answer", "")).strip()
    answer_b = str(pass_b.get("answer", "")).strip()
    if not answer_a or answer_a != answer_b:
        findings.append(finding("ANSWER_AB_MISMATCH", "PASS A and blind PASS B answers must match", item_id))
    if not nonempty_list(pass_a.get("answer_evidence")):
        findings.append(finding("PASS_A_EVIDENCE_MISSING", "PASS A answer_evidence is required", item_id))

    if pass_b.get("blind") is not True:
        findings.append(finding("PASS_B_NOT_BLIND", "PASS B must declare blind=true", item_id))
    excluded = {str(v).upper() for v in pass_b.get("excluded_inputs", []) if str(v).strip()}
    if not REQUIRED_EXCLUDED_INPUTS <= excluded:
        missing = sorted(REQUIRED_EXCLUDED_INPUTS - excluded)
        findings.append(finding("BLIND_INPUT_LEAK", f"PASS B excluded_inputs missing: {missing}", item_id))
    if not nonempty_list(pass_b.get("answer_evidence")):
        findings.append(finding("ANSWER_EVIDENCE_MISSING", "PASS B answer_evidence is required", item_id))
    if str(pass_b.get("confidence", "")).upper() not in CONFIDENCE_LEVELS:
        findings.append(finding("CONFIDENCE_INVALID", "PASS B confidence must be HIGH/MEDIUM/LOW", item_id))
    if not isinstance(pass_b.get("transfer_required"), bool):
        findings.append(finding("TRANSFER_FLAG_INVALID", "transfer_required must be boolean", item_id))

    scope = pass_b.get("scope_trace")
    if not isinstance(scope, dict) or str(scope.get("status", "")).upper() != "IN_SCOPE":
        findings.append(finding("SCOPE_TRACE_INVALID", "scope_trace.status must equal IN_SCOPE", item_id))
    elif not nonempty_list(scope.get("source_refs")):
        findings.append(finding("SCOPE_SOURCE_REFS_MISSING", "scope_trace.source_refs is required", item_id))

    option_judgments = pass_b.get("option_judgments")
    if item_format == "MCQ5" and (not isinstance(option_judgments, list) or len(option_judgments) != 5):
        findings.append(finding("OPTION_JUDGMENT_COUNT", "MCQ5 requires exactly five option judgments", item_id))
        option_judgments = option_judgments if isinstance(option_judgments, list) else []

    polarity = str(item.get("stem_polarity", "")).upper()
    if polarity not in {"POSITIVE", "NEGATIVE"} and subject == "KOR":
        findings.append(finding("STEM_POLARITY_MISSING", "KOR normative items require explicit POSITIVE/NEGATIVE polarity", item_id))
    if not polarity:
        polarity = "POSITIVE"  # legacy fixtures remain compatible; Korean reviewer must specify polarity
    if polarity not in {"POSITIVE", "NEGATIVE"}:
        findings.append(finding("STEM_POLARITY_INVALID", "stem_polarity must be POSITIVE/NEGATIVE", item_id))
    option_ids: list[str] = []
    true_ids: list[str] = []
    false_ids: list[str] = []
    uncertain_ids: list[str] = []
    semantic_keys: list[str] = []
    strong_distractors = 0
    for option in option_judgments or []:
        if not isinstance(option, dict):
            findings.append(finding("OPTION_JUDGMENT_INVALID", "Every option judgment must be a mapping", item_id))
            continue
        option_id = str(option.get("option_id", "")).strip()
        verdict = str(option.get("verdict", "")).upper()
        axis = str(option.get("axis", "")).strip().casefold()
        claim_key = str(option.get("claim_key", "")).strip().casefold()
        competitiveness = str(option.get("competitiveness", "")).upper()
        option_ids.append(option_id)
        if verdict == "TRUE":
            true_ids.append(option_id)
        elif verdict == "FALSE":
            false_ids.append(option_id)
        elif verdict in {"HALF_TRUE", "UNSUPPORTED"}:
            uncertain_ids.append(option_id)
        if verdict not in VERDICTS:
            findings.append(finding("OPTION_VERDICT_INVALID", f"Invalid verdict for option {option_id}", item_id))
        if competitiveness not in COMPETITIVENESS:
            findings.append(finding("OPTION_COMPETITIVENESS_INVALID", f"Invalid competitiveness for option {option_id}", item_id))
        elif option_id != answer_b and competitiveness == "STRONG":
            strong_distractors += 1
        if not axis or not claim_key:
            findings.append(finding("OPTION_SEMANTIC_KEY_MISSING", f"axis and claim_key required for option {option_id}", item_id))
        else:
            semantic_keys.append(f"{axis}::{claim_key}")
        if not nonempty_list(option.get("evidence_refs")):
            findings.append(finding("OPTION_EVIDENCE_MISSING", f"evidence_refs required for option {option_id}", item_id))

    if len(option_ids) != len(set(option_ids)):
        findings.append(finding("OPTION_ID_DUPLICATE", "Option IDs must be unique", item_id))
    if polarity == "NEGATIVE":
        if len(false_ids) != 1 or false_ids[0] != answer_b or len(true_ids) != 4:
            findings.append(finding("UNIQUE_ANSWER_INVALID", "Negative stem requires exactly one FALSE answer and four TRUE choices", item_id))
    elif len(true_ids) != 1 or (true_ids and true_ids[0] != answer_b):
        findings.append(finding("UNIQUE_ANSWER_INVALID", "Positive stem requires exactly one TRUE answer", item_id))
    if subject == "KOR" and uncertain_ids:
        findings.append(finding("KOR_OPTION_UNSUPPORTED", "KOR normative release cannot contain HALF_TRUE/UNSUPPORTED judgments", item_id))
    if len(semantic_keys) != len(set(semantic_keys)):
        findings.append(finding("OPTION_SEMANTIC_DUPLICATION", "Duplicate AXIS + CLAIM_KEY detected", item_id))

    second_best = str(pass_b.get("second_best_option", "")).strip()
    if not second_best or second_best == answer_b or second_best not in option_ids:
        findings.append(finding("SECOND_BEST_INVALID", "second_best_option must be a non-answer option", item_id))
    if str(pass_b.get("second_best_risk", "")).upper() not in SECOND_BEST_RISKS:
        findings.append(finding("SECOND_BEST_RISK_INVALID", "second_best_risk must be HIGH/MEDIUM/LOW/NONE", item_id))

    target = str(item.get("target_difficulty", "")).upper()
    actual = str(pass_b.get("actual_difficulty", "")).upper()
    if target not in DIFFICULTIES or actual not in DIFFICULTIES:
        findings.append(finding("DIFFICULTY_INVALID", "target and actual difficulty must be D1-D5", item_id))
    elif target != actual:
        findings.append(finding("DIFFICULTY_MISMATCH", f"target {target} != actual {actual}", item_id))

    reasoning_steps = pass_b.get("reasoning_steps")
    evidence_count = pass_b.get("evidence_count")
    immediate = pass_b.get("immediate_elimination_count")
    for field, value in (("reasoning_steps", reasoning_steps), ("evidence_count", evidence_count), ("immediate_elimination_count", immediate)):
        if not isinstance(value, int) or value < 0:
            findings.append(finding("DIFFICULTY_METRIC_INVALID", f"{field} must be a non-negative integer", item_id))

    if actual == "D3" and isinstance(reasoning_steps, int) and isinstance(immediate, int):
        if reasoning_steps < 1 or strong_distractors < 1 or immediate > 2:
            findings.append(finding("D3_SHORT", "D3 requires >=1 step, >=1 strong distractor, and <=2 immediate eliminations", item_id))
    if actual == "D4" and isinstance(reasoning_steps, int) and isinstance(immediate, int):
        if reasoning_steps < 2 or strong_distractors < 2 or immediate > 2:
            findings.append(finding("D4_SHORT", "D4 requires >=2 steps, >=2 strong distractors, and <=2 immediate eliminations", item_id))
    if actual == "D5" and all(isinstance(v, int) for v in (reasoning_steps, evidence_count, immediate)):
        if reasoning_steps < 3 or strong_distractors < 2 or evidence_count < 2 or immediate > 1:
            findings.append(finding("D5_MINIMUM_FAIL", "D5 minimum reasoning/evidence/distractor gate failed", item_id))

    findings.extend(gate_failures(item.get("gates"), ITEM_GATES, "ITEM", item_id))
    return findings


def analyze_korean_source_locks(data: dict[str, Any], item_ids: set[str]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if data.get("uses_source_text") is not True:
        return findings
    locks = data.get("source_text_locks")
    if not isinstance(locks, list) or not locks:
        return [finding("KOR_SOURCE_LOCK_MISSING", "Korean source text requires source_text_locks")]
    for lock in locks:
        if not isinstance(lock, dict):
            findings.append(finding("KOR_SOURCE_LOCK_INVALID", "Each source lock must be a mapping"))
            continue
        source_id = str(lock.get("source_text_id", "<missing>"))
        if str(lock.get("source_origin", "")).upper() not in KOR_ALLOWED_ORIGINS:
            findings.append(finding("KOR_SOURCE_ORIGIN_FORBIDDEN", f"Forbidden source origin for {source_id}"))
        if str(lock.get("source_role", "")).upper() != "RAW_SCHOOL_SOURCE":
            findings.append(finding("KOR_SOURCE_ROLE_INVALID", f"{source_id} must use RAW_SCHOOL_SOURCE"))
        if str(lock.get("text_fidelity", "")).upper() != "EXACT":
            findings.append(finding("KOR_SOURCE_NOT_EXACT", f"{source_id} must use TEXT_FIDELITY=EXACT"))
        if not str(lock.get("source_file_id", "")).strip() or not str(lock.get("source_location", "")).strip():
            findings.append(finding("KOR_SOURCE_PROVENANCE_INCOMPLETE", f"{source_id} requires file ID and location"))
        if not SHA256_RE.fullmatch(str(lock.get("source_text_sha256", ""))):
            findings.append(finding("KOR_SOURCE_CHECKSUM_INVALID", f"{source_id} requires a SHA-256 checksum"))
        linked = lock.get("linked_item_ids")
        if not nonempty_list(linked) or not set(map(str, linked)) <= item_ids:
            findings.append(finding("KOR_SOURCE_LINKAGE_INVALID", f"{source_id} requires valid linked_item_ids"))
        for field in ("wording_lock", "punctuation_lock", "line_break_lock", "boundary_lock"):
            if lock.get(field) is not True:
                findings.append(finding("KOR_SOURCE_BOUNDARY_UNLOCKED", f"{source_id}.{field} must be true"))
    return findings


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    subject = str(data.get("subject", "")).upper()
    item_format = str(data.get("item_format", "")).upper()
    items = data.get("items")
    item_count = data.get("item_count")

    if data.get("schema_version") != "ARC-QA-EVIDENCE-V1.0":
        findings.append(finding("SCHEMA_VERSION_INVALID", "schema_version must be ARC-QA-EVIDENCE-V1.0"))
    if subject not in SUBJECTS:
        findings.append(finding("SUBJECT_INVALID", "subject must be KOR/SOC/HIS/SCI/AI"))
    if item_format != "MCQ5":
        findings.append(finding("ITEM_FORMAT_UNSUPPORTED", "V1.0 executable gate supports MCQ5"))
    if not isinstance(items, list) or not isinstance(item_count, int) or item_count != len(items):
        findings.append(finding("ITEM_COUNT_MISMATCH", "item_count must equal the number of items"))
        items = items if isinstance(items, list) else []

    item_ids = [str(item.get("item_id", "")).strip() for item in items if isinstance(item, dict)]
    if any(not item_id for item_id in item_ids) or len(item_ids) != len(set(item_ids)):
        findings.append(finding("ITEM_ID_INVALID", "Every item_id must be non-empty and unique"))
    for item in items:
        findings.extend(analyze_item(item, item_format, subject))

    findings.extend(gate_failures(data.get("set_gates"), SET_GATES, "SET"))
    if subject == "KOR":
        findings.extend(analyze_korean_source_locks(data, set(item_ids)))
    if data.get("content_lock") is not True:
        findings.append(finding("CONTENT_LOCK_NOT_REQUESTED", "Final QA evidence must request content_lock=true"))

    status = "FAIL" if findings else "PASS"
    return {
        "tool": "ARC_CONTENT_QA_GATE_V1.0",
        "status": status,
        "subject": subject or None,
        "item_count": len(items),
        "fail_count": len(findings),
        "content_lock_allowed": status == "PASS",
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = analyze(load_payload(args.evidence))
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())

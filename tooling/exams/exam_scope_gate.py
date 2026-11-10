#!/usr/bin/env python3
"""Exam-scoped admission. Pending ranges and stale profiles fail closed.

This checks registered provenance and scope membership, not semantic truth.
Archived replay is an explicit test route and never authorizes release.
"""
from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
SUBJECTS = {"KOR", "SOC", "SCI", "HIS", "AI"}
PRODUCTS = {"ARC_CORE", "ARC_N", "ARC_FINAL"}


class ExamContextError(ValueError):
    pass


def digest(profile: dict) -> str:
    def encode(value):
        if isinstance(value, date):
            return value.isoformat()
        raise TypeError(f"Unsupported exam profile value: {type(value).__name__}")
    return hashlib.sha256(json.dumps(profile, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":"), default=encode).encode()).hexdigest()


def subject_code(value: Any) -> str:
    code = str(value).strip().upper().replace("-", "_")
    return {"KOREAN": "KOR", "SOCIAL": "SOC", "SCIENCE": "SCI", "HISTORY": "HIS",
            "SCI_REDOX": "SCI", "SCIENCE_REDOX": "SCI", "REDOX": "SCI"}.get(code, code)


def repo_file(root: Path, rel: Any) -> Path:
    if not isinstance(rel, str) or not rel or Path(rel).is_absolute():
        raise ExamContextError("EXAM_REGISTRY_PATH_INVALID")
    path = (root / rel).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ExamContextError("EXAM_REGISTRY_PATH_INVALID")
    return path


def load_registry(manifest_path: Path) -> tuple[dict, dict]:
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ExamContextError("EXAM_MANIFEST_INVALID")
    path = repo_file(manifest_path.parent, manifest.get("runtime", {}).get("exam_context_registry"))
    registry = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(registry, dict) or registry.get("schema_version") != "ARC-EXAM-CONTEXT-V1":
        raise ExamContextError("EXAM_REGISTRY_INVALID")
    if not isinstance(registry.get("exams"), dict):
        raise ExamContextError("EXAM_REGISTRY_INVALID")
    return manifest, registry


def identifiers(value: Any) -> set[str] | None:
    if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
        return None
    if len(set(value)) != len(value):
        return None
    return set(value)


def actual_source_ids(bundle: dict) -> set[str]:
    result = set()
    sets = bundle.get("sets", [])
    if isinstance(sets, list):
        for st in sets:
            if isinstance(st, dict):
                for work in st.get("works", []):
                    if isinstance(work, dict) and work.get("source_text_id"):
                        result.add(str(work["source_text_id"]))
    passages = bundle.get("passages", [])
    if isinstance(passages, list):
        result.update(str(p["source_text_id"]) for p in passages
                      if isinstance(p, dict) and p.get("source_text_id"))
    return result


def analyze(bundle: dict, manifest: dict, registry: dict, *, root: Path = ROOT,
            archived_replay: bool = False) -> dict:
    findings = []

    def fail(code: str, message: str):
        findings.append({"severity": "FAIL", "code": code, "message": message})

    context = bundle.get("exam_context")
    active_id = manifest.get("runtime", {}).get("active_exam_id")
    if archived_replay:
        # Callers must opt in. A current exam may not be relabelled a replay.
        if isinstance(context, dict) and context.get("exam_id") == active_id:
            fail("ACTIVE_EXAM_REPLAY_FORBIDDEN", "Current exam cannot use archived replay.")
        elif context and (not isinstance(context, dict) or not isinstance(context.get("exam_id"), str) or
                          registry.get("exams", {}).get(context.get("exam_id"), {}).get("status") != "ARCHIVED"):
            fail("ARCHIVED_EXAM_UNKNOWN", "Replay context must name an archived exam.")
        return {"status": "FAIL" if findings else "ARCHIVED_REPLAY", "exam_id": None,
                "release_allowed": False, "findings": findings, "anchor_path": None}

    if not isinstance(context, dict):
        fail("EXAM_CONTEXT_MISSING", "Explicit exam_context is required; midterm scope is never inherited.")
        return {"status": "FAIL", "exam_id": None, "release_allowed": False,
                "findings": findings, "anchor_path": None}
    exam_id = context.get("exam_id")
    if not isinstance(exam_id, str) or not exam_id:
        fail("EXAM_ID_MISSING", "exam_id is required.")
    if exam_id != active_id:
        fail("EXAM_ID_NOT_ACTIVE", "Bundle must target the active exam.")
    profile = registry.get("exams", {}).get(exam_id) if isinstance(exam_id, str) else None
    if not isinstance(profile, dict):
        fail("EXAM_NOT_REGISTERED", "Exam profile must exist in the registry.")
        return {"status": "FAIL", "exam_id": exam_id, "release_allowed": False,
                "findings": findings, "anchor_path": None}
    if profile.get("status") not in {"PREPARING", "ACTIVE"}:
        fail("ARCHIVED_EXAM_RELEASE_FORBIDDEN", "Archived exams are not current production inputs.")
    if profile.get("inherit_midterm_scope") is not False:
        fail("MIDTERM_SCOPE_INHERITANCE_FORBIDDEN", "Profiles must explicitly disable midterm inheritance.")
    if context.get("profile_sha256") != digest(profile):
        fail("EXAM_PROFILE_STALE", "Bundle must bind the current profile content hash.")
    subject = subject_code(bundle.get("subject", ""))
    subject_entries = profile.get("subjects")
    entry = subject_entries.get(subject) if isinstance(subject_entries, dict) else None
    if subject not in SUBJECTS or not isinstance(entry, dict):
        fail("EXAM_SUBJECT_NOT_REGISTERED", "Subject has no exam-specific configuration.")
        return {"status": "FAIL", "exam_id": exam_id, "release_allowed": False,
                "findings": findings, "anchor_path": None}
    if "active_subjects" in profile:
        active_subjects = identifiers(profile["active_subjects"])
        if not active_subjects or not active_subjects <= SUBJECTS:
            fail("EXAM_ACTIVE_SUBJECTS_INVALID", "Exam must specify a valid nonempty subject selection.")
        elif subject not in active_subjects:
            fail("EXAM_SUBJECT_NOT_ACTIVE", "Subject is excluded from this exam preparation cycle.")
    product = bundle.get("product_mode")
    enabled_products = identifiers(entry.get("products"))
    if not isinstance(product, str) or product not in PRODUCTS or not enabled_products or product not in enabled_products:
        fail("EXAM_PRODUCT_NOT_ACTIVE", "Product is not enabled for this exam subject.")
    scope_state = entry.get("scope_status")
    if scope_state not in {"CONFIRMED", "CONFIRMED_UNITS_ONLY"}:
        if scope_state == "PROVISIONAL_REMAINDER":
            fail("EXAM_SCOPE_PROVISIONAL", "Course minus actual midterm is the collection scope; publication needs verified scope IDs and evidence.")
        else:
            fail("EXAM_SCOPE_PENDING", "Scope is pending; collect sources before production.")
    if product == "ARC_FINAL" and scope_state != "CONFIRMED":
        fail("FINAL_SCOPE_NOT_CONFIRMED", "FINAL requires the confirmed full exam range.")
    if not identifiers(entry.get("scope_evidence_refs")):
        fail("EXAM_SCOPE_EVIDENCE_MISSING", "Scope confirmation needs explicit evidence references.")
    units = identifiers(context.get("unit_ids"))
    sources = identifiers(context.get("source_ids"))
    allowed_units = identifiers(entry.get("unit_ids"))
    allowed_sources = identifiers(entry.get("source_ids"))
    excluded_units = identifiers(entry.get("excluded_unit_ids", []))
    excluded_sources = identifiers(entry.get("excluded_source_ids", []))
    if not units or not allowed_units or excluded_units is None:
        fail("EXAM_UNIT_IDS_INVALID", "Nonempty, unique unit IDs are required.")
    elif not units <= allowed_units or units & excluded_units:
        fail("EXAM_UNIT_OUT_OF_SCOPE", "Bundle includes an unconfirmed or excluded unit.")
    if not sources or not allowed_sources or excluded_sources is None:
        fail("EXAM_SOURCE_IDS_INVALID", "Nonempty, unique source IDs are required.")
    elif not sources <= allowed_sources or sources & excluded_sources:
        fail("EXAM_SOURCE_OUT_OF_SCOPE", "Bundle includes an unconfirmed or excluded source.")
    actual = actual_source_ids(bundle)
    if actual and sources != actual:
        fail("EXAM_SOURCE_BINDING_MISMATCH", "Declared sources must equal sources used in passages/sets.")
    anchor_path = None
    if product == "ARC_FINAL":
        anchor = entry.get("difficulty_anchor")
        if not isinstance(anchor, dict):
            fail("FINAL_EXAM_ANCHOR_MISSING", "FINAL needs an exam-specific subject/unit anchor.")
        else:
            anchor_units = identifiers(anchor.get("unit_ids"))
            if subject_code(anchor.get("subject")) != subject or not units or not anchor_units or not units <= anchor_units:
                fail("FINAL_ANCHOR_UNIT_MISMATCH", "An anchor cannot calibrate unrelated units.")
            try:
                path = repo_file(root, anchor.get("path"))
                if not re.fullmatch(r"[0-9a-f]{64}", str(anchor.get("sha256", ""))) or hashlib.sha256(path.read_bytes()).hexdigest() != anchor.get("sha256"):
                    fail("FINAL_ANCHOR_CHECKSUM_MISMATCH", "Anchor file must match its registered hash.")
                else:
                    data = yaml.safe_load(path.read_text(encoding="utf-8"))
                    if not isinstance(data, dict) or subject_code(data.get("subject")) != subject:
                        fail("FINAL_ANCHOR_SUBJECT_MISMATCH", "Anchor payload must match the subject.")
                    else:
                        anchor_path = str(path)
            except (ExamContextError, OSError, yaml.YAMLError):
                fail("FINAL_ANCHOR_PATH_INVALID", "Anchor must be a readable file inside the repository.")
    return {"status": "FAIL" if findings else "PASS", "exam_id": exam_id,
            "profile_sha256": digest(profile), "release_allowed": not findings,
            "findings": findings, "anchor_path": anchor_path}


def check_bundle(bundle: dict, manifest_path: Path = ROOT / "SYSTEM_MANIFEST.yaml", *, archived_replay=False) -> dict:
    try:
        manifest, registry = load_registry(manifest_path)
        return analyze(bundle, manifest, registry, root=manifest_path.parent, archived_replay=archived_replay)
    except (ExamContextError, OSError, yaml.YAMLError) as exc:
        return {"status": "FAIL", "release_allowed": False, "anchor_path": None,
                "findings": [{"severity": "FAIL", "code": "EXAM_CONFIGURATION_INVALID", "message": str(exc)}]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--manifest", type=Path, default=ROOT / "SYSTEM_MANIFEST.yaml")
    parser.add_argument("--archived-replay", action="store_true", help="Test-only replay; never release eligible")
    args = parser.parse_args()
    payload = yaml.safe_load(args.bundle.read_text(encoding="utf-8"))
    result = check_bundle(payload if isinstance(payload, dict) else {}, args.manifest, archived_replay=args.archived_replay)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(result["status"] == "FAIL")


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate collection metadata and distinguish discovery from usable sources."""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import yaml

ROLES = {"PAST_EXAM", "RAW_SCHOOL_SOURCE", "OFFICIAL_GUIDE", "OFFICIAL_REFERENCE", "PRACTICE_REFERENCE", "GENERATED_PRACTICE", "UNCLASSIFIED"}
REVIEWS = {"METADATA_ONLY", "HEADER_REVIEWED", "LINK_REVIEWED", "CONTENT_REVIEWED"}


def canonical_url(url: str) -> str:
    parts = urlsplit(url)
    query = sorted((k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
                   if not k.startswith("utm_") and k not in {"usp", "gclid"})
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path, urlencode(query), ""))


def analyze(ledger: dict) -> dict:
    findings = []
    sources = ledger.get("sources") if isinstance(ledger, dict) else None
    if not isinstance(sources, list):
        return {"status": "FAIL", "findings": [{"code": "COLLECTION_SOURCES_INVALID", "severity": "FAIL"}]}
    ids = set()
    collection_scope = ledger.get("collection_scope", {})
    active_subjects = None
    if isinstance(collection_scope, dict) and "active_subjects" in collection_scope:
        selected = collection_scope["active_subjects"]
        if (not isinstance(selected, list) or not selected or
            any(not isinstance(code, str) or code not in {"KOR", "ENG", "SOC", "SCI", "HIS", "AI"} for code in selected) or
            len(set(selected)) != len(selected)):
            findings.append({"code": "COLLECTION_ACTIVE_SUBJECTS_INVALID", "severity": "FAIL"})
            active_subjects = set()
        else:
            active_subjects = set(selected)
    identities, possible = defaultdict(list), defaultdict(list)
    eligible = []
    for row in sources:
        if not isinstance(row, dict):
            findings.append({"code": "COLLECTION_ENTRY_INVALID", "severity": "FAIL"})
            continue
        sid = row.get("source_id")
        row_failure_start = len(findings)

        def fail(code):
            findings.append({"code": code, "severity": "FAIL", "source_id": sid})

        if not isinstance(sid, str) or not sid or sid in ids:
            fail("COLLECTION_ID_INVALID_OR_DUPLICATE")
        if isinstance(sid, str):
            ids.add(sid)
        for key in ["title", "provider", "collected_at", "reviewed_at", "curriculum", "exam_scope_status"]:
            if not isinstance(row.get(key), str) or not row[key].strip():
                fail("COLLECTION_METADATA_MISSING_" + key.upper())
        url = row.get("url")
        if not isinstance(url, str) or urlsplit(url).scheme != "https" or not urlsplit(url).netloc:
            fail("COLLECTION_URL_INVALID")
        else:
            identity = "drive:" + row["drive_file_id"] if row.get("drive_file_id") else canonical_url(url)
            identities[identity].append(sid)
        if row.get("role") not in ROLES:
            fail("COLLECTION_ROLE_INVALID")
        if row.get("review_status") not in REVIEWS:
            fail("COLLECTION_REVIEW_STATUS_INVALID")
        flag = row.get("eligible_for_current_exam")
        if not isinstance(flag, bool):
            fail("COLLECTION_ELIGIBILITY_FLAG_INVALID")
        if flag is True:
            if active_subjects is not None and row.get("subject") not in active_subjects:
                fail("COLLECTION_SUBJECT_NOT_ACTIVE")
            if row.get("collection_action") == "PARKED_BY_USER":
                fail("COLLECTION_PARKED_SOURCE_PROMOTION")
            refs = row.get("scope_evidence_refs")
            if row.get("exam_scope_status") != "CONFIRMED" or not isinstance(refs, list) or not refs or any(not isinstance(x, str) or not x.strip() for x in refs):
                fail("COLLECTION_UNCONFIRMED_PROMOTION")
            if row.get("review_status") != "CONTENT_REVIEWED":
                fail("COLLECTION_UNREVIEWED_PROMOTION")
            if row.get("curriculum") != "2022_REVISED":
                fail("COLLECTION_CURRICULUM_UNCONFIRMED")
            if row.get("role") != "RAW_SCHOOL_SOURCE":
                fail("COLLECTION_REFERENCE_AS_SCHOOL_SOURCE")
            units = row.get("unit_ids")
            if not isinstance(units, list) or not units or any(not isinstance(x, str) or not x.strip() for x in units) or row.get("subject") not in {"KOR", "ENG", "SOC", "SCI", "HIS", "AI"}:
                fail("COLLECTION_SCOPE_BINDING_MISSING")
            if not re.fullmatch(r"[0-9a-f]{64}", str(row.get("sha256", ""))) or not isinstance(row.get("content_verification_ref"), str) or not row["content_verification_ref"].strip():
                fail("COLLECTION_SOURCE_INTEGRITY_MISSING")
            if len(findings) == row_failure_start:
                eligible.append(sid)
        title = str(row.get("title", "")).strip()
        if row.get("size_bytes") is not None:
            possible[(title, row["size_bytes"])].append(sid)
    duplicates = [values for values in identities.values() if len(values) > 1]
    for values in duplicates:
        findings.append({"severity": "FAIL", "code": "COLLECTION_IDENTITY_DUPLICATE", "sources": values})
    return {"status": "FAIL" if findings else "PASS", "source_count": len(sources),
            "eligible_for_current_exam_count": len(eligible), "findings": findings,
            "possible_duplicates_not_content_verified": [v for v in possible.values() if len(v) > 1]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("ledger", type=Path)
    args = parser.parse_args()
    result = analyze(yaml.safe_load(args.ledger.read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(result["status"] == "FAIL")


if __name__ == "__main__":
    raise SystemExit(main())

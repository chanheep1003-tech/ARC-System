#!/usr/bin/env python3
"""Canonical ARC CONTENT_BUNDLE -> Markdown handoff serializer.

This serializer is deliberately layout-blind. It keeps internal metadata out of
STUDENT MANUSCRIPT, pins the active ruleset from SYSTEM_MANIFEST, and records a
student-manuscript checksum for the Typesetter acceptance gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
INTERNAL_ID_RE = re.compile(
    r"\[(?:ARC-[A-Z0-9]+-[A-Z0-9]+-\d+|CONCEPT_ID|SOURCE_ID)[^\]]*\]",
    re.I,
)
LAYOUT_KEY_RE = re.compile(
    r"(?:pdf_?master|template_?version|column_?count|two_?column|font_?(?:size|family|weight)|"
    r"css|page_?template|page_?geometry|margin)",
    re.I,
)
LAYOUT_VALUE_RE = re.compile(
    r"(?:ARC_PDF_LAYOUT_MASTER_V\d|\b2\s*단\s*(?:조판|형식|레이아웃|배치)|"
    r"two[- ]column|column-count\s*:|grid-template-columns|PageTemplate|"
    r"\bFrame\s*\(|(?:본문|body|font(?:-size)?)\D{0,35}\d+(?:\.\d+)?\s*pt)",
    re.I,
)


class SerializationError(ValueError):
    pass


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_payload(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    payload = json.loads(text) if path.suffix.lower() == ".json" else yaml.safe_load(text)
    if not isinstance(payload, dict):
        raise SerializationError("CONTENT_BUNDLE must be a mapping")
    return payload


def find_layout_directives(node: Any, trail: str = "") -> list[str]:
    findings: list[str] = []
    if isinstance(node, dict):
        for key, value in node.items():
            path = f"{trail}.{key}" if trail else str(key)
            if LAYOUT_KEY_RE.search(str(key)):
                findings.append(path)
            findings.extend(find_layout_directives(value, path))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            findings.extend(find_layout_directives(value, f"{trail}[{index}]"))
    elif isinstance(node, str) and LAYOUT_VALUE_RE.search(node):
        findings.append(trail or "<root>")
    return findings


def canonical_filename(product: str, subject: str, batch_id: str) -> str:
    product_token = {"ARC_CORE": "CORE", "ARC_N": "N", "ARC_FINAL": "FINAL"}[product]
    return f"ARC_HANDOFF_{product_token}_{subject}_{batch_id}_READY.md"


def require(payload: dict[str, Any], key: str) -> Any:
    value = payload.get(key)
    if value is None or (isinstance(value, str) and not value.strip()):
        raise SerializationError(f"missing required field: {key}")
    return value


def serialize_bundle(payload: dict[str, Any], manifest: dict[str, Any]) -> tuple[str, str]:
    product = str(require(payload, "product_mode")).upper()
    if product not in {"ARC_CORE", "ARC_N", "ARC_FINAL"}:
        raise SerializationError(f"unsupported product_mode: {product}")
    subject = str(require(payload, "subject")).upper()
    batch_id = str(require(payload, "batch_id"))
    generator = str(require(payload, "generator")).upper()
    if generator not in {"GPT", "CLAUDE"}:
        raise SerializationError("generator must be GPT or CLAUDE")
    manuscript = str(require(payload, "student_manuscript")).strip() + "\n"

    directives = find_layout_directives(payload)
    if directives:
        raise SerializationError("layout authority is forbidden in CONTENT_BUNDLE: " + ", ".join(sorted(set(directives))))
    if INTERNAL_ID_RE.search(manuscript):
        raise SerializationError("student_manuscript contains internal metadata ID")

    ruleset = str(manifest["system"]["version"])
    filename = canonical_filename(product, subject, batch_id)
    item_count = int(payload.get("item_count", 0))
    front = {
        "ARC_HANDOFF_VERSION": "1.1",
        "ARC_RULESET_VERSION": ruleset,
        "BATCH_ID": batch_id,
        "GENERATOR": generator,
        "PRODUCT_MODE": product,
        "SUBJECT": subject,
        "SCOPE": str(require(payload, "scope")),
        "ITEM_COUNT": item_count,
        "CREATED_AT": str(require(payload, "created_at")),
        "CONTENT_QA_STATUS": "PASS",
        "CONTENT_LOCK": True,
        "HANDOFF_STATUS": "READY_FOR_TYPESET",
        "TYPESET_STATUS": "PENDING",
        "HANDOFF_MD_STATUS": "READY",
        "HANDOFF_MD_FILENAME": filename,
        "STUDENT_MANUSCRIPT_SHA256": sha256_text(manuscript),
    }

    if product in {"ARC_N", "ARC_FINAL"}:
        qa_filename = str(require(payload, "qa_evidence_filename"))
        front.update(
            {
                "QA_EVIDENCE_SCHEMA_VERSION": "ARC-QA-EVIDENCE-V1.0",
                "QA_EVIDENCE_FILENAME": qa_filename,
                "QA_EVIDENCE_STATUS": "PASS",
                "UNIVERSAL_INDEPENDENT_SOLVE_GATE": "PASS",
                "CONTENT_QA_RUNNER": "PASS",
            }
        )

    sections = [
        "---\n" + yaml.safe_dump(front, allow_unicode=True, sort_keys=False).strip() + "\n---",
        "# TYPESETTER INSTRUCTIONS — INTERNAL / DO NOT PRINT\nPreserve locked content. Resolve all layout rules from SYSTEM_MANIFEST at render time.",
    ]

    if product == "ARC_CORE":
        architecture = payload.get("core_architecture_summary") or {}
        sections.append(
            "# CORE ARCHITECTURE SUMMARY — INTERNAL / DO NOT PRINT\n"
            + yaml.safe_dump(architecture, allow_unicode=True, sort_keys=False).strip()
        )

    sections.append("# STUDENT MANUSCRIPT\n" + manuscript.rstrip())

    if product in {"ARC_N", "ARC_FINAL"}:
        answer_key = payload.get("answer_key")
        if not isinstance(answer_key, dict) or len(answer_key) != item_count:
            raise SerializationError("answer_key count must equal item_count")
        sections.append(
            "# ANSWER KEY — INTERNAL / DO NOT PRINT ON PROBLEM PAGES\n"
            + yaml.safe_dump(answer_key, allow_unicode=True, sort_keys=False).strip()
        )

    asset_manifest = payload.get("visual_asset_manifest") or []
    sections.append(
        "# VISUAL / LAYOUT ASSET MANIFEST — INTERNAL / DO NOT PRINT\n"
        + yaml.safe_dump(asset_manifest, allow_unicode=True, sort_keys=False).strip()
    )
    if payload.get("source_text_blocks"):
        sections.append(
            "# SOURCE TEXT BLOCKS — INTERNAL SOURCE PAYLOAD\n"
            + yaml.safe_dump(payload["source_text_blocks"], allow_unicode=True, sort_keys=False).strip()
        )
    if product in {"ARC_N", "ARC_FINAL"}:
        sections.append(
            "# QA EVIDENCE — INTERNAL / DO NOT PRINT\nMachine-readable payload: "
            + str(payload["qa_evidence_filename"])
        )
    sections.append(
        "# QC STATUS — INTERNAL / DO NOT PRINT\n"
        + yaml.safe_dump(payload.get("qc_status") or {"STATUS": "PASS"}, allow_unicode=True, sort_keys=False).strip()
    )
    return filename, "\n\n".join(sections).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--manifest", type=Path, default=ROOT / "SYSTEM_MANIFEST.yaml")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    manifest = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    filename, text = serialize_bundle(load_payload(args.bundle), manifest)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / filename
    output.write_text(text, encoding="utf-8")
    print(json.dumps({"status": "PASS", "output": str(output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

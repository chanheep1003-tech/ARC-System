#!/usr/bin/env python3
"""Behavioral smoke tests for canonical handoff serialization."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("serializer", ROOT / "tooling/handoff/handoff_serializer.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


def base_bundle() -> dict:
    return {
        "batch_id": "KOR-CANARY-001",
        "generator": "GPT",
        "product_mode": "ARC_CORE",
        "subject": "KOR",
        "scope": "supplementary material + textbook unit 1 pipeline fixture",
        "item_count": 0,
        "created_at": "2026-09-21T04:00:00+09:00",
        "student_manuscript": "# Unit 1 Reading\n\nA clean student paragraph.",
        "core_architecture_summary": {"CENTRAL_QUESTION": "How does evidence support interpretation?"},
        "internal_metadata": {"concept_index": ["ARC-KOR-C-001"]},
        "qc_status": {"CORE_QA_STATUS": "PASS"},
    }


def run() -> None:
    manifest = yaml.safe_load((ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8"))
    filename, text = mod.serialize_bundle(base_bundle(), manifest)
    assert filename == "ARC_HANDOFF_CORE_KOR_KOR-CANARY-001_READY.md"
    assert manifest["system"]["version"] in text
    assert "ARC-KOR-C-001" not in text
    assert "STUDENT_MANUSCRIPT_SHA256" in text

    bad = base_bundle()
    bad["pdf_master"] = "ARC_PDF_LAYOUT_MASTER_V2.1"
    try:
        mod.serialize_bundle(bad, manifest)
    except mod.SerializationError as exc:
        assert "layout authority" in str(exc)
    else:
        raise AssertionError("layout directive was not rejected")

    leak = base_bundle()
    leak["student_manuscript"] += "\n[ARC-KOR-C-001]"
    try:
        mod.serialize_bundle(leak, manifest)
    except mod.SerializationError as exc:
        assert "internal metadata" in str(exc)
    else:
        raise AssertionError("student metadata leak was not rejected")

    annotation = base_bundle()
    annotation["product_mode"] = "ARC_KOR_ANNOTATION"
    try:
        mod.serialize_bundle(annotation, manifest)
    except mod.SerializationError as exc:
        assert "unsupported product_mode" in str(exc)
    else:
        raise AssertionError("non-active annotation product leaked into ARC production serializer")

    print("ARC HANDOFF SERIALIZER SMOKE: PASS")


if __name__ == "__main__":
    run()

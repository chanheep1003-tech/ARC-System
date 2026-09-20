#!/usr/bin/env python3
"""Behavioral smoke tests for ARC Markdown handoff preflight."""
from __future__ import annotations

import importlib.util
import hashlib
import tempfile
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "arc_handoff_preflight", ROOT / "tooling/handoff/handoff_preflight.py"
)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


def codes(result: dict) -> set[str]:
    return {item["code"] for item in result["findings"]}


def handoff(version: str, instructions: str, manuscript: str, filename: str) -> str:
    checksum = hashlib.sha256((manuscript.strip() + "\n").encode("utf-8")).hexdigest()
    return f"""---
ARC_RULESET_VERSION: {version}
BATCH_ID: TEST-001
PRODUCT_MODE: ARC_CORE
SUBJECT: SOC
SCOPE: smoke fixture
ITEM_COUNT: 0
CREATED_AT: 2026-09-21T04:00:00+09:00
CONTENT_LOCK: true
CONTENT_QA_STATUS: PASS
HANDOFF_STATUS: READY_FOR_TYPESET
HANDOFF_MD_STATUS: READY
TYPESET_STATUS: PENDING
HANDOFF_MD_FILENAME: {filename}
STUDENT_MANUSCRIPT_SHA256: {checksum}
---

# TYPESETTER INSTRUCTIONS — INTERNAL / DO NOT PRINT
{instructions}

# STUDENT MANUSCRIPT
{manuscript}

# QC STATUS — INTERNAL / DO NOT PRINT
PASS
"""


def run() -> None:
    manifest = yaml.safe_load((ROOT / "SYSTEM_MANIFEST.yaml").read_text(encoding="utf-8"))
    version = manifest["system"]["version"]
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)

        good = td / "ARC_HANDOFF_CORE_SOC_TEST-001_READY.md"
        good.write_text(
            handoff(
                version,
                "Preserve the locked text. Resolve layout from SYSTEM_MANIFEST.",
                "# A파트 · 사회 정의\n\n본문입니다.\n\n# B파트 · 세계화\n\n본문입니다.",
                good.name,
            ),
            encoding="utf-8",
        )
        result = mod.analyze(good, ROOT / "SYSTEM_MANIFEST.yaml")
        assert result["status"] == "PASS", result
        assert result["major_boundaries"] == ["A파트 · 사회 정의", "B파트 · 세계화"]

        stale = td / "ARC_HANDOFF_CORE_SOC_TEST-STALE_READY.md"
        stale.write_text(
            handoff(
                "1.8.0-dev",
                "판형: A4 2단 조판. ARC_PDF_LAYOUT_MASTER_V2.1, 본문 8.8pt, column-count: 2.",
                "## A파트 · 사회 정의\n\n[ARC-SOC-C-001] 본문입니다.",
                stale.name,
            ),
            encoding="utf-8",
        )
        result = mod.analyze(stale, ROOT / "SYSTEM_MANIFEST.yaml")
        expected = {
            "STALE_RULESET",
            "CORE_TWO_COLUMN_DIRECTIVE",
            "PDF_MASTER_PIN_FORBIDDEN",
            "LAYOUT_CODE_FORBIDDEN",
            "FONT_SIZE_PIN_FORBIDDEN",
            "STUDENT_INTERNAL_ID_LEAK",
            "UNMARKED_MAJOR_BOUNDARY",
        }
        assert expected <= codes(result), result
        assert result["status"] == "FAIL", result

        student_layout_leak = td / "ARC_HANDOFF_CORE_SOC_TEST-LEAK_READY.md"
        student_layout_leak.write_text(
            handoff(
                version,
                "Preserve the locked text. Resolve layout from SYSTEM_MANIFEST.",
                "# A파트 · 사회 정의\n\n본문입니다.\n\nARC_PDF_LAYOUT_MASTER_V2.1로 2단 조판하고 body 8.8pt, column-count: 2로 출력한다.",
                student_layout_leak.name,
            ),
            encoding="utf-8",
        )
        result = mod.analyze(student_layout_leak, ROOT / "SYSTEM_MANIFEST.yaml")
        expected_student = {
            "CORE_TWO_COLUMN_DIRECTIVE",
            "PDF_MASTER_PIN_FORBIDDEN",
            "LAYOUT_CODE_FORBIDDEN",
            "FONT_SIZE_PIN_FORBIDDEN",
        }
        assert expected_student <= codes(result), result
        assert result["status"] == "FAIL", result

        qa_good = td / "ARC_HANDOFF_N_SOC_TEST-N-001_READY.md"
        qa_manuscript = "1. 문항입니다."
        qa_checksum = hashlib.sha256((qa_manuscript + "\n").encode("utf-8")).hexdigest()
        qa_good.write_text(
            f"""---
ARC_RULESET_VERSION: {version}
BATCH_ID: TEST-N-001
PRODUCT_MODE: ARC_N
SUBJECT: SOC
SCOPE: smoke fixture
ITEM_COUNT: 1
CREATED_AT: 2026-09-21T04:00:00+09:00
CONTENT_LOCK: true
CONTENT_QA_STATUS: PASS
HANDOFF_STATUS: READY_FOR_TYPESET
HANDOFF_MD_STATUS: READY
TYPESET_STATUS: PENDING
HANDOFF_MD_FILENAME: {qa_good.name}
STUDENT_MANUSCRIPT_SHA256: {qa_checksum}
QA_EVIDENCE_SCHEMA_VERSION: ARC-QA-EVIDENCE-V1.0
QA_EVIDENCE_FILENAME: ARC_QA_EVIDENCE_SOC_001.yaml
QA_EVIDENCE_STATUS: PASS
UNIVERSAL_INDEPENDENT_SOLVE_GATE: PASS
CONTENT_QA_RUNNER: PASS
---

# STUDENT MANUSCRIPT
{qa_manuscript}

# QA EVIDENCE — INTERNAL / DO NOT PRINT
Machine-readable payload: ARC_QA_EVIDENCE_SOC_001.yaml

# QC STATUS — INTERNAL / DO NOT PRINT
PASS
""",
            encoding="utf-8",
        )
        result = mod.analyze(qa_good, ROOT / "SYSTEM_MANIFEST.yaml")
        assert result["status"] == "PASS", result

        qa_missing = td / "ARC_HANDOFF_N_SOC_TEST-N-002_READY.md"
        missing_checksum = hashlib.sha256((qa_manuscript + "\n").encode("utf-8")).hexdigest()
        qa_missing.write_text(
            f"""---
ARC_RULESET_VERSION: {version}
BATCH_ID: TEST-N-002
PRODUCT_MODE: ARC_N
SUBJECT: SOC
SCOPE: smoke fixture
ITEM_COUNT: 1
CREATED_AT: 2026-09-21T04:00:00+09:00
CONTENT_LOCK: true
CONTENT_QA_STATUS: PASS
HANDOFF_STATUS: READY_FOR_TYPESET
HANDOFF_MD_STATUS: READY
TYPESET_STATUS: PENDING
HANDOFF_MD_FILENAME: {qa_missing.name}
STUDENT_MANUSCRIPT_SHA256: {missing_checksum}
---

# STUDENT MANUSCRIPT
{qa_manuscript}

# QC STATUS — INTERNAL / DO NOT PRINT
PASS
""",
            encoding="utf-8",
        )
        result = mod.analyze(qa_missing, ROOT / "SYSTEM_MANIFEST.yaml")
        assert {"CONTENT_QA_META_INVALID", "QA_EVIDENCE_FILENAME_MISSING", "QA_EVIDENCE_SECTION_MISSING"} <= codes(result), result
        assert result["status"] == "FAIL", result

        tampered = td / "ARC_HANDOFF_CORE_SOC_TEST-TAMPER_READY.md"
        tampered.write_text(
            handoff(
                version,
                "Preserve locked content.",
                "# A파트 · 사회 정의\n\n원본 본문입니다.",
                tampered.name,
            ).replace("원본 본문입니다.", "변조된 본문입니다."),
            encoding="utf-8",
        )
        result = mod.analyze(tampered, ROOT / "SYSTEM_MANIFEST.yaml")
        assert "STUDENT_MANUSCRIPT_CHECKSUM_MISMATCH" in codes(result), result

    print("ARC HANDOFF PREFLIGHT SMOKE: PASS")


if __name__ == "__main__":
    run()

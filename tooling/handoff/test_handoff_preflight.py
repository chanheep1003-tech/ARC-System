#!/usr/bin/env python3
"""Behavioral smoke tests for ARC Markdown handoff preflight."""
from __future__ import annotations

import importlib.util
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


def handoff(version: str, instructions: str, manuscript: str) -> str:
    return f"""---
ARC_RULESET_VERSION: {version}
PRODUCT_MODE: ARC_CORE
CONTENT_LOCK: true
CONTENT_QA_STATUS: PASS
HANDOFF_STATUS: READY_FOR_TYPESET
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

        good = td / "good.md"
        good.write_text(
            handoff(
                version,
                "Preserve the locked text. Resolve layout from SYSTEM_MANIFEST.",
                "# A파트 · 사회 정의\n\n본문입니다.\n\n# B파트 · 세계화\n\n본문입니다.",
            ),
            encoding="utf-8",
        )
        result = mod.analyze(good, ROOT / "SYSTEM_MANIFEST.yaml")
        assert result["status"] == "PASS", result
        assert result["major_boundaries"] == ["A파트 · 사회 정의", "B파트 · 세계화"]

        stale = td / "stale.md"
        stale.write_text(
            handoff(
                "1.8.0-dev",
                "판형: A4 2단 조판. ARC_PDF_LAYOUT_MASTER_V2.1, 본문 8.8pt, column-count: 2.",
                "## A파트 · 사회 정의\n\n[ARC-SOC-C-001] 본문입니다.",
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

    print("ARC HANDOFF PREFLIGHT SMOKE: PASS")


if __name__ == "__main__":
    run()

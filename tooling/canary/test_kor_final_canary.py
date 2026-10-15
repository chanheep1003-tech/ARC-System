#!/usr/bin/env python3
"""Behavioral smoke for fixed KOR ARC_FINAL canary."""
from __future__ import annotations
import importlib.util
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("kor_final_canary", ROOT / "tooling/canary/kor_final_canary.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)

with tempfile.TemporaryDirectory() as td:
    result = mod.run(ROOT / "quality/canary/KOR_FINAL_CANARY_V1.yaml", Path(td))
    assert result["status"] == "CANARY_PASS", result
    assert result["stages"]["final_quality_gate"] == "PASS", result
    assert result["final_quality"]["FINAL_RELEASE"] == "PASS", result
    assert result["typeset"]["page_count"] == 4, result
    assert result["typeset"]["question_count"] == 10, result
    assert result["typeset"]["answer_count"] == 10, result
    assert result["render_plan"]["product"] == "ARC_FINAL", result
    assert result["render_plan"]["profile"]["answer_key_mode"] == "SEPARATE_ARTIFACT_ONLY", result
    assert all(x["status"] == "BLOCKED" for x in result["fault_injection"]), result
print("ARC KOR FINAL CANARY: PASS")

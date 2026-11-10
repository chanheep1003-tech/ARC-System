#!/usr/bin/env python3
"""Behavioral smoke for allowlisted PDF auto-fix planning."""
from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("autofix", ROOT / "tooling/pdf_qc/autofix_controller.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


def report(*codes: str) -> dict:
    return {"pages": [{"page": 2, "flags": [{"severity": "FAIL", "type": code} for code in codes]}]}


plan = mod.build_plan(report("CORE_BODY_FONT_TOO_SMALL", "CORE_TWO_COLUMN_FLOW"), "ARC_CORE")
assert plan["decision"] == "AUTO_FIX", plan
fixed = mod.apply_profile_fixes({"body_size": 8.5, "columns": 2}, plan)
assert fixed["body_size"] == 9.9 and fixed["columns"] == 1, fixed

returned = mod.build_plan(report("ARC_N_ANSWER_COUNT_MISMATCH"), "ARC_N")
assert returned["decision"] == "CONTENT_RETURN", returned

leak = mod.build_plan(report("ARC_N_SEPARATOR_NOT_BLANK"), "ARC_FINAL")
assert leak["decision"] == "HOLD" and leak["reason"] == "PRODUCT_RULE_LEAK", leak

first = mod.build_plan(report("CORE_BODY_FONT_TOO_SMALL"), "ARC_CORE")
stuck = mod.build_plan(report("CORE_BODY_FONT_TOO_SMALL"), "ARC_CORE", attempt=1, previous_fingerprint=first["fingerprint"])
assert stuck["decision"] == "HOLD" and stuck["reason"] == "AUTO_FIX_NO_PROGRESS", stuck

print("ARC PDF AUTO-FIX CONTROLLER SMOKE: PASS")

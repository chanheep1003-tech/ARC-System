#!/usr/bin/env python3
"""Behavioral smoke for fixed 10-item KOR ARC_N canary."""
from __future__ import annotations
import importlib.util
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("kor_n_canary", ROOT / "tooling/canary/kor_n_canary.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)

with tempfile.TemporaryDirectory() as td:
    result = mod.run(ROOT / "quality/canary/KOR_N_CANARY_V1.yaml", Path(td))
    assert result["status"] == "CANARY_PASS", result
    assert result["typeset"] == {"status": "PASS", "page_count": 6, "question_count": 10, "answer_count": 10}
    assert result["render_plan"]["authority"] == "TYPESETTER_GATEWAY", result
    assert result["render_plan"]["profile"]["columns"] == 2, result
print("ARC KOR N CANARY: PASS")

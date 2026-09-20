#!/usr/bin/env python3
"""Behavioral smoke for the fixed KOR CORE nightly canary."""
from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("nightly_canary", ROOT / "tooling/canary/nightly_canary.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(mod)


def run() -> None:
    with tempfile.TemporaryDirectory() as td:
        result = mod.run(ROOT / "quality/canary/KOR_CORE_CANARY_V1.yaml", Path(td))
        assert result["status"] == "CANARY_PASS", result
        assert result["typeset"]["page_count"] == 4, result
        assert all(item["status"] == "BLOCKED" for item in result["fault_injection"]), result
    print("ARC KOR CORE NIGHTLY CANARY: PASS")


if __name__ == "__main__":
    run()

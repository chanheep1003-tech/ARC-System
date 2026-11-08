#!/usr/bin/env python3
"""SOC/SCI ARC_N must contain no D1 items (user rule 2026-11-08); other subjects are unaffected."""
from __future__ import annotations

import copy
import importlib.util
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
BUNDLE = ROOT / "quality/production/KOR_N04_KANTHEGEL_20260925"
spec = importlib.util.spec_from_file_location("arc_production_pipeline", ROOT / "tooling/production/production_pipeline.py")
pipeline = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(pipeline)


def run(tmp, name, subject, bump_d1):
    items = yaml.safe_load((BUNDLE / "items.yaml").read_text(encoding="utf-8"))
    blind = yaml.safe_load((BUNDLE / "blind_review.yaml").read_text(encoding="utf-8"))
    items = copy.deepcopy(items)
    items["subject"] = subject
    if bump_d1:  # replace every D1 by D2 (target) so the set has no D1 items
        for it in items["items"]:
            if it["difficulty"] == "D1":
                it["difficulty"] = "D2"
    work = tmp / name
    work.mkdir()
    (work / "items.yaml").write_text(yaml.safe_dump(items, allow_unicode=True, sort_keys=False), encoding="utf-8")
    (work / "blind_review.yaml").write_text(yaml.safe_dump(blind, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return {f["code"] for f in pipeline.run(work, work / "out", archived_replay=True)["findings"]}


def main():
    assert pipeline.PROFILES[("SOC", "ARC_N")] == {"D1": (0.0, 0.0)}
    assert pipeline.PROFILES[("SCI", "ARC_N")] == {"D1": (0.0, 0.0)}
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        for subject in ("SOC", "SCI"):
            assert "BALANCE_D1_OUT_OF_RANGE" in run(tmp, f"{subject}_d1", subject, False), subject
            assert "BALANCE_D1_OUT_OF_RANGE" not in run(tmp, f"{subject}_ok", subject, True), subject
    print("SOC/SCI no-D1 gate: PASS")


if __name__ == "__main__":
    main()

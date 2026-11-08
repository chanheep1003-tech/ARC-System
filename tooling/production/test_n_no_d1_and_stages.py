#!/usr/bin/env python3
"""KOR/SOC/SCI ARC_N must contain no D1 items (user rule 2026-11-08) and may declare a ladder stage."""
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


def run(tmp, name, subject, bump_d1, stage=None):
    items = yaml.safe_load((BUNDLE / "items.yaml").read_text(encoding="utf-8"))
    blind = yaml.safe_load((BUNDLE / "blind_review.yaml").read_text(encoding="utf-8"))
    items = copy.deepcopy(items)
    items["subject"] = subject
    if stage:
        items["stage"] = stage
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
    for subject in ("KOR", "SOC", "SCI"):
        assert pipeline.PROFILES[(subject, "ARC_N")]["D1"] == (0.0, 0.0), subject
    assert set(pipeline.STAGE_SHARES) == {"S1", "S2", "S3", "S4"}
    assert all(abs(sum(v.values()) - 1.0) < 1e-9 for v in pipeline.STAGE_SHARES.values())
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        for subject in ("KOR", "SOC", "SCI"):
            assert "BALANCE_D1_OUT_OF_RANGE" in run(tmp, f"{subject}_d1", subject, False), subject
            assert "BALANCE_D1_OUT_OF_RANGE" not in run(tmp, f"{subject}_ok", subject, True), subject
        # a declared stage keeps the D1 ban, drops the legacy KOR mix bounds and reports share drift as WARN
        c = run(tmp, "kor_stage_d1", "KOR", False, stage="S2")
        assert "BALANCE_D1_OUT_OF_RANGE" in c and "BALANCE_D45_OUT_OF_RANGE" not in c, c
        c = run(tmp, "kor_stage_s4", "KOR", True, stage="S4")  # D2 60% / D3 40% / D4+ 0%: far from S4's 0.10/0.35/0.55
        assert "BALANCE_D1_OUT_OF_RANGE" not in c and {"STAGE_D2_SHARE_OFF", "STAGE_D45_SHARE_OFF"} <= c, c
        c = run(tmp, "kor_stage_s1", "KOR", True, stage="S1")  # D2 60% / D3 40% / D4+ 0% is within S1's tolerance
        assert not {x for x in c if x.startswith("STAGE_")}, c
        assert "STAGE_INVALID" in run(tmp, "bad_stage", "KOR", True, stage="V5")
    print("N no-D1 + stage gate: PASS")


if __name__ == "__main__":
    main()

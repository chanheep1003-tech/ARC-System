#!/usr/bin/env python3
"""KOR/SOC/SCI ARC_N: no D1 items (user rule 2026-11-08); stage, item count and difficulty shares are decided by the user per request."""
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


def run(tmp, name, subject, bump_d1, spec=None, replay=True):
    items = yaml.safe_load((BUNDLE / "items.yaml").read_text(encoding="utf-8"))
    blind = yaml.safe_load((BUNDLE / "blind_review.yaml").read_text(encoding="utf-8"))
    items = copy.deepcopy(items)
    items["subject"] = subject
    if spec is not None:
        items["request_spec"] = spec
    if bump_d1:  # replace every D1 by D2 (target) so the set has no D1 items
        for it in items["items"]:
            if it["difficulty"] == "D1":
                it["difficulty"] = "D2"
    work = tmp / name
    work.mkdir()
    (work / "items.yaml").write_text(yaml.safe_dump(items, allow_unicode=True, sort_keys=False), encoding="utf-8")
    (work / "blind_review.yaml").write_text(yaml.safe_dump(blind, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return {f["code"] for f in pipeline.run(work, work / "out", archived_replay=replay)["findings"]}


def spec(**over):
    base = {"decided_by": "USER", "stage": "S2", "item_count": 10, "difficulty_targets": {"D2": 0.6, "D3": 0.4, "D45": 0.0}}
    base.update(over)
    return base


def main():
    for subject in ("KOR", "SOC", "SCI"):
        assert pipeline.PROFILES[(subject, "ARC_N")]["D1"] == (0.0, 0.0), subject
    assert not hasattr(pipeline, "STAGE_SHARES"), "no default stage shares may exist"
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        # D1 ban in every subject
        for subject in ("KOR", "SOC", "SCI"):
            assert "BALANCE_D1_OUT_OF_RANGE" in run(tmp, f"{subject}_d1", subject, False), subject
            assert "BALANCE_D1_OUT_OF_RANGE" not in run(tmp, f"{subject}_ok", subject, True), subject
        # no request_spec -> blocked before anything else, and the finding tells the operator to ask the user
        for subject in ("KOR", "SOC", "SCI"):
            c = run(tmp, f"{subject}_nospec", subject, True, replay=False)
            assert c == {"REQUEST_SPEC_MISSING"}, (subject, c)
        # incomplete / not user-decided specs
        assert "REQUEST_SPEC_NOT_USER_DECIDED" in run(tmp, "auto", "KOR", True, spec(decided_by="DEFAULT"), replay=False)
        assert "REQUEST_ITEM_COUNT_MISSING" in run(tmp, "nocount", "SOC", True, spec(item_count=None), replay=False)
        assert "REQUEST_ITEM_COUNT_MISMATCH" in run(tmp, "badcount", "SCI", True, spec(item_count=99), replay=False)
        assert "REQUEST_STAGE_INVALID" in run(tmp, "v5", "KOR", True, spec(stage="V5"), replay=False)
        assert "REQUEST_DIFFICULTY_MISSING" in run(tmp, "nodiff", "KOR", True, spec(difficulty_targets=None), replay=False)
        assert "REQUEST_DIFFICULTY_MISSING" in run(tmp, "d1key", "KOR", True,
                                                   spec(difficulty_targets={"D1": 0.1, "D2": 0.5, "D3": 0.4}), replay=False)
        assert "REQUEST_DIFFICULTY_SUM" in run(tmp, "sum", "KOR", True,
                                               spec(difficulty_targets={"D2": 0.6, "D3": 0.6, "D45": 0.0}), replay=False)
        # a complete user-decided spec passes the request gate (later gates may still run)
        c = run(tmp, "complete", "KOR", True, spec(), replay=False)
        assert not {x for x in c if x.startswith("REQUEST_")}, c
        # user-decided targets are enforced; the legacy KOR mix bounds are replaced
        c = run(tmp, "kor_far", "KOR", True, spec(difficulty_targets={"D2": 0.1, "D3": 0.35, "D45": 0.55}))
        assert {"REQUEST_DIFFICULTY_D2_OFF", "REQUEST_DIFFICULTY_D45_OFF"} <= c and "BALANCE_D45_OUT_OF_RANGE" not in c, c
        c = run(tmp, "kor_near", "KOR", True, spec())  # bundle is D2 60% / D3 40% / D4+ 0%
        assert not {x for x in c if x.startswith("REQUEST_DIFFICULTY")}, c
    print("N no-D1 + per-request spec gate: PASS")


if __name__ == "__main__":
    main()

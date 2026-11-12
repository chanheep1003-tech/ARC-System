#!/usr/bin/env python3
"""Archetype gate regression: the Dongbuk-style sample passes; the rejected flat set and injected faults fail."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("arc_archetype_gate", ROOT / "tooling/korean/archetype_gate.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
LIB = "quality/korean/ARC_KOR_GRAMMAR_ARCHETYPES_V1.0.yaml"


def load(name: str) -> dict:
    return yaml.safe_load((ROOT / "quality/production" / name / "items.yaml").read_text(encoding="utf-8"))


def codes(report: dict) -> set[str]:
    return {f["code"] for f in report["findings"]}


def main() -> int:
    sample = load("KOR_V6_DONGBUK_STYLE_SAMPLE_20261111")
    assert gate.analyze(sample)["status"] == "PASS"

    # Bundles that predate the library are not judged by it.
    flat = load("KOR_V6_ORTHO_A_20261111")
    assert gate.analyze(flat)["status"] == "NOT_APPLICABLE"
    # Once the library applies, the rejected flat set fails on exactly the user's complaint.
    flat["archetype_library"] = LIB
    assert {"ARCHETYPE_UNREGISTERED", "CONSTRUCTED_RATIO_LOW"} <= codes(gate.analyze(flat))

    def variant(mutate) -> set[str]:
        bundle = copy.deepcopy(sample)
        mutate(bundle)
        return codes(gate.analyze(bundle))

    assert "VIEW_MISSING" in variant(lambda b: b["items"][0].pop("view"))
    assert "TRAP_UNCLASSIFIED" in variant(lambda b: b["items"][0]["judgments"][0].pop("trap"))
    assert "D1_RECALL_FORBIDDEN" in variant(lambda b: b["items"][0].update(difficulty="D1"))
    assert "CR_CONDITIONS_SHORT" in variant(lambda b: b["items"][5].update(conditions=["1. 한 문장으로 쓸 것."]))
    assert "STUDENT_TEXT_SPOT_COUNT" in variant(lambda b: b["items"][1].update(view=[v.replace("㉥", "") for v in b["items"][1]["view"]]))
    assert "MASKED_SPACING" in variant(lambda b: b["items"][0].update(stem="다음 문장의 [만] 가운데 붙여 써야 하는 것은?"))
    assert "CONSTRUCTED_RATIO_LOW" in variant(lambda b: b["items"].pop())
    assert "SINGLE_WORD_OPTIONS" in variant(lambda b: b["items"][0].update(options=["머릿말", "햇볕", "윗층", "갯수", "인삿말"]))
    assert "ARCHETYPE_UNREGISTERED" in variant(lambda b: b["items"][0].update(archetype="BARE_FIVE_SENTENCES"))
    print("archetype gate regression PASS (sample ok, flat set + 9 faults blocked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

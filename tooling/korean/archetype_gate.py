#!/usr/bin/env python3
"""School archetype gate for KOR grammar/orthography bundles.

Checks that every item is built from a registered exam archetype and that every
distractor names a trap from the taxonomy. Applies to bundles that declare
`archetype_library`; older bundles are reported NOT_APPLICABLE.

    python tooling/korean/archetype_gate.py <bundle_dir>/items.yaml
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
COMBO = re.compile(r"^[ㄱ-ㅎ㉠-㉯ⒶⒷⒸ,\s]+$")


def analyze(bundle: dict, root: Path = ROOT) -> dict:
    rel = bundle.get("archetype_library")
    if not rel:
        return {"status": "NOT_APPLICABLE", "findings": []}
    library = yaml.safe_load((root / rel).read_text(encoding="utf-8"))
    types, traps, design = library["archetypes"], set(library["trap_taxonomy"]), library["set_design"]
    findings: list[dict] = []

    def fail(code: str, item: str | None = None, **extra):
        findings.append({"severity": "FAIL", "code": code, **({"item_id": item} if item else {}), **extra})

    items = bundle.get("items", [])
    used = Counter()
    view_count = 0
    constructed = 0
    for it in items:
        iid = it.get("item_id", "<missing>")
        kind = it.get("format", "MCQ")
        arch = it.get("archetype")
        if arch not in types:
            fail("ARCHETYPE_UNREGISTERED", iid, archetype=arch)
            continue
        spec = types[arch]
        used[arch] += 1
        if spec["format"] != kind:
            fail("ARCHETYPE_FORMAT_MISMATCH", iid)
        if it.get("view"):
            view_count += 1
        elif spec.get("view") == "REQUIRED":
            fail("VIEW_MISSING", iid)
        if it.get("difficulty") == "D1":
            fail("D1_RECALL_FORBIDDEN", iid)
        text = " ".join([it.get("stem", "")] + list(it.get("view", [])))
        if arch != "A3_CONDITION_CLASSIFICATION" and re.search(r"\[[가-힣]{1,4}\]", text.replace("[A]", "")):
            fail("MASKED_SPACING", iid)
        if kind == "CR":
            constructed += 1
            if len(it.get("conditions", [])) < spec.get("conditions_min", 3):
                fail("CR_CONDITIONS_SHORT", iid)
            if not it.get("rubric") or not it.get("model_answer"):
                fail("CR_RUBRIC_MISSING", iid)
            continue
        options = it.get("options", [])
        if options and not all(COMBO.match(o) or o.startswith("Ⓐ") for o in options):
            if all(len(o.replace(" ", "")) <= 6 for o in options):
                fail("SINGLE_WORD_OPTIONS", iid)
        answer = int(it.get("answer", 0))
        for index, judgment in enumerate(it.get("judgments", []), 1):
            if index != answer and judgment.get("trap") not in traps:
                fail("TRAP_UNCLASSIFIED", iid, option=index, trap=judgment.get("trap"))
        if arch == "A2_STUDENT_TEXT_ERRORS":
            marks = set(re.findall(r"[㉠-㉯]", " ".join(it.get("view", []))))
            if len(marks) != spec["constraints"]["marked_spots"]:
                fail("STUDENT_TEXT_SPOT_COUNT", iid, spots=len(marks))
    total = len(items)
    if total:
        if view_count / total < design["view_anchor_rate_min"]:
            fail("VIEW_ANCHOR_RATE_LOW", rate=round(view_count / total, 2))
        if constructed / total < design["constructed_ratio_min"]:
            fail("CONSTRUCTED_RATIO_LOW", rate=round(constructed / total, 2))
        unit = bundle.get("unit_size") or total
        units = max(1, round(total / unit))
        over = [a for a, n in used.items() if n > design["archetype_repeat_max_in_unit"] * units]
        if over:
            fail("ARCHETYPE_OVERUSE", archetypes=over)
    return {"tool": "ARC_KOR_ARCHETYPE_GATE_V1.0", "status": "FAIL" if findings else "PASS",
            "archetypes": dict(used), "view_anchor_rate": round(view_count / total, 2) if total else None,
            "constructed": constructed, "findings": findings}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("items", type=Path)
    args = ap.parse_args()
    report = analyze(yaml.safe_load(args.items.read_text(encoding="utf-8")))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] in {"PASS", "NOT_APPLICABLE"} else 1


if __name__ == "__main__":
    sys.exit(main())

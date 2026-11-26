#!/usr/bin/env python3
"""School archetype gate for KOR grammar/orthography bundles.

Checks that every item is built from a registered exam archetype and that every
distractor names a trap from the taxonomy. Applies to bundles that declare
`archetype_library`; older bundles are reported NOT_APPLICABLE.

Libraries that define `item_contract` (quality/korean/ARC_KOR_ORTHO_ARCHETYPES_V2.0.yaml)
also get the V2 orthography checks: per-item topic/rules/judgment_units/levers, the
difficulty floor (fake-difficulty guard), archetype difficulty range, marked-spot and
passage-set shape, bundle topic shares and coverage, textbook-example reuse and
lexicon-only traps. Rules: quality/korean/ARC_KOR_ORTHO_ITEM_RULES_V2.0.md.

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

    def warn(code: str, item: str | None = None, **extra):
        findings.append({"severity": "WARN", "code": code, **({"item_id": item} if item else {}), **extra})

    v2 = "item_contract" in library

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
        masked_ok = spec.get("masked_allowed") or arch == "A3_CONDITION_CLASSIFICATION"
        if not masked_ok and re.search(r"\[[가-힣]{1,4}\]", text.replace("[A]", "")):
            fail("MASKED_SPACING", iid)
        if v2:
            check_v2_item(it, iid, arch, spec, library, fail)
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
        spots = (spec.get("constraints") or {}).get("marked_spots")
        if spots is not None:
            marks = set(re.findall(r"[㉠-㉯]", " ".join(it.get("view", []))))
            if isinstance(spots, int) and len(marks) != spots:
                fail("STUDENT_TEXT_SPOT_COUNT", iid, spots=len(marks))
            elif isinstance(spots, list) and not spots[0] <= len(marks) <= spots[1]:
                fail("MARKED_SPOT_COUNT", iid, spots=len(marks), target=spots)
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
        if v2:
            check_v2_bundle(bundle, items, library, fail, warn)
    status = "FAIL" if any(f["severity"] == "FAIL" for f in findings) else "PASS"
    return {"tool": "ARC_KOR_ARCHETYPE_GATE_V1.1", "status": status,
            "archetypes": dict(used), "view_anchor_rate": round(view_count / total, 2) if total else None,
            "constructed": constructed, "findings": findings}


def _units(it: dict) -> int:
    try:
        return int(it.get("judgment_units") or 0)
    except (TypeError, ValueError):
        return 0


def check_v2_item(it: dict, iid: str, arch: str, spec: dict, library: dict, fail) -> None:
    """Per-item V2 orthography contract: fields, difficulty floor, archetype range, lexicon traps."""
    missing = [k for k in library["item_contract"]["required"] if it.get(k) in (None, "", [])]
    if missing:
        fail("ORTHO_FIELD_MISSING", iid, fields=missing)
        return
    if it["topic"] not in library["topics"]:
        fail("TOPIC_UNKNOWN", iid, topic=it["topic"])
    unknown = [lv for lv in it["levers"] if lv not in library["difficulty_levers"]]
    if unknown:
        fail("LEVER_UNKNOWN", iid, levers=unknown)
    if it.get("needs_lexicon") and not it.get("lexicon_in_view"):
        fail("LEXICON_ONLY_TRAP", iid)
    if it.get("format", "MCQ") == "CR":
        return
    level = it.get("difficulty")
    order = ["D1", "D2", "D3", "D4", "D5"]
    lo, hi = spec.get("difficulty", ["D1", "D5"])
    if level in order and not order.index(lo) <= order.index(level) <= order.index(hi):
        fail("ARCHETYPE_DIFFICULTY_OUT_OF_RANGE", iid, difficulty=level, allowed=[lo, hi])
    floor = library.get("difficulty_floor", {}).get(level)
    if floor:
        if _units(it) < floor.get("judgment_units_min", 0):
            fail("FAKE_DIFFICULTY_UNITS", iid, units=_units(it), need=floor["judgment_units_min"])
        if len(set(it["rules"])) < floor.get("rules_min", 0):
            fail("FAKE_DIFFICULTY_RULES", iid, rules=len(set(it["rules"])), need=floor["rules_min"])
        if len(set(it["levers"])) < floor.get("levers_min", 0):
            fail("FAKE_DIFFICULTY_LEVERS", iid, levers=len(set(it["levers"])), need=floor["levers_min"])


def check_v2_bundle(bundle: dict, items: list[dict], library: dict, fail, warn) -> None:
    """Bundle-level V2 orthography checks: passage sets, topic shares/coverage, example reuse, constructed share."""
    design = library["set_design"]
    total = len(items)
    sets: Counter = Counter()
    for it in items:
        spec = library["archetypes"].get(it.get("archetype"), {})
        size = (spec.get("constraints") or {}).get("set_size")
        if size:
            sets[(it.get("archetype"), it.get("set_id") or it.get("item_id"))] += 1
    for (arch, sid), n in sets.items():
        need = library["archetypes"][arch]["constraints"]["set_size"][0]
        if n < need:
            fail("PASSAGE_SET_INCOMPLETE", set_id=sid, items=n, need=need)

    topics = Counter(it.get("topic") for it in items if it.get("topic") in library["topics"])
    tol = 1 / total if total else 0
    spacing_hi = library["topics"]["SPACING"]["target"][1] + 0.05
    if total and topics["SPACING"] / total > spacing_hi + 1e-9:
        fail("TOPIC_SHARE_OUT_OF_RANGE", topic="SPACING", share=round(topics["SPACING"] / total, 3), max=spacing_hi)
    if total >= library.get("topic_coverage_min_items", 30):
        absent = [t for t in library["topics"] if not topics[t]]
        if absent:
            fail("TOPIC_COVERAGE_MISSING", topics=absent)
        for name, spec in library["topics"].items():
            lo, hi = spec["target"]
            share = topics[name] / total
            if not lo - tol - 1e-9 <= share <= hi + tol + 1e-9:
                fail("TOPIC_SHARE_OUT_OF_RANGE", topic=name, share=round(share, 3), target=[lo, hi])
    elif total >= 8 and len(topics) < 4:
        fail("TOPIC_DIVERSITY_LOW", topics=len(topics), need=4)

    reuse = sum(1 for it in items if it.get("textbook_example_reuse"))
    if total and reuse / total > design.get("textbook_example_reuse_max", 1.0) + 1e-9:
        fail("TEXTBOOK_EXAMPLE_FLOOD", share=round(reuse / total, 3), max=design["textbook_example_reuse_max"])

    soft = design.get("view_chars_soft_max")
    if soft and total:
        long_items = [it.get("item_id") for it in items if len("".join(map(str, it.get("view") or []))) > soft]
        for iid in long_items:
            warn("VIEW_LONG", iid, max=soft)
        if len(long_items) / total > design.get("long_view_share_max", 1.0) + 1e-9:
            fail("LONG_VIEW_SHARE_HIGH", share=round(len(long_items) / total, 3), max=design["long_view_share_max"])

    constructed = sum(1 for it in items if it.get("format") == "CR")
    override = str(bundle.get("user_override") or (bundle.get("v6") or {}).get("user_override") or "")
    if total and constructed / total < design.get("constructed_ratio_recommended", 0) and "객관식" not in override:
        warn("CONSTRUCTED_BELOW_RECOMMENDED", rate=round(constructed / total, 2))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("items", type=Path)
    args = ap.parse_args()
    report = analyze(yaml.safe_load(args.items.read_text(encoding="utf-8")))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] in {"PASS", "NOT_APPLICABLE"} else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""ENG exam-type gate: every item uses a registered Dongbuk type code and ARC_FINAL follows the 38-item blueprint.

Checks form only (type codes, positions, points, part counts, sentence-level underlines,
constructed-response conditions). Answer correctness belongs to blind review.

    python tooling/english/exam_type_gate.py <bundle_dir>/items.yaml
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
LIBRARY = "quality/english/ARC_ENG_EXAM_TYPES_V1.0.yaml"
UNDERLINE = re.compile(r"\(([a-g])\)")


def analyze(bundle: dict, root: Path = ROOT) -> dict:
    if str(bundle.get("subject", "")).upper() != "ENG":
        return {"status": "NOT_APPLICABLE", "findings": []}
    lib = yaml.safe_load((root / LIBRARY).read_text(encoding="utf-8"))
    types = lib["types"]
    findings: list[dict] = []

    def fail(code: str, item: str | None = None, **extra):
        findings.append({"severity": "FAIL", "code": code, **({"item_id": item} if item else {}), **extra})

    items = bundle.get("items", [])
    mcq = [it for it in items if it.get("format", "MCQ") == "MCQ"]
    crq = [it for it in items if it.get("format") == "CR"]
    for it in items:
        iid = it.get("item_id", "<missing>")
        code = it.get("eng_type")
        if code not in types:
            fail("ENG_TYPE_UNREGISTERED", iid, eng_type=code)
            continue
        area = types[code]["area"]
        if (area == "CRQ") != (it.get("format") == "CR"):
            fail("ENG_TYPE_FORMAT_MISMATCH", iid)
        if it.get("format", "MCQ") == "MCQ" and len(it.get("options", [])) != 5:
            fail("OPTION_COUNT", iid)
        if code == "ARC-ENG-GRM-02":
            text = " ".join([it.get("stem", "")] + list(it.get("view", [])) + list(it.get("passage_lines", [])) + list(it.get("passage", [])))
            marks = set(UNDERLINE.findall(text))
            if len(marks) < 5:
                fail("GRM02_UNDERLINES_SHORT", iid, marks=len(marks))
            if not it.get("grm02_correct"):
                fail("GRM02_KEY_SET_MISSING", iid)
            elif len(marks) - len(it["grm02_correct"]) < 2:
                fail("GRM02_TOO_FEW_ERRORS", iid)
        if it.get("format") == "CR":
            if len(it.get("conditions", [])) < 2:
                fail("CRQ_CONDITIONS_SHORT", iid)
            if not it.get("model_answer") or not it.get("rubric"):
                fail("CRQ_RUBRIC_MISSING", iid)

    product = bundle.get("product_mode")
    if product == "ARC_FINAL":
        totals = lib["arc_final_totals"]
        if len(mcq) != totals["selected_items"] or len(crq) != totals["constructed_items"]:
            fail("FINAL_ITEM_COUNT", selected=len(mcq), constructed=len(crq))
        else:
            for row in lib["arc_final_blueprint"]:
                for pos in row["items"]:
                    it = crq[int(pos[1:]) - 1] if isinstance(pos, str) else mcq[pos - 1]
                    if it.get("eng_type") not in row["types"]:
                        fail("FINAL_POSITION_TYPE", it.get("item_id"), position=pos, allowed=row["types"])
                    pts = float(it.get("points", 0))
                    if "points_each" in row:
                        ok = abs(pts - row["points_each"]) < 1e-9
                    else:
                        ok = row["points"][0] - 1e-9 <= pts <= row["points"][1] + 1e-9
                    if not ok:
                        fail("FINAL_POSITION_POINTS", it.get("item_id"), position=pos, points=pts)
            sel = round(sum(float(i.get("points", 0)) for i in mcq), 2)
            con = round(sum(float(i.get("points", 0)) for i in crq), 2)
            if sel != totals["selected_points"] or con != totals["constructed_points"]:
                fail("FINAL_POINT_TOTAL", selected=sel, constructed=con)
        if bundle.get("notice_line") != lib["exam_format_2026"]["notice_line"]:
            fail("FINAL_NOTICE_LINE_MISSING")
    elif product == "ARC_N":
        parts = lib["arc_n_set"]["parts"]
        size = sum(parts.values())
        if len(items) % size == 0 and items:
            sets = len(items) // size
            counts = Counter(types[i["eng_type"]]["area"] for i in items if i.get("eng_type") in types)
            for key, n in parts.items():
                area = key.split("_")[1]
                if counts.get(area, 0) != n * sets:
                    fail("N_PART_COUNT", area=area, expected=n * sets, got=counts.get(area, 0))
            if sum(1 for i in items if i.get("eng_type") == "ARC-ENG-GRM-02") < 2 * sets:
                fail("N_GRM02_SHORT")
        else:
            findings.append({"severity": "WARN", "code": "N_PARTIAL_SET", "items": len(items), "set_size": size})
    status = "FAIL" if any(f["severity"] == "FAIL" for f in findings) else "PASS"
    return {"tool": "ARC_ENG_EXAM_TYPE_GATE_V1.0", "status": status, "selected": len(mcq), "constructed": len(crq),
            "findings": findings}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("items", type=Path)
    args = ap.parse_args()
    report = analyze(yaml.safe_load(args.items.read_text(encoding="utf-8")))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] in {"PASS", "NOT_APPLICABLE"} else 1


if __name__ == "__main__":
    sys.exit(main())

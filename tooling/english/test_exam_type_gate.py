#!/usr/bin/env python3
"""ENG exam-type gate regression on structural skeletons (no passage content)."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("arc_eng_gate", ROOT / "tooling/english/exam_type_gate.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
LIB = yaml.safe_load((ROOT / gate.LIBRARY).read_text(encoding="utf-8"))
OPTS = ["a", "b", "c", "d", "e"]


def item(code: str, n: int, points: float | None = None) -> dict:
    if LIB["types"][code]["area"] == "CRQ":
        it = {"item_id": f"C{n}", "format": "CR", "eng_type": code, "conditions": ["c1", "c2"], "model_answer": "x", "rubric": ["r"]}
    else:
        it = {"item_id": f"Q{n}", "eng_type": code, "stem": "s", "options": OPTS}
        if code == "ARC-ENG-GRM-02":
            it.update(view=["(a) x (b) x (c) x (d) x (e) x (f) x (g) x"], grm02_correct=["a", "c", "f"])
    if points is not None:
        it["points"] = points
    return it


def final_skeleton() -> dict:
    mcq, crq = {}, {}
    for row in LIB["arc_final_blueprint"]:
        for pos in row["items"]:
            pts = row.get("points_each", row.get("points", [0])[0])
            (crq if isinstance(pos, str) else mcq)[pos] = item(row["types"][0], int(str(pos).lstrip("C")), pts)
    items = [mcq[k] for k in sorted(mcq)] + [crq[k] for k in sorted(crq)]
    # ranges start at their minimum; raise items to reach exactly 80 selected points
    need = round(80.0 - sum(i["points"] for i in items if i.get("format") != "CR"), 2)
    for row in LIB["arc_final_blueprint"]:
        if "points" not in row:
            continue
        for pos in row["items"]:
            room = round(row["points"][1] - mcq[pos]["points"], 2)
            add = min(room, need)
            mcq[pos]["points"] = round(mcq[pos]["points"] + add, 2)
            need = round(need - add, 2)
    assert need == 0, need
    return {"subject": "ENG", "product_mode": "ARC_FINAL", "notice_line": LIB["exam_format_2026"]["notice_line"], "items": items}


def n_skeleton() -> dict:
    plan = [("ARC-ENG-VOC-01", 15), ("ARC-ENG-GRM-01", 8), ("ARC-ENG-GRM-02", 2), ("ARC-ENG-RDG-04", 15),
            ("ARC-ENG-CRQ-01", 6), ("ARC-ENG-CRQ-03", 4)]
    items, n = [], 0
    for code, count in plan:
        for _ in range(count):
            n += 1
            items.append(item(code, n))
    return {"subject": "ENG", "product_mode": "ARC_N", "items": items}


def codes(bundle: dict) -> set[str]:
    return {f["code"] for f in gate.analyze(bundle)["findings"] if f["severity"] == "FAIL"}


def main() -> int:
    final, nset = final_skeleton(), n_skeleton()
    assert gate.analyze(final)["status"] == "PASS", gate.analyze(final)["findings"]
    assert gate.analyze(nset)["status"] == "PASS", gate.analyze(nset)["findings"]
    assert gate.analyze({"subject": "KOR", "items": []})["status"] == "NOT_APPLICABLE"

    def v(base, mutate):
        b = copy.deepcopy(base)
        mutate(b)
        return codes(b)

    assert "ENG_TYPE_UNREGISTERED" in v(final, lambda b: b["items"][0].update(eng_type="FREE_FORM"))
    assert "FINAL_POSITION_TYPE" in v(final, lambda b: b["items"][22].update(eng_type="ARC-ENG-RDG-04"))     # 23번은 GRM-02
    assert "FINAL_POSITION_TYPE" in v(final, lambda b: b["items"][33].update(eng_type="ARC-ENG-RDG-07"))     # 34번은 요약문
    assert "FINAL_POSITION_POINTS" in v(final, lambda b: b["items"][2].update(points=2.0))                   # 단어는 1점
    assert "FINAL_POINT_TOTAL" in v(final, lambda b: b["items"][36].update(points=5.0))
    assert "FINAL_ITEM_COUNT" in v(final, lambda b: b["items"].pop(5))
    assert "FINAL_NOTICE_LINE_MISSING" in v(final, lambda b: b.pop("notice_line"))
    assert "GRM02_UNDERLINES_SHORT" in v(final, lambda b: b["items"][22].update(view=["(a) x (b) x"]))
    assert "GRM02_TOO_FEW_ERRORS" in v(final, lambda b: b["items"][22].update(grm02_correct=list("abcdef")))
    assert "CRQ_CONDITIONS_SHORT" in v(final, lambda b: b["items"][34].update(conditions=["only one"]))
    assert "OPTION_COUNT" in v(final, lambda b: b["items"][0].update(options=OPTS[:4]))
    assert "N_PART_COUNT" in v(nset, lambda b: b["items"][0].update(eng_type="ARC-ENG-RDG-01"))
    assert "N_GRM02_SHORT" in v(nset, lambda b: b["items"][23].update(eng_type="ARC-ENG-GRM-01", view=None))
    print("ENG exam-type gate regression PASS (FINAL blueprint + N set ok, 13 faults blocked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

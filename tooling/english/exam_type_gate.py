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
LIBRARY = "quality/english/ARC_ENG_EXAM_TYPES_V1.1.yaml"
UNDERLINE = re.compile(r"\(([a-g])\)")
HANGUL = re.compile(r"[가-힣]")
LATIN = re.compile(r"[A-Za-z]{2,}")


SIMILAR_RELATIONS = {"SYNONYM", "WORD_FAMILY", "CONFUSABLE_FORM"}
SINGLE_WORD_OPTION_TYPES = {"ARC-ENG-VOC-01", "ARC-ENG-VOC-02", "ARC-ENG-VOC-04"}


def load_word_levels(lib: dict, root: Path) -> dict[str, str]:
    """word -> registered level (G1/G2/G3) from the user's list, when given."""
    rel = (lib.get("vocab_source_rule") or {}).get("word_list")
    if not rel or not (root / rel).is_file():
        return {}
    data = yaml.safe_load((root / rel).read_text(encoding="utf-8")) or {}
    return {str(e.get("word", "")).strip().lower(): str(e.get("level")).upper()
            for e in data.get("entries") or [] if isinstance(e, dict) and e.get("level")}


def load_word_list(lib: dict, root: Path) -> set[str] | None:
    """Hackers 1800+ headwords, or None while the user's list is still pending."""
    rel = (lib.get("vocab_source_rule") or {}).get("word_list")
    if not rel or not (root / rel).is_file():
        return None
    data = yaml.safe_load((root / rel).read_text(encoding="utf-8")) or {}
    words = {str(e.get("word", "")).strip().lower() for e in data.get("entries") or [] if isinstance(e, dict)}
    words.discard("")
    return words or None


def vocab_source_findings(items: list[dict], lib: dict, root: Path) -> list[dict]:
    """vocab_source_rule (user directive 2026-11-20): words the writer picks come from the Hackers book;
    a word outside the book needs a similar book word (SYNONYM / WORD_FAMILY / CONFUSABLE_FORM)."""
    rule = lib.get("vocab_source_rule") or {}
    targets_for = set((rule.get("applies_to") or {}).keys())
    if not targets_for:
        return []
    book = load_word_list(lib, root)
    registered_levels = load_word_levels(lib, root)
    allowed_levels = set((rule.get("word_level") or {}).get("allowed") or ["G1", "G2"])
    out: list[dict] = []
    total = in_book = 0

    def add(severity: str, code: str, item: str | None = None, **extra):
        out.append({"severity": severity, "code": code, **({"item_id": item} if item else {}), **extra})

    for it in items:
        code, iid = it.get("eng_type"), it.get("item_id", "<missing>")
        if code not in targets_for:
            continue
        rows = [r for r in it.get("vocab_targets") or [] if isinstance(r, dict)]
        if not rows:
            add("FAIL", "VOCAB_SOURCE_MISSING", iid, eng_type=code)
            continue
        listed = {str(r.get("word", "")).strip().lower() for r in rows}
        if code in SINGLE_WORD_OPTION_TYPES:
            option_words = {str(o).strip().lower() for o in it.get("options", []) if re.fullmatch(r"[A-Za-z][A-Za-z\-()]*", str(o).strip())}
            option_words = {re.sub(r"\(.*?\)", "", w) for w in option_words}
            missing = sorted(w for w in option_words if w and w not in listed)
            if missing:
                add("FAIL", "VOCAB_OPTION_SOURCE_MISSING", iid, words=missing)
        for r in rows:
            word = str(r.get("word", "")).strip().lower()
            source = str(r.get("source", "")).upper()
            total += 1
            # Word level G1~G2 (user directive 2026-11-20); the registered list wins over the item's own label.
            level = registered_levels.get(word) or str(r.get("level", "")).upper()
            if not level:
                add("FAIL", "VOCAB_LEVEL_MISSING", iid, word=word)
            elif level not in allowed_levels:
                add("FAIL", "VOCAB_LEVEL_OUT_OF_RANGE", iid, word=word, level=level, allowed=sorted(allowed_levels))
            if source == "HACKERS":
                if book is not None and word not in book:
                    add("FAIL", "VOCAB_NOT_IN_BOOK", iid, word=word)
                else:
                    in_book += 1
            elif source == "SIMILAR":
                similar = str(r.get("similar_to", "")).strip().lower()
                if not similar or str(r.get("relation", "")).upper() not in SIMILAR_RELATIONS:
                    add("FAIL", "VOCAB_SIMILAR_LINK_MISSING", iid, word=word)
                elif book is not None and similar not in book:
                    add("FAIL", "VOCAB_SIMILAR_NOT_IN_BOOK", iid, word=word, similar_to=similar)
                elif book is not None and word in book:
                    in_book += 1  # it is a book word after all
            else:
                add("FAIL", "VOCAB_SOURCE_INVALID", iid, word=word, source=source)
    if book is None and total:
        add("WARN", "VOCAB_BOOK_LIST_PENDING", list=rule.get("word_list"))
    share_min = 0.50  # user directive 2026-11-20 (was 0.80)
    if total and in_book / total < share_min:
        add("WARN", "VOCAB_BOOK_SHARE_LOW", share=round(in_book / total, 2))
    return out


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
        if it.get("format", "MCQ") == "MCQ":
            langs = {("KO" if HANGUL.search(o) else "EN") for o in it.get("options", []) if LATIN.search(o) or HANGUL.search(o)}
            if len(langs) > 1:
                fail("OPTION_LANGUAGE_MIXED", iid)
        if area == "VOC" and bundle.get("workbook_profile") == "PASSAGE_5":
            fail("VOC_TYPE_OUTSIDE_VOCAB_SECTION", iid, eng_type=code)
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

    findings.extend(vocab_source_findings(items, lib, root))

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
    elif product == "ARC_N" and bundle.get("workbook_profile") == "PASSAGE_5":
        per = lib["passage_workbook"]["items_per_passage"]
        counts = Counter(i.get("source_code") for i in items)
        for src, k in sorted(counts.items(), key=lambda x: str(x[0])):
            if src is None or k != per:
                fail("PASSAGE_ITEM_COUNT", source_code=src, expected=per, got=k)
        if crq:
            fail("PASSAGE_WORKBOOK_CRQ", items=len(crq))
        if not (bundle.get("layout") or {}).get("body_pt"):
            fail("PASSAGE_LAYOUT_MISSING")
        for it in items:
            if not it.get("source_label"):
                fail("PASSAGE_SOURCE_LABEL_MISSING", it.get("item_id"))
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
    return {"tool": "ARC_ENG_EXAM_TYPE_GATE_V1.1", "status": status, "selected": len(mcq), "constructed": len(crq),
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

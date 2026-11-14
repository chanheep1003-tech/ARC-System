#!/usr/bin/env python3
"""Executable structural gate for Korean exam realism metadata."""
from __future__ import annotations
import argparse, json, statistics
from pathlib import Path
from typing import Any
import yaml

STRAWMAN_MARKERS: tuple[str, ...] = (
    "무장 투쟁",
    "격렬한 대화",
    "스스로 조롱",
    "경제적 풍요를 상징",
    "장모음 'ㅓ'를 표기",
)


def inspect_items_realism(items: list[dict[str, Any]]) -> dict[str, Any]:
    """Inspect item options/views for strawman distractors, option length asymmetry, and unlinked views."""
    strawman_hits: list[dict[str, Any]] = []
    asymmetry_hits: list[dict[str, Any]] = []
    view_unlinked_hits: list[dict[str, Any]] = []

    for idx, it in enumerate(items, 1):
        if not isinstance(it, dict):
            continue
        iid = str(it.get("item_id") or it.get("no") or f"ITEM-{idx}")
        opts_raw = it.get("options") if it.get("options") is not None else it.get("choices")
        opts = [str(o) for o in opts_raw] if isinstance(opts_raw, list) else []
        view_raw = it.get("view") if it.get("view") is not None else it.get("box_paras")
        view_texts = [str(v) for v in view_raw] if isinstance(view_raw, list) else ([str(view_raw)] if isinstance(view_raw, str) and view_raw.strip() else [])

        # 1. Strawman fabricated extremes in options or view boxes
        matched_markers = []
        for text in opts + view_texts:
            for marker in STRAWMAN_MARKERS:
                if marker in text:
                    matched_markers.append(marker)
        if matched_markers:
            strawman_hits.append({"item_id": iid, "markers": sorted(set(matched_markers))})

        # 2. Option prose length asymmetry (for full-sentence 5-choice MCQs)
        if len(opts) == 5:
            lens = [len(o.replace(" ", "")) for o in opts]
            med = float(statistics.median(lens))
            min_len, max_len = min(lens), max(lens)
            if min_len >= 8 and med >= 20.0:
                if (min_len / med) < 0.45 or (max_len / min_len) > 2.6:
                    asymmetry_hits.append({"item_id": iid, "lens": lens, "median": med})

        # 3. View-box linkage audit when structured judgments carry explicit evidence refs
        judgments = it.get("judgments")
        if view_texts and isinstance(judgments, list) and judgments:
            evs = [str(ref).upper() for j in judgments if isinstance(j, dict) for ref in (j.get("ev") or [])]
            if evs and not any("VIEW" in ref or "TABLE" in ref or "FIGURE" in ref for ref in evs):
                view_unlinked_hits.append({"item_id": iid})

    return {
        "strawman_choice_count": len(strawman_hits),
        "option_length_asymmetry_count": len(asymmetry_hits),
        "view_unlinked_count": len(view_unlinked_hits),
        "strawman_items": strawman_hits,
        "asymmetry_items": asymmetry_hits,
        "view_unlinked_items": view_unlinked_hits,
    }


def load(path: Path):
    data=yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("profile must be mapping")
    return data

def analyze(data):
    product=str(data.get("product_mode","")).upper()
    n=int(data.get("item_count",0) or 0)
    c=data.get("counts",{}) or {}
    item_audit = inspect_items_realism(data["items"]) if isinstance(data.get("items"), list) else None
    fails=[]
    def num(k):
        val = int(c.get(k,0) or 0)
        if val == 0 and item_audit and k in item_audit:
            return int(item_audit[k])
        return val
    if product not in {"ARC_N","ARC_FINAL"}:
        fails.append("PRODUCT_MODE_INVALID")
    if n < 1:
        fails.append("ITEM_COUNT_INVALID")
        n=1
    school_rate=num("school_task_family_count")/n
    meta_rate=num("unanchored_meta_task_count")/n
    rare_rate=num("rare_artificial_task_count")/n
    min_school=0.75 if product=="ARC_N" else 0.80
    if school_rate < min_school: fails.append("SCHOOL_TASK_FAMILY_RATE_LOW")
    if meta_rate > 0.10: fails.append("UNANCHORED_META_TASK_OVERUSE")
    if rare_rate > 0.10: fails.append("RARE_ARTIFICIAL_TASK_OVERUSE")
    min_distinct=5 if n>=20 else 4
    if num("distinct_school_task_families") < min_distinct: fails.append("TASK_FAMILY_DIVERSITY_LOW")
    if num("unfunctional_student_wrapper_count") > max(1,n//10): fails.append("UNFUNCTIONAL_STUDENT_WRAPPER_OVERUSE")
    if num("ai_choice_pattern_count") > 0 or num("strawman_choice_count") > 0 or num("option_length_asymmetry_count") > 0:
        fails.append("AI_CHOICE_PATTERN")
    if num("correct_length_cue_count") > 0: fails.append("CORRECT_LENGTH_CUE")
    if num("same_stem_skeleton_max_run") > 2: fails.append("STEM_SKELETON_RUN")
    status="PASS" if not fails else "FAIL"
    out = {
      "tool":"ARC_KOREAN_EXAM_REALISM_GATE_V1.0_EXEC",
      "status":status,
      "KOR_EXAM_REALISM_GATE":status,
      "KOR_AI_STYLE_LEAK_GATE":"PASS" if not any(x in fails for x in ["UNANCHORED_META_TASK_OVERUSE","UNFUNCTIONAL_STUDENT_WRAPPER_OVERUSE","AI_CHOICE_PATTERN","CORRECT_LENGTH_CUE","STEM_SKELETON_RUN"]) else "FAIL",
      "KOR_SCHOOL_TASK_FAMILY_GATE":"PASS" if not any(x in fails for x in ["SCHOOL_TASK_FAMILY_RATE_LOW","TASK_FAMILY_DIVERSITY_LOW","RARE_ARTIFICIAL_TASK_OVERUSE"]) else "FAIL",
      "school_task_family_rate":round(school_rate,4),
      "unanchored_meta_task_rate":round(meta_rate,4),
      "rare_artificial_task_rate":round(rare_rate,4),
      "strawman_choice_count":num("strawman_choice_count"),
      "option_length_asymmetry_count":num("option_length_asymmetry_count"),
      "view_unlinked_count":num("view_unlinked_count"),
      "findings":fails
    }
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("profile",type=Path)
    args=ap.parse_args()
    result=analyze(load(args.profile))
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result["status"]=="PASS" else 1

if __name__=="__main__":
    raise SystemExit(main())

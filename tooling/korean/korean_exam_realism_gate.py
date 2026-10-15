#!/usr/bin/env python3
"""Executable structural gate for Korean exam realism metadata."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

def load(path: Path):
    data=yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("profile must be mapping")
    return data

def analyze(data):
    product=str(data.get("product_mode","")).upper()
    n=int(data.get("item_count",0) or 0)
    c=data.get("counts",{}) or {}
    fails=[]
    def num(k): return int(c.get(k,0) or 0)
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
    if num("ai_choice_pattern_count") > 0: fails.append("AI_CHOICE_PATTERN")
    if num("correct_length_cue_count") > 0: fails.append("CORRECT_LENGTH_CUE")
    if num("same_stem_skeleton_max_run") > 2: fails.append("STEM_SKELETON_RUN")
    status="PASS" if not fails else "FAIL"
    return {
      "tool":"ARC_KOREAN_EXAM_REALISM_GATE_V1.0_EXEC",
      "status":status,
      "KOR_EXAM_REALISM_GATE":status,
      "KOR_AI_STYLE_LEAK_GATE":"PASS" if not any(x in fails for x in ["UNANCHORED_META_TASK_OVERUSE","UNFUNCTIONAL_STUDENT_WRAPPER_OVERUSE","AI_CHOICE_PATTERN","CORRECT_LENGTH_CUE","STEM_SKELETON_RUN"]) else "FAIL",
      "KOR_SCHOOL_TASK_FAMILY_GATE":"PASS" if not any(x in fails for x in ["SCHOOL_TASK_FAMILY_RATE_LOW","TASK_FAMILY_DIVERSITY_LOW","RARE_ARTIFICIAL_TASK_OVERUSE"]) else "FAIL",
      "school_task_family_rate":round(school_rate,4),
      "unanchored_meta_task_rate":round(meta_rate,4),
      "rare_artificial_task_rate":round(rare_rate,4),
      "findings":fails
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("profile",type=Path)
    args=ap.parse_args()
    result=analyze(load(args.profile))
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result["status"]=="PASS" else 1

if __name__=="__main__":
    raise SystemExit(main())

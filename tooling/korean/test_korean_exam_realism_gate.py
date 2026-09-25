#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location("kor_realism",ROOT/"tooling/korean/korean_exam_realism_gate.py")
mod=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(mod)

good={"product_mode":"ARC_N","item_count":20,"counts":{
 "school_task_family_count":17,"distinct_school_task_families":7,
 "unanchored_meta_task_count":1,"rare_artificial_task_count":1,
 "unfunctional_student_wrapper_count":0,"ai_choice_pattern_count":0,
 "correct_length_cue_count":0,"same_stem_skeleton_max_run":2}}
assert mod.analyze(good)["status"]=="PASS"

bad={"product_mode":"ARC_FINAL","item_count":20,"counts":{
 "school_task_family_count":11,"distinct_school_task_families":3,
 "unanchored_meta_task_count":5,"rare_artificial_task_count":4,
 "unfunctional_student_wrapper_count":4,"ai_choice_pattern_count":3,
 "correct_length_cue_count":2,"same_stem_skeleton_max_run":4}}
r=mod.analyze(bad)
assert r["status"]=="FAIL"
assert "AI_CHOICE_PATTERN" in r["findings"]
assert "SCHOOL_TASK_FAMILY_RATE_LOW" in r["findings"]
assert "CORRECT_LENGTH_CUE" in r["findings"]
print("ARC KOREAN EXAM REALISM GATE: PASS")

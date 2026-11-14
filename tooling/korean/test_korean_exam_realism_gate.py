#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location("kor_realism",ROOT/"tooling/korean/korean_exam_realism_gate.py")
mod=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(mod)

spec_samples=importlib.util.spec_from_file_location("subject_sample_specs",ROOT/"tooling/typeset/subject_sample_specs.py")
samples_mod=importlib.util.module_from_spec(spec_samples); assert spec_samples and spec_samples.loader; spec_samples.loader.exec_module(samples_mod)

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

straw_items=[{
 "item_id":"TEST-STRAW",
 "options":[
  "화자는 시적 대상의 고단한 현실을 차분한 어조로 그려 낸다.",
  "화자는 친구들과 격렬한 대화를 나누며 무장 투쟁을 결의한다.",
  "대상의 모습과 대비되는 색채를 통해 삶의 비애를 드러낸다.",
  "시선의 이동을 따라 과거의 내력을 조심스럽게 헤아린다.",
  "공간의 한기를 통해 인물의 쓸쓸한 처지를 부각한다.",
 ],
}]
ir=mod.inspect_items_realism(straw_items)
assert ir["strawman_choice_count"]==1, ir
straw_payload={**good, "items": straw_items}
sr=mod.analyze(straw_payload)
assert sr["status"]=="FAIL" and sr["KOR_AI_STYLE_LEAK_GATE"]=="FAIL", sr

asym_items=[{
 "item_id":"TEST-ASYM",
 "options":[
  "작품은 슬픔을 노래한다.",
  "화자는 침묵을 유지한다.",
  "이 문항의 정답은 지문의 앞부분과 뒷부분의 맥락을 모두 종합하여 비로소 확인할 수 있는 복합적 진술이다.",
  "보통 길이로 작성된 비교적 평범한 수준의 오답 진술 문장 하나",
  "역시 보통 길이로 서술된 비교적 평범한 오답 진술 문장 둘",
 ],
}]
ar=mod.inspect_items_realism(asym_items)
assert ar["option_length_asymmetry_count"]==1, ar
ar_res=mod.analyze({**good, "items": asym_items})
assert ar_res["status"]=="FAIL" and "AI_CHOICE_PATTERN" in ar_res["findings"], ar_res

kor_spec=samples_mod.SUBJECT_SAMPLES["KOR"]
kor_items=[kor_spec["body1"][k] for k in ("q1","q2","q3")] + [kor_spec["body2"][k] for k in ("q4","q5","q6")]
kor_audit=mod.inspect_items_realism(kor_items)
assert kor_audit["strawman_choice_count"]==0, kor_audit
assert kor_audit["option_length_asymmetry_count"]==0, kor_audit
print("ARC KOREAN EXAM REALISM GATE: PASS")

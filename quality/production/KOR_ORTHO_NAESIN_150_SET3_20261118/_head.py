"""한글 맞춤법 내신형 150제 · 1세트(50문항: 선택형 45 + 서답형 5). 저장소 루트에서 실행.
범위: 총칙(제1항) · 소리(제5~12항) · 형태①(제14·15·18~25·51항).
사용자 지시(2026-11-18): L2~L4, 기본·흔한 문제 축소, 새 <보기> 조항·예문·지문 추론형·심화·낯선 문제 위주,
㉠·㉡ 등 표지 문장은 단락을 나누어 조판."""
import yaml
from pathlib import Path

S, M, W = "STRONG", "MEDIUM", "WEAK"
FAM = {"A1_GENERAL_RULE_MAPPING": "VIEW_APPLICATION", "A2_STUDENT_TEXT_ERRORS": "ERROR_CORRECTION",
       "A3_CONDITION_CLASSIFICATION": "COMPARISON_MATRIX", "A4_INQUIRY_DIALOGUE_CHECK": "STUDENT_RESPONSE_EVALUATION",
       "A5_EXAMPLE_MULTI_JUDGMENT": "MULTI_JUDGMENT", "A6_RULE_CASE_EXPLANATION": "CASE_APPLICATION"}
TRAP = {"A1_GENERAL_RULE_MAPPING": "T1_RIGHT_CONCEPT_WRONG_CASE", "A2_STUDENT_TEXT_ERRORS": "T6_PARTIAL_SET",
        "A3_CONDITION_CLASSIFICATION": "T4_SAME_FORM_OTHER_FUNCTION", "A4_INQUIRY_DIALOGUE_CHECK": "T1_RIGHT_CONCEPT_WRONG_CASE",
        "A5_EXAMPLE_MULTI_JUDGMENT": "T6_PARTIAL_SET", "A6_RULE_CASE_EXPLANATION": "T5_RULE_JURISDICTION"}
STEPS = {"D2": 1, "D3": 2, "D4": 3}
raw = []


def mcq(arch, d, stem, view, opts, ans, whys, neg=False, fixed=False, topic=""):
    """whys: 선지별 (강도, 근거[, 함정]) — 정답 선지의 강도는 무시."""
    # ㉠~㉤ 순서대로 짝지은 선지는 순서를 바꾸지 않는다
    if all(o[:1] in "㉠㉡㉢㉣㉤" for o in opts):
        fixed = True
    raw.append(dict(arch=arch, d=d, stem=stem, view=view, opts=opts, ans=ans, whys=whys, neg=neg, fixed=fixed, topic=topic))


def cr(stem, view, conditions, model, rubric, d, topic=""):
    raw.append(dict(cr=True, stem=stem, view=view, conditions=conditions, model=model, rubric=rubric, d=d, topic=topic))


# ARC RUNTIME PRIORITY POLICY V1.5
VERSION: 1.4
DATE: 2026-09-25
STATUS: ACTIVE-DEV
ROLE: deadline scheduling, product focus, quality-first allocation

## 0. HARD DEADLINE
2026-09-25 23:59 KST.

## 1. ABSOLUTE ORDER
1. KOR ARC_N + ARC_FINAL — quality first
2. SOC ARC_N + ARC_FINAL
3. SCI-REDOX ARC_N + ARC_FINAL
4. HIS ARC_N only

CORE maintenance only.
SCI non-redox excluded.
HIS FINAL deferred.

## 2. KOREAN FOCUS LOCK
남은 discretionary quality work의 최소 60%를 국어에 우선 배정한다.
KOR N°와 FINAL 모두 다음을 만족할 때까지 국어 우선권 유지:
- readiness >= 80
- KOR_EXAM_REALISM_GATE=PASS
- KOR_AI_STYLE_LEAK_GATE=PASS
- KOR_SCHOOL_TASK_FAMILY_GATE=PASS
- KOR_ATTRACTIVE_DISTRACTOR_GATE=PASS
- KOR_ANSWER_LENGTH_AUDIT=PASS
- no open S1 Korean item-quality regression

인프라가 PASS여도 fresh content realism이 PENDING이면 국어 품질 작업을 종료하지 않는다.

## 3. RESOURCE ORDER
- KOR: 60
- SOC: 20
- SCI_REDOX: 12
- HIS_N: 8

한 run에 여러 작업을 얕게 흩뿌리지 않는다.
가장 높은 우선순위의 blocker를 실제로 닫고 동일 E2E/QA를 재실행하여 score delta 또는 PASS를 만든다.

## 4. KOR QUALITY METHOD
학교 실제 시험 2025~2026 구조 프로필을 TASK-FORM calibration으로 사용.
문구 복제/교사 의도 예측 금지.
실제 내신 빈출 과업에서 난도를 올린다:
내용 이해, 정서·태도, 표현 효과, 핵심 표현 기능, <보기> 적용, 비교, 복수판단, 구조/개념 관계.

AI 티 제거:
- 내부 QA 언어 학생 노출 금지
- 불필요한 학생/교사 wrapper 금지
- 기계적 평행 선지 금지
- 정답만 장문·온건·정교한 패턴 금지
- 황당한 오답으로 난도 위장 금지

## 4-A. KOREAN FRESH-SET CLOSURE
국어는 규칙 파일만 개선하고 종료하지 않는다.
최소 하나의 fresh KOR ARC_N 또는 ARC_FINAL 세트를 실제 현재 범위 원자료로 생성하여 다음을 모두 확인할 때까지 국어 품질 작업을 계속한다:
- 실제 내신 빈출 task family 비율 충족
- AI-style leak 0
- 정답 길이 cue 0
- D3+ strong distractor >=2
- obvious-answer D3+ = 0
- 동일 reasoning axis 과다 반복 없음
- exact/semantic duplicate gate 통과
- Generator→QA→Handoff→Typesetter→PDF→Preflight E2E PASS

한 run에서 의미 있는 결과는 최소 하나:
1. fresh KOR 세트가 위 gate를 통과
2. user-found Korean regression 하나를 실제 세트에서 재현 후 수정+재검사 PASS
3. KOR_N 또는 KOR_FINAL readiness +10 이상 상승

국어 N°와 FINAL이 둘 다 80 미만이면 다른 과목 polishing보다 국어를 우선한다.
단, 국어가 source-access hard blocker로 막힌 경우에만 다음 과목으로 이동한다.

## 5. REMAINING SUBJECTS
SOC: KOR quality blocker가 닫힌 다음 N°/FINAL.
SCI: OXIDATION_REDUCTION_ONLY, N°/FINAL.
HIS: N° ONLY.

## 6. MEANINGFUL RUN
한 실행의 완료 조건은 최소 하나:
- fresh KOR N°/FINAL quality gate PASS
- 실제 blocker 수정 + 동일 regression PASS
- subject/product readiness +10
- new E2E/CANARY PASS
- release readiness 실질 상승

상태 재확인만으로 완료 처리 금지.

END ARC RUNTIME PRIORITY POLICY V1.4


## FINAL PREPARATION OVERRIDE — 2026-10-03
For the active DONGBUK_2026_2_FINAL preparation cycle, resolve scope and product admission from runtime.exam_context_registry. The midterm SCI-REDOX-only, HIS-N-only sprint and its numeric allocation are historical. Do not use them to infer final-exam units, disable new subject collection, or carry exclusion marks into different sources. Existing subject priority is retained for discovery; current-source eligibility is evidence-bound and pending until verified. N°/FINAL quality improvements remain the development priority. CORE changes focus on compatibility, regression prevention, and critical defects. No teacher-style prediction or unverified grade claims.

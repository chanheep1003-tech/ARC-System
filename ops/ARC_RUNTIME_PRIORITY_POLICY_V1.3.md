# ARC RUNTIME PRIORITY POLICY V1.3
VERSION: 1.3
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
남은 discretionary quality work의 최소 절반을 국어에 우선 배정한다.
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
- KOR: 50
- SOC: 25
- SCI_REDOX: 15
- HIS_N: 10

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

END ARC RUNTIME PRIORITY POLICY V1.3

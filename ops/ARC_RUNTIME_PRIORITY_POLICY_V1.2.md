# ARC RUNTIME PRIORITY POLICY V1.2
VERSION: 1.2
DATE: 2026-09-24
STATUS: ACTIVE-DEV
ROLE: runtime scheduling, product focus, scope allocation

## 0. PURPOSE
시험 직전 제한된 시간과 계산 자원을 실제 학습효과가 가장 큰 N°/FINAL 산출물에 집중한다.
사용자의 최신 명시적 범위/제품 지시는 과거 일반 우선순위보다 우선한다.

## 1. MIDTERM PRODUCT-SCOPE LOCK
2026-09-25 RC까지 활성 목표:

1. KOR
   - PRODUCTS: ARC_N, ARC_FINAL
   - SCOPE: 학교 보충자료 + 교과서 1단원
   - PRIORITY: 보충자료 최우선

2. SOC
   - PRODUCTS: ARC_N, ARC_FINAL
   - SCOPE: 지정 시험범위 전체
   - Social C X-mark exclusion은 blocking scope rule 유지

3. HIS
   - PRODUCTS: ARC_N ONLY
   - SCOPE: 지정 시험범위 전체
   - ARC_FINAL: DEFERRED / OUT_OF_CURRENT_SPRINT
   - FINAL CANARY, FINAL 품질 최적화, FINAL 조판 개발에 자원 투입 금지
   - 단, 공통 FINAL 엔진 변경의 비의도 회귀 여부를 확인하기 위한 정적 호환성 검사만 허용

4. SCI
   - PRODUCTS: ARC_N, ARC_FINAL
   - SCOPE: OXIDATION_REDUCTION_ONLY
   - 산화·환원 외 모든 통합과학 단원은 CURRENT_SPRINT_EXCLUDED
   - 다른 단원 문제 생성, CORE 집필, N°/FINAL 생성, 외부자료 수집, CANARY, 회귀 fixture 신규 작성 금지
   - 기존 범용 과학 파일은 삭제하지 않되 현재 실행의 source/scope 후보로 사용하지 않음

5. AI
   - CURRENT_SPRINT_DEFERRED

## 2. RESOURCE ORDER
실제 처리 순서:
KOR N°/FINAL
→ SOC N°/FINAL
→ HIS N°
→ SCI-REDOX N°/FINAL

CORE는 maintenance mode이며 치명적 회귀 확인 외 신규 개선 금지.

권장 추가 자원:
- KOR 35
- SOC 30
- HIS_N 15
- SCI_REDOX 20

## 3. REQUIRED STAGES
P0 SCOPE / ACCURACY / UNIQUE ANSWER
P1 ACTUAL ITEM PRODUCTION
P2 REQUIRED QA
P3 REQUIRED VISUALS
P4 BANK / SET EDITORIAL
P5 RESEARCH / OPTIMIZATION

P0-P2는 생략 금지.
답에 직접 필요한 시각자료는 P3 생략 금지.

## 4. SCIENCE FAIL-CLOSED SCOPE
SCI request가 산화·환원 밖이면:
- CURRENT_SPRINT_SCOPE_REJECT
- 자동으로 다른 과학 단원을 생성하지 않음
- 자료수집 후보에도 넣지 않음
- 사용자가 명시적으로 스프린트 범위를 다시 확장하지 않는 한 유지

## 5. HISTORY PRODUCT FAIL-CLOSED
HIS request의 product가 ARC_FINAL이면:
- CURRENT_SPRINT_PRODUCT_DEFERRED
- 자동 FINAL 생성/조판/CANARY 금지
- 동일 범위의 ARC_N 작업으로 자원을 재배정

## 6. FAILURE ISOLATION
한 과목 실패가 전체 run을 종료하지 않는다.
현재 우선순위에 따라 다른 활성 제품으로 진행 후 blocker를 재시도한다.

## 7. USER OVERRIDE
이 정책은 2026-09-24 사용자 지시를 반영한 현재 중간고사 스프린트 lock이다.
추후 사용자가 명시적으로 범위 또는 제품을 다시 변경하면 새 지시가 우선한다.

END ARC RUNTIME PRIORITY POLICY V1.2

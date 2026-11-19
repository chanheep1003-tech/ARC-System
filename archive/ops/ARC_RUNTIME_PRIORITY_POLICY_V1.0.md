# ARC RUNTIME PRIORITY POLICY V1.0
VERSION: 1.0
DATE: 2026-09-18
STATUS: ACTIVE-DEV
ROLE: runtime scheduling and resource-allocation policy

## 0. PURPOSE
시간, 컨텍스트, 도구 호출 한도가 부족할 때 무엇을 먼저 완료하고 무엇을 미룰지 고정한다.
문항 정확성과 필수 QA를 희생해 더 많은 산출물을 만드는 것을 금지한다.

## 1. SUBJECT PRIORITY
기본 우선순위:
1. KOR — 공통국어2
2. SOC — 통합사회2
3. SCI — 통합과학2
4. HIS — 한국사2
5. AI — 인공지능기초

정상 100문항 QA에서는 과목당 20문항을 유지한다.
우선순위는 문항 수를 줄이는 기준이 아니라 처리 순서, 재시도, 추가 검수, 자료 탐색, 컨텍스트 배분의 기준이다.

권장 추가 리소스 비중:
- KOR 30%
- SOC 25%
- SCI 20%
- HIS 15%
- AI 10%

## 2. STAGE PRIORITY
P0 — SCOPE / ACCURACY / UNIQUE ANSWER
- 범위 잠금
- 정답 유일성
- 사실·수치·조건 오류 방지
- USER_X_EXCLUSION 등 hard scope rules

P1 — ACTUAL ITEM PRODUCTION
- 실제 RAW 문항 생성
- 과목별 persist-first 저장

P2 — REQUIRED QA
- Fact Audit
- Source Ledger when required
- Item Quality
- Naturalness
- Similarity
- Difficulty sanity
- Sentinel recheck

P3 — REQUIRED VISUALS
- 풀이에 필수인 그래프/도식/표/지도/연표/실험도
- 필수 자산의 실제 렌더 및 무결성

P4 — BANK / SET EDITORIAL
- BANK_PASS 저장
- set-level editorial
- 선택적 세트 균형 조정

P5 — RESEARCH / OPTIMIZATION
- 추가 외부자료 탐색
- 비필수 참고자료 확장
- 엔진/프롬프트 최적화
- 비필수 분석

## 3. DEGRADATION ORDER
리소스가 부족하면 다음 순서로 미룬다:
1. P5 전부
2. P4의 비필수 set-level polish
3. P3의 비필수 시각자료

P0~P2는 생략 금지.
필수 시각자료가 필요한 문항은 P3도 생략 금지.

## 4. SUBJECT FAILURE ISOLATION
각 과목은 독립 checkpoint다.
한 과목이 실패하면:
1. 실패 로그 저장
2. last_completed_stage 기록
3. 해당 과목을 FAILED_PENDING_RESUME로 표시
4. 다음 우선순위 과목으로 계속 진행
5. 모든 과목 1차 처리 후 실패 과목을 우선순위 순으로 resume

한 과목 실패 때문에 전체 런을 즉시 종료하지 않는다.

## 5. RETRY BUDGET
같은 과목/단계의 자동 재시도는 기본 1회.
두 번째 실패 시:
- 동일 런에서 무한 재시도 금지
- 실패 로그 + resume target 저장
- 다음 과목으로 진행

정확성 hard fail을 우회하기 위한 retry는 금지한다.

## 6. OPTIONAL WORK CAP
필수 산출물보다 추가 연구/최적화가 앞서면 안 된다.
한 런에서 P5 작업은 P0~P4가 필요한 과목에 대해 완료된 뒤에만 허용한다.
scheduled QA는 기본적으로 GitHub rule mutation을 하지 않는다.

## 7. SUCCESS REPORT
실행 보고서에 최소:
- SUBJECT_ORDER
- SUBJECT_STATUS
- DEFERRED_STAGE
- RETRY_USED
- REQUIRED_QA_SKIPPED = 0
- OPTIONAL_WORK_DEFERRED
를 기록한다.

## 8. USER OVERRIDE
사용자가 특정 과목을 명시적으로 최우선으로 지정하면 그 실행에 한해 subject order를 바꿀 수 있다.
명시적 override가 없으면 KOR→SOC→SCI→HIS→AI를 사용한다.

END ARC RUNTIME PRIORITY POLICY V1.0
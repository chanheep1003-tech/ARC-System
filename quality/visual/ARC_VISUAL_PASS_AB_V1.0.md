# ARC VISUAL PASS A/B V1.0
VERSION: 1.0
DATE: 2026-09-18
STATUS: ACTIVE-DEV

## PURPOSE
시각자료를 만든 주체의 자기검수만으로 정확성을 확정하지 않는다.

## PIPELINE
VISUAL_SPEC
→ deterministic render
→ VISUAL_PASS_A
→ independent VISUAL_PASS_B
→ QUESTION_VISUAL_CROSSCHECK
→ AUTHENTICITY_RUBRIC
→ PDF PREFLIGHT

## PASS A — RENDERER SELF CHECK
제작 직후 다음을 기계적으로 확인한다.
- spec schema 완전성
- renderer 성공
- semantic element 수
- 축/단위/범례/레이블 존재
- 필수 node/edge 존재
- asset 크기/빈 파일 여부
- RENDER_MANIFEST와 spec hash 기록

PASS A는 제작자/renderer 자신의 검증이므로 이것만으로 release할 수 없다.

## PASS B — INDEPENDENT CHECK
별도 verifier가 원 VISUAL_SPEC, RENDER_MANIFEST, 실제 SVG/PDF asset을 다시 읽는다.
검증기는 renderer의 PASS 판정을 그대로 신뢰하지 않는다.

### SCI-GRAPH
- x/y 데이터 배열
- 축 이름/단위
- 범례/series 수
- 방향/증감 관계
- 문항의 수치와 visual spec 일치

### SCI-PARTICLE
- species별 before/after 실제 element count
- charge/state label
- REDOX_LEDGER의 consumed/produced count
- 양이온 수와 전체 이온 수의 구분
- 전자수 보존과 입자 변화의 일치
- 금속 원자/이온 혼동 없음

### SCI-EXPERIMENT
- 필수 장치 node
- connection pair
- 방향 화살표
- 관찰 위치
- 조건 label

### SOC-DATA/STAT
- 변수/단위/분모/기준연도
- level vs rate
- 범주/series
- 표/그래프 숫자 일치

### SOC-MAP
- verified base map 사용
- region IDs
- highlight set
- legend
- 지도 경계/레이블이 spec과 일치

### SOC-FLOW/INSTITUTION
- node 집합
- directed edge 집합
- actor/institution/effect 구분
- 절차 방향

### HISTORY
- timeline order/date
- map region/route
- organization relation

## QUESTION_VISUAL_CROSSCHECK
문항 계산/정답 근거와 시각자료를 별도로 대조한다.
텍스트에서 계산한 값과 그림 속 개수/수치/방향이 다르면 HARD VISUAL FAIL.

## REQUIRED QC FIELDS
VISUAL_PASS_A = PASS/FAIL
VISUAL_PASS_B = PASS/FAIL/NOT_APPLICABLE
QUESTION_VISUAL_CROSSCHECK = PASS/FAIL
VISUAL_VERIFIER_VERSION
RENDER_MANIFEST_ID
REDOX_VISUAL_CROSSCHECK = PASS/FAIL/NOT_APPLICABLE

## HARD BLOCK
ESSENTIAL=true 시각자료에서 PASS A, PASS B, CROSSCHECK 중 하나라도 FAIL/미실행이면 BANK_PASS와 FINAL_RELEASE 금지.

END ARC VISUAL PASS A/B V1.0

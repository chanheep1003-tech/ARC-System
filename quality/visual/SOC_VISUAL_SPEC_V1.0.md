# ARC SOCIAL VISUAL SPEC V1.0
VERSION: 1.0
DATE: 2026-09-18
STATUS: ACTIVE-DEV
SUBJECT: 통합사회2

## SOC-FLOW
필수:
- NODES[id,label,role]
- EDGES[from,to,relation,directed]
- START/END 또는 흐름 기준
- 필요한 조건/시점
금지:
- 방향 없는 인과 흐름
- 교차 화살표로 관계 모호화
- 박스 배치만으로 위계를 암시하고 실제 edge를 생략

## SOC-CASEBOX
필수:
- actor
- situation
- relevant_condition
- evidence/data(optional)
- decision_target
금지:
- 사례 문장 자체가 정답을 직접 노출
- 판단에 불필요한 장식 아이콘
- 현실 판례와 교육용 변형 사례 혼동

## SOC-COMPARE
필수:
- entities[]
- shared_criteria[]
- values by criterion
- common/different relation if explicitly used
금지:
- 대상마다 다른 기준으로 비교
- 한쪽 정보 누락을 차이처럼 표현
- 공통점과 차이를 색상만으로 구분

## SOC-DATA / SOC-STAT
필수:
- metric
- unit
- denominator when ratio/share/rate
- reference_year/time
- categories/series
- values
- source_role
검증:
- 비율↔절대수 혼동 금지
- 증가율↔증가량 혼동 금지
- 평균↔개인 일반화 금지
- 서로 다른 분모 직접비교 금지
- 기준연도/단위 누락 금지

## SOC-MAP
필수:
- verified_base_source
- region_ids
- highlighted_regions/routes
- legend
- label_set
- projection/simplification note if relevant
금지:
- LLM이 임의 생성한 행정경계
- 실제 경계를 미관상 이동
- 지도에 없는 위치를 추정 표기
- 위성지도/마케팅 지도풍

## SOC-INSTITUTION
권리구제·기관·절차용.
필수:
- actor
- action/request
- institution
- institution_power
- remedy/effect
- directed procedure edges
금지:
- 기관과 권한 교환
- 청구/심판/재판 절차 방향 역전
- 효과를 기관명만으로 암시

## COMMON PASS B
모든 사회 시각자료는 원 spec과 실제 렌더를 독립 대조한다.
C파트 자료이면 C_X_MARK_FILTER가 선행 PASS여야 한다.

END ARC SOCIAL VISUAL SPEC V1.0

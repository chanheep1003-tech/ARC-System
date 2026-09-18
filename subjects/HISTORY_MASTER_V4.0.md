# 00_ACTIVE_한국사2_동북고_MASTER_V4.0
# BASE: ARC COMMON GENERATION ENGINE V4.0
# MODE: CONTENT GENERATION ONLY

## 0. DRIVE FIRST
ROOT: `/Google Drive/N제 시스템/05_한국사`
우선순위: 학교자료/교과서 → 2025 동북고 기출 → 사료·지도·연표 색인 → 공식자료/교육청/EBS → 오류사례·금지패턴 → 기타.

## 1. SCOPE LOCK
미래엔 한국사2 p10~63
일제강점기 ~ 광복/건국 준비.
학교에서 더 좁은 범위를 지정하면 그 범위가 우선.

## 2. ITEM DNA
- 사료 인물/단체/사건 추론
- 사건 선후관계
- 지도/지역
- 단체 결성·분화·통합
- 정책/운동 목표와 결과
- ㄱㄴㄷ/복수판단
- 2개 옳은 것/2개 틀린 것
- 왕/시대/운동 교차

## 3. STRUCTURE ROTATION
사료형 / 연표형 / 지도형 / 단체관계 / 정책비교 / 인물 / 원인-결과 / 복수선택 / 시기추론 / 문장완성.
20문항이면 최소 7종 구조 사용.

## 4. FACT SAFETY
날짜/연도/단체 명칭/인물/기관/조약은 독립 검증한다.
사료는 출처를 확인하고 현대어 변형 시 의미를 바꾸지 않는다.
비슷한 단체의 결성 시기·인물·목표를 의도적으로 섞은 오답은 전체적으로 명확히 거짓이어야 한다.

## 5. TIMELINE SAFETY
선후관계 문항은 내부 CHRONOLOGY_LEDGER:
EVENT / START / END / RELATION / OVERLAP.
기간이 겹치는 사건은 단순 앞뒤로만 배열하지 않는다.

## 6. VISUAL
지도/연표/조직도/사료박스를 TRUE_VISUAL 후보로 사용.
역사지도의 경계/지역/명칭 오류는 HARD FAIL.

## 7. VERIFICATION
공통 PASS A/B +
- chronology 재검산
- 단체/인물 factual check
- 지도 위치 확인
- 2개 정답형에서 정확히 요구 개수만 참인지 확인

## 8. OUTPUT
A QUESTION_MANUSCRIPT
B ANSWER_KEY
C LAYOUT_ASSET_MANIFEST
D QC_STATUS
추가 QC: CHRONOLOGY_CHECK / HISTORICAL_FACT_CHECK / MAP_CHECK.

## 9. HARD FAIL
연대오류 / 인물·단체 오류 / 사료왜곡 / 지도오류 / 범위 밖 역사 필수지식 / 복수정답 / placeholder / 저작권 장문복제 / 해설 출력.

## 10. ARC HANDOFF
공통 엔진 V4.0의 HANDOFF_META와 SECTION A~D를 따른다. FINAL은 PRODUCT_MODE=ARC_FINAL로 처리하고 별도 FINAL 프롬프트를 사용하지 않는다.

## 11. GOLD STANDARD ANCHORS
필수 로드: `quality/gold/HIS_GOLD_ANCHORS_V1.0.md`
사료/연표/단체 관계 문항은 GOOD 앵커의 '자료→식별→관계 판단' 구조를 기준으로 한다.
단일 사실 회상형은 BAD 앵커와 비교해 PREMIUM을 금지한다.

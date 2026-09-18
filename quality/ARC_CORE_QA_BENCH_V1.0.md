# ARC CORE QA BENCH V1.0
VERSION: 1.0
DATE: 2026-09-19
STATUS: ACTIVE-DEV
ROLE: ARC CORE 세트 단위 품질·편집 자연스러움 검수

## 0. PURPOSE
CORE가 정보는 맞지만 'AI가 자동 생성한 요약 카드'처럼 보이는 문제를 차단한다.
개념 정확성, 학교자료 충실도, 학습 효율, 편집 자연스러움을 함께 검사한다.

## 1. HARD FAIL
하나라도 발생하면 CORE_QA=FAIL:
- 범위 밖 내용을 핵심 개념처럼 확장
- 학교자료와 충돌하는 설명
- 학생용에 CONCEPT_ID / N_GENERATION_LINKS / QA score / BANK / priority 등 내부 metadata 노출
- 근거 없는 TRAP을 사실 또는 빈출 함정처럼 제시
- SOURCE_TEXT_BLOCK의 누락/순서 변경/임의 교정
- 작품 원문과 해설을 섞어 원문의 일부처럼 제시
- 같은 설명을 본문/MUST/TRAP에서 반복해 정보 밀도가 현저히 떨어짐
- 모든 concept가 사실상 동일한 블록 뼈대와 동일한 bullet 수로 반복
- 근거 없는 '시험에 무조건 나온다/선생님이 낸다' 표현
- 시각자료가 장식뿐이고 정보 기능이 없음

## 2. SCORE — 100
SOURCE_AND_SCOPE_FIDELITY /25
CONCEPT_COMPLETENESS /20
EDITORIAL_NATURALNESS /20
STUDENT_USEFULNESS /15
CONFUSING_TRAP_QUALITY /10
VISUAL_FUNCTION /5
METADATA_HYGIENE /5

92~100 = CORE_A
86~91 = CORE_B
80~85 = REVISE
79 이하 = FAIL
HARD FAIL은 점수와 무관하게 FAIL.

## 3. EDITORIAL NATURALNESS SENTINELS
세트 전체에서 검사:
- concept별 block 수가 자연스럽게 다른가
- MUST/CONFUSING/TRAP이 정말 필요한 곳에만 있는가
- 제목 문법과 문단 길이가 지나치게 균일하지 않은가
- 3단 bullet 패턴이 기계적으로 반복되지 않는가
- 동일 연결어/종결 표현이 연속적으로 반복되지 않는가
- 박스가 본문보다 시각적으로 많지 않은가
- 표가 비교가 필요한 곳에만 쓰이는가
- 빈 공간을 채우기 위한 장식 문구가 없는가

다음이면 AI_PATTERN_SUSPECT=true:
- 70% 이상 concept가 같은 선택 블록 조합을 가짐
- 70% 이상 MUST가 정확히 3개
- 70% 이상 TRAP이 동일 문형
- 연속 4개 concept가 같은 제목+본문+MUST+CONFUSING+TRAP 순서
- 짧은 concept까지 억지 예시/표/도식을 하나씩 보유

AI_PATTERN_SUSPECT=true면 최소 5개 concept를 blind editorial recheck한다.

## 4. REDUNDANCY AUDIT
같은 concept에서:
CORE EXPLANATION
MUST
CONFUSING
TRAP
EXAM CONNECTION
사이에 실질적으로 같은 문장이 반복되는지 확인한다.

같은 의미의 재진술이 3곳 이상 반복되면:
REDUNDANCY_FLAG
CORE_EDITORIAL_NATURALNESS != PASS
수정 필요.

## 5. TRAP AUDIT
각 TRAP은 내부적으로 TRAP_EVIDENCE를 가져야 한다.
허용 근거:
- 현재 학교자료의 명시적 혼동 포인트
- 실제 기출/검수된 문항에서 확인된 오개념 구조
- N° 검수에서 반복 확인된 오류
- 교과 개념상 일반적으로 명확한 오개념

금지:
- 난도를 높이기 위해 AI가 즉석에서 만든 극단적 오답
- 출제 빈도를 추측한 함정
- 범위 밖 지식으로만 반박 가능한 함정

TRAP_EVIDENCE가 없으면 학생용 TRAP을 삭제한다.

## 6. KOREAN CORE BENCH
국어는 추가 검사:
- 학교 보충자료의 해석 순서/용어가 반영되는가
- 작품을 주제/정서/표현법 카드로 과도하게 파편화하지 않았는가
- 작품 전체 흐름을 먼저 이해할 수 있는가
- 시어/장면/표현의 해석이 원문 근거와 연결되는가
- 관찰 사실과 화자 추론이 구분되는가
- 표현법 명칭과 효과가 분리되지 않고 근거로 연결되는가
- SOURCE_TEXT_BLOCK이 실제 source와 일치하는가
- 원문이 작품 단위로 공유되고 불필요하게 반복되지 않는가

필수:
KOR_SOURCE_ACCESS
KOR_SOURCE_TEXT_FIDELITY
KOR_INTERPRETATION_GROUNDED
KOR_WORK_FLOW_INTEGRITY
KOR_SUPPLEMENT_TERMINOLOGY_MATCH

## 7. STUDENT VIEW AUDIT
편집자 metadata를 숨긴 최종 학생용 원고만 따로 읽는다.
검사 질문:
1. 한 페이지를 펼쳤을 때 '자동 생성 카드'보다 참고서 본문처럼 보이는가?
2. 박스를 제거해도 설명 흐름이 유지되는가?
3. 중요한 내용과 보조 내용의 위계가 자연스러운가?
4. 같은 서식이 계속 반복되어 다음 내용을 예측할 수 있지 않은가?
5. 학생이 실제 시험 전에 다시 읽을 가치가 있는 정보 밀도인가?

1~5 중 2개 이상 NO면 REVISE.

## 8. OUTPUT
CORE_QA_STATUS
CORE_QA_SCORE
CORE_QA_TIER
CORE_EDITORIAL_NATURALNESS
AI_PATTERN_SUSPECT
AI_PATTERN_FLAGS[]
REDUNDANCY_FLAGS[]
TRAP_EVIDENCE_CHECK
STUDENT_METADATA_LEAK
SOURCE_GROUNDED
SUBJECT_SPECIFIC_QA

END ARC CORE QA BENCH V1.0

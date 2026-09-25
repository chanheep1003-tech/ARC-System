# ARC CORE QA BENCH V1.2
VERSION: 1.2
DATE: 2026-09-19
STATUS: ACTIVE-DEV
ROLE: ARC CORE 세트 단위 품질·편집 자연스러움 검수

## 0. PURPOSE
CORE가 정보는 맞지만 'AI가 자동 생성한 요약 카드'처럼 보이는 문제를 차단한다.
개념 정확성, 학교자료 충실도, 학습 효율, 편집 자연스러움을 함께 검사한다.

## 1. HARD FAIL
하나라도 발생하면 CORE_QA=FAIL:
- chapter/cluster backbone 없이 concept notes가 나열식으로 이어짐
- 동일 facts가 prose + table + summary + diagram에서 기능 변화 없이 3회 이상 반복
- chapter ending이 synthesis가 아니라 앞 내용의 재목록에 불과함
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
- HIGH_DIFFICULTY를 이유로 범위 밖 상위과정/배경지식을 필수화
- DEPTH_EVIDENCE 없이 concept를 HIGH_DIFFICULTY로 승격
- HIGH_DIFFICULTY인데 설명만 길어지고 실제 판단축/조건/경계가 늘지 않음

## 2. SCORE — 100
SOURCE_AND_SCOPE_FIDELITY /20
CONCEPT_COMPLETENESS /15
MACRO_COHERENCE /20
EDITORIAL_NATURALNESS /15
STUDENT_USEFULNESS /15
CONFUSING_TRAP_QUALITY /5
VISUAL_FUNCTION /5
METADATA_HYGIENE /5

DEPTH 관련 항목은 CONCEPT_COMPLETENESS / STUDENT_USEFULNESS / SOURCE_AND_SCOPE_FIDELITY에 반영한다.

92~100 = CORE_A
86~91 = CORE_B
80~85 = REVISE
79 이하 = FAIL
HARD FAIL은 점수와 무관하게 FAIL.

## 3. MACRO ARCHITECTURE BENCH
각 chapter/cluster를 다음 질문으로 검사한다.

1. 이 chapter가 답하는 CENTRAL_QUESTION이 명확한가?
2. 3~6개 backbone node가 하나의 흐름으로 이어지는가?
3. 세부 날짜/인물/용어가 backbone 안에 위치하는가?
4. dominant organization(시간/인과/비교/문제-해결/구조/작품/기제)이 보이는가?
5. 표/박스/도식이 본문을 보조하는가, 아니면 본문을 대체하는가?
6. chapter 끝 synthesis가 관계를 압축하는가?
7. 다음 chapter와의 연결이 자연스러운가?

Required:
CHAPTER_BACKBONE_PRESENT = PASS
DOMINANT_ORGANIZATION_CLEAR = PASS
INFORMATION_HIERARCHY = PASS
ANTI_LISTING = PASS
REDUNDANCY_BUDGET = PASS
SYNTHESIS_TRANSFORMS = PASS

다음 중 하나면 MACRO_COHERENCE=FAIL:
- 3개 이상 연속 section이 주로 bullet inventory
- 동일한 block sequence가 3개 chapter 이상 반복
- chapter 끝에 시간축+요약 bullet+문제 적용+도식을 매번 모두 배치
- 제목을 제거하면 section 관계를 복원하기 어려움

## 4. EDITORIAL NATURALNESS SENTINELS
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

## 5. REDUNDANCY AUDIT
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

## 6. TRAP AUDIT
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

## 6-A. DEPTH AUDIT
모든 concept:
DEPTH_PRIORITY
DEPTH_REASON[]
DEPTH_EVIDENCE[]
DEPTH_AXES[]
를 검사한다.

필수:
DEPTH_ASSIGNMENT = PASS
DEPTH_EVIDENCE = PASS
DEPTH_SCOPE_SAFETY = PASS
DEPTH_BUDGET = PASS

HIGH_DIFFICULTY concept 추가:
HIGH_DIFFICULTY_COMPLETENESS = PASS

검사:
- 사용자가 지정한 고난도 영역이 실제 범위에 있으면 우선 반영했는가
- 학교자료/기출/QA evidence 없이 임의 승격하지 않았는가
- 조건/경계/혼동축/복수판단 중 실제 필요한 축이 추가되었는가
- 범위 밖 지식으로 설명 길이만 늘리지 않았는가
- 동일한 '심화' 서식을 반복하지 않았는가
- STANDARD concept까지 불필요하게 장문화하지 않았는가

DEPTH_BUDGET_FAIL:
- 세트 대부분이 HIGH_DIFFICULTY가 되어 기본 개념 복습성이 사라짐
- 모든 concept에 비교표/TRAP/적용을 억지로 추가
- 고난도 영역 때문에 주변 concept까지 과잉 설명

## 7. KOREAN CORE BENCH
국어는 추가 검사:
- 학교 보충자료의 해석 순서/용어가 반영되는가
- 작품을 주제/정서/표현법 카드로 과도하게 파편화하지 않았는가
- 작품 전체 흐름을 먼저 이해할 수 있는가
- 시어/장면/표현의 해석이 원문 근거와 연결되는가
- 관찰 사실과 화자 추론이 구분되는가
- 표현법 명칭과 효과가 분리되지 않고 근거로 연결되는가
- SOURCE_TEXT_BLOCK이 실제 source와 일치하는가
- 원문이 작품 단위로 공유되고 불필요하게 반복되지 않는가

추가:
- 보충자료 중심 요청이면 교과서 재요약보다 보충자료 해석·비교축이 실제 본문 중심인가
- 보충자료의 세부 강조를 교과서 일반론으로 덮어쓰지 않았는가
- 교과서 내용은 기초/빈틈 보완 역할에 머무르는가

필수:
KOR_SOURCE_ACCESS
KOR_SOURCE_TEXT_FIDELITY
KOR_INTERPRETATION_GROUNDED
KOR_WORK_FLOW_INTEGRITY
KOR_SUPPLEMENT_TERMINOLOGY_MATCH

## 7-A. SUBJECT DEPTH SENTINELS
### SOCIAL
칸트·베카리아 형벌/사형 논쟁이 범위에 있으면:
- HIGH_DIFFICULTY 우선 처리 여부
- 정당화 근거/목적/책임/비례성/사회계약/비판 범위 중 실제 source가 다루는 축을 충분히 반영
- CLAIM FIDELITY 유지
- 찬반 암기표로 축소하지 않음

### SCIENCE
OR 산화·환원 또는 EM 전자기 유도가 범위에 있으면:
- HIGH_DIFFICULTY 우선 처리 여부
- SCIENCE_MASTER 범위 안에서만 깊이 확장
- OR: 반응성/전자 이동/이온 수/입자/완결/그래프/질량 변화 조건 중 source 관련 축 확인
- EM: 상대 운동/방향/속력/감은 수/회로 상태/발전/시간 변화 중 source 관련 축 확인
- ADVANCED LEAK BLOCK 위반 0

### HISTORY
사전 HIGH_DIFFICULTY 강제 금지.
HISTORY_DIFFICULTY_SIGNAL을 cluster별로 확인한다.
- 유사 단체/정책
- 결성·분화·통합
- 겹치는 시기
- 세력 관계
- 사료 주체 추론
- 지도/지역 결합
- 인물의 복수 활동

evidence가 충분한 cluster만 ADVANCED/HIGH_DIFFICULTY로 승격한다.

## 8. STUDENT VIEW AUDIT
편집자 metadata를 숨긴 최종 학생용 원고만 따로 읽는다.
검사 질문:
1. 한 페이지를 펼쳤을 때 '자동 생성 카드'보다 참고서 본문처럼 보이는가?
2. 한 chapter를 읽고 난 뒤 3~6개의 큰 구조가 기억되는가?
3. 박스를 제거해도 설명 흐름이 유지되는가?
4. 중요한 내용과 보조 내용의 위계가 자연스러운가?
5. 같은 서식이 계속 반복되어 다음 내용을 예측할 수 있지 않은가?
6. 학생이 실제 시험 전에 다시 읽을 가치가 있는 정보 밀도인가?
7. summary가 앞 내용의 복사가 아니라 구조를 압축하는가?

1~7 중 2개 이상 NO면 REVISE.

## 9. OUTPUT
CORE_QA_STATUS
CORE_QA_SCORE
CORE_QA_TIER
CORE_EDITORIAL_ARCHITECTURE
MACRO_COHERENCE
CHAPTER_BACKBONE_PRESENT
DOMINANT_ORGANIZATION_CLEAR
INFORMATION_HIERARCHY
ANTI_LISTING
REDUNDANCY_BUDGET
SYNTHESIS_TRANSFORMS
CORE_EDITORIAL_NATURALNESS
AI_PATTERN_SUSPECT
AI_PATTERN_FLAGS[]
REDUNDANCY_FLAGS[]
TRAP_EVIDENCE_CHECK
STUDENT_METADATA_LEAK
SOURCE_GROUNDED
DEPTH_ASSIGNMENT
DEPTH_EVIDENCE
DEPTH_SCOPE_SAFETY
DEPTH_BUDGET
HIGH_DIFFICULTY_COMPLETENESS
SUBJECT_SPECIFIC_QA

END ARC CORE QA BENCH V1.2

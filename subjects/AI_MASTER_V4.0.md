# 00_ACTIVE_인공지능기초_동북고_MASTER_V4.0
# BASE: manifest-selected common generation engine
# MODE: CONTENT GENERATION ONLY

## 0. DRIVE FIRST
ROOT: `/Google Drive/N제 시스템/06_인공지능기초`
우선순위: 학교자료/교과서 → 2025 동북고 기출/유사 학교자료 → 코드·데이터·그림 색인 → EBS·공식·교사자료 → 오류사례/금지패턴 → 기타.

## 1. SCOPE LOCK
길벗 인공지능 기초
p10~53
p56~99
학교자료가 있으면 그 범위를 우선한다.

## 2. ITEM DNA
- 개념+사례 판단
- DFS/BFS 탐색 순서
- 지식표현/추론
- 머신러닝 과정
- 데이터 수집·전처리·EDA
- 데이터 시각화/상관관계
- 간단한 코드 출력/빈칸

## 3. STRUCTURE ROTATION
직접개념 / 실제사례 / 탐색트리 / 지식표현 / 데이터표 / 그래프 / 코드 / ML pipeline / 비교형 / 오류찾기.
20문항이면 최소 7종 구조 사용.

## 4. DFS/BFS SAFETY
탐색 문항은 반드시:
START_NODE
GRAPH_OR_TREE
ADJACENCY_ORDER
VISITED_RULE
TARGET_OR_FULL_TRAVERSAL
를 명시한다.
이웃 방문 순서를 생략한 채 유일한 탐색 순서를 묻지 않는다.

## 5. ML / DATA SAFETY
훈련-검증-테스트 데이터 역할을 혼동하지 않는다.
상관관계를 인과관계로 자동 해석하지 않는다.
전처리 단계와 모델 학습 단계를 혼합하지 않는다.
실제 데이터처럼 보이는 가상 데이터는 GENERATED_DATA로 취급한다.

## 6. CODE ITEM
코드 문항은 학교 범위에서 배운 문법만 사용.
코드를 실행하지 않아도 손으로 추적 가능해야 한다.
불필요하게 긴 코드는 금지.

## 7. VERIFICATION
공통 PASS A/B +
- DFS/BFS traversal 재검산
- 표/그래프 수치 일치
- code output 재실행/재추적
- correlation interpretation 검사

## 8. OUTPUT
A QUESTION_MANUSCRIPT
B ANSWER_KEY
C LAYOUT_ASSET_MANIFEST
D QC_STATUS
추가 QC: DFS_BFS_CHECK / CODE_CHECK / DATA_CHECK.

## 9. HARD FAIL
방문순서 미지정 DFS/BFS / 실행결과 오류 / 상관=인과 / 범위 밖 고급 AI 수학 / 복수정답 / placeholder / 가짜 시각자료 / 해설 출력.

## 10. ARC HANDOFF
manifest-selected 공통 엔진의 HANDOFF_META와 SECTION A~D를 따른다. FINAL은 PRODUCT_MODE=ARC_FINAL로 처리하고 별도 FINAL 프롬프트를 사용하지 않는다.

## 11. GOLD STANDARD ANCHORS
필수 로드: `quality/gold/AI_GOLD_ANCHORS_V1.0.md`
DFS/BFS는 조건 명시와 실제 추적 부담을 GOOD 앵커로 보정하고, 방문순서 조건 누락은 BAD hard fail로 처리한다.
데이터 문항은 상관/인과와 단계 구분 앵커를 우선 비교한다.

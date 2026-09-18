# ARC_QA_BENCH_V1.2
VERSION: 1.2
DATE: 2026-09-18
ROLE: 출제 프롬프트 회귀검사·품질 비교
STATUS: ACTIVE

## 0. PURPOSE
MASTER/ENGINE/QA 변경이 실제 생성 품질을 개선했는지 동일 조건에서 비교한다.
V1.2는 자동 점수 인플레이션과 '형식상 PASS'를 차단하고, frozen regression fixture로 규칙 변경의 회귀를 검출한다.

## 1. HARD FAIL
하나라도 발생하면 FAIL:
- 범위 밖 지식이 정답에 필수
- 복수정답/정답 없음
- 정답키 불일치
- 필수 자료 누락/placeholder
- 사용 금지 범위 유입, 통합사회 C파트 X 영역 침범
- 저작권 과복제
- 데이터·그래프·입자모형 오류
- 역사 사료 주체/시기 오류
- DFS/BFS 탐색 순서 오류
- 저장/조판 handoff 필수 필드 누락
- QA 근거 없이 점수만 기입
- 자동화 실행이 산출물 없이 SUCCESS 처리

## 2. RELEASE SCORE — 100
|평가축|점수|
|---|---:|
|정확성/유일정답|25|
|범위 충실도|15|
|현재 학교자료 적합도|15|
|오답 품질|10|
|문항 구조 다양성|10|
|자료·시각 무결성|10|
|난도/변별 균형|5|
|원작성/저작권|5|
|출력·HANDOFF 무결성|5|

- 92~100 + HARD FAIL 0 = RELEASE PASS
- 87~91 + HARD FAIL 0 = RC
- 86 이하 = FAIL

과거 다른 교사 기출은 학교자료 적합도 점수의 '스타일 근거'로 쓰지 않고 난이도 calibration에만 사용한다.

## 3. EVIDENCE-BASED QA
각 점수축에 최소 1개 관찰 근거를 남긴다.
'검토 완료', 'independently checked', '적절함'만으로는 근거가 아니다.

필수 예:
- distractor_quality: '②는 원인-결과 전도, ④는 조건 누락 HALF_TRUE'
- reasoning: '자료 A에서 시기 식별 → B와 선후관계 결합의 2단계'
- school_material_fit: '현재 학습지의 표 구조를 새 데이터로 재설계'

## 4. SENTINEL RECHECK
과목별 20문항 중 최소 4문항을 독립 재검수한다.
우선순위:
1) 최고 ITEM 점수 문항
2) 최고 난도 문항
3) 자료/시각 문항
4) 가장 낮은 점수의 PASS 문항

독립 재검수 점수 차이가 6점 이상이거나 PASS/REVISE 판정이 뒤집히면 그 과목 20문항 전체를 재채점한다.

## 5. SCORE DISTRIBUTION AUDIT
다음은 회귀 FAIL 사유:
- 점수가 88/89/90/91처럼 기계적 순환
- 70% 이상 문항이 5점 폭 안에 몰림
- 모든 QUALITY_FLAGS가 비어 있음
- PREMIUM 비율이 높지만 자료/추론 근거가 없음
- D3 이상인데 1단계 직접개념 문항이 반복

## 6. FROZEN REGRESSION FIXTURES
활성 회귀셋:
- `quality/regression/ARC_REGRESSION_POLICY_V1.0.md`
- `quality/regression/REGRESSION_FIXTURES_V1.0.yaml`

총 30개: 5과목 × GOOD 3 + BAD 3.
COMMON ENGINE/MASTER/QA/난이도/Source/BANK 판정 규칙 변경 시 `arc-eval-regression`으로 전수 재평가한다.
- GOOD가 REVISE/DISCARD로 내려가면 FAIL
- BAD가 BANK_A/PREMIUM으로 올라가면 FAIL
- BAD-DISCARD가 PASS/BANK로 올라가면 FAIL
- 기대 점수 범위/상한을 3점 이상 벗어나면 drift를 기록하고 정책 기준에 따라 WARN/FAIL
- fixture 기대값을 변경하여 테스트를 통과시키는 행위 금지

## 7. GENERATIVE FIXED BENCH SET
KOR-B01 탄궁가 20: 직접확인 편중, 표현효과, HALF_TRUE
KOR-B02 팔원 15: 관찰 사실 vs 화자 추론
KOR-B03 칸트-헤겔 15: 공통점/차이, 범위 밖 철학사 금지
SCI-B01 산화환원 20: REDOX_LEDGER, 입자/질량/자료
SCI-B02 진화·생물다양성 20: 집단 변화, 자료형 비중
SCI-B03 전자기유도 15: 방향/세기/그래프
SOC-B01 C파트 20: X_MARK_FILTER
SOC-B02 B파트 20: 학습지 직접 근거, 지도/인구자료
SOC-B03 기본권·권리구제 20: 기관/절차/효과
HIS-B01 범위 종합 20: 사료/지도/연표 >=7
HIS-B02 민족주의·사회주의·민족협동전선 15
HIS-B03 사료·연표 고난도 15
AI-B01 DFS/BFS 15
AI-B02 전처리·시각화 15
AI-B03 범위 종합 20: 자료해석 >=6

## 8. AUTOMATION BENCH
자동화는 품질과 별도로 실행 내구성을 검사한다.
- RUN folder created
- SUBJECT checkpoint written after each subject
- RAW doc exists before QA starts
- QA report exists
- BANK write exists or explicit zero-pass explanation exists
- failure produces failure log
- partial completion can resume next run
- no self-optimization before item production completes

## 9. RELEASE GATE
COMMON ENGINE/QA 변경:
- 관련 5과목 최소 1 BENCH
- HARD FAIL 0
- SENTINEL RECHECK 통과
- SCORE DISTRIBUTION AUDIT 통과
- AUTOMATION BENCH 통과
- REGRESSION_FIXTURES 30개 전수 실행
- REGRESSION_FAIL_COUNT = 0

END ARC QA BENCH V1.2

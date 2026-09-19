# ARC KOREAN ITEM QA V1.0
VERSION: 1.0
DATE: 2026-09-19
STATUS: ACTIVE-DEV
ROLE: 국어 ARC_N / ARC_FINAL 전용 문항·지문군 품질 게이트

## 0. PURPOSE
국어는 지문이 좋아도 문항이 단순 확인형·중복형·정답 노출형이면 세트 품질이 급격히 떨어진다.
이 QA는 '정답이 맞다'와 '좋은 국어 문항이다'를 분리한다.

## 1. ITEM HARD FAIL
다음 중 하나면 해당 문항 REVISE/DISCARD:
- 지문을 거의 읽지 않고 작품명/갈래/라벨만으로 해결 가능하며 그 문항이 기본 확인 슬롯으로 명시되지 않음
- 정답이 지문의 한 문장을 거의 그대로 반복하고 오답 3개 이상이 즉시 제거 가능
- STRONG_DISTRACTOR_COUNT < 2인데 D3 이상으로 분류
- 정답만 의미상 필요 없이 유독 길고 구체적
- 극단 표현 하나만 보고 오답을 제거할 수 있는 선지가 3개 이상
- 같은 지문에서 기존 문항과 실질적으로 동일한 판단축/정답 논리를 재사용
- 문학 해석이 작품 내부 근거 없이 외부 지식에 의존
- 비문학 문항이 정의 문장 위치 찾기만 요구하면서 적용/추론형으로 분류됨

## 2. PASSAGE-GROUP GATE
지문군 10문항 기준 진단:
- P2+P3+P4 문항 최소 5
- 동일 REASONING_AXIS 2개 초과 금지
- direct theme/genre/definition 확인 합계 기본 3개 이하
- transfer/application 최소 2
- multi-evidence 최소 3
- 강한 오답 2개 미만 문항 비율 25% 미만

문학 추가:
- 실제 시어/행/장면 근거를 2곳 이상 결합하는 문항 최소 3

비문학 추가:
- 서로 다른 문단 2개 이상을 연결하는 문항 최소 3
- 새 사례/학생 판단/조건 적용 문항 최소 2

## 3. ANSWER-LENGTH LEAK
20문항 이상:
- 정답이 단독 최장 선지인 비율 > 50% => REVISE
- > 65% => FAIL
- 정답이 상위 2개 길이에 속하는 비율 > 75% => REVISE

문항 단위:
CORRECT_TO_MEDIAN_RATIO > 1.35 => 검토 필수.

길이를 기계적으로 동일화하지 않는다.
정답 위치와 문장 길이가 예측 신호가 되지 않게 한다.

## 4. STEM / LANGUAGE PATTERN
- 동일 stem skeleton 3연속 => FAIL
- 단일 stem skeleton 60% 초과 => REVISE
- '가장 적절한 것은?' 반복 자체보다 실제 요구 사고의 중복을 더 중요하게 본다.
- 정답만 온건한 복합문이고 오답은 모두 극단 단문이면 AI_CHOICE_PATTERN.

## 5. DUPLICATE REASONING AUDIT
지문별로 모든 문항에 ITEM_REASONING_AXIS를 부여한다.

동일 축 2개까지 허용 가능하나 둘 사이에 최소 하나가 달라야 한다:
- 근거 범위
- 요구 단계
- 적용 대상
- 비교 대상
- 조건

같은 축 + 같은 근거 + 같은 결론이면 DUPLICATE_AXIS_FAIL.

## 6. PASSAGE UTILIZATION SCORE
지문군마다 100점:
- MULTI_EVIDENCE /25
- TRANSFER_APPLICATION /20
- REASONING_DIVERSITY /20
- DISTRACTOR_COMPETITIVENESS /20
- LANGUAGE_NONLEAK /10
- SOURCE_GROUNDED /5

90+ = PASS
84~89 = REVISE
83 이하 = FAIL

단, hard fail은 점수 무관.

## 7. SET RELEASE GATE
필수:
KOR_PASSAGE_MAP = PASS
KOR_PASSAGE_UTILIZATION = PASS
KOR_REASONING_DIVERSITY = PASS
KOR_DUPLICATE_AXIS = PASS
KOR_DISTRACTOR_COMPETITIVENESS = PASS
KOR_ANSWER_LENGTH_AUDIT = PASS
KOR_STEM_DIVERSITY = PASS
KOR_ANSWER_PATTERN = PASS
KOR_SOURCE_TEXT_FIDELITY = PASS when applicable

하나라도 FAIL이면 CONTENT_QA_STATUS=PASS 금지.

## 8. CURRENT FAILURE SENTINELS
다음 유형은 특히 재발 방지한다:
- 같은 지문에서 주제/정서/태도 문항을 표현만 바꿔 반복
- 관찰과 추론 구분을 3문항 이상 반복
- 비문학 10문항 중 대부분이 문장 직접 찾기
- 정답 선지가 거의 항상 가장 길고 상세함
- ①②③④⑤가 5문항 단위로 순환
- 오답이 '모두/완전히/오직/무조건' 같은 단어만으로 탈락

## 9. INTERNAL REPORT
PASSAGE_ID별:
ITEM_COUNT
PASSAGE_USE_DISTRIBUTION
REASONING_DEPTH_DISTRIBUTION
REASONING_AXIS_DISTRIBUTION
DIRECT_LOOKUP_COUNT
MULTI_EVIDENCE_COUNT
TRANSFER_COUNT
STRONG_DISTRACTOR_DEFICIT_ITEMS
ANSWER_LENGTH_FLAGS
STEM_PATTERN_FLAGS
DUPLICATE_AXIS_FLAGS
PASSAGE_UTILIZATION_SCORE

학생용 출력 금지.

END ARC KOREAN ITEM QA V1.0

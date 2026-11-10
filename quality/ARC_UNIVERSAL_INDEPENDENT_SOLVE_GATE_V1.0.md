# ARC UNIVERSAL INDEPENDENT SOLVE & DIFFICULTY GATE V1.0
VERSION: 1.0
DATE: 2026-09-21
STATUS: ACTIVE-DEV
SCOPE: KOR / SOC / HIS / SCI / AI · ARC_N / ARC_FINAL

## 0. PURPOSE
출제자의 의도와 정답을 보지 않은 독립 재풀이를 모든 과목의 공통 QA 허브로 사용한다.
단순히 PASS A/B 정답 번호만 맞추지 않고, 전 선지 판정·근거·범위·실제 난도를 구조화해 CONTENT_LOCK 전에 검증한다.

## 1. CANONICAL ORDER
GENERATION
→ STRUCTURAL GATES
→ PASS A AUTHOR SOLVE
→ PASS B BLIND INDEPENDENT SOLVE
→ A/B ANSWER MATCH
→ ALL-OPTION VERDICT AUDIT
→ OPTION SEMANTIC DUPLICATION REVIEW
→ ANSWER EVIDENCE TRACE
→ SCOPE EVIDENCE TRACE
→ ACTUAL DIFFICULTY RECLASSIFICATION
→ SET-LEVEL DIFFICULTY / STRUCTURE AUDIT
→ CONTENT_LOCK

PASS B는 ANSWER_KEY, PASS A 풀이, 출제 의도, 목표 난도 라벨을 보지 않는다.
동일 모델을 쓰더라도 새 컨텍스트에서 위 정보를 제외해야 한다.

## 2. PER-ITEM QA EVIDENCE
각 문항은 내부 QA_EVIDENCE에 최소 다음을 기록한다.

- ITEM_ID / SUBJECT / ITEM_FORMAT
- TARGET_DIFFICULTY
- PASS_A.ANSWER / PASS_A.ANSWER_EVIDENCE
- PASS_B.ANSWER / BLIND=true / EXCLUDED_INPUTS
- PASS_B.CONFIDENCE
- PASS_B.ANSWER_EVIDENCE
- PASS_B.SCOPE_TRACE = IN_SCOPE + SOURCE_REFS
- 모든 선지의 OPTION_ID / VERDICT / CLAIM_KEY / AXIS / EVIDENCE_REFS / COMPETITIVENESS
- SECOND_BEST_OPTION / SECOND_BEST_RISK
- REASONING_STEPS / EVIDENCE_COUNT / IMMEDIATE_ELIMINATION_COUNT / TRANSFER_REQUIRED
- ACTUAL_DIFFICULTY
- FACTUAL_ACCURACY_REVIEW
- OPTION_SEMANTIC_DUPLICATION_REVIEW
- ANSWER_EVIDENCE_TRACE
- SCOPE_EVIDENCE_TRACE
- ALL_OPTION_AUDIT
- UNIQUE_ANSWER
- DIFFICULTY_MATCH

선지 VERDICT:
TRUE | FALSE | HALF_TRUE | UNSUPPORTED

5지선다에서는 TRUE가 정확히 1개이며 PASS A/B 정답과 같아야 한다.
HALF_TRUE와 UNSUPPORTED는 왜 전체 명제로 거짓인지 근거를 남긴다.

## 3. SEMANTIC DUPLICATION
문자열 유사도가 아니라 `AXIS + CLAIM_KEY + EVIDENCE`를 비교한다.

다음 중 하나면 REVISE:
- 정답과 사실상 같은 뜻의 다른 선지
- 두 오답이 같은 판단을 표현만 바꿔 반복
- 한 선지가 다른 선지를 포함해 둘 다 참으로 읽힐 위험
- 서로 다른 번호인데 AXIS와 CLAIM_KEY가 동일

Runner는 구조화된 중복 key와 필수 근거 누락을 잡는다.
최종 의미 동일성은 독립 reviewer가 판정하며 자동 PASS만으로 대체하지 않는다.

## 4. EVIDENCE AND SCOPE
독립 재풀이의 정답은 source 근거 없이 확정할 수 없다.

과목별 최소 근거:
- KOR: 원문 행·연·문단, 학교 학습활동 또는 허용된 교과서/보충자료 위치
- SOC: 교과서·학습지 개념, 사상가의 실제 주장·정당한 함의
- HIS: 사료 주체·시기·사건·인과 또는 지도/연표 위치
- SCI: 개념·실험 조건·표/그래프·계산 또는 보존 관계
- AI: 교과 개념·알고리즘 조건·자료/코드 실행 규칙

정답 근거와 범위 근거는 분리 기록한다.
PASS A/B가 같은 잘못을 공유할 수 있으므로 A/B 일치만으로 FACTUAL_ACCURACY_REVIEW를 PASS하지 않는다.

## 5. DIFFICULTY DURING PASS B
난도는 출제 라벨이 아니라 독립 재풀이의 실제 해결 부담으로 재판정한다.

PASS B 실측값:
- REASONING_STEPS
- EVIDENCE_COUNT
- IMMEDIATE_ELIMINATION_COUNT
- STRONG_DISTRACTOR_COUNT
- SECOND_BEST_RISK
- TRANSFER_REQUIRED
- ACTUAL_DIFFICULTY

CONTENT_LOCK 전 TARGET_DIFFICULTY와 ACTUAL_DIFFICULTY를 일치시킨다.
불일치하면 문항을 수정해 A/B부터 다시 실행하거나 난도 메타를 재분류한다.

D4 최소:
- REASONING_STEPS >= 2
- STRONG_DISTRACTOR_COUNT >= 2
- IMMEDIATE_ELIMINATION_COUNT <= 2

D5 최소:
- REASONING_STEPS >= 3
- STRONG_DISTRACTOR_COUNT >= 2
- EVIDENCE_COUNT >= 2
- IMMEDIATE_ELIMINATION_COUNT <= 1

장문·어려운 용어·불필요한 계산·범위 밖 지식은 난도 근거가 아니다.

## 5A. BLIND ROUND POLICY (2026-09-25 사용자 지시)
- 블라인드 독립 풀이는 번들당 1회만 진행한다. 모든 제품과 파이프라인에 적용된다(`runtime.blind_review_rounds: 1`).
- 풀이자는 새 컨텍스트에서 원고만 받는다. 정답, 작성 의도, 목표 난도는 주지 않는다.
- 블라인드 결과로 드러난 문제는 저자가 수정하되, 재블라인드 없이 `post_blind_edits`에 기록한다. 정답 불일치 문항은 수정 근거를 남기고 보고서에 명시한다.
- `blind_review.yaml`의 `rounds`는 1이어야 한다. 그 밖의 값은 `BLIND_ROUND_POLICY_VIOLATION`(FAIL)이다. 정책 이전 번들만 `round_policy_exemption`으로 WARN 처리한다.

## 6. SET GATES
다음 8개 현행 gate는 전부 PASS여야 한다.

- STRUCTURE
- ANSWER_COUNT_MATCH
- MANUSCRIPT_CONTAMINATION
- TOO_EASY
- MID_GAP
- STRUCTURE_BIAS
- D4_SHORT
- PASSAGE_TRUNCATION

추가 의미 gate:
- FACTUAL_ACCURACY_REVIEW
- OPTION_SEMANTIC_DUPLICATION_REVIEW
- ANSWER_EVIDENCE_TRACE
- SCOPE_EVIDENCE_TRACE
- ALL_OPTION_AUDIT

## 7. KOREAN EXACT SOURCE LOCK
국어 SOURCE_TEXT_BLOCK은 사용자가 제공한 교과서·학교 보충자료·업로드 또는 연결 Drive의 RAW SCHOOL SOURCE만 허용한다.

허용 origin:
- USER_UPLOAD
- USER_PROVIDED_SCHOOL_SUPPLEMENT
- USER_PROVIDED_TEXTBOOK
- CONNECTED_DRIVE_RAW_SCHOOL_SOURCE

금지 origin:
- WEB_SEARCH / SEARCH_SNIPPET / UNVERIFIED_EXTERNAL / UNKNOWN
- ARC_N_OUTPUT / ARC_FINAL_OUTPUT / ARC_CORE_OUTPUT
- GENERATED_MANUSCRIPT / VERIFIED_BANK / DEEP_RESEARCH / EXTERNAL_PROBLEM_BOOK

필수:
- SOURCE_ROLE=RAW_SCHOOL_SOURCE
- TEXT_FIDELITY=EXACT
- SOURCE_FILE_ID
- SOURCE_LOCATION
- SOURCE_TEXT_SHA256
- wording / punctuation / line-break / stanza-or-paragraph boundary lock

WHITESPACE_NORMALIZED는 학생용 원문에 사용 금지한다.
시의 행·연이 공간에 맞지 않으면 원문을 고치지 않고 조판을 재배치한다.

## 8. EXECUTABLE GATE
Runner:
`tooling/content_qa/content_qa_gate.py`

입력:
`quality/semantic/ARC_QA_EVIDENCE_SCHEMA_V1.0.yaml`에 맞춘 YAML 또는 JSON QA evidence.

Runner가 PASS해도 사실·해석의 의미적 진실성이 자동 보장되는 것은 아니다.
Runner는 독립 검수 기록의 완결성, A/B 일치, 유일정답, 선지 key 중복, 근거·범위 trace, 난도 최소조건, 국어 source provenance를 강제한다.

## 9. RELEASE AUTHORITY
CONTENT_LOCK은 이 gate PASS 뒤에만 가능하다.
READY_FOR_TYPESET은 CONTENT_LOCK 뒤에 가능하다.
FINAL_RELEASED는 실제 산출물을 검토한 인간만 선언한다.

END ARC UNIVERSAL INDEPENDENT SOLVE & DIFFICULTY GATE V1.0

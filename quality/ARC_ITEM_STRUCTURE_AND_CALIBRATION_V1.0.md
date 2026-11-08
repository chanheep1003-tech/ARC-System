# ARC N 문항 구조·난이도 측정 규칙 V1.0 (D-22 / D-23)

사용자 결정(2026-11-08): S2 20문항 실험(KOR v4, SCI v2, SOC v1~v3)이 난이도 게이트를 통과하지 못했고, 원인이 문항 소재보다 설계·측정 방식에 있어 시스템을 수정한다.
적용 범위: ARC_N 의 KOR / SOC / SCI. ARC_FINAL 은 기존 앵커 방식 그대로다.

## 1. 출제 구조 라이브러리 (`quality/exam_style/EXAM_STRUCTURE_LIBRARY_V1.0.yaml`)
- 모든 ARC_N 문항은 `template` 코드를 기록한다(SOC: T1~T15, SCI: S1~S11, KOR: K1~K13). 코드가 없거나 라이브러리에 없으면 FAIL(TEMPLATE_MISSING / TEMPLATE_UNKNOWN).
- 문항의 난이도 라벨은 그 템플릿이 허용하는 범위 안이어야 한다(TEMPLATE_DIFFICULTY_OUT_OF_RANGE).
- 구조 점수(structure score): 풀이 단계(최대 5), 표·도식, 4줄 이상 자료, 판단 진술 3개/4개 이상, 비교 대상 수, 계산 템플릿(+2), 즉시 소거 가능 선지 ≤1 을 더한다. 밴드는 D2 ≤6, D3 ≤9, D4 >9.
  라벨이 D4 인데 구조 밴드가 D3 이하이면 FAIL(STRUCTURE_BAND_BELOW_LABEL), 라벨이 D3 인데 밴드가 D2 이면 WARN.
- 밴드 경계는 SOC S2 v1~v3 60문항에서 구조 밴드와 AI 풀이자 라벨의 일치율 46/60 (77%) 로 정한 잠정값이다. v3 의 D4 라벨 6문항 중 5문항은 풀이 평가 전에 구조 점수로 예측된 대로 D3 이하였다.
- 구조 분포가 사용자 목표 ±허용치 밖이면 WARN(STRUCTURE_DISTRIBUTION_OFF_TARGET) — 풀이 평가를 돌리기 전 사전 점검이다.

## 2. 난이도 측정 보정 (`quality/anchors/CALIBRATION_ANCHOR_REGISTRY_V1.0.yaml`, `tooling/production/difficulty_calibration.py`)
- 풀이 평가 원고 끝에 기준 문항 `ANCHOR-<id>` 를 붙여 같은 풀이자가 풀게 한다. 기준 문항은 출판사 난이도 라벨(하/중/중상/상)이 있는 모의고사 문항이다. 원문은 저작물이라 저장소에 넣지 않고 Drive 위치만 등록한다.
- 기준 문항이 4개 이상이고 낮은 라벨과 높은 라벨이 모두 있으면 풀이자의 평균 오차(offset)를 계산해 SOLVER_LENIENT / SOLVER_HARSH / CALIBRATED 로 표시하고 보정 분포를 같이 보고한다. 부족하면 INSUFFICIENT_ANCHORS 이고 보정값을 적용하지 않는다(파이프라인 게이트 DIFFICULTY_MEASUREMENT=WARN).
- 구조 밴드와 풀이자 평가가 한 단계 이상 다른 문항은 사람이 확인할 대상으로 보고한다(`structure_solver_mismatch`).
- 한계: 라벨은 학생 정답률이 아니다. 실제 정답률 자료가 생기면 재보정한다.

## 3. 요청 전 가능성 점검 (`feasibility`)
- 요청에 `scope_profile.subunit_count`(범위의 소단원 수)를 기록한다. 없으면 WARN(REQUEST_SCOPE_PROFILE_MISSING).
- D4+ 목표가 cap(소단원 1개 10% + 추가 소단원당 10%, 최대 40%) + 허용치를 넘으면 REQUEST_SPEC 게이트에서 FAIL 하고 사용자에게 (1) 범위 확대 (2) D4+ 하향 (3) 그대로 진행 중 하나를 묻는다. 그대로 진행하면 `request_spec.feasibility_acknowledged_by: USER` 를 기록한다.
- 근거: SOC S2 한 소단원으로 세 번 만들어도 D4 가 0개였다. cap 은 잠정값이다.

## 4. 자동 검사 (`tooling/production/item_structure_gate.py`)
- LENGTH_CUE_ANSWER_LONGEST: 정답 선지가 가장 길고 오답 평균의 1.25배 초과(FAIL), 1.15배 초과(WARN). ㄱㄴㄷ·㉠~㉤ 같은 기호 선지는 제외.
- ABSOLUTE_WORD_CUE: 정답에는 없고 오답 3개 이상에 절대 표현(언제나, 어떤 경우에도, 반드시, 오직, 전혀, 절대, 얼마든지, 무조건, 항상, 순전히)이 있으면 FAIL, 2개면 WARN. 보기 진술의 절대 표현은 WARN.
- ANSWER_POSITION_BIAS / ANSWER_POSITION_RUN: 한 번호가 ceil(n/5)+1 개 초과이거나 같은 번호가 3번 연속이면 FAIL.
- TEXTBOOK_COPY: 교과서 원문(source_texts)과 14자 조각이 60% 이상 겹치는 선지·보기는 FAIL(D-21). 원문을 주지 않으면 WARN(TEXTBOOK_COPY_UNCHECKED).

## 5. 파이프라인 연결
- `production_pipeline.run()`: REQUEST_SPEC 단계에서 feasibility FAIL 을 확인하고, SOC/SCI(및 template 코드를 쓰는 KOR) ARC_N 은 EXAM_SCOPE·GENERATION_SOURCE_MIX 다음에 ITEM_STRUCTURE 게이트를 실행한다. 보고서에 `item_structure`, `difficulty_calibration` 이 포함된다.
- 사용법: `python tooling/production/item_structure_gate.py <items.yaml> [교과서 원문.txt ...]`, `python tooling/production/difficulty_calibration.py <blind_output.yaml>`.

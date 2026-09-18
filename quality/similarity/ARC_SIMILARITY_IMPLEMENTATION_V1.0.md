# ARC SIMILARITY IMPLEMENTATION V1.0
VERSION: 1.0
DATE: 2026-09-18
STATUS: ACTIVE-DEV

## PURPOSE
AI의 서술형 유사도 판단에 정량 semantic similarity를 추가한다.

## TOOLCHAIN
- sentence-transformers
- Qdrant local mode
- `tooling/similarity/arc_similarity.py`
- `tooling/similarity/calibrate_similarity.py`

## EMBEDDING AXES
각 문항을 최소 3개 vector로 저장:
- FULL_ITEM
- STEM
- DISTRACTORS

구조 메타데이터도 함께 저장:
CONCEPT_ID, QUESTION_FORM, REASONING_FORM, CONDITION_PATTERN, ANSWER_PATH, VISUAL_TEMPLATE.

## MODEL
기본은 한국어를 포함하는 multilingual sentence-transformers 모델.
실행 시 `--model` 또는 환경변수로 교체 가능.
모델 변경 시 threshold 재보정.

## QDRANT
로컬 path 기반 persistent Qdrant를 기본으로 한다.
BANK 원문 전체를 외부 서비스에 전송하지 않는다.

## CALIBRATION
임계값을 임의로 고정하지 않는다.
실제 BANK에서 LOW/MEDIUM/HIGH/DUPLICATE 라벨쌍을 만든 뒤 calibrate script로 threshold를 생성한다.
`SIMILARITY_THRESHOLDS_V1.0.yaml`이 CALIBRATED가 되기 전에는 cosine score는 advisory이며 기존 structural guard를 대체하지 않는다.

## FINAL RISK
CALIBRATED 이후:
- semantic vector scores
- structural match count
- recent bank/product reuse
를 결합해 LOW/MEDIUM/HIGH/CRITICAL 판정.

CRITICAL은 폐기.
HIGH는 재설계 원칙.
정량 score 하나만으로 copyright/duplication을 확정하지 않는다.

END ARC SIMILARITY IMPLEMENTATION V1.0

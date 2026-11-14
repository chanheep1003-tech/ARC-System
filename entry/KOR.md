# KOR 진입 파일 — 국어 작업일 때만 읽는다

경로는 항상 `SYSTEM_MANIFEST.yaml`에서 확인한다. 아래는 2026-11 기준 활성 경로다.

## 필수 로드
- 버전 정책 V1–V6: `quality/korean/ARC_KOR_V1_V6_LEVEL_POLICY_V1.2.md` (옛 V1–V5 사다리는 보관본)
- 동적 자료 선택: `quality/korean/ARC_KOR_DYNAMIC_SOURCE_SELECTION_V1.0.yaml` (미리 정한 작품 목록 없음)
- 문법 원형: `quality/korean/ARC_KOR_GRAMMAR_ARCHETYPES_V1.0.yaml` → 게이트 `python tooling/korean/archetype_gate.py <번들>/items.yaml`
- 과목 MASTER: manifest `subjects` 항목의 KOR 경로

## 버전 규칙 (국어 전용, 다른 과목은 상속하지 않음)
- V1–V4 = ARC_N, V5 = ARC_FINAL, V6 = ARC_N 맞춤법·띄어쓰기 특화.
- V3 낯선 자료는 갈래마다 다르다: 문학은 새 작품 비교, 비문학은 새 개념 설명·비교, 문법은 실제 새 용례(허락되면 노래 가사·시·소설 포함).
- 출처 원문이나 저작권이 확인되지 않으면 BLOCKED.

## V6 (현대 국어 맞춤법)
- 정책: `quality/korean/ARC_KOR_V6_UNFAMILIAR_EXPRESSION_ORTHOGRAPHY_V1.0.md`
- 문법 규칙을 먼저 고정하고, 문항마다 낯선 어휘·관용구·문장을 고른다. 품사 / 사전 사실 / 정식 규정을 구분한다.
- 정답을 모르는 독립 풀이, 모든 선지 진위 점검, 새로움·저작권 기록이 필요하다.
- 정책 파일이 있다고 해서 100문항이 만들어졌다고 말하지 않는다.

## 2026-11-05 교정 패치 (N° 맞춤법·중세 국어 검토 시)
- `quality/korean/ARC_KOR_NORM_20261105_CORRECTION_POLICY.md`를 추가로 읽는다.
- 부정 발문은 FALSE 답이 정확히 하나여야 한다.
- 정적 PDF PASS는 내용 확정이 아니다. 원본, 대기 중 패치, 검토 영수증을 따로 보존한다.

## 중세 국어 (사용자가 명시적으로 요청할 때만)
- manifest `runtime.korean_middle_korean_policy`와 그 회귀 파일을 읽는다.

## 출제자 시선 (전 과목 공통)
- `quality/ARC_EXAMINER_LENS_V1.1.md` — 내신 출제 순서(§1~§5) + 변별 4단계 RECALL/APPLY/INFER/EXTEND(§6~§7).
- 이 과목의 새 자료 만드는 법: 같은 문서 §8 국어.

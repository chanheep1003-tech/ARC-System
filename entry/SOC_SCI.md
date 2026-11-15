# SOC · SCI 진입 파일 — 사회·과학 작업일 때만 읽는다

- 과목 MASTER: manifest `subjects` 항목의 SOC / SCI 경로. MASTER의 SCOPE LOCK(중간고사 범위)은 `ops/exams/DONGBUK_2026_2_FINAL_SCOPE_NOTICE.yaml`로 대체된다.
- 기본 문항 수 20. 버전 사다리(V1–V6)는 국어 전용이며 상속하지 않는다.
- 자료(표·그래프·그림)는 공유 렌더러를 쓴다: `tooling/typeset/` (임의 조판 코드 작성 금지).

## 출제자 시선 (전 과목 공통)
- `quality/ARC_EXAMINER_LENS_V1.3.md` — 내신 출제 순서(§1~§5) + 변별 4단계(§6~§7) + 난도↔유형 연결(§13: D4는 추론·심화, D5는 심화).
- 이 과목의 새 자료 만드는 법: 같은 문서 §8 사회·과학.

## ARC FINAL (실전 모의고사)
- `quality/ARC_FINAL_QUALITY_GATE_V1.2.md` — 학교 수준(STANDARD, 기본) / 심화판(ADVANCED, 평균 3.0~3.5). 사회 22+2문항(90/10점, A 7+1 · B 7+1 · C 8, 문항마다 part), 학교 수준 2.87 ± 0.22 / 과학 24+4문항(80/20점, A~D part), 학교 수준 2.53 ± 0.22.
- `arc.py plan --product ARC_FINAL --edition 학교수준|심화판`, `arc.py scaffold --product ARC_FINAL`(final_gate·final_edition·points·part 필드 포함).
- **출제 스타일 프롬프트**(N°·FINAL 출제 전 먼저 읽기): 사회 `quality/style/ARC_STYLE_PROMPT_SOC_V1.0.md`, 과학 `quality/style/ARC_STYLE_PROMPT_SCI_V1.0.md`.

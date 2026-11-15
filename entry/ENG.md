# ENG 진입 파일 — 영어 작업일 때만 읽는다

- 문항 유형은 `quality/english/ARC_ENG_EXAM_TYPES_V1.0.yaml`의 코드에서만 고른다. 게이트: `python tooling/english/exam_type_gate.py <번들>/items.yaml`
- ARC N° 1세트 = 어휘 15 + 어법 10 + 독해 15 + 서답형 10. ARC FINAL = 38문항(선택형 34 + 서답형 4).
- 과목 MASTER: manifest `subjects` 항목의 ENG 경로.
- 버전 사다리(V1–V6)는 국어 전용이다. 영어에는 없다.

## 출제자 시선 (전 과목 공통)
- `quality/ARC_EXAMINER_LENS_V1.3.md` — 내신 출제 순서(§1~§5) + 변별 4단계(§6~§7) + 난도↔유형 연결(§13: D4는 추론·심화, D5는 심화).
- 이 과목의 새 자료 만드는 법: 같은 문서 §8 영어.

## ARC FINAL (실전 모의고사)
- `quality/ARC_FINAL_QUALITY_GATE_V1.2.md` — 학교 수준(STANDARD, 기본) / 심화판(ADVANCED, 평균 3.0~3.5). 영어 34+4문항(80/20점, 1~10번 어휘 각 1점, 번호·유형은 arc_final_blueprint), 난도 기준은 잠정(LOW) 2.85 ± 0.30.
- `arc.py plan --product ARC_FINAL --edition 학교수준|심화판`, `arc.py scaffold --product ARC_FINAL`(final_gate·final_edition·points·part 필드 포함).

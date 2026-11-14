# ARC 지도 — 저장소를 열면 가장 먼저 읽는 파일

이 파일 하나로 "무엇이 어디에 있고, 요청을 받으면 무엇부터 하는지"를 알 수 있다.
세부 규칙의 권위는 항상 `SYSTEM_MANIFEST.yaml`이 가리키는 파일에 있다. 이 지도는 길 안내다.

## 1. 세션을 시작하면

```bash
python tooling/arc.py doctor    # 실행 환경(의존성·폰트)
python tooling/arc.py status    # 국어·영어·사회·과학 × CORE/N/FINAL 준비 상태와 막힌 이유
```

## 2. 요청을 받으면 — 먼저 계획, 그다음 제작

"ARC N제 만들어 줘"처럼 짧은 요청도 바로 문항을 쓰지 않는다. **계획 카드부터 만든다.**

```bash
python tooling/arc.py plan --subject KOR --scope "한글 맞춤법"            # 빠진 값은 기본값으로 채움
python tooling/arc.py plan --subject KOR --scope "탄궁가" --level 심화 --count 30
```

계획 카드에 들어가는 것: 제품·단계, 총 문항 수와 단원 세트 수, 선택형/서답형 수, 난도 분포, 핵심/심화 수, 문항 원형 배분, 범위 상태와 막힌 이유.

1. 사용자가 말한 값은 그대로 쓴다. 빠진 값만 `ops/planning/ARC_PLAN_DEFAULTS_V1.yaml`로 채운다.
2. 계획 카드를 사용자에게 보여 준다. 기본값으로 채운 항목은 "기본값"이라고 표시한다.
3. 과목이나 범위를 전혀 알 수 없을 때만 묻는다. 그 밖에는 묻지 않고 **단원 세트 1개**를 먼저 만든다.
4. 세트 1개를 검토받은 뒤 나머지 세트를 만든다. 한 번에 전부 만들지 않는다.

규칙 원문: `ops/ARC_REQUEST_PLANNING_V1.0.md`

## 3. 제품과 단계

| 제품 | 무엇 | 조판 |
|---|---|---|
| ARC CORE | 개념서 | 1단 |
| ARC N° | 단원·유형별 문제집 | 2단, 정답은 맨 뒤 |
| ARC FINAL | 실전 모의고사 | 2단, 정답 PDF 분리 |

국어 ARC N°의 단계 (2026-11-14부터. 옛 V1–V6 버전 사다리는 폐지, `quality/korean/ARC_KOR_LEVEL_POLICY_V2.0.md`):

| 단계 | 성격 | 선택형 난도 D2/D3/D4/D5 | 심화 비율 |
|---|---|---|---|
| 기본(L1) | 범위 개념을 빠짐없이 확인·적용 | 40 / 45 / 15 / 0 | 20% |
| 표준(L2) | 내신 실전 수준 (기본값) | 25 / 45 / 25 / 5 | 25% |
| 심화(L3) | 상위권 변별, 새 자료 추론·심화 비중 최대 | 15 / 50 / 30 / 5 | 30% |

- **어려운 문항일수록 추론·심화 (전 과목)**: D2 확인·적용 / D3 적용·추론·심화 / D4 추론·심화 / D5 심화. 단계를 올리면 추론·심화 비중이 자동으로 커진다 (`quality/ARC_EXAMINER_LENS_V1.3.md` §13).
- 단계를 말하지 않으면 표준(L2), 같은 범위 기록이 있으면 한 단계 위. `--level 기본|표준|심화|L1|L2|L3` (옛 V1~V4·V6도 받아서 바꾼다).
- ARC FINAL은 단계가 아니라 제품이다(옛 V5). 맞춤법·띄어쓰기는 범위에 있으면 어느 단계에서나 쓰는 주제 모듈이다(옛 V6).
- 영어·사회·과학에는 단계가 없고 과목별 난도 분포 하나를 쓴다. 난도↔유형 연결은 같이 적용된다.
- 기본 문항 수: 국어 50, 영어 50, 사회 20, 과학 20. 국어는 선택형 11 + 서답형 1짜리 단원 세트로 나눈다.
- 영어 ARC N° 1세트 = 어휘 15 + 어법 10 + 독해 15 + 서답형 10. 영어 ARC FINAL = 실제 시험과 같은 38문항(선택형 34 + 서답형 4).
- 모든 ARC N°: 핵심 70~80% / 심화 20~30%.

## 3-1. 현재 시험 범위 (2026학년도 2학기 기말, 학교 공지 2026-11-13)

| 과목 | 범위 | 구조 |
|---|---|---|
| 국어 (공통국어2) | 교과서 3단원, 4-1단원 (104~149쪽), 보충 프린트 전범위 | 선택형 22(80점) + 서술형 4(20점) |
| 영어 (공통영어2) | 교과서 Lesson 2, 해커스보카 수능완성 1800+ Day31~40, 2026 수능기출문제집 고난도독해 Level1 p78~91(28지문) | 선택형 34(80점) + 서술형 4(20점) |
| 사회 (통합사회2) | A: 44~61쪽, 108~123쪽, 학습지 / B: 134~151쪽, 학습지 / C: 25~26쪽, 64~83쪽, 학습지 | 선택형 22(90점) + 서술형 2(10점). A 7+1, B 7+1, C 8 |
| 과학 (통합과학2) | A: 110~117, 134~137, 144~149쪽 / B: 46~62쪽 / C: 70~95, 130~133쪽 / D: 98~101, 150~154쪽 | 선택형 24(80점) + 서술형 4(20점) |

과목 MASTER의 SCOPE LOCK에 남아 있는 중간고사 범위는 이 표로 대체된다. 한국사·AI는 보류, 수학은 ARC 과목이 아니다.

## 4. 동북고 문항처럼 만들기

문항은 "개념 → 문항"이 아니라 **"확인된 시험 원형 → 개념 대입 → 함정 설계"** 순서로 만든다.

- 근거 장부: `quality/school/ARC_SCHOOL_EVIDENCE_LEDGER_V1.0.yaml` — 규칙마다 D1(원안 직접 확인)/D2(내부 기록)/D3(외부 추정). 차단 게이트는 D1·D2로만 만든다.
- 국어 문법 원형: `quality/korean/ARC_KOR_GRAMMAR_ARCHETYPES_V1.0.yaml` — 원형 7종, 금지 형식 4종, 오답 함정 6종.
- 게이트: `python tooling/korean/archetype_gate.py <번들>/items.yaml`
- 규칙 원문: `quality/ARC_SCHOOL_ARCHETYPE_GATE_V1.0.md`
- 영어 문항 유형: `quality/english/ARC_ENG_EXAM_TYPES_V1.0.yaml` — 유형 코드 20종과 FINAL 38문항 배치표. 영어는 유형이 거의 고정이라 이 코드에서만 고른다. 게이트: `python tooling/english/exam_type_gate.py <번들>/items.yaml`
- 교사 개인 성향 예측은 하지 않는다(`teacher_style_prediction: disabled`).

## 5. 제작 흐름

```
계획(plan) → 자료 열람(Drive) → 번들 작성(items.yaml) → 자체 점검 + 미리보기(draft_preview)
→ 독립 재풀이(blind_review.yaml) → 생산 파이프라인(production_pipeline) → 사용자 검수 1회 통과 → Google Drive 저장 → 기록(log)
```

| 단계 | 명령 |
|---|---|
| 초안 미리보기 (범위 미확정이어도 가능, 출판 불가) | `python tooling/production/draft_preview.py <번들> --output-dir <out>` |
| 원형 게이트 | `python tooling/korean/archetype_gate.py <번들>/items.yaml` |
| 정식 생산 (범위 확정 + 독립 재풀이 필요) | `python tooling/production/production_pipeline.py <번들> --output-dir <out>` |
| 범위 등록 (근거 필수) | `python tooling/arc.py scope --subject KOR --status CONFIRMED --units … --sources … --evidence …` |
| 실행 기록 | `python tooling/arc.py log --run-id … --product ARC_N --subject KOR --range … --items …` |
| 파일을 고친 뒤 | `python tooling/arc.py checksums` |
| 푸시 전 | `python tooling/arc.py ci` |

번들 형식: `tooling/production/README.md`

## 6. 폴더 지도

| 위치 | 내용 |
|---|---|
| `SYSTEM_MANIFEST.yaml` | 지금 유효한 규칙 파일 목록. 버전이 여러 개인 파일은 여기 적힌 것만 유효 |
| `ARC_MAP.md` | 이 지도 |
| `AGENTS.md` (`CLAUDE.md`는 이것을 불러옴) | 에이전트 진입점: 공통 규칙 + 포인터 |
| `entry/` | 과목별 진입 파일 (`KOR.md`, `ENG.md`, `SOC_SCI.md`) — 맡은 과목 것만 읽는다 |
| `archive/` | manifest가 고르지 않는 지난 버전 규칙 (원래 경로 유지, 비활성) |
| `ops/ARC_RUNBOOK.md` | 운영 절차 원문 |
| `ops/HANDOFF_20261114_EXAMINER_LENS.md` | 최근 인수인계: 홈 레포 정리, 출제자 시선 V1.0→V1.3, 국어 단계 통합, 시범 세트, 미확인 사항 |
| `quality/ARC_EXAMINER_LENS_V1.3.md` | 출제자 시선(내신 출제 순서 + 변별 4단계 + 난도 상한·학생 안내·<보기> 조판 + 난도↔유형 연결), 전 과목 |
| `ops/ARC_REQUEST_PLANNING_V1.0.md`, `ops/planning/` | 요청 → 계획 규칙과 기본값 |
| `ops/exams/EXAM_CONTEXTS_V1.yaml` | 현재 시험과 과목별 범위 상태 |
| `ops/exams/DONGBUK_2026_2_FINAL_SCOPE_NOTICE.yaml` | 학교 기말 범위 공지를 옮겨 적은 기록 (범위 근거) |
| `engine/` | 공통 생성 엔진, 국어 문항 엔진, CORE 엔진 |
| `subjects/` | 과목 MASTER (범위·과목 규칙) |
| `quality/` | 품질 규칙·게이트, 난도, 앵커, 카나리, 생산 번들(`quality/production/`) |
| `quality/school/` | 학교 출제 근거 장부 |
| `quality/korean/` | 국어 단계 정책(기본·표준·심화), 맞춤법 주제 모듈, 문법 원형 |
| `quality/english/` | 영어 문항 유형 라이브러리 |
| `templates/` | 조판 규칙과 HTML 마스터 |
| `tooling/` | 실행 도구 (`arc.py`, 생산 파이프라인, 조판기, 게이트, 카나리) |
| `tools/oss/` | 외부 오픈소스 도구 설치기와 목록 |
| `ops/RUN_LOG.jsonl` | 실행 기록 |

원본 자료(교과서·학습지·기출·생성 PDF)는 Google Drive에 있고 저장소에는 올리지 않는다.

## 7. 반드시 지키는 것

- **파일을 만들면 사용자에게 보여 주고, 검수를 1번 통과하면 반드시 Google Drive에 저장한다.** 통과 전에는 저장하지 않는다. (`ops/ARC_DRIVE_SAVE_RULE_V1.0.md`)
- 범위는 추정으로 확정하지 않는다. 학교 공지나 사용자 지시가 근거다.
- 규칙은 manifest가 고른 파일에만 넣는다. 지난 버전 파일에 덧붙이지 않는다.
- 독립 재풀이를 하지 않은 문항을 검증 완료라고 하지 않는다.
- 기출·문제집의 문장과 선지를 베끼지 않는다.
- 범위가 `PROVISIONAL_REMAINDER`인 동안 나오는 PDF는 모두 검토용 초안이다.

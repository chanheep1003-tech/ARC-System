# 인수인계 — 2026-11-14 출제자 시선(Examiner Lens) 정비 + 국어 단계 통합

이 문서는 2026-11-14 세션 하나에서 한 일을, 그 대화를 보지 못한 다음 에이전트가 그대로 이어받을 수 있게 정리한 것이다.
브랜치: `claude/beautiful-gauss-ykl03y` (main에 아직 병합하지 않음). 로컬 CI 마지막 결과: **39 pass / 0 fail / 1 skipped**.

---

## 0. 먼저 할 일 (이어받는 에이전트)

```bash
git fetch origin claude/beautiful-gauss-ykl03y && git checkout claude/beautiful-gauss-ykl03y
python tooling/arc.py doctor && python tooling/arc.py status
```

1. `AGENTS.md` → `ARC_MAP.md` → `SYSTEM_MANIFEST.yaml` → 맡은 과목의 `entry/<과목>.md` 하나만 읽는다.
2. 문항을 만들거나 검토한다면 `quality/ARC_EXAMINER_LENS_V1.3.md`를 처음부터 끝까지 읽는다(이 문서 §3·§10이 요약). 국어는 `quality/korean/ARC_KOR_LEVEL_POLICY_V2.0.md`도.
3. Middle Korean(중세 국어)은 사용자가 명시했을 때만 `subjects/KOREAN_MIDDLE_KOREAN_QUALITY_RULES_V1.0.md`를 읽는다.
4. Old Hangul이 들어간 PDF를 만든다면 폰트를 먼저 확인한다(§6 참고): `fc-list | grep -i -E "hando|noto.*cjk"`.

---

## 1. 이번 세션에서 바뀐 것 (커밋 순서)

| 커밋 | 내용 |
|---|---|
| `b0d4b97` | `.claude/settings.json`: addyosmani/agent-skills 마켓플레이스 이름이 실제로는 `addy-agent-skills`라서 플러그인이 한 번도 로드되지 않았음 → 키 수정. 스킬 25개(spec-driven-development, context-engineering, doubt-driven-development 등) 사용 가능 |
| `4bcb3d8` | **홈 레포 패턴 정리**(aihero.dev "The Home Repo Pattern" 참고). `AGENTS.md`를 포인터 허브로 축소, 과목별 진입 파일 `entry/KOR.md`·`entry/ENG.md`·`entry/SOC_SCI.md` 신설, manifest가 고르지 않는 지난 버전 규칙 91개를 `archive/`(원래 경로 유지)로 이동, `CLAUDE.md`(=`@AGENTS.md`) 추가 |
| `ae7823a` | **출제자 시선 V1.0**: 내신 교사 출제 순서(출제 계획표 → 수업 근거 → 오개념별 오답 → 이의 제기 검토 → 동료 교사 블라인드 검토). 역할 `agents/school-examiner.md`, 게이트 `tooling/content_qa/examiner_lens_gate.py` + 회귀 테스트, `arc.py scaffold`가 해당 필드를 기본으로 생성 |
| `44a49ad` | 시범 세트 `KOR_N_MKO10_20261114`(3단원 중세국어 5 + 맞춤법 5). **렌더러 버그 수정**: Linux에서 옛한글이 낱자로 흩어져 찍히던 문제(나눔고딕에는 옛한글 조합 기능이 없음) → 조합용 자모 구간을 HANDotum 또는 Noto CJK로 그리고, 한 음절을 한 칸 폭으로 측정. `tooling/ci/install_fonts.sh`에 `fonts-noto-cjk` 추가 |
| `2fd2e7b` | **출제자 시선 V1.1**: 변별 4단계(RECALL/APPLY/INFER/EXTEND), 세트 배분, 새 자료 규칙, 과목별(국·영·사·과) 적용 지침 |
| `d456d6c` | V1.1 시범 세트 `KOR_N_MKV11_20261114`(확인 2 · 적용 4 · 추론 2 · 심화 2) |
| `1c12503` | **출제자 시선 V1.2**: 난도 상한(칸 하나 차이 조합형은 최대 D3), 낯선 자료의 학생용 안내 필수, `<보기>` 조판 규약. 렌더러 `structure_view_lines`. 수정 세트 `KOR_N_MKV12_20261114` |

활성 규칙은 **V1.3 하나**다(§10 참고). V1.0·V1.1·V1.2는 `archive/quality/`에 있고 읽지도 고치지도 않는다.

---

## 2. 저장소 구조 (홈 레포 패턴)

```
AGENTS.md              ← 에이전트 진입점. 공통 규칙 + 포인터만. (CLAUDE.md는 이걸 불러옴)
ARC_MAP.md             ← 저장소 지도, 제품·버전 표, 제작 흐름
SYSTEM_MANIFEST.yaml   ← 활성 규칙 경로의 유일한 권위. 버전이 여러 개면 여기 적힌 것만 유효
entry/KOR.md           ← 국어 작업 때만 읽음 (V1–V6, V6 맞춤법, 11-05 교정 패치, 중세 국어)
entry/ENG.md           ← 영어 작업 때만 (유형 코드 라이브러리)
entry/SOC_SCI.md       ← 사회·과학 작업 때만
archive/               ← 대체된 지난 버전 (원래 경로 그대로). 비활성
quality/production/    ← 문항 번들(items.yaml)
```

원칙: **공통 규칙은 AGENTS.md, 과목 전용 규칙은 entry 파일, 상세는 manifest가 가리키는 파일.** 과목 특례를 AGENTS.md 본문에 덧붙이지 않는다.
규칙을 바꿀 때는 활성 파일을 고치지 말고 새 버전 파일을 만들고, 지난 버전을 `archive/`로 옮기고, manifest·AGENTS.md·entry·역할 파일의 경로를 모두 바꾼다(`grep -rln "<옛 파일명>"`으로 확인).

---

## 3. 출제자 시선 요약 (`quality/ARC_EXAMINER_LENS_V1.3.md` — V1.2까지의 내용, V1.3 변경은 §10)

### 3-1. 출제 순서 (모든 과목)
1. **출제 계획표**(`blueprint`): 단원 × 내용 × 행동 영역 × 단계 × 난도 × 배점. 문장은 그다음.
2. **수업 근거**(`teaching_anchor`): 교과서 쪽·학습활동·학습지 항목. 새 자료 문항도 **개념**의 근거는 필수.
3. **오답 = 학생 오개념 하나씩, 서로 다르게**(`distractor_misconceptions`). 같은 실수를 네 번 반복하면 실패.
4. **시험지 표준 발문**, 교사가 실제로 쓸 문장.
5. **이의 제기 검토**(`appeal_check`): 수업 밖 지식 필요? 복수 정답? 발문 뜻이 하나?
6. **동료 교사 블라인드 검토**(`agents/school-examiner.md`): 정답·해설·목표 난도 없이 학생용 시험지만 보고 KEEP/REWRITE/DROP. REWRITE+DROP > 30%면 세트를 사용자에게 보이지 않고 다시 만든다. 작성자와 같은 대화 맥락에서 검토하면 블라인드가 아니다.

### 3-2. 변별 4단계 (`transfer_level`)
| 단계 | 무엇을 묻나 |
|---|---|
| RECALL 확인 | 교과서·프린트 예문 그대로 |
| APPLY 적용 | 같은 개념을 새 예문에 |
| INFER 추론 | 처음 보는 자료를 배운 개념으로 해석 |
| EXTEND 심화 | 처음 보는 조항·조건을 `<보기>`로 주고 결합 판단 |

~~고정 배분(ARC_N RECALL ≤ 30%, INFER+EXTEND ≥ 30%)~~ → **V1.3에서 폐지**, 난도↔유형 연결로 대체(§10).

### 3-3. 새 자료 규칙 (`novel_material`)
- `kind`: NEW_EXAMPLE · NEW_PASSAGE · NEW_DATA · NEW_CLAUSE · NEW_CASE / `source`: 실제 출처 또는 AUTHORED.
- **개념은 배운 것, 자료만 새것.** 새 조항은 `<보기>`에 전문. 실제 작품·법조문·통계는 원문 그대로 + 출처. 교과서 예문 단어만 바꾼 것은 새 자료가 아니다(FAKE_TRANSFER).
- EXTEND는 NEW_CLAUSE / NEW_DATA / NEW_CASE 중 하나가 있어야 한다.

### 3-4. V1.2에서 추가된 것 (사용자 검토 반영)
- **§10 난도 상한**: `<보기>`가 규칙을 다 주고 오답이 정답과 **칸 하나씩만** 다른 조합형은 **최대 D3**(게이트 `GRID_ONE_CELL_D4`). 판별 안내를 준 문항은 한 단계 낮게 본다.
- **§11 학생용 안내**: NEW_CLAUSE·NEW_DATA에는 `student_support`로 GUIDE(판별 방법)·EXAMPLE(풀어 본 예)·PLAIN(쉬운 말 풀이) 중 하나 이상(게이트 `STUDENT_SUPPORT_MISSING`). 안내는 원리만 주고 정답을 알려 주지 않는다. **추론의 어려움은 자료 해독이 아니라 개념 적용에 있어야 한다.**
- **§12 `<보기>` 조판**: `제28항`, `[붙임]`, `걸 「준말」` 같은 표제는 굵게 한 줄, 본문·①②는 아래 줄 들여쓰기. 렌더러가 자동 처리하므로 번들에는 한 줄로 써도 된다.

### 3-5. 시험지 표기 규약 (게이트가 검사)
- `년[만]에`처럼 대괄호로 띄어쓰기를 가리지 않는다(NON_SCHOOL_MARKUP). 발음 `[꼬치]`, 구간 `[A]`, A3 원형의 `<보기 2>`는 허용.
- 제작 용어(판단축, 정답 후보, distractor …)를 학생용 문장에 쓰지 않는다.
- 정답이 늘 가장 긴 선지 / 정답 번호 쏠림 금지.
- (생산 파이프라인 쪽 기존 규칙) "적절하지 않은 것" 발문은 10문항 중 2개까지, "가장 적절한 것"은 40%까지, 문항 유형(family) 4종 이상, D4·D5 비중 15~35%.

---

## 4. 문항 세트 만드는 명령 순서

```bash
# 1) 계획 카드 (사용자 지정값은 그대로, 빠진 값만 기본값)
python tooling/arc.py plan --subject KOR --scope "3단원 중세국어 + 한글 맞춤법" --count 10 --level 표준   # 기본|표준|심화, 생략 시 표준

# 2) 번들 뼈대 — examiner_lens: V1.3 필드가 기본으로 들어감
python tooling/arc.py scaffold --subject KOR --product ARC_N --scope "…" --actor CLAUDE --out quality/production/<번들>

# 3) 자료 열람(Drive) → items.yaml 작성 → 게이트
python tooling/content_qa/examiner_lens_gate.py quality/production/<번들>/items.yaml
python tooling/korean/archetype_gate.py quality/production/<번들>/items.yaml      # 국어 문법 원형을 쓸 때
python tooling/english/exam_type_gate.py quality/production/<번들>/items.yaml     # 영어

# 4) 조판 미리보기 + 작성자 자체 점검 (블라인드 미실시 경고는 정상)
python tooling/production/draft_preview.py quality/production/<번들> --output-dir <scratch>
#   report의 author_side_failures / author_selfcheck_failures가 비어야 한다. pdf_qc는 PASS

# 5) 동료 교사 블라인드 검토(별도 컨텍스트) → 사용자 검수 1회 → 통과 시 Drive 저장(ops/ARC_DRIVE_SAVE_RULE_V1.0.md)

# 6) 파일을 고쳤으면
python tooling/arc.py checksums && python tooling/arc.py ci
```

번들 필드 예시는 `quality/production/KOR_N_MKV12_20261114/items.yaml`을 본다(V1.2 필드를 모두 갖춘 번들). 단, V1.3으로 검사하면 4번(RECALL인데 D4)이 DIFFICULTY_TRANSFER_MISMATCH로 걸린다 — 새 세트는 이 점을 지켜 만든다.

---

## 5. 사용자 피드백 → 반영 위치 (규칙이 왜 이렇게 생겼나)

| 사용자 피드백 (요지) | 원인 진단 | 반영 |
|---|---|---|
| "N제 문항 퀄리티가 별로" | 오답이 같은 규칙의 복제(오답 4개가 같은 오개념), 난도·오답 강도를 작성자가 스스로 적음, 정답 번호 쏠림 | V1.0 오개념별 오답, 게이트 CLONE_DISTRACTORS / ANSWER_POSITION_SKEW |
| "AI스럽다, 기출로 나올 것 같지 않다, 출제자·내신 선생님 기준으로" | 규칙 문서 → 문항 순서로 만듦. 수업 근거 없이 지어낸 예문, `[만]` 같은 비학교 표기 | V1.0 출제 순서, teaching_anchor, NON_SCHOOL_MARKUP, 동료 교사 역할 |
| "교과서·프린트 예문만 내지 말고 새 보기·선지·예문·조항으로 추론·심화. 국어뿐 아니라 영·과·사도" | 시범 세트가 RECALL/APPLY뿐(INFER+EXTEND 0) | V1.1 4단계·배분·새 자료 규칙·과목별 지침, 게이트 TRANSFER_SHORT |
| "3번이 이게 D4?" | 규칙을 `<보기>`에서 다 주고 칸 하나 차이 → 오답마다 대조 한 번 | V1.2 §10, GRID_ONE_CELL_D4 |
| "9번 아이디어는 좋은데 아이들이 이해하기 어려울 듯, 설명을 더" | 사전 뜻풀이를 원문 그대로 제시, 판별 단서 없음 | V1.2 §11 student_support, STUDENT_SUPPORT_MISSING |
| "`<보기>` 안 ①이 조항 아래로 내려가면 좋겠다, 다른 문항도" | `<보기>` 줄이 한 줄로 이어짐 | V1.2 §12, `kor_renderer.structure_view_lines` |
| "문제 퀄리티·수준은 좋다", "다른 과목은 괜찮다" (V1.2 시점) | — | 현재 방향 유지. 영·사·과 시범 세트는 사용자가 필요 없다고 함 |

사용자가 처음부터 일관되게 원한 것: **실사용 문항 대량 생산이 아니라, 어색함이 생기지 않는 출제 시스템**. 다음 작업도 이 목표에서 시작한다.

---

## 6. 시범 번들과 상태

| 번들 | 내용 | 상태 |
|---|---|---|
| `quality/production/KOR_N_MKO10_20261114` | V1.0 시범. RECALL/APPLY만 | 비교용. V1.1 게이트로는 TRANSFER_SHORT(회귀 테스트가 이것을 확인) |
| `quality/production/KOR_N_MKV11_20261114` | V1.1 시범. 확인 2·적용 4·추론 2·심화 2 | V1.2 게이트로는 3번 GRID_ONE_CELL_D4, 9번 STUDENT_SUPPORT_MISSING (회귀 테스트가 확인) |
| `quality/production/KOR_N_MKV12_20261114` | **V1.2 수정본** — 3번 D3, 9번 학생 말 + 판별 방법, 7번 판별 방법, 2번 D4 | 게이트·자체 점검·PDF QC PASS. **블라인드 검토 PENDING, 사용자 최종 검수 전, Drive 미저장** |

수업 근거로 쓴 학교 자료(Drive):
- `동북고_1학년_국어_기말고사_보충자료1_중세국어문법보충_스캔본.pdf` (ID `1TYpLcCrGd8HkIQlW054oCl7U8Yq_tFu5`) — 선생님 배포 프린트 9쪽. 끝에 선생님 연습문항 2개("'…'를 보니, 현대 국어와 달리 …을 알 수 있군" 형식).
- `…중세국어문법보충_전문전사본` (Google Doc `1op8cDZtnBEqFgZE40H6osFOlu0dhLu6D5uZCAEaA8pE`) — 옛한글 표기는 이쪽이 정확. ★ 표시가 선생님 강조점.

---

## 7. 아직 확인되지 않은 것 / 알려진 한계

- **블라인드 재풀이 미실시**: 세 시범 세트 모두 `INDEPENDENT_RECHECK`, `KOR_MID_*` 게이트가 PENDING. 정답 유일성은 작성자 확인뿐이다.
- **원문 미대조**: 「두시언해」 「춘망」 구절(KOR_N_MKV12 2번)과 하ᄂᆞᆯ토·하ᄂᆞᆯᄒᆞᆯ·내콰(3번)는 작성자 기억에 의존. 출판 전 원문·판본 대조 필요.
- **교과서 쪽 번호 미확인**: 한글 맞춤법 문항의 `teaching_anchor`는 "쪽 번호 미확인"으로 적혀 있다. Drive에서 맞춤법 쪽 학교 프린트는 찾지 못했다.
- **제28·29항 수업 여부 미확인**: 교과서에서 다뤘다면 KOR_N_MKV12 7번은 EXTEND가 아니라 APPLY다.
- **선생님 프린트 전사본 자체의 오류**: 'ᄯᆞᄅᆞᆷ'의 합용 병서를 ㅳ으로(실제 ㅼ), '아니ᄒᆞᆯᄊᆡ'의 'ᄒᆞ다'를 '많다'로 적은 주석이 있다. 문항 근거로 쓰지 말 것.
- **폰트**: 학교 시험지 폰트 HANDotum(한컴, 라이선스)은 이 환경에 없다. Linux에서는 Noto CJK로 옛한글을 조합한다(`fonts-noto-cjk` 필요). Windows/한컴 설치 환경에서는 HANDotum이 우선.
- **게이트의 한계**: examiner_lens_gate는 표기·필드·배분·조합형 구조만 기계적으로 본다. "어색한 문장"인지는 동료 교사 블라인드 검토에서만 걸러진다.
- **발문 상한과 학교 자료의 차이**: 선생님 연습문항은 둘 다 "적절하지 않은 것"이지만, 파이프라인 상한은 10문항 중 2개다. 바꾸지 않았다(시험지 전체로는 타당하다고 판단). 사용자가 다르게 원하면 상한 조정을 제안할 것.
- 영어·사회·과학에는 V1.1/V1.2 지침만 있고 **시범 번들은 없다**(사용자: "다른 과목은 괜찮아").

---

## 8. 사용자 작업 방식 (지켜야 할 것)

- 항상 **한국어**로 답한다.
- **토큰을 많이 쓰는 작업(블라인드 검토 에이전트, 대량 제작 등) 전에는 중간에 한 번 묻는다.**
- 규칙 변경은 이 브랜치 같은 유지보수 브랜치에서. PR은 사용자가 요청할 때만 만든다.
- 산출물은 사용자 검수를 1번 통과한 뒤에만 Drive에 저장한다(통과 후에는 반드시 저장).
- 특정 교사의 개인 성향을 예측하지 않는다(`teacher_style_prediction: disabled`). 기출 문장·선지를 베끼지 않는다.
- 실행하지 않은 검증을 PASS라고 적지 않는다. 일어나지 않은 모델 간 위임을 했다고 말하지 않는다.

---

## 9. 다음 후보 작업 (사용자 확인 필요)

1. KOR_N_MKV12에 대해 동료 교사 블라인드 검토를 실제로 실행(별도 컨텍스트) → 결과로 V1.2 규칙 보정.
2. `KOR_N_MKV12` 2·3번 중세 국어 원문을 판본과 대조해 `SOURCE_VERIFIED` 기록.
3. 브랜치를 main에 병합할지 사용자에게 확인(PR 요청 시에만 생성).
4. 사용자가 원하면 같은 V1.2 기준으로 다른 단원(4-1 문학 등)에 추론·심화 문항 시범 적용.

---

## 10. 추가 변경 (같은 날 후반): 국어 단계 통합 + 출제자 시선 V1.3

사용자 지시: "국어 버전을 나누지 말고 통합해서 난이도로 나누자. 어려운 문제일수록 심화·추론 문제로." 그리고 (1) 난도↔유형 연결을 영어·사회·과학에도 적용, (2) 단계 이름은 기본/표준/심화와 L1~L3을 함께.

**국어 V1–V6 사다리 폐지 → 기본(L1) · 표준(L2) · 심화(L3)** — `quality/korean/ARC_KOR_LEVEL_POLICY_V2.0.md`
| 단계 | D2/D3/D4/D5 | 심화 비율 |
|---|---|---|
| 기본(L1) | 40/45/15/0 | 20% |
| 표준(L2, 기본값) | 25/45/25/5 | 25% |
| 심화(L3) | 15/50/30/5 | 30% |
- 옛 이름은 이렇게 읽는다: V1→L1, V2·V3→L2, V4→L3, **V5→ARC FINAL(제품)**, **V6→맞춤법·띄어쓰기 주제 모듈**(범위에 있으면 어느 단계에서나). `korean_v6_*` manifest 키와 `ARC_KOR_V6_*` 파일 이름은 호환 때문에 그대로 두었다.
- `arc.py plan --level 기본|표준|심화|L1|L2|L3` (옛 `--version V1~V4·V6`도 받아서 바꿈, V5는 오류로 ARC_FINAL 안내). 단계를 말하지 않으면 표준, 같은 범위 RUN_LOG가 있으면 한 단계 위.
- 계획 기본값: `ops/planning/ARC_PLAN_DEFAULTS_V1.yaml`의 `kor_levels`, `kor_level_aliases`, `difficulty_transfer`.

**출제자 시선 V1.3** — `quality/ARC_EXAMINER_LENS_V1.3.md` §13 (전 과목)
| 난도 | 허용 유형 |
|---|---|
| D1 | RECALL |
| D2 | RECALL · APPLY |
| D3 | APPLY · INFER · EXTEND |
| D4 | INFER · EXTEND |
| D5 | EXTEND |
- 게이트 `DIFFICULTY_TRANSFER_MISMATCH`. 고정 배분 규칙(RECALL ≤ 30% 등)은 V1.3에서 없앴다 — 기본 단계 세트가 확인 문항 위주인 것은 정상이고, 단계를 올리면 추론·심화가 자동으로 늘어난다.
- 영어는 범위 지문의 변형(새 요약문·새 문장·새 문맥)이 새 자료로 인정되므로, 유형 코드를 지키면서 D4 문항을 변형 자료로 만든다.
- 계획 카드에 `유형` 줄이 생겨 난도별 허용 유형을 보여 준다(전 과목).

**바뀐 파일**: 위 두 정책(신규), 지난 버전 `archive/quality/ARC_EXAMINER_LENS_V1.2.md`, `archive/quality/korean/ARC_KOR_V1_V6_LEVEL_POLICY_V1.2.md`, manifest(`korean_levels`, `korean_final_product`, `korean_orthography_module`, `difficulty_transfer_rule`), `arc.py`(plan/scaffold), 계획 기본값, 게이트·회귀 테스트, `entry/*.md`, `ARC_MAP.md`, `AGENTS.md`, `agents/TEAM.md`, 런북·국어 문항 엔진(날짜 붙인 오버라이드 절 추가).

**아직 없는 것**: 이 단계·V1.3 기준으로 새로 만든 문항 세트는 없다. 첫 시범은 사용자 확인 후.

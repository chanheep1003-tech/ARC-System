# HANDOFF — ARC N° 통합과학2 산화와 환원 고난도 20제 V1.0

```
PRODUCT_MODE = ARC_N
SUBJECT      = 통합과학2
TITLE        = 산화와 환원 · 고난도 20제
TARGET_RANGE = OR p38~45 산화·환원 (SCIENCE_MASTER V4.0 SCOPE LOCK)
ITEM_COUNT   = 20 (객관식 5지선다)
SET_NO       = 1
SCHOOL       = 동북고등학교
EXAM_PERIOD  = 2학기 중간고사 대비
PDF_MASTER   = ARC_PDF_조판_MASTER_V2.0
DIFFICULTY   = D3 4 · D4 9 · D5 7 (사용자 요청: D3~5, 고난도 강화)
```

산출물

| 파일 | 용도 |
|---|---|
| `ARC_N_SCI_통합과학2_산화환원_고난도20_V1.0.pdf` | 합본 12쪽: 표지 → 빈 쪽 → 문제 8쪽 → 빈 쪽 → 정답 (해설·난도 표시 없음) |
| `ARC_N_SCI_통합과학2_산화환원_고난도20_V1.0.html` | 조판 소스 (생성물) |
| `items.py` / `figures.py` | SECTION A 원고 원본 / 시각자료(SVG) 원본 |
| `build.py` | HTML → PDF 조판 (`python3 build.py [--png DIR]`) |
| `verify.py` | PASS B 독립 재풀이 (`python3 verify.py`) |

## SECTION A — QUESTION_MANUSCRIPT

원고 원본은 `items.py`이며 학생용 PDF에 그대로 조판되어 있다. 학생 원고에는 정답·해설·난도·QC 메타데이터를 넣지 않았다.

## SECTION B — ANSWER_KEY

| 01 | 02 | 03 | 04 | 05 | 06 | 07 | 08 | 09 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| ③ | ⑤ | ④ | ③ | ④ | ② | ① | ④ | ⑤ | ② |

| 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|
| ④ | ② | ① | ③ | ② | ④ | ① | ⑤ | ③ | ⑤ |

정답 분포: ① 3 · ② 4 · ③ 4 · ④ 5 · ⑤ 4 (같은 번호 3연속 없음)

### 편집자용 검증 요약 (학생 PDF 비포함)

| # | CONCEPT_ID | 구조 | D | 결정 근거 (REDOX_LEDGER 요약) |
|---|---|---|---|---|
| 01 | SCI-OR-ELECTRON | 탄소 흐름 모식도 · 산소 이동 | D3 | (가)(라) CO₂ 산소 잃음. (나)(다)에는 CO₂가 반응물로 없으므로 ㄷ 거짓 |
| 02 | SCI-OR-QUANT | 금속+산 H₂ 그래프 · 전하 추론 | D4 | A: H₂ 2N ↔ e⁻ 4N → A²⁺. B: H₂ 3N → B³⁺. 이온 수 A쪽 H⁺6N+A²⁺2N+Cl⁻10N=18N, B쪽 16N |
| 03 | SCI-OR-ELECTRON | 은 변색 제거(생활) · 전자 수 | D3 | Ag₂S 3N → Ag⁺ 6N → e⁻ 6N → Al 2N (ㄴ 거짓) |
| 04 | SCI-OR-QUANT | 두 비커 입자 모형 · 음이온으로 전하 고정 | D5 | X⁺(8N/8N), Y³⁺(12N/4N), M: X⁺6N 환원/3N → M²⁺. 전체 이온 Ⅰ 13N, Ⅱ 17N. 혼합 후 e⁻ 8N 추가 → M²⁺ 10N |
| 05 | SCI-OR-EXPERIMENT | 철 부식 시험관 · 변인 통제 | D3 | (나)–(라)는 산소·소금 두 변인이 다르므로 ㄷ 거짓 |
| 06 | SCI-OR-REACTIVITY | 금속 이용 연표 + 탄소 환원 표 | D4 | C>Cu, C>Fe, Al>C, Al>Fe. 가장 늦게 쓰인 Al이 가장 반응성 큼 → ㄱ 거짓 |
| 07 | SCI-OR-REACTIVITY | 양이온 수 ‘일정’의 두 의미 · 반드시 옳은 것 | D5 | Ⅱ,Ⅳ 일정 = 무반응(전하 다름) → A>B, D>A. Ⅲ → C>B. Ⅰ은 전하 같아 판정 불가. 가능한 서열 전수 조사 결과 ①만 항상 참 |
| 08 | SCI-OR-ELECTRON | 산소 이동 vs 전자 이동 교차 | D4 | Cu 2N: C N개, Zn 2N개(ㄴ 거짓). Cu 1개당 e⁻ 2개 동일 |
| 09 | SCI-OR-QUANT | 판 질량 그래프 (감소해도 석출) | D4 | (가) 원자당 −65+64=−1 → 3단위, (나) 원자당 +41 → 2단위. 판 질량 감소 = 수용액 질량 증가 |
| 10 | SCI-OR-EXPERIMENT | 가설 반증 | D4 | 반증: 전하 작은 금속이 더 반응성 큼(ㄱ P⁺>Q²⁺, ㄹ R²⁺>S³⁺). ㄴ·ㄷ은 가설과 부합 |
| 11 | SCI-OR-QUANT | 두 이온 순차 반응 꺾은선 그래프 | D5 | 0~3N: A⁺ 6N 환원 → C²⁺. 3N~6N: e⁻ 6N / B 2N → B³⁺. 4.5N: B 2N−1N = N |
| 12 | SCI-OR-REACTIVITY | 도금·희생 금속 | D4 | X>Fe>Y>Z → (가) X 먼저, (나)·Z판은 철 먼저 |
| 13 | SCI-OR-ELECTRON | 탈산소제 vs 방습제 | D3 | Fe 4N → e⁻ 12N → O₂ 3N (ㄴ 거짓), 실리카겔은 물리 흡착 |
| 14 | SCI-OR-QUANT | 연쇄 전이 (A→B→C) | D5 | A 2N → B 6N ⇒ A³⁺. B 6N(e⁻ 6N) → C 2N ⇒ C³⁺. (가) 양이온 −4N, (나) +4N |
| 15 | SCI-OR-QUANT | 일반화 주장 반례 찾기 | D4 | 수빈 반례: 1가 금속→2가 이온(증가). 하람 반례: 같은 전하·가벼운 판. 도윤: 음이온 불변 ⇒ 양전하 총합 불변 |
| 16 | SCI-OR-REACTIVITY | 혼합 가루 분리 흐름도 | D5 | D²⁺ 8N 중 6N 환원(A,B 각 3N) → 고체 C 3N + D 6N. D²⁺가 남았는데 C 미반응 ⇒ D>C. (나) A: (3N+2N)×2 = e⁻ 10N |
| 17 | SCI-OR-QUANT | 막대그래프 · 음이온 전하 균형 | D4 | 3x+4y=10 → X²⁺, Y⁺ (유일). 4+2z=10 → Z³⁺. Y⁺ 불변 ⇒ Y>Z>X |
| 18 | SCI-OR-REACTIVITY | 미지 금속 위치 판별 | D4 | Ⅰ M<Fe, Ⅱ Cu>M, Ⅲ M>Ag 및 M⁺ ⇒ ㉣. Cu 1개 e⁻ 2 → M 2개 |
| 19 | SCI-OR-QUANT | 양이온 수 비 → 전하 역추론 | D5 | a=x, b=1.5x, c=x/2 ∈{1,2,3} ⇒ x=2 유일 → A²⁺,B³⁺,C⁺. 반응 원자 수 C:B = 3:1 |
| 20 | SCI-OR-QUANT | 판 질량 일정 + 양이온 수 · 통합 | D5 | B²⁺ 6N(e⁻12N) → A 이온 4N ⇒ A³⁺. 4N·m_A = 6N·m_B ⇒ m_A=1.5m_B. 새 판: 원자당 +3m_B ×2N = 6N·m_B = A 4N 질량 |

난이도 기준: ARC_DIFFICULTY_ENGINE V1.0 구조점수 + 2025 동북고 2학기 중간 7~12번(산화·환원) 대비 상대 비교.
동북고 기출 최상위 변별 문항(입자 모형 전하비)을 D4 기준점으로 두고, D5는 자료 2종 이상 통합 또는 미확정 조건의 전수 판단을 요구하는 문항으로 한정하였다.
DIFFICULTY_CONFIDENCE = MEDIUM (실제 풀이 데이터 없음).

## SECTION C — LAYOUT_ASSET_MANIFEST

| ITEM | VISUAL | ASSET_CLASS | ASSET_TYPE | STATUS | WIDTH | ESSENTIAL | KEEP_TOGETHER |
|---|---|---|---|---|---|---|---|
| 01 | V01 | TRUE_VISUAL | flowchart + 반응식 표 | RENDERED | COLUMN | Y | Y |
| 02 | V02 | TRUE_VISUAL | graph | RENDERED | COLUMN | Y | Y |
| 03 | — | TEXT_ONLY | 반응식 박스 | — | COLUMN | — | Y |
| 04 | V04 | TRUE_VISUAL | particle_model | RENDERED | COLUMN | Y | Y |
| 05 | V05 | TRUE_VISUAL | experiment_diagram + DATA_TABLE | RENDERED | COLUMN | Y | Y |
| 06 | V06 | TRUE_VISUAL | timeline + DATA_TABLE | RENDERED | COLUMN | Y | Y |
| 07 | — | DATA_TABLE | 표 2개 | RENDERED | COLUMN | Y | Y |
| 08 | V08 | TRUE_VISUAL | experiment_diagram | RENDERED | COLUMN | N | Y |
| 09 | V09 | TRUE_VISUAL | graph(2패널) + DATA_TABLE | RENDERED | COLUMN | Y | Y |
| 10 | — | DATA_TABLE | 이온 표 | RENDERED | COLUMN | Y | Y |
| 11 | V11 | TRUE_VISUAL | graph | RENDERED | COLUMN | Y | Y |
| 12 | V12 | TRUE_VISUAL | 단면 모식도 + DATA_TABLE | RENDERED | COLUMN | Y | Y |
| 13 | — | TEXT_ONLY | 설명 박스 | — | COLUMN | — | Y |
| 14 | — | TEXT_ONLY | 실험 과정 | — | COLUMN | — | Y |
| 15 | — | TEXT_ONLY | 대화 박스 | — | COLUMN | — | Y |
| 16 | V16 | TRUE_VISUAL | flowchart | RENDERED | COLUMN | Y | Y |
| 17 | V17 | TRUE_VISUAL | graph(막대) | RENDERED | COLUMN | Y | Y |
| 18 | V18 | TRUE_VISUAL | 반응성 서열 도식 + DATA_TABLE | RENDERED | COLUMN | Y | Y |
| 19 | — | DATA_TABLE | 비율 표 | RENDERED | COLUMN | Y | Y |
| 20 | V20 | TRUE_VISUAL | graph(2패널) | RENDERED | COLUMN | Y | Y |

## SECTION D — QC_STATUS

```
SCOPE_LOCK             PASS  (OR p38~45 내. 몰·화학량론·한계반응물·전지전위·산화수 계산 불필요)
DRIVE_FIRST            PASS  (2025 동북고 2학기 중간 원안, ARC N° V1.2 초안 확인)
INDEPENDENT_RECHECK    PASS  (verify.py — 미지 전하·반응성 서열 전수 조사, 20/20 일치)
UNIQUE_ANSWER          PASS
NUMBERING              PASS  (01~20 연속, 렌더 PDF 텍스트 대조)
COPY_RISK              LOW   (V1.2 초안·동북고 기출과 문장·수치·구조 중복 회피)
ASSET_SPEC_COMPLETE    PASS
CONTENT_READY          PASS
ASSET_READY            PASS
REDOX_LEDGER           PASS
REACTIVITY_ORDER_AUDIT PASS  (07·16·18 전수 조사)
MATERIAL_BASED_COUNT   16/20
TRUE_VISUAL_PLANNED    13/20
TRUE_VISUAL_ESSENTIAL  12/20
GRAPH_COUNT            5  (02, 09, 11, 17, 20)
PARTICLE_MODEL_COUNT   1  (04)
EXPERIMENT_DIAGRAM     3  (05, 08, 12)
FLOW/COMPOSITE         3  (01, 16, 18)
DATA_TABLE_COUNT       9
COVERAGE_CHECK         PASS  (SCI-OR-ELECTRON 4 · REACTIVITY 5 · QUANT 9 · EXPERIMENT 2)
BLOCKED_SCOPE_CHECK    PASS
ERROR_DB_CHECK         PASS  (RISK-SCI-01/02/03 방어 확인)
PDF_RENDER_VERIFY      PASS  (전 페이지 렌더 확인, clipping/overlap 0, 대체 글꼴 0)
HANDOFF_GATE           PASS
```

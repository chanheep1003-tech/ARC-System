## 1.8.48-dev — 2026-11-08
- 사용자 결정 반영(ops/ARC_DECISIONS_20261108.md): ARC_N 메타 스트립 D1~D5 난이도 표시, ARC_FINAL 확대 흑백 기준, ARC_N 흑백 로고, ARC_N 문항 배치(4문항 기본, 여유 시 5·6문항으로 확장), 기말 임시 범위 일원화(MASTER SCOPE LOCK은 중간 스냅샷 표시), 사회 CORE X표시 BLOCKING, 사회 C X표시 기말 제외 유지, FINAL 난이도 오프셋, 초안 임시 저장/제품 폴더 승인 후, 기말 FINAL 임시 확정 출시 허용, 마감 2026-12-07.
- 기출·창작 정책 §10 과목별 프로필(PAST_70_AI_30 / STRUCTURE_REFERENCE_ONLY)과 ORIGINAL_TRIAL을 정의하고 generation_source_gate.py에 구현·테스트 추가.
- 규칙 내부 모순 정비: V2.4 §25 정답표 위치(LAST+2), V2.4 §6~§8·§16, 공통 엔진 §15·§21, 문항 품질 루브릭 번호·참조, 국어 엔진 중복 절 번호, 자동화 런타임(과목 순서·자원 비중·참조), 준비도 게이트 기말 재기준화.
- 낡은 버전 참조 정리(활성 파일 20여 개). 이력 문서(오류 DB, 폐기 레지스트리, 동결 회귀 fixture)는 변경하지 않음.
- 코드 강제(ARC_N): kor_renderer가 D1~D5 난이도 스트립을 그림(ARC_FINAL 제외, 값이 없으면 만들지 않음), pdf_preflight에 --require-difficulty-strip(및 선택적 --max-questions-per-page) 추가, typesetter_gateway 프로필에 슬롯·스트립·로고 항목과 release_blockers(BRAND_ASSET_MISSING) 추가, 테스트 14개 신설.
- 과학 기말 FINAL 앵커 신설(quality/anchors/SCI_DONGBUK_MULTI_EXAM_DIFFICULTY_ANCHOR_V1.0.yaml): 학교 시험 4회 앙상블(평균 2.53)에 임시 오프셋 +0.2를 적용한 목표 2.73. 매니페스트 arc_final_difficulty_anchor_sci를 교체하고 산화·환원 앵커는 참고용으로 강등. EXAM_CONTEXTS에 과목별 목표 평균(KOR 3.09/SOC 3.07/SCI 2.73) 추가.
- ARC N° 흑백 로고 등록: Drive 원본(해시 검증) → 휘도 변환으로 ARC_N_LOCKUP_MASTER_BW.png 생성(565×380, 재그리기 없음), 등록부에 해시 기록. N 표지의 BRAND_ASSET_MISSING 차단 해제. Drive 업로드(ID 기록)는 대기.
- 사회·과학 ARC_N 4단계 사다리 신설(quality/ARC_N_STAGE_LADDER_SOC_SCI_V1.0.md): 사고 동작 기준 S1~S4, 기출/변형/창작 구성은 문제은행 재고(B vs ceil(0.7N))로 결정(상시 사용자 규칙). 수치는 PROVISIONAL.
- 사회·과학 ARC_N 에서 D1 문항 전면 금지(D2~D5), S1 분포 D2 0.65/D3 0.30/D4+ 0.05 로 조정. production_pipeline PROFILES 에 (SOC|SCI, ARC_N) D1=0 하드 게이트 추가(test_n_no_d1_and_stages.py, CI 등록).
- 국어를 사회·과학과 같은 4단계(S1~S4)로 통일: 사다리 문서를 quality/ARC_N_STAGE_LADDER_V1.1.md(KOR·SOC·SCI 공통)로 개정, 국어 D1 금지(기존 10% 허용 폐지), 국어 V5·V6 단계 제거(옛 V1~V6 문서·AGENTS·RUNBOOK·TEAM 에 대체 표기, 장르별 출처·검수 규칙은 유효). production_pipeline: KOR D1=0, 번들 stage(S1~S4) 선언 시 단계별 분포 WARN 검사(수치 PROVISIONAL), 테스트 test_n_no_d1_and_stages.py.
- 요청별 사용자 결정(D-20): 단계·세트 문항 수·난이도 분포(ARC_N)·국어 기출/창작 구성에 기본값을 두지 않고 비어 있으면 사용자에게 묻도록 변경. production_pipeline.request_spec_findings(REQUEST_SPEC_MISSING/NOT_USER_DECIDED/ITEM_COUNT_*/STAGE_INVALID/DIFFICULTY_*)와 사용자 분포 일치 검사(REQUEST_DIFFICULTY_*_OFF) 추가, 고정 STAGE_SHARES 제거, KOR SOURCE_PROFILE_UNDECLARED 를 WARN→FAIL. 국어 V5 는 ARC_FINAL 로 통일.
- 기말 임시 범위 등록(사용자 지시 2026-11-08): KOR 공통국어2 3단원(중세 국어+한글 맞춤법), SOC 천재 통합사회2 II-2 자유주의와 공동체주의 정의관(pp.44-49; 소단원 선택은 교과서 확인 후 임시 판단), SCI 산·염기와 중화 반응(학교 자료 미확인). EXAM_CONTEXTS 세 과목 CONFIRMED_UNITS_ONLY, 근거는 quality/source/FINAL_SCOPE_REGISTRATION_20261108.yaml. 요청 기록 ops/requests/REQ_20261108_S2_20ITEMS.yaml 상태 갱신. exam gate 테스트가 REQUEST_SPEC·KOR 소스 프로필 규칙을 반영하도록 수정.
- 알려진 미완: N 레이아웃 코드 강제 없음, 흑백 로고 Drive 업로드, 사다리 코드 게이트 없음(문서 규칙만). 상세는 ops/ARC_DECISIONS_20261108.md.

## 1.8.47-dev external tools integration candidate — 2026-11-07

- Added a pinned registry and project-local installer, task router, preliminary document converter and optional tutor/memory adapters for Orkas-AI/Orkas, p-e-w/heretic, HKUDS/DeepTutor, obra/superpowers, pbakaus/impeccable, mattpocock/skills, thedotmack/claude-mem and microsoft/markitdown.
- Intake: isolated local installs plus ARC-owned adapter; no upstream executable/skill text copied into the ARC engine. Upstream revisions and MIT/Apache-2.0/AGPL-3.0-or-later license identifiers are recorded in tooling/external/tools.lock.json; each installed checkout retains its LICENSE/notice. Node release dependencies retain npm integrity hashes. Python transitive packages remain platform-resolved upstream dependencies, not a portable frozen environment.
- Existing source, QA, blind-review, CONTENT_LOCK, print-template and one-run-state authority remains unchanged. Converted text stays UNVERIFIED; optional model output stays draft. Global hooks, automatic capture, model-weight changes and production activation remain disabled/unverified.
- Actual validation and host limitations are recorded in ops/ARC_EXTERNAL_TOOLS_VALIDATION_20261107.json. Adapter tests: 9 PASS; synthetic TXT/DOCX/PPTX/XLSX/PDF extraction: 5 PASS; Orkas typecheck and Impeccable static detector: PASS. Existing workflow/source/QA/handoff/gateway checks pass; exam-scope suite has a missing-Nanum-font environment error. Model-quality regression and live multi-model execution were not run.

## 1.8.41-dev — 2026-10-30
- Added a single request/run-state CLI and canonical operational runbook. Chunk checkpoints, ownership, expected-version guards, stage gates, isolated-review handoffs, manuscript hash binding and verified storage receipts now share one state contract.
- The CLI is an evidence ledger; external AI calls, Drive writes and semantic correctness are still host responsibilities. Draft storage and post-blind edits cannot silently become active bank items.
- Root AGENTS, expert TEAM, manifest and CI point to the common entry. Prior policy versions and unmerged PR #6 remain preserved.
- Local workflow suite: 11 behavioral tests PASS. Full repository CI is checked on this PR; static success is not model-quality proof.

## 1.8.34-dev — 2026-09-25
- Registered four textbook source texts in the source registry as USER_PROVIDED_TEXTBOOK / RAW_SCHOOL_SOURCE / EXACT, with the user's explicit authorization:
  - 속미인곡: the textbook 현대어 풀이 excerpt, taken from the PDF text layer.
  - 수라, the 아홉 켤레의 구두로 남은 사내 excerpt, and the 고속 철도 negotiation excerpt: transcribed once by eye from the page images. No second independent transcription was compared.
- Production pipeline and renderer: a set can carry `lead` text (e.g. [앞부분의 줄거리], [상황]) that is printed before the passage.
- Final KOR semi-final bundle `KOR_SEMIFINAL_FINAL_20260925`:
  - 22 선택형 + 4 서술형, 100점: 속미인곡+탄궁가 / 수라+팔원+기억할 만한 지나침 / 아홉 켤레 / 협상 / 칸트–헤겔.
  - One blind round, which matched all 22 keys. Every gate passes except FINAL_DIFFICULTY: the blind profile is D2 13 / D3 9 / D4 0 (mean 2.41), easier than the 동북고 anchor (mean 2.76).
  - 춘향전 and 제망매가 are excluded because the textbook front file (pp.1-37) is over the 10MB download limit.
- Drive: renamed the textbook split files by unit.

## 1.8.33-dev — 2026-09-25
- Policy (user directive): one blind independent solve per bundle, in every pipeline. `runtime.blind_review_rounds: 1`; the production pipeline blocks any other `rounds` value with BLIND_ROUND_POLICY_VIOLATION. Findings from the single round are fixed by the author and recorded as `post_blind_edits`, with no rerun. The N04 and first semi-final bundles are marked as legacy fixtures (WARN).
- Policy (user directive): ARC FINAL difficulty now matches the 동북고 exam instead of the fixed hard profile. The new SCHOOL_ANCHOR mode in `final_quality_gate.py` compares a set's blind profile with `quality/anchors/KOR_DONGBUK_2025_2_MID_DIFFICULTY_ANCHOR_V1.0.yaml`: the 2025-2 동북고 midterm, 21 MCQ rated by one blind rater as D1 1 / D2 7 / D3 9 / D4 4, mean 2.76. The set fails if it is easier (FINAL_SCHOOL_ANCHOR_EASIER) or harder (FINAL_SCHOOL_ANCHOR_HARDER) than the anchor.
- The three literature supplement texts (탄궁가, 팔원, 기억할 만한 지나침) are promoted to EXACT on the user's confirmation that the registry readings are correct. Files were renamed from `_DRAFT` to `_V1.0`.
- The semi-final regression now covers the anchor pass/easier/harder cases and the round policy.

## 1.8.32-dev — 2026-09-25
- Extended the production pipeline to real school-exam shape: multi-work passage sets (`sets`, (가)/(나) labels, set notes/glosses), verse sources with `L#` / `W<n>.L#` evidence refs, printed verse margin line numbers every N lines (`line_numbers`), constructed-response (서술형) items with <조건>, model answers, rubrics and accepted variants, and per-item points. New gates: CONSTRUCTED_RESPONSE_GATE (blind answer must meet the rubric; ambiguous conditions block) and POINTS_GATE (total must be 100).
- Renderer: ARC_FINAL numbering (`1.` with points, `[서술형 k]` with 조건 box and answer box), key PDF with model answers and 채점 기준, verse line numbers kept on the same row across column breaks, unbreakable `( ㉠ )` blanks.
- Fixed a rendering defect: Hanja (顔瓢, 原憲, 萇楚, 慈城, 內地, 書記) printed as empty boxes because Nanum has no CJK ideographs, and preflight did not notice. Text is now split into runs by glyph coverage with a CJK fallback font (Noto Serif CJK or WenQuanYi Zen Hei); a glyph missing from both fonts stops rendering with GLYPH_MISSING. CI installs fonts-wqy-zenhei. Fonts are now embedded only on pages that use them: an unused font cannot be subset, which had left a whole Nanum Myeongjo Bold (and CJK fallback) inside the key PDF (8.0 MB -> 0.17 MB).
- Added the hash-verified ARC FINAL lockup (`templates/brand/assets/ARC_FINAL_LOCKUP_MASTER.png`, SHA-256 matches the brand registry) so covers render and verify offline.
- Registered three literature supplement drafts (정훈 「탄궁가」, 백석 「팔원」, 기형도 「기억할 만한 지나침」) as PENDING_USER_CONFIRMATION with their open transcription conflicts; content QA keeps them blocked until confirmed.
- Added the KOR semi-final bundle (22 선택형 + 4 서술형, 100점; 2025-2 동북고 midterm used only for structure/points calibration). Three fresh blind rounds each matched all 22 keys. Measured state: integrity, length (longest-key rate 9%), stem-form, answer-position, CR and points gates PASS; BLOCKED by KOR_SOURCE_NOT_EXACT (draft literature texts) and FINAL_DIFFICULTY (blind D1 1 / D2 13 / D3 8 / D4+ 0). `test_semifinal_bundle.py` covers the bundle plus CR, points, verse-ref and glyph fault injection.

## 1.8.31-dev — 2026-09-25
- Fixed a Korean renderer defect: the first stem line was wrapped without reserving the question-number width, so the N04 stems for items 7 and 8 ran into the column gutter. PDF preflight had passed that PDF.
- ARC_N / ARC_FINAL preflight now fails `COLUMN_GUTTER_CROSSING` when a problem-page line from the left column reaches the gutter. Reproduced on the unfixed renderer (items 7 and 8 flagged); PASS after the fix. A regression case was added to `test_preflight_korean_n.py`.

## 1.8.30-dev — 2026-09-25
- Added the production pipeline (`tooling/production/production_pipeline.py`): a single item bundle (items + independent blind review) drives the manuscript, QA evidence, realism/leak/length/stem-form/answer-position/difficulty-balance metrics, handoff, typesetter admission, Korean rendering and PDF preflight. Realism counts, length cues and balance shares are now computed, not self-reported; PASS B comes from the blind review file.
- Added the Korean production renderer (`tooling/typeset/kor_renderer.py`) for ARC_N (cover, blank verso, two columns, blank separator, key) and ARC_FINAL (problem sheet without key plus a separate key PDF), with subset-embedded Nanum fonts and hash-verified canonical logo support.
- Added the Korean source-text registry. The Kant-Hegel supplement text (이행남) is locked as EXACT by SHA-256, stored on Drive (1OF_fc8N6SmcwM1oRVXJF69_jlVRmFcf-) and in `quality/source/text/`. Verification: character-level diff against the scan OCR (1162/1162 after one OCR fix), no spaces added, user-confirmed author and user-authorized finalization. Visual line-by-line review was not performed.
- The KOR N04 bundle is the first production canary. The source block is cleared. The measured state is still BLOCKED: blind difficulty is D1 30% and D4+D5 0% against the KOR ARC_N balance, and item 8 was flagged obvious at D3. The first metric run also exposed failures the earlier ad-hoc run had hidden by self-reporting: a same-stem run of 4, 5 single-best stems, and weak distractors on items 4 and 10. All three were fixed.
- CI installs fonts-nanum and runs the production regression: the baseline bundle is measured, and injected faults (length cue, metadata leak, blind mismatch, multiple-answer flag, stem run, source wording change) are blocked. The ARC_FINAL path refuses a too-easy set and keeps the key off the problem sheet.

## 1.8.29-dev — 2026-09-25
- Fixed an E2E_PDF_READY blocker for every real Korean ARC_N PDF: `pdf_preflight.py` only counted the synthetic canary markers (`QUESTION n`, `n. 3`), so a production N° PDF with `01 …` stems and `01 ③` key lines was reported as 0 questions / 0 answers and FAILED. Reproduced on the fresh KOR N04 draft and on the N03 layout convention.
- ARC_N preflight now counts canary and Korean production markers, restricts question counting to problem pages and answer counting to the answer-key pages, accepts `정답` as the answer-key heading, and requires the exact id set 1..N (reports missing/unexpected ids) instead of only a count.
- Added `tooling/pdf_qc/test_preflight_korean_n.py` (valid Korean-marker PDF passes; missing question, missing answer and missing separator are blocked) and wired it into CI.
- Corrected the Kant-Hegel supplement author to 이행남 (user-confirmed) in the supplement page map.
- Fresh model-backed KOR ARC_N set (N04, 칸트-헤겔 비문학 10문항) produced from the Drive school supplement: 4 blind independent-solve rounds all matched the key, answer-length cue rate 0.0, realism/AI-style/task-family gates PASS, handoff PASS, PDF preflight PASS. Content QA remains blocked only by KOR_SOURCE_NOT_EXACT until the OCR-reconstructed source text is visually confirmed; FINAL_USER_APPROVAL=PENDING, DRIVE_SAVE=BLOCKED.

## 1.8.26-dev — 2026-09-25
- Updated strict system validation to recognize the new ARC_N 70/30 balance policy instead of the superseded D4+D5>=35% ARC_N floor.
- Added runtime validation for ARC_N balance gate and its 70~80% core / 20~30% advanced targets.
- Synchronized unrelated Social A Thought Map checksum drift discovered by CI; no Social scope or content rule was changed by this checksum repair.
- All earlier behavioral canary stages had already passed before the strict validator caught the stale policy marker.

## 1.8.25-dev — 2026-09-25
- Generalized the Korean ARC_N balance correction to every ARC_N subject.
- Activated Common Generation Engine V4.7, Difficulty Engine V1.4 and universal ARC_N Balance Gate V1.0.
- Default ARC_N content mix is now CORE_EXAM_POINT 70~80% + ADVANCED_DISCRIMINATION 20~30%. Recommended counts include 7~8/2~3 per 10, 14~16/4~6 per 20, and 28~32/8~12 per 40.
- CORE_EXAM_POINT is not synonymous with easy recall: core items may be D3/D4 when they use strong distractors, representative data or standard application. The change limits dedicated discrimination tasks, not item quality.
- Added subject-specific core-axis maps for Korean, Social Studies, History, Science and AI. Current sprint scope locks remain unchanged: Science is oxidation-reduction only, History is ARC_N only, and AI remains deferred.
- Default ARC_N difficulty curve is rebalanced to D1 0~10%, D2 25~35%, D3 35~45%, D4 15~25%, D5 0~5% with D4+D5 generally 20~30%.
- Explicit high-difficulty/elite N requests or verified school anchors may raise the advanced share, but core-axis coverage must be established first.
- ARC_FINAL is unchanged and continues to use the dedicated FINAL difficulty/item-quality release gate.

## 1.8.23-dev — 2026-09-24
- Rebalanced Korean ARC_N after user review of ARC_N03: individually valid upper-tier items had displaced core school-exam coverage.
- Activated Korean Item Engine V1.3, Korean Item QA V1.4, and Korean Master V4.3.
- Korean ARC_N default per 10 items is now 3 foundation/core + 4 school-standard + 2 upper + 0~1 extreme; default D4+D5 target 20~30%.
- Added hard CORE_EXAM_POINT_COVERAGE for theme/attitude/expression/key-material/structure in literature and claim/structure/concept-relation/explicit-accuracy/application in nonfiction.
- Added RARE_TASK_BUDGET: counterfactual deletion/replacement max 1 per 10; micro-reference trace max 1; discrimination-only tasks max 2.
- Registered KOR_N03_OVERDISCRIMINATION_20260924_V1 as a user-found regression sentinel. Status remains PENDING_MODEL_CANARY.
- ARC_FINAL and non-Korean hardening are unchanged.

## 1.8.19-dev — 2026-09-23
- Added the user's third detailed Korean four-passage analysis note to Drive and activated KOR Supplement Point Map V1.1.
- V1.1 expands per-passage priority axes and near-miss distractor seeds for 「탄궁가」, 「팔원－서행시초 3」, 「기억할 만한 지나침」, and the Kant/Hegel reading, with special emphasis on fact-vs-inference, past-vs-present, direct-intervention overstatement, device-function reduction, and concept/condition swaps.
- Added a cross-passage matrix for the two modern poems and Kant/Hegel, plus explicit SCHOOL_SOURCE_VERIFY_REQUIRED labels for external-note details that cannot become answer-bearing evidence until confirmed in the actual school material.
- RAW SCHOOL SOURCE remains authoritative; the three analysis notes remain SECONDARY_REFERENCE only.

## 1.8.18-dev — 2026-09-23
- Marked the user-found Korean weak-distractor regression explicitly as `PENDING_MODEL_CANARY`; rule/QA activation is not treated as proof that production item quality is fixed.
- Recovered CI wiring after separating the new user-found sentinel from the original frozen 30-case GOLD suite and synchronized strict checksums in the same commit so the current dev head can be tested as one coherent state.

## 1.8.17-dev — 2026-09-23
- Kept the original GOLD-based regression suite frozen at exactly 30 cases and isolated the new user-found Korean weak-distractor sentinel as a separate regression class. This fixes CI compatibility with the V1.0 fixed-regression runner while preserving the new realism failure case.
- Manifest now reports 30 frozen GOLD fixtures + 1 separately registered user-found Korean regression sentinel; the new sentinel must not silently re-baseline the original fixture suite.
- The Korean distractor-quality patch remains REGRESSION_PENDING until a fresh model-generated set passes the new semantic gates.

## 1.8.16-dev — 2026-09-23
- Saved the user's two Korean supplement point-analysis notes into Google Drive under `N제 시스템/01_국어/문제집·참고자료/출제포인트·분석자료` and registered a manifest-selected secondary point map for the four supplement passages. The notes do not replace the RAW SCHOOL SOURCE; the point-map intake classifies each candidate point before it can support an answer.
- Audited the previously produced `ARC_N02_공통국어2_보충자료4편_V1.0.pdf` after user solve feedback that answers were too obvious and distractors were not competitive. Several option sets were confirmed as realism sentinels where the correct choice stood apart by relevance while alternatives were remote/direct reversals.
- Activated Korean Item Engine V1.2 and Korean Item QA V1.3. D3+ items now require key-hidden first-pass candidate ranking, at least two source-grounded strong distractors, a documented second-best option with decisive refutation, and an obvious-answer gate. D4/D5 immediate-elimination tolerance is tightened further.
- Added per-distractor proof fields (TRUE_KERNEL, DISTORTION_CLASS, WHY_TEMPTING, DECISIVE_FLAW, DECISIVE_EVIDENCE_REF) plus adversarial defense/rebuttal review so a distractor cannot self-label as strong without source-grounded evidence.
- Added and registered the user-found regression fixture `KOR_N_WEAK_DISTRACTOR_20260923_V1.yaml`; regression remains pending until a fresh model-generated Korean mini-set passes the new semantic gates. No production-quality PASS is claimed by this rule patch alone.

## 1.8.15-dev — 2026-09-23
- Re-opened the canonical three-page Korean supplement from Drive, verified its SHA-256, and added a page-level visual map for `탄궁가`, `팔원 - 서행시초3`, `기억할 만한 지나침`, and the Kant/Hegel article. Headings and page boundaries are verified; exact body transcription remains HOLD and no OCR guess is promoted to source truth.
- Re-opened and rendered all ten pages of the Social C worksheet. Visual review fixed three large handwritten-X exclusions: the power-separation confirmation figure and the Singer and Thoreau civil-disobedience blocks. The Rawls block remains included; incidental correction marks are not expanded into section exclusions.
- Corrected the active Social C policy from a non-blocking user filter to a blocking scope-exclusion gate. CORE/N canaries now explicitly avoid the three excluded regions and point to the canonical exclusion index.
- Executing the X-mark detector on the real worksheet exposed a missing OpenCV runtime dependency and a Hough-line array-shape failure. CI now installs OpenCV, the detector normalizes line output before iteration, and a raster-X-versus-blank smoke test prevents recurrence.
- Re-ran KOR and Social CORE/N synthetic canaries through QA, handoff, Typesetter, PDF and preflight. All four structural fixtures pass locally, but Korean exact-source production, Social B extraction, model-backed generation and user-approved release remain unclaimed.

## 1.8.14-dev — 2026-09-23
- Added a Drive-grounded Social A/B/C source inventory with canonical file IDs, filenames, page counts and SHA-256 values. A is source-locked; B visual extraction and C exact handwritten X-mark exclusion indexing remain HOLD, so no full-scope source-fidelity PASS is claimed.
- Added fixed synthetic Social CORE and N° canaries covering A justice/distribution, B globalization/population and C human-rights/constitutional judgment. CORE is four pages with each part on a fresh one-column page; N° is six pages with 10 questions, 10 answers and the required blank-page sequence.
- The first Social CORE render exposed a long Part C heading entering the right safety margin. The canary renderer now wraps major headings in a bounded text box and fails closed if the heading cannot fit; the same fixture was rerun with zero PDF failures and warnings.
- Generalized the fixed KOR canary runners so subject labels, filenames, QA evidence and outputs cannot be silently hard-coded to Korean when a Social fixture is selected. Re-ran KOR CORE/N° and Social CORE/N° after the change.
- Wired Social fixtures and the source inventory into CI and strict system validation. Synthetic structural PASS does not imply real school-source fidelity, Korean text fidelity, or user-approved problem-set release.

## 1.8.13-dev — 2026-09-22
- Added mandatory problem-prompt deduplication and final-user-approval governance. Generation must load prior approved/Drive history, build an exclusion registry, run exact and semantic duplicate checks, replace duplicates and recheck before presenting a candidate set.
- A final problem set remains `FINAL_USER_APPROVAL=PENDING` and `DRIVE_SAVE=BLOCKED` until the user explicitly approves it. Missing history access must be reported as `DUP_HISTORY_ACCESS=UNAVAILABLE`; it cannot be represented as a duplicate-check PASS.
- Registered the policy in the active Manifest so approval-before-save overrides zero-touch auto-save for problem-generation products.

## 1.8.12-dev — 2026-09-22
- Closed a QA-proof replay gap: ARC_N/ARC_FINAL Typesetter admission now requires a SHA-256 of the final STUDENT MANUSCRIPT in its sibling QA evidence file and matches the hash against the locked handoff. Proofs from a different manuscript with identical answer keys, or without a binding digest, fail closed.
- Re-ran fixed synthetic KOR CORE and N° pipelines and same-answer manuscript-swap fault injection. Actual school supplement text remains unverified; this change does not claim production Korean source fidelity.
- Updated Generator and Content Bundle contracts so future QA evidence emitters know how to calculate the required manuscript binding; this remains a contract and synthetic-runner check, not proof that every production generator already emits it.

## 1.8.11-dev — 2026-09-22
- Found and inspected the actual 3-page image-only school Korean supplement and 232-page teacher textbook; registered verified Drive IDs, SHA-256 values, and source readiness without declaring exact OCR/text fidelity. Supplement remains HOLD for visual line-by-line transcription; textbook usage remains unit 1 only.
- Typesetter admission now opens the sibling QA proof for ARC_N/ARC_FINAL, reruns executable content QA, and compares its subject, item count, and each answer with the locked handoff answer key. A missing or mutated proof, and a numerically complete but wrong answer key, are blocked before rendering.
- Re-ran the fixed KOR CORE/N° PDF canaries with QA readback; a synthetic canary PASS does not imply source-faithful Korean production readiness.
- Render-first review found distorted Latin glyph spacing in the synthetic PDF despite zero preflight findings. Both fixed canaries now embed regular/bold DejaVu fonts and verify embedded Unicode font streams; re-rendered CORE/N° retain their page-order and PDF-QC results. Korean glyph/font production verification remains HOLD.

## 1.8.10-dev — 2026-09-22
- Added a manifest-owned Typesetter gateway as the single executable admission point for HTML and ReportLab routes.
- The gateway runs handoff preflight, rejects inactive products, resolves the active PDF/HTML masters and PDF QC tools at runtime, and does not expose caller layout/template overrides.
- Added explicit ARC_CORE / ARC_N / ARC_FINAL profile isolation and route-consistency checks. HTML and ReportLab must share ruleset, product invariants, preflight and bounded auto-fix policy.
- Routed both fixed KOR CORE and KOR N° canaries through the gateway before PDF generation; independent canary-side Manifest profile selection is removed.
- Extended CI and static validation to compile and test the gateway and to trigger on Typesetter contract/template changes.

## 1.8.9-dev — 2026-09-21
- Added a bounded PDF preflight auto-fix controller. Only allowlisted Typesetter profile values may change; locked wording, answers, item counts and source text cannot be auto-mutated.
- Added loop guards: maximum two attempts, identical-fingerprint no-progress detection, unknown-defect HOLD and cross-product rule-leak HOLD.
- Connected the KOR CORE canary to an actual fail → classify → profile repair → re-render → PASS cycle by injecting an 8.5pt body defect and restoring the active 9.9pt token.
- Added explicit isolation coverage so a non-active `ARC_KOR_ANNOTATION` two-column writing-print request cannot enter the ARC CORE/N°/FINAL production serializer.
- Re-ran KOR CORE and KOR N° canaries after the Social A worksheet source-lock update; both remain CANARY_PASS.

## 1.8.8-dev — 2026-09-21
- Registered the two current 2026 통합사회2-A school worksheets in the canonical Drive A-part folder and locked their Drive IDs, filenames, byte sizes, page counts and SHA-256 values.
- Added a machine-readable Social A school-source registry and activated it through the system manifest.
- Split the former broad Social A scope into justice concepts, Aristotle, punishment theory and substantive distribution criteria so coverage and evidence can be audited independently.
- Social A generation now treats blank worksheet response cells as unfilled student activity space, forbids invented completion, and blocks BANK_PASS when the canonical source cannot be reopened or its integrity fields change.

## 1.8.7-dev — 2026-09-21
- Added a fixed 10-item KOR ARC_N canary that executes structural content QA, canonical serialization, handoff preflight, two-column typesetting, PDF rendering and PDF preflight.
- Added executable ARC_N page-order checks: cover verso must be completely blank, the page immediately before ANSWER KEY must be completely blank, and question/answer counts must equal the expected item count.
- Handoff preflight now parses the internal answer-key mapping and rejects missing, malformed or count-mismatched keys before Typesetter acceptance.
- The generated six-page canary follows COVER → BLANK → two problem pages → BLANK → ANSWER KEY, with 10 questions and 10 answers. Rendered preflight completed with zero failures and zero warnings.
- Added answer-key missing/short, stale PDF master and layout-directive fault injection. All four faults must be blocked for CANARY_PASS.
- This is a synthetic pipeline fixture; it does not claim school-supplement source fidelity or production question quality.

## 1.8.6-dev — 2026-09-21
- Added the canonical layout-blind CONTENT_BUNDLE → Markdown serializer. It pins the active ruleset, strips internal metadata, rejects layout authority, emits canonical filenames, and locks STUDENT MANUSCRIPT with SHA-256.
- Upgraded handoff preflight to V1.3. All products now require lifecycle metadata and verify the declared filename and manuscript checksum; stale PDF master, CSS/ReportLab geometry, font-size, column, and student-ID contamination are checked across the complete handoff.
- Added a fixed executable KOR CORE canary covering serializer → handoff gate → deterministic one-column PDF → PDF preflight, with 4-page output and explicit A/B/C major-boundary page starts.
- Added serializer fault injection for stale PDF master, two-column, 8.8pt body, and internal student ID. All four must be blocked for CANARY_PASS.
- Wired the serializer and KOR canary into GitHub Actions and retained the generated handoff/PDF/render/report as seven-day CI evidence. The canary uses synthetic English content and validates pipeline behavior only; it does not claim Korean source fidelity or model-authored content quality.

## 1.8.5-dev — 2026-09-21
- Activated Common Generation Engine V4.5 and the Universal Independent Solve & Difficulty Gate V1.0 for KOR/SOC/HIS/SCI/AI ARC_N and ARC_FINAL production.
- PASS B is now blind to ANSWER_KEY, PASS A, AUTHOR_INTENT and TARGET_DIFFICULTY. Every MCQ5 option must carry a verdict, semantic axis/key, evidence refs and competitiveness rating; exactly one TRUE option must match PASS A/B.
- Added required factual-accuracy, option-semantic-duplication, answer-evidence, scope-evidence, all-option, unique-answer and difficulty-match gates before CONTENT_LOCK.
- Difficulty is now measured again during PASS B. TARGET_DIFFICULTY must equal ACTUAL_DIFFICULTY after revision/reclassification; D4/D5 have executable reasoning, evidence, distractor and immediate-elimination minimums.
- Preserved the existing eight set gates: STRUCTURE, ANSWER_COUNT_MATCH, MANUSCRIPT_CONTAMINATION, TOO_EASY, MID_GAP, STRUCTURE_BIAS, D4_SHORT and PASSAGE_TRUNCATION.
- Added a machine-readable QA evidence schema and `tooling/content_qa/content_qa_gate.py` with behavioral smoke coverage for answer mismatch, semantic-key duplication, D4 inflation and Korean source-lock violations.
- Upgraded Generator Contract V1.8, Content Bundle Contract V1.6, QA Bench V1.6, Difficulty Engine V1.2 and Item Quality Rubric V1.4. ARC_N/FINAL handoff preflight now rejects missing QA evidence metadata/section.
- Activated Korean Master V4.2 and Korean Item QA V1.2. Student source text is EXACT-only and must come from user-provided or connected raw school textbook/supplement sources with file/location/checksum provenance. WHITESPACE_NORMALIZED and ARC/BANK/web/Deep Research/external problem-book source authority are forbidden.
- Wired the new runner and schema into CI and active-system validation. Local content-QA, handoff, PDF and system smoke checks pass. The model-backed 30-fixture Promptfoo candidate regression still requires a configured candidate adapter and is not claimed by this patch.

## 1.8.4-dev — 2026-09-20
- USER reassigned the PRIMARY SYSTEM MAINTAINER role from the ChatGPT interactive session to a dedicated Claude maintainer session. USER remains SYSTEM OWNER; GPT and other models become optional Generator/Reviewer/Auxiliary agents. ARC stays one unified system with no model-specific fork.
- Added MULTI-MODEL GOVERNANCE V1.1, CLAUDE HANDOFF V1.4, AUTOMATION RUNTIME V1.1 carrying the reassignment; the single-writer rule is now explicitly role-scoped, not model-scoped.
- Fixed configuration drift: AUTOMATION RUNTIME still declared subject priority KOR→SOC→SCI→HIS→AI and referenced RUNTIME_PRIORITY_POLICY V1.0. Both now match the manifest and V1.1 (KOR→SOC→HIS→SCI→AI).
- Added STORAGE TARGETS V1.1 with a per-subject product tree. Every active subject (KOR/SCI/SOC/HIS/AI) now has ARC_CORE, ARC_N and ARC_FINAL output folders in Drive, registered by folder ID, so product placement is decided by PRODUCT rather than by filename. HIS/SCI manuscript and review folders are registered for the first time, and the missing AI output folders were created.
- Registered forbidden product targets: 91_검증문항은행 (verified item bank) and My Drive root. Existing ARC CORE 통합사회2 output was relocated out of the item bank, and the released 통합사회 N°01 and 공통국어2 N°01 PDFs were moved into their product folders. 완성N제 is demoted to LEGACY_READ_ONLY for pre-ARC sets.
- Registered 98_정리대기 as the ROOT_STAGING cleanup folder.
- Drive mirror hygiene: six stale files carrying an `00_ACTIVE` label were renamed to 99_SUPERSEDED_/99_DEPRECATED_ so no runtime can mistake them for current rules. The v0.3 CORE PATCH mirror was the highest-risk one because it reintroduces the forbidden nine-block concept card.
- Drive ROOT_STAGING residue from the 통합사회 N°01 run was moved out of My Drive root into 98_정리대기 and labeled DUPLICATE / ORPHAN_STAGED.
- CI now runs `validate_system.py --strict-checksums`, so checksum drift fails the build instead of passing silently. Append-only RUN_LOG artifacts are excluded from the strict audit as ephemeral outputs.
- Regenerated CHECKSUMS.sha256; three entries (handoff preflight tooling and RUN_LOG) had drifted since 1.8.3-dev.

## 1.8.3-dev — 2026-09-20
- Added an executable stale-handoff gate. ARC CORE handoffs now fail before layout when they pin an old ruleset/PDF master, request two-column flow, prescribe body font size or concrete CSS/ReportLab geometry, expose internal IDs, or leave Social A/B/C part headings below level 1.
- Removed layout authority from Generator handoffs. The active SYSTEM_MANIFEST, PDF master, product patch, and Typesetter contract are resolved at render time.
- Level-1 headings inside ARC CORE STUDENT MANUSCRIPT now represent PART/MAJOR_TOPIC boundaries and start a fresh physical page. Social A/B/C parts are always separate page openings.
- Added duplicate-break and blank-page prevention. A registered boundary may explain a 25–45% previous-page remainder; pages below 25% still require within-part reflow.
- Added rendered-PDF detection for an explicit A/B/C part title that appears mid-page (`CORE_MAJOR_BOUNDARY_NOT_PAGE_START`).
- Added handoff and PDF behavioral smoke tests and wired both into CI. Local smoke tests and the active-system validator pass; representative Social/History re-typesetting remains required before main promotion.

## 1.8.2-dev — 2026-09-19
- Reworked ARC CORE typesetting after direct review of the user-provided Social and History CORE PDFs. The History artifact exposed ARC N°-style two-column leakage; the Social artifact exposed heading/carry-over and semantic page-flow defects.
- Baseline PDF inspection independently confirmed both reviewed CORE PDFs embed `NotoSansKR-Thin`; this converts the readability complaint into a verified font-weight regression, not a subjective-only styling issue.
- The new line-lane detector was calibrated against the same rendered PDFs: it flags History CORE pages 2–11 as two-column body flow while leaving the Social CORE pages unflagged, reducing table false positives.
- PDF metadata inspection confirms the two reviewed artifacts were produced by ReportLab, so the observed defects are not attributed to the legacy HTML template. Separately, the repository audit found `ARC_CORE_master_v0.2.html` used a fixed A4 height with `overflow:hidden` and 8.7pt body text; it is now retired in favor of v0.3 with visible overflow + source HOLD audit, explicit CORE namespace/one-column lock, and 9.9pt body tokens.
- Activated PDF Layout Master V2.4: ARC CORE main reading flow is now hard-locked to ONE_COLUMN with product-specific namespace requirements; ARC N°/FINAL two-column body rules may not leak into CORE.
- Added semantic pagination: Part/Chapter/Section openings, callouts, tables, figures, and synthesis blocks now have explicit keep/split semantics; headings require following body, table rows cannot split, figures cannot be clipped, and 1–3 line carry-over is a reflow priority.
- Activated CORE Template Patch v0.8 with a four-level Part → Chapter → Section → Functional Label hierarchy and print-first typography tokens.
- Activated Typesetter Contract V1.6 and added JIT `arc-typeset-qa` skill for product isolation, source overflow audit, semantic pagination, typography, and render-first visual QA.
- Activated PDF Preflight V1.2 policy and implementation. Preflight now accepts explicit PRODUCT_MODE and adds CORE two-column detection, vertical-interval occupancy, sparse/near-empty checks, body typography metrics, heading-orphan candidates, raw-markup and production-metadata leak detection.
- Added executable `tooling/pdf_qc/test_preflight_smoke.py` and wired it into GitHub Actions with PyMuPDF.
- Repaired stale system validation: `tooling/validate_system.py` now resolves the manifest-selected PDF master/CORE patch/preflight/typesetter instead of hardcoding V2.2/v0.6.
- Recorded four user-found layout incidents in ARC_ERROR_DATABASE and attached prevention/regression IDs.
- External design references used in REFERENCE_ONLY mode: `jelaludo/claude-skill-typography` for typography-token/audit concepts and `thedanielmay/visual-review-skill` for render-first/overflow/density QA concepts. No upstream code/text was copied; licenses were not established during intake.
- Corrected stale ARC N° answer-key sequence wording in the PDF master: required blank separator is LAST_PROBLEM+1 and answer key starts LAST_PROBLEM+2.
- The legacy full-tree CHECKSUMS.sha256 snapshot was found stale and line-ending-sensitive. Default CI now treats structural manifest validation + executable smoke as the gate; full-tree checksum audit is opt-in via `--strict-checksums` until that registry is deliberately regenerated.
- Main promotion remains blocked until CI/static validation and representative Social/History CORE re-typeset review are complete.

## 1.8.1-dev — 2026-09-19
- Optimized ARC PDF typesetting for print readability and page-flow quality after review of the Social CORE V0.2 draft.
- Upgraded PDF Layout Master to V2.3 with adaptive page reflow, page-occupancy auditing, orphan/widow control, raw HTML/Markdown sanitization, and student metadata leak checks.
- ARC CORE no longer permits a forced blank cover-verso page; near-empty unregistered pages below 25% effective content are release-blocking, while pages below 45% require reflow unless explicitly justified.
- Korean body typography now requires Pretendard/Noto Sans KR Regular(400) or heavier. Thin/ExtraLight/Light are forbidden for body, table text, captions, and running heads.
- Added print-first ARC CORE typography targets: body 9.6–10.2 pt, table/support 8.8–9.3 pt, body line-height roughly 1.45–1.60, and darker neutral body text.
- Upgraded CORE Template Patch to v0.7 with print-legibility, sparse-page, orphan/widow, and raw-markup gates.
- Upgraded PDF Preflight to V1.1 with sparse-page, font-weight, raw-markup, and production-metadata checks.
- Upgraded Typesetter Contract to V1.5. Reflow must redistribute content before shrinking fonts and may not fill whitespace with decorative cards.
- Activated FONT_WEIGHT_AUDIT, PRINT_LEGIBILITY, PAGE_OCCUPANCY_AUDIT, sparse-page reflow, and raw-markup leak gates in SYSTEM_MANIFEST.
- Static connector verification only; executable PDF preflight/regression was not run in this maintenance pass.

## 1.8.0-dev — 2026-09-19
- Added `ARC_PIPELINE_INTEGRITY_CONTRACT_V1.0` as the cross-cutting authority for Generator → Typesetter → Publisher, manifest-only version resolution, source/scope locks, answer integrity, checksums, and release-state transitions.
- Locked item generation to school-material priority, range containment, one unique answer, independent PASS A/B after every option shuffle, evidence-based difficulty calibration, similarity checks, functional/authentic visuals, and exact rendered-answer agreement.
- Locked CORE to chapter/cluster-first editorial architecture. Legacy v0.3 fixed nine-block cards, student-facing IDs/N° links, and mandatory optional blocks are explicitly forbidden.
- Removed legacy CORE card requirements from the active PDF master. CORE Typesetter acceptance now uses the locked manuscript, architecture summary, internal integrity index, and actual asset references.
- Resolved active-version drift: active subject MASTERs and Common V4.4 now defer to manifest-selected engines/templates instead of hardcoded older Common/PDF versions.
- Corrected Science MASTER answer handling so ARC_N includes the mandatory compact answer section after the required completely blank separator page.
- Preserved immutable ARC_N order: COVER → completely blank cover verso → problem pages → completely blank separator → answer key; preserved canonical ARC master logo hash lock and prohibited logo regeneration.
- Added the deprecation registry and `tooling/validate_system.py` to verify manifest targets, 1.8 runtime invariants, CORE anti-regression markers, mandatory answer behavior, frozen 30-fixture integrity, and full tracked-file checksum coverage.
- Extended CI smoke to compile the validator, validate the deprecation registry, and run system/checksum validation.
- Drive mirror debt remains explicit: `pending_sync` entries are not treated as current mirrors and do not override GitHub `dev`.

## 1.7.11-dev — 2026-09-19
- Added question task-form diversity as a required set-level quality dimension across ARC_N / ARC_FINAL.
- Upgraded COMMON_GENERATION_ENGINE to V4.4 with QUESTION_TASK_FORM and STEM_POLARITY planning before generation.
- Added task-form taxonomy including SINGLE_BEST_STATEMENT, EXCEPT_INCORRECT, MULTI_JUDGMENT, PAIR_MATCH, SEQUENCE_ORDER, CASE_APPLICATION, EVIDENCE_SUPPORT, ERROR_CORRECTION, DATA_INFERENCE, CONDITION_CHANGE, SOURCE_IDENTIFICATION, and COMPARISON_MATRIX.
- For 20+ item sets, default diagnostics now limit SINGLE_BEST_STATEMENT to 40%, SINGLE_BEST+EXCEPT to 60%, negative stems to 25%, require at least five task forms, and require at least 35% transformed task forms unless a subject MASTER justifies an override.
- Upgraded SET_EDITORIAL_ENGINE to V1.2 with QUESTION_TASK_DIVERSITY and flags for SINGLE_BEST_OVERUSE, NEGATIVE_OVERUSE, TASK_FORM_LOW_DIVERSITY, TASK_FORM_STREAK, and SURFACE_VARIATION_ONLY.
- Upgraded Korean Item Engine to V1.1 and Korean Item QA to V1.1. A 10-item Korean passage group now targets at least four task forms, at least two case/application items, limits simple single-best and negative-selection overuse, and blocks three consecutive identical task forms.
- Explicitly prevents superficial diversity where only the stem wording or polarity changes while the actual student task stays the same.
- SYSTEM_MANIFEST activated COMMON V4.4, KOR Item Engine V1.1, KOR Item QA V1.1, SET Editorial V1.2, and required task-form diversity gates.
- Static connector verification only; executable frozen-fixture regression was not run or claimed.

## 1.7.10-dev — 2026-09-19
- Upgraded Korean question generation with a dedicated passage-first item engine: engine/korean/ARC_KOREAN_ITEM_ENGINE_V1.0.md.
- Added required KOR passage mapping before generation, reasoning-depth classes, passage-utilization classes, duplicate-axis blocking, distractor-competitiveness gates, answer-length leakage audit, stem-diversity audit, and answer-pattern checks.
- Added quality/ARC_KOREAN_ITEM_QA_V1.0.md. Generic ITEM_QA PASS can no longer override failed Korean passage-utilization, duplicate-axis, distractor, or answer-length gates.
- Generator Contract V1.7 now loads manifest-declared subject-specific item engines and QA for ARC_N / ARC_FINAL.
- Korean release now requires KOR_PASSAGE_MAP, KOR_PASSAGE_UTILIZATION, KOR_REASONING_DIVERSITY, KOR_DUPLICATE_AXIS, KOR_DISTRACTOR_COMPETITIVENESS, KOR_ANSWER_LENGTH_AUDIT, KOR_STEM_DIVERSITY, and KOR_ANSWER_PATTERN to PASS before handoff.
- Current failure sentinels explicitly target direct-definition overuse, repeated judgment axes inside one passage group, weak/extreme distractors, correct-option length leakage, and mechanical 1-2-3-4-5 answer cycles.
- Reordered subject priority to KOR → SOC → HIS → SCI → AI.
- Extra-resource weights are now KOR 30 / SOC 25 / HIS 20 / SCI 15 / AI 10.
- Activated ARC_RUNTIME_PRIORITY_POLICY_V1.1 and subject-specific item-engine mode in SYSTEM_MANIFEST.
- Static connector verification completed. Executable frozen-fixture regression was not run or claimed.

## 1.7.8-dev — 2026-09-19
- Added mandatory portable Markdown handoff after every Generator completion.
- Generator V1.6 now requires HANDOFF_MD_STATUS=READY before READY_FOR_TYPESET is considered complete.
- Canonical filename: ARC_HANDOFF_<PRODUCT>_<SUBJECT>_<BATCH_ID>_READY.md.
- Content Bundle V1.5 defines one self-contained UTF-8 Markdown serialization containing front matter, student manuscript, product-specific answer key, visual/layout asset manifest, source-text payloads, QC state, and CORE architecture summary when applicable.
- Typesetter V1.4 can ingest the Markdown handoff directly without asking the user to paste the manuscript again.
- INTERNAL / DO NOT PRINT sections remain available to Typesetter but are excluded from student-facing output.
- The Markdown artifact and locked CONTENT_BUNDLE must be semantically identical; mismatch blocks handoff readiness.
- This maintenance pass used connector/static checks only; executable frozen-fixture regression was not claimed.

## 1.7.7-dev — 2026-09-19
- Reworked ARC CORE from concept-card-first generation to chapter/cluster-first editorial architecture.
- Added ARC_CORE_EDITORIAL_ARCHITECTURE_V2.0 with CENTRAL_QUESTION, CHAPTER_THESIS, DOMINANT_ORGANIZATION, BACKBONE_NODES, information hierarchy, anti-listing, redundancy budget, and one-synthesis principles.
- Upgraded ARC_CORE_CONTENT_ENGINE to V1.3 so macro architecture is built before concept writing.
- Upgraded ARC_CORE_DEPTH_ENGINE to V1.1 with cluster-first depth assignment to prevent advanced concepts from fragmenting into repeated mini-cards.
- Upgraded ARC_CORE_EDITORIAL_NATURALNESS to V1.2 with macro AI-pattern detection in addition to sentence-level style checks.
- Upgraded ARC_CORE_QA_BENCH to V1.2 with MACRO_COHERENCE, CHAPTER_BACKBONE_PRESENT, ANTI_LISTING, REDUNDANCY_BUDGET, and SYNTHESIS_TRANSFORMS gates.
- Upgraded ARC_TEMPLATE_SYSTEM CORE patch to v0.6: prose-first layout, fewer repeated cards, one primary synthesis per chapter, and no duplicate recap visuals.
- Upgraded ARC_GENERATOR_CONTRACT to V1.5 so ARC CORE route builds chapter architecture before concept maps and uses the manifest-selected Content Bundle contract.
- Upgraded ARC_CONTENT_BUNDLE_CONTRACT to V1.4: answer-key gates are now product-specific, while CORE carries architecture summary metadata for Typesetter without exposing it to students.
- Review basis: first Social and History ARC CORE PDFs showed strong factual density but excessive repeated summaries, warning blocks, tables, and recap cards. The new architecture targets that failure mode directly.
- Current Social CORE workflow override: handwritten C-part X-mark detection is non-blocking for CORE only, while ARC_N/FINAL keep strict X exclusion; Bentham is excluded from student-facing Social CORE unless explicitly restored.
- Connector-based static consistency checks only; executable frozen-fixture regression was not claimed.

## 1.7.6-dev — 2026-09-19
- Tightened final release approval after review of a real Claude production log.
- Generic positive reactions such as "좋아", "좋다니까", or "성공적이야" no longer count as evidence that a printed copy was physically reviewed.
- Added ARC_HUMAN_REVIEW_GATE_V1.2 with explicit physical-review evidence requirements.
- Added ARC_PRODUCTION_ORCHESTRATOR_V1.1 with release-approval disambiguation and canonical STORAGE_PLACEMENT=VERIFIED normalization.
- Added ARC_PUBLISHER_CONTRACT_V1.1 so Publisher cannot promote FINAL_RELEASED from ambiguous praise.
- Added ARC_CLAUDE_HANDOFF_V1.3 with the same physical-review language guard.
- Legacy STORAGE_PLACEMENT=PASS remains readable as an alias, while new output should use VERIFIED.
- No executable frozen-fixture regression was claimed in this connector-only maintenance pass.

## 1.7.5-dev — 2026-09-19
- Added ARC_PRODUCTION_ORCHESTRATOR_V1.0 with AUTO_CONTINUE_UNTIL_HARD_FAIL. Generator → Typesetter → Publisher transitions no longer require user confirmation after normal PASS states.
- Added ARC_PUBLISHER_CONTRACT_V1.0. Publisher is restricted to artifact integrity, locked-answer-table comparison, storage, exact parent verification, and release-state transitions; it may not independently re-grade answers or rewrite content.
- Added ARC_STORAGE_TARGETS_V1.0 as a central destination registry so registered KOR/SOC output folder IDs are resolved without asking again.
- Activated ARC_GENERATOR_CONTRACT_V1.4, ARC_CONTENT_BUNDLE_CONTRACT_V1.3, and ARC_TYPESETTER_CONTRACT_V1.3 with automatic end-to-end handoff while preserving role separation.
- Activated ARC_DRIVE_WRITE_ADAPTER_V1.2 with FILE_REFERENCE_FIRST binary upload. Inline base64 PDF upload is disabled by default; hosts with only expensive inline base64 use MANUAL_UPLOAD_REQUIRED without a redundant 1/2 choice.
- Activated ARC_HUMAN_REVIEW_GATE_V1.1. Physical HUMAN REVIEW is now explicitly a FINAL_RELEASE-only gate and does not block full typesetting, PDF QC, upload, or exact parent verification.
- Added ARC_N_TYPESET_REFERENCE_V1.0 using the digitally accepted Kant–Beccaria N° PDF as a reusable layout reference; repeated intermediate sample approval is skipped when the PDF master/brand system is materially unchanged.
- Activated ARC_CLAUDE_HANDOFF_V1.2 so end-to-end Claude/Cowork runs follow the same continuity, storage-target, binary-transport, and Publisher authority rules.
- Fixed Typesetter startup to resolve the active PDF master from SYSTEM_MANIFEST instead of hardcoding V2.1.
- No executable frozen-fixture regression was claimed in this connector-only maintenance pass.

## 1.7.4-dev — 2026-09-19
- Activated ARC_CORE_CONTENT_ENGINE_V1.2 with adaptive concept depth.
- Added ARC_CORE_DEPTH_ENGINE_V1.0 with internal STANDARD / ADVANCED / HIGH_DIFFICULTY priorities. Depth labels remain hidden from student-facing CORE.
- HIGH_DIFFICULTY now expands condition, boundary, premise, trap-logic, and multi-step reasoning only when supported by scope/evidence; it does not authorize out-of-scope enrichment.
- User-designated high-depth priorities: Social Kant–Beccaria punishment/death-penalty debate; Science OR redox and EM electromagnetic induction; Korean supplement-centered interpretation. History uses evidence-based difficulty-signal detection instead of a fixed hard unit.
- Science OR/EM depth remains bounded by SCIENCE_MASTER's ADVANCED LEAK BLOCK; high depth emphasizes data/condition reasoning rather than upper-grade formulas.
- Korean CORE source emphasis now prioritizes school supplements/worksheets and uses textbook content primarily for original text, foundations, and gap filling rather than repetitive re-summary.
- History CORE detects clusters with overlapping periods, similar organizations/policies, formation-split-unification, ideological relations, source-speaker inference, map/region coupling, and multi-period actors before increasing depth.
- Activated ARC_CORE_QA_BENCH_V1.1 with DEPTH_ASSIGNMENT, DEPTH_EVIDENCE, DEPTH_SCOPE_SAFETY, DEPTH_BUDGET, and HIGH_DIFFICULTY_COMPLETENESS gates.
- Activated ARC_CORE_EDITORIAL_NATURALNESS_V1.1 and ARC_TEMPLATE_SYSTEM_v0.5_CORE_PATCH so adaptive depth changes information density rather than adding repetitive "advanced/killer" badges or fixed deep-dive cards.
- Activated ARC_GENERATOR_CONTRACT_V1.3 with separate ARC_CORE and ARC_N/FINAL production routes.
- Activated ARC_CLAUDE_HANDOFF_V1.1. Claude now resolves active versions from SYSTEM_MANIFEST and loads a CORE-specific stack for PRODUCT_MODE=ARC_CORE instead of hardcoded legacy N° files.
- ARC_CORE subject MASTER use is scope/source/factual authority; N°-specific output, answer-key, distractor, and item-handoff clauses do not override the active CORE product contract.
- GitHub dev remains source of truth; new CORE/Depth mirrors are pending_sync.
- Executable frozen-fixture regression was not claimed in this connector-only maintenance pass.

## 1.7.3-dev — External skill intake addendum — 2026-09-19
- Added ARC_EXTERNAL_SKILL_INTAKE_POLICY_V1.0 for governed use of public GitHub skills when ARC has a capability gap.
- External skills are on-demand and remain below ARC scope/master/engine/QA authority.
- Default intake is REFERENCE_ONLY or ADAPT; automatic vendoring is disabled.
- License, executable-code, credential, network, write-capability, overlap, and instruction-conflict checks are required before adoption.
- Proprietary/source-available skills may be used only as design references unless a compatible license explicitly permits reuse.
- Registered the intake policy in SKILL_REGISTRY, skill governance, orchestration, and SYSTEM_MANIFEST.
- Initial design references: OpenAI official skills/skill-creator patterns for JIT loading and skill validation; Anthropic skills repository only where licensing permits, with proprietary document skills treated as reference-only.

## 1.7.3-dev — 2026-09-19
- Activated ARC_CORE_CONTENT_ENGINE_V1.1.
- CORE student output no longer exposes CONCEPT_ID, N° linkage, priority, BANK, QA, or internal source metadata.
- Replaced student-facing N° LINK with internal-only N_GENERATION_LINKS for future N° blueprint coverage and concept combination.
- Added evidence-gated TRAP blocks; unsupported or invented traps are removed instead of being shown to students.
- Added ARC_CORE_EDITORIAL_NATURALNESS_V1.0 to suppress repetitive card layouts, fixed block counts, repeated phrasing, redundant summaries, decorative boxes, and unsupported exam-prediction language.
- Added ARC_CORE_QA_BENCH_V1.0 with set-level AI-pattern sentinels, redundancy audit, TRAP evidence audit, student-view audit, and Korean-specific source/interpretation checks.
- Activated ARC_TEMPLATE_SYSTEM_v0.4_CORE_PATCH. CORE now uses paragraph-led reference-book flow with optional MUST / CONFUSING / TRAP / EXAM CONNECTION blocks instead of a fixed nine-block template.
- Korean CORE now follows KOREAN_MASTER_V4.1 SOURCE-BOUND ORIGINAL TEXT MODE: user-provided/uploaded or connected user-accessible school/textbook/supplement source text may be embedded as verified SOURCE_TEXT_BLOCK, preserving poem line/stanza and prose paragraph order.
- Korean CORE prioritizes whole-work flow and school-supplement interpretation structure over fragmented theme/emotion/expression cards.
- GitHub dev remains source of truth; the new CORE engine Drive mirror is pending_sync.
- Executable regression was not claimed in this connector-only maintenance pass.

## 1.7.2-dev — 2026-09-19
- Activated COMMON_GENERATION_ENGINE_V4.3 with SOURCE-BOUND TEXT EXCEPTION for user-pasted/uploaded and connected user-accessible school/textbook/supplement sources.
- Activated KOREAN_MASTER_V4.1. Korean ARC output now defaults to self-contained source presentation when the original text is actually available from an allowed source.
- Added SOURCE_TEXT_BLOCK with source provenance, inclusion mode, fidelity state, exact text body, and linked item IDs.
- Protected modern literary works may be included as VERBATIM_FULL or VERBATIM_RANGE when the text comes from a user-provided/uploaded or connected user-accessible source; web search/snippets/unverified external pages cannot authorize full protected-text reproduction.
- Added source-text fidelity checks for poem line/stanza order, prose paragraph order, completeness, source access, and question linkage.
- Activated Generator / Content Bundle / Typesetter contracts V1.2 and PDF layout master V2.2 for lossless source-text handoff and two-column pagination.
- Activated KOR_GOLD_ANCHORS_V1.1 and QA BENCH V1.5 with KOR-B04 source-text fidelity bench.
- ARC N° Korean source blocks may continue across columns/pages while remaining COLUMN_ONLY; Typesetter may not omit or rewrite source text to force fit.
- Korean ARC N° answer-key handoff was aligned with the current mandatory blank separator + compact final answer section.
- New GitHub rules are authoritative; Drive mirrors for new Common/Korean master remain pending_sync until explicitly mirrored.
- Executable frozen-fixture regression was not claimed in this connector maintenance pass.

## 1.7.1-dev — 2026-09-18
- Activated COMMON_GENERATION_ENGINE_V4.2 with natural five-choice answer-position planning: soft distribution bands, streak/periodicity flags, and mandatory re-verification after option shuffling.
- Added CLAIM_FIDELITY safeguards for thinker/theory items: explicit position vs supported implication vs opponent critique vs straw-man risk.
- Activated SOCIAL_MASTER_V4.1 with PHILOSOPHY_ATTRIBUTION, CRITIQUE_TARGET_FIDELITY, and ABSOLUTE_WORDING_AUDIT gates.
- Activated ARC_ITEM_QUALITY_RUBRIC_V1.3, ARC_SET_EDITORIAL_ENGINE_V1.1, and ARC_QA_BENCH_V1.4.
- Added SOC-B04 Kant/Beccaria punishment-theory bench target for attribution, critique fidelity, absolute wording, and answer-position distribution.
- Corrected manifest answer-key placement wording to AFTER_REQUIRED_SEPARATOR_BLANK, consistent with the required blank page before the answer section.
- Drive mirrors for the newly activated Common/Social masters are marked pending_sync; GitHub dev remains the rules source of truth.
- Executable 30-fixture regression was not claimed in this connector-only maintenance pass; release promotion still requires the existing regression gate.

## 1.7.0-dev — 2026-09-18
- ARC N° physical order locked to COVER → BLANK_COVER_VERSO → PROBLEM_PAGES → BLANK_BEFORE_ANSWER → ANSWER_KEY.
- Added mandatory ANSWER_KEY_COMPLETE / ANSWER_COUNT_MATCH release gates.
- Added immutable ARC logo registry with Drive IDs, pixel dimensions and SHA-256 hashes.
- Activated COMMON_GENERATION_ENGINE_V4.1 and ARC_PDF_LAYOUT_MASTER_V2.1.
- Activated Generator / Content Bundle / Typesetter contracts V1.1.
- Drive mirror/start docs updated; older active references retained only as superseded history.
- GitHub remains engine/rules source of truth; Google Drive remains school/source/bank/PDF storage.

# CHANGELOG

## 1.6.4-dev — 2026-09-18
- ARC N° physical PDF order is now fixed for duplex printing: cover → one completely blank cover-verso page → problem pages → answer key.
- The cover-verso blank page is a real A4 PDF page with no logo, header, footer, page number, note, watermark, or decoration; the first problem begins on physical page 3.
- ARC N° answer key now has a mandatory page break before it and starts on the immediate physical page after the last problem page, even when space remains on the final problem page.
- No extra blank spacer is inserted between the problem section and answer key.
- Added explicit PDF QC fields for blank-verso presence, first-problem physical page, and answer-key page placement.

## 1.6.3-dev — 2026-09-18
- ARC N° now includes a compact answer-key section at the end of the same student PDF by default; detailed explanations remain disabled.
- Problem pages still prohibit answer exposure.
- Reworked ARC N° cover into a left-aligned Swiss-editorial grid to avoid the previous floating centered composition.
- Locked cover full logos to exact canonical Drive assets for CORE / N° / FINAL.
- Logo retyping/redrawing/regeneration is forbidden; missing logo assets now return BRAND_ASSET_MISSING instead of synthesizing a substitute.
- Canonical ARC N° logo preserves the approved burgundy arc, both endpoint dots, wordmark geometry, divider, and N° label.
- Uploaded canonical full-cover lockup assets into `N제 시스템/00_브랜드/로고·디자인요소`.

## 1.6.2-dev — 2026-09-18
- Hardened ARC self-scoring against score/difficulty inflation after review of Claude KOR batch ARC-CLAUDE-20260918-KOR-01.
- Added ITEM QUALITY V1.2 with EXPLICIT_CUE_RESTATEMENT ceiling, distractor-distance audit, blind rescoring for BANK_A/D4/D5, and zero-rejection/premium-rate audits.
- Added DIFFICULTY ENGINE V1.1 with minimum D4/D5 gates and explicit-cue discount; long passages or the presence of a <보기> no longer count as difficulty by themselves.
- Added KOR high-difficulty gate requiring at least two genuinely competitive distractors and multi-step reasoning for D4/BANK_A.
- Added QA BENCH V1.3 adversarial D4 sentinels and set-level inflation checks.
- Added DRIVE WRITE ADAPTER V1.1 exact-file-ID parent verification. Root-level files may no longer be reported as STORAGE_PLACEMENT=VERIFIED for a subject folder.
- Repaired the reviewed Claude KOR PDF placement by moving its exact PDF FILE_ID into the canonical KOR 완성N제 folder.
- Existing Claude KOR batch remains a v1.5.0 DRAFT_REVIEW artifact; new rules apply to subsequent batches.

## 1.6.1-dev — 2026-09-18
- Added KOR PROTECTED_TEXT_MODE: protected modern literary works remain valid generation sources, but ARC outputs avoid full/long continuous reproduction and use school-source references when full text is required.
- Added STUDENT_SOURCE_REQUIRED / SOURCE_REFERENCE handoff behavior for protected works and prohibited invention of unseen wording or lineation.
- ARC N° problem pages are now strictly COLUMN_ONLY two-column layout.
- Removed ARC N° FULL_WIDTH and temporary one-column fallback for large passages, tables, graphs, maps, timelines, experiment diagrams, and composite visuals.
- Oversized ARC N° assets must be redesigned/split safely at content handoff or returned to Generator; Typesetter may not change layout mode to force fit.
- ARC FINAL and ARC CORE retain flexible layout only where their own active product rules permit it.

## 1.6.0-dev — 2026-09-18
- Split ARC production into dedicated Generator and Typesetter roles to reduce repeated context usage.
- Added ARC_GENERATOR_CONTRACT_V1.0, ARC_CONTENT_BUNDLE_CONTRACT_V1.0, and ARC_TYPESETTER_CONTRACT_V1.0.
- Generators now stop at CONTENT_QA_STATUS=PASS + CONTENT_LOCK=true + HANDOFF_STATUS=READY_FOR_TYPESET.
- Dedicated Typesetter sessions load only the locked bundle, PDF master, brand spec, and necessary layout/visual rules.
- Typesetters do not reload subject textbooks, worksheets, GOLD anchors, or generation QA by default.
- Locked content cannot be silently edited during layout; suspected content defects return via CONTENT_ERROR_FLAG.
- GPT and Claude may each serve as Generator or Typesetter, but one role is used per project/session.
- System maintenance remains exclusive to ChatGPT interactive SYSTEM_MAINTAINER.

## 1.5.0-dev — 2026-09-18
- Established permanent multi-model governance: GPT and Claude are recurring ARC generators; ChatGPT interactive maintenance is the single system/code/rule maintainer.
- Added `ops/ARC_MULTI_MODEL_GOVERNANCE_V1.0.md` with single-writer GitHub rules and append-only Drive production.
- Generator batches now pin ARC_RULESET_VERSION and use unique BATCH_ID metadata.
- GPT/Claude may both produce independent sets without overwriting each other.
- Generators may report SYSTEM_FEEDBACK but cannot patch MASTER/QA/templates/tooling during production.
- Claude absorption is persistent by ruleset version: full absorption on first use or relevant rule change, FAST_REFRESH otherwise.
- Scheduled GPT production is explicitly separated from interactive system maintenance.

## 1.4.7-dev — 2026-09-18
- Added a mandatory Claude/Cowork ARC system-absorption gate before first item generation in a fresh session.
- Claude must read the canonical manifest, common engine, requested subject MASTER/GOLD, QA/source rules, PDF master, brand lockup, and relevant Drive structure before claiming readiness.
- Added explicit user override allowing an independent Claude KOR batch even when a GPT KOR batch exists.
- Added canonical KOR/SOC manuscript, QA, and finished-N° Drive destinations for Claude E2E production.
- Claude-produced PDFs default to DRAFT_REVIEW and are intended for user + ChatGPT post-production review before any ARC rule/template change.

## 1.4.6-dev — 2026-09-18
- Added `ops/ARC_CLAUDE_HANDOFF_V1.0.md` so Claude can generate ARC batches from the same GitHub/Drive source-of-truth without maintaining a separate ARC fork.
- Added required generator attribution and BATCH_ID metadata for GPT/Claude batch coordination.
- Added duplicate-batch avoidance across generators.
- Default multi-model mode is throughput-first: one primary generator per batch, no universal cross-model regrading, selective independent review only for high-risk items.
- Claude starts production first for the current cycle; GPT resumes later by skipping fresh Claude batches.

## 1.4.5-dev — 2026-09-18
- Diagnosed the 18:57 QA failure: root native-Doc creation and read succeeded, but background Drive metadata move was blocked by a safety check.
- Scheduled QA no longer performs Drive parent mutations.
- Added ROOT_STAGING as the scheduled persistence mode: create/write/read at provider root, record intended target folder, and defer folder organization to interactive maintenance.
- The first real RAW shell now doubles as the persistence preflight, eliminating disposable probe overhead.
- RAW generation is checkpointed every 5 items.
- Hourly QA now targets at least one fully QA-complete 20-item subject per run and continues to the next subject only if runtime remains, avoiding fragile 100-item monolithic transactions.
- ROOT_STAGED artifacts count as compute persistence success but are not reported as full storage placement success.

## 1.4.4-dev — 2026-09-18
- Locked the approved ARC master logo/sub-brand system into the template layer.
- ARC wordmark and burgundy arc symbol are now identical across CORE / N° / FINAL.
- Divider geometry, label baseline, spacing, and overall lockup proportions are fixed across all three product variants.
- Product differentiation is restricted to secondary label/divider color: CORE warm gray, N° deep navy, FINAL burgundy.
- N° may receive limited optical glyph compensation while retaining the same label zone.
- Cover volume numbers are separate metadata and no longer distort the ARC N° lockup.
- PDF and CORE template rules now reference ARC_BRAND_LOCKUP_SPEC_V1.0.

## 1.4.3-dev — 2026-09-18
- Added mandatory one-time Drive write preflight before any expensive subject generation.
- Verified OAuth/delegated persistence end-to-end: root native Doc creation → parent read → addParents/removeParents move → content write → destination verification.
- Canonicalized Drive persistence on `ops/ARC_DRIVE_WRITE_ADAPTER_V1.0.md`; the duplicate persistence-policy file is now a deprecated alias.
- Scheduled runtime now defaults to CREATE_THEN_MOVE after a connection-capability mismatch and does not repeatedly retry unsupported direct parent creation.
- QA generation stops before consuming item-generation budget when persistence preflight fails.

## 1.4.2-dev — 2026-09-18
- Diagnosed RUN10 failure as a Drive persistence adapter incompatibility, not an item-QA failure.
- OAuth/delegated native Google Doc creation rejects direct `parent_folder_id` placement on the connected Drive.
- Added ARC_DRIVE_WRITE_ADAPTER_V1.0: create at provider root/default, persist FILE_ID, move with addParents/removeParents, then verify destination.
- Folder-placement failure after durable creation no longer destroys or aborts completed subject work; it becomes MOVE_PENDING with one repair retry.
- Moved RUN10 failure log into the canonical failure folder.
- Verified the new create-then-move path end-to-end with a native Google Doc smoke test in the RUN_LOG folder.
- Scheduled QA should use CREATE_THEN_MOVE by default when connection mode is unknown.

## 1.4.1-dev — 2026-09-18
- Added lightweight SCHOOL_REFERENCE_PROFILE; historical exams remain difficulty/broad-format references only and teacher-style prediction stays disabled.
- Added dormant POST_EXAM_CALIBRATION skeleton for use only after the real exam is available.
- Added GitHub Actions smoke checks for Python syntax, YAML parsing, and exact 30-fixture loading.
- Completed manifest wiring for the executable tooling layer.

## 1.4.0-dev — 2026-09-18
- Added executable tooling layer instead of policy-only checks.
- Added promptfoo regression runner for the 30 frozen fixtures with side-by-side baseline/candidate adapters and decision/score/hard-fail assertions.
- Added sentence-transformers + local Qdrant similarity engine with FULL/STEM/DISTRACTOR embeddings and structural metadata.
- Similarity thresholds now require labeled BANK calibration; raw cosine does not become a hard gate before calibration.
- Added PyMuPDF PDF preflight for page-boundary, margin, overlap, glyph, image/drawing, empty-page and render screening.
- Added Social C-part X-mark detector: PDF annotations → vector diagonal crossings → OpenCV raster fallback.
- Added deterministic visual renderer for graphs, particle models and major social diagrams plus an independent visual PASS B verifier.
- Added mandatory Visual PASS A/B + QUESTION_VISUAL_CROSSCHECK for essential visuals, including REDOX_LEDGER ↔ particle-count cross-check.
- Expanded social visual specification to MAP/STAT/DATA/FLOW/CASEBOX/COMPARE/INSTITUTION with explicit required fields and hard checks.
- Upgraded active visual template/authenticity/anchors and similarity guard to V1.1.
- Added runtime truthfulness rule: connector-only environments must report TOOLING_UNAVAILABLE rather than pretending local tools executed.

## 1.3.4-dev — 2026-09-18
- Added ARC_RUNTIME_PRIORITY_POLICY_V1.0.
- Default subject execution order is now KOR → SOC → SCI → HIS → AI.
- Normal 100-item QA still targets 20 items per subject; priority controls order, retries, extra review, research, and context allocation.
- Added recommended extra-resource weights 30/25/20/15/10.
- Added stage priorities P0–P5 and explicit degradation order: defer P5, then nonessential P4, then nonessential P3; P0–P2 are never skipped.
- Subject failures are isolated, checkpointed, and resumed after the first pass instead of terminating the entire run.
- Default retry budget is one automatic retry per failed subject/stage.

## 1.3.3-dev — 2026-09-18
- Added frozen regression fixture system.
- Registered 30 fixed cases: 5 subjects × GOOD 3 + BAD 3, referenced from the subject GOLD anchor packs.
- Each fixture now has a fixed expected decision, score range/ceiling, and hard-fail expectation.
- Added ARC_REGRESSION_POLICY_V1.0 and upgraded arc-eval-regression to run all fixtures for engine/MASTER/QA/source/bank-rule changes.
- Added QA BENCH V1.2; main promotion now requires REGRESSION_FAIL_COUNT=0.
- Regression fixtures are versioned and cannot be silently rewritten to make a candidate rule pass.

## 1.3.2-dev — 2026-09-18
- Added ARC SOURCE_LEDGER V1.0 and machine-readable schema.
- Source-sensitive claims now carry SOURCE_ID, source role, location, and one of VERIFIED / UNVERIFIED / SOURCE_MISSING.
- PASS B must re-open the original source for ANSWER_BASIS claims; search snippets, filenames, and previous AI summaries cannot establish VERIFIED.
- Added Drive checkpoint folder `92_자동화실행/04_SOURCE_LEDGER`.
- BANK_PASS is blocked when required answer-basis sources are unverified, missing, conflicting, or not reopenable.
- Basic low-risk curriculum definitions do not require source records, avoiding unnecessary ledger overhead.

## 1.3.1-dev — 2026-09-18
- Added mandatory HUMAN_REVIEW_GATE before FINAL release of ARC N°/FINAL/CORE PDFs.
- Human review is intentionally lightweight: scope, Social C X-mark exclusion where applicable, rendered visuals, and answer/final-PDF sanity only.
- AI remains responsible for full answer verification, fact checks, data checks, and render QC before human review.
- Added DRAFT_REVIEW → HUMAN_REVIEW → FINAL_RELEASED state contract.
- Added FAST_HUMAN_REVIEW for exam-period use with high-risk items capped at five.

## 1.3.0-dev — 2026-09-18
- Added fixed GOLD STANDARD anchor system for all five active subjects.
- Each subject now has 3 GOOD + 3 BAD ARC-original example items with expected scores, decisions, and explicit reasons.
- Subject MASTER files now require their GOLD anchor pack during generation and QA.
- Item generator/QA/runtime record nearest GOOD/BAD anchor and apply BAD score ceilings before BANK decisions.
- Anchors calibrate structure, reasoning, distractor realism, and evidence use without expanding scope or copying copyrighted source items.

## 1.2.2-dev — 2026-09-18
- Diagnosed RUN09 scheduled QA failure: run folder created, then execution stopped before first subject artifact write.
- Added checkpointed automation runtime policy with per-subject JIT loading and persist-first behavior.
- Scheduled runs now prefer native Google Docs for RAW/QA/BANK/log artifacts.
- Added ITEM QUALITY V1.1 anti-inflation ceilings and evidence-required scoring.
- Added QA BENCH V1.1 sentinel recheck and score-distribution audit.
- Added BANK POLICY V1.1: pre-V1.1 BANK remains stored but is inactive until V1.1 revalidation.
- Direct recall, weak distractors, generic contexts, and ungrounded style can no longer receive inflated PREMIUM scores.
- Automation failures must preserve partial progress and resume targets instead of reporting success.

## 1.2.1-dev — 2026-09-18
- MCP server registration changed to persistent-by-default.
- Connections remain available when the host supports persistence; actual tool invocation stays on-demand.
- Added startup health checks and automatic reconnect policy.
- Avoids preloading every MCP tool into working context, preserving token efficiency.

## 1.2.0-dev — 2026-09-18
- Added ARC MCP Tool Layer.
- Registered GitHub official MCP, draw.io official MCP, ChemCP, and Timeline Generator MCP.
- GitHub MCP is read-only by default during question-generation runs; write tools are reserved for explicit system maintenance.
- Google Drive remains on the existing connector and third-party Drive MCP is disabled.
- Added MCP security policy, server registry, orchestration, host setup examples, and fallback matrix.
- MCP tools are on-demand only and never override Scope Lock, MASTER, QA, or difficulty rules.

## 1.1.2-dev — 2026-09-18
- Added Reference-First visual protocol: inspect real textbook/school exam/worksheet/workbook visuals before rendering.
- Visuals now extract layout grammar, density, labeling, and print conventions without copying source artwork.
- Added reference-gap and copy-risk gates to visual QA.
- Updated visual anchors priority to include current-range textbook explicitly.

## 1.1.1-dev — 2026-09-18
- Added verified visual skill stack: draw.io base, concept diagrams, chemistry visuals, and timeline visuals.
- Upgraded `arc-visual-renderer` into a router skill.
- Added `ARC_VISUAL_SKILL_STACK_V1.0.md` for subject/type-based routing.

## 1.1.0-dev — 2026-09-18
- Added on-demand ARC skill layer with 13 project-specific skills.
- Added source ingest for PDF/HWP/HWPX/Office-style structured materials.
- Added research grounding and claim-ledger workflow.
- Added item generation, distractor design, factual audit, item naturalness audit, item QA, set editorial, visual rendering, bank curation, regression evaluation, skill orchestration and governance.
- Added `ARC_SKILL_ORCHESTRATION_V1.0.md` and `SKILL_REGISTRY.yaml`.
- Explicitly disabled learner-adaptive wrong-answer regeneration and personal weakness tracking.
- External skill projects are design references only; no upstream scripts/code vendored.

## 1.0.0 — 2026-09-18
- GitHub-first engine architecture initialized.
- `SYSTEM_MANIFEST.yaml` added.
- `main` RELEASE / `dev` development workflow added.
- RUN_LOG JSONL + CSV initialized.
- ARC CORE detailed concept engine included.
- CONCEPT_ID → N° linkage enabled.
- School historical exams restricted to difficulty calibration.
- Teacher-style prediction disabled.
- Freeze mode intentionally not added.


## 2026-09-24 — N° / FINAL Dongbuk difficulty & distractor hardening
- Activated COMMON_GENERATION_ENGINE_V4.6, ARC_DIFFICULTY_ENGINE_V1.3, ARC_ITEM_QUALITY_RUBRIC_V1.5.
- Added ARC_FINAL_QUALITY_GATE_V1.0 as a mandatory FINAL release gate.
- Added universal attractive-distractor requirements: D3+ requires at least two strong distractors and at least three first-pass plausible candidates; D4/D5 require effective choice count >= 4.
- Added answer-length/detail bias audit. A uniquely longest correct option with >=1.25 longest/median ratio is a hard-revise condition when extra length is not structurally necessary.
- Added set-level longest-option-is-key audit (>30% revise, >40% fail).
- Raised Dongbuk default ARC_N difficulty floor to D4+D5 >=35% and D1+D2 <=25%, subject to verified school-anchor calibration.
- Added ARC_FINAL difficulty profile floor with D4+D5 target >=30%, no unjustified BELOW_SCHOOL items, and late-section discrimination requirements.
- CORE remains maintenance-only; quality development priority is N° and FINAL.


## 2026-09-24 — Midterm scope compression for deadline
- Activated ARC_RUNTIME_PRIORITY_POLICY_V1.2.
- Science is now hard-locked to oxidation-reduction only for generation, research, N°/FINAL, canary, and regression work in the current sprint.
- Korean History is now ARC_N-only for the current sprint; HIS FINAL work is deferred.
- Current RC target is KOR N°/FINAL + SOC N°/FINAL + HIS N° + SCI-REDOX N°/FINAL.
- CORE remains maintenance-only.


## 2026-09-24 — Product readiness floor locked at 80%
- Added ARC_PRODUCT_READINESS_GATE_V1.0.
- ARC_N readiness is the minimum of KOR_N, SOC_N, HIS_N, SCI_REDOX_N.
- ARC_FINAL readiness is the minimum of KOR_FINAL, SOC_FINAL, SCI_REDOX_FINAL.
- Each subject/product readiness score uses five evidence-backed 20-point gates: scope/source, generation quality, QA/governance, E2E/PDF, regression/release.
- 2026-09-25 RC requires both ARC_N_PRODUCT_READINESS >=80 and ARC_FINAL_PRODUCT_READINESS >=80.
- Scores cannot override hard failures such as wrong-answer risk, out-of-scope evidence, duplicate leakage, FINAL difficulty failure, or PDF corruption.


## 2026-09-25 — Korean-first exam realism hardening
- Priority order changed to KOR N°/FINAL → SOC N°/FINAL → SCI-REDOX N°/FINAL → HIS N°.
- KOR receives 50% of remaining discretionary quality allocation until its realism/quality gates pass.
- Added KOR_DONGBOOK_EXAM_TYPE_PROFILE_2025_2026_V1.0 from four accessible Dongbuk Korean exams; historical exams calibrate task-form prevalence and difficulty only, never answer content or teacher intent.
- Added ARC_KOREAN_EXAM_REALISM_GATE_V1.0 and executable smoke gate.
- Activated KOREAN_MASTER_V4.4, KOREAN_ITEM_ENGINE_V1.4, KOREAN_ITEM_QA_V1.5.
- Korean release now blocks AI-style internal QA language, artificial wrapper use, mechanical option prose, answer-length cues, repeated stem skeletons, and exotic-task overuse.
- Registered ARC_N03 as a realism re-audit sentinel; fresh model-backed N°/FINAL must pass before Korean realism regression is closed.


## 2026-09-25 — Korean absolute-priority sprint
- Activated ARC_RUNTIME_PRIORITY_POLICY_V1.4.
- Remaining discretionary quality allocation is KOR 60 / SOC 20 / SCI-REDOX 12 / HIS-N 8.
- Korean N°/FINAL must produce a fresh meaningful result, not only rule-document changes.
- Fresh KOR closure requires school-task realism, AI-style leak removal, strong distractors, answer-length neutrality, dedup, and full E2E PDF verification.
- Priority order is now KOR N°/FINAL → SOC N°/FINAL → SCI-REDOX N°/FINAL → HIS N°.


## 2026-09-26 — FINAL difficulty recalibrated from all supplied Dongbuk exams
- Audited 16 actual Dongbuk High School exam PDFs: four KOR, four SOC, four SCI, and four HIS papers across 2025-2 and 2026-1 mid/final terms.
- Added DONGBUK_ACTUAL_EXAM_DIFFICULTY_CORPUS_V1.0 with structural difficulty profiles and confidence labels.
- Replaced the single 2025-2 KOR-mid FINAL anchor with subject-specific multi-exam ensembles.
- KOR FINAL center: D12 34.3%, D3 40.0%, D45 25.7%, mean 2.89.
- SOC FINAL center: D12 31.0%, D3 47.2%, D45 21.8%, mean 2.87.
- SCI-REDOX FINAL center: D12 30.1%, D3 39.1%, D45 30.8%, mean 2.97; direct 2025-2 mid redox items 8-12 receive 65% relevance weight.
- HIS difficulty ensemble is diagnostic only because HIS FINAL is outside the active sprint.
- ARC_N no longer has to match the school's exam difficulty distribution. N° keeps its basic→standard→advanced learning ladder and balance/quality gates.
- ARC_FINAL now requires SCHOOL_MULTI_EXAM_ANCHOR calibration and fails closed when the subject anchor is missing.
- Student correct-rate data is not available; these profiles are structural difficulty calibration, not psychometric difficulty claims.

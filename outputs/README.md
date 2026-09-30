# outputs — 산출물 세트와 파이프라인

각 폴더 = 한 세트. PDF와 `src/`(원고·조판 스크립트)를 함께 둔다. 지문 원문은 `sources/`에서 import한다(복사 금지).

| 폴더 | 내용 | 원고 → 조판 |
|---|---|---|
| `KOR/ARC_N06~N09_…` | 보충자료 4편 40문항 | `content.py` → `build.py` |
| `KOR/ARC_N08_…` | N08 + 간단 해설 | + `explain.py` |
| `KOR/ARC_N10_1단원_80Q` | 교과서 1단원 80문항 | `passages.py`, `items.py` → `build.py` |
| `KOR/ARC_N11_시험범위11편_110Q` | 시험 범위 11편 × 10 (V1.1: 선지 재구성, D2 없음) — 문제지·정답표·해설·**합본** | `items_a/b/c.py` + `revise_a~e.py` → `apply_rev.py` → `build_n11.py`, `make.sh` |
| `KOR/ARC_N12_보충자료4편_핵심40Q` | 보충 4편 핵심 40 (V1.1) — 3종 PDF + **합본** | `items_n12.py` + `revise_n12.py` → `apply_rev.py` → `build_n12.py`, `make.sh` |
| `KOR/ARC_FINAL_공통국어2_N01/N02` | 시험 모사: 선택형 22 + 서·논술형 4 | `items_final*.py` → `build_final.py` |
| `KOR/ARC_CORE_보충자료4편` | 개념서 V1.2 | `core_content.py` → `build_core.py` |

## 새 세트 만드는 순서
1. 가장 가까운 세트의 `src/`를 복사한다 (N 계열은 N11, 시험 모사는 FINAL).
2. 지문은 `sources/<과목>/`에서 import, 표기(㉠~㉤)는 문항에 맞춰 지문 문자열에 삽입.
3. 중요한 문항은 이전 세트 문항을 먼저 진화시킨다(선지 재구성·발문 변경, 계보 기록). 새 문항은 필요한 곳에만 만든다.
   문항 원고 작성 시 `quality/ARC_DISTRACTOR_ENGINEERING_V1.0.md`의 단일 변이 규칙을 따른다.
4. **납품 전 `python3 quality/tools/option_cue_lint.py <세트 이름>`** 실행. 새 세트는 도구의 `REGISTRY`에 등록한다.
5. `src/make.sh`로 빌드 → PDF → **문제지+답지 합본**(`quality/tools/bundle_pdf.py`) → 시각 점검 → `ops/RUN_LOG.*` 기록 → 커밋.

## 규칙
- PDF 외의 생성물(`src/*.html`, `__pycache__`)은 커밋하지 않는다.
- D등급 라벨은 배점에서 역산하지 않는다(난이도 엔진 LABEL INTEGRITY).
- **문제지와 답지는 항상 함께**: 모든 세트는 `…_문제지+답지.pdf` 합본을 만든다(문제지 → 정답표 → 해설/채점 기준). 규칙: `quality/ARC_PAIRED_DELIVERY_V1.0.md`.

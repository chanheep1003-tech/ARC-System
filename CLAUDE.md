# ARC-System 작업 메모

- 출제 지문: `sources/<과목>/` 라이브러리를 먼저 import (예: `sources/KOR/공통국어2/unit1.py`, `supplement4.py`). Drive 교과서 PDF는 텍스트층이 없어 재추출 금지.
- 새 지문을 Drive에서 추출했다면 라이브러리 모듈에 추가 → `export_md.py`로 md 재생성 → Drive `ARC_지문라이브러리_공통국어2` 폴더(`1n5ZBALgxepDFrwXFS5yRiSCIsb3HQz6y`)에도 반영.
- 조판 파이프라인: `outputs/KOR/ARC_N10_1단원_80Q/src/` (build.py → HTML, pdf.js → Playwright PDF)를 복사해 시작. 정답 위치는 items `_assign()` 무작위 균등 배치.
- 실행 로그: `ops/RUN_LOG.jsonl` + `ops/RUN_LOG.csv`에 run 1건씩 추가.
- ARC FINAL: `outputs/KOR/ARC_FINAL_공통국어2_N01/src/` (passages_final.py → items_final.py → build_final.py, pdf.js). 시험 범위 지문은 `sources/`에서 import, 선택형+서·논술형 구성·배점 합(80+20)과 정답표/채점기준 PDF를 함께 생성.
- ARC FINAL N°02: `outputs/KOR/ARC_FINAL_공통국어2_N02/src/` (passages_final2.py → items_final2.py → build_final.py). 개수형·ㄱ~ㅁ·표 정오·사례 적용으로 난도 상향. 난이도 검사 결과는 각 폴더의 `난이도검사_*.md`.
- ARC N°11: `outputs/KOR/ARC_N11_시험범위11편_110Q/src/` (items_a/b/c.py → build_n11.py; 문항마다 해설 `e` 포함, pdf.js가 문제지·정답표·해설 3종 출력).
- ARC N°12: `outputs/KOR/ARC_N12_보충자료4편_핵심40Q/src/` (N°11 파이프라인 복사: items_n12.py → build_n12.py).
- **문항 출제 전 필독**: `quality/ARC_DISTRACTOR_ENGINEERING_V1.0.md` (선지는 정답의 한 요소만 바꿔 만든다, 길이·구조·구체성 평준화). 납품 전 `python3 quality/tools/option_cue_lint.py <세트>` 통과 필수, 새 세트는 도구 REGISTRY에 등록. D등급은 배점에서 역산 금지.
- 산출물 지도는 `outputs/README.md`.
- **재사용 정책**: 새 세트가 이전 세트와 겹쳐도 된다. 핵심 문항은 이전 문항을 선지 재구성/발문 변경(EVOLVE)으로 개선해 재사용하고 계보(parent/change/delta)를 남긴다. 무개선 복붙(COPY)은 세트의 10% 이하. (quality/ARC_SIMILARITY_GUARD_V1.0.md §6)
- **문제지와 답지는 항상 함께 조판·납품**(합본 `…_문제지+답지.pdf` = 문제지+정답표가 기본 산출물, **해설은 합본에 넣지 않고 별도 PDF**). 세트 `src/make.sh` = 빌드 → PDF 3종 → `quality/tools/bundle_pdf.py`로 문제지+정답표 합본. 규칙: `quality/ARC_PAIRED_DELIVERY_V1.0.md`.
- FINAL N°01(V1.2)·N°02(V1.1)도 `revise_final.py` → `apply_rev.py`로 개정본을 빌드에 적용한다(`src/make.sh`). 난이도 재검사: `python3 quality/tools/final_difficulty_recheck.py`.
- N°11·N°12는 V1.1(선지 재구성, D2 배제): 원고는 `items_*.py`(V1.0 계보) + `revise_*.py`(선지·표·<보기> 덮어쓰기) → `apply_rev.py`가 빌드·린트에서 공통 적용. 문항 수정은 `revise_*.py`에서 한다.


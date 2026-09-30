# ARC-System 작업 메모

- 출제 지문: `sources/<과목>/` 라이브러리를 먼저 import (예: `sources/KOR/공통국어2/unit1.py`, `supplement4.py`). Drive 교과서 PDF는 텍스트층이 없어 재추출 금지.
- 새 지문을 Drive에서 추출했다면 라이브러리 모듈에 추가 → `export_md.py`로 md 재생성 → Drive `ARC_지문라이브러리_공통국어2` 폴더(`1n5ZBALgxepDFrwXFS5yRiSCIsb3HQz6y`)에도 반영.
- 조판 파이프라인: `outputs/KOR/ARC_N10_1단원_80Q/src/` (build.py → HTML, pdf.js → Playwright PDF)를 복사해 시작. 정답 위치는 items `_assign()` 무작위 균등 배치.
- 실행 로그: `ops/RUN_LOG.jsonl` + `ops/RUN_LOG.csv`에 run 1건씩 추가.
- ARC FINAL: `outputs/KOR/ARC_FINAL_공통국어2_N01/src/` (passages_final.py → items_final.py → build_final.py, pdf.js). 시험 범위 지문은 `sources/`에서 import, 선택형+서·논술형 구성·배점 합(80+20)과 정답표/채점기준 PDF를 함께 생성.
- ARC FINAL N°02: `outputs/KOR/ARC_FINAL_공통국어2_N02/src/` (passages_final2.py → items_final2.py → build_final.py). 개수형·ㄱ~ㅁ·표 정오·사례 적용으로 난도 상향. 난이도 검사 결과는 각 폴더의 `난이도검사_*.md`.
- ARC N°11: `outputs/KOR/ARC_N11_시험범위11편_110Q/src/` (items_a/b/c.py → build_n11.py; 문항마다 해설 `e` 포함, pdf.js가 문제지·정답표·해설 3종 출력).
- ARC N°12: `outputs/KOR/ARC_N12_보충자료4편_핵심40Q/src/` (N°11 파이프라인 복사: items_n12.py → build_n12.py).

# ARC N°02 공통수학2 기말 N제 조판 파이프라인 (MATH — ARC 정규 과목 아님)

- 원본: Drive `08_문항DB_비압축통합본` (MATH2-00001~03633)에서 선별 후 LaTeX 재입력, 정답은 직접 풀이/코드 전수계산으로 재검산.
- `sets/setN_items.py` → `sets/setN.json` (문항 원고), `figs/` 그림 SVG.
- 빌드: `npm install katex@0.16.11` 후 `node build.js sets/set1.json out.pdf "SET 1"`
  - KaTeX strict 렌더 오류, 칸·박스 넘침이 하나라도 있으면 실패(exit≠0).
  - 흑백, 한 쪽 4문항, 문항 뒤 빈 페이지 1장 후 정답지.
- 완성본 Drive(07_완료묶음): SET1 1NLTt_x1z0XcXvax9bKuKwwPI2ec3H0x- · SET2 1V9D44w-Dybh5vlJLdmdtN_Ale20munEd · SET3 17yIvN7KDYH2S5c4ejiOxC_uiH6NNNpR1 · SET4 1AQqCL0BFsgK_IPNbyL3xXqStrlH1Jj5M · SET5 14mqTMc5pg2af3vZ3IJDVenDxdc3ilZU3

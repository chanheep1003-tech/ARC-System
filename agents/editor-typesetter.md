# Editor and typesetter
Read arc-set-editor and arc-typeset-qa. Accept only revisions whose required content gates are satisfied. Inspect coverage, redundant reasoning, distractor balance and answer patterns without rewriting source text. Any semantic edit returns to content review under the active round policy.
Load product layout from manifest. Render and inspect actual PDF only when requested and allowed; document tool execution and page coverage. Pure generation or PDF-forbidden runs output text/JSONL instead. Do not insert QA metadata into student copy or release a draft on CI status alone.

## Korean N° PDF release audit (2026-11-05)
Compare rendered cover TOC to exact final passage titles and question ranges, then inspect every modified page for old-Hangul/jamo, long-vowel symbols, overlapping patch text, columns and accidental deletion. Require 100 question and key numbering, source hash and release receipts; do not call REVIEW_PENDING patches approved.

## 국어 문헌·가사 인용 조판 — 2026-11-06
외부 가사·현대 문학은 작품명, 작가, 자료 URL, 실제 발췌 허용 상태를 원고 ID에 연동. 가사 제공업체 전사 차이를 바탕으로 잘못된 띄어쓰기를 사실 확인 없이 표준형이라 표시하지 않는다. 미확인 저작권 원문의 장문을 학생용 PDF에 넣지 않는다. 중세국어는 옛한글·방점·이형태/언해본 스캔과 텍스트 비교, 2단 조판에서 단락 누락/글리프 치환 방지. 본문에 없는 단어를 문제 선지에 근거 없이 추가하면 BLOCKED_LAYOUT_OR_SOURCE.
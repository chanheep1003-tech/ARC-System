# ARC PDF PREFLIGHT V1.1
VERSION: 1.1
DATE: 2026-09-18
STATUS: ACTIVE-DEV

## PURPOSE
육안 검수 전에 PyMuPDF 기반 deterministic 1차 QC를 수행한다.

## TOOL
`tooling/pdf_qc/pdf_preflight.py`

## CHECKS
- page boundary overflow
- configured margin 침범
- suspicious text-text bbox overlap
- image/drawing bbox outside page
- empty/near-empty page
- unregistered sparse page / page occupancy anomaly
- embedded font-name audit for Thin/ExtraLight/Light-only body typography
- visible raw HTML/Markdown token candidates
- student-facing production metadata leak candidates
- replacement/broken glyph 후보
- unexpected page size
- render failure
- optional pdftoppm/PyMuPDF page raster export

## RESULT
PASS: hard issue 없음
WARN: 사람이 볼 의심 페이지 존재
FAIL: solving/reading에 영향을 주는 overflow/overlap/render/glyph 문제, 또는 print-legibility hard gate 위반

ARC_CORE 추가:
- registered blank page가 아닌 25% 미만 near-empty page = FAIL
- 45% 미만 sparse page = WARN/REFLOW
- body text가 Thin/ExtraLight/Light only로 임베드된 경우 = FAIL
- raw <br>/<b>/</b> 등 markup token 노출 = FAIL

## LIMIT
bbox 검사는 정상적인 표/카드 내부 중첩을 완전히 이해하지 못하므로 WARN은 human/visual QC로 확인한다.
자동 preflight는 최종 육안 검수를 대체하지 않는다.

## RELEASE
PDF_PREFLIGHT_STATUS와 PDF_PREFLIGHT_REPORT가 없으면 FINAL_RELEASE 금지.
FAIL은 human approval로 덮을 수 없다.

END ARC PDF PREFLIGHT V1.1

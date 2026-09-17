---
name: arc-source-ingest
description: 'ARC의 교과서·학습지·기출·외부자료를 원문 구조를 보존해 추출·정규화하고, 범위 잠금과 문항 생성이 사용할 source packet으로 만든다. PDF/HWP/HWPX/DOCX/XLSX/PPTX/이미지 자료를 다룰 때 사용한다.'
metadata:
  version: 1.0.0
  arc-role: source-ingest
---
# ARC Source Ingest

## 목적
문항 생성 전에 원자료를 **정확한 구조와 출처 위치를 유지한 상태**로 정규화한다. 추출 편의 때문에 표·다단·주석·X표시·그림 조건을 평문으로 뭉개지 않는다.

## 입력
- 현재 시험범위와 과목 MASTER
- 교과서, 학습지, 학교 기출, 학교 보조자료, 외부 참고자료
- 필요 시 사용자 지정 제외 표시(예: 통합사회 C파트 손글씨 X)

## 핵심 절차
1. 파일 형식을 식별하고 파일별 parser를 선택한다.
2. PDF는 텍스트 추출만 믿지 말고 다단·표·그림·스캔 여부를 triage한다.
3. HWP/HWPX는 전용 구조 추출을 우선한다. 표 셀과 문단 순서를 보존한다.
4. XLSX/DOCX/PPTX도 표·텍스트박스·차트·발표자 노트 등 실제 구조를 가능한 한 보존한다.
5. 페이지/슬라이드/시트/섹션 단위 위치 정보를 유지한다.
6. 시각적으로 의미가 있는 표식(X, 동그라미, 색 구분, 화살표)은 별도 플래그로 기록한다.
7. 추출 결과를 원본 페이지와 표본 대조한다. 구조가 깨졌으면 다른 추출 경로를 사용한다.
8. 최종 결과는 `SOURCE_PACKET`으로 넘긴다.

## SOURCE_PACKET 최소 필드
- `source_id`
- `source_type`
- `subject`
- `scope_status`: R/S/C/X/UNKNOWN
- `location`: page/slide/sheet/section
- `text_blocks`
- `tables`
- `visual_refs`
- `handwritten_or_visual_marks`
- `extraction_confidence`
- `notes`

## ARC 전용 우선순위
현재 학습지/교사자료 > 현재 교과서 > 학교 보조자료 > 공식 외부자료 > 일반 외부자료.

통합사회 C파트의 사용자 손글씨 X 표시는 **X 범위로 강제**한다. X 범위는 정답 근거, 오답 필수지식, 보기 핵심, 고난도 확장에 사용할 수 없다.

## Hard Fail
- 페이지/표 위치가 뒤섞여 출처를 역추적할 수 없음
- 원자료의 제외 표시를 유실함
- 표의 행·열 관계가 깨졌는데 정상으로 간주함
- 스캔/그림 자료를 텍스트만 보고 완전 추출로 표시함
- 여러 파일 형식 중 일부를 조용히 생략함

## Gotchas
- 빠른 추출은 초벌용이다. 시험범위 판단에 쓰일 정보는 원본과 대조한다.
- OCR은 최후 수단이다. 숫자, 단위, 첨자, 한자, 기호는 별도 검증한다.
- 외부 parser 사용 가능 여부와 관계없이 ARC의 최종 기준은 원본 자료와의 일치다.

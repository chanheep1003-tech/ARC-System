---
name: arc-source-ingest
description: 'ARC의 교과서·학습지·기출·외부자료를 구조와 위치를 보존해 추출하고 SOURCE_PACKET/SOURCE_LEDGER 입력으로 정규화한다.'
metadata:
  version: 1.1.0
  arc-role: source-ingest
---
# ARC Source Ingest

## 목적
문항 생성 전에 원자료를 정확한 구조와 출처 위치를 유지한 상태로 정규화한다.

## 핵심 절차
1. 파일 형식을 식별한다.
2. PDF는 다단·표·그림·스캔 여부를 triage한다.
3. HWP/HWPX/DOCX/XLSX/PPTX는 표·문단·텍스트박스 구조를 가능한 한 보존한다.
4. 페이지/슬라이드/시트/섹션 단위 위치 정보를 유지한다.
5. X, 동그라미, 색 구분, 화살표 등 시각 표식을 별도 플래그로 기록한다.
6. 추출 결과를 원본과 표본 대조한다.
7. SOURCE_PACKET을 만든다.
8. SOURCE_REQUIRED 후보는 quality/ARC_SOURCE_LEDGER_V1.0.md 형식으로 SOURCE_ID를 준비한다.

## SOURCE_PACKET 최소 필드
- source_id
- source_type
- subject
- scope_status: R/S/C/X/UNKNOWN
- location: page/slide/sheet/section
- text_blocks
- tables
- visual_refs
- handwritten_or_visual_marks
- extraction_confidence
- notes

## 출처 위치 규칙
Drive 자료는 가능한 경우 FILE_ID + page/section을 남긴다.
위치가 불분명하면 페이지를 추정하지 않고 UNVERIFIED로 둔다.

## ARC 전용 우선순위
현재 학습지/교사자료 > 현재 교과서 > 학교 보조자료 > 공식 외부자료 > 일반 외부자료.

통합사회 C파트 손글씨 X 표시는 X 범위로 강제한다.
OCR 텍스트만으로 X 여부를 확정하지 않는다.

## Hard Fail
- 역추적 가능한 위치를 보존하지 못함
- 원자료의 제외 표시 유실
- 표 행·열 관계가 깨졌는데 정상으로 간주
- 스캔/그림 자료를 텍스트만 보고 완전 추출로 표시
- 실제로 읽지 않은 자료를 SOURCE_PACKET에 포함

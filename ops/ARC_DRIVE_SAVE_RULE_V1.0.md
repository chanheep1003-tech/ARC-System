# ARC DRIVE SAVE RULE V1.0
VERSION: 1.0
DATE: 2026-11-12
STATUS: ACTIVE
AUTHORITY: USER_DIRECTIVE:2026-11-12
ROLE: 만든 파일을 언제 Google Drive에 저장하는지 정한다

## 규칙
1. 파일(PDF·정답·해설 등 산출물)을 만들면 먼저 사용자에게 보여 준다.
2. **사용자 검수를 1번 통과하면 반드시 Google Drive에 저장한다.** 저장을 빠뜨리지 않는다. 추가 승인을 다시 묻지 않는다.
3. 검수를 통과하기 전에는 Drive에 저장하지 않는다.
4. 사용자가 고치라고 하면 통과가 아니다. 고친 파일을 다시 보여 주고, 그 파일이 통과하면 저장한다.

## 저장 방법
- 위치: `ops/ARC_STORAGE_TARGETS_V1.1.yaml`에 등록된 과목·제품 폴더. 등록된 폴더가 없으면 저장 전에 위치를 사용자에게 한 번 확인한다.
- 함께 저장: 학생용 PDF, 정답(FINAL은 별도 PDF), 교사용 해설.
- 저장 뒤 Drive에서 파일을 다시 열어 확인하고, 파일 ID를 `python tooling/arc.py log … --output <Drive 파일 ID>`로 RUN_LOG에 남긴다.
- 저장에 실패하면 실패했다고 알리고 다시 시도한다. 저장했다고 말하지 않는다.

## 상태 표시
검수 통과는 저장 조건이지 품질 인증이 아니다. 독립 재풀이를 하지 않았거나 시험 범위가 확정되지 않은 파일은 파일명과 기록에 그 상태(초안, 범위 미확정)를 그대로 적어 저장한다.

## 기존 규칙과의 관계
`problem_final_user_approval_before_drive_save: required`, `problem_drive_save_before_user_approval: forbidden`을 그대로 따른다. 이 규칙은 "통과 후에는 반드시 저장"을 더한다. 필요한 통과 횟수는 1번이다.

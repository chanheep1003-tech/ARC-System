# ARC CORE EDITORIAL NATURALNESS V1.2
VERSION: 1.2
DATE: 2026-09-19
STATUS: ACTIVE-DEV
ROLE: ARC CORE 학생용 원고의 편집 자연스러움·참고서 현실성 검수

## 0. PURPOSE
ARC CORE가 'AI가 항목을 자동 정리한 카드 모음'처럼 보이지 않게 한다.
목표는 인간이 편집한 내신 개념서의 밀도, 흐름, 용어 선택, 정보 위계를 재현하는 것이다.
정확성·범위·학교자료 우선순위를 희생해서 자연스러움을 만들지 않는다.

## 1. CORE EDITORIAL PRINCIPLE
- 모든 concept를 동일한 템플릿 길이와 동일한 블록 수로 맞추지 않는다.
- 제목 아래에 필요한 설명이 자연스럽게 이어지는 '본문 흐름'을 기본으로 한다.
- MUST / CONFUSING / TRAP / COMPARE / VISUAL은 필요한 경우에만 사용한다.
- 같은 페이지에서 모든 개념이 MUST 3개 + CONFUSING 2개 + TRAP 2개처럼 기계적으로 반복되면 FAIL.
- 한 개념이 한두 문단으로 충분하면 억지로 표·박스·목록을 추가하지 않는다.
- 복잡한 개념은 설명을 길게 허용하고, 단순 개념은 짧게 끝낸다.
- 학생이 실제로 읽는 순서와 사고 흐름을 우선한다.
- concept별 DEPTH_PRIORITY가 달라도 학생용에서는 '표준/심화/고난도'라는 시스템 라벨을 반복 노출하지 않는다.
- HIGH_DIFFICULTY 내부 분석 단계(FUNDAMENTAL/CONDITIONS/BOUNDARIES 등)를 학생용 고정 소제목으로 그대로 출력하지 않는다.

## 2. AI-LIKE SIGNALS
다음은 AI 편집 신호로 본다.
- 모든 제목이 같은 문법 구조
- 모든 개념에 동일한 수의 bullet
- 3단 병렬 문장 반복
- '핵심은 ~입니다', '쉽게 말하면', '즉', '따라서'가 과도하게 반복
- 모든 문단이 2~3문장으로 기계적으로 동일
- 개념마다 억지 예시를 하나씩 붙임
- 불필요한 친절한 재진술
- 같은 내용을 본문/MUST/TRAP에서 세 번 반복
- 표를 만들 이유가 없는데 2열 표를 남발
- 카드형 박스가 연속되어 본문 흐름이 끊김
- 이모지, 과장된 느낌표, 마케팅형 카피
- '시험에 무조건 나온다', '선생님이 좋아한다' 같은 근거 없는 예측
- 모든 TRAP을 '~가 아니다' 형태로만 씀
- 학생용에 내부 ID, QC, priority, DEPTH_PRIORITY, N° 연결 상태를 노출
- 고난도 concept마다 '심화', '고난도 포인트', '킬러 대비' 같은 배지를 기계적으로 반복
- HIGH_DIFFICULTY concept마다 동일한 5~7단 소제목을 출력

## 2-A. MACRO AI-LIKE SIGNALS
문장 하나하나가 자연스러워도 chapter 구조가 아래와 같으면 AI-like로 본다.

- 모든 소단원이 같은 "들어가기 전에 → 설명 → 핵심 정리 → 주의할 점 → 문제 적용" 순서
- 본문에서 설명한 사실을 chapter 끝에서 시간축/목록/도식으로 다시 전부 반복
- 한 chapter 안에서 표·카드·요약 블록이 설명보다 더 많은 시각적 면적을 차지
- 제목을 지우면 section 간 관계가 거의 보이지 않고 독립 note 조각만 남음
- 사건/개념이 원인·관계보다 이름과 특징의 목록으로 기억되게 구성
- 모든 chapter가 "시험에서 어떻게 나오는가" 메타 설명으로 시작하거나 끝남
- summary가 synthesis가 아니라 inventory임

이 신호가 2개 이상이면 MICRO 문체가 자연스러워도 CORE_EDITORIAL_NATURALNESS는 PASS할 수 없다.

## 2-B. HUMAN EDITOR SIGNALS
다음은 실제 참고서형 구조의 긍정 신호다.

- chapter 첫 1/3 안에 중심 질문 또는 전체 흐름이 보임
- 세부 사실이 등장할 때 앞뒤 개념과의 관계가 설명됨
- 긴 설명과 짧은 설명의 길이가 내용 중요도에 따라 달라짐
- 표는 문장을 줄이기 위해서가 아니라 비교축을 드러내기 위해 사용됨
- chapter 마지막이 앞 내용을 한 단계 높은 구조로 압축함
- 다음 chapter로 넘어가는 인과/시간/개념 연결이 자연스럽게 존재함

## 3. LANGUAGE
- 현재 교과서와 학교 학습지의 용어를 우선한다.
- 정확한 교과 용어를 쉬운 말로 대체해 의미를 희석하지 않는다.
- 설명은 필요하면 쉬운 연결 문장을 사용하되 유아화하지 않는다.
- 문장 길이를 인위적으로 균일화하지 않는다.
- 수식어를 줄이고 판단 근거가 있는 문장을 쓴다.
- 동일 의미 재진술은 한 번이면 충분하다.
- 출처가 말하지 않은 해석을 '당연히', '분명히' 같은 단어로 확정하지 않는다.

## 4. BLOCK NATURALNESS
### MUST
정말 암기·고정해야 하는 내용만 1~3개.
본문과 동일한 문장을 그대로 복사하지 않는다.

### CONFUSING
실제로 서로 헷갈릴 만한 둘 이상의 개념/판단축이 있을 때만.
차이가 한 축이면 문장으로, 여러 축이면 표를 사용한다.

### TRAP
실제 학교자료, 기존 문항, 검수 과정, 일반적인 오개념에서 근거가 있는 함정만 사용.
억지 오답을 만들기 위해 새 함정을 발명하지 않는다.
형식은 자유롭게 하되 '왜 틀리는지'가 한 번에 보이게 한다.
TRAP이 필요 없는 개념은 생략한다.

### EXAM CONNECTION
문제 출제 예언이 아니라 '이 개념을 어떤 판단 과정으로 사용할 수 있는가'만 설명.
매 concept마다 강제하지 않는다.

## 4-A. DEPTH NATURALNESS
STANDARD / ADVANCED / HIGH_DIFFICULTY 차이는 주로 다음으로 표현한다:
- 설명 길이
- 근거의 세밀함
- 비교축 수
- 필요한 표/도식의 유무
- CONFUSING/TRAP의 질
- 적용 사고 흐름의 깊이

배지·경고색·고정 박스 수 증가로 표현하지 않는다.
HIGH_DIFFICULTY 페이지도 본문이 중심이어야 한다.
'어려운 내용'이라는 사실을 디자인이 먼저 외치지 않게 한다.

## 5. PAGE / CHAPTER RHYTHM
페이지 리듬뿐 아니라 chapter 전체 리듬을 검사한다.
한 페이지 안에서:
- 본문 → 필요 시 보조 박스 → 다시 본문 흐름이 가능
- 박스가 본문보다 많지 않게 한다
- 연속 2~3페이지가 카드/표/요약 위주가 되지 않게 한다
- 같은 facts를 설명 페이지 뒤에 다시 카드 페이지로 복제하지 않는다
- chapter 종료 시 synthesis artifact는 원칙적으로 1개를 우선한다
- 짧은 개념 2~3개가 자연스럽게 묶일 수 있음
- 복잡한 개념은 한 페이지 이상 허용
- 빈 공간을 채우기 위한 장식/문구 금지
- 정보 밀도가 페이지마다 조금 달라도 허용

## 6. KOREAN
국어 CORE는 작품을 '정서/표현/주제' 카드 세트로만 쪼개지 않는다.
작품 전체의 흐름 → 중요한 장면/시어/표현 → 해석 근거 → 비교·혼동 포인트 순으로 읽히게 구성한다.
사용자가 제공/업로드했거나 연결 Drive의 학교자료·교과서에서 실제 확보한 SOURCE_TEXT_BLOCK은 KOREAN_MASTER_V4.1 규칙에 따라 포함할 수 있다.
학교 보충자료의 해석·정리 방식이 현재 시험 대비에서 가장 중요한 편집 기준이다.
원문과 해설은 시각적으로 구분하고, 해설을 원문의 일부처럼 섞지 않는다.

## 7. QA
CORE_EDITORIAL_NATURALNESS = PASS/REVISE/FAIL
MACRO_COHERENCE = PASS/FAIL
ANTI_LISTING = PASS/FAIL
SUMMARY_TRANSFORMATION = PASS/FAIL
AI_PATTERN_FLAGS = []
BLOCK_REPETITION = PASS/FAIL
LANGUAGE_RHYTHM = PASS/FAIL
SOURCE_TERMINOLOGY_MATCH = PASS/FAIL
STUDENT_METADATA_LEAK = PASS/FAIL

FAIL:
- chapter backbone이 없고 나열식 concept note가 본문 구조를 지배
- 동일 facts가 prose/table/summary/diagram에서 기능 변화 없이 3회 이상 반복
- 학생용에 내부 metadata 노출
- 모든 concept의 고정 템플릿 반복으로 카드형 AI 문서가 됨
- 같은 설명의 반복이 심해 실제 학습 밀도가 떨어짐
- 근거 없는 TRAP/시험예측으로 학교자료보다 AI 추정이 앞섬

END ARC CORE EDITORIAL NATURALNESS V1.2

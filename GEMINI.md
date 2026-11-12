# ARC 단일 진입 규칙 (Gemini / Claude / ChatGPT 공통)

항상 한국어로 대답한다.

1. **가장 먼저 읽을 파일**: [`ARC_MAP.md`](ARC_MAP.md) 및 [`SYSTEM_MANIFEST.yaml`](SYSTEM_MANIFEST.yaml).
2. **세션 시작 점검**:
   ```bash
   python tooling/arc.py doctor && python tooling/arc.py status
   ```
3. **3대 모델(Gemini / Claude / ChatGPT) 일관성 절대 규칙**:
   - **임의 PDF/HTML 조판 코드 작성 금지**: 모델이 자체적으로 ReportLab, WeasyPrint, HTML/CSS 스크립트를 짜서 PDF를 만들지 않는다.
   - **표준 파이프라인 강제**:
     1. 계획 카드 생성: `python tooling/arc.py plan --subject <KOR|SOC|SCI> --scope "..."`
     2. 표준 번들 스켈레톤 생성: `python tooling/arc.py scaffold --subject <KOR|SOC|SCI> --product <ARC_N|ARC_FINAL> --scope "..." --actor <GEMINI|CLAUDE|GPT>`
     3. `items.yaml`에 확인된 학교 원형(`archetype`), `<보기>`(`view`), 5선지 정오 근거(`judgments`), 함정 유형(`trap`) 작성 (단원 세트 1개씩 먼저 제작)
     4. 단일 조판 및 게이트 실행: `python tooling/production/draft_preview.py <번들폴더> --output-dir <출력폴더>` (문제지 PDF + 빠른 정답표 + 별도 상세 해설지 `*_SOLUTIONS_DRAFT_PREVIEW.pdf` 자동 생성)
4. **조판 디자인 기준 (`tooling/typeset/kor_renderer.py`)**:
   - **ARC N°**: 순수 흑백(Pure B&W), 표지는 제목·학교명(동북고등학교)·로고만 심플하게 표시. 본문은 2단 여유로운 조판(기본 4문항 목표, 긴 지문/문항은 자연스럽게 다음 단으로 이동). 문항에는 난이도(`[3]`, `[4]`)만 표시. 문제지 맨 뒤에는 빠른 정답표만 수록하고 상세 해설지는 별도 PDF(`*_SOLUTIONS.pdf`)로 동시 생성.
   - **ARC FINAL**: 실제 동북고 시험지 스타일 상단 헤더 배너 + 문항별 배점·난이도 표시 + 정답표 및 상세 해설지 별도 PDF 분리.
5. **파일 수정 후 필수 실행**:
   ```bash
   python tooling/arc.py checksums
   python tooling/arc.py ci
   ```

#!/usr/bin/env python3
"""UserPromptSubmit hook: for every request, print the ARC external-tool route as context.

Only classifies the prompt and prints `arc_external.py route <task>` JSON. It never runs a tool,
never writes memory, never grants content approval (authority stays with SYSTEM_MANIFEST.yaml).
Fail-open: any error prints nothing and exits 0 so a prompt is never blocked.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RULES = [
    ("source", ("pdf", "docx", "pptx", "교과서", "학습지", "기출", "원문", "markdown", "변환", "자료")),
    ("design", ("디자인", "ui", "사이트", "html", "템플릿", "레이아웃", "조판")),
    ("memory", ("기억", "결정 기록", "memory")),
    ("tutor", ("튜터", "설명 초안", "해설 초안")),
    ("team", ("에이전트", "팀", "지휘", "orkas")),
    ("model-lab", ("heretic", "모델 실험")),
    ("maintenance", ("규칙", "수정", "코드", "버그", "테스트", "검증", "커밋", "리팩", "스크립트", "manifest")),
]


def classify(prompt):
    p = prompt.lower()
    hits = [t for t, keys in RULES if any(k in p for k in keys)]
    return hits or ["maintenance"]


def main():
    try:
        data = json.load(sys.stdin)
        prompt = str(data.get("prompt", ""))
        out = []
        for task in classify(prompt)[:3]:
            r = subprocess.run([sys.executable, str(ROOT / "tooling/external/arc_external.py"), "route", task],
                               capture_output=True, text=True, timeout=10)
            if r.returncode == 0:
                out.append(json.dumps(json.loads(r.stdout), ensure_ascii=False))
        if out:
            print("[ARC external-tool route; on-demand only, no content approval, manifest/user scope win]\n" + "\n".join(out))
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""문항이 'N행', 'N~M행'으로 인용한 행 번호를 뽑는다. 빌드에서 본문의 해당 행을 볼드로 표시하는 데 쓴다.
(규칙: quality/ARC_LINE_CITE_BOLD_V1.0.md)"""
import re

_RE = re.compile(r"(\d+)\s*(?:[~∼–-]\s*(\d+))?\s*행")

def cited_lines(*texts):
    out = set()
    for t in texts:
        t = re.sub(r"<[^>]+>", "", t or "")
        for a, b in _RE.findall(t):
            a = int(a); b = int(b) if b else a
            if a <= b: out.update(range(a, b + 1))
    return out

def q_texts(q):
    return [q.get("stem", ""), q.get("box", "") or ""] + list(q.get("choices", []))

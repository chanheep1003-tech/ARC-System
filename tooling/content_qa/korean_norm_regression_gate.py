#!/usr/bin/env python3
"""Static Korean N° PDF regression; PASS_STATIC_ONLY is NOT content approval."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
import fitz

REGRESSIONS = [
    ("KOR-25-2-AS-APPENDIX", re.compile(r"제25항\s*\[붙임\].{0,45}?원형을\s*밝", re.S)),
    ("KOR-25-APPENDIX-MISNUMBER", re.compile(r"제25항\s*제2호.{0,35}?(?:하다|붙지|소리대로)", re.S)),
    ("KOR-BYEOLBIT-WRONG-PRONUNCIATION", re.compile(r"별빛\s*\[별삳\]")),
]
STALE_TOC=["찬기파랑가","사모곡","강호사시가","어부단가","도산십이곡","고산구곡가"]
ACTUAL_TOC=["제망매가","상저가","면앙정가","소학언해"]

def scan_pdf(path):
    with fitz.open(path) as doc:
        pages=[page.get_text(sort=True) for page in doc]
    findings=[]
    for page_number,text in enumerate(pages,1):
        compact=re.sub(r"\s+","",text)
        for code,rx in REGRESSIONS:
            target=text if code=="KOR-25-APPENDIX-MISNUMBER" else compact
            if rx.search(target):
                findings.append({"code":code,"page":page_number})
    if "중세국어" in path.name and "V3.0" in path.name and "정답및해설" not in path.name:
        cover=pages[0]
        findings.extend({"code":"KOR-MID-V3-STALE-TOC","page":1,"title":title}
                        for title in STALE_TOC if title in cover)
        findings.extend({"code":"KOR-MID-V3-INCOMPLETE-TOC","page":1,"title":title}
                        for title in ACTUAL_TOC if title not in cover)
    return {"file":path.name,"page_count":len(pages),
            "findings":findings,"status":"FAIL" if findings else "PASS_STATIC_ONLY"}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("pdfs",type=Path,nargs="+")
    parser.add_argument("--json",type=Path)
    args=parser.parse_args()
    report={"tool":"korean_norm_regression_gate",
            "limitations":"static signatures only; all-option, source and blind semantic QA required",
            "files":[scan_pdf(path) for path in args.pdfs]}
    report["fail_count"]=sum(len(f["findings"]) for f in report["files"])
    output=json.dumps(report,ensure_ascii=False,indent=2)
    print(output)
    if args.json:
        args.json.write_text(output,encoding="utf-8")
    raise SystemExit(1 if report["fail_count"] else 0)

if __name__=="__main__":
    main()

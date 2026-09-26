# -*- coding: utf-8 -*-
"""지문 모듈 → 사람이 읽는 md 생성 (Drive 업로드·검토용). 실행: python3 export_md.py"""
import re
from pathlib import Path
import unit1 as U, supplement4 as S

OUT = Path(__file__).parent / "md"

def clean(t):
    t = re.sub(r"<br\s*/?>", "\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    return t.replace("&lt;", "<").replace("&gt;", ">")

def poem(x):
    return [clean(l) for l in x] + [""]

def body(x):
    out = []
    for p in x:
        if isinstance(p, (list, tuple)):          # 연(stanza)
            out += [clean(l) for l in p] + [""]
        elif p.startswith("@@LAB@@"):
            out += [f"**{clean(p[7:])}**", ""]
        elif p.startswith("@@SUM@@"):
            out += ["> " + clean(p[7:]), ""]
        elif p.startswith("@@VERSE@@"):
            out += [clean(l) for l in p[9:].split("|")] + [""]
        else:
            out += [clean(p), ""]
    return out

def notes(ns):
    return ["", "### 주석", *[f"- {clean(n)}" for n in ns]] if ns else []

def write(name, title, src, parts):
    lines = [f"# {title}", "", f"출처: {src}", ""]
    for p in parts: lines += p
    (OUT / f"{name}.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

OUT.mkdir(exist_ok=True)
# 1단원
write("1단원_01_제망매가", "월명사, 「제망매가」 (김완진 해독)", "교과서 1단원", [poem(U.JMG)])
write("1단원_02_속미인곡", "정철, 「속미인곡」", "교과서 1단원", [body(U.SMI), notes(U.SMI_NOTES)])
write("1단원_03_춘향전", "작자 미상, 「춘향전」", "교과서 1단원", [["> " + clean(U.CHH_PRE), ""], body(U.CHH), notes(U.CHH_NOTES)])
write("1단원_04_수라", "백석, 「수라」", "교과서 1단원", [body(U.SURA), notes(U.SURA_NOTES)])
write("1단원_05_아홉켤레의구두로남은사내", "윤흥길, 「아홉 켤레의 구두로 남은 사내」 (발췌)", "교과서 1단원 · 2025 기출",
      [["> " + clean(U.GU_PRE), ""], body(U.GU), notes(U.GU_NOTES)])
# 보충자료
write("보충_01_탄궁가", S.TAN_SRC, "보충자료", [poem(S.TAN_LINES), notes(S.TAN_NOTES)])
write("보충_02_팔원", S.PAL_SRC, "보충자료", [poem(S.PAL_LINES), notes(S.PAL_NOTES)])
write("보충_03_기억할만한지나침", S.MEM_SRC, "보충자료", [body(S.MEM_STANZAS), notes(S.MEM_NOTES)])
write("보충_04_칸트헤겔자유", S.KANT_SRC, "보충자료", [body(S.KANT_PARAS), ["", "### 보충 해설문", clean(S.EXTRA_MATERIAL)]])
print(sorted(p.name for p in OUT.iterdir()))

# 통합본 (Drive 1파일 조회용)
ALL = ["# ARC 지문 라이브러리 — 공통국어2 (1단원 5작품 + 보충자료 4편)", "",
       "GitHub `sources/KOR/공통국어2/` 의 unit1.py·supplement4.py 에서 생성. 원문 수정은 GitHub 쪽에서 하고 export_md.py로 재생성.", ""]
for f in sorted(OUT.glob("*.md")):
    if f.name.startswith("_"): continue
    ALL += ["---", "", f.read_text(encoding="utf-8").replace("\n# ", "\n## ").replace("# ", "## ", 1).replace("### 주석", "#### 주석").replace("### 보충", "#### 보충"), ""]
(OUT / "_ALL_공통국어2_지문라이브러리.md").write_text("\n".join(ALL), encoding="utf-8")

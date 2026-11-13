"""영어 ARC N° — N기출 고난도 독해 Level 1 (3-4-1~3-6-4) 지문당 5문항 변형. 저장소 루트에서 실행.

사용자 지시(2026-11-13):
- 선택형만 낸다(서술형 제외).
- 영영풀이·유의어 등 단어 파트 유형(VOC-*)은 1~10번 단어 문항 전용이므로 지문 워크북에 넣지 않는다.
- 한 문항의 선지는 한 언어로만 쓴다.
- 어법·문맥 어휘 문항은 밑줄이 든 부분만 발췌해 지문을 줄인다.

지문마다 5개 슬롯: S1 대의(RDG-01/02/08) · S2 어법(GRM-01/02) · S3 문맥 어휘 또는 어법(RDG-03/GRM-01) ·
S4·S5 구조·추론(RDG-04/05/06/07/09). 유형 코드는 quality/english/ARC_ENG_EXAM_TYPES_V1.0.yaml에서만 고른다.
본문은 passages.yaml(Drive 마스터 DB 정제본)에서 읽고, 변형은 find/replace로만 만든다(찾는 문자열이 정확히
한 번 나와야 한다). ⟦…⟧ = 밑줄. 문항 내용은 items_*.py(회차별)에 있다.
"""
from pathlib import Path
import re
import yaml

HERE = Path(__file__).resolve().parent
PASS = {p["code"]: p for p in yaml.safe_load((HERE / "passages.yaml").read_text(encoding="utf-8"))["passages"]}
S, M, W = "STRONG", "MEDIUM", "WEAK"
U = lambda s: f"⟦{s}⟧"
CIRC = "①②③④⑤"
NUMS = list(CIRC)
FAMILY = {"RDG-01": "MAIN_IDEA", "RDG-02": "IMPLIED_MEANING", "RDG-03": "VOCAB_IN_CONTEXT", "RDG-04": "BLANK_INFERENCE",
          "RDG-05": "IRRELEVANT_SENTENCE", "RDG-06": "SEQUENCE_ORDER", "RDG-07": "SENTENCE_INSERTION",
          "RDG-08": "CONTENT_UNDERSTANDING", "RDG-09": "SUMMARY_COMPLETION", "GRM-01": "GRAMMAR_ERROR",
          "GRM-02": "GRAMMAR_CORRECT_SET"}
STEM = {
    "GRM-01": "다음 글의 밑줄 친 부분 중, 어법상 틀린 것은?",
    "GRM-02": "다음 글의 밑줄 친 부분 중, 어법상 올바른 것끼리 짝지은 것은?",
    "RDG-03": "다음 글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?",
    "RDG-04": "다음 빈칸에 들어갈 말로 가장 적절한 것은?",
    "RDG-05": "다음 글에서 전체 흐름과 관계 없는 문장은?",
    "RDG-06": "주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?",
    "RDG-07": "글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳은?",
    "RDG-08": "다음 글의 내용과 일치하지 않는 것은?",
    "RDG-09": "다음 글의 내용을 한 문장으로 요약하고자 한다. 빈칸 (A), (B)에 들어갈 말로 가장 적절한 것은?",
}
ORDER_OPTS = ["(A) - (C) - (B)", "(B) - (A) - (C)", "(B) - (C) - (A)", "(C) - (A) - (B)", "(C) - (B) - (A)"]
items: list[dict] = []
counter: dict[str, int] = {}


def text(code: str) -> str:
    return PASS[code]["text"]


def sents(code: str) -> list[str]:
    return re.split(r"(?<=[.?!\"])\s+(?=[A-Z])", text(code))


def excerpt(code: str, a: int, b: int) -> str:
    """Sentences a..b (0-based, inclusive): grammar / context-word items print only the underlined part."""
    return " ".join(sents(code)[a:b + 1])


def edit(src: str, *pairs: tuple[str, str]) -> str:
    for find, repl in pairs:
        if src.count(find) != 1:
            raise SystemExit(f"EDIT_NOT_UNIQUE: {find!r} x{src.count(find)}")
        src = src.replace(find, repl, 1)
    return src


def ulist(src: str, *finds) -> str:
    """Underline finds in order as ①⟦…⟧ … ⑤⟦…⟧. A (context, word) pair underlines word inside a unique context."""
    pairs = []
    for i, f in enumerate(finds):
        ctx, w = f if isinstance(f, tuple) else (f, f)
        pairs.append((ctx, ctx.replace(w, f"{CIRC[i]}{U(w)}", 1)))
    return edit(src, *pairs)


def _id(code: str) -> str:
    counter[code] = counter.get(code, 0) + 1
    return f"ENG-NG-{code}-{counter[code]}"


def mcq(code, t, d, stem, passage, opts, ans, sb, judg, steps=2, elim=1, view=None, view_label=""):
    stem = stem or STEM[t]
    neg = bool(re.search(r"틀린 것|않은 것|않는 것|관계 없는", stem))  # negative stem: key is the one FALSE option
    js = []
    for i, (claim, c, why) in enumerate(judg, 1):
        js.append({"axis": "reading", "c": "CORRECT" if i == ans else c, "claim": claim,
                   "ev": ["PASSAGE", f"OPTION{i}", f"SCOPE:NGICHUL-L1-{code}"], "v": (i != ans) if neg else (i == ans),
                   "why": why})
    if d in ("D4", "D5"):
        steps = max(steps, 2)
    it = {"item_id": _id(code), "set": None, "eng_type": f"ARC-ENG-{t}", "source_code": code,
          "scope_refs": [f"NGICHUL-L1-{code}"], "stem": stem, "passage": passage if isinstance(passage, list) else [passage],
          "options": opts, "answer": ans, "second_best": sb, "difficulty": d, "family": FAMILY[t],
          "balance": "ADVANCED_DISCRIMINATION" if d in ("D4", "D5") else "CORE_EXAM_POINT",
          "reasoning_steps": steps, "immediate_elimination": elim, "transfer": True,
          "stem_polarity": "NEGATIVE" if neg else "POSITIVE", "judgments": js}
    if view:
        it["view"] = view
        it["view_label"] = view_label
    items.append(it)
    return it


def under(code, t, d, rng, finds, swap, sb, judg, steps=2):
    """GRM-01 / RDG-03 on an excerpt: five underlines; swap=(index, wrong word) plants the single error."""
    src = ulist(excerpt(code, *rng), *finds)
    idx, wrong = swap
    f = finds[idx]
    right = f[1] if isinstance(f, tuple) else f
    src = edit(src, (f"{CIRC[idx]}{U(right)}", f"{CIRC[idx]}{U(wrong)}"))
    return mcq(code, t, d, None, src, NUMS, idx + 1, sb, judg, steps=steps)


def slots(code, order, marks=None):
    """Join sentence indexes (or literal strings) in order; marks={i: '( ① )'} goes before sentence i."""
    s = sents(code)
    out = []
    for i in order:
        if isinstance(i, str):
            out.append(i)
            continue
        if marks and i in marks:
            out.append(marks[i])
        out.append(s[i])
    return " ".join(out)


def ordering(code, d, given, parts, labels, ans, sb, judg):
    """RDG-06: given = sentence range in the box; parts = [(a, b), …] in true order; labels = their letters."""
    s = sents(code)
    body = {lab: " ".join(s[a:b + 1]) for lab, (a, b) in zip(labels, parts)}
    passage = [" ".join(s[given[0]:given[1] + 1]), ""] + [f"({k}) {body[k]}" for k in "ABC"]
    return mcq(code, "RDG-06", d, None, passage, ORDER_OPTS, ans, sb, judg, steps=3)


for f in sorted(HERE.glob("items_*.py")):
    exec(f.read_text(encoding="utf-8"), globals())


def _ending(it):
    return re.sub(r"\s", "", it["stem"])[-8:]


def _no_triple_runs(seq):
    """Within each passage keep the written order unless three same-ending stems or three same keys would run in a row."""
    from itertools import permutations
    out: list[dict] = []
    groups: dict[str, list[dict]] = {}
    for it in seq:
        groups.setdefault(it["source_code"], []).append(it)
    for grp in groups.values():
        for perm in permutations(grp):
            trial = out[-2:] + list(perm)
            if all(not (_ending(trial[k]) == _ending(trial[k - 1]) == _ending(trial[k - 2]))
                   and not (trial[k]["answer"] == trial[k - 1]["answer"] == trial[k - 2]["answer"])
                   for k in range(2, len(trial))):
                out += list(perm)
                break
        else:
            raise SystemExit(f"STEM_RUN_UNAVOIDABLE: {grp[0]['source_code']}")
    return out


items = _no_triple_runs(items)

bundle = {
    "batch_id": "ENG-N-NGICHUL-L1-20261113", "product_mode": "ARC_N", "subject": "ENG", "generator": "CLAUDE",
    "set_label": "ARC N° 영어", "course": "공통영어2",
    "cover_subtitle": "N기출 고난도 독해 Level 1 · 3-4-1~3-6-4 · 지문당 5문항(선택형)",
    "school_line": "동북고등학교 1학년 · 2026 2학기 기말",
    "created_at": "2026-11-13T21:00:00+09:00",
    "scope": "N기출 고난도 독해 Level 1 p78~91 (Mini 모의고사 04~06회, 28지문)",
    "scope_refs": ["NGICHUL-L1-3-4-1~3-6-4"], "workbook_profile": "PASSAGE_5",
    "exam_context_id": "DONGBUK_2026_2_FINAL",
    "sets": [], "items": items,
}
(HERE / "items.yaml").write_text(yaml.safe_dump(bundle, allow_unicode=True, sort_keys=False, width=4000), encoding="utf-8")
print(len(items), "items")

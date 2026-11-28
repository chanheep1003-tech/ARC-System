#!/usr/bin/env python3
"""Merge authoring parts -> ../items.yaml. Balances key positions by swapping the key
into a target slot (ordered items stay fixed). Deterministic."""
import random, re, statistics, sys
from collections import Counter
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import part1, part2, part3, part4  # noqa: E402

FIXED_EXTRA = {11, 53}
NEG_RE = re.compile(r"적절하지 않은|바르지 않은|어긋나는|아닌 것은")

def polarity(it):
    return "NEGATIVE" if it.get("neg") or NEG_RE.search(it["stem"]) else "POSITIVE"

items = [dict(it, set=m.S) for m in (part1, part2, part3, part4) for it in m.ITEMS]
assert [it["n"] for it in items] == list(range(1, 81))
import revisions  # noqa: E402  round-2 edits after blind round 1
for it in items:
    it.update(revisions.REV.get(it["n"], {}))
    for old, new in revisions.REV_TEXT.get(it["n"], []):
        hits = [i for i, o in enumerate(it["opts"]) if old in o]
        assert len(hits) == 1, (it["n"], old)
        it["opts"][hits[0]] = it["opts"][hits[0]].replace(old, new)
    import revisions3  # noqa: E402  round-3 redesign
    it.update(revisions3.REV3.get(it["n"], {}))
    for old, new in revisions3.REV3_TEXT.get(it["n"], []):
        hits = [i for i, o in enumerate(it["opts"]) if old in o]
        assert len(hits) == 1, (it["n"], old)
        it["opts"][hits[0]] = it["opts"][hits[0]].replace(old, new)
    for pos, tup in revisions3.REV3_O.get(it["n"], {}).items():
        it["o"] = list(it["o"]); it["o"][pos - 1] = tup
    import revisions4  # noqa: E402
    it.update(revisions4.REV4.get(it["n"], {}))
    import revisions5  # noqa: E402
    it.update(revisions5.REV5.get(it["n"], {}))
    if it["n"] in (19, 38, 57, 80):
        it["bal"] = "CORE"
    if it["n"] == 60:
        it["opts"] = [re.sub(r"(?<!~)13행", "12~13행", o) for o in it["opts"]]
    assert len(it["opts"]) == 5 and len(it["o"]) == 5, it["n"]

# ---- target key sequence
def make_seq(seed):
    rng = random.Random(seed)
    counts, seq = Counter(), []
    isfixed = lambda it: it.get("fixed") or it["n"] in FIXED_EXTRA or it["opts"][0][:1] in ("㉠", "ⓐ")
    for idx, it in enumerate(items):
        if isfixed(it):
            k = it["key"]
        else:
            nxt = items[idx + 1]["key"] if idx + 1 < len(items) and isfixed(items[idx + 1]) else None
            cands = [p for p in range(1, 6) if not (len(seq) >= 2 and seq[-1] == seq[-2] == p)
                     and not (seq and seq[-1] == p == nxt)]
            low = min(counts[p] for p in cands)
            k = rng.choice([p for p in cands if counts[p] == low])
        seq.append(k); counts[k] += 1
    return seq, counts

for _seed in range(20261128, 20261328):
    seq, counts = make_seq(_seed)
    if max(len(m.group(0)) for m in re.finditer(r"(.)\1*", "".join(map(str, seq)))) <= 2 and max(counts.values()) <= 17:
        break

def swap(it, target):
    k = it["key"]
    if k == target:
        return it
    a, b = k - 1, target - 1
    for f in ("opts", "o"):
        L = list(it[f]); L[a], L[b] = L[b], L[a]; it[f] = L
    sb = it["sb"]
    it["sb"] = target if sb == k else (k if sb == target else sb)
    it["key"] = target
    return it

out = []
for it, k in zip(items, seq):
    it = swap(dict(it), k)
    labs = ["A", "B", "C", "D", "E"] if any(o.startswith("학생 A") for o in it["opts"]) else (["1", "2", "3", "4", "5"] if any(o.startswith("학생 1") for o in it["opts"]) else None)
    if labs:
        it["opts"] = [re.sub(r"^학생 [A-E1-5]:", f"학생 {labs[i]}:", o) for i, o in enumerate(it["opts"])]
    pol = polarity(it)
    judg = []
    for i, (c, ev, why) in enumerate(it["o"], 1):
        is_key = i == it["key"]
        truth = is_key if pol == "POSITIVE" else not is_key
        judg.append({"v": truth, "c": c, "axis": f"{it['set']}-{it['n']:02d}-{it['cov'].lower()}",
                     "claim": f"opt{i}", "ev": ev, "why": why})
    d = it["d"]
    rec = {"item_id": f"KOR-NF4-{it['n']:03d}", "set": it["set"], "format": "MCQ",
           "family": it["fam"], "coverage": it["cov"], "difficulty": d,
           "balance": "ADVANCED_DISCRIMINATION" if it["bal"] == "ADV" else "CORE_EXAM_POINT",
           "core_exam_point": it["bal"] != "ADV", "stem_polarity": pol, "stem": it["stem"]}
    if it.get("view"):
        rec["view"] = it["view"]
    rec.update({"options": it["opts"], "answer": it["key"], "second_best": it["sb"], "judgments": judg,
                "reasoning_steps": {"D2": 1, "D3": 2, "D4": 3, "D5": 4}[d],
                "immediate_elimination": {"D2": 2, "D3": 1, "D4": 1, "D5": 0}[d],
                "transfer": it["fam"] in ("VIEW_APPLICATION", "CASE_APPLICATION")})
    out.append(rec)

SETS = [
 {"id": "S1", "prompt": "다음 글을 읽고 물음에 답하시오.",
  "works": [{"label": None, "source_text_id": "KOR-SUPP-2026F-LIT-WONYUGA", "line_numbers": 5, "marks": [
    {"find": "삼간초당", "replace": "ⓐ삼간초당"},
    {"find": "무릉도원이 여기 아닌가", "replace": "㉠무릉도원이 여기 아닌가"},
    {"find": "서울 거리", "replace": "ⓑ서울 거리"},
    {"find": "출세가 저러한데 늦게 옴은 웬일인고", "replace": "㉡출세가 저러한데 늦게 옴은 웬일인고"},
    {"find": "충신열사 후예로서", "replace": "㉢충신열사 후예로서"},
    {"find": "하늘 같은 궁궐 안에 이 노래 들으시면", "replace": "㉣하늘 같은 궁궐 안에 이 노래 들으시면"},
    {"find": "의정부에", "replace": "ⓒ의정부에"},
    {"find": "한강수", "replace": "ⓓ한강수"},
    {"find": "담양군에", "replace": "ⓔ담양군에"},
    {"find": "천하 만사 한바탕 웃음이다", "replace": "㉤천하 만사 한바탕 웃음이다"}]}],
  "notes": [
    "* 화전난무 봉삼하요 운외고성 안구추라: 꽃 앞에 어지럽게 춤추는 벌은 여름을 누리고 구름 밖에 우는 기러기는 가을을 기다리는구나.",
    "* 풍운: 세상에 두각을 나타냄. 높은 지위.",
    "* 이윤의~섬겼으니: 성군을 섬긴 충신 이윤과 강태공에 대한 이야기.",
    "* 급암의~의사런가: 충신 급암과 절의를 지킨 노중련에 대한 이야기.",
    "* 삼고초려~또 아닌가: 뛰어난 인재를 등용하려 한 촉한의 유비와 송 태조에 대한 이야기.",
    "* 고요직설: 성군 요 임금과 순 임금을 모신 어진 신하들을 일컬음.",
    "* 오현금 남풍시: 순 임금이 오현금을 타면서 백성의 평안함을 노래한 시.",
    "* 범려의 오호주: 월나라 범려가 은거할 때 탔던 배."]},
 {"id": "S2", "prompt": "다음 글을 읽고 물음에 답하시오.",
  "works": [{"label": None, "source_text_id": "KOR-SUPP-2026F-LIT-JOSANG-MUNJIP", "marks": [
    {"find": "멀뚱히 내려다본다", "replace": "ⓐ멀뚱히 내려다본다"},
    {"find": "주둥이를 삐죽 빼문다", "replace": "ⓑ주둥이를 삐죽 빼문다"},
    {"find": "멀지도 않은 증조부의 문집을", "replace": "㉠멀지도 않은 증조부의 문집을"},
    {"find": "팔랑팔랑 서너 장 넘겨본다", "replace": "ⓒ팔랑팔랑 서너 장 넘겨본다"},
    {"find": "책을 만드는 데 돈이 얼마나 드는지 아세요?", "replace": "㉢책을 만드는 데 돈이 얼마나 드는지 아세요?"},
    {"find": "이맛살을 약간 찌푸리며 슬그머니 고개를 돌린다", "replace": "ⓓ이맛살을 약간 찌푸리며 슬그머니 고개를 돌린다"},
    {"find": "나는 일자무식이다마는", "replace": "㉣나는 일자무식이다마는"},
    {"find": "너의 애비가", "replace": "㉤너의 애비가"},
    {"find": "방문을 탁 닫고 나가 버린다", "replace": "ⓔ방문을 탁 닫고 나가 버린다"}]}],
  "notes": []},
 {"id": "S3", "prompt": "다음 글을 읽고 물음에 답하시오.",
  "works": [{"label": None, "source_text_id": "KOR-SUPP-2026F-LIT-BOSEOK1", "line_numbers": 5, "marks": [
    {"find": "결코 지상으로 내려오지 않는 새.", "replace": "㉠결코 지상으로 내려오지 않는 새."},
    {"find": "쥐라기 지층 어느 하늘 아래", "replace": "㉡쥐라기 지층 어느 하늘 아래"},
    {"find": "가령 죽음이라든가,", "replace": "㉢가령 죽음이라든가,"},
    {"find": "지상의 별들이여", "replace": "㉣지상의 별들이여"},
    {"find": "묻혀라 화석에.", "replace": "㉤묻혀라 화석에."}]}],
  "notes": []},
 {"id": "S4", "prompt": "다음 글을 읽고 물음에 답하시오.",
  "works": [{"label": "(가)", "source_text_id": "KOR-SUPP-2026F-LIT-BOSEOK1", "line_numbers": 5, "marks": []},
            {"label": "(나)", "source_text_id": "KOR-SUPP-2026F-LIT-EOLGUL", "line_numbers": 5, "marks": [
    {"find": "어둠이 손에 배자", "replace": "㉠어둠이 손에 배자"},
    {"find": "그 튼튼한 폐허를", "replace": "㉡그 튼튼한 폐허를"},
    {"find": "마음처럼 얇디얇은 얼굴이여", "replace": "㉢마음처럼 얇디얇은 얼굴이여"},
    {"find": "선글라스만한 구멍 뚫린 크고 검은 눈으로", "replace": "㉣선글라스만한 구멍 뚫린 크고 검은 눈으로"},
    {"find": "햇빛은 살로 변하여", "replace": "㉤햇빛은 살로 변하여"}]}],
  "notes": []},
]

ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "tooling" / "exams"))
import exam_scope_gate  # noqa: E402
_profile = yaml.safe_load((ROOT / "ops/exams/EXAM_CONTEXTS_V1.yaml").read_text(encoding="utf-8"))["exams"]["DONGBUK_2026_2_FINAL"]
EXAM_CONTEXT = {"exam_id": "DONGBUK_2026_2_FINAL", "profile_sha256": exam_scope_gate.digest(_profile),
                "unit_ids": ["KOR-SUPP-PRINT"],
                "source_ids": ["KOR-SUPP-2026F-LIT-WONYUGA", "KOR-SUPP-2026F-LIT-JOSANG-MUNJIP",
                               "KOR-SUPP-2026F-LIT-BOSEOK1", "KOR-SUPP-2026F-LIT-EOLGUL"]}

bundle = {
 "batch_id": "KOR-N-FINAL-LIT4-20261128", "product_mode": "ARC_N", "subject": "KOR", "generator": "CLAUDE",
 "level": "V2", "set_label": "ARC N°", "course": "공통국어2",
 "cover_subtitle": "2학기 기말고사 대비 · 문학 보충 4작품 80문항",
 "school_line": "동북고등학교 1학년 · 2026",
 "created_at": "2026-11-28T12:00:00+09:00",
 "scope": "2026 동북고 1학년 2학기 기말 보충 프린트 Ⅰ. 문학 보충 — 남석하 「원유가」, 하근찬 「조상의 문집」, 오세영 「보석 1」, 김기택 「얼굴」",
 "scope_refs": ["ops/exams/DONGBUK_2026_2_FINAL_SCOPE_NOTICE.yaml#KOR(보충 프린트 전범위)"],
 "exam_context": EXAM_CONTEXT,
 "sets": SETS, "items": out}

(HERE.parent / "items.yaml").write_text(yaml.safe_dump(bundle, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")

# ---- quick self-audit
pos = Counter(r["answer"] for r in out)
runs = max(len(m.group(0)) for m in re.finditer(r"(.)\1*", "".join(str(r["answer"]) for r in out)))
print("positions", dict(sorted(pos.items())), "max_run", runs)
print("difficulty", dict(Counter(r["difficulty"] for r in out)), "adv", sum(r["balance"] == "ADVANCED_DISCRIMINATION" for r in out))
sb = sum(re.sub(r"\s", "", r["stem"]).endswith("가장적절한것은?") for r in out)
ex = sum("적절하지않은" in re.sub(r"\s", "", r["stem"]) for r in out)
print("single_best", sb, "except", ex)
ends = [re.sub(r"\s", "", r["stem"])[-8:] for r in out]
for i in range(2, 80):
    if ends[i] == ends[i-1] == ends[i-2]:
        print("STEM RUN at", out[i]["item_id"], ends[i])
longest_key = 0
for r in out:
    L = [len(o.replace(" ", "")) for o in r["options"]]
    med = statistics.median(L); k = L[r["answer"] - 1]
    uniq_long = k == max(L) and L.count(k) == 1
    longest_key += uniq_long
    flag = []
    if uniq_long and k >= 1.25 * med: flag.append("KEY_LONG_CUE")
    if min(L) >= 8 and med >= 20 and (min(L) / med < 0.45 or max(L) / min(L) > 2.6): flag.append("ASYM")
    if flag: print(r["item_id"], flag, L)
print("longest_is_key", longest_key, round(longest_key / 80, 3))

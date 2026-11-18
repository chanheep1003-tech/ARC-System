# ───────────── 조립: 발문 연속 방지 → 선지 재배열로 정답 위치 균형 ─────────────
import re as _re
def _end(r):
    return _re.sub(r"\s", "", r["stem"])[-8:]
mcqs = [r for r in raw if not r.get("cr")]
crs = [r for r in raw if r.get("cr")]
for i in range(2, len(mcqs)):
    if _end(mcqs[i]) == _end(mcqs[i - 1]) == _end(mcqs[i - 2]):
        for j in range(i + 1, len(mcqs)):
            if _end(mcqs[j]) != _end(mcqs[i - 1]):
                mcqs[i], mcqs[j] = mcqs[j], mcqs[i]
                break
raw = mcqs + crs
items = []
fixed_counts = {k: 0 for k in range(1, 6)}
for r in raw:
    if not r.get("cr") and r["fixed"]:
        fixed_counts[r["ans"]] += 1
free = [r for r in raw if not r.get("cr") and not r["fixed"]]
total_mcq = sum(1 for r in raw if not r.get("cr"))
target_each = total_mcq // 5
need = []
for k in range(1, 6):
    need += [k] * max(0, target_each - fixed_counts[k])
while len(need) < len(free):
    need.append(1 + len(need) % 5)
import random
rng = random.Random(20261118)
rng.shuffle(need)
prev2 = []
for r in raw:
    if r.get("cr"):
        continue
    if r["fixed"] or r["opts"][0] == "㉠":
        prev2 = (prev2 + [r["ans"]])[-2:]
        continue
    choices = [k for k in need if not (len(prev2) == 2 and prev2[0] == prev2[1] == k) and not (prev2 and prev2[-1] == k)] or need
    t = choices[0]
    need.remove(t)
    prev2 = (prev2 + [t])[-2:]
    perm = list(range(5))
    a = r["ans"] - 1
    perm.remove(a)
    perm.insert(t - 1, a)
    r["opts"] = [r["opts"][i] for i in perm]
    r["whys"] = [r["whys"][i] for i in perm]
    r["ans"] = t

# 난도: 강한 오답 2개 미만인 D4는 D3로, D4는 MCQ의 1/3 이하로 제한
for r in raw:
    if r.get("cr") or r["d"] != "D4":
        continue
    r["strong"] = sum(1 for i, w in enumerate(r["whys"]) if i != r["ans"] - 1 and w[0] == S)
    if r["strong"] < 2:
        r["d"] = "D3"
d4 = sorted([r for r in raw if not r.get("cr") and r["d"] == "D4"], key=lambda r: -r["strong"])
cap = total_mcq // 3
for r in d4[cap:]:
    r["d"] = "D3"
adv_ids = {id(r) for r in d4[:min(cap, int(total_mcq * 0.29))]}
for r in raw:
    if r.get("cr"):
        continue
    lens = [len(o) for o in r["opts"]]
    k = lens[r["ans"] - 1]
    others = sorted(lens[:r["ans"] - 1] + lens[r["ans"]:])
    if k > others[-1] and k / (sum(others) / 4) >= 1.25:
        print("LENGTH_CUE", r["topic"], r["opts"][r["ans"] - 1][:30])

# 독립 블라인드 검수의 실측 난도를 표기 난도로 채택(하한 원칙)
_bp = Path(__file__).with_name("blind_review.yaml")
BLIND = {b["item_id"]: b for b in yaml.safe_load(_bp.read_text(encoding="utf-8"))["items"]} if _bp.is_file() else {}
# 사용자 지시(2026-11-18): 문항마다 관련 조항 번호를 발문 앞에 표시
for r in raw:
    if r.get("topic") and not r["stem"].startswith("["):
        r["stem"] = f"[{r['topic']}] " + r["stem"]

n = 0
for r in raw:
    n += 1
    iid = f"KOR-ON1-{n:03d}"
    if iid in BLIND and BLIND[iid].get("difficulty"):
        r["d"] = BLIND[iid]["difficulty"]
        if r["d"] != "D4":
            adv_ids.discard(id(r))
    if r.get("cr"):
        items.append({"item_id": iid, "archetype": "C1_CONSTRUCTED_BLANK_SENTENCE", "format": "CR", "points": 5,
                      "stem": r["stem"], "view": r["view"], "conditions": r["conditions"], "model_answer": r["model"],
                      "rubric": r["rubric"], "ev": ["VIEW"], "difficulty": r["d"], "topic": r["topic"]})
        continue
    js = []
    strengths = [w[0] for i, w in enumerate(r["whys"]) if i != r["ans"] - 1]
    sb_idx = next((i for i, w in enumerate(r["whys"]) if i != r["ans"] - 1 and w[0] == S), None)
    for i, w in enumerate(r["whys"]):
        st, why, *tr = w
        is_ans = i == r["ans"] - 1
        j = {"axis": "orthography", "c": "CORRECT" if is_ans else st, "claim": f"{iid}-{i+1}", "ev": ["VIEW", f"OPTION{i+1}"],
             "v": (not is_ans) if r["neg"] else is_ans, "why": why or ("정답 근거: 해설 참고." if is_ans else "보기의 조항·자료에 비추어 바른 설명이다." if r["neg"] else "보기의 조항·자료와 맞지 않는다.")}
        if not is_ans:
            j["trap"] = tr[0] if tr else TRAP[r["arch"]]
        js.append(j)
    items.append({"item_id": iid, "archetype": r["arch"], "stem": r["stem"], "view": r["view"], "options": r["opts"],
                  "answer": r["ans"], "second_best": (sb_idx + 1) if sb_idx is not None else (1 if r["ans"] != 1 else 2),
                  "difficulty": r["d"], "family": "EXCEPT_INCORRECT" if (r["neg"] and r["arch"] == "A4_INQUIRY_DIALOGUE_CHECK") else FAM[r["arch"]],
                  "balance": "ADVANCED_DISCRIMINATION" if id(r) in adv_ids else "CORE_EXAM_POINT",
                  "reasoning_steps": STEPS[r["d"]], "immediate_elimination": 1, "transfer": True,
                  "stem_polarity": "NEGATIVE" if r["neg"] else "POSITIVE", "topic": r["topic"], "judgments": js})

bundle = {"batch_id": "KOR-ORTHO-NAESIN-150-SET1-20261118", "product_mode": "ARC_N", "subject": "KOR", "generator": "CLAUDE",
          "set_label": "ARC N° 맞춤법 내신형 150제 · 1세트", "course": "공통국어2",
          "cover_subtitle": "한글 맞춤법 1세트 50문항 (선택형 45 + 서답형 5)",
          "cover_lines": ["총칙 · 소리에 관한 것(된소리·구개음화·ㅖ/ㅢ·두음 법칙)", "형태에 관한 것 ①(체언·조사, 어간·어미, 파생어, -이/-히)",
                          "새 <보기> 조항·사전 자료·생활 지문·옛 표기·남북한 표기 추론형 중심"],
          "school_line": "동북고등학교 1학년 · 2026", "created_at": "2026-11-18T15:00:00+09:00",
          "scope": "미래엔 공통국어2 3-(2) 한글 맞춤법과 오늘날의 국어생활 (2026-2 기말 범위)",
          "scope_refs": ["TEXTBOOK:미래엔 공통국어2 3-(2) 한글 맞춤법", "NOTICE:DONGBUK_2026_2_FINAL_SCOPE_NOTICE",
                         "DRIVE:ARC_한글맞춤법_기출및규범_70제 (형식 참고, 문장 미사용)"],
          "layout": {"marked_sentence_paragraphs": True},
          "archetype_library": "quality/korean/ARC_KOR_GRAMMAR_ARCHETYPES_V1.0.yaml", "sets": [], "items": items}
Path(__file__).with_name("items.yaml").write_text(yaml.safe_dump(bundle, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")
from collections import Counter
print(len(items), "MCQ answers:", sorted(Counter(i["answer"] for i in items if "answer" in i).items()),
      "difficulty:", sorted(Counter(i["difficulty"] for i in items).items()))

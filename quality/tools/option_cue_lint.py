# -*- coding: utf-8 -*-
"""ARC 선지 경쟁력·단서 린트 (Distractor Competitiveness Lint) — V1.1

'읽지 않고도, 또는 선지 생김새만으로 맞힐 수 있는가'를 자동 점검한다. 기준선(무작위) = 20%.

사용 (저장소 루트에서):
    python3 quality/tools/option_cue_lint.py                 # 등록된 모든 세트
    python3 quality/tools/option_cue_lint.py N11 N12         # 일부 세트
    python3 quality/tools/option_cue_lint.py --report quality/reports/CUE_LINT.md
    python3 quality/tools/option_cue_lint.py --strict N12    # 게이트 미통과 시 종료 코드 1

새 세트 등록: 아래 REGISTRY에 (폴더, 문항 모듈, 지문 모듈) 추가.
문항 dict 필드: stem, choices, c(정답 인덱스), fixed(조합·순서형이면 True), table, box, boxpre.
게이트 기준은 quality/ARC_DISTRACTOR_ENGINEERING_V1.0.md 5장과 동일하게 유지한다.
"""
import sys, re, importlib, collections, statistics as st, pathlib, argparse

ROOT = pathlib.Path(__file__).resolve().parents[2]
KOR = ROOT / "outputs" / "KOR"
REGISTRY = {  # 이름: (폴더, [문항 모듈들], 지문 모듈)
    "FINAL01": ("ARC_FINAL_공통국어2_N01", ["items_final"], "passages_final"),
    "FINAL02": ("ARC_FINAL_공통국어2_N02", ["items_final2"], "passages_final2"),
    "N11": ("ARC_N11_시험범위11편_110Q", ["common", "items_a", "items_b", "items_c"], "passages_n11"),
    "N12": ("ARC_N12_보충자료4편_핵심40Q", ["common", "items_n12"], "passages_n12"),
}
# 게이트 기준: R0(2025 동북고 기출, n=18 선택형 분석) 실측 — 최장=정답 22%(긍정 발문 2/7), 정답/오답 길이 0.79배, 근접오답유사도 0.14
# 임시 기준(PROVISIONAL): 기출 표본이 작으므로 여유를 두고 설정. 어휘중복 정확도는 R0 지문 대조 전이라 20%+10%p로 가정.
GATE = dict(longest_pos=0.35, longest_all=0.30, overlap=0.30, ratio_lo=0.75, ratio_hi=1.25, abs_single=0.30)
ABS = ["완전히", "반드시", "오직", "전혀", "확정", "직접", "오히려", "항상", "절대", "결코", "일방적", "전부", "오로지", "즉시", "곧바로", "무관"]
NEG = re.compile("않|아닌|다른|틀린")
PURGE = ("common", "passages_final", "passages_final2", "items_final", "items_final2", "items_a", "items_b", "items_c",
         "items_n12", "passages_n11", "passages_n12", "apply_rev", "revise_a", "revise_b", "revise_c", "revise_d", "revise_e", "revise_f", "revise_g", "revise_n12", "revise_n12b", "revise_final")

def clean(t):
    return re.sub(r"\{.\|([^}]*)\}", r"\1", re.sub(r"<[^>]+>", "", t or ""))

def flat(o):
    if isinstance(o, str): yield o
    elif isinstance(o, dict):
        for v in o.values(): yield from flat(v)
    elif isinstance(o, (list, tuple)):
        for v in o: yield from flat(v)

def grams(t, n=2):
    t = re.sub(r"[^가-힣0-9A-Za-z]", "", clean(t))
    return collections.Counter(t[i:i + n] for i in range(len(t) - n + 1))

def jacc(a, b):
    ga, gb = set(grams(a)), set(grams(b))
    return len(ga & gb) / max(1, len(ga | gb))

def load(name):
    folder, mods, pmod = REGISTRY[name]
    src = str(KOR / folder / "src")
    for m in PURGE: sys.modules.pop(m, None)
    sys.path.insert(0, src)
    try:
        for m in mods: importlib.import_module(m)
        sets = importlib.import_module(pmod).SETS
        Q = sys.modules["common"].Q if "common" in sys.modules else sys.modules[mods[0]].Q
        if (KOR / folder / "src" / "apply_rev.py").exists():   # V1.1 개정본(REV) 반영
            importlib.import_module("apply_rev").apply(Q)
    finally:
        sys.path.remove(src)
    return Q, sets

def lint(name):
    Q, sets = load(name)
    R = collections.Counter(); ratios = []; best_sims = []; per = []
    for i, q in enumerate(Q, 1):
        if q.get("fixed") or q.get("table"): continue
        ch = [clean(c) for c in q["choices"]]
        if len(ch) != 5 or any(len(c) < 6 for c in ch): continue
        c = q["c"]; neg = bool(NEG.search(clean(q["stem"])))
        st_ = next(s for s in sets if s["rng"][0] <= i <= s["rng"][1])
        ctx = " ".join(flat(st_.get("parts", st_))) + " " + clean(q.get("box")) + " " + clean(q.get("boxpre"))
        cg = grams(ctx)
        ov = [sum(min(v, cg[k]) for k, v in grams(x).items()) / max(1, sum(grams(x).values())) for x in ch]
        ln = [len(x) for x in ch]; ab = [sum(w in x for w in ABS) for x in ch]
        R["n"] += 1; R["neg" if neg else "pos"] += 1
        longest = ln[c] == max(ln) and ln.count(max(ln)) == 1   # 동률은 단서가 아님
        R["longest"] += longest; R["longest_pos"] += (longest and not neg)
        _t = (min if neg else max)(ov); R["overlap"] += (ov[c] == _t and ov.count(_t) == 1)
        mo = st.mean(ln[k] for k in range(5) if k != c); r = ln[c] / mo; ratios.append(r)
        R["len_outlier"] += (r > 1.25 or r < 0.75)
        if neg and max(ab) > 0:
            R["abs_n"] += 1; R["abs_single"] += (ab.index(max(ab)) == c and ab.count(max(ab)) == 1)
        best_sims.append(max(jacc(ch[c], ch[k]) for k in range(5) if k != c))
        per.append((i, neg, longest, r))
    n = R["n"]
    return dict(name=name, n=n, pos=R["pos"], neg=R["neg"],
                longest=R["longest"] / n, longest_pos=R["longest_pos"] / max(1, R["pos"]),
                overlap=R["overlap"] / n, len_outlier=R["len_outlier"] / n, ratio=st.mean(ratios),
                abs_single=R["abs_single"] / max(1, R["abs_n"]), abs_n=R["abs_n"],
                best_sim=st.mean(best_sims), per=per)

def verdict(r):
    fails = []
    if r["longest_pos"] > GATE["longest_pos"]: fails.append(f"긍정 발문 최장=정답 {r['longest_pos']:.0%} > {GATE['longest_pos']:.0%}")
    if r["longest"] > GATE["longest_all"]: fails.append(f"전체 최장=정답 {r['longest']:.0%} > {GATE['longest_all']:.0%}")
    if r["overlap"] > GATE["overlap"]: fails.append(f"어휘중복 정확도 {r['overlap']:.0%} > {GATE['overlap']:.0%}")
    if not (GATE["ratio_lo"] <= r["ratio"] <= GATE["ratio_hi"]): fails.append(f"정답/오답 평균 길이 비 {r['ratio']:.2f} (허용 {GATE['ratio_lo']}~{GATE['ratio_hi']})")
    if r["abs_n"] >= 5 and r["abs_single"] > GATE["abs_single"]: fails.append(f"과잉 단정어 단독 적중 {r['abs_single']:.0%} > {GATE['abs_single']:.0%}")
    return fails

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*"); ap.add_argument("--report"); ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    names = a.names or list(REGISTRY)
    rows, bad = [], 0
    for nm in names:
        r = lint(nm); f = verdict(r); bad += bool(f)
        rows.append((r, f))
        print(f"{nm}: n={r['n']} 최장=정답 {r['longest']:.0%}(긍정 {r['longest_pos']:.0%}) 어휘중복 {r['overlap']:.0%} 길이이탈 {r['len_outlier']:.0%} "
              f"정답/오답길이 {r['ratio']:.2f}배 근접오답유사도 {r['best_sim']:.2f} → {'PASS' if not f else 'FAIL: ' + '; '.join(f)}")
    if a.report:
        L = ["# 선지 경쟁력 린트 결과", "", "기준선(무작위) 20%. 게이트: " + ", ".join(f"{k}={v}" for k, v in GATE.items()), "",
             "| 세트 | 대상 | 최장=정답 | 긍정 발문 최장=정답 | 어휘중복 정확도 | 길이 이탈 | 정답/오답 길이 | 근접오답 유사도 | 판정 |", "|---|---:|---:|---:|---:|---:|---:|---:|---|"]
        for r, f in rows:
            L.append(f"| {r['name']} | {r['n']} | {r['longest']:.0%} | {r['longest_pos']:.0%} | {r['overlap']:.0%} | {r['len_outlier']:.0%} | {r['ratio']:.2f} | {r['best_sim']:.2f} | {'PASS' if not f else 'FAIL'} |")
        for r, f in rows:
            if f: L += ["", f"**{r['name']}** 미통과 사유: " + "; ".join(f)]
        pathlib.Path(a.report).write_text("\n".join(L) + "\n", encoding="utf-8")
    if a.strict and bad: sys.exit(1)

if __name__ == "__main__":
    main()

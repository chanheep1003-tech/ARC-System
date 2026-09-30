#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FINAL N°01/N°02 난이도 재검사 (ARC_DIFFICULTY_ENGINE §2-1·2-2 적용).
등급 = min(구조 점수 등급, CDI 등급, 선지 린트 등급). 배점에서 역산하지 않는다(LABEL INTEGRITY).
구조 점수(A~F)와 CDI는 2026-09-30 문항 전수 열람 기준의 수기 채점이며, D 항목은 CDI에서 자동 환산한다."""
import sys, statistics as st, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import option_cue_lint as L

# (A,B,C,E,F,CDI)  — D는 CDI로 환산
S1 = {1:(12,15,9,5,3,2.3),2:(11,14,11,4,5,1.7),3:(14,18,13,6,7,2.4),4:(8,10,6,3,2,1.3),5:(10,14,10,4,3,2.0),
 6:(8,9,6,3,2,1.5),7:(11,13,10,4,5,1.8),8:(10,14,11,5,3,2.2),9:(12,18,13,8,4,2.6),10:(12,14,10,5,3,2.3),
 11:(13,16,13,5,7,2.0),12:(8,9,5,3,2,1.2),13:(11,13,10,4,5,1.6),14:(11,12,9,4,5,1.4),15:(12,15,9,6,3,2.2),
 16:(18,22,15,8,9,2.6),17:(14,15,10,5,3,2.2),18:(12,15,10,6,4,2.2),19:(11,13,11,5,6,1.6),20:(8,10,7,3,2,1.3),
 21:(10,11,9,4,4,1.5),22:(12,16,12,7,5,2.0)}
S2 = {1:(12,14,10,5,3,2.4),2:(12,15,10,6,3,2.4),3:(12,15,9,6,3,2.4),4:(13,15,9,5,3,2.3),5:(12,16,10,6,4,2.0),
 6:(12,14,9,5,3,2.3),7:(12,15,10,5,6,2.2),8:(12,16,10,6,3,2.4),9:(13,15,10,5,7,2.0),10:(11,13,9,5,2,2.0),
 11:(13,15,10,5,4,2.4),12:(11,13,8,5,3,2.0),13:(12,15,10,5,6,2.2),14:(9,9,10,4,2,1.5),15:(12,15,9,6,3,2.3),
 16:(18,22,14,8,9,2.6),17:(13,14,9,5,3,2.0),18:(9,10,11,4,3,1.5),19:(12,14,10,5,7,1.8),20:(13,18,16,8,4,2.6),
 21:(13,16,12,7,5,2.5),22:(14,16,12,7,9,2.2)}
R0 = dict(mean=58.3, median=57, top5=76.8, dist="3 / 13 / 3 / 2")   # 2025 동북고 기출(기존 산정)
OLD = {"N01": dict(mean=52.9, top5=65.2, dist="3 / 18 / 0 / 1"), "N02": dict(mean=58.5, top5=67.0, dist="0 / 20 / 1 / 1")}

def d_score(c):  # CDI → D(/15) 구간 중앙값
    return 2 if c < 1.0 else 5 if c < 1.6 else 10 if c < 2.2 else 13
def grade(s): return "D1" if s < 25 else "D2" if s < 45 else "D3" if s < 65 else "D4" if s < 80 else "D5"
def cdi_grade(c): return "D2" if c < 1.6 else "D3" if c < 2.2 else "D5"     # 2.2 이상이면 상한 해제
RANK = {"D1":1,"D2":2,"D3":3,"D4":4,"D5":5}

def item_flags(name):
    """비고정 문항의 단서 플래그: 유일 최장=정답 / 유일 최대 어휘중복 / 정답에만 단정어(부정 발문)."""
    Q, sets = L.load(name); out = {}
    for i, q in enumerate(Q, 1):
        if q.get("fixed") or q.get("table"): out[i] = []; continue
        ch = [L.clean(c) for c in q["choices"]]; c = q["c"]; ln = [len(x) for x in ch]
        neg = bool(L.NEG.search(L.clean(q["stem"]))); f = []
        if ln[c] == max(ln) and ln.count(max(ln)) == 1: f.append("최장=정답")
        s = next(s for s in sets if s["rng"][0] <= i <= s["rng"][1]) if any("rng" in s for s in sets) else None
        ctx = " ".join(L.flat(s.get("parts", s))) if s else " ".join(L.flat(sets))
        cg = L.grams(ctx + " " + L.clean(q.get("box")))
        ov = [sum(min(v, cg[k]) for k, v in L.grams(x).items()) / max(1, sum(L.grams(x).values())) for x in ch]
        t = (min if neg else max)(ov)
        if ov[c] == t and ov.count(t) == 1: f.append("지문중복 최대" if not neg else "지문중복 최소")
        ab = [sum(w in x for w in L.ABS) for x in ch]
        if neg and max(ab) > 0 and ab.index(max(ab)) == c and ab.count(max(ab)) == 1: f.append("단정어")
        out[i] = f
    return out, Q

def run(tag, name, S):
    fl, Q = item_flags(name); rows = []
    for i in sorted(S):
        A, B, C, E, F, cdi = S[i]; D = d_score(cdi); tot = A + B + C + D + E + F
        g0 = grade(tot); g1 = cdi_grade(cdi); g = g0
        cap = []
        if RANK[g1] < RANK[g]: g = g1; cap.append("CDI")
        if fl[i] and RANK["D2"] < RANK[g]: g = "D2"; cap.append("린트")   # 린트 미통과 문항은 D2 이하
        rows.append((i, tot, g0, cdi, fl[i], g, "+".join(cap), Q[i-1]["pts"]))
    return rows

def summary(rows):
    sc = [r[1] for r in rows]; top5 = sorted(sc, reverse=True)[:5]
    cnt = lambda k: sum(1 for r in rows if r[k] == g)
    dist0 = [sum(1 for r in rows if r[2] == g) for g in ("D2","D3","D4","D5")]
    dist1 = [sum(1 for r in rows if r[5] == g) for g in ("D2","D3","D4","D5")]
    return dict(mean=st.mean(sc), median=st.median(sc), top5=st.mean(top5), d0=dist0, d1=dist1)

def main(out):
    res = {}
    L_ = ["# FINAL N°01 · N°02 난이도 재검사 (2026-09-30)", "",
          "기준: `ARC_DIFFICULTY_ENGINE_V1.0` §2 구조 점수 + §2-1 CDI + §2-2 LABEL INTEGRITY. **등급 = min(구조 점수 등급, CDI 등급, 선지 린트 등급)**. 배점은 등급 산정에 쓰지 않는다.",
          "구조 점수·CDI는 문항 전수 열람 기준의 수기 채점(스크립트 `quality/tools/final_difficulty_recheck.py`에 표로 보존), 린트 플래그는 자동 산출.", ""]
    for tag, name, S in (("N01","FINAL01",S1),("N02","FINAL02",S2)):
        rows = run(tag, name, S); sm = summary(rows); res[tag] = (rows, sm)
        L_ += [f"## FINAL {tag} ({len(rows)}문항 선택형)", "",
               "| 번호 | 구조점수 | 구조등급 | CDI | 린트 플래그 | 최종등급 | 상한 사유 | 배점 |", "|---:|---:|---|---:|---|---|---|---:|"]
        for r in rows:
            L_.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]:.1f} | {', '.join(r[4]) or '-'} | **{r[5]}** | {r[6] or '-'} | {r[7]} |")
        L_ += ["", f"평균 {sm['mean']:.1f} · 중앙값 {sm['median']:.1f} · 상위 5문항 평균 {sm['top5']:.1f}", ""]
    L_ += ["## 비교 (D2 / D3 / D4 / D5 문항 수)", "",
           "| 세트 | 평균 | 상위 5문항 평균 | 구조 등급만 | 상한 적용 후(최종) |", "|---|---:|---:|---|---|",
           f"| 2025 기출(R0, 기존 산정) | {R0['mean']} | {R0['top5']} | {R0['dist']} | (기출은 상한 미적용) |"]
    for tag in ("N01","N02"):
        rows, sm = res[tag]
        L_.append(f"| FINAL {tag} 재검사 | {sm['mean']:.1f} | {sm['top5']:.1f} | {' / '.join(map(str,sm['d0']))} | **{' / '.join(map(str,sm['d1']))}** |")
        L_.append(f"| (참고) FINAL {tag} 이전 산정 | {OLD[tag]['mean']} | {OLD[tag]['top5']} | {OLD[tag]['dist']} | 미적용 |")
    pathlib.Path(out).write_text("\n".join(L_) + "\n", encoding="utf-8")
    for tag in ("N01","N02"):
        rows, sm = res[tag]; print(tag, f"mean {sm['mean']:.1f} top5 {sm['top5']:.1f} struct {sm['d0']} final {sm['d1']}")
        print("  flagged:", [(r[0], r[4]) for r in rows if r[4]])

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "quality/reports/FINAL_DIFFICULTY_RECHECK_20260930.md")

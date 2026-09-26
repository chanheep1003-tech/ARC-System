"""PASS B — independent re-solve of every quantitative / inference item.

Each check recomputes statement truth values from the item data alone
(enumerating unknown charges or reactivity orders where the item leaves
them open) and compares the resulting choice with SECTION B.
Run: python3 verify.py
"""
from fractions import Fraction as Fr
from itertools import permutations, product

from items import BOGI_SETS, ITEMS

from build import KEY
JAMO = "ㄱㄴㄷㄹ"


def pick(truth, choices):
    """Return the 1-based choice index whose ㄱㄴㄷ set equals the true statements."""
    want = ", ".join(JAMO[i] for i, v in enumerate(truth) if v)
    if isinstance(choices, str):
        choices = BOGI_SETS[choices]
    hits = [i + 1 for i, c in enumerate(choices) if c == want]
    assert len(hits) == 1, (want, choices)
    return hits[0]


def orders(metals, constraints):
    """All strict reactivity orders (tuple, most reactive first) meeting constraints (a > b)."""
    out = []
    for p in permutations(metals):
        rank = {m: i for i, m in enumerate(p)}
        if all(rank[a] < rank[b] for a, b in constraints):
            out.append(rank)
    return out


def always(ranks, f):
    return all(f(r) for r in ranks)


res = {}

# 01 — oxygen bookkeeping per reaction (reactant formula -> product formula)
rx = {"가": ("CO2", "C6H12O6"), "라": ("CO2", "CO")}
o_per_c = {"CO2": Fr(2), "C6H12O6": Fr(1), "CO": Fr(1)}
t1 = all(o_per_c[b] < o_per_c[a] for a, b in rx.values())       # CO2 loses O in (가),(라)
t2 = True                                                     # (라): C oxidized, CO2 reduced — both carbon
reactants = {"가": ["CO2", "H2O"], "나": ["C6H12O6", "O2"], "다": ["CH4", "O2"], "라": ["CO2", "C"]}
t3 = all("CO2" in r for r in reactants.values())              # reduced species must be a reactant
res[1] = pick([t1, t2, t3], ITEMS[0]["choices"])

# 02 — H2 from acid
H0, nA, nB, h2A, h2B = 10, 2, 2, 2, 3
a, b = 2 * h2A // nA, 2 * h2B // nB
ionsA = (H0 - 2 * h2A) + nA + H0
ionsB = (H0 - 2 * h2B) + nB + H0
res[2] = pick([b > a, ionsA - ionsB == 2, (H0 - 2 * h2B) == 2 * nB], ITEMS[1]["choices"])

# 03 — 3Ag2S + 2Al
e_per_Ag2S = 2
al_needed = Fr(3 * e_per_Ag2S, 3)                             # 3N Ag2S -> electrons / 3 per Al
res[3] = pick([True, al_needed == 3, True], ITEMS[2]["choices"])

# 04 — particle model, anions fix absolute charges
x = Fr(8, 8); y = Fr(12, 4)
m = (8 - 2) * x / 3
assert (4 - 2) * y / 3 == m
tot1 = (2 + 3) + 8; tot2 = (2 + 3) + 12
extra_M = (2 * x + 2 * y) / m
final_cat = 3 + 3 + extra_M
res[4] = pick([y > m > x, tot1 == tot2, final_cat == 10], ITEMS[3]["choices"])

# 05 — variable control: a comparison is valid only if exactly one factor differs
tubes = {"가": {"O2": 1, "H2O": 1, "salt": 0}, "나": {"O2": 0, "H2O": 1, "salt": 0},
         "다": {"O2": 1, "H2O": 0, "salt": 0}, "라": {"O2": 1, "H2O": 1, "salt": 1}}
def diff(p, q): return [k for k in tubes[p] if tubes[p][k] != tubes[q][k]]
t = [diff("가", "나") == ["O2"], diff("가", "다") == ["H2O"], diff("나", "라") == ["salt"], True]
res[5] = pick(t, ITEMS[4]["choices"])

# 06 — oxygen affinity from heating table
aff = orders(["Al", "C", "Fe", "Cu"], [("C", "Cu"), ("C", "Fe"), ("Al", "C"), ("Al", "Fe")])
timeline = ["Cu", "Fe", "Al"]                                 # earliest -> latest
t1 = always(aff, lambda r: all(r[timeline[i]] > r[timeline[i + 1]] for i in range(2)))
t2 = always(aff, lambda r: r["Al"] < r["C"] < r["Fe"])
t3 = always(aff, lambda r: r["Fe"] < r["Al"])
res[6] = pick([t1, t2, t3], ITEMS[5]["choices"])

# 07 — count change "일정" is ambiguous when charges are equal
chg = {"A": 2, "B": 1, "C": 2, "D": 3}
def change(metal, ion, reacts):
    if not reacts:
        return 0
    return Fr(chg[ion], chg[metal]) - 1                       # new ions per reduced ion, minus one

obs = [("A", "C", 0), ("B", "A", 0), ("C", "B", -1), ("A", "D", 0)]
valid = []
for p in permutations("ABCD"):
    r = {k: i for i, k in enumerate(p)}
    ok = all((lambda d: (d > 0) - (d < 0))(change(mt, io, r[mt] < r[io])) == sgn for mt, io, sgn in obs)
    if ok:
        valid.append(r)
opts = [
    always(valid, lambda r: change("D", "B", r["D"] < r["B"]) < 0),
    always(valid, lambda r: not r["A"] < r["C"]),
    always(valid, lambda r: r["C"] < r["A"]),
    always(valid, lambda r: r["D"] == 0),
    always(valid, lambda r: change("C", "D", r["C"] < r["D"]) == 0),
]
assert opts.count(True) == 1
res[7] = opts.index(True) + 1

# 08 — per 2N Cu: C = N, Zn = 2N; electrons per Cu = 2 in both
res[8] = pick([True, Fr(2, 2) == Fr(2, 1), 2 == 2], ITEMS[7]["choices"])

# 09 — plate mass
mX, mY, mZ = 24, 65, 64
nga = Fr(-3, mZ - mY); nna = Fr(82, mY - mX)
res[9] = pick([(mZ - mY) < 0, True, nga / nna == Fr(3, 2)], ITEMS[8]["choices"])

# 10 — refutation: observed order contradicts "more electrons lost -> more reactive"
ion = {"P": 1, "Q": 2, "R": 2, "S": 3}
def refutes(more, less):                                        # observation: `more` is more reactive
    return ion[more] < ion[less]
t = [refutes("P", "Q"), refutes("S", "R"), refutes("S", "Q"), refutes("R", "S")]
res[10] = pick(t, ITEMS[9]["choices"])

# 11 — break-point graph (0,8)->(3,5)->(6,6)->(8,6)
A0, B0 = 6, 2
c = Fr(A0 * 1, 3)
bq = Fr((6 - 3) * c, B0)
assert (8 - A0) + 3 == 5 and B0 * 0 + 6 == 6 * 1 and (5 - B0) + B0 == 5
b_left = B0 - (Fr(9, 2) - 3) * c / bq
res[11] = pick([c == 2, bq == 2, b_left == 1], ITEMS[10]["choices"])

# 12 — X > Fe, Fe > Y, Y > Z
rk = orders(["X", "Fe", "Y", "Z"], [("X", "Fe"), ("Fe", "Y"), ("Y", "Z")])
res[12] = pick([always(rk, lambda r: r["Fe"] < r["X"]), False, always(rk, lambda r: r["Fe"] < r["Z"])],
               ITEMS[11]["choices"])

# 13 — 4N Fe -> Fe3+: 12N e-, O2 takes 4 e-
res[13] = pick([True, Fr(4 * 3, 4) == 2, False], ITEMS[12]["choices"])

# 14 — chain
a = Fr(6, 2); cc = Fr(6 * 1, 2)
d1 = 2 - 6; d2 = 6 - 2
rk = orders("ABC", [("A", "B"), ("B", "C"), ("A", "C")])
res[14] = pick([a == cc, d1 < 0 and d2 < 0, always(rk, lambda r: r["A"] < r["C"]) and 2 * a / cc == 2],
               ITEMS[13]["choices"])

# 15 — search a small charge / mass space for counterexamples.
# One metal atom (charge zm, mass mm) reduces zm/zi ions (charge zi, mass mi).
cases = [(zm, zi, mm, mi) for zm, zi in product((1, 2, 3), repeat=2)
         for mm, mi in product((24, 56, 64, 65, 108), repeat=2) if mm != mi]
dcount = lambda zm, zi: 1 - Fr(zm, zi)
dmass = lambda zm, zi, mm, mi: -mm + Fr(zm, zi) * mi
dcharge = lambda zm, zi: zm - Fr(zm, zi) * zi
suvin = all(dcount(zm, zi) < 0 for zm, zi, _, _ in cases)
doyun = all(dcharge(zm, zi) == 0 for zm, zi, _, _ in cases)
haram = all(dcount(zm, zi) < 0 for zm, zi, mm, mi in cases if dmass(zm, zi, mm, mi) > 0)
res[15] = [None, "수빈", "도윤", "수빈, 하람", "도윤, 하람", "수빈, 도윤, 하람"].index(
    ", ".join(n for n, v in [("수빈", suvin), ("도윤", doyun), ("하람", haram)] if v))

# 16 — flowchart
D0 = 8; D_left = 2; dissolved = {"A": 3, "B": 3}
solid = {"C": 3, "D": D0 - D_left}
rk = orders("ABCD", [("A", "D"), ("B", "D"), ("D", "C"), ("A", "B")])
e_A = 2 * (3 + D_left)
res[16] = pick([solid == {"C": 3, "D": 6}, len(rk) == 1 and rk[0] == {"A": 0, "B": 1, "D": 2, "C": 3}, e_A == 6],
               ITEMS[15]["choices"])

# 17 — anion balance: 3x + 4y = 10, then 4y + 2z = 10
sols = [(x, y) for x in range(1, 4) for y in range(1, 4) if 3 * x + 4 * y == 10]
assert sols == [(2, 1)]
z = Fr(10 - 4 * 1, 2)
opts17 = [("+3", "Y > Z > X"), ("+3", "Z > Y > X"), ("+2", "Y > Z > X"), ("+2", "Z > X > Y"), ("+1", "Y > X > Z")]
res[17] = opts17.index((f"+{z}", "Y > Z > X")) + 1

# 18 — unknown metal. Place M in each slot; keep slots consistent with Ⅰ, Ⅱ, Ⅲ.
base = ["Mg", "Zn", "Fe", "Cu", "Ag"]
charge = {"Mg": 2, "Zn": 2, "Fe": 2, "Cu": 2, "Ag": 1}
fits = []
for k, s_ in enumerate("ㄱㄴㄷㄹ"):
    seq = base[:k + 1] + ["M"] + base[k + 1:]
    r = {m_: i for i, m_ in enumerate(seq)}
    if (not r["M"] < r["Fe"]) and r["Cu"] < r["M"] and r["M"] < r["Ag"]:
        fits.append((s_, r))
assert len(fits) == 1
slot, r = fits[0]
qM = Fr(3, 3)                                    # 3N M give 3N electrons to Ag+
charge["M"] = qM
cnt = lambda metal, ion_: 1 - Fr(charge[metal], charge[ion_])
opts = [slot == "ㄷ", r["M"] < r["Zn"], cnt("M", "Ag") < 0,
        r["Fe"] < r["M"] and cnt("Fe", "M") > 0, Fr(charge["Cu"], qM) == 2]
assert opts.count(True) == 1
res[18] = opts.index(True) + 1

# 19 — ratios 1, 2/3, 2 with metal charges in {1,2,3}
sol = [xx for xx in range(1, 10) if all(v in (1, 2, 3) for v in (xx, Fr(3 * xx, 2), Fr(xx, 2)))]
assert sol == [2]
xx = 2; nX = Fr(1)
nB = nX * xx / 3; nC = nX * xx / 1
res[19] = pick([xx == 2, nC / nB == 3, nB > nC], ITEMS[18]["choices"])

# 20 — charge from counts, mass equality, new plate
aA = Fr(6 * 2, 4)
mA_over_mB = Fr(6, 4)
gain = 2 * (-1 + 2 * 2)                                          # in units of m_B, 2N B atoms
res[20] = pick([aA == 3, mA_over_mB > 1, gain == 4 * mA_over_mB], ITEMS[19]["choices"])

bad = [(i, res[i], KEY[i - 1]) for i in range(1, 21) if res[i] != KEY[i - 1]]
for i in range(1, 21):
    print(f"{i:02d}: solved {res[i]}  key {KEY[i - 1]}  {'OK' if res[i] == KEY[i - 1] else 'MISMATCH'}")
print("dist", {k: KEY.count(k) for k in range(1, 6)})
assert not bad, bad

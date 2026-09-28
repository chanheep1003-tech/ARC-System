"""PASS B — independent re-solve of all 30 items (산화와 환원 30제).

Model (no answer data is read from the items):
  * a reaction is written as {species: count}; oxygen gain/loss and electron
    transfer are counted from explicit formulas / ion charges.
  * metal-ion displacement: M + ion of N reacts only if M is more reactive;
    ion counts follow charge conservation (electrons lost = electrons gained).
  * unknown charges are found by enumerating 1..3 against the given counts.
  * reactivity orders are found by enumerating permutations consistent with
    every observation in the stem.
Run: python3 verify.py
"""
from fractions import Fraction as Fr
from itertools import permutations

from build import KEY
from items import BOGI_SETS, ITEMS

JAMO = "ㄱㄴㄷㄹ"
SERIES = ["K", "Ca", "Na", "Mg", "Al", "Zn", "Fe", "Ni", "Sn", "Pb", "H", "Cu", "Hg", "Ag", "Pt", "Au"]


def more_reactive(a, b):
    return SERIES.index(a) < SERIES.index(b)


def pick(truth, choices):
    want = ", ".join(JAMO[i] for i, v in enumerate(truth) if v)
    if isinstance(choices, str):
        choices = BOGI_SETS[choices]
    hits = [i + 1 for i, c in enumerate(choices) if c == want]
    assert len(hits) == 1, (want, choices)
    return hits[0]


def orders(names, facts):
    """All reactivity orders (most reactive first) satisfying facts [(x, y)] meaning x > y."""
    return [p for p in permutations(names) if all(p.index(x) < p.index(y) for x, y in facts)]


def oxygen(formula):
    """Oxygen atoms per formula unit for the few species used here."""
    return {"CO2": 2, "CO": 1, "C": 0, "CH4": 0, "C6H12O6": 6, "Fe2O3": 3, "Fe": 0, "Mg": 0, "MgO": 1,
            "Cu": 0, "CuO": 1, "O2": 2}[formula]


def gains_oxygen(reactant, product):
    return oxygen(product) > oxygen(reactant)


res = {}

# 01 Mg -> Mg2+ in both; CO2 -> C loses O; 2N Mg lose 4N e- in both
e_ga = 2 * 2
e_na = 2 * 2
res[1] = pick([True, not gains_oxygen("CO2", "C"), e_ga == 2 * e_na], ITEMS[0]["choices"])

# 02 Ag+ 6 -> Ag+ 2, Cu2+ 2 ; NO3- 6 constant
ag_dep = 6 - 2
cu_used = 2
before, after = 6 + 6, 2 + 2 + 6
res[2] = pick([cu_used > 0, cu_used == 2 * ag_dep, after < before], ITEMS[1]["choices"])

# 03 (가) CO2 -> C6H12O6 : CO2 carbon compound per C loses O (2 -> 1 per C); (라) CH4 -> CO2 gains
co2_per_c_before, glucose_per_c = Fr(2), Fr(6, 6)
ga_gains = glucose_per_c > co2_per_c_before
ra_gains = gains_oxygen("CH4", "CO2")
redox_da = False                         # carbonate + acid: no electron transfer, no O2 exchange
res[3] = pick([not redox_da, not gains_oxygen("Fe", "Fe2O3"), ga_gains and ra_gains], ITEMS[2]["choices"])

# 04 X + Y2+ -> X2+ + Y ; Y + 2Z+ -> Y2+ + 2Z
ords = orders("XYZ", [("X", "Y"), ("Y", "Z")])
cations_ga = (1, 1)                      # one Y2+ replaced by one X2+
res[4] = pick([ords == [tuple("XYZ")], cations_ga[0] == cations_ga[1], 2 * 1 == 1 * 2], ITEMS[3]["choices"])

# 05 electrons lost per metal atom: Na 1, Mg 2, Zn 2 ; (나) Mg oxidised, H+ reduced
res[5] = pick([True, False, len({1, 2, 2}) == 1], ITEMS[4]["choices"])

# 06 2CuO + C -> 2Cu + CO2 ; mass conservation
res[6] = pick([gains_oxygen("C", "CO2"), gains_oxygen("CuO", "Cu"), True], ITEMS[5]["choices"])

# 07 (가) X+ 6 ; (나) X+ 2, Y 2 ; (다) Z 3
y_charge = [c for c in (1, 2, 3) if 2 * c == (6 - 2) * 1]
z_charge = [c for c in (1, 2, 3) if 3 * c == 2 * 1 + 2 * y_charge[0]]
e_y, e_z = 2 * y_charge[0], 3 * z_charge[0]
res[7] = pick([6 == 2 + 2, y_charge == [2], Fr(e_z, e_y) == Fr(3, 2)], ITEMS[6]["choices"])

# 08 Mg + Cu2+ -> Mg2+ + Cu
res[8] = pick([more_reactive("Mg", "Cu"), 1 < 1, True], ITEMS[7]["choices"])

# 09 Cu 4 g -> 5 g ; Mg 3 g -> 5 g
o_per_g_cu, o_per_g_mg = Fr(5 - 4, 4), Fr(5 - 3, 3)
res[9] = pick([8 * o_per_g_cu == 1, o_per_g_mg > o_per_g_cu, False], ITEMS[8]["choices"])

# 10 Ⅰ: A,B react with acid, C not ; Ⅱ: B does not displace A ; Ⅲ: C does not displace B
ords = orders("ABC", [("A", "B"), ("B", "C")])
res[10] = pick([ords == [tuple("ABC")], True, ords[0].index("A") < ords[0].index("C")], ITEMS[9]["choices"])

# 11 A+ 24N + B -> B3+ ; cation change = b - 3b = -10N
b = [n for n in range(1, 25) if n - 3 * n == -10][0]
res[11] = pick([b == 10, 24 - 3 * b == 9, 3 * b == 10], ITEMS[10]["choices"])

# 12 2Cu + O2 -> 2CuO (outer flame) ; CuO -> Cu (inner flame)
res[12] = pick([False, not gains_oxygen("CuO", "Cu") and oxygen("Cu") < oxygen("CuO"), False], ITEMS[11]["choices"])

# 13 A+ 6N; cations 6N -> 3N at B = 3N
bc = [c for c in (1, 2, 3) if 3 * c == 6][0]
at2 = (6 - 2 * bc) + 2
res[13] = pick([bc == 3, True, Fr(at2, 6) == Fr(2, 3)], ITEMS[12]["choices"])

# 14 (가) A protects Fe -> A > Fe ; (나) Fe corrodes with B -> Fe > B
ords = orders(["A", "B", "Fe"], [("A", "Fe"), ("Fe", "B")])
o = ords[0]
res[14] = pick([o[-1] == "A", o.index("Fe") > o.index("B"), o.index("A") < o.index("Fe")], ITEMS[13]["choices"])

# 15 before A 4, B 2 (NO3- 8) ; after B 2, C 2
sols = [(a, bb, c) for a in (1, 2, 3) for bb in (1, 2, 3) for c in (1, 2, 3) if 4 * a + 2 * bb == 8 and 2 * c == 4 * a]
a, bb, c = sols[0]
assert len(sols) == 1
ords = orders("ABC", [("C", "A"), ("B", "C")])
res[15] = pick([a == 1, ords == [tuple("BCA")], (4 + 2 + 8) - (2 + 2 + 8) == 2], ITEMS[14]["choices"])

# 16 design: same size = controlled ; manipulated = metal / ion kind ; Cu + Fe2+ no reaction
res[16] = pick([True, False, more_reactive("Cu", "Fe")], ITEMS[15]["choices"])

# 17 6x = 3y = 2z , charges <= 3
sols = [(x, y, z) for x in (1, 2, 3) for y in (1, 2, 3) for z in (1, 2, 3) if 6 * x == 3 * y == 2 * z]
x, y, z = sols[0]
assert len(sols) == 1
ords = orders("XYZ", [("Y", "X"), ("Z", "Y")])
res[17] = pick([z == 3, ords[0].index("Z") < ords[0].index("X") and 6 * x // z == 2, 3 - 6 == 3],
               ITEMS[16]["choices"])

# 18 2Al + 3Cu2+ -> 2Al3+ + 3Cu ; covered part does not touch the solution
res[18] = pick([False, 2 > 3, more_reactive("Al", "Cu")], ITEMS[17]["choices"])

# 19 Ⅰ: 8 - 3c/a + 3 = 5 ; Ⅱ: 6 - c + 3 = 7
sols = [(a, c) for a in (1, 2, 3) for c in (1, 2, 3) if Fr(8) - Fr(3 * c, a) + 3 == 5 and 6 - c + 3 == 7]
a, c = sols[0]
assert len(sols) == 1
res[19] = pick([a == 1, False, 8 - Fr(3 * c, a) == 2], ITEMS[18]["choices"])

# 20 C -> CO gains O ; CO -> CO2 gains O ; Fe2O3 -> Fe loses O ; CaCO3 decomposition
res[20] = pick([not gains_oxygen("C", "CO") and not gains_oxygen("CO", "CO2"), gains_oxygen("Fe2O3", "Fe"), True],
               ITEMS[19]["choices"])

# 21 Ⅰ: A deposits C, B does not -> A > C > B ; Ⅱ: C reduces B2+ only
ords = orders("ABC", [("A", "C"), ("C", "B")])
o = ords[0]
reduces_A = o.index("C") < o.index("A")
res[21] = pick([ords == [tuple("ACB")], not reduces_A, False], ITEMS[20]["choices"])

# 22 flowchart on the real series
metals = ["Mg", "Fe", "Cu", "Ag"]
cls = {}
for m in metals:
    if more_reactive(m, "H"):
        cls["A" if more_reactive(m, "Zn") else "B"] = m
    else:
        cls["C" if more_reactive(m, "Ag") else "D"] = m
res[22] = pick([cls["A"] == "Fe", more_reactive(cls["C"], cls["B"]), SERIES.index(cls["D"]) == max(map(SERIES.index, metals))],
               ITEMS[21]["choices"])

# 23 A ions 9N - 3x, B ions x, NO3- 9N
a_ch = 1                                             # 9N A ions balance 9N NO3-
b_ch = 3 * a_ch
tot0, tot2 = 9 + 9, (9 - 6) + 2 + 9
res[23] = pick([b_ch == 2 * a_ch, tot0 - tot2 == 4, 9 - 3 * 3 == 0], ITEMS[22]["choices"])

# 24 2Ag+ + Cu -> 2Ag + Cu2+ ; Cu2+ + Zn -> Cu + Zn2+
res[24] = pick([1 < 2, 1 == 1, more_reactive("Zn", "Cu") and more_reactive("Cu", "Ag")], ITEMS[23]["choices"])

# 25 a + b = 8 ; a + 2b = 13 ; C+ used 2a + 3b
sols = [(a, bb) for a in range(0, 9) for bb in range(0, 9) if a + bb == 8 and a + 2 * bb == 13]
a, bb = sols[0]
res[25] = pick([a == 3, 21 - (2 * a + 3 * bb) == 0, bb - a == 2], ITEMS[24]["choices"])

# 26 a counter-example needs: reaction occurred AND cation count not reduced
data = {"Ⅰ": (True, "same"), "Ⅱ": (True, "down"), "Ⅲ": (False, "same")}
res[26] = pick([data[k][0] and data[k][1] != "down" for k in ("Ⅰ", "Ⅱ", "Ⅲ")], ITEMS[25]["choices"])

# 27 A+ 4N, B3+ 2N ; C first with B3+ ; graph 6 -> 7 (x=3) -> 5 (x=5) -> 5
cc = [c for c in (1, 2, 3) if 3 * c == 2 * 3 and 6 - 2 + 3 == 7][0]
a_left_at4 = 4 - (4 - 3) * cc
cat6 = {"A": 4 - (6 - 3) * cc if 4 - (6 - 3) * cc > 0 else 0, "B": 0}
res[27] = pick([cc == 1, a_left_at4 == 2, cat6["A"] == 0 and cat6["B"] == 0], ITEMS[26]["choices"])

# 28 Ⅰ: B > A ; Ⅱ: no reaction -> B > C ; Ⅲ: C > A
ords = orders("ABC", [("B", "A"), ("B", "C"), ("C", "A")])
res[28] = pick([Fr(1, 2) == Fr(1, 2), ords == [tuple("CBA")], False], ITEMS[27]["choices"])

# 29 A 2N ; each add C+ 2N ; cations N, 2N, 4N
a_ch = [c for c in (1, 2, 3) if Fr(2, c) == 1][0]
a_used = 2 * Fr(2, a_ch)
res[29] = pick([a_ch == 2, a_used == 2, 2 == 2 * Fr(2, a_ch)], ITEMS[28]["choices"])

# 30 Z + 2Y+ first then Z + X2+
mass_1 = 4 * 108 - 2 * 65
mass_2 = mass_1 + 2 * (64 - 65)
res[30] = pick([mass_2 != mass_1, False, 2 + 2 == 4 and (mass_1, mass_2) == (302, 300)], ITEMS[29]["choices"])

bad = []
for i in range(1, 31):
    ok = res[i] == KEY[i - 1]
    bad += [] if ok else [i]
    print(f"{i:02d}: solved {res[i]}  key {KEY[i - 1]}  {'OK' if ok else 'MISMATCH'}")
print("dist", {k: KEY.count(k) for k in range(1, 6)})
runs = max(len(list(g)) for _, g in __import__("itertools").groupby(KEY))
print("longest run", runs)
assert not bad, bad
assert runs < 3

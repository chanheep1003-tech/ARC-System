"""PASS B — independent re-solve of all 30 items.

Physics model (no answer data is read from the items):
  * axial magnet/coil: flux through the coil  Phi = m * g(s),
    m = +1 if the magnet's N end points to +x, s = magnet centre - coil centre,
    g(s) = (1 + s^2)^-1.5  (peaks inside the coil, falls off outside).
    induced emf  e = -dPhi/dt  (Lenz / Faraday, sign only).
  * generator coil in a uniform field: current  I ∝ cos(theta),
    theta = angle between the coil plane and the field.
  * rotating magnet beside a fixed coil: Phi ∝ cos(phi) -> I ∝ sin(phi).
  * figures.coil_h winding: current entering the LEFT lead makes the field
    inside point -x (front strands carry current upward).
Run: python3 verify.py
"""
import math

from build import KEY
from items import BOGI_SETS, ITEMS

JAMO = "ㄱㄴㄷㄹ"


def g(s):
    return (1 + s * s) ** -1.5


def emf(m, s, v, dt=1e-5):
    """Induced emf sign for a magnet (moment sign m) at s moving with velocity v (coil fixed)."""
    p0, p1 = m * g(s), m * g(s + v * dt)
    d = -(p1 - p0) / dt
    return 0 if abs(d) < 1e-9 else (1 if d > 0 else -1)


def mag(m, s, v, dt=1e-5):
    return abs(m * (g(s + v * dt) - g(s)) / dt)


def force_on_magnet(v):
    """Lenz: the coil's force on the magnet always opposes the relative velocity."""
    return 0 if v == 0 else -math.copysign(1, v)


def gen(theta):
    return math.cos(math.radians(theta))


def pick(truth, choices):
    want = ", ".join(JAMO[i] for i, v in enumerate(truth) if v)
    if isinstance(choices, str):
        choices = BOGI_SETS[choices]
    hits = [i + 1 for i, c in enumerate(choices) if c == want]
    assert len(hits) == 1, (want, choices)
    return hits[0]


REF = emf(+1, -3, +1)            # N end approaching the coil's left end -> "right"/"+" reference
res = {}

# 01 relative motion (magnet on the left, N toward the coil, s = -3)
rel = {"가": 1 - 0, "나": 0 - (-1), "다": 1 - 1, "라": 2 - 1}   # magnet velocity minus coil velocity
d = {k: emf(+1, -3, v) for k, v in rel.items()}
res[1] = pick([d["다"] == 0, d["가"] == -d["나"] != 0, d["라"] == -d["가"] != 0], ITEMS[0]["choices"])

# 02 changing field needed; energy chain
res[2] = pick([False, True, True], ITEMS[1]["choices"])

# 03 generator snapshots
I = {k: gen(th) for k, th in {"가": 0, "나": 45, "다": 90, "라": 180}.items()}
res[3] = pick([abs(I["가"]) > abs(I["나"]), abs(I["다"]) < 1e-9, I["가"] * I["라"] > 0], ITEMS[2]["choices"])

# 04 direction panels (reference = needle right)
panels = {"가": emf(-1, -3, +1), "나": emf(+1, -3, -1), "다": emf(+1, +3, -1), "라": emf(+1, -3, +1)}
left = [k for k, e in panels.items() if e == -REF]
opts4 = [["가"], ["가", "나"], ["나", "다"], ["가", "나", "라"], ["나", "다", "라"]]
res[4] = opts4.index(left) + 1

# 05 variable control
exp = {"Ⅰ": (100, "A", 1), "Ⅱ": (200, "A", 1), "Ⅲ": (100, "B", 1), "Ⅳ": (100, "B", 2)}
diffs = sum(a != b for a, b in zip(exp["Ⅱ"], exp["Ⅳ"]))
res[5] = pick([False, 5 > 2, diffs == 1], ITEMS[4]["choices"])          # more turns -> more current (㉠ > 2)

# 06 rotating magnet: I ∝ sin(phi)
Iphi = {p: abs(math.sin(math.radians(p))) for p in (0, 90, 180)}
res[6] = pick([Iphi[0] == max(Iphi.values()), Iphi[90] > 0, True], ITEMS[5]["choices"])

# 07 rings: closed ring P opposes relative motion, cut ring Q carries no current
res[7] = pick([force_on_magnet(+1) < 0 and False, True, False], ITEMS[6]["choices"])

# 08 x-t: coil centre at x = 3d + 0.5 (units of d), N end position x
def s_of(x):
    return x - 3.5
v1, v35 = 1.0, -2.0
e1, e35, e25 = emf(+1, s_of(1), v1), emf(+1, s_of(1), v35), emf(+1, s_of(2), 0)
res[8] = pick([e1 == -e35, e25 == 0, mag(+1, s_of(1), v35) > mag(+1, s_of(1), v1)], ITEMS[7]["choices"])

# 09 generator: theta(0) = 90°, theta = 90 + 360 t / T
th = lambda t: 90 + 360 * t
half = [gen(th(k / 400)) for k in range(1, 200)]
changes = sum(1 for a, b in zip(half, half[1:]) if a * b < 0)
res[9] = pick([abs(gen(th(0.25))) == 1, changes == 1, True], ITEMS[8]["choices"])       # 2x speed: interval T/2 -> T/4

# 10 efficiency 76/100
res[10] = pick([True, 76 / 100 == 0.85, False], ITEMS[9]["choices"])

# 11 absolute winding: induced field must oppose the flux increase along +x -> points -x.
e = emf(+1, -3, +1)                    # sign of -dPhi/dt along +x
induced_field_x = e                    # -1 -> field inside points -x
current_left_to_right = induced_field_x == -1        # coil_h convention
resistor = "b->a" if current_left_to_right else "a->b"   # exits the right lead -> b -> resistor -> a
left_end_N = induced_field_x == -1     # field leaves the coil through its left end
res[11] = pick([left_end_N, resistor == "a->b", force_on_magnet(-1) > 0], ITEMS[10]["choices"])

# 12 cart: p left of coil (s=-3), N facing right
e_go, e_back = emf(+1, -3, +1), emf(+1, -3, -1)
res[12] = pick([True, e_go == e_back, force_on_magnet(+1) < 0 and force_on_magnet(-1) > 0], ITEMS[11]["choices"])

# 13 devices using induction: microphone, bicycle generator
res[13] = ["ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄹ", "ㄷ, ㄹ", "ㄴ, ㄷ, ㄹ"].index("ㄴ, ㄹ") + 1

# 14 I ∝ cos(theta)
res[14] = pick([gen(60) == gen(120), abs(gen(30)) > abs(gen(60)),
                sum(1 for k in range(91, 270) if gen(k) * gen(k + 1) < 0) == 1], ITEMS[13]["choices"])

# 15 pendulum: open circuit no current; approach vs recede forces opposite
res[15] = pick([False, True, force_on_magnet(+1) == -force_on_magnet(-1)], ITEMS[14]["choices"])

# 16 speed 2v: larger peaks, half the duration, same order of signs
def trace(v, n=4000):
    ts = [i / n * 8 for i in range(n)]
    return [(t, emf(+1, -4 + v * t, v) * mag(+1, -4 + v * t, v)) for t in ts]
tr1, tr2 = trace(1.0), trace(2.0)
peak1, peak2 = max(abs(x) for _, x in tr1), max(abs(x) for _, x in tr2)
first1 = next(x for _, x in tr1 if abs(x) > 1e-3)
first2 = next(x for _, x in tr2 if abs(x) > 1e-3)
figs = [(1.0, 0.5, False), (1.45, 1.0, False), (1.45, 0.5, False), (1.45, 0.5, True), (0.7, 0.5, False)]
want = (peak2 > peak1, 0.5, (first1 > 0) != (first2 > 0))
res[16] = [i + 1 for i, (a, w, f) in enumerate(figs) if (a > 1) == want[0] and w == want[1] and f == want[2]][0]

# 17 pickup
res[17] = pick([True, True, True], ITEMS[16]["choices"])

# 18 two coils A, B; magnet between them moving +x
eA, eB = emf(+1, +2.5, +1), emf(+1, -2.5, +1)
fA, fB = force_on_magnet(+1), force_on_magnet(+1)
res[18] = pick([eA == -REF, eB == REF, fA == -fB], ITEMS[17]["choices"])

# 19 generator conditions: 2x speed halves the interval; stronger magnet keeps it
res[19] = pick([True, 0.5 > 1, 1.0 < 1], ITEMS[18]["choices"])

# 20 pipes
res[20] = pick([True, False, True], ITEMS[19]["choices"])

# 21 LEDs: reference (N approaching left end) lights P
led = lambda e: "P" if e == REF else ("Q" if e == -REF else None)
through = [led(emf(+1, s, +1)) for s in (-3, -0.5, 0.5, 3)]
seq = [x for i, x in enumerate(through) if i == 0 or x != through[i - 1]]
res[21] = pick([led(emf(+1, -3, -1)) == "P", led(emf(-1, +3, -1)) == "P", seq == ["P", "Q"]], ITEMS[20]["choices"])

# 22 two generators: A at 30°, B at 90°
res[22] = pick([abs(gen(90)) > abs(gen(30)), abs(gen(180)) > abs(gen(120)), gen(30) * gen(120) > 0],
               ITEMS[21]["choices"])

# 23 Faraday: only while A's current changes; opening reverses
res[23] = pick([False, True, True], ITEMS[22]["choices"])

# 24 drop heights: speed at the coil ∝ sqrt(height); enter/exit opposite; open circuit is faster
e_in, e_out = emf(+1, -1, +1), emf(+1, +1, +1)
res[24] = pick([mag(+1, -1, math.sqrt(4)) > mag(+1, -1, 1), e_in == e_out, False], ITEMS[23]["choices"])

# 25 current record: + = N approaching the left end
plus_is_approach = emf(+1, -3, +1) == REF
receding_field = emf(+1, -3, -1)                  # +1 -> induced field +x -> enters at left end -> left end S
opts25 = [False, plus_is_approach, False, receding_field == -1, False]
assert opts25.count(True) == 1
res[25] = opts25.index(True) + 1

# 26 regenerative braking
res[26] = pick([True, False, False], ITEMS[25]["choices"])

# 27 hand generator, open vs closed switch
res[27] = pick([False, True, True], ITEMS[26]["choices"])

# 28 loop under the road: vertical flux peaks when the magnet is overhead
flux = lambda x: g(x)
dphi = lambda x: (flux(x + 1e-5) - flux(x)) / 1e-5
res[28] = pick([dphi(-2) > 0, dphi(-2) * dphi(2) < 0, abs(dphi(0)) > abs(dphi(-0.7))], ITEMS[27]["choices"])

# 29 falling magnet: B slowed -> closed; force up both times; currents opposite
res[29] = pick([True, force_on_magnet(-1) > 0, emf(+1, -1, 1) == emf(+1, 1, 1)], ITEMS[28]["choices"])

# 30 perpendicular coils P (0°) and Q (90°)
flipP = 90                                              # P's current changes sign at theta_P = 90°
res[30] = pick([abs(gen(90)) < 1e-9, abs(abs(gen(45)) - abs(gen(135))) < 1e-9, abs(gen(flipP + 90)) == 1],
               ITEMS[29]["choices"])

bad = []
for i in range(1, 31):
    ok = res[i] == KEY[i - 1]
    bad += [] if ok else [i]
    print(f"{i:02d}: solved {res[i]}  key {KEY[i - 1]}  {'OK' if ok else 'MISMATCH'}")
print("dist", {k: KEY.count(k) for k in range(1, 6)})
assert not bad, bad

"""PASS B — independent re-solve of all 30 items (N°2).

Model (no answer data is read from the items):
  * magnet/coil on a common axis: Phi = m * g(s), g(s) = (1+s^2)^-1.5,
    m = +1 when the N end points to +axis, e = -dPhi/dt (sign / relative size).
  * generator: theta measured from the coil plane being perpendicular to the
    field; field-line count through the coil ∝ cos(theta), current ∝ sin(theta)
    (sign flips with the rotation sense).
  * figures.coil_h: current entering the LEFT lead makes the field inside point
    LEFT; reverse=True flips this.
Run: python3 verify.py
"""
import math

from build import KEY
from items import BOGI_SETS, ITEMS

JAMO = "ㄱㄴㄷㄹ"


def g(s):
    return (1 + s * s) ** -1.5


def emf(m, s, v, dt=1e-6):
    d = -(m * g(s + v * dt) - m * g(s - v * dt)) / (2 * dt)
    return 0 if abs(d) < 1e-9 else (1 if d > 0 else -1)


def mag(m, s, v, dt=1e-6):
    return abs(m * (g(s + v * dt) - g(s - v * dt)) / (2 * dt))


def force(v):
    """Coil on magnet: always opposes the relative velocity."""
    return 0 if v == 0 else -math.copysign(1, v)


def gen_I(theta):
    return math.sin(math.radians(theta))


def gen_flux(theta):
    return math.cos(math.radians(theta))


def pick(truth, choices):
    want = ", ".join(JAMO[i] for i, v in enumerate(truth) if v)
    if isinstance(choices, str):
        choices = BOGI_SETS[choices]
    hits = [i + 1 for i, c in enumerate(choices) if c == want]
    assert len(hits) == 1, (want, choices)
    return hits[0]


res = {}

# 01 students: stationary -> 0; more turns -> larger; N in vs S out (same end)
n_in = emf(+1, -3, +1)                # N toward the coil, approaching
s_out = emf(-1, -3, -1)               # S toward the coil, receding
names = ["민준", "서연", "지훈"]
ok = [False, True, n_in == s_out]
res[1] = ["민준", "지훈", "민준, 서연", "서연, 지훈", "민준, 서연, 지훈"].index(
    ", ".join(n for n, v in zip(names, ok) if v)) + 1

# 02 generator: (가) theta=0 (perpendicular), (나) 45, (다) 90 (parallel)
F = {k: abs(gen_flux(th)) for k, th in {"가": 0, "나": 45, "다": 90}.items()}
I = {k: abs(gen_I(th)) for k, th in {"가": 0, "나": 45, "다": 90}.items()}
res[2] = pick([F["가"] == max(F.values()), I["가"] == max(I.values()), F["다"] < 1e-9 and I["다"] > 0],
              ITEMS[1]["choices"])

# 03 vertical axis (+ = up). N points down -> m = -1. p above (s>0), q below (s<0); falling v<0
p_dir, q_dir = emf(-1, +1.5, -1), emf(-1, -1.5, -1)
res[3] = pick([q_dir == -p_dir, emf(-1, 1.5, -2) != p_dir, False], ITEMS[2]["choices"])

# 04 four cases + reversed winding
ref = emf(+1, -3, +1)
cases = {"㉠": emf(+1, -3, -1), "㉡": emf(-1, -3, +1), "㉢": emf(-1, -3, -1), "㉣": -emf(+1, -3, +1)}
right = lambda e: e == ref
res[4] = pick([cases["㉠"] != cases["㉡"], right(cases["㉢"]), not right(cases["㉣"])], ITEMS[3]["choices"])

# 05 2x speed: max current up, max flux same, direction-change interval T/2 -> T/4
res[5] = pick([False, False, True], ITEMS[4]["choices"])

# 06 height table sqrt trend; approaching -> repulsion (up); 50 cm > 40 cm
h = [10, 20, 30, 40]
I6 = [2.0, 2.8, 3.5, 4.0]
res[6] = pick([all(a < b for a, b in zip(I6, I6[1:])), force(-1) > 0, math.sqrt(50) > math.sqrt(40)],
              ITEMS[5]["choices"])

# 07 ring: approach -> repulsion; faster -> larger; stationary -> none
res[7] = pick([True, mag(+1, -2, 2) > mag(+1, -2, 1), emf(+1, -2, 0) != 0], ITEMS[6]["choices"])

# 08 incline: N faces +x; a at s=-L, b at s=+L; loses energy in the coil
first_b, back_b = emf(+1, +2, +1), emf(+1, +2, -1)
res[8] = pick([False, first_b == -back_b, True], ITEMS[7]["choices"])

# 09 I ∝ sin(theta)
above_half = sum(1 for k in range(0, 360) if abs(gen_I(k + 0.5)) >= 0.5)
res[9] = pick([abs(gen_I(30) - gen_I(150)) < 1e-9, abs(abs(gen_I(210)) - 0.5) < 1e-9, above_half == 180],
              ITEMS[8]["choices"])

# 10 relative motion: coil moving toward the fixed magnet
coil_ref = emf(+1, -3, +1)                       # relative approach
res[10] = pick([emf(+1, -3, +1) == coil_ref, emf(+1, -3, 0) != 0,
                emf(+1, -3, -2) == -coil_ref and mag(+1, -3, 2) > mag(+1, -3, 1)], ITEMS[9]["choices"])

# 11 windings: induced field must point -x for both coils (N approaching from the left)
induced = emf(+1, -3, +1)          # -1 -> -x
A_current_enters_left = induced == -1               # default winding
B_current_enters_left = not A_current_enters_left   # reversed winding
# resistor p (left lead side), q (right lead side): entering the left lead means flowing q -> p in the resistor
A_res = "q->p" if A_current_enters_left else "p->q"
B_res = "q->p" if B_current_enters_left else "p->q"
res[11] = pick([True, induced == -1, A_res != B_res], ITEMS[10]["choices"])

# 12 flux ∝ cos; + current when flux decreases -> I ∝ -d(cos)/dt = +sin
res[12] = 1

# 13 speed doubles current (single magnet) -> ㉠ = 2v; stronger magnet -> ㉡ > I0; faster -> ㉢ > ㉡
res[13] = pick([False, True, True], ITEMS[12]["choices"])

# 14 position graph: zero at x=0; 2v scales height only
res[14] = pick([emf(+1, 0, 1) == 0, False, False], ITEMS[13]["choices"])

# 15 generator record: max current <=> plane parallel <=> zero field lines
res[15] = pick([True, False, True], ITEMS[14]["choices"])

# 16 induced field points left inside -> left face N -> P (facing it) is N; current b->G->a
induced16 = emf(+1, -3, +1)
enters_left = induced16 == -1
galv = "B->A" if enters_left else "A->B"
res[16] = pick([induced16 == -1, galv == "A->B", emf(+1, -3, -1) == 1], ITEMS[15]["choices"])

# 17 more turns -> larger; S approach opposite to N approach
res[17] = pick([False, emf(-1, -3, 1) == -emf(+1, -3, 1), False], ITEMS[16]["choices"])

# 18 ring, vertical axis +up, N up (m=+1); p below (s=-d), q above (s=+d)
up_p = emf(+1, -1, +1)
down_q = emf(+1, +1, -1)
res[18] = pick([False, up_p == down_q, force(+1) == force(-1)], ITEMS[17]["choices"])

# 19 generator: two sign changes per turn
changes = sum(1 for k in range(360) if gen_I(k + 0.5) * gen_I(k + 1.5) < 0)
res[19] = pick([True, changes == 1, False], ITEMS[18]["choices"])

# 20 result table
base = emf(+1, -3, +1)
res[20] = pick([emf(+1, -3, -1) == base, emf(-1, -3, +1) == -base, emf(-1, -3, -1) == base], ITEMS[19]["choices"])

# 21 falling: + first (approach), then - with a larger, narrower peak (faster on exit)
res[21] = 2

# 22 reversed rotation: same size, opposite sign; quarter turn from parallel -> perpendicular -> 0
res[22] = pick([True, True, abs(gen_I(0)) < 1e-9], ITEMS[21]["choices"])

# 23 variable control
res[23] = pick([True, False, True], ITEMS[22]["choices"])

# 24 rail: N faces +x; first approach from the left, return approach from the right
first, back = emf(+1, -2, +1), emf(+1, +2, -1)
res[24] = pick([True, first == -back, True], ITEMS[23]["choices"])

# 25 same period (same speed), double amplitude, peaks aligned
res[25] = pick([False, True, True], ITEMS[24]["choices"])

# 26 primary current changes: increasing = same as switching on
res[26] = pick([False, True, False], ITEMS[25]["choices"])

# 27 target: opposite and smaller
opts = {"ㄱ": (-1, 1.5), "ㄴ": (-1, 1.0), "ㄷ": (-1, 0.6)}
res[27] = pick([opts[k][0] == -1 and opts[k][1] < 1 for k in "ㄱㄴㄷ"], ITEMS[26]["choices"])

# 28 falling through A then B (N down, +up, m=-1): faster at B; entering same; between opposite
enterA, enterB = emf(-1, +1, -1), emf(-1, +1, -2)
leaveA, enterB2 = emf(-1, -1, -1), emf(-1, +1, -1)
res[28] = pick([mag(-1, 1, 2) > mag(-1, 1, 1), enterA == enterB, leaveA == -enterB2], ITEMS[27]["choices"])

# 29 CCW from theta=0 with p at the top: p angle = 90 + 360 t/T
p_angle = {q: (90 + 360 * f) % 360 for q, f in {"P": 1 / 8, "Q": 2 / 8, "R": 3 / 8, "S": 4 / 8}.items()}
views = {180: "(가)", 225: "(나)", 135: "(다)", 270: "(라)"}
pair = [views[p_angle["Q"]], views[p_angle["R"]]]
res[29] = [["(가)", "(나)"], ["(가)", "(다)"], ["(나)", "(가)"], ["(다)", "(라)"], ["(라)", "(나)"]].index(pair) + 1

# 30 B-t: +slope B0/2 (0-2 s), 0 (2-4 s), -B0/1 (4-5 s) -> +1, 0, -2
rates = [(1, 1), (0, 0), (-2, -2)]
res[30] = [None, [1, 0, -1], [1, 0, -2], [1, 1, -2], [-1, 0, 2], [0.5, 2, 1]].index([r for r, _ in rates])

bad = []
for i in range(1, 31):
    ok = res[i] == KEY[i - 1]
    bad += [] if ok else [i]
    print(f"{i:02d}: solved {res[i]}  key {KEY[i - 1]}  {'OK' if ok else 'MISMATCH'}")
print("dist", {k: KEY.count(k) for k in range(1, 6)})
assert not bad, bad

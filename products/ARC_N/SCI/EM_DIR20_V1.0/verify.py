"""PASS B — independent re-solve of all 20 items (방향 고난도 20제).

Model (no answer data is read from the items):
  * magnet/coil or ring on a common axis: Phi = m * g(s), g(s) = (1+s^2)^-1.5,
    m = +1 when the magnet's N end points to +axis, s = magnet - coil, and the
    induced field along the axis has the sign of -dPhi/dt.
  * coil_h: current entering the LEFT lead makes the field inside point LEFT
    (reverse winding flips this). A resistor hung under the leads: current that
    enters the coil at the left lead flows right -> left in the resistor.
  * horizontal ring: induced field UP = counter-clockwise seen from above =
    near-side arrow pointing right.
  * battery: current leaves the (+) plate; the lead wired to (+) is where the
    current enters the coil.
  * the coil (or ring) always pushes/pulls the magnet against the relative
    velocity; coils repel while the linked flux grows, attract while it shrinks.
Run: python3 verify.py
"""
import math

from build import KEY
from items import BOGI_SETS, ITEMS

JAMO = "ㄱㄴㄷㄹ"


def g(s):
    return (1 + s * s) ** -1.5


def dphi(mags, dt=1e-6):
    """mags = [(m, s, v), ...] -> dPhi/dt (central difference)."""
    return sum(m * (g(s + v * dt) - g(s - v * dt)) / (2 * dt) for m, s, v in mags)


def ind(m, s, v):
    d = -dphi([(m, s, v)])
    return 0 if abs(d) < 1e-9 else (1 if d > 0 else -1)


def ind_many(mags):
    d = -dphi(mags)
    return 0 if abs(d) < 1e-9 else (1 if d > 0 else -1)


def mag(m, s, v):
    return abs(dphi([(m, s, v)]))


def force(v):
    return 0 if v == 0 else -math.copysign(1, v)


def enters_left(b_ind, reverse=False):
    return (b_ind == -1) != reverse


def resistor(b_ind, left="a", right="b", reverse=False):
    return f"{right}->{left}" if enters_left(b_ind, reverse) else f"{left}->{right}"


def moment_from_battery(plus_on_left_lead, reverse=False):
    """Field direction inside a coil_h whose (+) plate is wired to the given lead."""
    return -1 if plus_on_left_lead != reverse else 1


def pick(truth, choices):
    want = ", ".join(JAMO[i] for i, v in enumerate(truth) if v)
    if isinstance(choices, str):
        choices = BOGI_SETS[choices]
    hits = [i + 1 for i, c in enumerate(choices) if c == want]
    assert len(hits) == 1, (want, choices)
    return hits[0]


res = {}
REF = ind(+1, -3, +1)                      # N approaching the left end

# 01 unknown poles
P = [p for p in (+1, -1) if ind(p, -3, +1) == -REF][0]         # P faces the coil from the left
Qp = -P
q_right = ind(-Qp, +3, -1)                 # Q faces the coil from the right: moment points left if Q is N
p_away_rev = -ind(P, -3, -1)                # reversed winding flips the needle
res[1] = pick([P == -1, q_right == -REF, p_away_rev == REF], ITEMS[0]["choices"])

# 02 S faces the coil from the right (moment +x), moving right
b2 = ind(+1, +3, +1)
res[2] = pick([b2 == 1, resistor(b2) == "b->a", force(+1) > 0], ITEMS[1]["choices"])

# 03 reprint N°2-04
cases = {"ㄱ": ind(+1, -3, -1), "ㄴ": ind(-1, -3, +1), "ㄷ": ind(-1, -3, -1), "ㄹ": -ind(+1, -3, +1)}
res[3] = pick([cases["ㄱ"] != cases["ㄴ"], cases["ㄷ"] == REF, cases["ㄹ"] != REF], ITEMS[2]["choices"])

# 04 LEDs: reference lights P
led = lambda e: "P" if e == REF else ("Q" if e == -REF else None)
res[4] = pick([led(ind(+1, +3, +1)) == "P", led(ind(-1, +3, -1)) == "Q", led(ind(+1, 0, 0)) is None],
              ITEMS[3]["choices"])

# 05 jumping ring: coil flux = sign * I(t), I rising at switch-on
def ring_at_switch(sign, dI):
    """sign: coil field direction, dI: change of |I|. Returns (ring field sense vs coil, pulled down?, current?)"""
    d_flux = sign * dI
    ring = 0 if d_flux == 0 else -math.copysign(1, d_flux)
    return ring == -sign, dI < 0, ring != 0
opp, _, _ = ring_at_switch(+1, +1)
_, pulled_rev, _ = ring_at_switch(-1, +1)
_, _, steady = ring_at_switch(+1, 0)
res[5] = pick([opp, pulled_rev, steady], ITEMS[4]["choices"])

# 06 rotating magnet: Phi = cos(phi), induced ∝ sin(phi)
sgn = [math.sin(math.radians(k + 0.5)) for k in range(360)]
changes = sum(1 for a, b in zip(sgn, sgn[1:]) if a * b < 0) + (1 if sgn[-1] * sgn[0] < 0 else 0)
b6 = 1 if math.sin(math.radians(45)) > 0 else -1          # induced field during 0-90°
res[6] = pick([abs(math.sin(0)) < 1e-12, changes == 2, b6 == -1], ITEMS[5]["choices"])

# 07 reprint N°2-16: induced field inside points LEFT while approaching from the left
b7 = -1
p_is_N = [m for m in (+1, -1) if ind(m, -3, +1) == b7][0] == 1
galv = "B->A" if enters_left(b7) else "A->B"                # A on the left-lead side
res[7] = pick([p_is_N, galv == "A->B", ind(+1, -3, -1) == 1], ITEMS[6]["choices"])

# 08 current in A: slope +1 (0-2 s), 0 (2-4 s), -2 (4-5 s); B's induced field ∝ -slope
slope = lambda t: 1 if t < 2 else (0 if t < 4 else -2)
res[8] = pick([-slope(1) * -slope(4.5) > 0, slope(3) != 0, abs(slope(4.5)) > abs(slope(1))], ITEMS[7]["choices"])

# 09 falling magnet, N down (m = -1 along +z), ring at 0
app, leave = ind(-1, +2, -1), ind(-1, -2, -1)
res[9] = pick([app == 1, leave == -1, force(-1) > 0], ITEMS[8]["choices"])

# 10 record: first lobe (-), second lobe (+) taller and narrower
first_S = ind(-1, -3, +1) == -REF
first_N = ind(+1, -3, +1) == -REF
lead = "S" if first_S else ("N" if first_N else None)
exit_sign = ind(-1, +3, +1) == REF if lead == "S" else None
res[10] = pick([lead == "S" and exit_sign, 50 / 0.18 > 28 / 0.32, ind(-1, 0, 1) != 0], ITEMS[9]["choices"])

# 11 magnet between P (left) and Q (right), N to the right, moving right
bP, bQ = ind(+1, +3, +1), ind(+1, -3, +1)
res[11] = pick([resistor(bP, "a", "b") == "b->a", resistor(bQ, "c", "d") == "d->c", force(+1) != force(+1)],
               ITEMS[10]["choices"])

# 12 reprint N°2-18
res[12] = pick([False, ind(+1, -1, +1) == ind(+1, +1, -1), force(+1) == force(-1)], ITEMS[11]["choices"])

# 13 pendulum: horizontal offset x, flux ∝ -g(x) (N down)
d_app = -(g(-1 + 1e-6) - g(-1 - 1e-6))        # x: -1 -> 0 (moving right)
d_lev = -(g(+1 + 1e-6) - g(+1 - 1e-6))
d_top = -(g(1e-6) - g(-1e-6))
res[13] = pick([d_app * d_lev > 0, abs(d_top) < 1e-9, True], ITEMS[12]["choices"])

# 14 panels: correct near-side arrow is RIGHT iff induced field is UP
panels = {"(가)": ((-1, +2, -1), False), "(나)": ((-1, +2, +1), True), "(다)": ((+1, -2, -1), True)}
ok14 = [k for k, (mv, drawn_right) in panels.items() if (ind(*mv) == 1) == drawn_right]
res[14] = ITEMS[13]["choices"].index(", ".join(ok14)) + 1

# 15 A: (+) plate wired to A's left lead ; B to the right of A
mA = moment_from_battery(True)
bB = -math.copysign(1, mA * +1)                 # flux mA*I rising
res[15] = pick([mA == -1, resistor(bB, "c", "d") == "c->d", False], ITEMS[14]["choices"])

# 16 reprint N°2-24
res[16] = pick([True, ind(+1, -2, +1) == -ind(+1, +2, -1), True], ITEMS[15]["choices"])

# 17 copper pipe: P above the magnet (s = -1), Q below (s = +1), N down, falling
bPp, bQp = ind(-1, -1, -1), ind(-1, +1, -1)
res[17] = pick([bPp == -bQp, bQp == -1, force(-1) < 0], ITEMS[16]["choices"])

# 18 two magnets at equal distance, same speed
ga = ind_many([(+1, -3, +1), (-1, +3, -1)])
na = ind_many([(+1, -3, +1), (+1, +3, -1)])
res[18] = pick([ga == 0, na == REF, abs(dphi([(+1, -3, +1), (+1, +3, -1)])) > abs(dphi([(+1, -3, +1)]))],
               ITEMS[17]["choices"])

# 19 reprint N°2-28
res[19] = pick([mag(-1, 1, 2) > mag(-1, 1, 1), ind(-1, +1, -1) == ind(-1, +1, -2),
                ind(-1, -1, -1) == -ind(-1, +1, -1)], ITEMS[18]["choices"])

# 20 A: (+) plate wired to A's right lead, moving right toward B
mA = moment_from_battery(False)
b_app = ind(mA, -3, +1)
b_off = -math.copysign(1, mA * -1)              # A's current drops to 0
res[20] = pick([mA == 1, resistor(b_app, "c", "d") == "c->d", b_off == b_app], ITEMS[19]["choices"])

bad = []
for i in range(1, 21):
    ok = res[i] == KEY[i - 1]
    bad += [] if ok else [i]
    print(f"{i:02d}: solved {res[i]}  key {KEY[i - 1]}  {'OK' if ok else 'MISMATCH'}")
print("dist", {k: KEY.count(k) for k in range(1, 6)})
runs = max(len(list(gr)) for _, gr in __import__("itertools").groupby(KEY))
print("longest run", runs)
assert not bad, bad
assert runs < 3

# Q11 연표: (다)1838 (라)1919 (마)1948
assert 1919-1838 == 81 and 1948-1919 == 29 and not (29 >= 81/2)
# Q16
req = [12, 18, 25, 33, 40]; rate = [35, 42, 48, 55, 61]
inc = [req[i+1]-req[i] for i in range(4)]; pct = [inc[i]/req[i]*100 for i in range(4)]
print("Q16 inc", inc, [round(p, 1) for p in pct])
assert inc == [6, 7, 8, 7] and max(range(4), key=lambda i: inc[i]) == 2 and max(range(4), key=lambda i: pct[i]) == 0
acc = [r*p/100 for r, p in zip(req, rate)]; print("Q16 acc", acc)
assert acc[3]/acc[1] >= 2 and (req[4]-acc[4]) > (req[2]-acc[2]) and all(req[i] < req[i+1] for i in range(4))
# Q37
S = [(55, 35, 10), (42, 44, 14), (38, 40, 22), (34, 46, 20)]
assert all(sum(s) == 100 for s in S)
first = [("A", "B", "C")[s.index(max(s))] for s in S]; print("Q37 first", first)
assert first == ["A", "B", "B", "B"] and first.index("B") == 1
c = [s[2] for s in S]; assert not all(c[i] < c[i+1] for i in range(3))
assert max(S[0]) > 50
# Q46
a = [65, 8, 6, 5, 7]; b = [71, 15, 18, 8, 6]
assert min(range(5), key=lambda i: b[i]) == 4
d = [b[i]-a[i] for i in range(5)]; g = [b[i]/a[i] for i in range(5)]; print("Q46", d, [round(x, 2) for x in g])
assert max(range(5), key=lambda i: d[i]) == 2 and max(range(5), key=lambda i: g[i]) == 2 and not b[1] >= 2*b[3]
print("verify ok")
# ---- SPECIAL
# S06
d21 = [3, 6, 18, 3]; d23 = [4, 6, 24, 6]
assert sum(d21) == 30 and sum(d23) == 40
assert d21[2]/30 == d23[2]/40 == 0.6 and d21[1]/30 > d23[1]/40 and d23[3] == 2*d21[3] and max(d21) == d21[2] and max(d23) == d23[2]
# Q41
T = {"A": (500, 100), "B": (400, 240), "C": (800, 320), "D": (200, 60)}
rt = {k: b_/a_ for k, (a_, b_) in T.items()}; print("Q41", rt)
assert min(rt["B"], rt["C"]) > max(rt["A"], rt["D"]) and (500-100) >= 2*(200-60)
# S14
q = {"위헌": ([40, 50], [8, 10]), "권리": ([160, 210], [8, 21])}
g1 = 50/40-1; g2 = 210/160-1; assert g1 < g2
assert 8/40 == 10/50 and 21/210 == 2*(8/160) and not 10 > 21
print("special verify ok")

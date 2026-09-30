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
# S11
A_ = [4, 3, 3]; B_ = [1, 6, 1]; C_ = [3, 2, 4]
rg = lambda v: max(v)-min(v)
assert rg(A_) < rg(C_) < rg(B_) and sum(A_) == 10 and sum(B_) == 8 and sum(C_) == 9 and max(map(sum, (A_, B_, C_))) == sum(A_)
# S14
hx = [9, 12, 7, 15]; cf = [2, 5, 0, 3]
r = [c/h for c, h in zip(cf, hx)]; print("S14", [round(x, 3) for x in r])
assert r[1] > r[0] and cf.index(max(cf)) != hx.index(max(hx))
assert sum(hx) == 43 and sum(cf) == 10 and (43-10)/43 >= 0.7
print("special verify ok")

import sys; sys.path.insert(0, ".")
import popdata as PD
# Q02
assert [42-35, 51-42, 56-51] == [7, 9, 5]
# Q05
assert 132-100 == 32 and (21-12, 31-21) == (9, 10)
# Q08
d = {"가": [330, 280, 300, 270, 240, 260], "나": [300, 240, 260, 310, 290, 250], "다": [250, 210, 230, 300, 320, 280]}
t = {k: sum(v) for k, v in d.items()}; print("Q08", t)
assert t["가"] > t["나"] > t["다"] and d["가"][0] == max(v[0] for v in d.values()) and d["나"][3] > d["다"][3]
assert d["다"][4] == max(v[4] for v in d.values()) and not all(v[1] > v[2] for v in d.values()) and not d["나"][5] > d["가"][0]
# Q13
P = [100, 102, 108, 118, 125, 128]; inc = [P[i+1]-P[i] for i in range(5)]; print("Q13 inc", inc)
assert inc == [2, 6, 10, 7, 3] and not (inc[3] > inc[2] and inc[4] > inc[3])
# Q16
assert 45000-30000 == 15000 and 3400-2000 == 1400
assert (45000-30000 > 0) and 41600 == 45000-3400 and 28000 == 30000-2000 and 41600 > 28000
assert 3400/2000 > 45000/30000 and 45000/3400 < 30000/2000
# Q19
assert sum([10, 35, 45, 10]) == 100 and sum([30, 15, 40, 15]) == 100 and 10+35 == 45
# Q21
assert 35-48 == -13 and 44-30 == 14
# Q23
v = [0.3, 3.5, 5.7, 27, 41, 20.5, 2.0]; assert abs(sum(v)-100) < 1e-9
assert sum(v[3:]) >= 90 and v[4] >= 40 and sum(v[:3]) < v[3]
# Q24
pc = [59.4, 17.5, 9.5, 8.3, 4.8, 0.5]; assert abs(sum(pc)-100) < 1e-9
assert pc[0]/pc[1] >= 3 and pc[2]/pc[4] < 2 and abs(8000*pc[1]/100-1400) < 1 and 8000*pc[3]/100 < 10000
# Q26
for k, e in {"A": (44, 53, 3), "B": (27, 65, 8), "C": (15, 66, 19), "D": (10, 58, 32)}.items():
    assert PD.groups(k) == e, k
# Q29
tb = {"A": (40, 38), "B": (41, 18), "C": (22, 9), "D": (11, 10), "E": (7, 11)}; g = {k: a-b for k, (a, b) in tb.items()}; print("Q29", g)
assert max(g, key=g.get) == "B" and g["D"] > 0
# Q32
assert 5063/1787 >= 2 and 654+568+566+545 == 2333 and 357/654 > 0.5
# Q37
for a, b, c in [(34, 62, 4), (21, 72, 7), (13, 71, 16)]: assert a+b+c == 100
assert 16/13*100 > 100 and 7/21 > 4/34
# Q40
P_ = (120, 700, 180); Q_ = (280, 660, 60)
tp = P_[0]/P_[1]+P_[2]/P_[1]; tq = Q_[0]/Q_[1]+Q_[2]/Q_[1]; print("Q40", tp*100, tq*100)
assert tq > tp and P_[2]/P_[1] > Q_[2]/Q_[1] and P_[2]/P_[0]*100 >= 100 and Q_[2]/sum(Q_) < P_[2]/sum(P_)
# Q42
for (a, b, n) in [(50, 62, 9), (40, 44, 10), (30, 31, -2), (20, 27, 6)]: print("Q42", b-a-n)
# Q43
c = PD.groups("C"); d_ = PD.groups("D")
yc, nc = c[0]/c[1]*100, c[2]/c[1]*100; yd, nd = d_[0]/d_[1]*100, d_[2]/d_[1]*100; print("Q43", yc, nc, yc+nc, yd, nd, yd+nd)
assert 1.8 < nd/nc < 2.1 and yd < yc and yd+nd > yc+nc and (yc-yd) < (nd-nc)
# Q44
assert 140/50 == 2.8 and 140e8/90e4 > 50e8/40e4 and 2000-1950 == 90-40
# Q45
a = [18, 25, 35, 46, 51]; b = [52, 62, 71, 77, 80]
assert 51/18 > 2.7 and b[-1] > a[-1] and (51-18) >= 25 and (80-52) >= 25 and a[-1] < b[0]
# Q48
assert 38-12 == 26 and 9 < 11 and abs(3/44*100-6.8) < 0.1 and 32/10*100 == 320
print("ALL OK")

# ---- special ----
g = PD.groups
def dep(k): 
    y, c, n = g(k); return y/c*100, n/c*100, (y+n)/c*100, n/y*100
B_, C_, D_, A_ = dep("B"), dep("C"), dep("D"), dep("A")
print("S02", B_, C_)
assert B_[2] > C_[2] and C_[1]/B_[1] >= 2 and not (C_[3]/B_[3] >= 5) and not (B_[0] < C_[0])
assert 38-14 == 24 and 20-7 == 13 and 10-9 == 1 and A_[2] > C_[2]
tb = [(40, 37), (39, 20), (25, 10), (13, 9), (9, 11)]; ni = [a-b for a, b in tb]; print("S04", ni)
assert ni.index(max(ni)) == 1 and ni[2]-ni[3] == 11 and (40-39) < (37-20) and ni[3] > 0
tp = [(15, 66, 19), (10, 58, 32), (8, 50, 42)]
tot = [(y+n)/c*100 for y, c, n in tp]; print("S07", tot, [n/c for y, c, n in tp], [n/y*100 for y, c, n in tp])
assert tot[0] < tot[1] < tot[2] and abs(42/50-0.84) < 1e-9 and (tot[2]-tot[1]) > (tot[1]-tot[0]) and 42/8*100 > 400
P = (210, 600, 90); Q = (120, 640, 240)
vals = {"가": P[0]/P[1]*100, "나": P[2]/P[1]*100, "다": Q[0]/Q[1]*100, "라": Q[2]/Q[1]*100}; print("S08", vals)
assert sorted(vals, key=vals.get, reverse=True) == ["라", "가", "다", "나"]
yo = [6, 5, 4.5, 4, 3.5, 3]; wk = [36, 33, 29, 26, 24, 22]; ol = [8, 12, 15, 17, 19, 20]
tt = [a+b+c for a, b, c in zip(yo, wk, ol)]; print("S09", tt)
assert tt == [50, 50, 48.5, 47, 46.5, 45] and (50-45)/50 == 0.1 and (72-22/45*100) >= 20 and (20/22)/(8/36) >= 4
inc = [ol[i+1]-ol[i] for i in range(5)]; print("S09 inc", inc); assert not all(inc[i+1] > inc[i] for i in range(4))
assert 190-120 == 70 and (36+190+44)-(30+120+30) == 90 and 90-20 == 70 and 70/90 < 0.8 and 70 > (6+14)
assert round(560/440*100, 1) == 127.3 and 255/245 < 560/440 and 255 < 560/2
assert round(121/134, 2) == 0.9
assert 14.0 >= 14 and 10.8 < 14
sc = {"현": (10, 58, 32), "가": (13, 57, 30), "나": (11, 61, 28), "다": (14, 62, 24)}
for k, (y, c, n) in sc.items(): print("S17", k, round(y/c*100, 1), round(n/c*100, 1), round((y+n)/c*100, 1))
assert min(sc, key=lambda k: (sc[k][0]+sc[k][2])/sc[k][1]) == "다"
assert 13/57 > 10/58 and 30/57 < 32/58 and (13+30)/57 > (10+32)/58 and (32/58-28/61)*100 < 10
assert 15 == 90/600*100 and 150/600*100 == 25 and 15+25 == 40
assert (A_[0]/D_[0] >= 4) and not (D_[1]/A_[1] >= 10) and (D_[3]/A_[3] >= 40) and A_[2] > D_[2]
assert 18.75 < 35 and 8.75 < 37.5 < 118.75
print("SPECIAL OK")

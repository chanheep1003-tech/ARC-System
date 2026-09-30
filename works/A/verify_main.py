"""수치·논리 검증 (PASS B용 독립 계산)."""
import sys; sys.path.insert(0, ".")
import numpy as np
from figs_main import a34_data

# Q05
assert 500*6/10==300 and 500*3/10==150 and 500*1/10==50 and 300/50==6
# Q08
tot={"가":60+50-30,"나":30+30+0,"다":70+55-50}; print("Q08",tot); assert tot["가"]>tot["다"]>tot["나"]
# Q12/13
perf=[50,30,20]; pot=[20,40,40]; need=[100,250,150]
X=[1000*v/sum(perf) for v in perf]; Y=[1000*v/sum(pot) for v in pot]; Z=[1000*v/sum(need) for v in need]
print("X",X,"Y",Y,"Z",Z); assert X==[500,300,200] and Y==[200,400,400] and Z==[200,500,300]
W=[400*n/sum(need)+600*p/sum(perf) for n,p in zip(need,perf)]; print("W",W); assert W==[380,380,240]
assert Z[1]==max(Z+X+Y) or Z[1]==500  # B largest need gets most in Z
assert Z[1]>=max(X[1],Y[1])
# Q12 ㄷ: 부족액 최대(B)가 가장 적은 금액? -> B in Z=500 is the largest => 거짓
assert not (Z[1]<min(X[1],Y[1]))
# Q13 options
assert not (W[0]>X[0]); assert W[0]==W[1]; assert not (W[2]>Y[2]); assert not (W[1]>Z[1])
# Q25
A=[5,5,1,3];B=[2,3,2,5];C=[3,1,5,2]; print("Q25 sums",sum(A),sum(B),sum(C)); assert sum(A)>sum(B)>sum(C)
# Q27
assert abs((8.7-5.2)-3.5)<1e-9 and abs((8.8-7.4)-1.4)<1e-9
# Q28
g=((92+70)/2-(55+15)/2, (95+50)/2-(70+18)/2); print("Q28 belief effect",g); assert g[0]>g[1]
# Q29
print("Q29 means", np.mean([30,35,28,33]), np.mean([63,58,66,61]))
# Q31
assert 72-26==46 and 65-30==35 and 46>35 and 30>26
# Q32
assert abs((7.0-5.0)-2.0)<1e-9 and abs((7.6-3.4)-4.2)<1e-9 and abs((6.3-5.9)-0.4)<1e-9
# Q33
assert 36-34==2 and 47-22==25
# Q34
(pa,na),(pb,nb)=a34_data()
ra=np.corrcoef(pa,na)[0,1]; rb=np.corrcoef(pb,nb)[0,1]; print("Q34 r",ra,rb)
assert ra<-0.6 and abs(rb)<0.35
assert sum((pb>=6.5)&(nb>=6.5))>=2
# Q41
n=[36,33,30]; p=[41,38,35]; s=[32,30,27]
assert n[0]>n[1]>n[2] and p[1]>n[0] and not (p[2]<s[0])
# Q47 boxes overlap
assert 82<=110 and 91<=102  # T1 IQR overlap
# Q48
assert 8.2-6.9<8.4-4.1
print("ALL OK")

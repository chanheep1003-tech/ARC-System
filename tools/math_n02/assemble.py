"""Build item dicts for any MATH2 id: existing clean sets > manual_items > autoitem(DB)."""
import json, glob, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from autoitem import autoitem
from verified_new import V
from manual_items import M
DB = json.load(open(os.environ.get('MATH2_DB', '/tmp/claude-0/-home-user-ARC-System/d52620ed-c5b3-58a9-b74d-3065454054c1/scratchpad/work/items.json')))
UNIT = {'01_명제':'명제','02_함수':'함수','03_유리함수':'유리함수','04_무리함수':'무리함수'}
EXIST = {}
for f in sorted(glob.glob(os.path.join(HERE, 'sets', 'set?.json'))):
    for it in json.load(open(f)): EXIST[it['id']] = it
FIX = {
 'MATH2-03158': [('$bar OA + bar OB$', '$\\overline{\\mathrm{OA}}+\\overline{\\mathrm{OB}}$')],
 'MATH2-02644': [('f^n+1 (x)', 'f^{n+1} (x)')],
 'MATH2-00924': [(' [4.7]', '')],
 'MATH2-03143': [('$U = { x | x$는 $12$의 약수$}$', r'$U=\{x\mid x\text{는 }12\text{의 약수}\}$')],
 'MATH2-02628': [('$X= { 2$, $3$, $4$, $5$, $6 }$', r'$X=\{2,3,4,5,6\}$')],
 'MATH2-00013': [('함수 $f$ 중', '함수 $f$ 중 다음 조건을 만족시키는 함수의 개수는?')],
 'MATH2-03254': [('$X = { 1, 2, 3, 4, 5, 6$', r'$X=\{1,2,3,4,5,6\}$'), ('$f(4) not= 4$', r'$f(4)\ne 4$'), (r'$f(2) \times { f(4) + f(5)$', r'$f(2)\times\{f(4)+f(5)\}$')],
 'MATH2-03284': [('$A={x | x$는 $15$이하의 소수$}$', r'$A=\{x\mid x\text{는 }15\text{ 이하의 소수}\}$'), ('$f : X rarrowY$ ', r'$f:X\to Y$')],
 'MATH2-02914': [('$A= {2, 3, 4, 5, 6$', r'$A=\{2,3,4,5,6\}$'), ('$B= {2, 3, 4, 9, 12, 18, 20$', r'$B=\{2,3,4,9,12,18,20\}$'), (r' 조 건 ㈎ $x_{1} \in A$, $x_{2} \in A$이고 $x_{1}<x_{2}$이면 $f (x_{1} ) \le f (x_{2} )$ ㈏ $f(2) f(5)=36$', ''), ('아래 두 조건', '다음 두 조건')],
 'MATH2-03243': [('$X= { x | x$는 $10$이하의 자연수$}$', r'$X=\{x\mid x\text{는 }10\text{ 이하의 자연수}\}$')],
 'MATH2-03281': [(r'$S= { x | 1 \le x \le 300, x$는 $30$의 배수$$ 의', r'$S=\{x\mid 1\le x\le 300,\ x\text{는 }30\text{의 배수}\}$의')],
 'MATH2-03240': [('$X= { 1, 2, 3, 4, 5, 6, 7, 8$', r'$X=\{1,2,3,4,5,6,7,8\}$')],
 'MATH2-03259': [(r'$f ( 7 ) \times { f ( 4 ) +f ( 6 ) }$', r'$f(7)\times\{f(4)+f(6)\}$')],
 'MATH2-03431': [('점수 $k$', '정수 $k$')],
 'MATH2-03436': [('h ( k+2 )$$=2$', 'h ( k+2 )=2$')],
 'MATH2-02784': [('$r : x$는 $n$의 배수이다. 있다.', '$r : x$는 $n$의 배수이다.')],
 'MATH2-02848': [('값 의', '값의')],
 'MATH2-02538': [('다음 중에서', '다음 중에서 (단, $A$, $B$, $C$는 집합이다.)')],
 'MATH2-02924': [(' ㆍ 모든 실수 $x$에 대하여 $p$이다. ㆍ $p$는 $simq$이기 위한 충분조건이다.', '')],
}
FIXC = {
 'MATH2-03055': ['$-3$', '$-2$', '$-1$', '$1$', '$2$'],
 'MATH2-02538': ['$xy < 0$이면 $x^{2}+y^{2} > 0$이다.', '$x+y=0$이면 $x=0$이고 $y=0$이다.', '$x > 0$이고 $y > 0$이면 $xy= | xy |$이다.', '$x \\le 2$ 또는 $y \\le 2$이면 $x+y \\le 4$이다.', '$A \\subset (B \\cap C )$이면 $A \\subset B$이고 $A \\subset C$이다.'],
}
FIXS2 = {
 'MATH2-02672': r'$f(-2)+f(-1)+f(0)+\cdots+f(4)$의 값을 구하시오.',
 'MATH2-02627': r'가능한 모든 집합 $X$, $Y$에 대하여 $X$에서 $Y$로의 일대일함수의 개수는?',
}
FIXB = {
 'MATH2-02672': ([r'(가) 집합 $X$의 모든 원소 $x$에 대하여 $$\{f(x)-2x^2+4x-4\}$$ $$\times\{f(x)-|10x-7|+3\}=0$$ 이다.', '(나) $f(0)+f(1)+f(2)$는 $4$의 배수이다.'], None),
 'MATH2-02669': (['(가) 함수 $f$의 치역의 원소의 개수는 $5$이다.', r'(나) $f(1)+f(2)+\cdots+f(7)=21$', '(다) $f(a)=f(b)=f(c)$를 만족시키는 집합 $X$의 서로 다른 세 원소 $a$, $b$, $c$가 존재한다.'], None),
 'MATH2-03240': (['(가) 함수 $f$의 치역의 원소의 개수는 $7$이다.', r'(나) $f(1)+f(2)+\cdots+f(8)=40$', '(다) 함수 $f$의 치역의 원소 중 최댓값과 최솟값의 차는 $6$이다.'], None),
 'MATH2-02914': ([r'(가) $A$의 두 원소 $x_1$, $x_2$에 대하여 $x_1<x_2$이면 $f(x_1)\le f(x_2)$이다.', r'(나) $f(2)f(5)=36$'], None),
 'MATH2-00013': (['(가) $f$는 일대일함수이다.', '(나) $f(1)+f(2)+f(3)+f(4)$는 짝수이다.'], None),
 'MATH2-02627': ([r'(가) $X\cup Y=U$, $X\cap Y=\varnothing$', r'(나) $\{1,2\}\subset X\subset\{1,2,3,4\}$'], None),
 'MATH2-02924': (['ㆍ 모든 실수 $x$에 대하여 $p$이다.', 'ㆍ $p$는 $\\sim q$이기 위한 충분조건이다.'], None),
}
def src(i): return re.sub(r'\s*#.*$', '', DB[i]['src']).replace('_', ' ').strip()
def item(i):
    if i in EXIST: return dict(EXIST[i])
    v = DB[i]
    d = M[i] if i in M else autoitem(v)
    it = dict(id=i, D=v['D'], unit=UNIT[v['unit']], src=src(i), ans=V[i], fig=None, boxtitle=d.get('boxtitle'))
    it.update({k: d.get(k) for k in ('stem', 'box', 'stem2', 'box2', 'choices')})
    for k in ('stem', 'stem2'):
        if it[k]:
            t = re.sub(r'\s*\[(\d{4}년[^\]]*|단답형)\]', '', it[k])
            t = re.sub(r'\s*공통수학2 명제 모의고사.*$', '', t)
            for a, b in FIX.get(i, []): t = t.replace(a, b)
            it[k] = t.strip()
    if i in FIXC: it['choices'] = FIXC[i]
    if i in FIXB: it['box'], it['boxtitle'] = FIXB[i]
    if i in FIXS2: it['stem2'] = FIXS2[i]
    if it['box2'] and not it['stem2'] and not it['boxtitle'] and not it['box']:
        it['boxtitle'] = '보기'; it['box'], it['box2'] = it['box2'], None
    return it
def pool(D):
    ids = [i for i, it in EXIST.items() if it['D'] == D] + [i for i in V if DB[i]['D'] == D]
    return list(dict.fromkeys(ids))

# -*- coding: utf-8 -*-
"""ARC 선지 단서(cue) 린트 — 문항 세트가 '읽지 않고도 맞힐 수 있는지' 점검한다.
사용: python3 quality/tools/option_cue_lint.py   (저장소 루트 기준, 아래 대상 목록을 수정해 사용)
지표(기준선 20%): 최장 선지=정답 비율, 지문 어휘 중복 휴리스틱 정확도, 부정 발문에서 과잉 단정어 단서.
권장 게이트: 각 지표 ≤ 30% (긍정 발문의 최장 선지=정답은 ≤ 35%). 초과 시 선지 길이·구조를 평준화해 재출제.
"""
# -*- coding: utf-8 -*-
import sys, re, importlib, collections, statistics as st, itertools
K='/home/user/ARC-System/outputs/KOR/'
def load(dir_, mods, mainmod, sets_attr='SETS'):
    p=K+dir_+'/src'
    for m in list(sys.modules):
        if m in ('common','passages_final','passages_final2','items_final','items_final2','items_a','items_b','items_c','items_n12','passages_n11','passages_n12'): del sys.modules[m]
    sys.path.insert(0,p)
    for m in mods: importlib.import_module(m)
    sets=importlib.import_module(mainmod).SETS
    Q=sys.modules['common'].Q if 'common' in sys.modules else sys.modules[mods[0]].Q
    sys.path.remove(p)
    return Q,sets
def flat(o):
    if isinstance(o,str): yield o
    elif isinstance(o,dict):
        for v in o.values(): yield from flat(v)
    elif isinstance(o,(list,tuple)):
        for v in o: yield from flat(v)
def clean(t): return re.sub(r'\{.\|([^}]*)\}',r'\1',re.sub(r'<[^>]+>','',t))
def grams(t,n=2):
    t=re.sub(r'[^가-힣0-9A-Za-z]','',clean(t)); return collections.Counter(t[i:i+n] for i in range(len(t)-n+1))
ABS=['완전히','반드시','오직','전혀','확정','직접','오히려','모두','항상','절대','만','뿐','결코','무관','일방적','자책','포기','전부','오로지','즉시','곧바로']
def analyze(name,Q,sets):
    res=collections.Counter(); rows=[]
    for i,q in enumerate(Q,1):
        if q.get('fixed') or q.get('table'): continue
        ch=[clean(c) for c in q['choices']]
        if len(ch)!=5 or any(len(c)<6 for c in ch): continue
        neg=bool(re.search('않|아닌|다른|틀린',re.sub('<[^>]+>','',q['stem'])))
        c=q['c']
        st_=[s for s in sets if s['rng'][0]<=i<=s['rng'][1]]
        ctx=" ".join(flat(st_[0]['parts'] if 'parts' in st_[0] else st_[0]))+" "+clean(q.get('box','') or '')+" "+clean(q.get('boxpre','') or '')
        cg=grams(ctx)
        ov=[sum(min(v,cg[k]) for k,v in grams(x).items())/max(1,sum(grams(x).values())) for x in ch]
        ln=[len(x) for x in ch]
        ab=[sum(w in x for w in ABS) for x in ch]
        # H1 overlap
        pick=(min if neg else max)(range(5),key=lambda k:ov[k]); res['overlap']+=(pick==c)
        # H2 longest
        res['longest']+=(max(range(5),key=lambda k:ln[k])==c)
        # H3 abs cue (neg: max abs)
        if neg and max(ab)>0: res['abs_neg_n']+=1; res['abs_neg_hit']+=(ab.index(max(ab))==c and ab.count(max(ab))==1)
        # correct option abs cue presence
        if neg: res['neg_n']+=1; res['neg_correct_has_abs']+=(ab[c]>0)
        res['n']+=1
        # combined heuristic: neg -> low overlap + abs cue
        score=[(-ov[k] if neg else ov[k])+(0.08*ab[k] if neg else -0.08*ab[k]) for k in range(5)]
        res['combo']+=(max(range(5),key=lambda k:score[k])==c)
        rows.append((i,neg,pick==c))
    return res,rows
out={}
for name,d,mods,main in [('FINAL01','ARC_FINAL_공통국어2_N01',['items_final'],'passages_final'),('FINAL02','ARC_FINAL_공통국어2_N02',['items_final2'],'passages_final2'),
                         ('N11','ARC_N11_시험범위11편_110Q',['common','items_a','items_b','items_c'],'passages_n11'),('N12','ARC_N12_보충자료4편_핵심40Q',['common','items_n12'],'passages_n12')]:
    Q,sets=load(d,mods,main)
    if name.startswith('FINAL'):
        Q=sys.modules[mods[0]].Q if mods[0] in sys.modules else Q
    r,rows=analyze(name,Q,sets); out[name]=r
    n=r['n']
    print(f"{name}: 대상 {n}문항 | 어휘중복 휴리스틱 정확도 {r['overlap']/n:.0%} | 최장 선지 {r['longest']/n:.0%} | 결합 {r['combo']/n:.0%} | 부정발문 {r['neg_n']}개 중 정답에 과잉단정어 포함 {r['neg_correct_has_abs']/max(1,r['neg_n']):.0%} | 과잉단정어 단서로 단독 적중 {r['abs_neg_hit']}/{r['abs_neg_n']}")

print('---- 상세 ----')
import statistics as S2
for name,d,mods,main in [('FINAL01','ARC_FINAL_공통국어2_N01',['items_final'],'passages_final'),('N11','ARC_N11_시험범위11편_110Q',['common','items_a','items_b','items_c'],'passages_n11'),('N12','ARC_N12_보충자료4편_핵심40Q',['common','items_n12'],'passages_n12')]:
    Q,sets=load(d,mods,main)
    if name.startswith('FINAL'): Q=sys.modules[mods[0]].Q
    pos=[0,0];neg=[0,0];ratios=[];q_marks=[0,0]
    for i,q in enumerate(Q,1):
        if q.get('fixed') or q.get('table'): continue
        ch=[clean(c) for c in q['choices']]
        if len(ch)!=5 or any(len(c)<6 for c in ch): continue
        isneg=bool(re.search('않|아닌|다른|틀린',re.sub('<[^>]+>','',q['stem'])))
        ln=[len(x) for x in ch]; c=q['c']
        hit=(max(range(5),key=lambda k:ln[k])==c)
        (neg if isneg else pos)[0]+=hit; (neg if isneg else pos)[1]+=1
        others=[ln[k] for k in range(5) if k!=c]
        ratios.append(ln[c]/S2.mean(others))
        # 정답 선지 안 따옴표 인용 비율
        q_marks[0]+=('‘' in ch[c]); q_marks[1]+=sum('‘' in ch[k] for k in range(5) if k!=c)/4
    print(f"{name}: 최장선지=정답 (긍정발문 {pos[0]}/{pos[1]}, 부정발문 {neg[0]}/{neg[1]}) | 정답길이/오답평균 = {S2.mean(ratios):.2f}배 (중앙 {S2.median(ratios):.2f}) | 따옴표 인용 포함: 정답 {q_marks[0]}개 vs 오답 평균 {q_marks[1]:.1f}개")
    # 유형 구성
    kinds=collections.Counter()
    for q in Q:
        if q.get('fixed') and '개' in "".join(q['choices']): kinds['개수형']+=1
        elif q.get('fixed') and q.get('table'): kinds['표정오']+=1
        elif q.get('fixed'): kinds['ㄱ~ㅁ조합']+=1
        elif q.get('table'): kinds['표']+=1
        elif q.get('box'): kinds['보기']+=1
        else: kinds['일반']+=1
    print('  유형:',dict(kinds))

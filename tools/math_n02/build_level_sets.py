"""Build 5 sets of 50 for one difficulty level from the verified pool (repeats across sets allowed)."""
import sys, json, re, difflib, random, collections
sys.path.insert(0, '.')
import assemble as A
D = sys.argv[1]; NSET = 5; SIZE = 50; CAP = int(sys.argv[2]) if len(sys.argv) > 2 else 2
ids = A.pool(D)
items = {i: A.item(i) for i in ids}
norm = {i: re.sub(r'[\s$\d{}\\()^_,.]', '', (items[i]['stem'] or '') + ''.join(items[i]['box'] or []))[:90] for i in ids}
# cluster near-identical templates
cl = {}; reps = []
for i in ids:
    for r in reps:
        if difflib.SequenceMatcher(None, norm[i], norm[r]).ratio() > 0.72:
            cl[i] = cl[r]; break
    else:
        cl[i] = len(reps); reps.append(i)
random.seed(20261124)
order = sorted(ids, key=lambda i: (cl[i], random.random()))
sets = [[] for _ in range(NSET)]; use = collections.Counter()
def ok(s, i, cap): return i not in s and sum(1 for j in s if cl[j] == cl[i]) < cap
# primary: round robin, each item once
k = 0
for i in order:
    for t in range(NSET):
        s = sets[(k + t) % NSET]
        if len(s) < SIZE and ok(s, i, CAP): s.append(i); use[i] += 1; k += 1; break
# fill: least used first
for cap in (CAP, CAP + 1, CAP + 2, 99):
    for s in sets:
        for i in sorted(ids, key=lambda i: (use[i], random.random())):
            if len(s) >= SIZE: break
            if ok(s, i, cap): s.append(i); use[i] += 1
uorder = {'명제': 0, '함수': 1, '유리함수': 2, '무리함수': 3}
out = []
for n, s in enumerate(sets, 1):
    s.sort(key=lambda i: (uorder[items[i]['unit']], i))
    json.dump([items[i] for i in s], open(f'sets/{D.lower()}_set{n}.json', 'w'), ensure_ascii=False, indent=1)
    out.append((n, len(s), collections.Counter(items[i]['unit'] for i in s)))
print('pool', len(ids), 'clusters', len(reps), 'max use', max(use.values()), 'items used once', sum(1 for v in use.values() if v == 1))
for o in out: print(o)

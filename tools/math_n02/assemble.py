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
def src(i): return re.sub(r'\s*#.*$', '', DB[i]['src']).replace('_', ' ').strip()
def item(i):
    if i in EXIST: return dict(EXIST[i])
    v = DB[i]
    d = M[i] if i in M else autoitem(v)
    it = dict(id=i, D=v['D'], unit=UNIT[v['unit']], src=src(i), ans=V[i], fig=None, boxtitle=d.get('boxtitle'))
    it.update({k: d.get(k) for k in ('stem', 'box', 'stem2', 'box2', 'choices')})
    if it['box2'] and not it['stem2'] and not it['boxtitle'] and not it['box']:
        it['boxtitle'] = '보기'; it['box'], it['box2'] = it['box2'], None
    return it
def pool(D):
    ids = [i for i, it in EXIST.items() if it['D'] == D] + [i for i in V if DB[i]['D'] == D]
    return list(dict.fromkeys(ids))

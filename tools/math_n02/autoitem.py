"""Convert MATH2 DB bodies (HWP-equation flavored markdown) into ARC item dicts.

Used only for items whose answers were independently re-verified. KaTeX strict rendering in
build.js is the gate that catches anything this converter leaves malformed.
"""
import re

CIRC = '①②③④⑤'


def _over(t):
    # {a} \over {b} with one level of nested braces
    pat = re.compile(r'\{((?:[^{}]|\{[^{}]*\})*)\}\s*\\?over\s*\{((?:[^{}]|\{[^{}]*\})*)\}')
    while True:
        n = pat.sub(lambda m: r'\frac{' + m.group(1) + '}{' + m.group(2) + '}', t)
        if n == t: return n
        t = n


def fix_math(t):
    t = t.replace('LEQ', r'\le ').replace('GEQ', r'\ge ').replace('&&&', '&').replace('&&', '&')
    def cases(m):
        inner = m.group(1).replace('#', r' \\ ')
        return r'\begin{cases} ' + inner + r' \end{cases}'
    t = re.sub(r'(?<!\\)cases\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}', cases, t)
    if re.search(r'(?<!\\)cases\s*\{', t):          # unbalanced: cases{ ... to end
        t = re.sub(r'(?<!\\)cases\s*\{(.*)$', lambda m: r'\begin{cases} ' + m.group(1).replace('#', r' \\ ') + r' \end{cases}', t)
    t = re.sub(r'\{\s*([a-z])\s+\1\s*(?=[<>]|\\le|\\ge)', r'{\1 | \1', t)
    t = re.sub(r'(?<![\\a-zA-Z])root\s*(\d+)', r'\\sqrt{\1}', t)
    t = _over(t)
    t = t.replace('->', r'\to ').replace('cdots', r'\cdots ').replace(r'\\cdots', r'\cdots')
    t = re.sub(r'\{\s*"([A-Za-z]+)"\s*\}', r'\\mathrm{\1}', t)
    t = re.sub(r'"([A-Z]{1,3})"', r'\\mathrm{\1}', t)
    t = re.sub(r'\{([^{}]*)\}\s*\\over\s*\{([^{}]*)\}', r'\\frac{\1}{\2}', t)
    t = re.sub(r'\bLEQ\b|(?<!\\)\ble\b(?=\s*[\d\-a-z(])', r'\\le ', t)
    t = re.sub(r'(?<!\\)\bge\b(?=\s*[\d\-a-z(])', r'\\ge ', t)
    # set braces written without escape:  = { 1, 2, 3 }  or  { x | ... }
    def setb(m):
        pre = t2[:m.start()].rstrip()
        if re.search(r'(\\sqrt|\\frac|\\[a-z]+|[\^_]|\})$', pre):
            return m.group(0)
        return '\\{' + m.group(1) + '\\}'
    t2 = t
    t = re.sub(r'(?<!\\)\{(\s*[^{}]*?(?:,|\||\\mid)[^{}]*?)\}(?!\s*\{)', setb, t)
    t = re.sub(r'\bGEQ\b', r'\\ge ', t)
    t = t.replace('!=', r'\ne ')
    for a, b in [('SMALLINTER', r'\cap '), ('TRIANGLE', r'\triangle '), ('RIGHT', ''), ('LEFT', ''),
                 ('right\\}', r'\}'), ('rightvert', '|'), ('leftvert', '|'), ('right}', '}'), ('vert', '|')]:
        t = t.replace(a, b)
    t = re.sub(r'(?<![\\a-zA-Z])circ\s*', r'\\circ ', t)
    t = re.sub(r'(?<=\s)in(?=[A-Z])', r'\\in ', t)
    t = re.sub(r'(?<![\\a-zA-Z])le(?=[0-9a-z])', r'\\le ', t)
    t = re.sub(r'(?<![\\a-zA-Z])leq\b', r'\\le ', t)
    t = re.sub(r'(?<![\\a-zA-Z])geq\b', r'\\ge ', t)
    t = re.sub(r'\\to(?=[A-Za-z])', r'\\to ', t)
    t = re.sub(r'\^\s*-1(?![0-9}])', r'^{-1}', t)
    t = re.sub(r'(?<!\\)\broot\s*\{', r'\\sqrt{', t)
    t = re.sub(r'(?<![\\a-zA-Z])overline\s*\{', r'\\overline{', t)
    t = re.sub(r'([가-힣][가-힣 ]*[가-힣]|[가-힣])', lambda m: r'\text{' + m.group(1) + '}', t)
    t = re.sub(r'\s+', ' ', t)
    return t


def fix_text(s):
    # apply math fixes only inside $...$
    parts = re.split(r'(\$[^$]*\$)', s)
    out = []
    for p in parts:
        if p.startswith('$') and p.endswith('$') and len(p) > 1:
            inner = fix_math(p[1:-1]).strip()
            out.append('$' + inner + '$')
        else:
            out.append(p)
    s = ''.join(out)
    s = re.sub(r'\[\s*\$?[\d.]+\$?\s*점\s*\]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def autoitem(v):
    b = v['body']
    b = re.sub(r'\n\[(학  교|년  도|중단원|난이도)\].*', '', b)
    b = re.sub(r'\n\[20\d\d년[^\]]*\]', '', b)
    b = re.sub(r'\n\d+ \| (객관식|주관식).*', '', b)
    b = re.split(r'출 ?제 ?학 ?교|\[정답\]|\[해설\]|문항별 배점|\d+\. \[출제의도\]', b)[0]
    b = re.sub(r'[A-Za-z0-9+/]{40,}={0,2}', ' ', b)
    b = re.sub(r'\$NGD\$|<\s*조\s*건\s*>|\d+\s*\|?\s*(?:객관식|주관식)?\s*\|?\s*\d{4}\s*\.\s*\d+\s*\.\s*학력평가(?:\[[^\]]*\])?', ' ', b)
    b = b.replace('[보기]', ' ')
    b = ''.join(seg if seg.startswith('$') else seg.replace('|', ' ') for seg in re.split(r'(\$[^$]*\$)', b))
    b = re.sub(r'\s+', ' ', b)
    # choices
    choices = None
    m = re.search(r'①(.*?)②(.*?)③(.*?)④(.*?)⑤(.*)$', b)
    if m:
        choices = [fix_text(x.strip()) for x in m.groups()]
        b = b[:m.start()]
    # <보기> block
    box2 = None
    mbs = list(re.finditer(r'<\s*보\s*기\s*>', b))
    mb = mbs[-1] if mbs else None
    if mb:
        tail = b[mb.end():]
        b = b[:mb.start()]
        items = re.split(r'(?=[ㄱㄴㄷㄹ]\s*\.)', tail)
        box2 = [fix_text(x) for x in items if x.strip()]
    # conditions (가)(나)(다)(라)
    box = None
    stem2 = None
    mc = re.search(r'\(가\)', b)
    if mc:
        head, conds = b[:mc.start()], b[mc.start():]
        segs = re.split(r'(?=\((?:가|나|다|라)\))', conds)
        segs = [s for s in segs if s.strip()]
        last = segs[-1]
        # split trailing question sentence off the last condition
        mq = re.match(r'^(.*?(?:다\.|\$\.|\)\.))\s*(\S.*)$', last)
        if not (mq and re.search(r'\?|시오', mq.group(2))):
            mq = None
            # first boundary: closing $ (even count so far) followed by opening $ or a question phrase
            for mm in re.finditer(r'\$', last):
                k = mm.end()
                if last[:k].count('$') % 2: continue
                rest = last[k:].lstrip()
                if (rest.startswith('$') or re.match(r'(옳은|이때|이 때)', rest)) and re.search(r'\?|시오', rest):
                    mq = re.match(r'^(.{%d})\s*(.*)$' % k, last, re.S); break
        if mq and re.search(r'\?|시오', mq.group(2)):
            segs[-1] = mq.group(1)
            stem2 = fix_text(mq.group(2))
        box = [fix_text(s) for s in segs]
        b = head
    stem = fix_text(b)
    if box and not stem2:
        mm = re.match(r'^(.*?(?:만족시킨다|만족한다|만족시킬 때|같다)\.?)\s*(\S.*(?:\?|시오\.?))$', stem)
        if mm and not re.search(r'\?|시오', mm.group(1)):
            stem, stem2 = mm.group(1), mm.group(2)
    if box2 and not stem2 and box:
        stem2 = None
    return dict(stem=stem, box=box, stem2=stem2, box2=box2, choices=choices)

#!/usr/bin/env python3
"""ARC CORE 공통국어2 보충자료 4편 — 원고(Markdown 확장) -> HTML -> PDF 빌더.

원문 무결성 원칙
- 원문 블록(:::src)은 src/raw_*.md 원본 파일에서만 생성한다. 원고에 원문을 손으로 다시 적지 않는다.
- 해설 안의 원문 인용은 ⟦...⟧ 로 표시하고, 빌드 때 원본과 대조한다. 하나라도 원본에 없으면 빌드가 실패한다.
- 인용의 위치(행/문단)는 원본에서 자동으로 계산해 붙인다.
"""
import html, os, re, subprocess, sys, json, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src')
MAN = os.path.join(ROOT, 'manuscript')
OUT = os.path.join(ROOT, 'build', 'out')
os.makedirs(OUT, exist_ok=True)

# ------------------------------------------------------------------ sources
WORKS = {
    'tan': dict(file='raw_01_tangungga.md', kind='poem', unit='행'),
    'pal': dict(file='raw_02_palwon.md', kind='poem', unit='행'),
    'mem': dict(file='raw_03_memory.md', kind='poem', unit='행'),
    'kant': dict(file='raw_04_kant_hegel.md', kind='prose', unit='문단'),
}

def load_source(key):
    w = WORKS[key]
    raw = open(os.path.join(SRC, w['file']), encoding='utf-8').read()
    lines = raw.split('\n')
    title = lines[0][2:].strip()
    assert lines[0].startswith('# ')
    origin = lines[2].strip()            # "출처: 보충자료"
    body, notes, extra = [], [], []
    mode = 'body'
    for ln in lines[3:]:
        if ln.startswith('### '):
            mode = 'notes' if ln[4:].strip() == '주석' else 'extra'
            extra_title = ln[4:].strip()
            if mode == 'extra': extra.append(('__title__', extra_title))
            continue
        if mode == 'body': body.append(ln)
        elif mode == 'notes': notes.append(ln)
        else: extra.append(('p', ln))
    # strip leading/trailing blank lines of body, keep inner blank lines (연 구분)
    while body and not body[0].strip(): body.pop(0)
    while body and not body[-1].strip(): body.pop()
    notes = [n[2:] for n in notes if n.startswith('- ')]
    ex_title = next((t for k, t in extra if k == '__title__'), None)
    ex_paras = [t for k, t in extra if k == 'p' and t.strip()]
    d = dict(w, key=key, title=title, origin=origin, notes=notes, extra_title=ex_title, extra=ex_paras, raw=raw)
    if w['kind'] == 'poem':
        # numbered lines (blank line = stanza gap, not numbered)
        num, items = 0, []
        for ln in body:
            if ln.strip():
                num += 1; items.append((num, ln))
            else:
                items.append((None, ''))
        d['items'] = items
        d['lines'] = {n: t for n, t in items if n}
        d['nlines'] = num
    else:
        paras = [p for p in body if p.strip()]
        d['paras'] = paras
    return d

SOURCES = {k: load_source(k) for k in WORKS}

# ------------------------------------------------------------------ quote verification
QUOTE_LOG = []

def locate(key, quote):
    """Return (locator_text, ok). quote may contain ' / ' (line break) and ' … ' (elision, ordered fragments)."""
    s = SOURCES[key]
    if s['kind'] == 'poem':
        text = '\n'.join(s['lines'][i] for i in sorted(s['lines']))
        frags = quote.split(' … ')
        pos = 0; first_idx = None; last_idx = None
        for f in frags:
            f_norm = f.replace(' / ', '\n')
            idx = text.find(f_norm, pos)
            if idx < 0: return None
            if first_idx is None: first_idx = idx
            last_idx = idx + len(f_norm)
            pos = last_idx
        # line numbers of first and last char
        ln_a = text.count('\n', 0, first_idx) + 1
        ln_b = text.count('\n', 0, last_idx - 1) + 1
        return (f'{ln_a}{s["unit"]}' if ln_a == ln_b else f'{ln_a}~{ln_b}{s["unit"]}')
    else:
        frags = quote.split(' … ')
        found_paras = []
        for f in frags:
            hit = [i + 1 for i, p in enumerate(s['paras']) if f in p]
            if not hit: return None
            found_paras.append(hit[0])
        a, b = min(found_paras), max(found_paras)
        return (f'{a}{s["unit"]}' if a == b else f'{a}~{b}{s["unit"]}')

# ------------------------------------------------------------------ inline
def esc(t): return html.escape(t, quote=False)

def inline(t, key):
    t = esc(t)
    # verified quotes ⟦text⟧ or ⟦text¬⟧ (no locator)
    def qrepl(m):
        body = html.unescape(m.group(1))
        qkey = key
        mm = re.match(r'^(tan|pal|mem|kant):(.*)$', body, re.S)
        if mm: qkey, body = mm.group(1), mm.group(2)
        show_loc = True
        if body.endswith('¬'):
            body = body[:-1]; show_loc = False
        loc = locate(qkey, body)
        if loc is None:
            raise SystemExit(f'[QUOTE MISMATCH] {qkey}: “{body}” 가 원본에 없습니다.')
        QUOTE_LOG.append((qkey, body, loc))
        disp = esc(body).replace(' / ', ' <span class="mk">/</span> ')
        return f'<span class="q">“{disp}”</span>' + (f'<span class="loc">({loc})</span>' if show_loc else '')
    t = re.sub(r'⟦(.+?)⟧', qrepl, t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'__(.+?)__', r'<u>\1</u>', t)
    t = t.replace('†', '<span class="mk">†</span>').replace('◇', '<span class="mk">◇</span>')
    return t

# ------------------------------------------------------------------ blocks
def src_block(key, with_extra=True):
    s = SOURCES[key]
    o = [f'<section class="src" aria-label="원문">',
         f'<div class="src-title">{esc(s["title"])}</div>',
         f'<div class="src-from">{esc(s["origin"])}</div>']
    if s['kind'] == 'poem':
        o.append('<div class="core-poem">')
        for n, t in s['items']:
            if n is None: o.append('<div class="gap"></div>')
            else: o.append(f'<div class="ln"><span class="no">{n}</span><span class="txt">{esc(t)}</span></div>')
        o.append('</div>')
    else:
        o.append('<div class="core-prose">')
        for i, p in enumerate(s['paras'], 1):
            o.append(f'<div class="pp"><span class="no">{i}</span><span class="txt">{esc(p)}</span></div>')
        o.append('</div>')
    if s['notes']:
        o.append('<div class="src-notes"><div class="nh">주석</div><ul>' + ''.join(f'<li>{esc(n)}</li>' for n in s['notes']) + '</ul></div>')
    if s['extra_title'] and with_extra:
        o.append(f'<div class="src-extra"><div class="nh">{esc(s["extra_title"])}</div>' + ''.join(f'<p>{esc(p)}</p>' for p in s['extra']) + '</div>')
    o.append('</section>')
    return '\n'.join(o)

def ev_block(key, spec):
    s = SOURCES[key]
    a, _, b = spec.partition('-')
    a = int(a); b = int(b or a)
    o = ['<div class="ev">']
    for n in range(a, b + 1):
        o.append(f'<div class="ln"><span class="no">{n}</span><span class="txt">{esc(s["lines"][n])}</span></div>')
    o.append('</div>')
    return '\n'.join(o)

def write_block(n):
    return '<div class="write"><div class="lbl">필기</div>' + '<div class="wl"></div>' * n + '</div>'

def table_block(rows, key):
    rows = [r for r in rows]
    head = [c.strip() for c in rows[0].strip().strip('|').split('|')]
    body = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows[2:]]
    o = ['<table class="core-cmp"><thead><tr>' + ''.join(f'<th>{inline(h, key)}</th>' for h in head) + '</tr></thead><tbody>']
    for r in body:
        o.append('<tr>' + ''.join(f'<td>{inline(c, key)}</td>' for c in r) + '</tr>')
    o.append('</tbody></table>')
    return '\n'.join(o)

# ------------------------------------------------------------------ manuscript parser
def parse(md_path, key):
    text = open(md_path, encoding='utf-8').read()
    lines = text.split('\n')
    out, i = [], 0
    heads = []   # (level, no, title) for TOC
    chap_no = 0
    part_open = False
    lead = []
    def flush_lead():
        nonlocal lead
        if lead:
            out.append('<div class="part-lead">' + ''.join(f'<p>{inline(p, key)}</p>' for p in lead) + '</div>')
            lead = []
    while i < len(lines):
        ln = lines[i]
        if not ln.strip(): i += 1; continue
        if ln.startswith('# '):
            title = ln[2:].strip(); kicker = sub = ''
            j = i + 1
            while j < len(lines) and lines[j].startswith('%'):
                k, _, v = lines[j][1:].partition(' ')
                if k == 'kicker': kicker = v
                if k == 'sub': sub = v
                j += 1
            out.append(f'<header class="part-open"><div class="part-kicker">{esc(kicker)}</div>'
                       f'<h1 class="part-title">{esc(title)}</h1><div class="part-sub">{esc(sub)}</div>')
            i = j
            # lead paragraphs until a directive or heading
            lead_ps = []
            while i < len(lines) and not (lines[i].startswith(('#', ':::'))):
                if lines[i].strip():
                    buf = [lines[i]]; i += 1
                    while i < len(lines) and lines[i].strip() and not lines[i].startswith(('#', ':::')):
                        buf.append(lines[i]); i += 1
                    lead_ps.append(' '.join(buf))
                else: i += 1
            out.append('<div class="part-lead">' + ''.join(f'<p>{inline(p, key)}</p>' for p in lead_ps) + '</div></header>')
            heads.append((1, None, title))
            continue
        if ln.startswith('## '):
            chap_no += 1
            t = ln[3:].strip()
            out.append(f'<h2><span class="no">{chap_no}</span>{inline(t, key)}</h2>')
            heads.append((2, chap_no, t)); i += 1; continue
        if ln.startswith('### '):
            t = ln[4:].strip()
            out.append(f'<h3>{inline(t, key)}</h3>'); heads.append((3, None, t)); i += 1; continue
        if ln.startswith('#### '):
            out.append(f'<h4>{inline(ln[5:].strip(), key)}</h4>'); i += 1; continue
        if ln.startswith(':::extra'):
            ek = ln[8:].strip() or key
            se = SOURCES[ek]
            out.append('<section class="src src-solo"><div class="src-from">보충자료에 실린 설명</div><div class="src-extra" style="border-top:0;margin-top:0;padding-top:0"><div class="nh">' + esc(se['extra_title']) + '</div>' + ''.join(f'<p>{esc(p)}</p>' for p in se['extra']) + '</div></section>')
            i += 1; continue
        if ln.startswith(':::src'):
            out.append(src_block(key, with_extra=('noextra' not in ln))); i += 1; continue
        m = re.match(r':::ev\s+(\d+(?:-\d+)?)\s*$', ln)
        if m: out.append(ev_block(key, m.group(1))); i += 1; continue
        m = re.match(r':::write\s+(\d+)\s*$', ln)
        if m: out.append(write_block(int(m.group(1)))); i += 1; continue
        if ln.startswith(':::keep'):
            i += 1; inner = []
            while i < len(lines) and lines[i].strip() != ':::':
                inner.append(lines[i]); i += 1
            i += 1
            paras, buf = [], []
            for l2 in inner:
                if l2.strip(): buf.append(l2)
                elif buf: paras.append(' '.join(buf)); buf = []
            if buf: paras.append(' '.join(buf))
            out.append('<div class="keep">' + ''.join(f'<p>{inline(p, key)}</p>' for p in paras) + '</div>')
            continue
        if ln.startswith('>> '):
            out.append(f'<p class="thesis">{inline(ln[3:].strip(), key)}</p>'); i += 1; continue
        if ln.startswith('> '):
            out.append(f'<p class="point">{inline(ln[2:].strip(), key)}</p>'); i += 1; continue
        if ln.startswith(':::def'):
            title = ln[6:].strip(); i += 1; rows = []
            while i < len(lines) and lines[i].strip() != ':::':
                if lines[i].strip():
                    lab, _, txt = lines[i].partition('|')
                    rows.append((lab.strip(), txt.strip()))
                i += 1
            i += 1
            out.append('<div class="core-def"><div class="ct">' + inline(title, key) + '</div>' +
                       ''.join(f'<div class="r"><span class="l">{esc(l)}</span><span class="t">{inline(t, key)}</span></div>' for l, t in rows) + '</div>')
            heads.append((3, None, title)); continue
        if ln.startswith(':::flow'):
            title = ln[7:].strip(); i += 1; nodes_line = ''
            while i < len(lines) and lines[i].strip() != ':::':
                nodes_line += lines[i].strip() + ' '; i += 1
            i += 1
            nodes = [n.strip() for n in nodes_line.strip().split(' => ')]
            parts_html = []
            for n_i, n in enumerate(nodes):
                items = [x.strip() for x in n.split(' / ')]
                parts_html.append('<div class="fn"><b>' + inline(items[0], key) + '</b>' + ''.join(f'<span>{inline(x, key)}</span>' for x in items[1:]) + '</div>')
                if n_i < len(nodes) - 1: parts_html.append('<div class="fa">→</div>')
            out.append('<div class="core-flow"><div class="ft">' + inline(title, key) + '</div><div class="fr">' + ''.join(parts_html) + '</div></div>')
            continue
        if ln.startswith(':::rule'):
            title = ln[7:].strip(); i += 1; inner = []
            while i < len(lines) and lines[i].strip() != ':::':
                inner.append(lines[i]); i += 1
            i += 1
            paras, buf = [], []
            for l2 in inner:
                if l2.strip(): buf.append(l2)
                elif buf: paras.append(' '.join(buf)); buf = []
            if buf: paras.append(' '.join(buf))
            out.append('<div class="core-rule">' + (f'<div class="rt">{inline(title, key)}</div>' if title else '') +
                       ''.join(f'<p>{inline(p, key)}</p>' for p in paras) + '</div>')
            continue
        if ln.startswith(':::box'):
            title = ln[6:].strip(); i += 1; inner = []
            while i < len(lines) and lines[i].strip() != ':::':
                inner.append(lines[i]); i += 1
            i += 1
            paras, buf = [], []
            for l2 in inner:
                if l2.strip(): buf.append(l2)
                elif buf: paras.append(' '.join(buf)); buf = []
            if buf: paras.append(' '.join(buf))
            out.append('<div class="box">' + (f'<div class="bt">{inline(title, key)}</div>' if title else '') +
                       ''.join(f'<p>{inline(p, key)}</p>' for p in paras) + '</div>')
            continue
        if ln.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append(lines[i]); i += 1
            out.append(table_block(rows, key)); continue
        if re.match(r'^(- |\d+\. )', ln):
            ordered = bool(re.match(r'^\d+\. ', ln)); items = []
            while i < len(lines) and re.match(r'^(- |\d+\. )', lines[i]):
                buf = [re.sub(r'^(- |\d+\. )', '', lines[i])]; i += 1
                while i < len(lines) and lines[i].startswith('  ') and lines[i].strip():
                    buf.append(lines[i].strip()); i += 1
                items.append(' '.join(buf))
            tag = 'ol' if ordered else 'ul'
            # a lead-in line (요지 문장 or a short intro paragraph) must not be stranded at the foot of a page:
            # bind it to the first list item, and let the remaining items flow on
            prev = out[-1] if out else ''
            lead_in = prev.startswith('<p class="point">') or (prev.startswith('<p>') and len(prev) < 170)
            if lead_in and items:
                out.pop()
                pre = out.pop() if out and out[-1].startswith('<div class="ev">') else ''   # keep the quoted lines with their reading
                first, rest = items[0], items[1:]
                grp = f'<div class="keepfirst">{pre}{prev}<{tag}><li>{inline(first, key)}</li></{tag}></div>'
                if rest:
                    start = ' start="2"' if ordered else ''
                    grp += f'<{tag} class="cont"{start}>' + ''.join(f'<li>{inline(x, key)}</li>' for x in rest) + f'</{tag}>'
                out.append(grp); continue
            out.append(f'<{tag}>' + ''.join(f'<li>{inline(x, key)}</li>' for x in items) + f'</{tag}>'); continue
        # paragraph
        buf = [ln]; i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#|:::|\||>|- |\d+\. )', lines[i]):
            buf.append(lines[i]); i += 1
        out.append(f'<p>{inline(" ".join(buf), key)}</p>')
    return '\n'.join(out), heads

def page_html(body, title):
    return ('<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>' + esc(title) + '</title>'
            '<link rel="stylesheet" href="../../fonts/notosanskr/400.css"><link rel="stylesheet" href="../../fonts/notosanskr/600.css"><link rel="stylesheet" href="../../fonts/notosanskr/700.css"><link rel="stylesheet" href="../style.css"></head>'
            '<body><main data-product="arc-core">' + body + '</main></body></html>')

def build_part(md_name, key, out_name):
    body, heads = parse(os.path.join(MAN, md_name), key)
    p = os.path.join(OUT, out_name + '.html')
    open(p, 'w', encoding='utf-8').write(page_html(body, out_name))
    return p, heads

def render(html_path, pdf_path):
    env = dict(os.environ)
    env.setdefault('PW_CORE', '/tmp/claude-0/-home-user-ARC-System/93342be4-b04c-59ef-9919-cabc732871c0/scratchpad/tools/node_modules/playwright-core')
    r = subprocess.run(['node', os.path.join(ROOT, 'build', 'render_pdf.js'), html_path, pdf_path], capture_output=True, text=True, env=env)
    if r.returncode != 0: raise SystemExit(r.stderr)
    info = json.loads(r.stdout.strip().splitlines()[-1])
    if info['errs']: print('render warnings:', info['errs'])
    return info

if __name__ == '__main__':
    which = sys.argv[1:] or ['tan']
    cfg = {'tan': ('01_tangungga.md', 'part_01_tangungga')}
    for k in which:
        md, name = cfg[k]
        p, heads = build_part(md, k, name)
        info = render(p, os.path.join(OUT, name + '.pdf'))
        json.dump(heads, open(os.path.join(OUT, name + '.heads.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        print(name, 'ok; quotes verified:', sum(1 for q in QUOTE_LOG if q[0] == k), '| column_count =', info['audit']['columnCount'])

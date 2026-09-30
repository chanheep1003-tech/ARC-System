#!/usr/bin/env python3
"""원고(빌드용 확장 표기) -> 깨끗한 학생용 Markdown 원고.
- ⟦인용⟧ 은 build.py 와 같은 방식으로 원본과 대조한 뒤 “인용”(위치) 로 바꾼다.
- :::src/ev/def/rule/flow/keep/box/write/extra 는 일반 Markdown 으로 펼친다.
- 원문 블록은 src/raw_*.md 에서만 만든다(원고에 손으로 옮겨 적지 않는다).
usage: python3 export_md.py [출력파일]
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B
import assemble as A
import assemble_all as AA

OUT_DEFAULT = os.path.join(B.ROOT, 'ARC_CORE_공통국어2_보충자료4편_V2.0_원고.md')
SPECIAL = re.compile(r'([\\*_<>\[\]`|])')

def mdesc(t):
    return SPECIAL.sub(r'\\\1', t)

def inl(t, key):
    def qrepl(m):
        body = m.group(1)
        qkey = key
        mm = re.match(r'^(tan|pal|mem|kant):(.*)$', body, re.S)
        if mm: qkey, body = mm.group(1), mm.group(2)
        show = True
        if body.endswith('¬'): body, show = body[:-1], False
        loc = B.locate(qkey, body)
        if loc is None:
            raise SystemExit(f'[QUOTE MISMATCH] {qkey}: “{body}”')
        B.QUOTE_LOG.append((qkey, body, loc))
        return f'“{body}”' + (f'({loc})' if show else '')
    t = re.sub(r'⟦(.+?)⟧', qrepl, t)
    t = re.sub(r'__(.+?)__', r'<u>\1</u>', t)
    return t

def bold_line(t, key):
    return '**' + inl(t, key).replace('**', '') + '**'

def bq(lines):
    return '\n'.join(('> ' + l if l else '>') for l in lines)

def src_md(key, with_extra=True):
    s = B.SOURCES[key]
    o = [f'**{s["title"]}**', '', s['origin'], '']
    q = []
    if s['kind'] == 'poem':
        for n, t in s['items']:
            q.append('' if n is None else f'{n:>2}  {mdesc(t)}  ')
    else:
        for i, p in enumerate(s['paras'], 1):
            if i > 1: q.append('')
            q.append(f'**{i}**  {mdesc(p)}')
    o.append(bq(q))
    if s['notes']:
        o += ['', '**주석**', ''] + [f'- {n}' for n in s['notes']]
    if s['extra_title'] and with_extra:
        o += ['', f'**{s["extra_title"]}**', '']
        o.append(bq([l for p in s['extra'] for l in (mdesc(p), '')][:-1]))
    return '\n'.join(o)

def ev_md(key, spec):
    s = B.SOURCES[key]
    a, _, b = spec.partition('-'); a = int(a); b = int(b or a)
    return bq([f'{n:>2}  {mdesc(s["lines"][n])}  ' for n in range(a, b + 1)])

def paras_of(inner):
    paras, buf = [], []
    for l2 in inner:
        if l2.strip(): buf.append(l2)
        elif buf: paras.append(' '.join(buf)); buf = []
    if buf: paras.append(' '.join(buf))
    return paras

def convert(md_name, key):
    lines = open(os.path.join(B.MAN, md_name), encoding='utf-8').read().split('\n')
    out, i, chap = [], 0, 0
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
            i = j
            out.append(f'## {title}')
            meta = ' · '.join(x for x in (kicker, sub) if x)
            if meta: out.append(f'*{meta}*')
            lead = []
            while i < len(lines) and not lines[i].startswith(('#', ':::')):
                if lines[i].strip():
                    buf = [lines[i]]; i += 1
                    while i < len(lines) and lines[i].strip() and not lines[i].startswith(('#', ':::')):
                        buf.append(lines[i]); i += 1
                    lead.append(inl(' '.join(buf), key))
                else: i += 1
            out += lead
            continue
        if ln.startswith('## '):
            chap += 1; out.append(f'### {chap}. {inl(ln[3:].strip(), key)}'); i += 1; continue
        if ln.startswith('### '):
            out.append(f'#### {inl(ln[4:].strip(), key)}'); i += 1; continue
        if ln.startswith('#### '):
            out.append(f'##### {inl(ln[5:].strip(), key)}'); i += 1; continue
        if ln.startswith(':::extra'):
            ek = ln[8:].strip() or key
            se = B.SOURCES[ek]
            out.append('\n'.join([f'**보충자료에 실린 설명 — {se["extra_title"]}**', '',
                                  bq([l for p in se['extra'] for l in (mdesc(p), '')][:-1])]))
            i += 1; continue
        if ln.startswith(':::src'):
            out.append(src_md(key, with_extra=('noextra' not in ln))); i += 1; continue
        m = re.match(r':::ev\s+(\d+(?:-\d+)?)\s*$', ln)
        if m: out.append(ev_md(key, m.group(1))); i += 1; continue
        m = re.match(r':::write\s+(\d+)\s*$', ln)
        if m: out.append(f'**필기** (빈 줄 {m.group(1)}줄)'); i += 1; continue
        if ln.startswith(':::keep'):
            i += 1; inner = []
            while i < len(lines) and lines[i].strip() != ':::': inner.append(lines[i]); i += 1
            i += 1
            out.append('\n\n'.join(inl(p, key) for p in paras_of(inner))); continue
        if ln.startswith('>> '):
            out.append(bold_line(ln[3:].strip(), key)); i += 1; continue
        if ln.startswith('> '):
            out.append(bold_line(ln[2:].strip(), key)); i += 1; continue
        if ln.startswith(':::def'):
            title = ln[6:].strip(); i += 1; rows = []
            while i < len(lines) and lines[i].strip() != ':::':
                if lines[i].strip():
                    lab, _, txt = lines[i].partition('|'); rows.append((lab.strip(), txt.strip()))
                i += 1
            i += 1
            out.append('\n'.join([f'**{inl(title, key)}**', ''] + [f'- **{l}** {inl(t, key)}' for l, t in rows])); continue
        if ln.startswith(':::flow'):
            title = ln[7:].strip(); i += 1; nodes_line = ''
            while i < len(lines) and lines[i].strip() != ':::': nodes_line += lines[i].strip() + ' '; i += 1
            i += 1
            nodes = []
            for n in nodes_line.strip().split(' => '):
                items = [x.strip() for x in n.split(' / ')]
                nodes.append(f'**{inl(items[0], key)}**' + (f'({", ".join(inl(x, key) for x in items[1:])})' if items[1:] else ''))
            out.append(f'**{inl(title, key)}**\n\n' + ' → '.join(nodes)); continue
        if ln.startswith((':::rule', ':::box')):
            tag = ln[:7] if ln.startswith(':::rule') else ln[:6]
            title = ln[len(tag):].strip(); i += 1; inner = []
            while i < len(lines) and lines[i].strip() != ':::': inner.append(lines[i]); i += 1
            i += 1
            q = ([f'**{inl(title, key)}**', ''] if title else [])
            for p in paras_of(inner): q += [inl(p, key), '']
            out.append(bq(q[:-1] if q and q[-1] == '' else q)); continue
        if ln.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'): rows.append(lines[i]); i += 1
            out.append('\n'.join(re.sub(r'⟦.+?⟧', lambda m: inl(m.group(0), key), r) for r in rows)); continue
        if re.match(r'^(- |\d+\. )', ln):
            items = []
            while i < len(lines) and re.match(r'^(- |\d+\. )', lines[i]):
                head = re.match(r'^(- |\d+\. )', lines[i]).group(1)
                buf = [lines[i][len(head):]]; i += 1
                while i < len(lines) and lines[i].startswith('  ') and lines[i].strip():
                    buf.append(lines[i].strip()); i += 1
                items.append(head + inl(' '.join(buf), key))
            out.append('\n'.join(items)); continue
        buf = [ln]; i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#|:::|\||>|- |\d+\. )', lines[i]):
            buf.append(lines[i]); i += 1
        out.append(inl(' '.join(buf), key))
    return '\n\n'.join(out)

def front():
    o = ['# 공통국어2 보충자료 4편 해설 필기노트', '',
         '정훈 「탄궁가」 · 백석 「팔원」 · 기형도 「기억할 만한 지나침」  ',
         '이행남 「칸트의 도덕적 자율성으로부터 헤겔의 인륜적 자율성으로」', '',
         '2026 동북고 1학년 2학기 중간대비', '', '## 차례', '']
    for k in AA.ORDER:
        c = AA.PARTS[k]
        o.append(f'- {c["toc"]}' + (f' ({c["toc_sub"]})' if c['toc_sub'] else ''))
        for j, ch in enumerate(c['chs'], 1): o.append(f'  - {j}. {ch}')
    o += ['', '## 읽는 방법', '']
    for dt, dd in re.findall(r'<dt>(.*?)</dt>\s*<dd>(.*?)</dd>', A.GUIDE_HTML, re.S):
        o += [f'**{dt}**', '', dd, '']
    return '\n'.join(o)

def main(path):
    body = [front()]
    for k in AA.ORDER:
        c = AA.PARTS[k]
        body.append(convert(c['md'], c['key']))
    txt = '\n\n'.join(body).rstrip() + '\n'
    txt = re.sub(r'\n{3,}', '\n\n', txt)
    leaks = [t for t in ('⟦', '⟧', '¬', ':::', '%kicker', '%sub') if t in txt]
    assert not leaks, f'markup leak: {leaks}'
    open(path, 'w', encoding='utf-8').write(txt)
    print('wrote', path, len(txt.encode('utf-8')), 'bytes,', txt.count('\n') + 1, 'lines')
    print('quotes verified this run:', len(B.QUOTE_LOG))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else OUT_DEFAULT)

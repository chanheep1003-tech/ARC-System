#!/usr/bin/env python3
"""전체 조립: 표지 + 차례·읽는 방법 + 작품 4편 + 네 작품 비교 + 시험 직전 정리 (흑백).
usage: python3 assemble_all.py [--parts tan,pal,mem,kant,cmp,fin] [--out 파일명] [--max-pages 40]
차례의 쪽 번호는 조립된 PDF에서 제목을 찾아 채운다(placeholder 없음).
"""
import os, sys, json, argparse
import pymupdf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B
import assemble as A

ROOT = B.ROOT
PARTS = {
    'tan':  dict(md='01_tangungga.md', key='tan',  name='part_01_tangungga', run='공통국어2 · 「탄궁가」 정훈',        toc='「탄궁가」', toc_sub='정훈 · 가사',
                 chs=['기본 이해', '형식과 전개', '부분별 해석', '시험 대비 개념', '헷갈리는 개념', '정리']),
    'pal':  dict(md='02_palwon.md',    key='pal',  name='part_02_palwon',    run='공통국어2 · 「팔원」 백석',          toc='「팔원」', toc_sub='백석 · 현대시',
                 chs=['기본 이해', '형식과 전개', '부분별 해석', '시험 대비 개념', '헷갈리는 개념', '정리']),
    'mem':  dict(md='03_memory.md',    key='mem',  name='part_03_memory',    run='공통국어2 · 「기억할 만한 지나침」 기형도', toc='「기억할 만한 지나침」', toc_sub='기형도 · 현대시',
                 chs=['기본 이해', '형식과 전개', '부분별 해석', '시험 대비 개념', '헷갈리는 개념', '정리']),
    'kant': dict(md='04_kant_hegel.md', key='kant', name='part_04_kant',      run='공통국어2 · 칸트·헤겔 (이행남)',     toc='칸트의 도덕적 자율성으로부터 헤겔의 인륜적 자율성으로', toc_sub='이행남 · 비문학',
                 chs=['기본 이해', '글의 구조', '문단별 해석', '시험 대비 개념', '헷갈리는 개념', '정리']),
    'cmp':  dict(md='05_compare.md',   key='tan',  name='part_05_compare',   run='공통국어2 · 네 작품 비교',            toc='네 작품 비교', toc_sub='',   chs=[]),
    'fin':  dict(md='06_final.md',     key='tan',  name='part_06_final',     run='공통국어2 · 시험 직전 정리',          toc='시험 직전 정리', toc_sub='', chs=[]),
}
ORDER = ['tan', 'pal', 'mem', 'kant', 'cmp', 'fin']

def toc_html(rows):
    """rows: list of (level, title, sub, page or None, chapters[(label,page)])"""
    o = ['<h2 class="front-title">차례</h2><div class="toc">']
    for lvl, title, sub, pg, chs in rows:
        p = f'{pg:02d}' if pg else ''
        s = f' <span class="tsub">{sub}</span>' if sub else ''
        o.append(f'<div class="row l1"><span>{title}{s}</span><span class="pg">{p}</span></div>')
        if chs:
            o.append('<div class="row l2"><span>' + ' · '.join(f'{l} {n:02d}' for l, n in chs if n) + '</span><span></span></div>')
    o.append('</div>')
    return ''.join(o)

def find_pages(doc, first, last, chap_titles):
    """part page range [first,last]; return {chapter_no: page(1-based)} by locating large-heading spans."""
    found = {}
    for i in range(first, last + 1):
        for b in doc[i].get_text('dict')['blocks']:
            for l in b.get('lines', []):
                txt = ''.join(s['text'] for s in l['spans']).strip()
                size = max((s['size'] for s in l['spans']), default=0)
                if size >= 14 and size < 17:
                    for no, t in chap_titles.items():
                        if no not in found and t in txt: found[no] = i + 1
    return found

CHAPTER_RULE = (0.6157, 0.6314, 0.6549)   # #9DA1A7, the rule above a chapter heading

def strip_top_chapter_rules(doc, first_body_page):
    """A chapter heading that lands at the top of a page would sit right under the
    running-head rule and read as a doubled line. Remove only that rule (line art only)."""
    n = 0
    for i in range(first_body_page, len(doc)):
        page = doc[i]
        hit = []
        for dr in page.get_drawings():
            r, fill = dr['rect'], dr.get('fill')
            if (fill and r.width > 300 and r.height < 1.5 and 60.5 < r.y0 < 64
                    and all(abs(a - b) < 0.01 for a, b in zip(fill, CHAPTER_RULE))):
                hit.append(r)
        for r in hit:
            page.add_redact_annot(pymupdf.Rect(r.x0 - 1, r.y0 - 0.6, r.x1 + 1, r.y1 + 0.6))
        if hit:
            page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                                  graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                                  text=pymupdf.PDF_REDACT_TEXT_NONE)
            n += len(hit)
    print('top-of-page chapter rules removed:', n)

def build(parts, out_name, max_pages):
    built, heads_by = {}, {}
    for k in parts:
        cfg = PARTS[k]
        md = os.path.join(B.MAN, cfg['md'])
        if not os.path.exists(md):
            print('skip (no manuscript):', k); continue
        p, heads = B.build_part(cfg['md'], cfg['key'], cfg['name'])
        B.render(p, os.path.join(B.OUT, cfg['name'] + '.pdf'))
        built[k] = os.path.join(B.OUT, cfg['name'] + '.pdf'); heads_by[k] = heads
    parts = [k for k in parts if k in built]

    cover = A.make_front('front_cover', A.COVER_HTML)
    def front(rows):
        return A.make_front('front_toc', toc_html(rows) + A.GUIDE_HTML_COMPACT)
    # pass 1 (page numbers unknown yet -> same page count either way)
    rows = [(1, PARTS[k]['toc'], PARTS[k]['toc_sub'], None, [(l, 0) for l in PARTS[k]['chs']]) for k in parts]
    toc_pdf = front(rows)

    def assemble(toc_pdf):
        doc = pymupdf.open()
        for f in (cover, toc_pdf):
            doc.insert_pdf(pymupdf.open(f))
        ranges = {}
        for k in parts:
            src = pymupdf.open(built[k]); start = len(doc)
            doc.insert_pdf(src); ranges[k] = (start, len(doc) - 1)
        return doc, ranges
    doc, ranges = assemble(toc_pdf)
    # compute real numbers
    rows = []
    for k in parts:
        first, last = ranges[k]
        chap_titles = {no: t for (lvl, no, t) in heads_by[k] if lvl == 2}
        pgs = find_pages(doc, first, last, chap_titles)
        chs = [(PARTS[k]['chs'][no - 1], pgs.get(no)) for no in sorted(chap_titles) if no - 1 < len(PARTS[k]['chs'])] if PARTS[k]['chs'] else []
        rows.append((1, PARTS[k]['toc'], PARTS[k]['toc_sub'], first + 1, chs))
    toc_pdf = front(rows)
    doc, ranges = assemble(toc_pdf)
    assert len(doc) == (2 + sum(r[1] - r[0] + 1 for r in ranges.values())), 'page count mismatch'

    plan = {1: ('공통국어2 · 차례와 읽는 방법', True)}
    for k, (a, b) in ranges.items():
        for i in range(a, b + 1): plan[i] = (PARTS[k]['run'], True)
    strip_top_chapter_rules(doc, first_body_page=2)
    A.stamp(doc, plan)
    doc.set_metadata({'title': '공통국어2 보충자료 4편 해설 필기노트', 'author': 'ARC CORE', 'subject': '2026 동북고 1학년 2학기 중간대비'})
    doc.subset_fonts()
    out = os.path.join(ROOT, out_name)
    doc.save(out, garbage=4, deflate=True)
    print('saved', out, '|', len(doc), 'pages | ranges', {k: (a + 1, b + 1) for k, (a, b) in ranges.items()})
    if len(doc) > max_pages:
        print(f'!! PAGE BUDGET EXCEEDED: {len(doc)} > {max_pages}')
    return out, ranges

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--parts', default=','.join(ORDER))
    ap.add_argument('--out', default='ARC_CORE_공통국어2_보충자료4편_V2.0_흑백.pdf')
    ap.add_argument('--max-pages', type=int, default=40)
    a = ap.parse_args()
    build([p for p in a.parts.split(',') if p], a.out, a.max_pages)

#!/usr/bin/env python3
"""표지·읽는 방법·작품 PDF를 합치고 러닝헤드/쪽 번호를 넣는다(흑백).
usage: python3 assemble.py draft   -> 탄궁가 시안(표지+읽는 방법+탄궁가)
"""
import os, sys, json, html
import pymupdf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B

ROOT = B.ROOT
FONTS = os.path.join(ROOT, 'fonts', 'pretendard')
F_REG, F_SEMI = os.path.join(FONTS, 'Pretendard-Regular.ttf'), os.path.join(FONTS, 'Pretendard-SemiBold.ttf')
MM = 72 / 25.4
INK = (0x24 / 255, 0x28 / 255, 0x2F / 255)
MUTE = (0x5F / 255, 0x64 / 255, 0x6B / 255)
RULE = (0xBF / 255, 0xC2 / 255, 0xC6 / 255)

COVER_HTML = """
<div class="cover">
  <div class="rule"></div>
  <div class="title-block">
    <div class="c-subject">공통국어2</div>
    <div class="c-sub">보충자료 4편 해설 필기노트<br>정훈 「탄궁가」 · 백석 「팔원」 · 기형도 「기억할 만한 지나침」<br>이행남 「칸트의 도덕적 자율성으로부터 헤겔의 인륜적 자율성으로」</div>
  </div>
  <div class="c-meta">2026 동북고 1학년 2학기 중간대비</div>
</div>
"""

GUIDE_HTML = """
<h2 class="front-title">읽는 방법</h2>
<dl class="guide">
<dt>원문과 해설</dt>
<dd>각 작품의 첫머리에 보충자료의 원문과 주석을 있는 그대로 실었고, 해설은 그 뒤에 붙였다. 원문 옆의 번호는 해설에서 위치를 가리키려고 붙인 것으로, 시는 행 번호이고 산문은 문단 번호이다.</dd>
<dt>원문 인용</dt>
<dd>해설에서 원문을 옮긴 부분은 “ ” 안에 넣고, 대체로 뒤에 (10행)처럼 위치를 밝혔다. 두 행 이상을 옮길 때 행이 바뀌는 곳은 /로 표시했다. 각 부분 해석 앞에서 왼쪽에 세로선이 있는 줄은 해당 행을 원문에서 그대로 옮겨 놓은 것이다.</dd>
<dt>† 표시</dt>
<dd>보충자료에는 없고 다른 자료로 덧붙인 사실이나 배경에 붙였다. 작가, 제목의 한자, 고사의 배경, 다른 학습 자료의 설명 등이 여기에 해당한다. 보충자료로 확인되는 설명과 구별해서 읽는다.</dd>
<dt>◇ 표시</dt>
<dd>풀이가 갈릴 수 있어 수업 시간에 어떻게 정리했는지 확인해 둘 항목에 붙였다. 학교에서 정한 기준이 있으면 그 기준을 따른다.</dd>
<dt>선지 판단 예시</dt>
<dd>이 노트에서 새로 만든 학습용 예시이며 실제 기출문항이 아니다.</dd>
</dl>
"""

GUIDE_HTML_COMPACT = GUIDE_HTML.replace('<h2 class="front-title">읽는 방법</h2>', '<h2 class="front-title f2">읽는 방법</h2>').replace('<dl class="guide">', '<dl class="guide compact">')

def make_front(name, body_html, height_fix=None):
    p = os.path.join(B.OUT, name + '.html')
    open(p, 'w', encoding='utf-8').write(B.page_html(body_html, name))
    B.render(p, os.path.join(B.OUT, name + '.pdf'))
    return os.path.join(B.OUT, name + '.pdf')

def text_w(font, txt, size):
    return pymupdf.Font(fontfile=font).text_length(txt, fontsize=size)

def stamp(doc, plan):
    """plan: {page_index: (right_text, show_number)}"""
    W, H = 210 * MM, 297 * MM
    for i, (rt, num) in plan.items():
        pg = doc[i]
        pg.insert_font(fontname='PR', fontfile=F_REG)
        pg.insert_font(fontname='PS', fontfile=F_SEMI)
        y = 12.6 * MM
        x = 17 * MM
        for ch in 'ARC CORE':                      # text-only compact running head (letter-spaced)
            pg.insert_text((x, y), ch, fontname='PS', fontfile=F_SEMI, fontsize=7.4, color=INK)
            x += text_w(F_SEMI, ch, 7.4) + 0.75
        w = text_w(F_REG, rt, 7.2)
        pg.insert_text((W - 17 * MM - w, y), rt, fontname='PR', fontfile=F_REG, fontsize=7.2, color=MUTE)
        pg.draw_line((17 * MM, 15.6 * MM), (W - 17 * MM, 15.6 * MM), color=RULE, width=0.45)
        if num:
            s = f'{i + 1:02d}'
            w = text_w(F_REG, s, 7.6)
            pg.draw_line((17 * MM, H - 15.2 * MM), (W - 17 * MM, H - 15.2 * MM), color=RULE, width=0.45)
            pg.insert_text(((W - w) / 2, H - 11.4 * MM), s, fontname='PR', fontfile=F_REG, fontsize=7.6, color=MUTE)

def assemble_draft():
    cfg_name = 'part_01_tangungga'
    p, heads = B.build_part('01_tangungga.md', 'tan', cfg_name)
    B.render(p, os.path.join(B.OUT, cfg_name + '.pdf'))
    json.dump(heads, open(os.path.join(B.OUT, cfg_name + '.heads.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    cover = make_front('front_cover', COVER_HTML)
    guide = make_front('front_guide', GUIDE_HTML)
    doc = pymupdf.open()
    for f in (cover, guide, os.path.join(B.OUT, cfg_name + '.pdf')):
        doc.insert_pdf(pymupdf.open(f))
    n_cover, n_guide = 1, 1
    plan = {}
    for i in range(len(doc)):
        if i == 0: continue
        right = '공통국어2 · 읽는 방법' if i == 1 else '공통국어2 · 「탄궁가」 정훈'
        plan[i] = (right, True)
    stamp(doc, plan)
    doc.set_metadata({'title': '공통국어2 보충자료 4편 해설 필기노트 — 「탄궁가」 시안', 'author': 'ARC CORE', 'subject': '2026 동북고 1학년 2학기 중간대비'})
    doc.subset_fonts()
    out = os.path.join(ROOT, 'ARC_CORE_공통국어2_보충자료4편_V2.0_시안_탄궁가_흑백.pdf')
    doc.save(out, garbage=4, deflate=True)
    print('saved', out, len(doc), 'pages')
    return out

if __name__ == '__main__':
    if sys.argv[1:] == ['draft']:
        assemble_draft()

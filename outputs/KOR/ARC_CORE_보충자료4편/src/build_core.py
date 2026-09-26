# -*- coding: utf-8 -*-
import re, sys, pathlib
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from core_content import TAN_NOTES, PAL_NOTES, MEM_NOTES, KANT_NOTES
from core_blocks import OVERVIEW, BLOCKS, COMPARE, EXTRA, EXTRA_MAP, CROSS, TRAPS, OX

def hl(s):
    s = re.sub(r"\{\{(.+?)\}\}", r'<mark>\1</mark>', s)
    return re.sub(r"\[\[(.+?)\]\]", r'<span class="ul">\1</span>', s)

# ───────── SVG ─────────
NAVY, BURG, WARM, GREY = "#1F2A44", "#7A2E35", "#E9E7E1", "#6b7076"
F = "font-family=\"'Noto Sans CJK KR',sans-serif\""

def t(x, y, s, size=11, fill="#23272c", weight=400, anchor="middle"):
    return f'<text x="{x}" y="{y}" {F} font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{s}</text>'

def svg_pal():
    o = ['<svg viewBox="0 0 680 250" class="fig">',
         f'<rect x="10" y="40" width="330" height="170" rx="14" fill="#f7f6f2" stroke="{NAVY}" stroke-width="1.6"/>',
         t(175, 30, "차 안 — 묘향산행 승합자동차(텅 비인 차)", 12, NAVY, 700),
         f'<circle cx="95" cy="115" r="30" fill="#fff" stroke="{NAVY}" stroke-width="1.4"/>', t(95, 111, "계집아이", 11, NAVY, 700), t(95, 126, "운다", 10, GREY),
         t(95, 168, "새 저고리 · 터진 손잔등", 10), t(95, 183, "(관찰)", 9.5, GREY),
         f'<circle cx="255" cy="115" r="30" fill="#fff" stroke="{BURG}" stroke-width="1.4"/>', t(255, 107, "어느 한", 10.5, BURG, 700), t(255, 121, "사람(화자)", 10.5, BURG, 700),
         t(255, 168, "한구석에서 눈을 씻는다", 10), t(255, 183, "(자신을 객체화)", 9.5, GREY),
         f'<line x1="360" y1="40" x2="360" y2="210" stroke="{GREY}" stroke-width="3" stroke-dasharray="2 5"/>',
         t(360, 228, "쌔하얗게 얼은 유리창(경계)", 10.5, GREY, 700),
         f'<rect x="380" y="40" width="290" height="80" rx="12" fill="#fff" stroke="{NAVY}" stroke-width="1.2"/>',
         t(525, 30, "유리창 밖", 12, NAVY, 700),
         t(525, 72, "내지 주재소장 ‘같은’ 어른 + 어린아이 둘", 11, NAVY, 700), t(525, 96, "내임을 낸다(배웅) — 관찰 + 짐작", 10, GREY),
         f'<rect x="380" y="138" width="290" height="72" rx="12" fill="#fbf6f6" stroke="{BURG}" stroke-width="1.2" stroke-dasharray="5 4"/>',
         t(525, 162, "추측: 몇 해고 내지인 주재소장 집에서", 10.5, BURG, 700), t(525, 180, "밥 짓기 · 걸레 치기 · 아이보개", 10.5, BURG), t(525, 198, "(-었을 것이다)", 9.5, GREY),
         t(175, 236, "전해 들음: 자성 삼백오십 리 / 묘향산 어디메 삼촌", 10, GREY),
         '</svg>']
    return "".join(o)

def panel(x0, title, inside, inside_sub, outside, outside_sub, who_in, arrow_out_to_in):
    o = [f'<rect x="{x0}" y="36" width="310" height="170" rx="12" fill="#fff" stroke="#c9ccd0"/>',
         t(x0 + 155, 26, title, 12, NAVY, 700),
         f'<rect x="{x0+12}" y="50" width="150" height="142" rx="8" fill="#f3f2ee"/>',
         t(x0 + 87, 72, "창 안", 10, GREY, 700), t(x0 + 87, 112, inside, 11, NAVY, 700), t(x0 + 87, 130, inside_sub, 10, GREY),
         t(x0 + 87, 152, who_in, 10.5, BURG if "화자" in who_in else NAVY, 700),
         f'<line x1="{x0+172}" y1="50" x2="{x0+172}" y2="192" stroke="{GREY}" stroke-width="3" stroke-dasharray="2 5"/>',
         t(x0 + 240, 72, "창밖", 10, GREY, 700), t(x0 + 240, 112, outside, 11, NAVY, 700), t(x0 + 240, 130, outside_sub, 10, GREY)]
    if arrow_out_to_in:
        o.append(t(x0 + 240, 152, "화자", 10.5, BURG, 700))
        o.append(f'<line x1="{x0+240}" y1="176" x2="{x0+90}" y2="176" stroke="{BURG}" stroke-width="1.6" marker-end="url(#ah)"/>')
        o.append(t(x0 + 165, 199, "창밖에서 바라봄", 9, BURG))
    else:
        o.append(f'<line x1="{x0+87}" y1="176" x2="{x0+240}" y2="176" stroke="{BURG}" stroke-width="1.6" marker-end="url(#ah)"/>')
        o.append(t(x0 + 165, 199, "창 안에서 창밖을 봄", 9, BURG))
    return "".join(o)

def svg_mem():
    return ('<svg viewBox="0 0 680 250" class="fig"><defs><marker id="ah" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="' + BURG + '"/></marker></defs>'
            + panel(10, "1연 — 과거", "관공서 ‘춥고 큰 방’", "희미한 불빛", "캄캄한 거리", "눈이 퍼붓는다", "서기: 혼자 울고 있음", True)
            + panel(360, "2연 — 현재", "‘텅 빈 사무실’", "깊은 밤", "창밖", "눈이 퍼붓는다", "화자: 그를 떠올림", False)
            + t(340, 236, "창밖에서 바라보던 화자 → 이제 창 안(사내가 있던 자리)에 놓임 = 처지의 겹침", 11, BURG, 700)
            + '</svg>')

def box(x, y, w, h, title, lines, color):
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="#fff" stroke="{color}" stroke-width="1.3"/>',
         t(x + w / 2, y + 20, title, 11, color, 700)]
    for i, ln in enumerate(lines):
        o.append(t(x + w / 2, y + 34 + i * 13, ln, 9.4))
    return "".join(o)

def svg_kant():
    o = ['<svg viewBox="0 0 680 300" class="fig"><defs><marker id="ak" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#8a8f96"/></marker></defs>']
    for col, (x, name, sub, color, steps, verdict) in enumerate([
        (10, "현상계", "감각 경험으로 인식 · 모든 사건은 앞선 원인에 의해 필연적", NAVY,
         [("원인", ["감각적 욕구 등", "이성이 아닌 것"]), ("의지 규정", ["쾌 추구 ·", "불쾌 회피"]), ("행위", ["예: 배가 아파", "음식을 안 먹음"])], "타율적 행위"),
        (350, "예지계", "이성으로 사유될 뿐 경험적으로 인식되지 않음", BURG,
         [("원인", ["이성 — 도덕 법칙", "(준칙 + 보편성)"]), ("의지 규정", ["자기 입법:", "스스로 부과"]), ("행위 실천", ["예: 배고픔 참고", "음식 양보"])], "자유를 의식")]):
        o.append(f'<rect x="{x}" y="8" width="320" height="286" rx="12" fill="#faf9f6" stroke="#d6d8db"/>')
        o.append(t(x + 160, 32, name, 14, color, 700))
        o.append(t(x + 160, 50, sub, 9.5, GREY))
        for i, (h, ls) in enumerate(steps):
            yy = 62 + i * 68
            o.append(box(x + 60, yy, 200, 54, h, ls, color))
            o.append(f'<line x1="{x+160}" y1="{yy+54}" x2="{x+160}" y2="{yy+66}" stroke="#8a8f96" stroke-width="1.4" marker-end="url(#ak)"/>')
        o.append(f'<rect x="{x+85}" y="{62+3*68}" width="150" height="28" rx="14" fill="{color}"/>')
        o.append(t(x + 160, 62 + 3 * 68 + 19, verdict, 12, "#fff", 700))
    o.append('</svg>')
    return "".join(o)

def svg_hegel():
    o = ['<svg viewBox="0 0 680 250" class="fig"><defs><marker id="ag" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="' + BURG + '"/></marker></defs>']
    steps = [("가족", "기반: 사랑이라는 정서", "한계: 제도적 보장이 약함"),
             ("시민 사회", "기반: 권리·이익 추구, 각종 제도 수립", "한계: 이해관계 충돌 → 불안정"),
             ("국가", "기반: 국가의 법과 제도", "법적 보호 + 이해관계 조정 → 가장 구체화")]
    for i, (n, a, b) in enumerate(steps):
        x = 20 + i * 215; y = 170 - i * 60; h = 70 + i * 60
        col = [GREY, NAVY, BURG][i]
        o.append(f'<rect x="{x}" y="{y}" width="200" height="{h}" rx="8" fill="{["#f3f2ee", "#eef0f4", "#f7eeee"][i]}" stroke="{col}" stroke-width="1.4"/>')
        o.append(t(x + 100, y + 22, n, 13, col, 700))
        o.append(t(x + 100, y + 42, a, 9.4))
        o.append(t(x + 100, y + 58, b, 9.4, col, 700))
    o.append(f'<line x1="40" y1="28" x2="600" y2="28" stroke="{BURG}" stroke-width="1.6" marker-end="url(#ag)"/>')
    o.append(t(320, 20, "자유의 실현: 점점 더 안정적이고 지속 가능한 형태로 (앞 단계의 약점을 뒤 단계가 보완)", 10.5, BURG, 700))
    o.append('</svg>')
    return "".join(o)

SVGS = {"pal_space": svg_pal, "mem_space": svg_mem, "kant": svg_kant, "hegel": svg_hegel}

# ───────── 렌더 ─────────
def table(rows, cls="tbl"):
    h = [f'<table class="{cls}"><tr>' + "".join(f"<th>{c}</th>" for c in rows[0]) + "</tr>"]
    for r in rows[1:]:
        h.append("<tr>" + "".join(f'<td class="{"k" if j == 0 else ""}">{c}</td>' for j, c in enumerate(r)) + "</tr>")
    return "".join(h) + "</table>"

def flow(steps):
    parts = []
    for i, (a, b, c) in enumerate(steps):
        sub = "".join(f"<span>{x}</span>" for x in (b, c) if x)
        parts.append(f'<div class="fs"><b>{a}</b>{sub}</div>')
        if i < len(steps) - 1:
            parts.append('<div class="fa">→</div>')
    return '<div class="flow">' + "".join(parts) + "</div>"

def notes_poem(sections):
    out = []
    for head, sub, rows in sections:
        out.append(f'<div class="seg"><span class="segh">{head}</span><span class="segs">{sub}</span></div>')
        for (a, b), lines, note, star in rows:
            no = f"{a}" if a == b else f"{a}~{b}"
            text = "<br>".join(hl(l) for l in lines)
            out.append(f'<div class="nr{" star" if star else ""}"><div class="nno">{no}</div><div class="ntx">{text}</div><div class="nnote">{note}</div></div>')
    return "\n".join(out)

def notes_prose(sections):
    out = []
    for head, sub, rows in sections:
        out.append(f'<div class="seg"><span class="segh">{head}</span><span class="segs">{sub}</span></div>')
        for sent, note in rows:
            out.append(f'<div class="nr prose"><div class="ntx">{hl(sent)}</div><div class="nnote">{note}</div></div>')
    return "\n".join(out)

def block(b):
    h = [f'<section class="concept"><div class="chead"><span class="cid">{b["id"]}</span><span class="pri p{b["pri"]}">{b["pri"]}</span></div>',
         f'<h3 class="ctitle">{b["title"]}</h3>',
         f'<div class="one"><span class="lab">한 줄 정의</span>{b["one"]}</div>', b["body"]]
    if b.get("table"): h.append(table(b["table"]))
    if b.get("flow"): h.append(flow(b["flow"]))
    if b.get("svg"): h.append('<div class="figwrap">' + SVGS[b["svg"]]() + "</div>")
    h.append('<div class="must"><div class="lab">MUST</div><ul>' + "".join(f"<li>{m}</li>" for m in b["must"]) + "</ul></div>")
    if b["conf"]:
        h.append('<div class="conf"><div class="lab">CONFUSING</div>' + "".join(
            f'<div class="xo"><div class="x"><b>×</b>{x}</div><div class="o"><b>○</b>{o}</div></div>' for x, o in b["conf"]) + "</div>")
    h.append('<div class="exam"><div class="lab">EXAM CONNECTION</div><ul>' + "".join(f"<li>{e}</li>" for e in b["exam"]) + "</ul></div>")
    h.append(f'<div class="nlink">N° 연결 → {b["nlink"]}</div></section>')
    return "\n".join(h)

def chapter(no, title, author, key, notes_html, src_note):
    ov = "".join(f'<tr><th>{k}</th><td>{v}</td></tr>' for k, v in OVERVIEW[key])
    return (f'<section class="chapter"><div class="chno">CORE {no:02d}</div><h2 class="chtitle">{title}</h2><div class="chauth">{author}</div>'
            f'<div class="h4">작품 한눈에 보기</div><table class="ov">{ov}</table>'
            f'<div class="h4">원문 필기 <span class="h4s">{src_note}</span></div><div class="notes">{notes_html}</div>'
            f'<div class="h4">핵심 개념</div>' + "\n".join(block(b) for b in BLOCKS[key]) + "</section>")

CSS = open(HERE / "core.css", encoding="utf-8").read()

def build():
    p = [f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>ARC CORE 공통국어2</title><style>{CSS}</style></head><body>"]
    p.append("""<section class="cover"><div class="kicker">ARC CORE</div><div class="toprule"></div><div class="accent"></div>
<div class="covermain"><h1>공통국어2</h1><div class="covermeta"><strong>동북고등학교</strong><br>2학기 중간고사 대비 · 보충자료 4편 핵심 개념서</div>
<div class="works">정훈, 「탄궁가」<br>백석, 「팔원 - 서행시초3」<br>기형도, 「기억할 만한 지나침」<br>이행남, 「칸트의 도덕적 자율성으로부터 헤겔의 인륜적 자율성으로」</div></div>
<div class="year">2026</div><div class="series">CONCEPT CORE</div></section><section class="blankpage"></section>""")
    # 가이드
    maprows = [["작품", "반드시 잡을 축", "대표 함정"],
               ["「탄궁가」", "가난의 구체상 · 표현 효과 · 귀신 대목(발화 주체) · 체념적 수용", "귀신 말↔화자 말, 풍자↔자조, 극복·달관"],
               ["「팔원」", "관찰/전해 들음/추측 · 대비 이미지 · 절제된 연민 · 식민지 현실", "추측을 사실로, ‘어느 한 사람’ = 타인, 저항 의지"],
               ["「기억할 만한 지나침」", "회상 구조 · 창을 사이에 둔 자리 바꿈 · 떠나지 못함 · 14행 부정 표현", "‘지금’ = 그날, 위로함, 반어"],
               ["칸트·헤겔", "원인으로 판정(타율/자유) · 보편성 · 3단계 · 구체적/추상적 자유 · 비교", "겉모습 판정, 시민 사회 = 충돌 해소, 법 = 외적 강제"]]
    p.append(f"""<section class="guide"><div class="chno">GUIDE</div><h2 class="chtitle">이 책의 구성과 사용법</h2>
<div class="toc"><div><b>CORE 01</b> 정훈, 「탄궁가」</div><div><b>CORE 02</b> 백석, 「팔원」</div><div><b>CORE 03</b> 기형도, 「기억할 만한 지나침」</div><div><b>CORE 04</b> 칸트와 헤겔의 자유</div><div><b>CORE 05</b> 통합 정리 · 오답 패턴 · O/X 최종 점검</div></div>
<div class="h4">표기 약속</div>
<table class="legend"><tr><td><mark>하이라이트</mark></td><td>시험에 그대로 인용되는 핵심 구절</td></tr>
<tr><td><span class="ul">밑줄</span></td><td>함께 봐야 할 대비·연결 구절</td></tr>
<tr><td><span class="starbar">★ 행</span></td><td>출제 빈도가 높은 행(왼쪽 버건디 선)</td></tr>
<tr><td>⚠</td><td>선지에서 자주 뒤틀리는 부분</td></tr>
<tr><td><b class="navy">MUST</b> / <b class="burg">CONFUSING</b></td><td>반드시 기억할 것 / × 오답 진술과 ○ 바른 이해</td></tr>
<tr><td><b>EXAM CONNECTION</b></td><td>문항이 이 개념을 어떤 사고 과정으로 묻는가</td></tr>
<tr><td><b>N° 연결</b></td><td>ARC N°05~07에서 이 개념을 다룬 문항 번호 — 개념을 읽고 바로 풀어 볼 것</td></tr></table>
<div class="h4">한눈에 보는 출제 지도</div>{table(maprows)}
<p class="tip">공부 순서: ① 원문 필기를 원문 → 필기 순으로 읽고 ② 개념 블록의 MUST·CONFUSING을 소리 내어 정리한 뒤 ③ N° 연결 문항을 풀고 ④ 마지막 O/X로 점검한다. 틀린 문항은 해당 개념 블록으로 돌아와 CONFUSING부터 다시 본다.</p></section>""")
    p.append(chapter(1, "정훈, 「탄궁가」", "가사 · 가난에 대한 탄식에서 체념적 수용으로", "TAN", notes_poem(TAN_NOTES), "왼쪽 원문 · 오른쪽 필기 / 행 번호는 ARC N°과 동일"))
    p.append(chapter(2, "백석, 「팔원 - 서행시초3」", "자유시 · 식민지 현실 속 어린 계집아이에 대한 절제된 연민", "PAL", notes_poem(PAL_NOTES), "행 번호는 ARC N°과 동일"))
    p.append(chapter(3, "기형도, 「기억할 만한 지나침」", "자유시 · 우연히 목격한 타인의 울음과 훗날의 이해", "MEM", notes_poem(MEM_NOTES), "1연 1~11행 / 2연 12~14행"))
    p.append(chapter(4, "칸트와 헤겔의 자유", "이행남, 「칸트의 도덕적 자율성으로부터 헤겔의 인륜적 자율성으로」", "AUT", notes_prose(KANT_NOTES), "문장 단위 필기"))
    # 통합
    cross = "".join(f'<div class="crow"><b>{a}</b><span>{b}</span></div>' for a, b in CROSS)
    traps = [["패턴", "이렇게 비튼다", "주로 나오는 곳"]] + [list(x) for x in TRAPS]
    ox = "".join(f'<tr><td class="k">{i:02d}</td><td>{q}</td><td class="ans">{a}</td><td class="why">{w}</td></tr>' for i, (q, a, w) in enumerate(OX, 1))
    p.append(f"""<section class="chapter"><div class="chno">CORE 05</div><h2 class="chtitle">통합 정리</h2><div class="chauth">작품 간 비교 · 추가 자료 적용 · 문학×비문학 · 오답 패턴 · O/X</div>
<section class="concept"><div class="chead"><span class="cid">ARC-KOR-SUP-001</span><span class="pri p필수">필수</span></div><h3 class="ctitle">세 작품 비교 매트릭스</h3>
<div class="one"><span class="lab">한 줄 정의</span>세 시 모두 괴로움·슬픔을 지닌 인물이 나오지만, 「탄궁가」는 자기 고통의 토로, 「팔원」과 「기억할 만한 지나침」은 타인의 고통을 바라보는 시다.</div>
{table(COMPARE)}
<div class="must"><div class="lab">MUST</div><ul><li>세 작품 모두 결말에서 대상의 처지가 나아지기를 바라는 소망을 <b>직접</b> 드러내지 않는다.</li><li>「팔원」과 「기억할 만한 지나침」은 모두 <b>우연히 마주친 타인의 울음</b>을 목격하고, 모두 <b>유리창</b>이 등장한다(팔원: 우는 아이와 배웅하는 이 사이 / 기형도: 화자와 우는 사내 사이).</li></ul></div>
<div class="exam"><div class="lab">EXAM CONNECTION</div><ul><li>(가)~(다) 비교형: 공통점은 맞추고 한 작품의 사실만 뒤바꾼 선지를 찾는다.</li></ul></div>
<div class="nlink">N° 연결 → N05 17 / N06 17·24·30 / N07 30</div></section>
<section class="concept"><div class="chead"><span class="cid">ARC-KOR-SUP-002</span><span class="pri p필수">필수</span></div><h3 class="ctitle">학교 ‘추가 자료’ 적용표</h3>
<div class="one"><span class="lab">한 줄 정의</span>같은 &lt;보기&gt;를 두 작품에 대면, 「팔원」은 ‘관찰·추측·현실 확대’, 「기억할 만한 지나침」은 ‘동일시’ 쪽에 맞는다.</div>
<div class="quote">{EXTRA}<div class="qsrc">— 동북고 1학년 국어 중간고사 보충자료, ‘추가 자료’</div></div>
{table(EXTRA_MAP)}
<div class="nlink">N° 연결 → N06 20·25</div></section>
<section class="concept"><div class="chead"><span class="cid">ARC-KOR-SUP-003</span><span class="pri p이해">이해</span></div><h3 class="ctitle">문학 × 비문학 연계</h3>
<div class="one"><span class="lab">한 줄 정의</span>작품 속 행동을 비문학의 판단 기준에 대 보되, 작품에 없는 사실을 단정하지 않는다.</div>{cross}
<div class="nlink">N° 연결 → N06 40</div></section>
<section class="concept"><div class="chead"><span class="cid">ARC-KOR-SUP-004</span><span class="pri p필수">필수</span></div><h3 class="ctitle">오답 패턴 10</h3>
<div class="one"><span class="lab">한 줄 정의</span>오답은 ‘일부는 맞고 전체는 틀리게’ 만든다. 어디가 틀렸는지 한 문장으로 말할 수 있어야 한다.</div>{table(traps)}</section>
<section class="concept ox"><div class="chead"><span class="cid">FINAL CHECK</span></div><h3 class="ctitle">O/X 최종 점검 20</h3>
<table class="oxt"><tr><th>번호</th><th>진술</th><th>O/X</th><th>근거</th></tr>{ox}</table></section>
</section>""")
    p.append("</body></html>")
    return "\n".join(p)

if __name__ == "__main__":
    (HERE / "core.html").write_text(build(), encoding="utf-8")
    print("ok")

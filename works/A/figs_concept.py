import sys
sys.path.insert(0, "/home/user/ARC-System/works")
from figlib import *
from matplotlib.patches import Rectangle

OUT = "/home/user/ARC-System/works/A/fig/"
WW = 6.7
LH = 4.55   # 줄 간격(데이터 단위)


def nlines(s):
    return s.count("\n") + 1


def draw_node(ax, x, ytop, w, h, title, body, qs, fs=6.8, tfs=7.4):
    ax.add_patch(Rectangle((x, ytop - h), w, h, fc="white", ec=G1, lw=0.7, zorder=2))
    ax.text(x + 1.6, ytop - 1.6, title, ha="left", va="top", fontsize=tfs, fontweight="bold", color=NAVY, zorder=3)
    ax.text(x + 1.6, ytop - 7.2, body, ha="left", va="top", fontsize=fs, color=G1, linespacing=1.5, zorder=3)
    ax.text(x + w - 1.4, ytop - h + 1.4, qs, ha="right", va="bottom", fontsize=6.4, color=BURG, fontweight="bold", zorder=3)


def stack(items, head, figh):
    f, ax = plt.subplots(figsize=(WW, figh))
    total = 6 + sum(it["h"] + 3 for it in items) + 8
    ax.set_xlim(-0.5, 100.5); ax.set_ylim(0, total); ax.axis("off")
    ax.text(0, total - 1, head, fontsize=8.4, fontweight="bold", color=NAVY, va="top")
    ax.plot([0, 100], [total - 6, total - 6], color=NAVY, lw=0.9)
    y = total - 9
    for it in items:
        if it["kind"] == "pair":
            for k, nd in enumerate(it["nodes"]):
                draw_node(ax, k * 51, y, 49, it["h"], **nd)
        elif it["kind"] == "full":
            draw_node(ax, 0, y, 100, it["h"], **it["node"])
        else:
            it["draw"](ax, y, it["h"])
        y -= it["h"] + 3
    return f, ax


def h_of(*bodies, extra=0):
    return 8 + max(nlines(b) for b in bodies) * LH + 5 + extra


def table_dist(ax, ytop, h):
    ax.add_patch(Rectangle((0, ytop - h), 100, h, fc="white", ec=G1, lw=0.7, zorder=2))
    ax.text(1.6, ytop - 1.6, "분배의 실질적 기준 — 능력 · 업적 · 필요", fontsize=7.4, fontweight="bold", color=NAVY, va="top")
    ax.text(98.6, ytop - h + 1.4, "Q 09 10 11 12 13 14 15 24 25", fontsize=6.4, color=BURG, fontweight="bold", ha="right", va="bottom")
    cols = [1.6, 9, 33, 57, 79]   # 기준 / 분배의 근거 / 장점 / 단점 / 사례
    heads = ["기준", "분배의 근거", "장점", "단점", "사례"]
    yy = ytop - 8
    for c, t in zip(cols, heads):
        ax.text(c, yy, t, fontsize=6.6, fontweight="bold", va="top", color=G2)
    ax.plot([1, 99], [yy - 4.2, yy - 4.2], color=G3, lw=0.5)
    rows = [
        ("능력", "잠재력·재능,\n성장 가능성이 큰 사람", "잠재력을 실현할\n기회 제공", "우연적 요소, 결과 전\n객관적 평가 곤란", "수능·내신 선발,\n국가고시"),
        ("업적", "성취한 결과에 비례", "동기 부여,\n객관화·수량화 쉬움", "약자 배려 부족,\n과열 경쟁", "노벨상, 올림픽\n연금, 유공자 포상"),
        ("필요", "기본적 필요 충족이\n어려운 사회적 약자", "최대한 많은 사람이\n인간다운 삶", "자원 부족, 성취\n동기 약화", "기초생활수급,\n재난지원금"),
    ]
    yy -= 6
    for r in rows:
        ax.text(cols[0], yy, r[0], fontsize=6.9, fontweight="bold", va="top", color=NAVY)
        for c, t in zip(cols[1:], r[1:]):
            ax.text(c, yy, t, fontsize=6.3, va="top", color=G1, linespacing=1.4)
        yy -= 9.4


def table_pun(ax, ytop, h):
    ax.add_patch(Rectangle((0, ytop - h), 100, h, fc="white", ec=G1, lw=0.7, zorder=2))
    ax.text(1.6, ytop - 1.6, "교정적 정의와 사형제 논쟁 — 칸트 vs 베카리아", fontsize=7.4, fontweight="bold", color=NAVY, va="top")
    ax.text(98.6, ytop - h + 1.4, "Q 16 17 18 19 20 21 23", fontsize=6.4, color=BURG, fontweight="bold", ha="right", va="bottom")
    ax.text(30, ytop - 9, "칸트 (응보주의)", fontsize=6.9, fontweight="bold", ha="center", va="top", color=G2)
    ax.text(72, ytop - 9, "베카리아 (공리주의)", fontsize=6.9, fontweight="bold", ha="center", va="top", color=G2)
    ax.plot([1, 99], [ytop - 13.4, ytop - 13.4], color=G3, lw=0.5)
    rows = [
        ("근거", "범죄를 저질렀기 때문에\n(다른 선의 수단 아님)", "사회적 이익의 증진"),
        ("강도", "동등성의 원칙", "새 해악 방지·타인의 범죄 억제에\n충분한 정도까지만"),
        ("사형", "고통받는 인격을 해방하여\n인간의 존엄성을 실현", "한순간의 인상뿐, 종신 노역형이 더 큰 공포\n국가의 전쟁, 법을 빙자한 살인"),
        ("인격·계약", "시민적 인격성을 잃어도\n생득적 인격성은 유지", "생명을 빼앗을 권능을 양도(사회 계약)\n할 사람은 없다"),
    ]
    yy = ytop - 15.5
    for lab, k, b in rows:
        ax.text(1.6, yy, lab, fontsize=6.6, fontweight="bold", va="top", color=NAVY)
        ax.text(14, yy, k, fontsize=6.3, va="top", color=G1, linespacing=1.4)
        ax.text(51, yy, b, fontsize=6.3, va="top", color=G1, linespacing=1.4)
        yy -= 9.4
    ax.text(1.6, yy + 0.6, "※ 범죄자 처벌·손해배상은 교정적 정의(산술적 비례)의 영역이며, 스페셜 트랙에서 심화한다.", fontsize=6.3, va="top", color=G2)


def cA():
    n = lambda **k: k
    items = [
        dict(kind="pair", h=h_of("a\nb\nc\nd"), nodes=[
            n(title="불평등 → 평등 → 형평성 → 정의", body="평등: 차별 요소를 없애 똑같이 대우(사정 미고려)\n형평성: 출발점·필요를 인식하고 해결\n정의: 불평등의 장벽 자체를 제도적으로 개혁", qs="Q 01 02 26"),
            n(title="아리스토텔레스의 정의", body="‘같은 것은 같게, 다른 것은 다르게’\n일반적 정의(법 준수·공익)\n특수적 정의: 분배(기하학적 비례)·교정\n(산술적 비례)·교환(같은 가치의 교환)", qs="Q 03 04 05 07 22")]),
        dict(kind="pair", h=h_of("a\nb\nc\nd"), nodes=[
            n(title="정의가 요청되는 이유", body="기본권 보장 — 인간다운 삶의 권리\n갈등 조정 — 이해관계 충돌의 조정\n사회 통합 — 동등한 대우에 대한 신뢰와 협력", qs="Q 06 24"),
            n(title="분배·교정·교환 유형의 적용", body="성과·기여에 비례해 나눔 → 분배적(기하학적 비례)\n손해·불공정 계약을 바로잡음 → 교정적(산술적 비례)\n같은 가치의 물건·노동과 임금 → 교환적", qs="Q 03 04 05 08")]),
        dict(kind="draw", h=48, draw=table_dist),
        dict(kind="draw", h=61, draw=table_pun),
    ]
    f, ax = stack(items, "Ⅰ. 정의의 의미와 필요성 · 정의의 실질적 기준", 8.4)
    save(f, OUT + "C_A.svg")


def cA2():
    n = lambda **k: k
    items = [
        dict(kind="pair", h=h_of("a\nb\nc"), nodes=[
            n(title="논리 vs 경험 (CH6)", body="형식 논리·비모순 vs 경험·맥락\n전형성, 결론의 그럴듯함이 타당성 판단에 영향\n→ 능력의 우열이 아니라 사고 습관의 차이", qs="Q 27 28 36"),
            n(title="Either/Or vs Both/And", body="변증법의 세 원리: 변화 · 모순 · 연관성\n갈등 해결·상반된 연구·절충안·상반된 정서\n→ 중용·타협, 모순의 동시 수용", qs="Q 29 30 31 32 33 34 35")]),
        dict(kind="full", h=h_of("a\nb\nc"), node=n(title="사고 방식의 기원 (CH7)", body="생태 ↔ 경제 ↔ 사회 구조 ↔ 주의 방식 ↔ 형이상학 ↔ 인식론 ↔ 사고 과정  (화살표는 상호작용, 결정론 아님)\n고대 중국: 협동 농업·중앙집권·조화 → 관계·맥락·전체 중시\n고대 그리스: 교역·이동·논쟁·자율성 → 대상 속성·범주·형식 논리\n장의존성(배경의 영향)·장독립성 — 생업과 사회적 제약이 영향", qs="Q 37 38 39 40 41", fs=6.6)),
        dict(kind="full", h=h_of("a\nb\nc\nd"), node=n(title="실생활 속 차이와 각 사고의 장·단점 (CH8)", body="의학(부위 분리·직접 개입 vs 몸 전체의 균형) · 법(승패 판정 vs 조정) · 계약(고정 vs 재협상) · 기업(공개 논쟁 vs 사전 합의)\n국제 사건(단일 직접 원인 vs 복합·관계적 원인) · 귀인 오류(행위자의 성격 vs 상황) · 인권(사회계약 vs 유기적 관계)\n과학: 단순하고 검증 가능한 가설·공개 논쟁 ↔ 복잡성·맥락의 이해 — 두 사고는 서로의 오류를 교정하는 보완 관계", qs="Q 42 43 44 45 46 48 49", fs=6.4)),
        dict(kind="pair", h=h_of("a\nb\nc\nd"), nodes=[
            n(title="지능 검사의 문화 편향", body="비언어 검사도 문화 중립이 아님\n한 검사의 결과를 집단의 지능으로 일반화 금지\n집단 평균을 개인에게 적용 금지", qs="Q 47"),
            n(title="미래 전망과 이중문화 프라이밍", body="서구화·수렴 / 차이 지속(근대화≠서구화)\n/ 상호 수렴·혼합\n이미지·대명사 프라이밍으로 사고 방식이\n상황에 따라 전환될 수 있음", qs="Q 41 50")]),
    ]
    f, ax = stack(items, "Ⅱ. 『생각의 지도』 p.156~233 — 동양과 서양의 사고 방식", 6.6)
    save(f, OUT + "C_A2.svg")


def cS():
    f, ax = plt.subplots(figsize=(WW, 5.9))
    ax.set_xlim(-0.5, 100.5); ax.set_ylim(0, 106); ax.axis("off")
    ax.text(0, 105, "칸트 vs 베카리아 — 사형 논쟁 핵심 대비", fontsize=8.4, fontweight="bold", color=NAVY, va="top")
    ax.plot([0, 100], [99, 99], color=NAVY, lw=0.9)
    ax.text(31.5, 94, "칸트 (응보주의)", ha="center", fontsize=7.6, fontweight="bold", color=NAVY)
    ax.text(76, 94, "베카리아 (공리주의)", ha="center", fontsize=7.6, fontweight="bold", color=NAVY)
    rows = [
        ("형벌의 정당화\n근거", "범죄를 저질렀기 때문에\n(다른 선을 위한 수단이 아님)", "사회적 이익의 증진", "Q 01 02 03 05 19"),
        ("형벌 강도의\n기준", "동등성의 원칙", "새 해악 방지·타인의 범죄 억제에\n충분한 정도까지만", "Q 09 11 17 20"),
        ("사형에 대한\n평가", "고통받는 인격을 해방하여\n인간의 존엄성을 실현", "한순간의 인상뿐, 종신 노역형이 더 큰 공포\n국가의 전쟁, 법을 빙자한 살인", "Q 07 12 13"),
        ("인격·계약의\n관점", "시민적 인격성을 잃어도\n생득적 인격성은 유지", "자신의 생명을 빼앗을 권능을\n양도(사회 계약)할 사람은 없다", "Q 08 10 15"),
    ]
    y = 90
    for lab, k, b, q in rows:
        ax.text(0, y - 7.5, lab, fontsize=6.7, fontweight="bold", va="center", color=G1, linespacing=1.3)
        box(ax, 15, y - 15, 33, 15, k, fs=6.4, fc="white")
        box(ax, 51, y - 15, 49, 15, b, fs=6.4, fc="white")
        ax.text(100, y - 17.2, q, ha="right", fontsize=6.2, color=BURG, fontweight="bold", va="center")
        y -= 20.5
    ax.text(0, 5.5, "공통 · 연결   범죄자 처벌은 교정적 정의(산술적 비례)의 영역 (Q 15 20)\n두 사상가는 서로 다른 ‘근거’에서 출발하며, 결론이 같아도 근거는 다를 수 있다 (Q 14 17)", fontsize=6.4, va="center", color=G1, linespacing=1.6)
    save(f, OUT + "C_S.svg")


if __name__ == "__main__":
    cA(); cA2(); cS(); print("ok")

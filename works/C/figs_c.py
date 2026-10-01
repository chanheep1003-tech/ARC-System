import sys
sys.path.insert(0, "/home/user/ARC-System/works")
from figlib import *
import numpy as np
from matplotlib.patches import Rectangle, Polygon, FancyBboxPatch, Circle

OUT = "/home/user/ARC-System/works/C/fig/"


def canvas(h, xmax=100, ymax=None, w=W):
    f, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xmax); ax.set_ylim(0, ymax if ymax else h * 30); ax.axis("off")
    return f, ax


def tag(ax, x, y, s, r=3.6, fs=6.8, fc="white", ec=NAVY):
    ax.add_patch(Circle((x, y), r, fc=fc, ec=ec, lw=0.9, zorder=4))
    ax.text(x, y, s, ha="center", va="center", fontsize=fs, fontweight="bold", color=ec, zorder=5)


# ---------------------------------------------------------------- CM03 인권의 발달
def cm03():
    f, ax = canvas(2.15, 100, 100)
    ax.annotate("", xy=(3.6, 2), xytext=(3.6, 98), arrowprops=dict(arrowstyle="-|>", lw=0.9, color=G2, mutation_scale=7))
    ax.text(0.2, 100, "시간", fontsize=6.3, color=G2, va="bottom")
    rows = [
        ("(가)", "18~19세기", "시민 혁명기",
         "왕과 국가 권력의 간섭에서 벗어나\n개인의 자유를 지키려는 요구가 커짐",
         "대표 문서: 미국 독립 선언,\n프랑스 인권 선언"),
        ("(나)", "20세기 초", "산업화 이후",
         "빈곤과 불평등을 해소하기 위해\n국가의 적극적인 역할을 요구함",
         "대표 문서: 바이마르 헌법"),
        ("(다)", "20세기 후반 이후", "지구촌 시대",
         "환경·평화·빈곤 등 지구촌 문제의\n해결을 위해 국가와 집단 사이의\n연대를 요구함",
         ""),
    ]
    y = 97
    for t, era, nm, body, doc in rows:
        h = 30
        tag(ax, 3.6, y - h / 2, t, r=3.3, fs=6.2)
        ax.add_patch(Rectangle((10, y - h), 26, h, fc=G5, ec=G1, lw=0.7, zorder=2))
        ax.text(23, y - h / 2, era + "\n" + nm, ha="center", va="center", fontsize=6.2, fontweight="bold", color=NAVY, linespacing=1.4, zorder=3)
        ax.add_patch(Rectangle((36, y - h), 64, h, fc="white", ec=G1, lw=0.7, zorder=2))
        txt = body + ("\n" + doc if doc else "")
        ax.text(38, y - h / 2, txt, ha="left", va="center", fontsize=5.9, color=G1, linespacing=1.55, zorder=3)
        y -= h + 2
    save(f, OUT + "CM03.svg")


# ---------------------------------------------------------------- CM11 연표
def cm11():
    f, ax = canvas(1.25, 100, 50)

    def X(yr):
        return 1.5 + (yr - 1200) / 500 * 9 if yr < 1700 else 10.5 + (yr - 1700) / 260 * 85
    y0 = 22
    ax.plot([1.5, 98], [y0, y0], color=G1, lw=1.0, zorder=1)
    ax.annotate("", xy=(99.5, y0), xytext=(96, y0), arrowprops=dict(arrowstyle="-|>", lw=1.0, color=G1, mutation_scale=7))
    # 축 생략 표시
    bx = 6.0
    ax.plot([bx - 0.8, bx + 0.0], [y0 - 3.2, y0 + 3.2], color=G1, lw=0.8, zorder=3)
    ax.plot([bx + 0.6, bx + 1.4], [y0 - 3.2, y0 + 3.2], color=G1, lw=0.8, zorder=3)
    ax.add_patch(Rectangle((bx - 0.3, y0 - 1.2), 1.4, 2.4, fc="white", ec="none", zorder=2))
    pts = [("(가)", 1215, 1), ("(나)", 1789, 1), ("(다)", 1838, -1), ("(라)", 1919, 1), ("(마)", 1948, -1)]
    for t, yr, up in pts:
        x = X(yr)
        ax.plot([x, x], [y0, y0 + up * 6.5], color=G3, lw=0.6, zorder=1)
        tag(ax, x, y0 + up * 10.2, t, r=3.7, fs=6.2)
        ax.plot([x], [y0], "o", ms=3.6, mfc="white", mec=G1, mew=0.9, zorder=4)
        ax.text(x, y0 - up * 4.2 - (1.5 if up < 0 else 0) + (0 if up > 0 else 0), "%d" % yr, ha="center",
                va="top" if up > 0 else "bottom", fontsize=5.9, color=G2)
    # (다)·(마)는 아래에 있으므로 연도는 위쪽
    save(f, OUT + "CM11.svg")


# ---------------------------------------------------------------- CM16 잊힐 권리
def cm16():
    f, ax = plt.subplots(figsize=(W, 2.05))
    yrs = ["2019", "2020", "2021", "2022", "2023"]
    req = [12, 18, 25, 33, 40]; rate = [35, 42, 48, 55, 61]
    b = ax.bar(yrs, req, color=G4, ec=G1, lw=0.7, width=0.55, zorder=2)
    for r in b:
        ax.text(r.get_x() + r.get_width() / 2, r.get_height() / 2, "%d" % r.get_height(), ha="center", va="center", fontsize=6.6, color=G1)
    ax.set_ylim(0, 52); ax.set_ylabel("삭제 요청 건수(천 건)", fontsize=6.3)
    ax.tick_params(axis="both", labelsize=6.3)
    ax2 = ax.twinx(); ax2.spines["right"].set_visible(True)
    ax2.plot(yrs, rate, marker="o", ms=3.6, color=BURG, lw=1.1, mfc="white", mew=0.9, zorder=5)
    for x, v in zip(yrs, rate):
        ax2.text(x, v + 4.2, "%d" % v, ha="center", fontsize=6.3, color=BURG, fontweight="bold")
    ax2.set_ylim(0, 80); ax2.set_ylabel("수용률(%)", fontsize=6.3, color=BURG)
    ax2.tick_params(axis="y", labelsize=6.3, colors=BURG)
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(fc=G4, ec=G1, label="삭제 요청 건수(왼쪽)"), Line2D([], [], color=BURG, marker="o", mfc="white", ms=3.6, label="수용률(오른쪽)")],
              loc="upper left", fontsize=6.0, frameon=False, ncol=1, bbox_to_anchor=(0.0, 1.0))
    save(f, OUT + "CM16.svg")


# ---------------------------------------------------------------- CM21 기본권 체계
def cm21():
    f, ax = canvas(2.1, 100, 100)
    ax.set_ylim(14, 100)
    box(ax, 4, 84, 92, 14, "제10조  인간으로서의 존엄과 가치, 행복 추구권\n(기본권 전반의 이념적 기초)", fc=G5, fs=6.6, bold=True, tc=NAVY)
    specs = [("(가)", "제12조", "신체의 자유"), ("(나)", "제11조", "법 앞에 평등,\n차별 금지"), ("(다)", "제24조", "선거권"),
             ("(라)", "제34조", "인간다운 생활을\n할 권리"), ("(마)", "제29조", "국가 배상 청구")]
    xs = [2, 35, 68]
    ys = [47, 18]
    pos = [(xs[0], ys[0]), (xs[1], ys[0]), (xs[2], ys[0]), (xs[0], ys[1]), (xs[1], ys[1])]
    ax.plot([50, 50], [84, 78], color=G1, lw=0.8)
    ax.plot([17, 84], [78, 78], color=G1, lw=0.8)
    for (t, art, nm), (x, y) in zip(specs, pos):
        w = 30; h = 24
        if y == ys[0]:
            ax.plot([x + w / 2, x + w / 2], [78, y + h], color=G1, lw=0.8)
        ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=G1, lw=0.7, zorder=2))
        ax.text(x + 2, y + h - 2.2, t, fontsize=6.6, fontweight="bold", color=NAVY, va="top", zorder=3)
        ax.text(x + w / 2, y + h / 2 - 2, art + "\n" + nm, ha="center", va="center", fontsize=6.3, color=G1, linespacing=1.3, zorder=3)
    # 아래 행 연결선
    ax.plot([17, 17], [47, 42], color=G1, lw=0.8); ax.plot([50, 50], [47, 42], color=G1, lw=0.8)
    ax.plot([17, 50], [42, 42], color=G3, lw=0.0)
    # (라),(마)는 위 행의 (가),(나) 아래쪽에 세로선으로 연결
    for x in (xs[0] + 15, xs[1] + 15):
        ax.plot([x, x], [47, 42], color=G1, lw=0.8)
    ax.add_patch(Rectangle((xs[2], ys[1]), 30, 24, fc="white", ec=G1, lw=0.9, ls=(0, (3, 2)), zorder=2))
    ax.text(xs[2] + 15, ys[1] + 12, "헌법에 열거되지\n않은 자유와 권리\n(제37조 제1항)", ha="center", va="center", fontsize=6.2, color=G1, linespacing=1.35)
    save(f, OUT + "CM21.svg")


# ---------------------------------------------------------------- CM31 기본권 제한 판단 흐름도
def cm31():
    f, ax = canvas(3.3, 100, 100)
    steps = [("(가)", "제한의 목적이 국가 안전 보장·\n질서 유지·공공복리에 해당하는가?"),
             ("(나)", "국회가 제정한 법률에 근거하는가?"),
             ("(다)", "목적 달성에 필요한 범위를\n넘지 않는가?"),
             ("(라)", "자유와 권리의 본질적인 내용을\n침해하지 않는가?")]
    box(ax, 12, 93, 44, 6.5, "기본권 제한 조치", fc=G5, fs=6.6, bold=True, tc=NAVY)
    y = 93
    hh = 13.5; gap = 7.5
    for i, (t, q) in enumerate(steps):
        ytop = y - gap
        ax.annotate("", xy=(34, ytop), xytext=(34, y), arrowprops=dict(arrowstyle="-|>", lw=0.8, color=G1, mutation_scale=6))
        ax.text(36, y - gap / 2, "예", fontsize=6.0, va="center", color=G1)
        ax.add_patch(Rectangle((2, ytop - hh), 64, hh, fc="white", ec=G1, lw=0.7, zorder=2))
        ax.text(4, ytop - hh / 2, t, fontsize=6.6, fontweight="bold", color=NAVY, va="center")
        ax.text(13, ytop - hh / 2, q, fontsize=6.2, color=G1, va="center", linespacing=1.35)
        ax.annotate("", xy=(78, ytop - hh / 2), xytext=(66, ytop - hh / 2), arrowprops=dict(arrowstyle="-|>", lw=0.8, color=BURG, mutation_scale=6))
        ax.text(72, ytop - hh / 2 + 1.6, "아니요", fontsize=5.4, color=BURG, ha="center", va="bottom")
        ax.add_patch(Rectangle((78, ytop - hh / 2 - 5), 21, 10, fc="white", ec=BURG, lw=0.8, zorder=2))
        ax.text(88.5, ytop - hh / 2, "한계를 벗어남", fontsize=5.9, color=BURG, ha="center", va="center", fontweight="bold")
        y = ytop - hh
    ax.annotate("", xy=(34, y - gap), xytext=(34, y), arrowprops=dict(arrowstyle="-|>", lw=0.8, color=G1, mutation_scale=6))
    ax.text(36, y - gap / 2, "예", fontsize=6.0, va="center", color=G1)
    box(ax, 12, y - gap - 6.5, 44, 6.5, "모든 한계를 충족함", fc=G5, fs=6.4, bold=True, tc=NAVY)
    ax.set_ylim(y - gap - 12, 100)
    ax.text(99, y - gap - 10.5, "※ 위에서부터 차례로 판단하며, ‘아니요’가 나오면 그 단계에서 판단을 마친다.",
            ha="right", fontsize=5.4, color=G2)
    save(f, OUT + "CM31.svg")


# ---------------------------------------------------------------- CM37 의석 비율
def cm37():
    f, ax = plt.subplots(figsize=(W, 1.95))
    lab = ["제1회", "제2회", "제3회", "제4회"]
    A = [55, 42, 38, 34]; B = [35, 44, 40, 46]; C = [10, 14, 22, 20]
    x = np.arange(4)
    ax.bar(x, A, 0.52, color=G1, ec=G1, label="A당", zorder=2)
    ax.bar(x, B, 0.52, bottom=A, color=G3, ec=G1, lw=0.6, label="B당", zorder=2)
    ax.bar(x, C, 0.52, bottom=[a + b for a, b in zip(A, B)], color="white", ec=G1, lw=0.6, label="C당", zorder=2)
    for i in range(4):
        ax.text(i, A[i] / 2, "%d" % A[i], ha="center", va="center", color="white", fontsize=6.6, fontweight="bold")
        ax.text(i, A[i] + B[i] / 2, "%d" % B[i], ha="center", va="center", color=G1, fontsize=6.6)
        ax.text(i, A[i] + B[i] + C[i] / 2, "%d" % C[i], ha="center", va="center", color=G1, fontsize=6.6)
    ax.axhline(50, color=BURG, lw=0.8, ls=(0, (3, 2)), zorder=4)
    ax.set_xlim(-0.6, 3.85)
    ax.text(3.33, 51, "과반", fontsize=6.0, color=BURG, ha="left", va="bottom", fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(lab, fontsize=6.6)
    ax.set_ylim(0, 100); ax.set_ylabel("의석 비율(%)", fontsize=6.3); ax.tick_params(axis="y", labelsize=6.2)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.17), ncol=3, fontsize=6.2, frameon=False, handlelength=1.2)
    save(f, OUT + "CM37.svg")


# ---------------------------------------------------------------- CM38 권력 분립 개념도
def cm38():
    f, ax = canvas(2.3, 100, 100)
    ax.set_ylim(-8, 100)
    specs = [((50, 84), "(가)", "법률을 만든다"), ((15, 18), "(나)", "법률을 집행한다"), ((85, 18), "(다)", "법을 적용하여\n재판한다")]
    for (cx, cy), t, s_ in specs:
        ax.add_patch(Rectangle((cx - 16, cy - 10), 32, 20, fc=G5, ec=G1, lw=0.8, zorder=3))
        ax.text(cx - 14, cy + 6.6, t, fontsize=6.8, fontweight="bold", color=NAVY, va="center", zorder=4)
        ax.text(cx, cy - 3.0, s_, fontsize=6.5, color=G1, ha="center", va="center", zorder=4, linespacing=1.3)
    def two(p, q, off=2.6):
        (x1, y1), (x2, y2) = p, q
        dx, dy = x2 - x1, y2 - y1
        n = (dx * dx + dy * dy) ** 0.5
        nx, ny = -dy / n, dx / n
        for sgn, (a_, b_) in ((1, (p, q)), (-1, (q, p))):
            s0 = (a_[0] + nx * off * sgn, a_[1] + ny * off * sgn)
            s1 = (b_[0] + nx * off * sgn, b_[1] + ny * off * sgn)
            ax.annotate("", xy=s1, xytext=s0, arrowprops=dict(arrowstyle="-|>", lw=0.9, color=G2, mutation_scale=7, shrinkA=0, shrinkB=0))
    # 끝점 조정
    two((42, 74), (17, 29)); two((58, 74), (83, 29)); two((33, 18), (67, 18))
    ax.add_patch(Rectangle((36, 30), 28, 13, fc="white", ec=BURG, lw=0.9, zorder=5))
    ax.text(50, 36.5, "서로 견제하고\n균형을 이룸", ha="center", va="center", fontsize=6.4, fontweight="bold", color=BURG, linespacing=1.3, zorder=6)
    ax.text(50, -5, "국가 권력을 나누는 목적: 권력의 집중과 남용을 막음", ha="center", fontsize=6.0, color=G2, va="center")
    save(f, OUT + "CM38.svg")


# ---------------------------------------------------------------- CM43 위헌 법률 심판 절차도
def cm43():
    f, ax = canvas(2.55, 100, 100)
    box(ax, 10, 88, 80, 11, "법원의 재판 진행 중, 적용할 법률이 헌법에\n위반되는지 의심됨 (재판의 전제)", fc=G5, fs=6.3, tc=G1)
    ys = [72, 54, 36]
    txt = [("(가)", "위헌 여부 심판 제청 신청 또는 직권"), ("(나)", "법원이 헌법재판소에 위헌 여부 심판을 제청"), ("(다)", "헌법재판소의 심판")]
    prev = 88
    for (t, s), y in zip(txt, ys):
        ax.annotate("", xy=(50, y + 11), xytext=(50, prev), arrowprops=dict(arrowstyle="-|>", lw=0.9, color=G1, mutation_scale=7))
        ax.add_patch(Rectangle((10, y), 80, 11, fc="white", ec=G1, lw=0.8, zorder=2))
        ax.text(14, y + 5.5, t, fontsize=6.8, fontweight="bold", color=NAVY, va="center")
        ax.text(26, y + 5.5, s, fontsize=6.3, color=G1, va="center")
        prev = y
    ax.annotate("", xy=(25, 20), xytext=(25, 36), arrowprops=dict(arrowstyle="-|>", lw=0.9, color=BURG, mutation_scale=7))
    ax.annotate("", xy=(75, 20), xytext=(75, 36), arrowprops=dict(arrowstyle="-|>", lw=0.9, color=G1, mutation_scale=7))
    ax.text(27, 28, "위헌 결정", fontsize=6.0, color=BURG, va="center", fontweight="bold")
    ax.text(77, 28, "합헌 결정", fontsize=6.0, color=G1, va="center", fontweight="bold")
    box(ax, 2, 4, 46, 16, "그 법률은\n효력을 잃음", fc="white", ec=BURG, fs=6.3, tc=BURG)
    box(ax, 52, 4, 46, 16, "법원이 그 법률을\n적용하여 재판을 계속함", fc="white", fs=6.3)
    save(f, OUT + "CM43.svg")


# ---------------------------------------------------------------- CM46 정치 참여 경험 비율
def cm46():
    f, ax = plt.subplots(figsize=(W, 2.1))
    m = ["투표", "시민 단체 활동", "청원·입법 의견 제시", "공청회 참여", "정당 활동"]
    a = [65, 8, 6, 5, 7]; b = [71, 15, 18, 8, 6]
    y = np.arange(len(m))[::-1]
    h = 0.34
    r1 = ax.barh(y + h / 2, a, h, color="white", ec=G1, lw=0.7, label="2015년", zorder=2)
    r2 = ax.barh(y - h / 2, b, h, color=G1, ec=G1, lw=0.7, label="2023년", zorder=2)
    for yy, v in zip(y + h / 2, a):
        ax.text(v + 1.2, yy, "%d" % v, va="center", fontsize=6.3)
    for yy, v in zip(y - h / 2, b):
        ax.text(v + 1.2, yy, "%d" % v, va="center", fontsize=6.3, fontweight="bold")
    ax.set_yticks(y); ax.set_yticklabels(m, fontsize=6.5)
    ax.set_xlim(0, 82); ax.set_xlabel("경험 비율(%)", fontsize=6.3); ax.tick_params(axis="x", labelsize=6.2)
    ax.legend(loc="lower right", fontsize=6.2, frameon=False)
    save(f, OUT + "CM46.svg")


if __name__ == "__main__":
    for fn in (cm03, cm11, cm16, cm21, cm31, cm37, cm38, cm43, cm46):
        fn()
    print("ok")

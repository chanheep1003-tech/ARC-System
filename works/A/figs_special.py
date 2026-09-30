import sys
sys.path.insert(0, "/home/user/ARC-System/works")
from figlib import *
import numpy as np
from matplotlib.patches import Circle, Rectangle, Ellipse, Polygon

OUT = "/home/user/ARC-System/works/A/fig/"


def b03():
    f, ax = plt.subplots(figsize=(W, 2.5))
    ax.set_xlim(0, 100); ax.set_ylim(0, 84); ax.axis("off")
    # 축 라벨
    ax.text(68, 80.5, "형벌의 정당화 근거", ha="center", fontsize=6.8, fontweight="bold", color=NAVY)
    ax.text(48, 73, "범죄를 저질렀다는 사실\n(응보)", ha="center", va="center", fontsize=6.2)
    ax.text(88, 73, "사회적 이익의 증진", ha="center", va="center", fontsize=6.2)
    ax.text(6, 62, "사형에\n대한 태도", ha="center", va="center", fontsize=6.8, fontweight="bold", color=NAVY)
    ax.text(22, 48, "찬성", ha="center", va="center", fontsize=6.4)
    ax.text(22, 14, "반대", ha="center", va="center", fontsize=6.4)
    box(ax, 28, 30, 40, 30, "(가)", fs=7.5, fc="white")
    box(ax, 68, 30, 40, 30, "(나)", fs=7.5, fc="white")
    box(ax, 28, 0, 40, 30, "(다)", fs=7.5, fc="white")
    box(ax, 68, 0, 40, 30, "(라)", fs=7.5, fc="white")
    ax.set_xlim(0, 108)
    save(f, OUT + "B03.svg")


def b06():
    f, ax = plt.subplots(figsize=(W, 2.7))
    ax.set_xlim(0, 100); ax.set_ylim(0, 78); ax.axis("off"); ax.set_aspect("equal")
    ax.add_patch(Ellipse((33, 37), 66, 68, fc="none", ec=G1, lw=0.9))
    ax.add_patch(Ellipse((67, 37), 66, 68, fc="none", ec=G1, lw=0.9))
    ax.text(15, 75.5, "칸트", ha="center", fontsize=7.6, fontweight="bold", color=NAVY)
    ax.text(85, 75.5, "베카리아", ha="center", fontsize=7.6, fontweight="bold", color=NAVY)
    kw = dict(ha="center", va="center", fontsize=5.7, linespacing=1.3)
    ax.text(16, 50, "(가) 동등성의\n원칙에 따른\n응보적 처벌", **kw)
    ax.text(16, 24, "(다) 처벌은\n사회적 이익을\n증진하는 수단", **kw)
    ax.text(50, 50, "(라) 범죄자\n처벌 문제를\n다룸", **kw)
    ax.text(50, 24, "(바) 형벌의\n강도에 대한\n기준을 제시함", **kw)
    ax.text(83, 50, "(마) 사형을\n‘법을 빙자한\n살인’으로 봄", **kw)
    ax.text(82.5, 24, "(나) 사형이\n인격을 해방해\n존엄성을\n실현한다고 봄", **kw)
    save(f, OUT + "B06.svg")


def b12():
    f, ax = fig(1.7)
    t = [-3, -2, -1, 1, 2, 3]
    A = [6.2, 6.0, 6.1, 5.9, 5.8, 5.9]
    B = [6.3, 6.1, 6.2, 6.0, 5.9, 6.0]
    C = [6.4, 6.2, 6.3, 6.2, 6.1, 6.2]
    for name, y, mk, ls in [("A국 (사형 폐지, 종신 노역형 대체)", A, "o", "-"), ("B국 (사형 유지)", B, "s", "--"), ("C국 (사형 집행 확대)", C, "^", ":")]:
        ax.plot(t[:3], y[:3], marker=mk, ls=ls, color=G1, ms=3.2, lw=0.9, label=name)
        ax.plot(t[3:], y[3:], marker=mk, ls=ls, color=G1, ms=3.2, lw=0.9)
    ax.axvline(0, color=BURG, lw=0.7, ls=(0, (3, 2)))
    ax.text(0.08, 6.47, "t=0", color=BURG, fontsize=6.4)
    ax.set_ylim(5.6, 6.6); ax.set_xticks([-3, -2, -1, 0, 1, 2, 3]); ax.set_xlabel("t (연도, t=0에 제도 변경)", fontsize=6.4)
    ax.set_ylabel("인구 10만 명당\n살인 건수", fontsize=6.4)
    ax.legend(frameon=False, fontsize=6.0, loc="upper center", bbox_to_anchor=(0.5, -0.32), handlelength=2.2, labelspacing=0.25, ncol=1)
    save(f, OUT + "B12.svg")


def b13():
    f, ax = fig(1.85)
    x = [0, 1, 2, 3, 4]
    d = [9, 5, 3, 2, 2]; l = [6, 6, 6, 5.5, 5.5]
    ax.plot(x, d, marker="o", color=G1, ms=3.6, lw=1.0, label="사형")
    ax.plot(x, l, marker="s", color=G2, ms=3.6, lw=1.0, ls="--", label="종신 노역형")
    for xx, v in zip(x, d):
        ax.text(xx, v + (0.5 if xx == 0 else -1.15), "%g" % v, ha="center", fontsize=6.2)
    for xx, v in zip(x, l):
        ax.text(xx, v + 0.5, "%g" % v, ha="center", fontsize=6.2, color=G2)
    ax.set_xticks(x); ax.set_xticklabels(["선고 직후", "1개월 후", "3개월 후", "6개월 후", "12개월 후"], fontsize=6.2)
    ax.set_ylim(0, 10.5); ax.set_xlim(-0.3, 4.3); ax.set_ylabel("두려움의 크기(점)", fontsize=6.4)
    ax.legend(frameon=False, fontsize=6.4, loc="upper right")
    save(f, OUT + "B13.svg")


def b20():
    f, ax = plt.subplots(figsize=(W, 3.5))
    ax.set_xlim(0, 100); ax.set_ylim(0, 112); ax.axis("off")
    ax.text(24, 109, "칸트", ha="center", fontsize=7.4, fontweight="bold", color=NAVY)
    ax.text(76, 109, "베카리아", ha="center", fontsize=7.4, fontweight="bold", color=NAVY)
    ax.plot([50, 50], [4, 106], color=G4, lw=0.6, ls=(0, (3, 2)))
    def col(x0, texts, fs_list):
        x1 = x0 + 48; nx = x0 + 9
        ys = [86, 58]
        for y, t, fs, fc in zip(ys, texts, fs_list, [("white" if "?" in t else G5) for t in texts]):
            box(ax, nx, y, 39, 15, t.replace("?", ""), fs=fs, fc=("white" if "?" in t else G5))
        box(ax, nx, 30, 39, 12, "정당하다", fs=6.4, bold=True)
        box(ax, x0, 3, 48, 12, "정당하지 않다", fs=6.0)
        arrow(ax, nx + 19.5, 86, nx + 19.5, 73.4); ax.text(nx + 21, 79, "예", fontsize=6, va="center")
        arrow(ax, nx + 19.5, 58, nx + 19.5, 42.4); ax.text(nx + 21, 50, "예", fontsize=6, va="center")
        for y in (93.5, 65.5):
            ax.plot([nx, x0 + 4], [y, y], color=G1, lw=0.8)
        arrow(ax, x0 + 4, 93.5, x0 + 4, 15.4)
        ax.text(x0 + 4.8, 79, "아니요", fontsize=5.6, va="center", rotation=90, ha="left")
    col(0, ["범죄를 저질렀는가?", "( 가 )"], [6.2, 6.6])
    col(52, ["( 나 )", "( 다 )"], [6.6, 6.6])
    save(f, OUT + "B20.svg")


if __name__ == "__main__":
    for fn in (b03, b06, b12, b13, b20):
        fn(); print("ok", fn.__name__)

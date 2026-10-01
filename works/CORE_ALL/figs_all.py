import sys
sys.path.insert(0, "/home/user/ARC-System/works")
from figlib import *   # 폰트 등록·rcParams
import numpy as np
from matplotlib.patches import Rectangle, Polygon, Circle

OUT = "/home/user/ARC-System/works/CORE_ALL/fig/"
K = "#111111"; D = "#444444"; M = "#888888"; L = "#cfcfcf"; XL = "#ececec"
W2 = 6.6
plt.rcParams.update({"font.size": 7.6, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": K, "xtick.color": K, "ytick.color": K, "axes.labelcolor": K, "text.color": K})


def saveW(f, name):
    f.savefig(OUT + name + ".svg", format="svg", bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(f)


def person(ax, x, h, base=0.0):
    """막대 사람: 머리+몸. x 중심, h 키(몸 길이)."""
    ax.add_patch(Circle((x, base + h + 0.18), 0.17, fc="white", ec=K, lw=1.0, zorder=5))
    ax.plot([x, x], [base, base + h], color=K, lw=1.6, zorder=4, solid_capstyle="round")


def a_equity():
    f, axs = plt.subplots(1, 4, figsize=(W2, 1.9), gridspec_kw=dict(wspace=0.08))
    titles = ["(가) 불평등", "(나) 평등", "(다) 형평성", "(라) 정의"]
    notes = ["특정한 사람에게만\n상자를 줌", "같은 상자를\n똑같이 줌", "필요에 따라\n다르게 줌", "장벽 자체를\n제도로 바꿈"]
    boxes = [[0, 0, 2], [1, 1, 1], [2, 1, 0], [0, 0, 0]]
    heights = [0.9, 1.3, 1.7]
    xs = [1.0, 2.6, 4.2]
    fence_h = 2.15
    for k, ax in enumerate(axs):
        ax.set_xlim(0, 5.6); ax.set_ylim(-0.55, 3.35); ax.axis("off")
        ax.text(2.8, 3.25, titles[k], ha="center", va="top", fontsize=8.0, fontweight="bold")
        # 담장
        if k == 3:
            for xx in np.arange(4.95, 5.55, 0.18):
                ax.plot([xx, xx], [0, fence_h], color=M, lw=1.0)
            ax.plot([4.95, 5.55], [fence_h, fence_h], color=M, lw=1.0)
            ax.plot([4.95, 5.55], [fence_h * 0.5, fence_h * 0.5], color=M, lw=0.8)
        else:
            ax.add_patch(Rectangle((4.95, 0), 0.6, fence_h, fc=L, ec=K, lw=0.9, hatch="////", zorder=1))
        ax.plot([0.1, 5.5], [0, 0], color=K, lw=1.0)
        for i in range(3):
            b = boxes[k][i]
            for j in range(b):
                ax.add_patch(Rectangle((xs[i] - 0.4, j * 0.42), 0.8, 0.42, fc=XL, ec=K, lw=0.9, zorder=2))
            person(ax, xs[i], heights[i], base=b * 0.42)
        ax.plot([0.1, 4.9], [fence_h, fence_h], color=D, lw=0.7, ls=(0, (3, 2)))
        ax.text(2.6, -0.2, notes[k], ha="center", va="top", fontsize=6.9, color=D, linespacing=1.25)
    saveW(f, "A_equity")


def b_pyramid():
    f, axs = plt.subplots(1, 2, figsize=(W2, 2.7), gridspec_kw=dict(wspace=0.10))
    dev = np.array([14, 13, 12, 10.6, 9.6, 8.6, 7.6, 6.6, 5.6, 4.6, 3.8, 3.0, 2.3, 1.6, 1.0, 0.5])
    adv = np.array([3.2, 3.4, 3.6, 4.0, 4.5, 5.0, 5.5, 6.0, 6.2, 6.0, 5.7, 5.3, 4.8, 4.4, 4.0, 3.4])
    for ax, v, ttl, sub in ((axs[0], dev, "개발 도상국형", "출생률 높음 · 사망률 높음\n유소년층 비율 ↑ · 노년층 비율 ↓"),
                             (axs[1], adv, "선진국형", "출생률 낮음 · 기대 수명 김\n유소년층 비율 ↓ · 노년층 비율 ↑")):
        y = np.arange(len(v))
        ax.barh(y, -v, color="white", edgecolor=K, lw=0.7, hatch="////", height=0.88)
        ax.barh(y, v, color="white", edgecolor=K, lw=0.7, hatch="\\\\\\\\", height=0.88)
        for yy in (2.5, 12.5):
            ax.plot([-15, 15], [yy, yy], color=K, lw=0.8, ls=":")
        ax.set_yticks([0, 3, 13]); ax.set_yticklabels(["0세", "15세", "65세"], fontsize=6.4)
        ax.set_xlim(-15, 15); ax.set_xticks([])
        ax.spines["left"].set_visible(False); ax.spines["bottom"].set_visible(False)
        ax.tick_params(left=False)
        ax.text(0, 16.6, ttl, ha="center", fontsize=8.4, fontweight="bold")
        ax.text(0, -1.7, sub, ha="center", va="top", fontsize=6.9, color=D, linespacing=1.3)
        ax.text(-14.6, 15.4, "남", fontsize=6.6, color=D); ax.text(13.6, 15.4, "여", fontsize=6.6, color=D)
        ax.set_ylim(-3.6, 17.4)
    axs[1].text(15.6, 1.2, "유소년층\n(14세 이하)", fontsize=6.3, va="center", clip_on=False)
    axs[1].text(15.6, 7.5, "청장년층\n(15~64세)", fontsize=6.3, va="center", clip_on=False)
    axs[1].text(15.6, 14.3, "노년층\n(65세 이상)", fontsize=6.3, va="center", clip_on=False)
    f.text(0.5, -0.03, "개념도 (수치 아님)", fontsize=6.2, color=M, ha="center")
    saveW(f, "B_pyramid")


def b_dtm():
    f, ax = plt.subplots(figsize=(W2, 2.55))
    x = np.linspace(0, 10, 500)
    def sig(x0, k=1.8):
        return 1 / (1 + np.exp(-k * (x - x0)))
    death = 3.0 + 7.0 * (1 - sig(2.7)) + 0.6 * sig(8.4)
    birth = 3.0 + 7.0 * (1 - sig(5.4)) - 0.2 * sig(8.6)
    sc = lambda v: v * 0.46 + 0.35
    b, d = sc(birth), sc(death)
    ax.plot(x, b, color=K, lw=1.9)
    ax.plot(x, d, color=K, lw=1.9, ls=(0, (5, 2)))
    ax.fill_between(x, d, b, where=(birth > death), facecolor=L, edgecolor="none", alpha=0.9)
    ax.fill_between(x, b, d, where=(birth < death), facecolor="white", edgecolor=D, hatch="////", lw=0)
    for xv in (2.0, 4.0, 6.0, 8.0):
        ax.plot([xv, xv], [0, 7.7], color=M, lw=0.7, ls=":")
    labs = [(1.0, "1단계", "고출생·고사망"), (3.0, "2단계", "사망률 급감"),
            (5.0, "3단계", "출생률 감소"), (7.0, "4단계", "저출생·저사망"), (9.0, "5단계", "출생률 < 사망률")]
    for xv, a, bb in labs:
        ax.text(xv, 7.6, a, ha="center", va="top", fontsize=7.8, fontweight="bold")
        ax.text(xv, 6.75, bb, ha="center", va="top", fontsize=6.5, color=D)
    mid = (sc(birth[150]) + sc(death[150])) / 2
    ax.text(3.0, mid, "자연 증가\n가장 큼", ha="center", va="center", fontsize=6.4, fontweight="bold")
    ax.set_xlim(0, 10); ax.set_ylim(0, 7.8)
    ax.spines["left"].set_visible(True); ax.spines["bottom"].set_visible(True)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("시간 (경제 발전 수준) →", fontsize=7, loc="right"); ax.set_ylabel("출생률·사망률", fontsize=7)
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    hs = [Line2D([0], [0], color=K, lw=1.9), Line2D([0], [0], color=K, lw=1.9, ls=(0, (5, 2))),
          Patch(fc=L, ec="none"), Patch(fc="white", ec=D, hatch="////")]
    ax.legend(hs, ["출생률", "사망률", "자연 증가 (출생 > 사망)", "자연 감소 (출생 < 사망)"], loc="lower left",
              frameon=False, fontsize=6.6, ncol=2, bbox_to_anchor=(0.0, 0.0))
    ax.text(10, 7.75, "개념도 (수치 아님)", fontsize=6.2, color=M, ha="right", va="bottom")
    saveW(f, "B_dtm")


def c_timeline():
    f, ax = plt.subplots(figsize=(W2, 2.45))
    ax.set_xlim(0, 11); ax.set_ylim(-3.3, 2.7); ax.axis("off")
    ev = [("1215", "마그나카르타", "영국"), ("1689", "권리 장전", "영국"), ("1776", "독립 선언서", "미국"),
          ("1789", "인간과 시민의\n권리 선언", "프랑스"), ("1838", "인민헌장", "영국"), ("1919", "바이마르 헌법", "독일"),
          ("1948", "세계 인권 선언", "UN"), ("1965", "인종 차별\n철폐 협약", "UN"), ("1966", "국제 인권 규약", "UN"),
          ("1979", "여성 차별\n철폐 협약", "UN"), ("1989", "아동 권리 협약", "UN")]
    ax.plot([0.3, 10.8], [0, 0], color=K, lw=1.6)
    for i, (y, t, w) in enumerate(ev):
        xx = 0.75 + i * 0.95
        ax.add_patch(Circle((xx, 0), 0.11, fc=K, ec=K, zorder=3))
        up = (i % 2 == 0)
        ax.plot([xx, xx], [0, 0.55 if up else -0.55], color=M, lw=0.8)
        ax.text(xx, 0.7 if up else -0.7, y, ha="center", va="bottom" if up else "top", fontsize=8.0, fontweight="bold")
        ax.text(xx, 1.22 if up else -1.22, t, ha="center", va="bottom" if up else "top", fontsize=6.3, linespacing=1.2)
        ax.text(xx, 2.05 if (up and "\n" not in t) else (2.35 if up else -1.85 if "\n" not in t else -2.15), w, ha="center",
                va="bottom" if up else "top", fontsize=5.8, color=M)
    # 세대 띠
    def band(x0, x1, y, txt, fc, fs=6.9):
        ax.add_patch(Rectangle((x0, y), x1 - x0, 0.62, fc=fc, ec=K, lw=0.8, clip_on=False))
        ax.text((x0 + x1) / 2, y + 0.31, txt, ha="center", va="center", fontsize=fs, fontweight="bold",
                color=("white" if fc == K else K), linespacing=1.15)
    band(0.3, 5.0, -3.2, "1세대 — 자유권·평등권·참정권", XL)
    band(5.05, 6.0, -3.2, "2세대\n사회권", K, 6.4)
    band(6.05, 10.8, -3.2, "3세대 — 연대권 (국제 협약)", L)
    saveW(f, "C_timeline")


if __name__ == "__main__":
    a_equity(); b_pyramid(); b_dtm(); c_timeline()
    print("figs ok")

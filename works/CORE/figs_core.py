import sys
sys.path.insert(0, "/home/user/ARC-System/works")
from figlib import *   # 폰트 등록·rcParams
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch, Polygon

OUT = "/home/user/ARC-System/works/CORE/fig/"
K = "#111111"; D = "#444444"; M = "#888888"; L = "#cfcfcf"; XL = "#ececec"
W2 = 6.6
plt.rcParams.update({"font.size": 7.6, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": K, "xtick.color": K, "ytick.color": K, "axes.labelcolor": K, "text.color": K})


def saveW(f, name):
    f.savefig(OUT + name + ".svg", format="svg", bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(f)


def k_axis():
    f, axs = plt.subplots(2, 1, figsize=(W2, 2.55), gridspec_kw=dict(hspace=0.55))
    for ax in axs:
        ax.set_xlim(0, 100); ax.set_ylim(0, 10); ax.axis("off")
        ax.annotate("", xy=(100, 2.2), xytext=(0, 2.2), arrowprops=dict(arrowstyle="-|>", lw=0.9, color=K, mutation_scale=8))
        ax.text(0, 0.2, "약함", fontsize=6.6, color=D); ax.text(100, 0.2, "강한 형벌 →", fontsize=6.6, color=D, ha="right")
    a, b = axs
    # 칸트
    a.text(0, 9.9, "칸트 — 동등성의 원칙", fontsize=8.4, fontweight="bold", va="top")
    a.add_patch(Rectangle((0, 3.2), 44, 4.2, fc="white", ec=M, lw=0.7, hatch="////", zorder=1))
    a.add_patch(Rectangle((56, 3.2), 44, 4.2, fc="white", ec=M, lw=0.7, hatch="////", zorder=1))
    a.plot([50, 50], [2.2, 8.2], color=K, lw=3.0, solid_capstyle="butt", zorder=3)
    a.text(50, 8.9, "범죄의 무게와 같은 형벌만 정당", ha="center", fontsize=7.4, fontweight="bold")
    a.text(22, 5.3, "죄에 못 미침  ×", ha="center", va="center", fontsize=7.4, bbox=dict(fc="white", ec="none", pad=1.5), zorder=4)
    a.text(78, 5.3, "죄를 넘어섬  ×", ha="center", va="center", fontsize=7.4, bbox=dict(fc="white", ec="none", pad=1.5), zorder=4)
    # 베카리아
    b.text(0, 9.9, "베카리아 — 최소성(충분한 정도의 강도만)", fontsize=8.4, fontweight="bold", va="top")
    b.add_patch(Rectangle((0, 3.2), 30, 4.2, fc="white", ec=M, lw=0.7, hatch="\\\\\\\\", zorder=1))
    b.add_patch(Rectangle((66, 3.2), 34, 4.2, fc="white", ec=M, lw=0.7, hatch="////", zorder=1))
    b.add_patch(Rectangle((30, 3.2), 36, 4.2, fc=L, ec=K, lw=1.3, zorder=2))
    b.text(48, 5.3, "허용 범위\n(예방에 필요한 정도)", ha="center", va="center", fontsize=7.3, fontweight="bold", zorder=4)
    b.text(15, 5.3, "예방 목적을 못 이룸  ×", ha="center", va="center", fontsize=6.9, bbox=dict(fc="white", ec="none", pad=1.5), zorder=4)
    b.text(83, 5.3, "쓸데없는 고통  ×", ha="center", va="center", fontsize=7.2, bbox=dict(fc="white", ec="none", pad=1.5), zorder=4)
    b.text(30, 1.0, "하한", ha="center", fontsize=6.9, color=D); b.text(66, 1.0, "상한", ha="center", fontsize=6.9, color=D)
    b.plot([30, 30], [2.2, 7.6], color=K, lw=0.8, ls=":"); b.plot([66, 66], [2.2, 7.6], color=K, lw=0.8, ls=":")
    saveW(f, "K_axis")


def k_impress():
    f, ax = plt.subplots(figsize=(W2, 2.0))
    t = np.linspace(0, 10, 400)
    spike = 9.0 * np.exp(-t * 3.2)
    plateau = 4.1 * (1 - np.exp(-t * 6)) * (1 - 0.03 * t) + 0.0
    ax.fill_between(t, 0, spike, facecolor="white", edgecolor=D, hatch="////", lw=0.8, zorder=2)
    ax.plot(t, spike, color=K, lw=1.6, zorder=3)
    ax.fill_between(t, 0, plateau, facecolor=L, edgecolor="none", alpha=0.85, zorder=1)
    ax.plot(t, plateau, color=K, lw=1.6, ls=(0, (5, 2)), zorder=3)
    ax.set_xlim(-0.2, 10.6); ax.set_ylim(0, 10.8)
    ax.spines["left"].set_visible(True); ax.spines["bottom"].set_visible(True)
    ax.set_xticks([]); ax.set_yticks([])
    ax.annotate("", xy=(10.6, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", lw=0.9, color=K, mutation_scale=8))
    ax.annotate("", xy=(0, 10.6), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", lw=0.9, color=K, mutation_scale=8))
    ax.set_xlabel("처벌 이후 시간", fontsize=7.2, loc="right"); ax.set_ylabel("사람들에게 남는 인상(공포)", fontsize=7.2)
    ax.text(0.55, 9.5, "사형", fontsize=8.2, fontweight="bold")
    ax.text(0.55, 8.35, "한순간의 강렬한 인상", fontsize=7.2)
    ax.text(5.2, 5.0, "종신 노역형", fontsize=8.2, fontweight="bold")
    ax.text(5.2, 4.2, "오래 이어지는 공포 → 억제는 이쪽이 더 큼", fontsize=7.2, va="top")
    ax.text(10.5, 10.4, "개념도 (수치 아님)", fontsize=6.5, color=M, ha="right")
    saveW(f, "K_impress")


if __name__ == "__main__":
    k_axis(); k_impress(); print("ok")


# ---------------------------------------------------------------- Part 2 figures
from matplotlib.patches import FancyBboxPatch, Circle
import random


def _node(ax, x, y, w, h, txt, fs=7.6, fc="white", ec=K, lw=1.0, bold=True, tc=K):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=1.2", fc=fc, ec=ec, lw=lw, zorder=3))
    ax.text(x, y, txt, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal", color=tc, zorder=4, linespacing=1.3)


def _arr2(ax, p, q, style="<|-|>", lw=1.0, color=K, shrink=0):
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle=style, lw=lw, color=color, mutation_scale=8, shrinkA=shrink, shrinkB=shrink), zorder=2)


def t_dialectic():
    f, ax = plt.subplots(figsize=(W2, 2.35))
    ax.set_xlim(0, 100); ax.set_ylim(0, 50); ax.axis("off")
    top, bl, br = (50, 41), (17, 9), (83, 9)
    _node(ax, *top, 26, 9, "변화", fs=9)
    _node(ax, *bl, 28, 9, "모순", fs=9)
    _node(ax, *br, 30, 9, "연관성 (종합론)", fs=8.6)
    _arr2(ax, (42, 36.5), (23.5, 13.6)); _arr2(ax, (58, 36.5), (76.5, 13.6)); _arr2(ax, (32, 9), (68, 9))
    ax.text(15, 30, "변화는 모순을 낳고,\n모순은 다시 변화를 낳는다", fontsize=6.9, ha="center", va="center", color=D)
    ax.text(85, 30, "변화하는 것은 다른 것과의\n관계 속에서 파악된다", fontsize=6.9, ha="center", va="center", color=D)
    ax.text(50, 14.2, "대립은 서로를 보완하고 모든 것은 연결된다", fontsize=6.9, ha="center", color=D)
    ax.add_patch(FancyBboxPatch((38, 21.5), 24, 8.6, boxstyle="round,pad=0,rounding_size=1.2", fc=XL, ec=K, lw=1.3, zorder=3))
    ax.text(50, 25.8, "중용 · 종합", ha="center", va="center", fontsize=8.6, fontweight="bold", zorder=4)
    saveW(f, "T_dialectic")


def t_chain():
    f, ax = plt.subplots(figsize=(W2, 3.15))
    ax.set_xlim(0, 100); ax.set_ylim(0, 62); ax.axis("off")
    names = ["생태 환경", "경제", "사회 구조", "주의", "형이상학", "인식론", "사고 과정"]
    # 왼쪽 선형
    ax.text(18, 60.5, "일반적 견해 — 한 방향", ha="center", fontsize=8, fontweight="bold")
    ys = np.linspace(54, 6, 7)
    for i, (n, y) in enumerate(zip(names, ys)):
        _node(ax, 18, y, 24, 5.6, n, fs=7.4)
        if i < 6:
            _arr2(ax, (18, y - 2.9), (18, ys[i + 1] + 2.9), style="-|>")
    # 오른쪽 상호작용
    ax.text(72, 60.5, "대안 — 서로 영향을 주고받음", ha="center", fontsize=8, fontweight="bold")
    cx, cy, r = 70, 31, 21
    ang = np.deg2rad(90 - np.arange(7) * 360 / 7)
    pts = [(cx + 21.5 * np.cos(a), cy + 21 * np.sin(a)) for a in ang]
    for i in range(7):
        _arr2(ax, pts[i], pts[(i + 1) % 7], lw=0.9, color=D, shrink=10)
    for i, j in ((0, 2), (2, 5), (3, 6)):
        _arr2(ax, pts[i], pts[j], lw=0.6, color=M, shrink=10)
    for (x, y), n in zip(pts, names):
        _node(ax, x, y, 15.5, 5.6, n, fs=7.0, fc="white")
    saveW(f, "T_chain")


def t_efield():
    f, axs = plt.subplots(1, 3, figsize=(W2, 2.0), gridspec_kw=dict(wspace=0.06))
    rnd = random.Random(7)
    shape = [(-0.35, -0.3), (0.35, -0.3), (0.35, 0.15), (0.0, 0.42), (-0.35, 0.15), (-0.35, -0.3)]  # 집 모양
    segs = []
    for _ in range(26):  # 배경: 겹치는 다각형 조각
        cxx, cyy = rnd.uniform(-1, 1), rnd.uniform(-1, 1)
        rr = rnd.uniform(0.25, 0.6); n = rnd.choice([3, 4, 5, 6]); a0 = rnd.uniform(0, 6.28)
        pg = [(cxx + rr * np.cos(a0 + k * 2 * np.pi / n), cyy + rr * np.sin(a0 + k * 2 * np.pi / n)) for k in range(n)]
        pg.append(pg[0])
        segs.append(pg)

    def draw(ax, mode):
        ax.set_xlim(-1.15, 1.15); ax.set_ylim(-1.15, 1.15); ax.set_aspect("equal"); ax.axis("off")
        ax.add_patch(Rectangle((-1.1, -1.1), 2.2, 2.2, fc="white", ec=K, lw=0.9))
        for pg in segs:
            xs, ys = zip(*pg)
            ax.plot(np.clip(xs, -1.1, 1.1), np.clip(ys, -1.1, 1.1), color=(M if mode == 2 else D), lw=(0.5 if mode == 2 else 0.9),
                    alpha=(0.55 if mode == 2 else 1.0))
        xs, ys = zip(*[(x * 0.9 + 0.15, y * 0.9 - 0.1) for x, y in shape])
        ax.plot(xs, ys, color=K, lw=(2.6 if mode == 2 else 0.9), solid_joinstyle="round")
    # (가) 찾을 도형
    a, b, c = axs
    a.set_xlim(-1.15, 1.15); a.set_ylim(-1.15, 1.15); a.set_aspect("equal"); a.axis("off")
    a.add_patch(Rectangle((-1.1, -1.1), 2.2, 2.2, fc="white", ec=K, lw=0.9))
    xs, ys = zip(*[(x * 1.4, y * 1.4) for x, y in shape]); a.plot(xs, ys, color=K, lw=2.2, solid_joinstyle="round")
    draw(b, 1); draw(c, 2)
    for ax, t in zip(axs, ["① 찾아야 할 도형", "② 복잡한 배경 속에 숨어 있다", "③ 위치 확인"]):
        ax.set_title(t, fontsize=7.2, fontweight="bold", pad=3)
    saveW(f, "T_efield")


def t_iq():
    f, ax = plt.subplots(figsize=(W2, 2.6))
    ax.set_xlim(0, 100); ax.set_ylim(0, 50); ax.axis("off")
    cols = [13, 36, 61, 86]
    titles = ["① 기억 · 반응 속도", "② 상식 문제", "③ 커텔\n문화 공평 검사", "④ 공간 능력 검사"]
    ax.annotate("", xy=(3, 41), xytext=(3, 4), arrowprops=dict(arrowstyle="-|>", lw=0.9, color=K, mutation_scale=8))
    ax.text(0.5, 43.5, "상대 점수", fontsize=6.8, color=D)
    ax.add_patch(Rectangle((6, 4), 38, 37, fc=XL, ec="none", zorder=0))
    ax.text(25, 39.2, "점수를 맞추어 집단을 고름", ha="center", fontsize=6.9, color=D)
    for x, t in zip(cols, titles):
        ax.text(x + 2, 1.5, t, ha="center", va="top", fontsize=7.2, fontweight="bold")
        ax.plot([x + 2, x + 2], [5, 36], color=L, lw=0.6, zorder=0)
    for i, x in enumerate(cols):
        if i < 2:
            ax.scatter([x], [22], s=60, facecolor="white", edgecolor=K, lw=1.3, zorder=3)
            ax.scatter([x + 4.2], [22], s=60, facecolor=K, edgecolor=K, zorder=3)
        elif i == 2:
            ax.scatter([x], [29], s=60, facecolor="white", edgecolor=K, lw=1.3, zorder=3)
            ax.scatter([x + 4.2], [16], s=60, facecolor=K, edgecolor=K, zorder=3)
            _arr2(ax, (x + 4.2, 28), (x + 4.2, 18), style="-|>", lw=0.9)
            ax.text(x - 3, 22.5, "중국이 더 낮음", fontsize=6.8, va="center", ha="right")
        else:
            ax.scatter([x], [16], s=60, facecolor="white", edgecolor=K, lw=1.3, zorder=3)
            ax.scatter([x + 4.2], [29], s=60, facecolor=K, edgecolor=K, zorder=3)
            _arr2(ax, (x + 4.2, 18), (x + 4.2, 27), style="-|>", lw=0.9)
            ax.text(x - 3, 22.5, "동양인이 더 높음", fontsize=6.8, va="center", ha="right")
    ax.scatter([48], [46.5], s=45, facecolor="white", edgecolor=K, lw=1.2); ax.text(50, 46.5, "미국", fontsize=7, va="center")
    ax.scatter([60], [46.5], s=45, facecolor=K, edgecolor=K); ax.text(62, 46.5, "중국 · 동양", fontsize=7, va="center")
    ax.text(100, 46.5, "개념도 (수치 아님)", ha="right", fontsize=6.4, color=M, va="center")
    saveW(f, "T_iq")


if __name__ == "__main__":
    t_dialectic(); t_chain(); t_efield(); t_iq(); print("ok2")

import sys
sys.path.insert(0, "/home/user/ARC-System/works"); sys.path.insert(0, "/home/user/ARC-System/works/B")
from figlib import *
import numpy as np
import figs_b as FB
from figs_b import pyramid, GR

OUT = "/home/user/ARC-System/works/B/fig/"


def two(name, keys, titles):
    f, axs = plt.subplots(1, 2, figsize=(W, 2.2))
    for ax, k, t in zip(axs, keys, titles):
        pyramid(ax, k, t); ax.set_xlabel("총인구에 대한 비율(%)", fontsize=5.8)
    f.subplots_adjust(wspace=0.4)
    save(f, OUT + name + ".svg")


def bs03():
    f, axs = plt.subplots(1, 3, figsize=(W, 1.95))
    for ax, k, t in zip(axs, ["A", "B", "C"], ["(가)", "(나)", "(다)"]):
        pyramid(ax, k, t, yticks_every=8)
        ax.set_xticks([-8, 0, 8]); ax.set_xticklabels(["8", "0", "8"], fontsize=5.4)
        for lbl in ax.get_yticklabels(): lbl.set_fontsize(5.2)
        ax.texts[0].set_visible(False); ax.texts[1].set_visible(False); ax.set_title(ax.get_title(), fontsize=7, fontweight="bold", color=NAVY, pad=3)
    axs[1].set_xlabel("총인구에 대한 비율(%)", fontsize=5.8)
    f.subplots_adjust(wspace=0.55)
    save(f, OUT + "BS03.svg")


def bs04():
    f, ax = fig(1.75)
    x = [0, 50, 100, 150, 200]
    b = [40, 39, 25, 13, 9]; d = [37, 20, 10, 9, 11]
    ax.plot(x, b, marker="o", color=G1, ms=3.4, ls="--", label="출생률"); ax.plot(x, d, marker="s", color=G1, ms=3.4, label="사망률")
    for xx, v in zip(x, b): ax.text(xx, v + (-5.6 if xx == 200 else 2.2), str(v), ha="center", fontsize=6.2)
    for xx, v in zip(x, d): ax.text(xx, v + (2.4 if xx == 200 else -5.2), str(v), ha="center", fontsize=6.2)
    ax.set_ylim(0, 50); ax.set_xticks(x); ax.set_xticklabels(["0", "50", "100", "150", "200"]); ax.set_xlabel("경과 기간(년)", fontsize=6.4)
    ax.set_ylabel("출생률·사망률(‰)", fontsize=6.4); ax.legend(frameon=False, fontsize=6.4, loc="upper right", ncol=2)
    save(f, OUT + "BS04.svg")


def bs05():
    f, ax = plt.subplots(figsize=(W, 2.0))
    t = np.linspace(0, 10, 300)
    birth = 9 + 29 / (1 + np.exp((t - 5.0) * 1.3))
    death = 10 + 26 / (1 + np.exp((t - 2.5) * 2.2)) + 3 / (1 + np.exp(-(t - 8.5) * 2))
    ax.plot(t, birth, color=G1, lw=1.1, ls="--"); ax.plot(t, death, color=G1, lw=1.1)
    for x in (2, 4, 6, 8): ax.axvline(x, color=G4, lw=0.6)
    for i in range(5): ax.text(1 + 2 * i, 45.5, "%d단계" % (i + 1), ha="center", fontsize=6.4, fontweight="bold", color=NAVY)
    for lab_, x in (("(가)", 3.0), ("(나)", 5.0), ("(다)", 9.0)):
        ax.axvline(x, color=BURG, lw=0.9, ymax=0.86)
        ax.text(x, 40.3, lab_, ha="center", fontsize=7.2, fontweight="bold", color=BURG, bbox=dict(fc="white", ec="none", pad=0.6))
    ax.plot([], [], color=G1, ls="--", label="출생률"); ax.plot([], [], color=G1, label="사망률")
    ax.legend(frameon=False, fontsize=6.2, loc="lower left", ncol=2, bbox_to_anchor=(0.0, 0.0))
    ax.set_xlim(0, 10); ax.set_ylim(0, 49); ax.set_xticks([]); ax.set_yticks([5, 40]); ax.set_yticklabels(["낮음", "높음"], fontsize=6.3)
    ax.set_xlabel("시간(경제 발전 수준) →", fontsize=6.3); ax.set_ylabel("출생률과 사망률", fontsize=6.3)
    save(f, OUT + "BS05.svg")


def bs09():
    f, ax = fig(1.9)
    yrs = [2020, 2030, 2040, 2050, 2060, 2070]
    yo = [6, 5, 4.5, 4, 3.5, 3]; wk = [36, 33, 29, 26, 24, 22]; ol = [8, 12, 15, 17, 19, 20]
    ax.plot(yrs, wk, marker="o", color=G1, ms=3.2, label="청장년층"); ax.plot(yrs, ol, marker="s", color=G2, ms=3.2, ls="--", label="노년층")
    ax.plot(yrs, yo, marker="^", color=G1, ms=3.4, ls=":", label="유소년층")
    for xx, v in zip(yrs, wk): ax.text(xx, v + 1.6, "%g" % v, ha="center", fontsize=6.0)
    for xx, v in zip(yrs, ol): ax.text(xx, v + (-3.6 if xx == 2070 else 1.6), "%g" % v, ha="center", fontsize=6.0, color=G2)
    for xx, v in zip(yrs, yo): ax.text(xx, v - 4.0, "%g" % v, ha="center", fontsize=6.0)
    ax.set_ylim(-2, 42); ax.set_xticks(yrs); ax.set_ylabel("인구(백만 명)", fontsize=6.4)
    ax.legend(frameon=False, fontsize=6.2, loc="upper right", ncol=3, bbox_to_anchor=(1.0, 1.12))
    save(f, OUT + "BS09.svg")


def bs13():
    f, ax = fig(1.7)
    yrs = ["2010", "2015", "2020"]
    for name, v, mk, ls in [("A국", [1.2, 1.3, 1.5], "o", "-"), ("B국", [1.2, 1.1, 1.0], "s", "--"), ("C국", [1.2, 1.5, 1.3], "^", ":")]:
        ax.plot(yrs, v, marker=mk, color=G1, ms=3.6, ls=ls, label=name)
        ax.text(2.06, v[2], "%.1f" % v[2], fontsize=6.2, va="center")
    ax.axhline(2.1, color=BURG, lw=0.7, ls=(0, (3, 2))); ax.text(-0.1, 2.14, "대체 수준 2.1명", fontsize=6.2, color=BURG)
    ax.set_xlim(-0.2, 2.4); ax.set_ylim(0.8, 2.4); ax.set_ylabel("합계 출산율(명)", fontsize=6.4)
    ax.legend(frameon=False, fontsize=6.4, loc="lower left", ncol=3, bbox_to_anchor=(0.0, 0.0))
    save(f, OUT + "BS13.svg")


if __name__ == "__main__":
    two("BS01", ["A", "C"], ["(가)", "(나)"])
    bs03(); bs04(); bs05(); bs09(); two("BS10", ["E", "F"], ["E", "F"]); bs13(); two("BS20", ["A", "D"], ["(가)", "(나)"])
    print("ok")

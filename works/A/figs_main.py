import sys
sys.path.insert(0, "/home/user/ARC-System/works")
from figlib import *
import numpy as np
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch, Polygon

OUT = "/home/user/ARC-System/works/A/fig/"
GR = [G1, "#8a8f97", "#c9ccd1"]   # 짙은/중간/옅은 회색


def label_bars(ax, bars, fmt="{:.0f}", dy=0.6, fs=6.4):
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + dy, fmt.format(b.get_height()),
                ha="center", va="bottom", fontsize=fs, color=G1)


# ---------------------------------------------------------------- A01
def person(ax, x, base, h, w=3.4):
    ax.add_patch(Rectangle((x - w / 2, base), w, h - 5.2, fc=G3, ec=G1, lw=0.6, zorder=3))
    ax.add_patch(Circle((x, base + h - 2.6), 2.6, fc="white", ec=G1, lw=0.7, zorder=4))
    return base + h - 2.6


def a01():
    f, axs = plt.subplots(2, 2, figsize=(W, 3.2))
    heights = [32, 24, 16]
    setups = {"(가)": [2, 0, 0], "(나)": [1, 1, 1], "(다)": [0, 1, 2], "(라)": [0, 0, 0]}
    FT = 24; BH = 6
    for ax, (name, boxes) in zip(axs.flat, setups.items()):
        ax.set_xlim(0, 58); ax.set_ylim(-1, 50); ax.axis("off"); ax.set_aspect("equal")
        ax.plot([0, 58], [0, 0], color=G1, lw=0.8)
        for i, (h, nb) in enumerate(zip(heights, boxes)):
            x = 6 + i * 10.5
            for k in range(nb):
                ax.add_patch(Rectangle((x - 3.6, k * BH), 7.2, BH, fc="white", ec=G1, lw=0.6, zorder=2))
            person(ax, x, nb * BH, h)
        if name == "(라)":
            ax.add_patch(Rectangle((40, 0), 10, FT, fc="none", ec=G2, lw=0.6, ls=(0, (2.5, 2))))
            for xx in (43.3, 46.7):
                ax.plot([xx, xx], [0, FT], color=G3, lw=0.4, ls=(0, (2.5, 2)))
        else:
            ax.add_patch(Rectangle((40, 0), 10, FT, fc=G4, ec=G1, lw=0.7, zorder=5))
            for xx in (43.3, 46.7):
                ax.plot([xx, xx], [0, FT], color=G2, lw=0.4, zorder=6)
            ax.plot([0, 40], [FT, FT], color=BURG, lw=0.6, ls=(0, (3, 2)), zorder=1)
        ax.text(0.5, 49.5, name, fontsize=7.6, fontweight="bold", va="top", color=NAVY)
    f.subplots_adjust(hspace=0.02, wspace=0.02)
    save(f, OUT + "A01.svg")


# ---------------------------------------------------------------- A03
def a03():
    f, ax = plt.subplots(figsize=(W, 2.75))
    ax.set_xlim(0, 100); ax.set_ylim(0, 92); ax.axis("off")
    box(ax, 18, 79, 64, 13, "아리스토텔레스의 정의\n‘같은 것은 같게, 다른 것은 다르게’", fs=6.5, bold=True, fc=G5)
    box(ax, 0, 40, 25, 30, "(가)\n법을 준수하여\n공익을\n실현함\n(모든 사람에게\n적용)", fs=5.7)
    box(ax, 30, 57, 70, 10, "특수적 정의", fs=6.5, bold=True, fc=G5)
    box(ax, 27, 4, 23.5, 38, "(나)\n각자의 가치나\n기여에 비례하여\n희소 자원을\n분배함", fs=5.6)
    box(ax, 51.5, 4, 23.5, 38, "(다)\n해를 끼친 만큼\n보상하게 하여\n동등하지 않음을\n바로잡음", fs=5.6)
    box(ax, 76, 4, 24, 38, "(라)\n같은 가치를\n지닌 두 물건을\n교환하게 함", fs=5.6)
    arrow(ax, 34, 79, 12.5, 70, style="-")
    arrow(ax, 66, 79, 65, 67, style="-")
    for x in (38.7, 63.2, 88):
        arrow(ax, 65, 57, x, 42, style="-")
    save(f, OUT + "A03.svg")


# ---------------------------------------------------------------- A12
def a12():
    f, ax = fig(1.85)
    X = [500, 300, 200]; Y = [200, 400, 400]; Z = [200, 500, 300]
    x = np.arange(3); w = 0.26
    for k, (v, lab) in enumerate(zip([X, Y, Z], ["방안 X", "방안 Y", "방안 Z"])):
        b = ax.bar(x + (k - 1) * w, v, w, color=GR[k], edgecolor=G1, linewidth=0.5, label=lab)
        label_bars(ax, b, dy=8)
    ax.set_xticks(x); ax.set_xticklabels(["동아리 A", "동아리 B", "동아리 C"])
    ax.set_ylim(0, 620); ax.set_yticks([0, 200, 400, 600]); ax.set_ylabel("배분액(만 원)")
    ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.16), fontsize=6.6, handlelength=1.2)
    save(f, OUT + "A12.svg")


# ---------------------------------------------------------------- A14
def a14():
    f, axs = plt.subplots(1, 2, figsize=(W, 1.55))
    xs = ["1차년도", "2차년도", "3차년도"]
    for ax, (ttl, ys, ylim, fmt) in zip(axs, [("(가) 수혜자 중 대회 입상 경력\n보유 비율(%)", [90, 55, 12], (0, 110), "{:.0f}"),
                                             ("(나) 수혜자의 평균 가구\n소득 분위(1=최저)", [6.6, 4.4, 2.1], (0, 8), "{:.1f}")]):
        ax.plot(xs, ys, marker="o", color=G1, ms=3.6, lw=1.0)
        for i, v in enumerate(ys):
            ax.text(i, v + (ylim[1] * 0.05), fmt.format(v), ha="center", fontsize=6.6)
        ax.set_ylim(*ylim); ax.set_xlim(-0.35, 2.35); ax.set_title(ttl, fontsize=6.6, loc="left", pad=3, linespacing=1.2)
        ax.tick_params(axis="x", labelsize=6.4)
    f.subplots_adjust(wspace=0.32)
    save(f, OUT + "A14.svg")


# ---------------------------------------------------------------- A17
def a17():
    f, ax = plt.subplots(figsize=(W, 3.7))
    ax.set_xlim(0, 100); ax.set_ylim(0, 122); ax.axis("off")
    box(ax, 0, 106, 100, 16, "전제  처벌은 사회적 이익을 증진하는 수단이며,\n그 강도는 억제에 충분한 정도에 그쳐야 한다", fs=6.2, fc=G5)
    box(ax, 0, 80, 48, 15, "전제 1\n( 가 )", fs=6.6)
    box(ax, 0, 55, 48, 15, "전제 2\n( 나 )", fs=6.6)
    box(ax, 0, 24, 48, 22, "중간 결론 1\n사형은 억제에 필요한\n강도를 넘어선다\n(종신 노역형으로 충분)", fs=6.0, fc=G5)
    box(ax, 56, 80, 44, 15, "전제 3\n( 다 )", fs=6.6)
    box(ax, 56, 46, 44, 24, "중간 결론 2\n국가는 시민의 생명을\n빼앗을 권능을\n갖지 못한다", fs=6.0, fc=G5)
    box(ax, 6, 0, 88, 12, "결론  사형은 국가의 전쟁이자\n법을 빙자한 살인이다", fs=6.2, bold=True, fc="white", lw=1.0)
    arrow(ax, 24, 106, 24, 95.3); arrow(ax, 78, 106, 78, 95.3)
    arrow(ax, 24, 80, 24, 70.3); arrow(ax, 24, 55, 24, 46.3)
    arrow(ax, 78, 80, 78, 70.3)
    arrow(ax, 24, 24, 34, 12.3); arrow(ax, 78, 46, 66, 12.3)
    save(f, OUT + "A17.svg")


# ---------------------------------------------------------------- A25
def a25():
    f, ax = plt.subplots(figsize=(W, 2.05))
    items = ["평가·측정의 용이성", "성취(업적) 동기 부여", "사회적 약자 배려", "잠재력 실현 기회 제공"]
    data = {"A": [5, 5, 1, 3], "B": [2, 3, 2, 5], "C": [3, 1, 5, 2]}
    mk = {"A": ("o", G1, G1), "B": ("s", "white", G1), "C": ("^", G3, G1)}
    for i in range(4):
        ax.axhline(3 - i, color=G4, lw=0.5, zorder=0)
    for k, v in data.items():
        m, fc, ec = mk[k]
        ax.scatter(v, [3 - i for i in range(4)], marker=m, s=34, facecolor=fc, edgecolor=ec, linewidth=0.8, zorder=3, label=k)
    ax.set_yticks([3 - i for i in range(4)]); ax.set_yticklabels(items, fontsize=6.6)
    ax.set_xlim(0.5, 5.5); ax.set_xticks([1, 2, 3, 4, 5]); ax.set_ylim(-0.6, 3.6)
    ax.set_xlabel("평가 점수(점)", fontsize=6.6)
    ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
    ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.2), fontsize=6.8, handletextpad=0.3, columnspacing=1.4)
    save(f, OUT + "A25.svg")


# ---------------------------------------------------------------- A27
def grouped(ax, groups, series, colors, ylim, fmt="{:.0f}", w=0.34, dy=None, legend=True, ncol=2):
    x = np.arange(len(groups))
    n = len(series)
    for k, (name, vals) in enumerate(series.items()):
        b = ax.bar(x + (k - (n - 1) / 2) * w, vals, w, color=colors[k], edgecolor=G1, linewidth=0.5, label=name)
        label_bars(ax, b, fmt, dy=dy if dy else ylim[1] * 0.015)
    ax.set_xticks(x); ax.set_xticklabels(groups); ax.set_ylim(*ylim)
    if legend:
        ax.legend(frameon=False, ncol=ncol, loc="upper center", bbox_to_anchor=(0.5, 1.18), fontsize=6.6, handlelength=1.2)


def a27():
    f, ax = fig(1.7)
    grouped(ax, ["집단 갑", "집단 을"], {"(가) 참새 결론": [8.7, 8.8], "(나) 펭귄 결론": [5.2, 7.4]}, [GR[0], GR[2]], (0, 10.5), fmt="{:.1f}")
    ax.set_ylabel("설득력 평가(점)")
    save(f, OUT + "A27.svg")


# ---------------------------------------------------------------- A28
def a28():
    f, ax = fig(1.95)
    cats = ["타당\n결론 그럴듯", "타당\n결론 낯섦", "부당\n결론 그럴듯", "부당\n결론 낯섦"]
    grouped(ax, cats, {"집단 갑": [92, 55, 70, 15], "집단 을": [95, 70, 50, 18]}, [GR[0], GR[2]], (0, 115), w=0.36, dy=1.5)
    ax.set_ylabel("‘타당하다’고 답한 비율(%)"); ax.set_yticks([0, 25, 50, 75, 100])
    ax.tick_params(axis="x", labelsize=6.2)
    save(f, OUT + "A28.svg")


# ---------------------------------------------------------------- A29
def a29():
    f, ax = fig(1.7)
    grouped(ax, ["속담 쌍 1", "속담 쌍 2", "속담 쌍 3", "속담 쌍 4"], {"집단 갑": [30, 35, 28, 33], "집단 을": [63, 58, 66, 61]}, [GR[0], GR[2]], (0, 90), w=0.36, dy=1.5)
    ax.set_ylabel("대립 의미 속담을\n고른 비율(%)", fontsize=6.6); ax.set_yticks([0, 25, 50, 75])
    save(f, OUT + "A29.svg")


# ---------------------------------------------------------------- A31
def a31():
    f, ax = plt.subplots(figsize=(W, 1.85))
    rows = [("어머니와 딸의 갈등\n– 집단 갑", 72), ("어머니와 딸의 갈등\n– 집단 을", 26), ("룸메이트 갈등\n– 집단 갑", 65), ("룸메이트 갈등\n– 집단 을", 30)]
    y = [3.2, 2.4, 0.9, 0.1]
    for yy, (lab, v) in zip(y, rows):
        ax.barh(yy, v, height=0.62, color=GR[0], edgecolor=G1, linewidth=0.5)
        ax.barh(yy, 100 - v, left=v, height=0.62, color=GR[2], edgecolor=G1, linewidth=0.5)
        ax.text(v / 2, yy, "%d%%" % v, color="white", ha="center", va="center", fontsize=6.6, fontweight="bold")
        ax.text(v + (100 - v) / 2, yy, "%d%%" % (100 - v), color=G1, ha="center", va="center", fontsize=6.6)
    ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=6.3)
    ax.set_xlim(0, 100); ax.set_xticks([0, 25, 50, 75, 100]); ax.set_xlabel("응답자 비율(%)", fontsize=6.6)
    ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(fc=GR[0], ec=G1, label="변증법적 해결"), Patch(fc=GR[2], ec=G1, label="비변증법적 해결")],
              frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(0.42, 1.2), fontsize=6.6, handlelength=1.2)
    save(f, OUT + "A31.svg")


# ---------------------------------------------------------------- A32
def a32():
    f, axs = plt.subplots(1, 2, figsize=(W, 1.85), sharey=True)
    data = {"집단 갑": {"p": (5.0, 3.4), "q": (7.0, 7.6)}, "집단 을": {"p": (5.0, 5.9), "q": (7.0, 6.3)}}
    for ax, (g, d) in zip(axs, data.items()):
        for k, (mk, ls, col) in {"p": ("o", "--", G2), "q": ("s", "-", G1)}.items():
            ax.plot([0, 1], d[k], marker=mk, ls=ls, color=col, ms=3.6, lw=1.0, label="연구 " + k)
            ax.text(-0.06, d[k][0], "%.1f" % d[k][0], ha="right", va="center", fontsize=6.3)
            dy = (0.28 if d[k][1] >= d["p" if k == "q" else "q"][1] else -0.28)
            ax.text(1.06, d[k][1] + dy, "%.1f" % d[k][1], ha="left", va="center", fontsize=6.3)
        ax.set_xlim(-0.35, 1.35); ax.set_xticks([0, 1]); ax.set_xticklabels(["단독 제시", "함께 제시"], fontsize=6.4)
        ax.set_ylim(1, 9); ax.set_title(g, fontsize=7, fontweight="bold", color=NAVY, pad=3)
    axs[0].set_ylabel("설득력 평가(점)"); axs[1].legend(frameon=False, fontsize=6.4, loc="lower right", handlelength=1.8)
    f.subplots_adjust(wspace=0.12)
    save(f, OUT + "A32.svg")


# ---------------------------------------------------------------- A33
def a33():
    f, (a1, a2) = plt.subplots(1, 2, figsize=(W, 1.95), gridspec_kw=dict(width_ratios=[1, 1.15]))
    pts = {"X": (9, 3), "Y": (6, 6), "Z": (3, 9)}
    for k, (x, y) in pts.items():
        a1.scatter([x], [y], s=26, color=G1, zorder=3)
        a1.text(x + 0.45, y + 0.5, k, fontsize=7, fontweight="bold")
    a1.set_xlim(0, 11); a1.set_ylim(0, 11); a1.set_xticks([0, 5, 10]); a1.set_yticks([0, 5, 10])
    a1.set_xlabel("속성 ㉠ 점수", fontsize=6.6); a1.set_ylabel("속성 ㉡ 점수", fontsize=6.6)
    a1.set_title("제품별 속성 점수", fontsize=6.6, loc="left", pad=3)
    x = np.arange(2); w = 0.34
    for k, (name, vals) in enumerate({"집단 갑": [34, 47], "집단 을": [36, 22]}.items()):
        b = a2.bar(x + (k - 0.5) * w, vals, w, color=[GR[0], GR[2]][k], edgecolor=G1, linewidth=0.5, label=name)
        label_bars(a2, b, dy=1)
    a2.set_xticks(x); a2.set_xticklabels(["이유 설명\n요구 없음", "이유 설명\n요구함"], fontsize=6.3)
    a2.set_ylim(0, 62); a2.set_yticks([0, 20, 40, 60])
    a2.set_title("Y를 선택한 비율(%)", fontsize=6.6, loc="left", pad=3)
    a2.legend(frameon=False, fontsize=6.3, loc="upper left", handlelength=1.1)
    f.subplots_adjust(wspace=0.38)
    save(f, OUT + "A33.svg")


# ---------------------------------------------------------------- A34
def a34_data():
    rng = np.random.default_rng(7)
    n = 24
    pa = np.clip(rng.uniform(0.8, 9.2, n), 0, 10)
    na = np.clip(9.4 - 0.85 * pa + rng.normal(0, 1.0, n), 0.3, 9.7)
    pb = rng.uniform(0.8, 9.2, n)
    nb = np.clip(rng.uniform(0.8, 9.2, n), 0, 10)
    # 을: 우상단(모두 강함) 점 확보
    pb[:3] = [7.6, 8.4, 6.9]; nb[:3] = [7.2, 6.8, 8.1]
    return (pa, na), (pb, nb)


def a34():
    (pa, na), (pb, nb) = a34_data()
    f, axs = plt.subplots(1, 2, figsize=(W, 1.75), sharey=True)
    for ax, (px, ny), g in zip(axs, [(pa, na), (pb, nb)], ["집단 갑", "집단 을"]):
        ax.scatter(px, ny, s=9, color=G1, alpha=0.9, linewidths=0)
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_xticks([0, 5, 10]); ax.set_yticks([0, 5, 10])
        ax.set_title(g, fontsize=7, fontweight="bold", color=NAVY, pad=3)
        ax.set_xlabel("긍정 정서 강도", fontsize=6.4)
    axs[0].set_ylabel("부정 정서 강도", fontsize=6.4)
    f.subplots_adjust(wspace=0.12)
    save(f, OUT + "A34.svg")


# ---------------------------------------------------------------- A37
def a37():
    f, ax = plt.subplots(figsize=(W, 2.0))
    ax.set_xlim(0, 100); ax.set_ylim(0, 60); ax.axis("off")
    bw, bh = 20, 13
    xs = [0, 26.6, 53.3, 80]
    row1 = ["생태 환경", "( 가 )", "사회 구조", "( 나 )"]
    for x, t in zip(xs, row1):
        box(ax, x, 40, bw, bh, t, fs=6.8, fc=(G5 if "(" in t else "white"))
    for i in range(3):
        arrow(ax, xs[i] + bw, 46.5, xs[i + 1], 46.5, style="<|-|>")
    xs2 = [80, 53.3, 26.6]
    row2 = ["형이상학\n(세계관)", "( 다 )", "사고 과정"]
    for x, t in zip(xs2, row2):
        box(ax, x, 6, bw, bh, t, fs=6.8, fc=(G5 if "(" in t else "white"))
    arrow(ax, 90, 40, 90, 19.5, style="<|-|>")
    for i in range(2):
        arrow(ax, xs2[i], 12.5, xs2[i + 1] + bw, 12.5, style="<|-|>")
    save(f, OUT + "A37.svg")


# ---------------------------------------------------------------- A40
def a40():
    f, axs = plt.subplots(1, 2, figsize=(W, 1.85), gridspec_kw=dict(width_ratios=[1.3, 1]), sharey=True)
    b = axs[0].bar(["수렵·채집\n집단", "농경\n집단", "도시 산업\n집단"], [26, 39, 29], width=0.55, color=[GR[2], GR[0], GR[1]], edgecolor=G1, linewidth=0.5)
    label_bars(axs[0], b, dy=0.8)
    b = axs[1].bar(["규범이\n엄격한 집단", "규범이\n자유로운 집단"], [41, 32], width=0.5, color=[GR[0], GR[2]], edgecolor=G1, linewidth=0.5)
    label_bars(axs[1], b, dy=0.8)
    axs[0].set_ylim(0, 52); axs[0].set_ylabel("평균 소요 시간(초)")
    axs[0].set_title("(가) 생업이 다른 집단", fontsize=6.6, loc="left", pad=3)
    axs[1].set_title("(나) 같은 사회 안의 두 집단", fontsize=6.6, loc="left", pad=3)
    for a in axs: a.tick_params(axis="x", labelsize=6.2)
    f.subplots_adjust(wspace=0.08)
    save(f, OUT + "A40.svg")


# ---------------------------------------------------------------- A41
def a41():
    f, ax = fig(1.95)
    grouped(ax, ["집단 갑", "집단 병", "집단 을"], {"처치 없음": [36, 33, 30], "복수 대명사(we, us, our)": [41, 38, 35], "단수 대명사(I, me, mine)": [32, 30, 27]},
            GR, (0, 56), w=0.26, dy=0.8, ncol=3)
    ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.2), fontsize=5.9, handlelength=1.0, columnspacing=0.8)
    ax.set_ylabel("평균 소요 시간(초)"); ax.set_yticks([0, 10, 20, 30, 40, 50])
    save(f, OUT + "A41.svg")


# ---------------------------------------------------------------- A47
def a47():
    f, ax = plt.subplots(figsize=(W, 2.3))
    stats = {
        ("T1", "갑"): (68, 82, 92, 102, 116), ("T1", "을"): (76, 91, 100, 110, 124),
        ("T2", "갑"): (84, 98, 108, 118, 130), ("T2", "을"): (74, 88, 98, 108, 120),
        ("T3", "갑"): (78, 93, 103, 112, 126), ("T3", "을"): (74, 90, 99, 108, 122),
    }
    pos = []; bx = []
    for i, t in enumerate(["T1", "T2", "T3"]):
        for j, g in enumerate(["갑", "을"]):
            lo, q1, med, q3, hi = stats[(t, g)]
            bx.append(dict(whislo=lo, q1=q1, med=med, q3=q3, whishi=hi, fliers=[]))
            pos.append(i * 3 + j * 1.05)
    bp = ax.bxp(bx, positions=pos, widths=0.85, showfliers=False, patch_artist=True,
                boxprops=dict(edgecolor=G1, linewidth=0.7), medianprops=dict(color=G1, linewidth=1.2),
                whiskerprops=dict(color=G1, linewidth=0.7), capprops=dict(color=G1, linewidth=0.7))
    for k, patch in enumerate(bp["boxes"]):
        patch.set_facecolor(GR[0] if k % 2 == 0 else GR[2])
        if k % 2 == 0: patch.set_facecolor("#9da2a9")
    ax.set_xticks([0.52, 3.52, 6.52]); ax.set_xticklabels(["T1\n(분류·규칙 찾기)", "T2\n(공간 구성)", "T3"], fontsize=6.4)
    ax.set_ylim(60, 138); ax.set_ylabel("점수(점)")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(fc="#9da2a9", ec=G1, label="집단 갑"), Patch(fc=GR[2], ec=G1, label="집단 을")], frameon=False, ncol=2,
              loc="upper center", bbox_to_anchor=(0.5, 1.15), fontsize=6.6, handlelength=1.2)
    save(f, OUT + "A47.svg")


# ---------------------------------------------------------------- A48
def a48():
    f, ax = fig(1.75)
    for name, ys, mk, ls in [("집단 갑", (8.2, 6.9), "o", "-"), ("집단 을", (8.4, 4.1), "s", "--")]:
        ax.plot([0, 1], ys, marker=mk, ls=ls, color=G1, ms=4, lw=1.0, label=name)
        ax.text(-0.05, ys[0] + (0.35 if ys[0] > 8.3 else -0.35), "%.1f" % ys[0], ha="right", va="center", fontsize=6.4)
        ax.text(1.05, ys[1], "%.1f" % ys[1], ha="left", va="center", fontsize=6.4)
    ax.set_xlim(-0.35, 1.35); ax.set_xticks([0, 1]); ax.set_xticklabels(["상황 정보를 주기 전", "‘배정된 과제’라는\n상황 정보를 준 후"], fontsize=6.4)
    ax.set_ylim(0, 10); ax.set_yticks([0, 5, 10]); ax.set_ylabel("글쓴이의 실제 태도\n추측 평균(점)", fontsize=6.4)
    ax.legend(frameon=False, fontsize=6.6, loc="lower left")
    save(f, OUT + "A48.svg")


if __name__ == "__main__":
    for fn in (a01, a03, a12, a14, a17, a25, a27, a28, a29, a31, a32, a33, a34, a37, a40, a41, a47, a48):
        fn(); print("ok", fn.__name__)

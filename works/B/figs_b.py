import sys, json
sys.path.insert(0, "/home/user/ARC-System/works")
sys.path.insert(0, "/home/user/ARC-System/works/B")
from figlib import *
import numpy as np
from matplotlib.patches import Polygon, Patch
from matplotlib.lines import Line2D
import popdata as PD

OUT = "/home/user/ARC-System/works/B/fig/"
GR = [G1, "#8a8f97", "#c9ccd1", "#e6e7e9"]
WORLD = json.load(open("/home/user/ARC-System/works/data/world.geo.json"))


def lab(ax, bars, fmt="{:.0f}", dy=None, fs=6.3, ylim=None):
    for b in bars:
        h = b.get_height()
        ax.text(b.get_x() + b.get_width() / 2, h + (dy if dy is not None else (ylim or h) * 0.02), fmt.format(h), ha="center", va="bottom", fontsize=fs)


# ------------------------------------------------------------ 지도
def draw_world(ax, lon=(-170, 190), lat=(-57, 78)):
    for f in WORLD["features"]:
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            ring = np.array(poly[0], dtype=float)
            if ring[:, 0].max() > 170 and ring[:, 0].min() < -170:
                ring[:, 0] = np.where(ring[:, 0] < 0, ring[:, 0] + 360, ring[:, 0])
            elif ring[:, 0].max() < -170 + 0.0:
                ring[:, 0] = ring[:, 0] + 360
            ax.add_patch(Polygon(ring, closed=True, fc="#eceae6", ec="#b7bac0", lw=0.25))
    ax.set_xlim(*lon); ax.set_ylim(*lat); ax.set_aspect("equal"); ax.axis("off")
    ax.plot([lon[0], lon[1]], [0, 0], color="#c2c5ca", lw=0.4, ls=(0, (3, 3)))


CITY = {"London": (-0.1, 51.5), "NewYork": (-74.0, 40.7), "Tokyo": (139.7, 35.7), "Paris": (2.35, 48.9),
        "Singapore": (103.8, 1.35), "Sydney": (151.2, -33.9), "SaoPaulo": (-46.6, -23.5), "Nairobi": (36.8, -1.3),
        "SanJose": (-121.9, 37.3), "Munich": (11.6, 48.1), "Bangalore": (77.6, 13.0), "HoChiMinh": (106.7, 10.8),
        "Jakarta": (106.8, -6.2), "Monterrey": (-100.3, 25.7), "Warsaw": (21.0, 52.2), "Dubai": (55.3, 25.2)}


def bm06():
    f, ax = plt.subplots(figsize=(W, 1.75))
    draw_world(ax)
    spec = [("(가)", "London", "o", (-22, 9)), ("(나)", "NewYork", "o", (-28, -14)), ("(다)", "Tokyo", "o", (5, 7)),
            ("(라)", "Paris", "o", (6, -10)), ("(마)", "Singapore", "D", (5, 6)), ("(바)", "Sydney", "D", (5, -8)),
            ("(사)", "SaoPaulo", "s", (5, -8)), ("(아)", "Nairobi", "s", (5, 6))]
    for name, c, m, off in spec:
        x, y = CITY[c]
        if m == "o":
            ax.scatter([x], [y], s=26, marker="o", facecolor="white", edgecolor=G1, linewidth=0.9, zorder=5)
        elif m == "D":
            ax.scatter([x], [y], s=20, marker="D", facecolor=G3, edgecolor=G1, linewidth=0.7, zorder=5)
        else:
            ax.scatter([x], [y], s=12, marker="o", facecolor=G1, edgecolor=G1, zorder=5)
        ax.text(x + off[0], y + off[1], name, fontsize=6.2, fontweight="bold", color=NAVY, zorder=6)
    ax.legend(handles=[Line2D([], [], marker="o", ls="", mfc="white", mec=G1, ms=5, label="점수 1,300 이상"),
                       Line2D([], [], marker="D", ls="", mfc=G3, mec=G1, ms=4.2, label="1,100~1,300"),
                       Line2D([], [], marker="o", ls="", mfc=G1, mec=G1, ms=3.4, label="1,100 미만")],
              loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=3, frameon=False, fontsize=6.3, handletextpad=0.2, columnspacing=1.0)
    save(f, OUT + "BM06.svg")


def bm11():
    f, ax = plt.subplots(figsize=(W, 1.9))
    draw_world(ax)
    HQ = ["Tokyo"]; RD = ["SanJose", "Munich", "Bangalore"]; FA = ["HoChiMinh", "Jakarta", "Monterrey", "Warsaw"]
    SA = ["NewYork", "London", "Sydney", "SaoPaulo", "Dubai"]
    for c in SA:
        ax.scatter(*CITY[c], s=12, marker="o", facecolor=G1, edgecolor="white", linewidth=0.3, zorder=5)
    for c in FA:
        ax.scatter(*CITY[c], s=20, marker="s", facecolor=G2, edgecolor=G1, linewidth=0.5, zorder=6)
    for c in RD:
        ax.scatter(*CITY[c], s=26, marker="^", facecolor="white", edgecolor=G1, linewidth=0.8, zorder=6)
    for c in HQ:
        ax.scatter(*CITY[c], s=60, marker="*", facecolor=BURG, edgecolor=BURG, linewidth=0.3, zorder=7)
    ax.legend(handles=[Line2D([], [], marker="*", ls="", mfc=BURG, mec=BURG, ms=7, label="본사"),
                       Line2D([], [], marker="^", ls="", mfc="white", mec=G1, ms=5, label="연구소"),
                       Line2D([], [], marker="s", ls="", mfc=G2, mec=G1, ms=4.5, label="생산 공장"),
                       Line2D([], [], marker="o", ls="", mfc=G1, mec=G1, ms=3.8, label="판매 법인")],
              loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=4, frameon=False, fontsize=6.4, handletextpad=0.2, columnspacing=1.2)
    save(f, OUT + "BM11.svg")


# ------------------------------------------------------------ 일반 차트
def bm02():
    f, axs = plt.subplots(1, 2, figsize=(W, 1.6))
    yrs = ["1990", "2000", "2010", "2020"]
    axs[0].plot(yrs, [1.0, 1.7, 2.6, 4.2], marker="o", color=G1, ms=3.4)
    for i, v in enumerate([1.0, 1.7, 2.6, 4.2]):
        axs[0].text(i, v + 0.25, "%.1f" % v, ha="center", fontsize=6.2)
    axs[0].set_ylim(0, 5.2); axs[0].set_title("(가) 국제 항공 여객 수(억 명)", fontsize=6.4, loc="left", pad=3)
    axs[1].plot(yrs, [35, 42, 51, 56], marker="s", color=G1, ms=3.4)
    for i, v in enumerate([35, 42, 51, 56]):
        axs[1].text(i, v + 2.2, "%d" % v, ha="center", fontsize=6.2)
    axs[1].set_ylim(20, 66); axs[1].set_title("(나) 세계 총생산 대비 교역 비중(%)", fontsize=6.4, loc="left", pad=3)
    for a in axs: a.tick_params(axis="x", labelsize=6.2); a.set_xlim(-0.4, 3.4)
    f.subplots_adjust(wspace=0.3)
    save(f, OUT + "BM02.svg")


def bm05():
    f, axs = plt.subplots(1, 2, figsize=(W, 1.7), gridspec_kw=dict(width_ratios=[1, 1.25]))
    b = axs[0].bar(["적용 전", "적용 후"], [100, 132], width=0.5, color=[GR[2], GR[0]], edgecolor=G1, linewidth=0.5)
    lab(axs[0], b, dy=3)
    axs[0].set_ylim(0, 160); axs[0].set_title("(가) ○○군 사과의 평균\n판매 가격 지수", fontsize=6.3, loc="left", pad=3, linespacing=1.2)
    b = axs[1].bar(["조성 전", "1년 후", "2년 후"], [12, 21, 31], width=0.5, color=[GR[2], GR[1], GR[0]], edgecolor=G1, linewidth=0.5)
    lab(axs[1], b, dy=0.8)
    axs[1].set_ylim(0, 38); axs[1].set_title("(나) △△군 연간 방문객(만 명)", fontsize=6.3, loc="left", pad=3)
    for a in axs: a.tick_params(axis="x", labelsize=6.2)
    f.subplots_adjust(wspace=0.3)
    save(f, OUT + "BM05.svg")


def bm08():
    f, ax = plt.subplots(figsize=(W, 1.85))
    comps = ["경제", "연구·개발", "문화 교류", "거주 적합성", "환경", "교통 접근성"]
    data = {"(가)": [330, 280, 300, 270, 240, 260], "(나)": [300, 240, 260, 310, 290, 250], "(다)": [250, 210, 230, 300, 320, 280]}
    shades = ["#2b2f36", "#555a62", "#8a8f97", "#b2b6bc", "#d3d5d9", "#eceded"]
    for i, (k, v) in enumerate(data.items()):
        y = 2 - i; left = 0
        for j, x in enumerate(v):
            ax.barh(y, x, left=left, height=0.62, color=shades[j], edgecolor="white", linewidth=0.4)
            ax.text(left + x / 2, y, str(x), ha="center", va="center", fontsize=6.2, color=("white" if j < 3 else G1))
            left += x
    ax.set_yticks([2, 1, 0]); ax.set_yticklabels(list(data)); ax.set_xlim(0, 1720)
    ax.set_xticks([0, 500, 1000, 1500]); ax.set_xlabel("점수", fontsize=6.4)
    ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
    ax.legend(handles=[Patch(fc=shades[j], ec=G3, lw=0.3, label=c) for j, c in enumerate(comps)], loc="upper center",
              bbox_to_anchor=(0.5, 1.3), ncol=3, frameon=False, fontsize=6.1, handlelength=1.0, columnspacing=0.9, labelspacing=0.3)
    save(f, OUT + "BM08.svg")


def bm13():
    f, ax = fig(1.7)
    yrs = ["2016", "2017", "2018", "2019", "2020", "2021"]
    ax.plot(yrs, [100, 102, 108, 118, 125, 128], marker="o", color=G1, ms=3.4, label="P")
    ax.plot(yrs, [100, 98, 90, 82, 78, 76], marker="s", color=G2, ms=3.4, ls="--", label="Q")
    for i, (p, q) in enumerate(zip([100, 102, 108, 118, 125, 128], [100, 98, 90, 82, 78, 76])):
        if i: ax.text(i, p + 2.5, str(p), ha="center", fontsize=6); ax.text(i, q - 6.5, str(q), ha="center", fontsize=6, color=G2)
    ax.set_ylim(65, 140); ax.set_ylabel("고용자 수 지수\n(2016년=100)", fontsize=6.3)
    ax.legend(frameon=False, fontsize=6.5, loc="upper left", ncol=2)
    save(f, OUT + "BM13.svg")


def bm19():
    f, ax = plt.subplots(figsize=(W, 1.35))
    segs = ["재배 농민", "중간 상인", "가공·유통 기업", "소매"]
    data = {"일반 거래": [10, 35, 45, 10], "공정 무역": [30, 15, 40, 15]}
    shades = [G1, "#6d727a", "#a9adb3", "#d8dadd"]
    for i, (k, v) in enumerate(data.items()):
        y = 1 - i; left = 0
        for j, x in enumerate(v):
            ax.barh(y, x, left=left, height=0.6, color=shades[j], edgecolor="white", linewidth=0.5)
            ax.text(left + x / 2, y, str(x), ha="center", va="center", fontsize=6.6, color=("white" if j < 2 else G1))
            left += x
    ax.set_yticks([1, 0]); ax.set_yticklabels(list(data)); ax.set_xlim(0, 100); ax.set_xticks([0, 25, 50, 75, 100])
    ax.spines["left"].set_visible(False); ax.tick_params(axis="y", length=0)
    ax.legend(handles=[Patch(fc=shades[j], ec=G3, lw=0.3, label=c) for j, c in enumerate(segs)], loc="upper center", bbox_to_anchor=(0.5, 1.42),
              ncol=4, frameon=False, fontsize=6.0, handlelength=1.0, columnspacing=0.8)
    save(f, OUT + "BM19.svg")


def bm23():
    f, ax = fig(1.75)
    labs = ["남위\n40~60°", "남위\n20~40°", "남위\n0~20°", "북위\n0~20°", "북위\n20~40°", "북위\n40~60°", "북위\n60~80°"]
    v = [0.3, 3.5, 5.7, 27, 41, 20.5, 2.0]
    b = ax.bar(labs, v, width=0.6, color=[GR[2]] * 3 + [GR[0]] * 4, edgecolor=G1, linewidth=0.5)
    for bb, vv in zip(b, v): ax.text(bb.get_x() + bb.get_width() / 2, vv + 0.9, "%g" % vv, ha="center", fontsize=6.3)
    ax.set_ylim(0, 50); ax.set_ylabel("세계 인구 비중(%)", fontsize=6.4); ax.tick_params(axis="x", labelsize=6.0)
    save(f, OUT + "BM23.svg")


def bm24():
    f, ax = plt.subplots(figsize=(W, 2.15))
    vals = [59.4, 17.5, 9.5, 8.3, 4.8, 0.5]
    names = ["아시아", "아프리카", "유럽", "중남부 아메리카", "북아메리카", "오세아니아"]
    cols = ["#6d727a", "#9da1a8", "#c3c6cb", "#dcdee1", "#eeeff0", "#ffffff"]
    w, _ = ax.pie(vals, startangle=90, counterclock=False, colors=cols, wedgeprops=dict(width=0.42, edgecolor=G1, linewidth=0.5))
    ax.text(0, 0.08, "2021년", ha="center", fontsize=6.4); ax.text(0, -0.12, "세계 인구\n(약 80억 명)", ha="center", va="top", fontsize=6.2)
    import math
    for wedge, n, v in zip(w, names, vals):
        ang = math.radians((wedge.theta1 + wedge.theta2) / 2)
        r = 1.0
        x, y = math.cos(ang), math.sin(ang)
        ha = "left" if x >= 0 else "right"
        yy = y * 1.25
        if n == "오세아니아": yy += 0.12
        ax.annotate("%s %g%%" % (n, v), xy=(x * 0.98, y * 0.98), xytext=(x * 1.22, yy), fontsize=6.2, ha=ha, va="center",
                    arrowprops=dict(arrowstyle="-", lw=0.4, color=G2))
    ax.set_xlim(-1.75, 1.75)
    save(f, OUT + "BM24.svg")


def pyramid(ax, key, title=None, xmax=9, yticks_every=4):
    p = PD.POP[key]
    n = len(p)
    fem = [PD.female_share(i) for i in range(n)]
    for i in range(n):
        m = p[i] * (1 - fem[i]); fv = p[i] * fem[i]
        ax.barh(i, -m, height=0.82, color="#a9adb3", edgecolor=G1, linewidth=0.3)
        ax.barh(i, fv, height=0.82, color="#dcdee1", edgecolor=G1, linewidth=0.3)
    ax.axvline(0, color=G1, lw=0.5)
    ax.set_xlim(-xmax, xmax); ax.set_ylim(-0.7, n - 0.3)
    ax.set_yticks(range(0, n, yticks_every)); ax.set_yticklabels([PD.AGES[i] for i in range(0, n, yticks_every)], fontsize=5.6)
    ax.set_xticks([-8, -4, 0, 4, 8]); ax.set_xticklabels(["8", "4", "0", "4", "8"], fontsize=5.6)
    ax.tick_params(length=1.5)
    for s in ("left", "top", "right"): ax.spines[s].set_visible(False)
    ax.text(0.25, 1.0, "남", fontsize=5.8, ha="center", va="bottom", transform=ax.transAxes); ax.text(0.75, 1.0, "여", fontsize=5.8, ha="center", va="bottom", transform=ax.transAxes)
    if title: ax.set_title(title, fontsize=7, fontweight="bold", color=NAVY, pad=9)


def bm26():
    f, axs = plt.subplots(2, 2, figsize=(W, 3.35))
    for ax, (t, k) in zip(axs.flat, [("(가)", "C"), ("(나)", "A"), ("(다)", "D"), ("(라)", "B")]):
        pyramid(ax, k, t)
    f.subplots_adjust(hspace=0.35, wspace=0.42, bottom=0.085)
    f.text(0.5, 0.0, "가로축: 총인구에 대한 비율(%), 세로축: 연령(세)", ha="center", fontsize=5.8, color=G2)
    save(f, OUT + "BM26.svg")


def bm27():
    f, axs = plt.subplots(1, 2, figsize=(W, 2.2))
    for ax, (t, k) in zip(axs, [("(가)", "A"), ("(나)", "C")]):
        pyramid(ax, k, t)
    axs[0].set_xlabel("총인구에 대한 비율(%)", fontsize=5.8); axs[1].set_xlabel("총인구에 대한 비율(%)", fontsize=5.8)
    f.subplots_adjust(wspace=0.4)
    save(f, OUT + "BM27.svg")


def bm43():
    f, axs = plt.subplots(1, 2, figsize=(W, 2.2))
    for ax, (t, k) in zip(axs, [("현재", "C"), ("미래", "D")]):
        pyramid(ax, k, t)
        ax.set_xlabel("총인구에 대한 비율(%)", fontsize=5.8)
    f.subplots_adjust(wspace=0.4)
    save(f, OUT + "BM43.svg")


def bm28():
    f, ax = plt.subplots(figsize=(W, 2.15))
    t = np.linspace(0, 10, 300)
    birth = 9 + 29 / (1 + np.exp((t - 5.0) * 1.3))
    death = 10 + 26 / (1 + np.exp((t - 2.5) * 2.2)) + 3 / (1 + np.exp(-(t - 8.5) * 2))
    ax.plot(t, birth, color=G1, lw=1.1, ls="--"); ax.plot(t, death, color=G1, lw=1.1)
    for x in (2, 4, 6, 8): ax.axvline(x, color=G4, lw=0.6)
    for i in range(5):
        ax.text(1 + 2 * i, 45.5, "%d단계" % (i + 1), ha="center", fontsize=6.6, fontweight="bold", color=NAVY)
    ax.annotate("(가)", xy=(1.2, 38.2), xytext=(1.2, 42.3), fontsize=7, fontweight="bold", ha="center", arrowprops=dict(arrowstyle="-", lw=0.4))
    ax.annotate("(나)", xy=(5.6, 10.1), xytext=(5.6, 4.0), fontsize=7, fontweight="bold", ha="center", arrowprops=dict(arrowstyle="-", lw=0.4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 49); ax.set_xticks([]); ax.set_yticks([5, 40]); ax.set_yticklabels(["낮음", "높음"], fontsize=6.4)
    ax.set_xlabel("시간(경제 발전 수준) →", fontsize=6.4); ax.set_ylabel("출생률과 사망률", fontsize=6.4)
    save(f, OUT + "BM28.svg")


def bm32():
    f, axs = plt.subplots(2, 1, figsize=(W, 3.5))
    panels = [("(가) 인구 유출국과 유입국(2020년, 만 명)", ["인도", "멕시코", "러시아", "중국", "미국", "독일", "사우디아라비아", "러시아"], [1787, 1186, 1076, 1046, 5063, 1576, 1345, 1164]),
              ("(나) 난민 유출국과 유입국(2022년, 만 명)", ["시리아", "우크라이나", "아프가니스탄", "베네수엘라", "튀르키예", "이란", "콜롬비아", "독일"], [654, 568, 566, 545, 357, 343, 246, 208])]
    for ax, (ttl, names, vals) in zip(axs, panels):
        y = [8, 7, 6, 5, 3.6, 2.6, 1.6, 0.6]
        cols = [GR[2]] * 4 + [GR[0]] * 4
        ax.barh(y, vals, height=0.75, color=cols, edgecolor=G1, linewidth=0.4)
        for yy, n, v in zip(y, names, vals):
            ax.text(-max(vals) * 0.02, yy, n, ha="right", va="center", fontsize=6.3)
            ax.text(v + max(vals) * 0.015, yy, "{:,}".format(v), ha="left", va="center", fontsize=6.2)
        ax.set_yticks([]); ax.set_xlim(0, max(vals) * 1.18); ax.set_ylim(0, 9)
        ax.spines["left"].set_visible(False); ax.tick_params(axis="x", labelsize=6)
        ax.set_title(ttl, fontsize=6.6, loc="left", pad=3)
        ax.legend(handles=[Patch(fc=GR[2], ec=G1, lw=0.4, label="유출국"), Patch(fc=GR[0], ec=G1, lw=0.4, label="유입국")], frameon=False,
                  fontsize=6.0, loc="lower right", handlelength=1.0)
    f.subplots_adjust(left=0.28, hspace=0.4)
    save(f, OUT + "BM32.svg")


def bm38():
    f, axs = plt.subplots(1, 2, figsize=(W, 1.7))
    b = axs[0].bar(["수도권", "비도시 지역"], [12, -9], width=0.5, color=[GR[0], GR[2]], edgecolor=G1, linewidth=0.5)
    axs[0].axhline(0, color=G1, lw=0.6)
    axs[0].text(0, 13, "+12", ha="center", fontsize=6.4); axs[0].text(1, -13, "−9", ha="center", fontsize=6.4)
    axs[0].set_ylim(-18, 18); axs[0].set_title("(가) 청장년층 순이동(만 명)", fontsize=6.3, loc="left", pad=3)
    b = axs[1].bar(["수도권", "비도시 지역"], [12, 27], width=0.5, color=[GR[2], GR[0]], edgecolor=G1, linewidth=0.5)
    lab(axs[1], b, dy=0.8); axs[1].set_ylim(0, 34); axs[1].set_title("(나) 노년층 비율(%)", fontsize=6.3, loc="left", pad=3)
    for a in axs: a.tick_params(axis="x", labelsize=6.2)
    f.subplots_adjust(wspace=0.32)
    save(f, OUT + "BM38.svg")


def bm45():
    f, ax = fig(1.75)
    yrs = [1950, 1970, 1990, 2010, 2020]
    a = [18, 25, 35, 46, 51]; b = [52, 62, 71, 77, 80]
    ax.plot(yrs, a, marker="o", color=G1, ms=3.4, label="개발 도상국"); ax.plot(yrs, b, marker="s", color=G2, ms=3.4, ls="--", label="선진국")
    for x, v in zip(yrs, a): ax.text(x, v - 7, str(v), ha="center", fontsize=6.1)
    for x, v in zip(yrs, b): ax.text(x, v + 3, str(v), ha="center", fontsize=6.1, color=G2)
    ax.set_ylim(0, 95); ax.set_xticks(yrs); ax.set_ylabel("도시 거주 인구 비율(%)", fontsize=6.3)
    ax.legend(frameon=False, fontsize=6.4, loc="lower right")
    save(f, OUT + "BM45.svg")


if __name__ == "__main__":
    for fn in (bm02, bm05, bm06, bm08, bm11, bm13, bm19, bm23, bm24, bm26, bm27, bm28, bm32, bm38, bm43, bm45):
        fn(); print("ok", fn.__name__)

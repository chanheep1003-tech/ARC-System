import sys
sys.path.insert(0, "/home/user/ARC-System/works")
sys.path.insert(0, "/home/user/ARC-System/works/C")
from figlib import *
import numpy as np
from matplotlib.patches import Rectangle, Patch
from figs_c import canvas, tag

OUT = "/home/user/ARC-System/works/C/fig/"
HATCH = ["", "////", "...."]


def cs06():
    f, ax = plt.subplots(figsize=(W, 1.75))
    cats = ["목적상", "형식상", "방법상", "내용상"]
    data = {"2021년": [3, 6, 18, 3], "2023년": [4, 6, 24, 6]}
    fcs = ["white", G4, G1, G3]
    y = [1, 0]
    for yy, (k, v) in zip(y, data.items()):
        left = 0
        for c, n, fc in zip(cats, v, fcs):
            ax.barh(yy, n, left=left, height=0.52, color=fc, ec=G1, lw=0.7, zorder=2)
            ax.text(left + n / 2, yy, "%d" % n, ha="center", va="center", fontsize=6.6, color="white" if fc == G1 else G1, fontweight="bold" if fc == G1 else "normal")
            left += n
        ax.text(left + 0.8, yy, "계 %d건" % sum(v), va="center", fontsize=6.4)
    ax.set_yticks(y); ax.set_yticklabels(list(data.keys()), fontsize=6.6)
    ax.set_xlim(0, 50); ax.set_xlabel("위헌 결정 건수", fontsize=6.3); ax.tick_params(axis="x", labelsize=6.2)
    ax.legend(handles=[Patch(fc=fc, ec=G1, label=c + " 한계 위반") for fc, c in zip(fcs, cats)], loc="upper center",
              bbox_to_anchor=(0.5, 1.30), ncol=4, fontsize=5.6, frameon=False, handlelength=1.0, columnspacing=0.8)
    save(f, OUT + "CS06.svg")


def cs10():
    f, ax = canvas(2.75, 100, 100)
    L = (50, 90); A = (12, 13); S = (88, 13)

    def nd(c, name, sub):
        ax.add_patch(Rectangle((c[0] - 12, c[1] - 7), 24, 14, fc=G5, ec=G1, lw=0.8, zorder=3))
        ax.text(c[0], c[1] + 1.6, name, ha="center", va="center", fontsize=6.8, fontweight="bold", color=NAVY, zorder=4)
        ax.text(c[0], c[1] - 3.4, sub, ha="center", va="center", fontsize=5.6, color=G2, zorder=4)
    nd(L, "입법부", "국회"); nd(A, "행정부", "대통령·정부"); nd(S, "사법부", "법원")

    def seg(p, q, t0, t1):
        return ((p[0] + (q[0] - p[0]) * t0, p[1] + (q[1] - p[1]) * t0), (q[0] - (q[0] - p[0]) * t1, q[1] - (q[1] - p[1]) * t1))

    def draw(p, q, sign, lab, ha, lx_extra=0.0, ly_extra=0.0, off=3.3, pos=None):
        (x1, y1), (x2, y2) = p, q
        dx, dy = x2 - x1, y2 - y1
        n = (dx * dx + dy * dy) ** 0.5
        nx, ny = -dy / n * sign, dx / n * sign
        a = (x1 + nx * off, y1 + ny * off); b = (x2 + nx * off, y2 + ny * off)
        ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="-|>", lw=1.0, color=G1, mutation_scale=8, shrinkA=0, shrinkB=0))
        mx, my = (a[0] + b[0]) / 2 + nx * 2.2 + lx_extra, (a[1] + b[1]) / 2 + ny * 2.2 + ly_extra
        if pos:
            mx, my = pos
        ax.text(mx, my, lab, fontsize=5.9, color=BURG, fontweight="bold", ha=ha, va="center", zorder=6,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    # 입법 <-> 행정 (왼쪽 변)
    p, q = seg(L, A, 0.27, 0.27)
    draw(p, q, +1, "ㄱ 국정 감사·조사권", "right")      # 입법 -> 행정, 바깥쪽(왼쪽)
    draw(q, p, +1, "ㄴ 명령·규칙 심사", "left", pos=(27, 55))          # 행정 -> 입법, 안쪽
    # 입법 <-> 사법 (오른쪽 변)
    p, q = seg(L, S, 0.27, 0.27)
    draw(q, p, +1, "ㅁ 위헌 법률 심판 제청", "right", pos=(73, 37))    # 사법 -> 입법 (안쪽)
    draw(p, q, +1, "ㅂ 탄핵소추", "left")                # 입법 -> 사법 (바깥쪽)
    # 행정 <-> 사법 (아래 변)
    p, q = (A[0] + 13, A[1]), (S[0] - 13, S[1])
    draw(q, p, +1, "ㄷ 사면권", "center", ly_extra=-1.2)   # 사법 -> 행정 (위쪽 화살표)
    draw(p, q, +1, "ㄹ 대법원장 임명", "center", ly_extra=1.2)          # 행정 -> 사법 (아래쪽)
    ax.set_ylim(0, 100)
    save(f, OUT + "CS10.svg")


def grouped(ax, labels, series, names, colors, hatches, ylim, lab_fs=6.3):
    n = len(series); w = 0.8 / n
    x = np.arange(len(labels))
    for i, (s, nm, c, h) in enumerate(zip(series, names, colors, hatches)):
        b = ax.bar(x - 0.4 + w * (i + 0.5), s, w * 0.92, color=c, ec=G1, lw=0.7, hatch=h, label=nm, zorder=2)
        for r in b:
            ax.text(r.get_x() + r.get_width() / 2, r.get_height() + ylim * 0.012, "%d" % r.get_height(), ha="center", va="bottom", fontsize=lab_fs)
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=6.6)
    ax.set_ylim(0, ylim); ax.tick_params(axis="y", labelsize=6.2)


def cs11():
    f, ax = plt.subplots(figsize=(W, 1.95))
    grouped(ax, ["A국", "B국", "C국"], [[4, 1, 3], [3, 6, 2], [3, 1, 4]], ["입법부", "행정부", "사법부"],
            ["white", G1, G4], ["", "", "////"], 7.6)
    ax.set_ylabel("행사할 수 있는 견제 수단 수", fontsize=6.0)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.2), ncol=3, fontsize=6.2, frameon=False, handlelength=1.2,
              title="견제하는 기관", title_fontsize=6.0)
    save(f, OUT + "CS11.svg")


def cs14():
    f, ax = plt.subplots(figsize=(W, 1.95))
    grouped(ax, ["2020", "2021", "2022", "2023"], [[9, 12, 7, 15], [2, 5, 0, 3]],
            ["거부권 행사 건수", "재의결로 확정된 건수"], [G4, G1], ["", ""], 18)
    ax.set_ylabel("건수", fontsize=6.3); ax.set_yticks(range(0, 19, 3))
    ax.legend(loc="upper left", fontsize=6.2, frameon=False, handlelength=1.2)
    save(f, OUT + "CS14.svg")


def flow(ax, y, h, letter, text, w=86, x=7, fc="white", ec=G1, fs=6.2):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=0.8, zorder=2))
    if letter:
        ax.text(x + 2.2, y + h / 2, letter, fontsize=6.8, fontweight="bold", color=NAVY, va="center")
        ax.text(x + 12, y + h / 2, text, fontsize=fs, color=G1, va="center", linespacing=1.35)
    else:
        ax.text(x + w / 2, y + h / 2, text, fontsize=fs, color=G1, va="center", ha="center", linespacing=1.35)


def dn(ax, x, y1, y2, color=G1):
    ax.annotate("", xy=(x, y2), xytext=(x, y1), arrowprops=dict(arrowstyle="-|>", lw=0.9, color=color, mutation_scale=7))


def cs15():
    f, ax = canvas(2.6, 100, 100)
    flow(ax, 87, 12, None, "공권력의 행사 또는 불행사로 국민의 기본권이 침해됨", fc=G5, fs=6.2)
    dn(ax, 50, 87, 77)
    flow(ax, 65, 12, "(가)", "행정 심판, 소송 등 다른 법적 구제 절차를 거침")
    dn(ax, 50, 65, 55)
    flow(ax, 43, 12, "(나)", "국민이 헌법재판소에 헌법소원을 청구함")
    dn(ax, 50, 43, 33)
    flow(ax, 21, 12, "(다)", "헌법재판소가 심판함")
    ax.annotate("", xy=(27, 7), xytext=(27, 21), arrowprops=dict(arrowstyle="-|>", lw=0.9, color=BURG, mutation_scale=7))
    ax.annotate("", xy=(73, 7), xytext=(73, 21), arrowprops=dict(arrowstyle="-|>", lw=0.9, color=G1, mutation_scale=7))
    ax.text(29, 14, "인용", fontsize=6.0, color=BURG, va="center", fontweight="bold")
    ax.text(75, 14, "기각", fontsize=6.0, color=G1, va="center", fontweight="bold")
    ax.add_patch(Rectangle((4, -5), 46, 12, fc="white", ec=BURG, lw=0.8))
    ax.text(27, 1, "침해한 공권력의 행사를\n취소하거나 위헌임을 확인함", fontsize=5.8, color=BURG, ha="center", va="center", linespacing=1.3)
    ax.add_patch(Rectangle((52, -5), 46, 12, fc="white", ec=G1, lw=0.8))
    ax.text(75, 1, "청구 이유가 없다고\n판단함", fontsize=5.8, color=G1, ha="center", va="center", linespacing=1.3)
    ax.set_ylim(-7, 100)
    save(f, OUT + "CS15.svg")


def cs18():
    f, ax = canvas(2.6, 100, 100)
    flow(ax, 86, 13, None, "갑은 ○○시로부터 영업 정지 처분을 받고\n행정 소송을 제기하여 재판을 받고 있다.", fc=G5, fs=6.0)
    dn(ax, 50, 86, 76)
    flow(ax, 62, 14, "(가)", "재판 중 갑이 ‘처분의 근거가 된 법률이 위헌’이라며\n법원에 헌법재판소 심판 제청을 신청함", fs=5.9)
    dn(ax, 50, 62, 52)
    flow(ax, 40, 12, "(나)", "법원이 제청 신청을 기각함")
    dn(ax, 50, 40, 30)
    flow(ax, 18, 12, "(다)", "갑이 헌법재판소에 직접 헌법소원을 청구함")
    dn(ax, 50, 18, 8)
    flow(ax, -4, 12, None, "헌법재판소의 심판", fc=G5)
    ax.set_ylim(-6, 100)
    save(f, OUT + "CS18.svg")


if __name__ == "__main__":
    for fn in (cs06, cs10, cs11, cs14, cs15, cs18):
        fn()
    print("ok")

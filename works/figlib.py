"""ARC 시각자료 공통 스타일 (흑백 안전, 얇은 선, 한글 Noto Sans KR)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from pathlib import Path

for f in ("NotoSansKR-Regular.otf", "NotoSansKR-Medium.otf", "NotoSansKR-Bold.otf"):
    fm.fontManager.addfont(str(Path.home() / ".fonts" / f))

NAVY = "#1F2A44"; BURG = "#7A2E35"; G1 = "#2b2f36"; G2 = "#6b7078"; G3 = "#a9adb3"; G4 = "#d5d7db"; G5 = "#eceae5"

plt.rcParams.update({
    "font.family": "Noto Sans KR", "font.size": 7.2, "svg.fonttype": "path",
    "axes.linewidth": 0.6, "axes.edgecolor": G1, "xtick.major.width": 0.5, "ytick.major.width": 0.5,
    "xtick.major.size": 2.2, "ytick.major.size": 2.2, "axes.spines.top": False, "axes.spines.right": False,
    "axes.unicode_minus": False, "lines.linewidth": 1.0, "figure.dpi": 100, "savefig.dpi": 100,
})

W = 3.30  # 단 폭 84mm ≈ 3.3in


def fig(h=2.0, w=W):
    return plt.subplots(figsize=(w, h))


def save(f, path):
    f.savefig(path, format="svg", bbox_inches="tight", pad_inches=0.04, transparent=False, facecolor="white")
    plt.close(f)


def box(ax, x, y, w, h, text, fc="white", ec=G1, lw=0.7, fs=6.8, bold=False, tc=G1, ls="-"):
    from matplotlib.patches import Rectangle
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, ls=ls, zorder=2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", color=tc, zorder=3, linespacing=1.25)


def arrow(ax, x1, y1, x2, y2, lw=0.8, style="-|>", color=G1, ls="-"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, lw=lw, color=color, shrinkA=0, shrinkB=0, ls=ls, mutation_scale=7), zorder=1)

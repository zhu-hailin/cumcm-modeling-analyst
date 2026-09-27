#!/usr/bin/env python3
"""Generate README documentation graphics, not scientific evidence.

Requires matplotlib and a CJK font. --font-file accepts an installed font;
no font binary is distributed. Editable SVG masters and outlined display SVGs
are written together. Optional PNG previews are for visual review only.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

ROOT = Path(__file__).resolve().parents[1]
INK, MUTED, PAPER = "#183A3A", "#546C6A", "#F7F7F0"
TEAL, LINE, ORANGE = "#137E73", "#D2DFD8", "#BD623A"


def font_path(explicit: Path | None) -> Path:
    if explicit:
        if not explicit.is_file():
            raise ValueError(f"Font not found: {explicit}")
        return explicit
    for candidate in ("Noto Sans CJK SC", "Microsoft YaHei", "Source Han Sans SC"):
        try:
            return Path(font_manager.findfont(candidate, fallback_to_default=False))
        except ValueError:
            continue
    raise ValueError("Install a CJK font or supply --font-file")


def canvas(width: int, height: int):
    fig = plt.figure(figsize=(width / 100, height / 100), dpi=100, facecolor=PAPER)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, width)
    ax.set_ylim(height, 0)
    ax.axis("off")
    return fig, ax


def text(ax, x, y, label, size=16, color=INK, weight="normal", **kwargs):
    return ax.text(x, y, label, fontsize=size, color=color, weight=weight,
                   va="top", linespacing=1.55, **kwargs)


def box(ax, x, y, w, h, color="white", edge=LINE, radius=20):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0,rounding_size={radius}",
                 linewidth=1, facecolor=color, edgecolor=edge))


def arrow(ax, start, end, color=TEAL, width=2, style="-|>"):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle=style,
                 mutation_scale=15, linewidth=width, color=color))


def hero():
    fig, ax = canvas(1600, 830)
    text(ax, 72, 53, "CUMCM / MODELING ANALYST", 15, TEAL, "bold")
    box(ax, 1370, 43, 155, 43, "#E1EEE8", "#E1EEE8", 21)
    text(ax, 1447, 51, "VERSION 12.0", 11, TEAL, "bold", ha="center")
    text(ax, 70, 135, "让建模思路\n成为完整论证", 45, INK, "bold")
    text(ax, 75, 336, "为什么这样建模？证据支持什么？\n怎样写成读者能理解的论文？", 21, MUTED)
    text(ax, 75, 456, "国赛实战经验  ·  逐问确认  ·  随题成稿", 18, TEAL, "bold")
    text(ax, 75, 507, "单代理或三角色，同一套质量标准。", 17, MUTED)

    box(ax, 836, 132, 690, 460, "#EEF3EB", "#EEF3EB", 25)
    text(ax, 866, 157, "协作由你选择", 20, INK, "bold")
    text(ax, 866, 204, "主 agent 统筹 · 统一口径、确认与验收", 15, MUTED)
    roles = [("01", "建模手", "选择依据 · 推导 · 有效性", "#FFFFFF"),
             ("02", "代码手", "真实运行 · Python 图表", "#FFFFFF"),
             ("03", "论文手", "文章主线 · 摘要 · 结果解释", "#FFFFFF")]
    for i, (num, title, desc, fill) in enumerate(roles):
        y = 263 + i * 98
        box(ax, 866, y, 630, 80, fill, LINE, 12)
        ax.add_patch(Circle((906, y + 40), 20, facecolor="#E0EEE7", edgecolor="none"))
        text(ax, 906, y + 27, num, 12, TEAL, "bold", ha="center")
        text(ax, 944, y + 22, title, 21, INK, "bold")
        text(ax, 1084, y + 27, desc, 15, MUTED)

    ax.plot([74, 1525], [661, 661], color=LINE, linewidth=1)
    columns = [(75, "论证", "模型理由与验证依据"),
               (475, "制图", "nature-figure · 赛中 Python"),
               (1015, "交付", "论文 + 支撑材料 + 清楚入口")]
    for x, title, desc in columns:
        text(ax, x, 690, title, 14, TEAL, "bold")
        text(ax, x, 730, desc, 17, INK)
    return fig


def workflow():
    fig, ax = canvas(1600, 1340)
    text(ax, 72, 48, "从题意到交付，每一步都形成证据", 30, INK, "bold")
    text(ax, 75, 113, "全题看清 · 每问确认 · 写作与图表同步推进", 18, MUTED)

    def label(y, n, title, desc):
        ax.add_patch(Circle((99, y + 32), 26, facecolor=TEAL, edgecolor="none"))
        text(ax, 99, y + 16, n, 15, "white", "bold", ha="center")
        text(ax, 151, y, title, 23, INK, "bold")
        text(ax, 151, y + 49, desc, 15, MUTED)

    label(198, "01", "选择方式，理解全题", "首次选择单代理或三角色；恢复已有选择、题意与证据。")
    box(ax, 1105, 190, 420, 96, "#E8F0E9", "#E8F0E9")
    text(ax, 1130, 210, "SINGLE  /  THREE_ROLE", 18, TEAL, "bold")
    text(ax, 1130, 249, "不开子代理，也采用相同质量标准", 13, MUTED)

    arrow(ax, (99, 275), (99, 324))
    label(329, "02", "确认当前问", "说明目标、关键假设、主 / 备用路线，再进入正式求解。")
    text(ax, 1130, 352, "后问仍需单独确认", 17, ORANGE, "bold")
    arrow(ax, (99, 405), (99, 448))

    box(ax, 73, 464, 1452, 313, "#EAF1E9", "#EAF1E9")
    text(ax, 102, 487, "03  本问协作：研究、实现、写作持续反馈", 22, INK, "bold")
    descriptions = [
        ("建模手", "为什么用这个模型？", "定义 · 推导 · 验证依据"),
        ("代码手", "如何得到可信结果？", "实现 · 运行 · Python 图表"),
        ("论文手", "怎样讲清楚判断过程？", "主线 · 摘要 · 图表解释")]
    for i, (role, question, details) in enumerate(descriptions):
        x = 102 + i * 470
        box(ax, x, 554, 430, 177, "white", LINE, 15)
        text(ax, x + 23, 572, role, 21, TEAL, "bold")
        text(ax, x + 23, 620, question, 17, INK)
        text(ax, x + 23, 664, details, 14, MUTED)
        if i < 2:
            arrow(ax, (x + 435, 638), (x + 465, 638), style="<->")
    text(ax, 103, 744, "主 agent 整合与验收；同一正式文件只有一名写入者。", 13, MUTED)

    label(825, "04", "随问出图，写清图下说明", "nature-figure + Python；每张图表下解释内容、发现、判断与边界。")
    box(ax, 1110, 815, 415, 100, "#FAEDDF", "#FAEDDF")
    text(ax, 1133, 835, "不要等到赛末才补画", 19, ORANGE, "bold")
    text(ax, 1133, 877, "后期重点核对版本、编号与排版", 13, MUTED)
    arrow(ax, (99, 901), (99, 958))
    label(964, "05", "分别核验四项完成情况", "计算完成 ≠ 完整交付完成；缺失项和边界明确说明。")
    for i, name in enumerate(("计算", "核验", "论文材料", "交付")):
        x = 1110 + i * 104
        box(ax, x, 985, 93, 48, "white", LINE, 10)
        text(ax, x + 46, 997, name, 13, INK, "bold", ha="center")
    arrow(ax, (99, 1042), (99, 1092))
    label(1098, "06", "更新交付目录，讨论下一问", "保留当前有效论文与支撑材料；验证实际文件和复现入口。")
    box(ax, 1108, 1090, 417, 100, "#E0EEE7", "#E0EEE7")
    text(ax, 1130, 1110, "论文 / 动态支撑材料 / 交付说明", 15, TEAL, "bold")
    text(ax, 1130, 1151, "草稿、审核稿与历史版本留在工作区", 12, MUTED)
    ax.plot([74, 1525], [1250, 1250], color=LINE, linewidth=1)
    text(ax, 75, 1272, "流程示意，不含赛题答案、实测成绩或获奖承诺。", 13, MUTED)
    return fig


def export(fig, basename, source_name, title, previews: Path | None):
    output = ROOT / "assets/readme-showcase"
    (output / "source").mkdir(parents=True, exist_ok=True)
    metadata = {"Date": None, "Title": title, "Description": "CUMCM v12 documentation diagram; no contest data or performance claims.", "Creator": "render_readme_assets.py"}
    with matplotlib.rc_context({"svg.fonttype": "none"}):
        fig.savefig(output / "source" / source_name, format="svg", metadata=metadata)
    with matplotlib.rc_context({"svg.fonttype": "path"}):
        fig.savefig(output / basename, format="svg", metadata=metadata)
    # Exports are actual standalone SVG documents, not images referenced by path.
    for path in (output / basename, output / "source" / source_name):
        # Matplotlib emits trailing spaces in multiline path attributes.
        svg = path.read_text("utf-8")
        path.write_text("\n".join(line.rstrip() for line in svg.splitlines()) + "\n", encoding="utf-8")
        ET.parse(path)
    if previews:
        previews.mkdir(parents=True, exist_ok=True)
        fig.savefig(previews / (Path(basename).stem + ".png"), dpi=100)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font-file", type=Path)
    parser.add_argument("--preview-dir", type=Path)
    args = parser.parse_args()
    selected = font_path(args.font_file)
    font_manager.fontManager.addfont(str(selected))
    family = font_manager.FontProperties(fname=selected).get_name()
    matplotlib.rcParams.update({"font.family": family, "svg.hashsalt": "cumcm-v12-readme", "axes.unicode_minus": False})
    export(hero(), "hero-cumcm-modeling-analyst.svg", "hero.svg", "CUMCM v12：让建模思路成为完整论证", args.preview_dir)
    export(workflow(), "cumcm-readme-workflow.svg", "workflow.svg", "CUMCM v12：可选三角色与逐问交付流程", args.preview_dir)
    print("Generated two README SVGs and editable masters; inspect the PNG previews.")


if __name__ == "__main__":
    main()

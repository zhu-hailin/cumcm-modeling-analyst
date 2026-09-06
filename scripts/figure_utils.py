"""数学建模科研绘图的轻量公共函数。

该模块只处理字体、保存和机械 QA，不规定应该画什么，也不固定颜色方案。
正式图仍需遵循 python-visualization-policy.md 的证据与视觉要求。
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager

CHINESE_FONT_CANDIDATES = (
    "Microsoft YaHei",
    "SimHei",
    "Noto Sans CJK SC",
    "Source Han Sans SC",
    "PingFang SC",
    "WenQuanYi Micro Hei",
)


def pick_chinese_font(candidates: Iterable[str] = CHINESE_FONT_CANDIDATES) -> str | None:
    """返回当前环境中第一个可用的中文字体族名称。"""
    available = {font.name for font in font_manager.fontManager.ttflist}
    return next((name for name in candidates if name in available), None)


def apply_readable_defaults(base_font_size: float = 9.0) -> str | None:
    """设置不涉及配色的基础可读性参数，并返回选中的中文字体。"""
    chinese_font = pick_chinese_font()
    sans_serif = [chinese_font] if chinese_font else []
    sans_serif.extend(["DejaVu Sans"])

    mpl.rcParams.update(
        {
            "font.size": base_font_size,
            "axes.titlesize": base_font_size,
            "axes.labelsize": base_font_size,
            "xtick.labelsize": max(base_font_size - 1, 7),
            "ytick.labelsize": max(base_font_size - 1, 7),
            "legend.fontsize": max(base_font_size - 1, 7),
            "font.sans-serif": sans_serif,
            "axes.unicode_minus": False,
            "savefig.bbox": "tight",
        }
    )
    return chinese_font


def save_figure(
    fig: plt.Figure,
    base_path: str | Path,
    *,
    formats: Iterable[str] = ("png", "svg", "pdf"),
    dpi: int = 300,
    close: bool = False,
) -> list[Path]:
    """以同一语义主干保存多格式图片。

    Parameters
    ----------
    fig:
        Matplotlib Figure。
    base_path:
        不带扩展名的目标路径，例如 ``04_results/figures/q1/paper/预测结果``。
    formats:
        输出扩展名列表。探索图可只传 ``("png",)``，正式线图建议保留矢量格式。
    dpi:
        位图输出 DPI；不改变原始数据或图形几何。
    close:
        保存后是否关闭 Figure。
    """
    base = Path(base_path)
    base.parent.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []

    for fmt in formats:
        normalized = fmt.lower().lstrip(".")
        target = base.with_suffix(f".{normalized}")
        kwargs = {"bbox_inches": "tight"}
        if normalized in {"png", "jpg", "jpeg", "tif", "tiff"}:
            kwargs["dpi"] = dpi
        fig.savefig(target, **kwargs)
        if not target.is_file() or target.stat().st_size == 0:
            raise RuntimeError(f"图片保存失败或为空：{target}")
        outputs.append(target)

    if close:
        plt.close(fig)
    return outputs


def assert_basic_labels(ax: plt.Axes) -> None:
    """对正式二维统计图执行最小标签检查。

    某些无坐标方法图/网络图不适用，应由调用者自行跳过。
    """
    if not ax.get_xlabel().strip():
        raise ValueError("缺少 x 轴标签")
    if not ax.get_ylabel().strip():
        raise ValueError("缺少 y 轴标签")

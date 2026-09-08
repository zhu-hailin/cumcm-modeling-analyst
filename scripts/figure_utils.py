"""数学建模科研绘图的轻量公共函数。

该模块只处理字体、保存和机械 QA，不规定应该画什么，也不固定颜色方案。
正式图仍需遵循 python-visualization-policy.md 的证据与视觉要求。
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable
import math
import shutil
import tempfile
import warnings

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


def apply_readable_defaults(base_font_size: float = 9.0, *, require_chinese: bool = False) -> str | None:
    """设置不涉及配色的基础可读性参数，并返回选中的中文字体。"""
    if not math.isfinite(base_font_size) or base_font_size <= 0:
        raise ValueError("基础字号必须是有限正数")
    chinese_font = pick_chinese_font()
    if chinese_font is None:
        message = "未找到候选中文字体；中文可能缺字。请配置可用字体后重新生成并检查。"
        if require_chinese:
            raise RuntimeError(message)
        warnings.warn(message, RuntimeWarning, stacklevel=2)
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
    formats: Iterable[str] | str = ("png", "svg", "pdf"),
    dpi: int = 300,
    close: bool = False,
    overwrite: bool = False,
) -> list[Path]:
    """以同一语义主干保存多格式图片。

    Parameters
    ----------
    fig:
        Matplotlib Figure。
    base_path:
        不带图片扩展名的目标主干，小数点/版本号原样保留，例如 ``参数0.1``。
    formats:
        输出扩展名列表。探索图可只传 ``("png",)``，正式线图建议保留矢量格式。
    dpi:
        位图输出 DPI；不改变原始数据或图形几何。
    close:
        全部成功保存后是否关闭 Figure；失败时保留以便修复。
    overwrite:
        默认拒绝已有文件；只在确认替换派生图时显式启用。不保证多文件事务。
    """
    base = Path(base_path)
    if not base.name:
        raise ValueError("图片主干不能为空")
    if not math.isfinite(dpi) or dpi <= 0:
        raise ValueError("DPI 必须是有限正数")
    requested = [formats] if isinstance(formats, str) else list(formats)
    if not requested or not all(isinstance(fmt, str) for fmt in requested):
        raise ValueError("至少指定一个有效图片格式")
    normalized = [fmt.strip().lower().lstrip(".") for fmt in requested]
    supported = fig.canvas.get_supported_filetypes()
    if len(set(normalized)) != len(normalized) or any(fmt not in supported for fmt in normalized):
        raise ValueError("图片格式重复或当前后端不支持")
    # with_suffix 会把“参数0.1/参数0.2”都截成“参数0.png”，因此必须追加扩展名。
    outputs = [base.parent / f"{base.name}.{fmt}" for fmt in normalized]
    for target in outputs:
        if target.is_symlink() or (target.exists() and not target.is_file()):
            raise ValueError(f"目标不是可替换的普通图片文件：{target}")
        if target.exists() and not overwrite:
            raise FileExistsError(f"图片已存在，请使用新版本路径或明确 overwrite=True：{target}")
    base.parent.mkdir(parents=True, exist_ok=True)
    # 先完整渲染所有格式；某个格式失败时不破坏已存在的正式图片。
    with tempfile.TemporaryDirectory(prefix=".figure_export_", dir=base.parent) as staging:
        for fmt, target in zip(normalized, outputs):
            temporary = Path(staging) / target.name
            fig.savefig(temporary, format=fmt, bbox_inches="tight", dpi=dpi)
            if not temporary.is_file() or temporary.stat().st_size == 0:
                raise RuntimeError(f"图片保存失败或为空：{target}")
        for target in outputs:
            temporary = Path(staging) / target.name
            if overwrite:
                temporary.replace(target)
            else:
                # 排除预检后另一写入者抢先创建目标的情况，不静默覆盖。
                with target.open("xb") as destination, temporary.open("rb") as source:
                    shutil.copyfileobj(source, destination)

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

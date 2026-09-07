#!/usr/bin/env python3
"""v11.2 competition-first 行为契约测试。

该测试不评价历史题得分，只防止后续编辑重新引入：过度加载、技术细节反复审批、
探索图论文级负担、强制推荐分、下载链接硬门、内部状态直接进入论文，或让正式
建模 Python 重新变成难以快速接手的“无区域结构代码”，以及丢失新建中文赛题项目
对简体中文文件名、注释和结果表字段的默认偏好，或把正式科研图重新默认拼成
(a)(b)(c)(d) 多面板图等回归。
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text("utf-8")


def require(text: str, source: str, *tokens: str) -> None:
    missing = [token for token in tokens if token not in text]
    if missing:
        raise AssertionError(f"{source} 缺少契约：{missing}")


def forbid(text: str, source: str, *tokens: str) -> None:
    found = [token for token in tokens if token in text]
    if found:
        raise AssertionError(f"{source} 重新引入了不应存在的硬约束：{found}")


def main() -> int:
    skill = read("SKILL.md")
    require(
        skill,
        "SKILL.md",
        "Codex 的自主执行边界",
        "已确认路线内，Agent 默认可以自主做",
        "以下情况需要用户决定",
        "探索快，定稿严",
    )

    manifest = read("manifest.yaml")
    require(manifest, "manifest.yaml", "version: 11.2", "stage1_modeling:", "literature_and_external_data:")
    always = manifest.split("routes:", 1)[0]
    forbid(always, "manifest always_load", "modeling-quality-gates.md", "source-verification-policy.md", "python-visualization-policy.md")

    stage1_block = manifest.split("stage1_modeling:", 1)[1].split("question_by_question:", 1)[0]
    require(stage1_block, "stage1_modeling route", "modeling-research-playbook.md", "modeling-quality-gates.md")
    forbid(stage1_block, "stage1_modeling route", "external-data-research-policy.md", "source-verification-policy.md")

    playbook = read("references/modeling-research-playbook.md")
    require(
        playbook,
        "modeling-research-playbook.md",
        "这不是模型清单",
        "能区分路线的小实验",
        "参数估计 / 反演 / 标定",
        "预测 / 分类 / 状态识别",
        "优化 / 调度 / 路径 / 资源配置",
        "综合评价 / 排名 / 决策",
        "一个通用研究循环",
    )

    core = read("references/core-workflow.md")
    require(
        core,
        "core-workflow.md",
        "已确认路线内默认自主执行",
        "以下情况必须交用户决定",
        "设计能区分这些机制的小实验或 EDA",
        "Requirement / Evidence 骨架",
    )

    code_policy = read("references/python-code-documentation-policy.md")
    require(
        code_policy,
        "python-code-documentation-policy.md",
        "简体中文优先、注释有效",
        "Python 文件名尽量使用简体中文语义名",
        "列名尽量使用清楚的简体中文语义",
        "`01_data/raw/` 中的官方原始列名应保持原样",
        "原字段 → 中文字段",
        "docstring 默认使用简体中文",
        "区域级注释：先让人一眼看懂“这一段在做什么”",
        "核心建模区域必须尽量写明实际模型/算法名称",
        "人工编写注释默认使用简体中文",
        "核心建模：XGBoost 回归",
        "结果验证",
    )

    q_template = read("assets/QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md")
    require(
        q_template,
        "QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md",
        "确认的是建模边界",
        "满足已确认触发条件后切换到已确认备用路线",
        "Python 文件名尽量使用清楚的**简体中文语义名**",
        "简体中文区域级注释",
        "人工编写的行内注释默认使用**简体中文**",
        "新建 `processed` 数据、CSV/XLSX 结果表",
        "原字段 → 中文字段",
        "核心建模：<实际模型/算法名称>",
        "一个图表 = 一个独立图片文件，由 Python 单独生成和保存",
        "图1、图2、图3……",
        "不为了省文件、省版面或视觉效果把独立图强行拼成 `(a)(b)(c)(d)`",
    )
    forbid(q_template, "QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md", "| 推荐指数 |", "写中文命名、带有效注释的正式 Python")

    one_pass = read("assets/STAGE2_ONE_PASS_SOLUTION_TEMPLATE.md")
    require(
        one_pass,
        "STAGE2_ONE_PASS_SOLUTION_TEMPLATE.md",
        "普通技术失败、调参失败、求解器更换或已确认备用路线触发，不单独暂停",
        "Python 文件名尽量使用清楚的**简体中文语义名**",
        "人工编写的行内注释默认使用**简体中文**",
        "新建 `processed` 数据、CSV/XLSX 结果表",
        "多阶段建模脚本用简体中文区域级注释标出主要职责",
        "核心建模区域尽量直接写明实际模型/算法名称",
        "一个图表 = 一个独立图片文件，由 Python 单独生成和保存",
        "图1、图2、图3……",
        "不为了减少文件数、节省页数或排版效果强行拼成 `(a)(b)(c)(d)`",
    )

    visualization = read("references/python-visualization-policy.md")
    require(
        visualization,
        "python-visualization-policy.md",
        "QUICK_EXPLORATION",
        "FORMAL_EVIDENCE",
        "探索图无需填写完整论文证据契约",
        "METHOD_FIGURE",
        "一个图表 = 一个独立图片文件，由 Python 单独生成并单独保存",
        "图1、图2、图3……",
        "`(a)(b)(c)(d)` 多面板图属于**例外**，不是默认风格",
        "不为了减少文件数、节省页数或“看起来更丰富”把多个本来可以独立表达的图拼成一张大图",
        "正文优先引用整张 `图3`",
    )

    source = read("references/source-verification-policy.md")
    require(
        source,
        "source-verification-policy.md",
        "访问状态与证据状态分开记录",
        "FULLTEXT_READ",
        "最终参考论文**不要求每篇被引用文献都有公开下载链接**",
    )

    ledger = read("references/model-run-ledger.md")
    require(ledger, "references/model-run-ledger.md", "同一运行元数据只维护一个权威来源", "METHOD_FIGURE")

    blueprint = read("references/paper-evidence-architecture.md")
    require(
        blueprint,
        "paper-evidence-architecture.md",
        "EARLY_SKELETON",
        "FINAL_FREEZE",
        "02_analysis/PAPER_EVIDENCE_BLUEPRINT.md",
        "05_paper/` 中的论文只引用这份蓝图",
    )

    paper = read("references/reference-paper-writing.md")
    require(
        paper,
        "reference-paper-writing.md",
        "02_analysis/PAPER_EVIDENCE_BLUEPRINT.md",
        "正式论文正文不机械展示内部 Agent 状态",
        "模型假设：每条都要有用途",
        "如何求解",
        "结果分析",
        "单图单文件、单图单图号",
        "图1、图2、图3……",
        "不为了省文件、省版面或营造“高级感”把独立图硬拼成 `(a)(b)(c)(d)`",
    )
    forbid(paper, "reference-paper-writing.md", "├─ PAPER_EVIDENCE_BLUEPRINT.md")

    audit = read("references/final-paper-audit.md")
    require(
        audit,
        "final-paper-audit.md",
        "默认一个图表对应一个独立图片文件和一个独立图号",
        "图1、图2、图3……",
        "组合 `(a)(b)(c)(d)` 只在共享坐标/尺度/图例或必须同时比较时例外使用",
    )

    audit_template = read("assets/FINAL_PAPER_AUDIT_TEMPLATE.md")
    require(
        audit_template,
        "FINAL_PAPER_AUDIT_TEMPLATE.md",
        "一个图表一个独立图片文件",
        "图1、图2、图3……",
        "强行使用 `(a)(b)(c)(d)`",
    )

    print("competition_first_contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
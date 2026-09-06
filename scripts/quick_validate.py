#!/usr/bin/env python3
"""对 Skill 路由、链接、关键契约和辅助脚本做快速静态校验。"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

REQUIRED_FILES = (
    "SKILL.md",
    "manifest.yaml",
    "references/problem-ingestion-security.md",
    "references/core-workflow.md",
    "references/modeling-research-playbook.md",
    "references/modeling-quality-gates.md",
    "references/model-run-ledger.md",
    "references/paper-evidence-architecture.md",
    "references/python-visualization-policy.md",
    "references/reference-paper-writing.md",
    "references/source-verification-policy.md",
    "references/final-paper-audit.md",
    "assets/QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md",
    "assets/STAGE2_ONE_PASS_SOLUTION_TEMPLATE.md",
    "assets/PAPER_EVIDENCE_BLUEPRINT_TEMPLATE.md",
    "scripts/run_record.py",
    "scripts/figure_utils.py",
    "scripts/delivery_check.py",
    "tests/test_old_problem_forward_contract.py",
    "tests/test_competition_first_contract.py",
    ".github/workflows/validate.yml",
)

REQUIRED_TOKENS = {
    "references/core-workflow.md": (
        "QUALITY_GATES_ARE_AUDITORS_NOT_MODEL_SELECTORS",
        "已确认路线内默认自主执行",
        "SCIENTIFIC_VALIDITY",
        "CONTEST_TASK_COMPLETION",
        "PAPER_EVIDENCE_BLUEPRINT_READY",
    ),
    "references/modeling-research-playbook.md": (
        "这不是模型清单",
        "机理 / 数值模型",
        "参数估计 / 反演 / 标定",
        "预测 / 分类 / 状态识别",
        "优化 / 调度 / 路径 / 资源配置",
        "综合评价 / 排名 / 决策",
        "一个通用研究循环",
    ),
    "references/problem-ingestion-security.md": (
        "INGESTION_SECURITY_AUDIT_REQUIRED",
        "INGESTION_SECURITY_AUDIT_PASSED",
        "INGESTION_SECURITY_AUDIT_LOCKED",
        "Evidence ID",
        "可见性上下文",
    ),
    "references/python-visualization-policy.md": (
        "QUICK_EXPLORATION",
        "FORMAL_EVIDENCE",
        "METHOD_FIGURE",
        "AI_COMMUNICATION_ONLY",
        "N/A（方法结构图）",
    ),
    "references/paper-evidence-architecture.md": (
        "EARLY_SKELETON",
        "FINAL_FREEZE",
        "PAPER_CORE",
        "PAPER_SUPPORT",
        "RUN_ONLY",
        "PAPER_EVIDENCE_BLUEPRINT_READY",
        "FIGURE_NOT_NEEDED",
        "NOT_IDENTIFIABLE",
    ),
    "references/source-verification-policy.md": (
        "PAGE_VERIFIED",
        "DOWNLOAD_VERIFIED",
        "FULLTEXT_READ",
        "最终参考论文**不要求每篇被引用文献都有公开下载链接**",
    ),
    "references/model-run-ledger.md": (
        "FINAL_RUN_ID",
        "METHOD_FIGURE",
        "SUPERSEDED",
    ),
}

FORBIDDEN_GENERIC_TERMS = ("高钾", "铅钡", "古代玻璃", "桂电")
POLICY_PLACEHOLDERS = re.compile(r"(?im)^\s*(?:TODO|TBD|FIXME)\s*:")
ROUTE_PATH = re.compile(r"^\s*-\s+((?:references|assets)/[^\s#]+\.md)\s*$")
MD_LINK = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")


def resolve_markdown_link(source: Path, target: str) -> Path | None:
    target = target.strip().split("#", 1)[0]
    if not target or target.startswith(("http://", "https://", "mailto:", "data:")):
        return None
    if target.startswith("/"):
        return None
    return (source.parent / target).resolve()


def validate(root: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    checks = 0

    for relative in REQUIRED_FILES:
        checks += 1
        if not (root / relative).is_file():
            errors.append(f"缺少必需文件：{relative}")

    manifest = root / "manifest.yaml"
    if manifest.is_file():
        text = manifest.read_text("utf-8")
        checks += 1
        if "version: 11.2" not in text:
            errors.append("manifest 版本未更新到 11.2")
        for line_no, line in enumerate(text.splitlines(), 1):
            match = ROUTE_PATH.match(line)
            if not match:
                continue
            checks += 1
            if not (root / match.group(1)).is_file():
                errors.append(f"manifest 路由断链：{match.group(1)}（第 {line_no} 行）")

        always = text.split("routes:", 1)[0]
        checks += 1
        if "modeling-quality-gates.md" in always or "python-visualization-policy.md" in always:
            errors.append("深层建模/绘图 policy 不应进入 always_load")

    for md_file in root.rglob("*.md"):
        text = md_file.read_text("utf-8")
        for target in MD_LINK.findall(text):
            resolved = resolve_markdown_link(md_file, target)
            if resolved is None:
                continue
            checks += 1
            if not resolved.exists():
                errors.append(f"Markdown 链接断链：{md_file.relative_to(root)} -> {target}")

    for relative, tokens in REQUIRED_TOKENS.items():
        path = root / relative
        if not path.is_file():
            continue
        text = path.read_text("utf-8")
        for token in tokens:
            checks += 1
            if token not in text:
                errors.append(f"关键契约缺失：{relative} 未包含 {token}")

    generic_files = [root / "SKILL.md", root / "manifest.yaml"]
    generic_files.extend((root / "references").glob("*.md"))
    for path in generic_files:
        if not path.is_file():
            continue
        text = path.read_text("utf-8")
        for term in FORBIDDEN_GENERIC_TERMS:
            checks += 1
            if term in text:
                errors.append(f"发现题目专用硬编码：{path.relative_to(root)} -> {term}")
        checks += 1
        if POLICY_PLACEHOLDERS.search(text):
            errors.append(f"发现未解决占位内容：{path.relative_to(root)}")

    for py_file in list((root / "scripts").glob("*.py")) + list((root / "tests").glob("*.py")):
        checks += 1
        try:
            ast.parse(py_file.read_text("utf-8"), filename=str(py_file))
        except SyntaxError as exc:
            errors.append(f"Python 语法错误：{py_file.relative_to(root)}:{exc.lineno}: {exc.msg}")

    skill = root / "SKILL.md"
    if skill.is_file():
        checks += 1
        size = skill.stat().st_size
        if size > 14_000:
            warnings.append(f"SKILL.md 已达到 {size} 字节，建议继续保持入口轻量")

    q_template = root / "assets/QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md"
    if q_template.is_file():
        text = q_template.read_text("utf-8")
        checks += 2
        if "| 推荐指数 |" in text:
            errors.append("逐题模板重新把数值推荐指数设为固定字段")
        if "写中文命名" in text or "中文源码结构" in text:
            errors.append("逐题模板重新把中文源码命名设为硬要求")

    visualization = root / "references/python-visualization-policy.md"
    if visualization.is_file():
        text = visualization.read_text("utf-8")
        checks += 1
        if "探索图无需填写完整论文证据契约" not in text:
            errors.append("绘图规范没有明确给探索图轻量通道")

    return {
        "status": "PASS" if not errors else "FAIL",
        "checks": checks,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = validate(args.root.resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"quick_validate: {result['status']} ({result['checks']} checks)")
        for warning in result["warnings"]:
            print(f"WARNING: {warning}")
        for error in result["errors"]:
            print(f"ERROR: {error}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())

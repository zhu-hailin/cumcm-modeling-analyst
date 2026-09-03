#!/usr/bin/env python3
"""对 Skill 路由、Markdown 链接和关键契约做快速静态校验。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = (
    "SKILL.md",
    "manifest.yaml",
    "references/problem-ingestion-security.md",
    "references/core-workflow.md",
    "references/modeling-quality-gates.md",
    "references/paper-evidence-architecture.md",
    "references/blind-benchmark-provenance.md",
    "references/python-visualization-policy.md",
    "references/reference-paper-writing.md",
    "references/final-paper-audit.md",
    "references/paper-evaluation-protocol.md",
    "references/python-code-documentation-policy.md",
    "assets/PAPER_EVIDENCE_BLUEPRINT_TEMPLATE.md",
    "assets/QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md",
    "assets/STAGE2_ONE_PASS_SOLUTION_TEMPLATE.md",
    "assets/FINAL_PAPER_AUDIT_TEMPLATE.md",
    "assets/readme-showcase/ASSET_MANIFEST.md",
    "assets/readme-showcase/hero-cumcm-modeling-analyst.svg",
)

REQUIRED_TOKENS = {
    "references/paper-evidence-architecture.md": (
        "PAPER_EVIDENCE_BLUEPRINT_READY",
        "PAPER_CORE",
        "PAPER_SUPPORT",
        "RUN_ONLY",
        "FIGURE_NOT_NEEDED",
        "NOT_IDENTIFIABLE",
    ),
    "references/modeling-quality-gates.md": (
        "QUALITY_GATES_ARE_AUDITORS_NOT_MODEL_SELECTORS",
        "SCIENTIFIC_VALIDITY",
        "CONTEST_TASK_COMPLETION",
        "NOT_IDENTIFIABLE",
    ),
    "references/blind-benchmark-provenance.md": (
        "BLIND_RUN_STARTED",
        "BLIND_SOLUTION_FROZEN",
        "POST_SOLUTION_COMPARISON",
        "POST_HOC_IMPROVEMENT",
        "blind_solution_hash",
    ),
    "references/final-paper-audit.md": (
        "PAPER_FAST_READ_GATE_FAILED",
        "页面级信息密度",
    ),
    "references/python-visualization-policy.md": (
        "方法与流程图",
        "AI_COMMUNICATION_ONLY",
        "N/A（方法结构图）",
    ),
    "references/problem-ingestion-security.md": (
        "Evidence ID",
        "唯一哈希",
        "可见性上下文",
    ),
}

# README 默认只公开不含赛题答案的项目宣传图。旧题结果如需公开，应进入
# 独立案例目录并明确 benchmark / POST_HOC 边界，而不是混入首页资源。
README_HERO = "assets/readme-showcase/hero-cumcm-modeling-analyst.svg"
OLD_CASE_FILENAMES = (
    "case-q1-weathering-clr-shift.png",
    "case-q2-loao-classification-margin.png",
    "case-q3-support-domain.png",
    "case-q4-proportionality-difference-matrix.png",
    "case-q4-simultaneous-intervals.png",
    "case-q1-weathering-clr-shift.webp",
    "case-q2-loao-classification-margin.webp",
    "case-q3-support-domain.webp",
    "case-q4-proportionality-difference-matrix.webp",
    "case-q4-simultaneous-intervals.webp",
)

FORBIDDEN_GENERIC_TERMS = ("高钾", "铅钡", "古代玻璃", "桂电")
POLICY_PLACEHOLDERS = re.compile(r"(?im)^\s*(?:TODO|TBD|FIXME)\s*:")
ROUTE_PATH = re.compile(r"^\s*-\s+((?:references|assets)/[^\s#]+\.md)\s*$")
MD_LINK = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
SVG_NUMBER = re.compile(r"^(\d+(?:\.\d+)?)")


def resolve_markdown_link(source: Path, target: str) -> Path | None:
    target = target.strip().split("#", 1)[0]
    if not target or target.startswith(("http://", "https://", "mailto:", "data:")):
        return None
    if target.startswith("/"):
        return None
    return (source.parent / target).resolve()


def svg_dimensions(path: Path) -> tuple[float, float] | None:
    """读取 SVG 的显式宽高；无法可靠判断时返回 None。"""
    text = path.read_text("utf-8")
    if "<svg" not in text or "viewBox=" not in text:
        return None

    width_match = re.search(r'\bwidth="([^"]+)"', text)
    height_match = re.search(r'\bheight="([^"]+)"', text)
    if not width_match or not height_match:
        return None

    width_number = SVG_NUMBER.match(width_match.group(1))
    height_number = SVG_NUMBER.match(height_match.group(1))
    if not width_number or not height_number:
        return None
    return float(width_number.group(1)), float(height_number.group(1))


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
        for line_no, line in enumerate(manifest.read_text("utf-8").splitlines(), 1):
            match = ROUTE_PATH.match(line)
            if not match:
                continue
            checks += 1
            if not (root / match.group(1)).is_file():
                errors.append(f"manifest 路由断链：{match.group(1)}（第 {line_no} 行）")

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

    readme = root / "README.md"
    hero = root / README_HERO
    asset_manifest = root / "assets/readme-showcase/ASSET_MANIFEST.md"

    if readme.is_file():
        readme_text = readme.read_text("utf-8")
        checks += 1
        if README_HERO not in readme_text:
            errors.append(f"README 未引用顶部宣传图：{README_HERO}")

        for filename in OLD_CASE_FILENAMES:
            checks += 1
            if filename in readme_text:
                warnings.append(
                    f"README 直接展示旧题结果图：{filename}；请确认不会污染后续盲测，并明确 POST_HOC 边界"
                )

    if hero.is_file():
        text = hero.read_text("utf-8")
        checks += 1
        dimensions = svg_dimensions(hero)
        if dimensions is None:
            errors.append("README 顶部宣传图不是可验证的 SVG，或缺少 viewBox / 显式宽高")
        elif dimensions[0] < 900 or dimensions[1] < 250:
            warnings.append(f"README 顶部宣传图尺寸偏小：{dimensions}")
        if "<title" not in text or "<desc" not in text:
            warnings.append("README 顶部 SVG 缺少 title/desc，无障碍说明不完整")

    if asset_manifest.is_file():
        checks += 1
        manifest_text = asset_manifest.read_text("utf-8")
        if Path(README_HERO).name not in manifest_text:
            errors.append("ASSET_MANIFEST 未登记 README 顶部宣传图")

    skill = root / "SKILL.md"
    if skill.is_file():
        checks += 1
        size = skill.stat().st_size
        if size > 18_000:
            warnings.append(f"SKILL.md 已达到 {size} 字节，建议继续保持入口轻量")

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

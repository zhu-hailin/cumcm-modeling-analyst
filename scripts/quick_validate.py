#!/usr/bin/env python3
"""对 Skill 路由、Markdown 链接和 v11.1 关键契约做快速静态校验。"""

from __future__ import annotations

import argparse
import hashlib
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

SHOWCASE_FILES = (
    "hero-cumcm-modeling-analyst.png",
    "case-q1-weathering-clr-shift.png",
    "case-q2-loao-classification-margin.png",
    "case-q3-support-domain.png",
    "case-q4-proportionality-difference-matrix.png",
    "case-q4-simultaneous-intervals.png",
)

FORBIDDEN_GENERIC_TERMS = ("高钾", "铅钡", "古代玻璃", "桂电")
POLICY_PLACEHOLDERS = re.compile(r"(?im)^\s*(?:TODO|TBD|FIXME)\s*:")
ROUTE_PATH = re.compile(r"^\s*-\s+((?:references|assets)/[^\s#]+\.md)\s*$")
MD_LINK = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
MANIFEST_HASH_ROW = re.compile(r"`([^`]+\.png)`[^\n]*`([0-9a-f]{64})`")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def png_dimensions(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()[:24]
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        return None
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


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
        if POLICY_PLACEHOLDERS.search(text):
            errors.append(f"发现未解决占位内容：{path.relative_to(root)}")

    asset_root = root / "assets/readme-showcase"
    hash_manifest = asset_root / "ASSET_MANIFEST.md"
    declared_hashes: dict[str, str] = {}
    if hash_manifest.is_file():
        declared_hashes = dict(MANIFEST_HASH_ROW.findall(hash_manifest.read_text("utf-8")))

    for filename in SHOWCASE_FILES:
        path = asset_root / filename
        checks += 1
        if not path.is_file():
            errors.append(f"README 展示图缺失：{filename}")
            continue
        dimensions = png_dimensions(path)
        if dimensions is None:
            errors.append(f"README 展示图不是有效 PNG：{filename}")
        elif dimensions[0] < 300 or dimensions[1] < 180:
            warnings.append(f"README 展示图尺寸偏小：{filename} {dimensions}")
        expected = declared_hashes.get(filename)
        if expected is None:
            errors.append(f"ASSET_MANIFEST 未登记：{filename}")
        elif sha256(path) != expected:
            errors.append(f"README 展示图哈希不一致：{filename}")

    skill = root / "SKILL.md"
    if skill.is_file():
        size = skill.stat().st_size
        checks += 1
        if size > 18_000:
            warnings.append(f"SKILL.md 已达到 {size} 字节，建议继续保持入口轻量")

    return {"status": "PASS" if not errors else "FAIL", "checks": checks, "errors": errors, "warnings": warnings}


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

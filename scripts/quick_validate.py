#!/usr/bin/env python3
"""校验 Skill 元数据、路由、相对链接与代码语法；不宣称验证了解题能力。"""
from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path

import yaml

MD_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REQUIRED_FILES = (
    "SKILL.md", "manifest.yaml", "agents/openai.yaml",
    "scripts/run_record.py", "scripts/delivery_check.py", "scripts/figure_utils.py",
    "tests/test_helper_tools.py", "tests/test_reliability.py", "tests/test_figures.py",
    "tests/test_competition_first_contract.py", "tests/test_old_problem_forward_contract.py",
    ".github/workflows/validate.yml",
)


def validate(root: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    checks = 0
    for relative in REQUIRED_FILES:
        checks += 1
        if not (root / relative).is_file():
            errors.append(f"缺少文件：{relative}")
    try:
        skill_text = (root / "SKILL.md").read_text("utf-8")
        if not skill_text.startswith("---\n"):
            raise ValueError("SKILL.md 缺少 YAML frontmatter")
        frontmatter = yaml.safe_load(skill_text.split("---", 2)[1])
        manifest = yaml.safe_load((root / "manifest.yaml").read_text("utf-8"))
        checks += 4
        name = frontmatter.get("name", "")
        if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            errors.append("Skill 名称无效")
        if not isinstance(frontmatter.get("description"), str) or not frontmatter["description"].strip():
            errors.append("Skill description 缺失")
        if manifest.get("name") != name:
            errors.append("manifest 与 Skill 名称不一致")
        if not isinstance(manifest.get("version"), str) or not re.fullmatch(r"\d+\.\d+(?:\.\d+)?", manifest["version"]):
            errors.append("版本须为带引号的版本字符串")
        routes = manifest.get("routes", {})
        if not isinstance(routes, dict) or not routes:
            raise ValueError("routes 必须是非空映射")
        loads = [("always_load", manifest.get("always_load"))]
        for route, config in routes.items():
            if not isinstance(config, dict) or not isinstance(config.get("when"), str):
                errors.append(f"路由缺少 when 条件：{route}")
                continue
            loads.append((route, config.get("load")))
        for route, paths in loads:
            checks += 1
            if not isinstance(paths, list) or not paths or not all(isinstance(path, str) for path in paths):
                errors.append(f"路由 load 无效：{route}")
                continue
            if len(paths) != len(set(paths)):
                errors.append(f"路由内重复加载：{route}")
            for relative in paths:
                checks += 1
                target = (root / relative).resolve()
                if not target.is_relative_to(root) or not target.is_file():
                    errors.append(f"路由断链/越界：{route} -> {relative}")
        principles = manifest.get("principles")
        if not isinstance(principles, list) or not principles or not all(isinstance(item, str) for item in principles):
            errors.append("principles 应为字符串列表，检查未引用的冒号")
        interface = yaml.safe_load((root / "agents/openai.yaml").read_text("utf-8")).get("interface", {})
        for field in ("display_name", "short_description", "default_prompt"):
            if not isinstance(interface.get(field), str) or not interface[field].strip():
                errors.append(f"UI 元数据缺失：{field}")
        if len(skill_text.encode("utf-8")) > 14000:
            warnings.append("入口超过 14KB，检查是否存在可移至按需规范的细节")
    except (OSError, ValueError, TypeError, AttributeError, yaml.YAMLError) as exc:
        errors.append(f"元数据/路由无法解析：{exc}")

    for path in root.rglob("*.md"):
        for target in MD_LINK.findall(path.read_text("utf-8")):
            target = target.split("#", 1)[0].strip()
            if not target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            checks += 1
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(root) or not resolved.exists():
                errors.append(f"相对链接断链/越界：{path.relative_to(root)} -> {target}")
    for path in list((root / "scripts").glob("*.py")) + list((root / "tests").glob("*.py")):
        checks += 1
        try:
            ast.parse(path.read_text("utf-8"), filename=str(path))
        except (SyntaxError, UnicodeError) as exc:
            errors.append(f"Python 语法/编码错误：{path.relative_to(root)}: {exc}")
    return {"status": "FAIL" if errors else "PASS", "checks": checks, "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true")
    result = validate(parser.parse_args().root.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(result["status"] != "PASS")


if __name__ == "__main__":
    raise SystemExit(main())

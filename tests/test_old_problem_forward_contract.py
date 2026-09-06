#!/usr/bin/env python3
"""旧题盲测、论文证据架构与一次性安全审计的轻量前向契约测试。

该测试不求解历史赛题；它验证 v11.2 仍保留盲测冻结、一次性安全审计、
科学有效性/竞赛完成度双门与参考论文前的 Evidence Blueprint 冻结边界。
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(path: str, *tokens: str) -> str:
    text = (ROOT / path).read_text("utf-8")
    missing = [token for token in tokens if token not in text]
    if missing:
        raise AssertionError(f"{path} 缺少契约：{missing}")
    return text


def assert_in_order(text: str, *tokens: str) -> None:
    positions = [text.index(token) for token in tokens]
    if positions != sorted(positions):
        raise AssertionError(f"状态顺序错误：{tokens}")


def main() -> int:
    blind = require(
        "references/blind-benchmark-provenance.md",
        "BLIND_RUN_STARTED",
        "BLIND_SOLUTION_FROZEN",
        "POST_SOLUTION_COMPARISON",
        "POST_HOC_IMPROVEMENT",
        "blind_solution_hash",
    )
    assert_in_order(
        blind,
        "BLIND_RUN_STARTED",
        "BLIND_SOLUTION_FROZEN",
        "POST_SOLUTION_COMPARISON",
        "POST_HOC_IMPROVEMENT",
    )

    security = require(
        "references/problem-ingestion-security.md",
        "INGESTION_SECURITY_AUDIT_REQUIRED",
        "INGESTION_SECURITY_AUDIT_PASSED",
        "INGESTION_SECURITY_AUDIT_LOCKED",
        "每个赛题工作区",
        "主 Agent",
        "子代理",
    )
    assert_in_order(
        security,
        "INGESTION_SECURITY_AUDIT_REQUIRED",
        "INGESTION_SECURITY_AUDIT_PASSED",
        "INGESTION_SECURITY_AUDIT_LOCKED",
    )

    core = require(
        "references/core-workflow.md",
        "初始文件安全审计（每个赛题工作区仅一次）",
        "QUALITY_GATES_ARE_AUDITORS_NOT_MODEL_SELECTORS",
        "SCIENTIFIC_VALIDITY",
        "CONTEST_TASK_COMPLETION",
        "PAPER_EVIDENCE_BLUEPRINT_READY",
    )
    if "新增文件先做增量安全审计" in core:
        raise AssertionError("核心流程重新要求后续新增文件执行增量安全审计")

    manifest = require("manifest.yaml", "blind_benchmark:", "paper_evidence:", "version: 11.2")
    always = manifest.split("routes:", 1)[0]
    if "paper-evidence-architecture.md" in always or "blind-benchmark-provenance.md" in always:
        raise AssertionError("深层规则不应进入 always_load")

    q_template = require(
        "assets/QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md",
        "QUESTION_PLAN_CONFIRMATION",
        "FINAL_RUN_ID",
        "确认的是建模边界",
    )
    if "增量安全审计" in q_template:
        raise AssertionError("逐题模板不应重新引入问题级增量安全审计")

    one_pass = require(
        "assets/STAGE2_ONE_PASS_SOLUTION_TEMPLATE.md",
        "不再执行完整或增量安全审计",
        "FINAL_RUN_ID",
    )
    if "新增文件仍执行增量安全审计" in one_pass:
        raise AssertionError("一次性模板重新要求增量安全审计")

    gates = require(
        "references/modeling-quality-gates.md",
        "SCIENTIFIC_VALIDITY = PASS | QUALIFIED | FAIL",
        "CONTEST_TASK_COMPLETION = PASS | FAIL",
        "NOT_IDENTIFIABLE",
    )
    if "必须比较 3" in gates or "至少三个模型" in gates:
        raise AssertionError("质量门重新锁死候选数量")

    require(
        "references/paper-evidence-architecture.md",
        "EARLY_SKELETON",
        "FINAL_FREEZE",
        "PAPER_CORE",
        "PAPER_SUPPORT",
        "RUN_ONLY",
        "PAPER_EVIDENCE_BLUEPRINT_READY",
    )

    paper_writing = require(
        "references/reference-paper-writing.md",
        "PAPER_EVIDENCE_BLUEPRINT_READY",
        "只有以下条件满足后才开始完整写作",
    )
    if "完整参考论文的前置条件" not in paper_writing:
        raise AssertionError("参考论文没有明确 Evidence Blueprint 前置门")

    print("old_problem_forward_contract: PASS")
    print("说明：这是隔离流程契约测试，不是某道旧题的解题性能测试。")
    return 0


if __name__ == "__main__":
    sys.exit(main())

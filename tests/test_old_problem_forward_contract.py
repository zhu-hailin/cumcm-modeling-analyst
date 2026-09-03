#!/usr/bin/env python3
"""旧题盲测状态与论文证据架构的轻量前向契约测试。

该测试不求解任何历史赛题，也不读取历史答案；它只验证 v11.1 的关键状态顺序和
路由约束，防止后续修改把参考资料提前解锁或绕过 Evidence Blueprint。
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
        "reference_unlock_time",
        "blind_solution_hash",
    )
    assert_in_order(
        blind,
        "BLIND_RUN_STARTED",
        "BLIND_SOLUTION_FROZEN",
        "POST_SOLUTION_COMPARISON",
        "POST_HOC_IMPROVEMENT",
    )

    core = require(
        "references/core-workflow.md",
        "QUALITY_GATES_ARE_AUDITORS_NOT_MODEL_SELECTORS",
        "SCIENTIFIC_VALIDITY",
        "CONTEST_TASK_COMPLETION",
        "PAPER_EVIDENCE_BLUEPRINT_READY",
    )
    if core.index("PAPER_EVIDENCE_BLUEPRINT_READY") > core.index("完整参考论文"):
        raise AssertionError("完整参考论文出现在 Evidence Blueprint Ready 之前")

    manifest = require("manifest.yaml", "blind_benchmark_provenance:", "paper_evidence_architecture:")
    always = manifest.split("routes:", 1)[0]
    if "paper-evidence-architecture.md" in always or "blind-benchmark-provenance.md" in always:
        raise AssertionError("P0 深层规则不应进入 always_load")

    gates = require(
        "references/modeling-quality-gates.md",
        "SCIENTIFIC_VALIDITY = PASS | QUALIFIED | FAIL",
        "CONTEST_TASK_COMPLETION = PASS | FAIL",
        "NOT_IDENTIFIABLE",
    )
    if "必须比较 3" in gates or "至少三个模型" in gates:
        raise AssertionError("质量门重新锁死候选数量")

    paper = require(
        "references/paper-evidence-architecture.md",
        "PAPER_CORE",
        "PAPER_SUPPORT",
        "RUN_ONLY",
        "PAPER_EVIDENCE_BLUEPRINT_READY",
    )
    if paper.index("PAPER_EVIDENCE_BLUEPRINT_READY") < paper.index("每个原题交付项"):
        raise AssertionError("Evidence Blueprint 未先覆盖原题交付项")

    print("old_problem_forward_contract: PASS")
    print("说明：这是隔离的流程契约测试，不是对某道旧题解题质量的性能测试。")
    return 0


if __name__ == "__main__":
    sys.exit(main())

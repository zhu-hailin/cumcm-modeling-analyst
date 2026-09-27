#!/usr/bin/env python3
"""验证加载拓扑和权威规则入口，不把特定中文句式锁成测试接口。"""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    manifest = yaml.safe_load((ROOT / "manifest.yaml").read_text("utf-8"))
    routes = manifest["routes"]
    loads = lambda name: set(routes[name]["load"])
    assert set(manifest["always_load"]) == {"references/core-workflow.md"}
    assert loads("link_bootstrap") == {"references/link-bootstrap.md"}
    assert loads("multi_agent") == {
        "references/multi-agent-collaboration.md", "assets/SUBAGENT_TASK_TEMPLATE.md"
    }
    assert "references/abstract-and-argumentation.md" in loads("abstract_revision")
    assert "assets/PAPER_OUTLINE_TEMPLATE.md" in loads("reference_paper")
    assert "references/final-consistency-sweep.md" not in loads("reference_paper")
    assert "assets/DELIVERY_README_TEMPLATE.md" in loads("internal_delivery")
    figure = manifest["external_dependencies"]["nature_figure"]
    assert figure["repository"] == "https://github.com/Yuan1z0825/nature-skills"
    assert figure["skill_path"] == "skills/nature-figure/SKILL.md"
    assert figure["backend"] == "python"
    assert figure["adapter"] in loads("visualization")
    assert loads("initial_ingestion") == {"references/problem-ingestion-security.md"}
    assert loads("stage1_modeling") == {
        "references/modeling-research-playbook.md", "references/modeling-quality-gates.md"
    }
    early = loads("paper_evidence")
    assert "references/paper-evidence-architecture.md" in early
    assert "references/final-consistency-sweep.md" not in early
    assert "references/reference-paper-writing.md" not in early
    assert "references/final-consistency-sweep.md" in loads("evidence_freeze")
    assert "references/competition-compliance.md" in loads("live_competition")
    assert "assets/AI_USAGE_LOG_TEMPLATE.md" in loads("live_competition")
    assert "references/python-code-documentation-policy.md" not in loads("local_workspace")
    assert "references/paper-evaluation-protocol.md" not in loads("literature_and_external_data")
    assert "references/paper-evaluation-protocol.md" not in loads("blind_benchmark")
    assert "references/paper-evaluation-protocol.md" in loads("paper_review")
    assert "references/source-verification-policy.md" in loads("paper_review")
    assert "one_pass" not in routes
    assert not (ROOT / "assets/STAGE2_ONE_PASS_SOLUTION_TEMPLATE.md").exists()
    assert "references/python-code-documentation-policy.md" in loads("question_by_question")
    assert "references/model-run-ledger.md" in loads("question_by_question")
    text = (ROOT / "assets/QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md").read_text("utf-8")
    for authority in ("core-workflow.md", "python-code-documentation-policy.md",
                      "model-run-ledger.md", "python-visualization-policy.md"):
        assert f"(../references/{authority})" in text
    print("competition_first_contract: PASS (routing/authority only; not modeling performance)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

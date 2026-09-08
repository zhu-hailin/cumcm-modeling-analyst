#!/usr/bin/env python3
"""验证加载拓扑和权威规则入口，不把特定中文句式锁成测试接口。"""
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    manifest = yaml.safe_load((ROOT / "manifest.yaml").read_text("utf-8"))
    routes = manifest["routes"]
    loads = lambda name: set(routes[name]["load"])
    assert set(manifest["always_load"]) == {
        "references/problem-ingestion-security.md", "references/core-workflow.md"
    }
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
    assert "one_pass" not in routes
    assert not (ROOT / "assets/STAGE2_ONE_PASS_SOLUTION_TEMPLATE.md").exists()
    for name in ("question_by_question",):
        assert "references/python-code-documentation-policy.md" in loads(name)
        assert "references/model-run-ledger.md" in loads(name)
    for template in ("QUESTION_BY_QUESTION_SOLUTION_TEMPLATE.md",):
        text = (ROOT / "assets" / template).read_text("utf-8")
        for authority in ("core-workflow.md", "python-code-documentation-policy.md",
                          "model-run-ledger.md", "python-visualization-policy.md"):
            assert f"(../references/{authority})" in text
    print("competition_first_contract: PASS (routing/authority only; not modeling performance)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

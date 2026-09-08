#!/usr/bin/env python3
"""核对初始审计/盲测状态与路由；行为能力另需实际试用。"""
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    security = (ROOT / "references/problem-ingestion-security.md").read_text("utf-8")
    assert all(state in security for state in (
        "INGESTION_SECURITY_AUDIT_REQUIRED", "INGESTION_SECURITY_AUDIT_PASSED",
        "INGESTION_SECURITY_AUDIT_LOCKED",
    ))
    for name in ("FILE_SECURITY_AUDIT_TEMPLATE.md", "FILE_AUDIT_MANIFEST_TEMPLATE.md"):
        assert "INGESTION_SECURITY_AUDIT_LOCKED" in (ROOT / "assets" / name).read_text("utf-8")
    blind = (ROOT / "references/blind-benchmark-provenance.md").read_text("utf-8")
    states = ("BLIND_RUN_STARTED", "BLIND_SOLUTION_FROZEN", "POST_SOLUTION_COMPARISON", "POST_HOC_IMPROVEMENT")
    assert [blind.index(state) for state in states] == sorted(blind.index(state) for state in states)
    assert "blind_solution_hash" in blind
    # 针对已经发生的具体回归；这不是通用语义矛盾检测器。
    for path in [ROOT / "SKILL.md", *(ROOT / "references").glob("*.md"), *(ROOT / "assets").glob("*.md")]:
        text = path.read_text("utf-8")
        assert not re.search(r"每份新资料继续执行文件安全审计|新增文件先做增量安全审计", text), path
    manifest = yaml.safe_load((ROOT / "manifest.yaml").read_text("utf-8"))
    assert "references/blind-benchmark-provenance.md" in manifest["routes"]["blind_benchmark"]["load"]
    assert "references/blind-benchmark-provenance.md" not in manifest["always_load"]
    print("old_problem_forward_contract: PASS (static boundary only; not blind problem solving)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

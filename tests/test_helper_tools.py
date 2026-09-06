#!/usr/bin/env python3
"""辅助工具的最小功能测试。

只验证机械行为：重要运行能被记录、缺失正式输出不会被误判为 FINAL、
交付 ZIP 会被真实解压并区分正常包与空包。
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=cwd or ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text("utf-8"))


def test_run_record() -> None:
    with tempfile.TemporaryDirectory(prefix="cumcm_run_record_test_") as tmp:
        project = Path(tmp)
        run_script = str(ROOT / "scripts" / "run_record.py")

        success = run(
            run_script,
            "--root",
            str(project),
            "--problem",
            "Q1",
            "--purpose",
            "tool test success",
            "--status",
            "FINAL",
            "--output",
            "result.txt",
            "--",
            sys.executable,
            "-c",
            "from pathlib import Path; Path('result.txt').write_text('ok', encoding='utf-8')",
        )
        if success.returncode != 0:
            raise AssertionError(f"run_record 成功案例失败：{success.stderr}\n{success.stdout}")

        r1 = load_json(project / "04_results" / "logs" / "runs" / "R001.json")
        if r1["status"] != "FINAL":
            raise AssertionError(f"成功运行没有登记为 FINAL：{r1['status']}")
        if not (project / "04_results" / "logs" / "RUN_LEDGER.md").is_file():
            raise AssertionError("run_record 未生成 RUN_LEDGER.md")

        missing = run(
            run_script,
            "--root",
            str(project),
            "--problem",
            "Q1",
            "--purpose",
            "tool test missing output",
            "--status",
            "FINAL",
            "--output",
            "missing.txt",
            "--",
            sys.executable,
            "-c",
            "print('command itself succeeded')",
        )
        if missing.returncode == 0:
            raise AssertionError("声明的正式输出缺失时 run_record 仍返回成功")

        r2 = load_json(project / "04_results" / "logs" / "runs" / "R002.json")
        if r2["status"] != "REJECTED":
            raise AssertionError(f"缺失正式输出没有被降级为 REJECTED：{r2['status']}")


def test_delivery_check() -> None:
    with tempfile.TemporaryDirectory(prefix="cumcm_delivery_test_") as tmp:
        temp = Path(tmp)
        valid_zip = temp / "valid.zip"
        empty_zip = temp / "empty.zip"

        with zipfile.ZipFile(valid_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("README.md", "# valid\n")
            zf.writestr("code.py", "print('ok')\n")
        with zipfile.ZipFile(empty_zip, "w"):
            pass

        checker = str(ROOT / "scripts" / "delivery_check.py")

        valid = run(checker, str(valid_zip), "--json")
        if valid.returncode != 0:
            raise AssertionError(f"正常 ZIP 未通过 delivery_check：{valid.stderr}\n{valid.stdout}")
        valid_result = json.loads(valid.stdout)
        if valid_result[0]["status"] != "PASS":
            raise AssertionError(f"正常 ZIP 状态不是 PASS：{valid_result}")

        empty = run(checker, str(empty_zip), "--json")
        if empty.returncode == 0:
            raise AssertionError("空 ZIP 被 delivery_check 错误判定为成功")
        empty_result = json.loads(empty.stdout)
        if empty_result[0]["status"] != "FAIL":
            raise AssertionError(f"空 ZIP 状态不是 FAIL：{empty_result}")


def main() -> int:
    test_run_record()
    test_delivery_check()
    print("helper_tools: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

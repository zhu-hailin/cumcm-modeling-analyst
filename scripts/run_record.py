#!/usr/bin/env python3
"""记录并执行一次影响建模决策或正式成果的重要运行。

示例：
python scripts/run_record.py --root . --problem Q1 --purpose "最终预测" \
    --status FINAL --input 01_data/processed/q1.csv -- \
    python 03_code/q1/main.py

脚本只负责机械记录，不判断模型是否科学合理。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path

VALID_STATUS = {
    "EXPLORATORY",
    "BASELINE",
    "CANDIDATE",
    "FINAL",
    "VALIDATION",
    "REJECTED",
    "SUPERSEDED",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def next_run_id(runs_dir: Path) -> str:
    highest = 0
    for path in runs_dir.glob("R*.json"):
        stem = path.stem
        if len(stem) == 4 and stem[1:].isdigit():
            highest = max(highest, int(stem[1:]))
    return f"R{highest + 1:03d}"


def file_record(root: Path, value: str) -> dict[str, object]:
    path = (root / value).resolve() if not Path(value).is_absolute() else Path(value).resolve()
    record: dict[str, object] = {"path": str(path.relative_to(root)) if path.is_relative_to(root) else str(path)}
    if path.is_file():
        record.update({"exists": True, "size": path.stat().st_size, "sha256": sha256(path)})
    else:
        record.update({"exists": path.exists(), "size": None, "sha256": None})
    return record


def append_ledger(ledger: Path, row: dict[str, str]) -> None:
    if not ledger.exists():
        ledger.write_text(
            "# RUN_LEDGER\n\n"
            "| Run ID | 问题 | 目的 | 代码/命令 | 输入/配置 | seed/重复 | 输出目录 | 关键结论 | 状态 |\n"
            "|---|---|---|---|---|---|---|---|---|\n",
            encoding="utf-8",
        )
    safe = {key: value.replace("|", "\\|").replace("\n", " ") for key, value in row.items()}
    with ledger.open("a", encoding="utf-8") as fh:
        fh.write(
            "| {run_id} | {problem} | {purpose} | `{command}` | {inputs} | {seed_repeat} | {outputs} | {conclusion} | {status} |\n".format(
                **safe
            )
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--problem", required=True)
    parser.add_argument("--purpose", required=True)
    parser.add_argument("--status", choices=sorted(VALID_STATUS), required=True)
    parser.add_argument("--input", action="append", default=[], help="相对项目根目录的输入文件，可重复")
    parser.add_argument("--output", action="append", default=[], help="预期输出文件/目录，可重复")
    parser.add_argument("--seed", default="")
    parser.add_argument("--repeat", default="")
    parser.add_argument("--conclusion", default="", help="可在运行后人工补充；这里只记录简短摘要")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="在 -- 之后提供真实运行命令")
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"项目根目录不存在：{root}")

    command = list(args.command)
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        parser.error("必须在 -- 后提供真实运行命令")

    logs_dir = root / "04_results" / "logs"
    runs_dir = logs_dir / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    run_id = next_run_id(runs_dir)

    stdout_path = runs_dir / f"{run_id}.stdout.log"
    stderr_path = runs_dir / f"{run_id}.stderr.log"
    started = datetime.now().astimezone().isoformat(timespec="seconds")

    proc = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
    stdout_path.write_text(proc.stdout, encoding="utf-8", errors="replace")
    stderr_path.write_text(proc.stderr, encoding="utf-8", errors="replace")

    effective_status = args.status if proc.returncode == 0 else "REJECTED"
    input_records = [file_record(root, value) for value in args.input]
    output_records = [file_record(root, value) for value in args.output]

    record = {
        "run_id": run_id,
        "problem": args.problem,
        "purpose": args.purpose,
        "requested_status": args.status,
        "status": effective_status,
        "started_at": started,
        "command": command,
        "command_display": shlex.join(command),
        "return_code": proc.returncode,
        "seed": args.seed or None,
        "repeat": args.repeat or None,
        "inputs": input_records,
        "outputs": output_records,
        "stdout_log": str(stdout_path.relative_to(root)),
        "stderr_log": str(stderr_path.relative_to(root)),
        "conclusion": args.conclusion,
    }
    json_path = runs_dir / f"{run_id}.json"
    json_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")

    append_ledger(
        logs_dir / "RUN_LEDGER.md",
        {
            "run_id": run_id,
            "problem": args.problem,
            "purpose": args.purpose,
            "command": shlex.join(command),
            "inputs": ", ".join(args.input) or "-",
            "seed_repeat": "/".join(part for part in (args.seed, args.repeat) if part) or "-",
            "outputs": ", ".join(args.output) or "-",
            "conclusion": args.conclusion or "-",
            "status": effective_status,
        },
    )

    print(f"{run_id}: {effective_status} (exit={proc.returncode})")
    print(f"record: {json_path.relative_to(root)}")
    if args.status == "FINAL" and proc.returncode != 0:
        print("FINAL 请求运行失败，已记录为 REJECTED，不得作为 FINAL_RUN_ID。", file=sys.stderr)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())

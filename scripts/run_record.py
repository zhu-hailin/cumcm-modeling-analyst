#!/usr/bin/env python3
"""执行并记录重要运行；运行成功不等于模型已通过科学验证。

命令和 --output 中的 {run_dir} 表示本次独立产物目录。
例如：--output '{run_dir}/结果.csv' -- python 求解.py --output-dir '{run_dir}'
只记录明确声明的输入、代码与输出，不声称自动捕获所有依赖。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path

VALID_STATUS = {"EXPLORATORY", "BASELINE", "CANDIDATE", "FINAL", "VALIDATION", "REJECTED", "SUPERSEDED"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def display_path(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def reserve_run(runs_dir: Path) -> tuple[str, Path]:
    """原子建目录预留编号；兼容旧 JSON 记录及超过 999 次的运行。"""
    highest = 0
    for path in runs_dir.iterdir():
        match = re.fullmatch(r"R(\d+)(?:\.json)?", path.name)
        if match:
            highest = max(highest, int(match.group(1)))
    while True:
        highest += 1
        run_id = f"R{highest:03d}"
        folder = runs_dir / run_id
        try:
            folder.mkdir()
            return run_id, folder
        except FileExistsError:
            continue


def snapshot(root: Path, path: Path, *, code: bool = False) -> dict[str, object]:
    """对声明的文件/目录做内容快照；不跟随符号链接。"""
    record: dict[str, object] = {"path": display_path(root, path), "exists": path.exists()}
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
        raise ValueError(f"声明路径包含符号链接：{path}")
    if path.is_file():
        record.update(kind="file", size=path.stat().st_size, sha256=sha256(path))
    elif path.is_dir():
        files = []
        for item in sorted(path.rglob("*")):
            relative = item.relative_to(path)
            if code and ("__pycache__" in relative.parts or item.suffix in {".pyc", ".pyo"}):
                continue
            if item.is_symlink():
                raise ValueError(f"目录含符号链接：{item}")
            if item.is_file():
                files.append({"path": item.relative_to(path).as_posix(), "size": item.stat().st_size, "sha256": sha256(item)})
            elif not item.is_dir():
                raise ValueError(f"不支持的文件类型：{item}")
        record.update(kind="directory", files=files)
    else:
        record.update(kind="missing")
    return record


def has_content(record: dict[str, object]) -> bool:
    if record["kind"] == "file":
        return bool(record["size"])
    return record["kind"] == "directory" and any(item["size"] for item in record["files"])


def rebuild_ledger(root: Path) -> Path:
    """JSON 为唯一权威记录；Markdown 可重建，不手改第二份元数据。"""
    runs_dir = root / "04_results" / "logs" / "runs"
    if not runs_dir.is_dir():
        raise ValueError("未发现运行记录目录，不能重建索引")
    marker = "<!-- cumcm-run-ledger: generated-from-json -->"
    lines = [marker, "# RUN_LEDGER", "", "由 runs/R*.json 生成；状态不代替建模质量门。", "",
             "| Run ID | 问题 | 目的 | 状态 | 执行 | 权威记录 |", "|---|---|---|---|---|---|"]
    for path in sorted(runs_dir.glob("R*.json")):
        record = json.loads(path.read_text("utf-8"))
        values = [record["run_id"], record["problem"], record["purpose"], record["status"],
                  record.get("execution_status", "LEGACY_UNVERIFIED"), f"runs/{path.name}"]
        lines.append("| " + " | ".join(str(value).replace("|", "\\|").replace("\n", " ") for value in values) + " |")
    ledger = runs_dir.parent / "RUN_LEDGER.md"
    if ledger.exists() and not ledger.read_text("utf-8").startswith(marker):
        ledger = ledger.with_name("RUN_LEDGER.generated.md")
        if ledger.exists() and not ledger.read_text("utf-8").startswith(marker):
            raise ValueError("已有非工具生成的索引文件，已保留原件；请人工指定索引位置后重建")
    temporary = ledger.with_suffix(f".{os.getpid()}.tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    temporary.replace(ledger)
    return ledger


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--problem")
    parser.add_argument("--purpose")
    parser.add_argument("--status", choices=sorted(VALID_STATUS))
    parser.add_argument("--input", action="append", default=[], help="输入文件/目录，可重复")
    parser.add_argument("--code", action="append", default=[], help="额外代码/配置；命令中的本地 .py 自动登记")
    parser.add_argument("--output", action="append", default=[], help="本次新建的文件/目录；支持 {run_dir}")
    parser.add_argument("--seed", default="")
    parser.add_argument("--repeat", default="")
    parser.add_argument("--conclusion", default="")
    parser.add_argument("--timeout", type=float, help="按本次预算设置秒数；超时保留失败记录")
    parser.add_argument("--rebuild-ledger", action="store_true")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"项目根目录不存在：{root}")
    if args.rebuild_ledger:
        try:
            print(rebuild_ledger(root))
        except (OSError, ValueError) as exc:
            parser.error(str(exc))
        return 0
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command or not all((args.problem, args.purpose, args.status)):
        parser.error("需要 --problem、--purpose、--status 和 -- 后的真实命令")
    if args.timeout is not None and args.timeout <= 0:
        parser.error("--timeout 必须大于 0")

    runs_dir = root / "04_results" / "logs" / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    run_id, folder = reserve_run(runs_dir)
    artifacts = folder / "artifacts"  # 不预建：空目录不能作为有效输出。
    command = [part.replace("{run_dir}", str(artifacts)) for part in command]

    def locate(value: str) -> Path:
        path = Path(value.replace("{run_dir}", str(artifacts)))
        return path if path.is_absolute() else root / path

    inputs = [locate(value) for value in args.input]
    code = [locate(value) for value in args.code]
    code.extend(locate(value) for value in command if value.endswith(".py") and locate(value).is_file())
    code = list(dict.fromkeys(code))
    outputs = [locate(value) for value in args.output]
    errors: list[str] = []
    record: dict[str, object] = {
        "schema_version": 2, "run_id": run_id, "problem": args.problem, "purpose": args.purpose,
        "requested_status": args.status, "status": "REJECTED", "execution_status": "PREFLIGHT_FAILED",
        "scientific_validity": "NOT_ASSESSED", "contest_task_completion": "NOT_ASSESSED",
        "started_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "command": command, "command_display": shlex.join(command), "return_code": None,
        "seed": args.seed or None, "repeat": args.repeat or None, "timeout_seconds": args.timeout,
        "inputs": [], "code": [], "outputs": [], "errors": errors,
        "stdout_log": None, "stderr_log": None, "conclusion": args.conclusion,
    }
    try:
        # 先保存输入/代码证据，避免运行修改数据后才记录输入 hash。
        record["inputs"] = [snapshot(root, path) for path in inputs]
        record["code"] = [snapshot(root, path, code=True) for path in code]
        for item in record["inputs"] + record["code"]:
            if not has_content(item):
                errors.append(f"输入/代码缺失或为空：{item['path']}")
        if args.status in {"FINAL", "VALIDATION"} and not outputs:
            errors.append("FINAL/VALIDATION 必须声明输出；无输入的解析题可只声明验证产物")
        for path in outputs:
            resolved = path.resolve()
            if not resolved.is_relative_to(root):
                errors.append(f"输出必须在项目目录内：{path}")
            if path.exists() or path.is_symlink():
                errors.append(f"输出已存在，不能证明来自本次运行；使用新路径或 {{run_dir}}：{path}")
            for source in inputs + code + [root / "00_problem", root / "01_data" / "raw"]:
                source = source.resolve()
                if resolved == source or resolved.is_relative_to(source) or source.is_relative_to(resolved):
                    errors.append(f"输出与输入/代码/原件路径重叠：{path}")
            if any(parent.is_symlink() for parent in path.parents):
                errors.append(f"输出父目录包含符号链接：{path}")

        if not errors:
            env = dict(os.environ, CUMCM_RUN_ID=run_id, CUMCM_OUTPUT_DIR=str(artifacts))
            env.setdefault("PYTHONIOENCODING", "utf-8")
            with (folder / "stdout.log").open("wb") as stdout, (folder / "stderr.log").open("wb") as stderr:
                record["stdout_log"] = display_path(root, folder / "stdout.log")
                record["stderr_log"] = display_path(root, folder / "stderr.log")
                try:
                    proc = subprocess.run(command, cwd=root, env=env, stdout=stdout, stderr=stderr,
                                          timeout=args.timeout, check=False)
                    record["return_code"] = proc.returncode
                    record["execution_status"] = "SUCCESS" if proc.returncode == 0 else "FAILED"
                    if proc.returncode:
                        errors.append(f"命令非零退出：{proc.returncode}")
                except subprocess.TimeoutExpired:
                    record["execution_status"] = "TIMEOUT"
                    errors.append("命令超时；其产物不得作为本次正式结果")
                except OSError as exc:
                    record["execution_status"] = "FAILED"
                    errors.append(f"命令无法启动：{exc}")

            record["inputs_after"] = [snapshot(root, path) for path in inputs]
            record["code_after"] = [snapshot(root, path, code=True) for path in code]
            if record["inputs"] != record["inputs_after"] or record["code"] != record["code_after"]:
                errors.append("运行修改了声明的输入或代码，保留前后快照；拒绝固化该运行")
            record["outputs"] = [snapshot(root, path) for path in outputs]
            for item in record["outputs"]:
                if not has_content(item):
                    errors.append(f"输出缺失或为空：{item['path']}")
        if not errors:
            record["status"] = args.status
    except (OSError, ValueError) as exc:
        errors.append(str(exc))

    record["finished_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
    record["artifact_integrity"] = "PASS" if not errors else "FAIL"
    json_path = runs_dir / f"{run_id}.json"
    temporary = folder / "record.tmp"
    temporary.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(json_path)
    try:
        ledger = rebuild_ledger(root)
    except (OSError, ValueError) as exc:
        print(f"运行 JSON 已保存，但阅读索引无法重建：{exc}", file=sys.stderr)
        return 2
    print(f"{run_id}: {record['status']} / {record['execution_status']} / artifacts={record['artifact_integrity']}")
    print(f"record: {display_path(root, json_path)}")
    print(f"index: {display_path(root, ledger)}")
    for error in errors:
        print(error, file=sys.stderr)
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())

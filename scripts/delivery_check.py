#!/usr/bin/env python3
"""实际解压并检查数学建模内部交付 ZIP 的基本完整性。

检查机械完整性，不评价论文数学质量。示例：
python scripts/delivery_check.py 06_submission/internal_delivery/*.zip
"""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
import zipfile
from pathlib import Path, PurePosixPath


def safe_member(name: str) -> bool:
    path = PurePosixPath(name.replace("\\", "/"))
    return not path.is_absolute() and ".." not in path.parts


def validate_docx(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        with zipfile.ZipFile(path) as zf:
            names = set(zf.namelist())
            for required in ("[Content_Types].xml", "word/document.xml"):
                if required not in names:
                    errors.append(f"DOCX 缺少 {required}: {path.name}")
    except zipfile.BadZipFile:
        errors.append(f"DOCX 不是有效 ZIP 容器: {path.name}")
    return errors


def validate_pdf(path: Path) -> list[str]:
    with path.open("rb") as fh:
        header = fh.read(5)
    return [] if header == b"%PDF-" else [f"PDF 头无效: {path.name}"]


def validate_python(path: Path) -> list[str]:
    try:
        compile(path.read_text("utf-8"), str(path), "exec")
        return []
    except Exception as exc:  # noqa: BLE001 - 这里只做静态语法检查
        return [f"Python 语法/编码检查失败: {path.name}: {exc}"]


def validate_zip(path: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    files_checked = 0

    if not path.is_file():
        return {"zip": str(path), "status": "FAIL", "errors": ["文件不存在"], "warnings": [], "files_checked": 0}
    if path.stat().st_size == 0:
        return {"zip": str(path), "status": "FAIL", "errors": ["ZIP 为 0 字节"], "warnings": [], "files_checked": 0}

    try:
        with zipfile.ZipFile(path) as zf:
            infos = zf.infolist()
            if not infos:
                errors.append("ZIP 没有任何 entry")
            bad_crc = zf.testzip()
            if bad_crc:
                errors.append(f"CRC 检查失败: {bad_crc}")

            for info in infos:
                if not safe_member(info.filename):
                    errors.append(f"不安全路径: {info.filename}")
                if not info.is_dir() and info.file_size == 0:
                    warnings.append(f"空文件: {info.filename}")
    except zipfile.BadZipFile:
        return {"zip": str(path), "status": "FAIL", "errors": ["不是有效 ZIP"], "warnings": [], "files_checked": 0}

    if errors:
        return {"zip": str(path), "status": "FAIL", "errors": errors, "warnings": warnings, "files_checked": 0}

    temp_dir = Path(tempfile.mkdtemp(prefix="cumcm_zip_check_"))
    try:
        with zipfile.ZipFile(path) as zf:
            zf.extractall(temp_dir)

        extracted_files = [p for p in temp_dir.rglob("*") if p.is_file()]
        files_checked = len(extracted_files)
        if not extracted_files:
            errors.append("实际解压后没有文件")

        for item in extracted_files:
            if item.stat().st_size == 0:
                warnings.append(f"解压后空文件: {item.relative_to(temp_dir)}")
                continue
            suffix = item.suffix.lower()
            if suffix == ".docx":
                errors.extend(validate_docx(item))
            elif suffix == ".pdf":
                errors.extend(validate_pdf(item))
            elif suffix == ".py":
                errors.extend(validate_python(item))
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    return {
        "zip": str(path),
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "files_checked": files_checked,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zips", nargs="+", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    results = [validate_zip(path.resolve()) for path in args.zips]
    failed = any(result["status"] != "PASS" for result in results)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for result in results:
            print(f"{result['status']}: {result['zip']} ({result['files_checked']} files)")
            for warning in result["warnings"]:
                print(f"  WARNING: {warning}")
            for error in result["errors"]:
                print(f"  ERROR: {error}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

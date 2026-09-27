#!/usr/bin/env python3
"""检查交付目录或真实解压后的 ZIP，不代替数学、复现与视觉验收。

--profile reference-paper 始终要求有效 PDF；--paper-source docx|latex|none
分别另需 DOCX、TEX 或不检查源稿（默认 docx）。auto 识别“参考论文”目录/ZIP。
--require 指定关键相对路径，可重复；--manifest 接受独立 JSON 对账清单：
{"files": [{"path": "结果.csv", "sha256": "...", "size": 123}]}
PDF 解析依赖 pypdf；依赖缺失会明确失败，不降级为只检查文件头。
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import stat
import tempfile
import zipfile
import zlib
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath

MAX_ENTRIES = 10000
MAX_UNCOMPRESSED = 1024 * 1024 * 1024  # 机械资源上限，可按可信成果规模调整。
MAX_XML_BYTES = 32 * 1024 * 1024
PROFILES = {"generic", "reference-paper"}
PAPER_SOURCES = {"docx", "latex", "none"}


def safe_member(name: str) -> bool:
    normalized = name.replace("\\", "/")
    path = PurePosixPath(normalized)
    return bool(normalized) and not path.is_absolute() and ".." not in path.parts and ":" not in normalized and "\0" not in normalized


def inventory(zf: zipfile.ZipFile, max_bytes: int) -> list[str]:
    """在解压/CRC 扫描前拒绝危险路径、重复名称和超预算容器。"""
    errors: list[str] = []
    infos = zf.infolist()
    if not infos:
        errors.append("ZIP 没有任何 entry")
    if len(infos) > MAX_ENTRIES or sum(info.file_size for info in infos) > max_bytes:
        errors.append("ZIP 超出声明的条目数/解压字节预算")
    names: set[str] = set()
    for info in infos:
        name = info.filename
        # Windows 与 POSIX 解压路径保持一致，避免同一 entry 两种解释。
        canonical = str(PurePosixPath(name.replace("\\", "/"))).casefold()
        if not safe_member(name) or "\\" in name:
            errors.append(f"不安全或不兼容路径：{name}")
        if canonical in names:
            errors.append(f"重复/大小写冲突的 ZIP 路径：{name}")
        names.add(canonical)
        if stat.S_ISLNK(info.external_attr >> 16):
            errors.append(f"不支持符号链接 entry：{name}")
        if info.flag_bits & 1:
            errors.append(f"加密 entry 无法验收：{name}")
    return errors


def read_xml(zf: zipfile.ZipFile, name: str) -> ET.Element:
    if zf.getinfo(name).file_size > MAX_XML_BYTES:
        raise ValueError(f"XML 超过解析预算：{name}")
    data = zf.read(name)
    if b"<!DOCTYPE" in data.upper() or b"<!ENTITY" in data.upper():
        raise ValueError(f"不接受 DTD/实体声明：{name}")
    return ET.fromstring(data)


def validate_docx(path: Path) -> list[str]:
    try:
        with zipfile.ZipFile(path) as zf:
            errors = inventory(zf, MAX_UNCOMPRESSED)
            if errors:
                return errors
            types = read_xml(zf, "[Content_Types].xml")
            package_rels = read_xml(zf, "_rels/.rels")
            document = read_xml(zf, "word/document.xml")
            w = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
            if not types.tag.endswith("}Types") or document.tag != w + "document":
                return [f"DOCX XML 根节点无效：{path.name}"]
            content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"
            if not any(node.get("PartName") == "/word/document.xml" and node.get("ContentType") == content_type for node in types):
                return [f"DOCX 缺少正确的正文内容类型：{path.name}"]
            if not any((node.get("Type") or "").endswith("/officeDocument") and
                       node.get("Target", "").lstrip("/") == "word/document.xml" and
                       node.get("TargetMode") != "External" for node in package_rels):
                return [f"DOCX 缺少包级正文关系：{path.name}"]
            body = document.find(w + "body")
            if body is None or not any((node.text or "").strip() for node in body.iter(w + "t")):
                return [f"DOCX 没有可读正文文字：{path.name}"]
            # 检查文档实际引用的图片是否打进包中，不加载外部关系。
            r = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
            a = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
            embedded = [node.get(r + "embed") for node in document.iter(a + "blip") if node.get(r + "embed")]
            if embedded:
                rels = read_xml(zf, "word/_rels/document.xml.rels")
                targets = {node.get("Id"): node for node in rels}
                for key in embedded:
                    node = targets.get(key)
                    if node is None or node.get("TargetMode") == "External":
                        errors.append(f"DOCX 图片关系缺失或非内嵌：{key}")
                        continue
                    target = node.get("Target", "")
                    if not safe_member(target):
                        errors.append(f"DOCX 图片路径不安全：{target}")
                        continue
                    member = str(PurePosixPath("word") / target)
                    if member not in zf.namelist() or not zf.getinfo(member).file_size:
                        errors.append(f"DOCX 引用的图片不存在或为空：{member}")
            return errors
    except (OSError, KeyError, ValueError, ET.ParseError, zipfile.BadZipFile,
            RuntimeError, EOFError, zlib.error) as exc:
        return [f"DOCX 解析失败：{path.name}: {exc}"]


def validate_pdf(path: Path) -> list[str]:
    try:
        from pypdf import PdfReader
    except ImportError:
        return [f"PDF 未验证：缺少 pypdf，请安装后重跑：{path.name}"]
    try:
        reader = PdfReader(str(path), strict=True)
        if reader.is_encrypted:
            return [f"PDF 加密，无法验收：{path.name}"]
        if len(reader.pages) == 0:
            return [f"PDF 页数为 0：{path.name}"]
        has_content = False
        drawing_ops = {b"S", b"s", b"f", b"F", b"f*", b"B", b"B*", b"b", b"b*", b"Do", b"sh", b"INLINE IMAGE"}
        text_ops = {b"Tj", b"TJ", b"'", b'"'}
        for page in reader.pages:
            contents = page.get_contents()
            if contents is None:
                continue
            # 字体/矩阵初始化也是非空内容流，但不会在页面上绘制任何内容。
            for operands, operator in contents.operations:
                if operator in drawing_ops:
                    has_content = True
                elif operator in text_ops:
                    for operand in operands:
                        parts = operand if isinstance(operand, list) else [operand]
                        if any(isinstance(part, (str, bytes)) and part.strip() for part in parts):
                            has_content = True
        if not has_content:
            return [f"PDF 没有文字或绘制操作，只有空白页/初始化内容：{path.name}"]
        # 有绘制指令不证明可见：白色文字、裁切和内容完整性仍需渲染 QA。
        return []
    except Exception as exc:
        return [f"PDF 无法完整解析：{path.name}: {exc}"]


def validate_python(path: Path) -> list[str]:
    try:
        compile(path.read_bytes(), str(path), "exec")
        return []
    except Exception as exc:
        return [f"Python 语法/编码检查失败：{path.name}: {exc}"]


def validate_table(path: Path) -> list[str]:
    if path.suffix.lower() not in {".csv", ".tsv"}:
        return []
    try:
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.reader(stream, delimiter="\t" if path.suffix.lower() == ".tsv" else ",")
            header = next(reader, [])
            if not header or not any(cell.strip() for cell in header):
                return [f"表格没有表头：{path.name}"]
            for row in reader:
                if row and len(row) != len(header):
                    return [f"表格行宽与表头不一致：{path.name}"]
        return []
    except (OSError, UnicodeError, csv.Error) as exc:
        return [f"表格读取失败：{path.name}: {exc}"]


def new_result(path: Path, kind: str, profile: str, paper_source: str) -> dict[str, object]:
    name = path.stem if kind == "zip" else path.name
    if profile == "auto":
        profile = "reference-paper" if name == "参考论文" else "generic"
    result: dict[str, object] = {
        "path": str(path), "kind": kind, "status": "FAIL", "profile": profile,
        "paper_source": paper_source, "scope": "MECHANICAL_ONLY",
        "errors": [], "warnings": [], "files_checked": 0,
    }
    if kind == "zip":
        result["zip"] = str(path)  # 保留旧调用方读取的字段。
    return result


def invalid_options(result: dict, max_bytes: int) -> bool:
    if result["profile"] not in PROFILES or result["paper_source"] not in PAPER_SOURCES or max_bytes <= 0:
        result["errors"].append("验收 profile、论文源格式或字节预算无效")
        return True
    return False


def is_link_or_reparse(info: os.stat_result) -> bool:
    # Windows junction 在 Python 3.11 不一定被 is_symlink() 识别。
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    )


def tree_inventory(folder: Path, max_bytes: int) -> tuple[list[Path], list[str]]:
    """仅用元数据预检整棵目录树，未通过前不读内容、不解析、不哈希。

    所有链接（包括内部链接）均要求物化为普通文件，使交付副本自包含。
    不跟随符号链接/junction，不接受设备/FIFO；计数包含空目录。
    """
    files: list[Path] = []
    errors: list[str] = []
    try:
        root_info = folder.lstat()
        if is_link_or_reparse(root_info) or not stat.S_ISDIR(root_info.st_mode):
            return [], ["交付根必须是普通目录，不支持符号链接或 reparse point"]
        root = folder.resolve(strict=True)
        pending = [folder]
        entry_count = total_bytes = 0
        names: set[str] = set()
        while pending:
            with os.scandir(pending.pop()) as entries:
                for entry in entries:
                    entry_count += 1
                    if entry_count > MAX_ENTRIES:
                        return [], errors + ["目录超出声明的条目数预算"]
                    item = Path(entry.path)
                    relative = item.relative_to(folder).as_posix()
                    info = entry.stat(follow_symlinks=False)
                    if is_link_or_reparse(info):
                        errors.append(f"不支持符号链接或 reparse point：{relative}")
                        continue
                    if not item.resolve(strict=True).is_relative_to(root):
                        errors.append(f"目录路径越界：{relative}")
                        continue
                    canonical = relative.casefold()
                    if not safe_member(relative) or "\\" in relative or canonical in names:
                        errors.append(f"目录路径不安全或存在大小写冲突：{relative}")
                    names.add(canonical)
                    if stat.S_ISDIR(info.st_mode):
                        pending.append(item)
                    elif stat.S_ISREG(info.st_mode):
                        files.append(item)
                        total_bytes += info.st_size
                        if total_bytes > max_bytes:
                            return [], errors + ["目录超出声明的字节预算"]
                    else:
                        errors.append(f"不支持的文件类型：{relative}")
    except (OSError, ValueError, RuntimeError) as exc:
        errors.append(f"目录预检失败：{exc}")
    return files, errors


def validate_tree(folder: Path, *, profile: str = "auto", required: tuple[str, ...] = (),
                  manifest: dict | None = None, max_bytes: int = MAX_UNCOMPRESSED,
                  paper_source: str = "docx") -> dict[str, object]:
    """目录与已解压 ZIP 共用的机械检查；不会执行、导入或编译 TEX。"""
    result = new_result(folder, "directory", profile, paper_source)
    errors, warnings = result["errors"], result["warnings"]
    if invalid_options(result, max_bytes):
        return result
    files, preflight_errors = tree_inventory(folder, max_bytes)
    errors.extend(preflight_errors)
    if errors:
        return result
    result["files_checked"] = len(files)
    try:
        if not files:
            errors.append("目录中没有文件")
        nonempty = [item for item in files if item.stat().st_size]
        if not nonempty:
            errors.append("目录中没有任何非空文件")

        # required/manifest 只能引用预检通过的普通文件，不能绕过链接/预算检查。
        known_files = {
            (item.relative_to(folder).as_posix().casefold() if os.name == "nt"
             else item.relative_to(folder).as_posix()): item for item in files
        }

        def find_file(name: object) -> Path | None:
            if not isinstance(name, str) or not safe_member(name):
                return None
            normalized = str(PurePosixPath(name.replace("\\", "/")))
            if os.name == "nt":
                normalized = normalized.casefold()
            return known_files.get(normalized)

        for name in required:
            file = find_file(name)
            if file is None or not file.stat().st_size:
                errors.append(f"必需文件缺失/为空/路径无效：{name}")
        if result["profile"] == "reference-paper":
            suffixes = [".pdf"] + {"docx": [".docx"], "latex": [".tex"], "none": []}[paper_source]
            for suffix in suffixes:
                if not any(item.suffix.lower() == suffix for item in nonempty):
                    errors.append(f"参考论文包缺少非空 {suffix}")
            if paper_source == "latex":
                warnings.append("TEX 仅检查存在且非空；编译、公式与资源依赖须另行验收")
        for item in files:
            if item.stat().st_size == 0:
                if item.name == "__init__.py":
                    warnings.append(f"允许空包初始化文件：{item.relative_to(folder)}")
                else:
                    errors.append(f"空成果文件：{item.relative_to(folder)}")
                continue
            suffix = item.suffix.lower()
            if suffix == ".docx":
                errors.extend(validate_docx(item))
            elif suffix == ".pdf":
                errors.extend(validate_pdf(item))
            elif suffix == ".py":
                errors.extend(validate_python(item))
            elif suffix in {".csv", ".tsv"}:
                errors.extend(validate_table(item))
        if manifest is not None:
            entries = manifest.get("files") if isinstance(manifest, dict) else None
            if not isinstance(entries, list) or not entries:
                errors.append("对账清单必须包含非空 files 列表")
            else:
                for entry in entries:
                    if not isinstance(entry, dict):
                        errors.append("对账清单条目必须是对象")
                        continue
                    name, expected = entry.get("path", ""), entry.get("sha256", "")
                    if not isinstance(name, str) or not safe_member(name) or not isinstance(expected, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", expected):
                        errors.append(f"对账条目路径/hash 无效：{name}")
                        continue
                    file = find_file(name)
                    if file is None:
                        errors.append(f"清单文件缺失：{name}")
                        continue
                    if entry.get("size") is not None and entry["size"] != file.stat().st_size:
                        errors.append(f"文件大小与清单不一致：{name}")
                    with file.open("rb") as stream:
                        digest = hashlib.file_digest(stream, "sha256").hexdigest()
                    if digest != expected.lower():
                        errors.append(f"SHA-256 与清单不一致：{name}")
    except (OSError, ValueError, RuntimeError) as exc:
        errors.append(f"目录验收失败：{exc}")
    result["status"] = "FAIL" if errors else "PASS"
    return result


def validate_directory(path: Path, *, profile: str = "auto", required: tuple[str, ...] = (),
                       manifest: dict | None = None, max_bytes: int = MAX_UNCOMPRESSED,
                       paper_source: str = "docx") -> dict[str, object]:
    return validate_tree(path, profile=profile, required=required, manifest=manifest,
                         max_bytes=max_bytes, paper_source=paper_source)


def validate_zip(path: Path, *, profile: str = "auto", required: tuple[str, ...] = (),
                 manifest: dict | None = None, max_bytes: int = MAX_UNCOMPRESSED,
                 paper_source: str = "docx") -> dict[str, object]:
    result = new_result(path, "zip", profile, paper_source)
    errors = result["errors"]
    if invalid_options(result, max_bytes):
        return result
    try:
        if not path.is_file() or path.stat().st_size == 0:
            errors.append("ZIP 不存在或为 0 字节")
            return result
        with zipfile.ZipFile(path) as zf:
            errors.extend(inventory(zf, max_bytes))
            if errors:
                return result
            if zf.testzip():
                errors.append("ZIP CRC 检查失败")
                return result
            with tempfile.TemporaryDirectory(prefix="cumcm_zip_check_") as tmp:
                folder = Path(tmp)
                zf.extractall(folder)
                checked = validate_tree(folder, profile=result["profile"], required=required,
                                        manifest=manifest, max_bytes=max_bytes, paper_source=paper_source)
                for key in ("status", "errors", "warnings", "files_checked"):
                    result[key] = checked[key]
                return result
    except (OSError, ValueError, RuntimeError, zipfile.BadZipFile, NotImplementedError, EOFError, zlib.error) as exc:
        errors.append(f"ZIP 验收失败：{exc}")
    return result


def validate_delivery(path: Path, **kwargs) -> dict[str, object]:
    # 不 resolve 输入，否则目录根本身的符号链接/junction 会被提前隐藏。
    return validate_directory(path, **kwargs) if path.is_dir() else validate_zip(path, **kwargs)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="交付目录或 ZIP，可指定多个")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--profile", choices=("auto", "generic", "reference-paper"), default="auto")
    parser.add_argument("--paper-source", choices=("docx", "latex", "none"), default="docx")
    parser.add_argument("--require", action="append", default=[])
    parser.add_argument("--manifest", type=Path, help="独立 JSON 清单；仅用于单个交付目录或 ZIP")
    parser.add_argument("--max-bytes", type=int, default=MAX_UNCOMPRESSED)
    args = parser.parse_args()
    if args.max_bytes <= 0:
        parser.error("--max-bytes 必须大于 0")
    if args.manifest and len(args.paths) != 1:
        parser.error("--manifest 一次只能对账一个目录或 ZIP")
    manifest = None
    if args.manifest:
        try:
            manifest = json.loads(args.manifest.read_text("utf-8"))
            if not isinstance(manifest, dict):
                raise ValueError("清单必须是 JSON 对象")
        except (OSError, ValueError) as exc:
            parser.error(f"清单不可读取：{exc}")
    results = [validate_delivery(path.absolute(), profile=args.profile, required=tuple(args.require),
                                manifest=manifest, max_bytes=args.max_bytes, paper_source=args.paper_source)
               for path in args.paths]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for result in results:
            print(f"{result['status']}: {result['path']} ({result['files_checked']} files; MECHANICAL_ONLY)")
            for message in result["warnings"]:
                print(f"  WARNING: {message}")
            for message in result["errors"]:
                print(f"  ERROR: {message}")
    return int(any(result["status"] != "PASS" for result in results))


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""真实解压并检查内部 ZIP 的机械完整性，不代替数学与视觉验收。

--profile reference-paper 要求有效 DOCX + PDF；auto 可识别“参考论文.zip”。
--require 指定包内关键文件，可重复；--manifest 接受包外 JSON 对账清单：
{"files": [{"path": "结果.csv", "sha256": "...", "size": 123}]}
PDF 解析依赖 pypdf；依赖缺失会明确失败，不降级为只检查文件头。
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
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
    except (OSError, KeyError, ValueError, ET.ParseError, zipfile.BadZipFile, RuntimeError) as exc:
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


def validate_zip(path: Path, *, profile: str = "auto", required: tuple[str, ...] = (),
                 manifest: dict | None = None, max_bytes: int = MAX_UNCOMPRESSED) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    profile = ("reference-paper" if path.stem == "参考论文" else "generic") if profile == "auto" else profile
    result: dict[str, object] = {"zip": str(path), "status": "FAIL", "profile": profile,
                                "scope": "MECHANICAL_ONLY", "errors": errors, "warnings": warnings, "files_checked": 0}
    if profile not in {"generic", "reference-paper"} or max_bytes <= 0:
        errors.append("验收 profile 或字节预算无效")
        return result
    if not path.is_file() or path.stat().st_size == 0:
        errors.append("ZIP 不存在或为 0 字节")
        return result
    try:
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
                files = [item for item in folder.rglob("*") if item.is_file()]
                result["files_checked"] = len(files)
                if not files:
                    errors.append("实际解压后没有文件")
                nonempty = [item for item in files if item.stat().st_size]
                if not nonempty:
                    errors.append("实际解压后没有任何非空文件")
                for name in required:
                    if not safe_member(name) or not (folder / name).is_file() or not (folder / name).stat().st_size:
                        errors.append(f"必需文件缺失/为空/路径无效：{name}")
                if profile == "reference-paper":
                    for suffix in (".docx", ".pdf"):
                        if not any(item.suffix.lower() == suffix for item in nonempty):
                            errors.append(f"参考论文包缺少非空 {suffix}")
                for item in files:
                    if item.stat().st_size == 0:
                        # 空 __init__.py 合法；论文、数据和其他空文件不能冒充成果。
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
                            name = entry.get("path", "")
                            expected = entry.get("sha256", "")
                            if not isinstance(name, str) or not safe_member(name) or not isinstance(expected, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", expected):
                                errors.append(f"对账条目路径/hash 无效：{name}")
                                continue
                            file = folder / name
                            if not file.is_file():
                                errors.append(f"清单文件缺失：{name}")
                                continue
                            if entry.get("size") is not None and entry["size"] != file.stat().st_size:
                                errors.append(f"文件大小与清单不一致：{name}")
                            with file.open("rb") as stream:
                                digest = hashlib.file_digest(stream, "sha256").hexdigest()
                            if digest != expected.lower():
                                errors.append(f"SHA-256 与清单不一致：{name}")
    except (OSError, ValueError, RuntimeError, zipfile.BadZipFile, NotImplementedError, EOFError, zlib.error) as exc:
        errors.append(f"ZIP 验收失败：{exc}")
    result["status"] = "FAIL" if errors else "PASS"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zips", nargs="+", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--profile", choices=("auto", "generic", "reference-paper"), default="auto")
    parser.add_argument("--require", action="append", default=[])
    parser.add_argument("--manifest", type=Path, help="包外 JSON 清单；仅用于单个 ZIP")
    parser.add_argument("--max-bytes", type=int, default=MAX_UNCOMPRESSED)
    args = parser.parse_args()
    if args.max_bytes <= 0:
        parser.error("--max-bytes 必须大于 0")
    if args.manifest and len(args.zips) != 1:
        parser.error("--manifest 一次只能对账一个 ZIP")
    manifest = None
    if args.manifest:
        try:
            manifest = json.loads(args.manifest.read_text("utf-8"))
            if not isinstance(manifest, dict):
                raise ValueError("清单必须是 JSON 对象")
        except (OSError, ValueError) as exc:
            parser.error(f"清单不可读取：{exc}")
    results = [validate_zip(path.resolve(), profile=args.profile, required=tuple(args.require),
                            manifest=manifest, max_bytes=args.max_bytes) for path in args.zips]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for result in results:
            print(f"{result['status']}: {result['zip']} ({result['files_checked']} files; MECHANICAL_ONLY)")
            for message in result["warnings"]:
                print(f"  WARNING: {message}")
            for message in result["errors"]:
                print(f"  ERROR: {message}")
    return int(any(result["status"] != "PASS" for result in results))


if __name__ == "__main__":
    raise SystemExit(main())

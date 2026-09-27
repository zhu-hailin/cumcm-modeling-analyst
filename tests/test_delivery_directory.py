#!/usr/bin/env python3
"""目录/ZIP 共用验收的行为回归；不会把机械通过当成科学或复现通过。"""

from __future__ import annotations

import hashlib
import io
import json
import os
import stat
import struct
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import delivery_check as checker
from test_reliability import docx, pdf


class DirectoryDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cumcm_directory_check_")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.delivery = self.root / "交付文件夹"
        self.delivery.mkdir()

    def file(self, name: str, data: str | bytes = "结果\n42\n") -> Path:
        path = self.delivery / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data.encode("utf-8") if isinstance(data, str) else data)
        return path

    def archive(self) -> Path:
        archive = self.root / "成果.zip"
        with zipfile.ZipFile(archive, "w") as zf:
            for item in self.delivery.rglob("*"):
                if item.is_file():
                    zf.write(item, item.relative_to(self.delivery).as_posix())
        return archive

    def invoke(self, path: Path, *args: str):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts/delivery_check.py"), str(path), "--json", *args],
            capture_output=True, text=True, encoding="utf-8", timeout=20,
        )

    def test_chinese_directory_and_zip_have_same_checks(self):
        self.file("支撑材料/结果.csv")
        self.file("支撑材料/入口.py", "print('ok')\n")
        directory = checker.validate_delivery(self.delivery, required=("支撑材料/结果.csv",))
        archive = self.archive()
        zipped = checker.validate_zip(archive, required=("支撑材料/结果.csv",))
        self.assertEqual(directory["status"], "PASS", directory)
        for key in ("status", "scope", "errors", "warnings", "files_checked"):
            self.assertEqual(directory[key], zipped[key])
        self.assertEqual(directory["kind"], "directory")
        self.assertEqual(directory["path"], str(self.delivery))
        self.assertNotIn("zip", directory)
        self.assertEqual(zipped["kind"], "zip")
        self.assertEqual(zipped["zip"], str(archive))
        self.assertEqual(zipped["path"], str(archive))

    def test_empty_directory_and_only_empty_subdirectory_fail(self):
        self.assertEqual(checker.validate_directory(self.delivery)["status"], "FAIL")
        (self.delivery / "空目录").mkdir()
        self.assertEqual(checker.validate_directory(self.delivery)["status"], "FAIL")

    def test_required_markdown_dependency_is_not_optional(self):
        self.file("入口.py", "from pathlib import Path\nPath('参数.md').read_text('utf-8')\n")
        result = checker.validate_directory(self.delivery, required=("参数.md",))
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("参数.md" in item for item in result["errors"]))
        self.file("参数.md", "# 运行参数\nlimit=3\n")
        self.assertEqual(checker.validate_directory(self.delivery, required=("参数.md",))["status"], "PASS")

    def test_manifest_hash_and_size(self):
        path = self.file("结果.csv")
        data = path.read_bytes()
        entry = {"path": "结果.csv", "size": len(data), "sha256": hashlib.sha256(data).hexdigest()}
        self.assertEqual(checker.validate_directory(self.delivery, manifest={"files": [entry]})["status"], "PASS")
        for overrides in ({"sha256": "0" * 64}, {"size": len(data) + 1}, {"path": "缺失.csv"}):
            with self.subTest(overrides=overrides):
                result = checker.validate_directory(self.delivery, manifest={"files": [entry | overrides]})
                self.assertEqual(result["status"], "FAIL")

    def test_required_and_manifest_cannot_read_outside_directory(self):
        outside = self.root / "external.txt"
        outside.write_text("outside", encoding="utf-8")
        self.file("结果.csv")
        manifest = {"files": [{"path": "../external.txt", "sha256": "0" * 64}]}
        with patch.object(checker.hashlib, "file_digest", side_effect=AssertionError("不得读取目录外内容")):
            result = checker.validate_directory(self.delivery, required=("../external.txt",), manifest=manifest)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(len(result["errors"]), 2)

    def test_byte_budget_precedes_content_reading(self):
        self.file("入口.py", "raise RuntimeError('not executed')\n")
        manifest = {"files": [{"path": "入口.py", "sha256": "0" * 64}]}
        with patch.object(checker, "validate_python", side_effect=AssertionError("预算失败时不得解析")), \
             patch.object(checker.hashlib, "file_digest", side_effect=AssertionError("预算失败时不得哈希")):
            result = checker.validate_directory(self.delivery, manifest=manifest, max_bytes=2)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["files_checked"], 0)

    def test_entry_budget_includes_empty_directories(self):
        self.file("入口.py", "print('ok')")
        (self.delivery / "empty").mkdir()
        with patch.object(checker, "MAX_ENTRIES", 1), \
             patch.object(checker, "validate_python", side_effect=AssertionError("预算失败时不得解析")):
            result = checker.validate_directory(self.delivery)
        self.assertEqual(result["status"], "FAIL")

    def test_python_is_compiled_for_syntax_but_never_executed(self):
        marker = self.root / "must-not-exist.txt"
        self.file("入口.py", f"from pathlib import Path\nPath({str(marker)!r}).write_text('executed')\n")
        for path in (self.delivery, self.archive()):
            result = checker.validate_delivery(path)
            self.assertEqual(result["status"], "PASS", result)
            self.assertEqual(result["scope"], "MECHANICAL_ONLY")
            self.assertFalse(marker.exists())

    def test_invalid_python_and_table_fail_in_directory(self):
        self.file("入口.py", "def broken(:")
        self.file("结果.csv", "a,b\n1,2,3\n")
        result = checker.validate_directory(self.delivery)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(len(result["errors"]), 2)

    def test_empty_init_allowed_but_empty_result_rejected(self):
        self.file("__init__.py", b"")
        self.file("入口.py", "pass\n")
        self.assertEqual(checker.validate_directory(self.delivery)["status"], "PASS")
        self.file("结果.csv", b"")
        self.assertEqual(checker.validate_directory(self.delivery)["status"], "FAIL")

    def test_reference_paper_source_modes(self):
        self.file("论文.pdf", pdf())
        for path in (self.delivery, self.archive()):
            self.assertEqual(checker.validate_delivery(path, profile="reference-paper")["status"], "FAIL")
            self.assertEqual(checker.validate_delivery(path, profile="reference-paper", paper_source="none")["status"], "PASS")
            self.assertEqual(checker.validate_delivery(path, profile="reference-paper", paper_source="latex")["status"], "FAIL")
        self.file("论文.tex", "\\documentclass{article}\n\\begin{document}Paper\\end{document}\n")
        self.assertEqual(checker.validate_directory(self.delivery, profile="reference-paper", paper_source="latex")["status"], "PASS")
        self.file("论文.docx", docx())
        for path in (self.delivery, self.archive()):
            for source in ("docx", "latex", "none"):
                self.assertEqual(checker.validate_delivery(path, profile="reference-paper", paper_source=source)["status"], "PASS")

    def test_source_mode_never_removes_pdf_requirement(self):
        self.file("论文.docx", docx())
        self.file("论文.tex", "source")
        for source in ("docx", "latex", "none"):
            result = checker.validate_directory(self.delivery, profile="reference-paper", paper_source=source)
            self.assertEqual(result["status"], "FAIL")
            self.assertTrue(any(".pdf" in item for item in result["errors"]))

    def test_corrupt_docx_stream_returns_fail_in_directory_and_zip(self):
        container = io.BytesIO()
        with zipfile.ZipFile(container, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml", "<Types/>")
        damaged = bytearray(container.getvalue())
        name_length, extra_length = struct.unpack_from("<HH", damaged, 26)
        # BTYPE=3 is reserved: listing succeeds, decompressing XML must fail.
        damaged[30 + name_length + extra_length] = 0x06
        self.file("paper.docx", bytes(damaged))
        for path in (self.delivery, self.archive()):
            result = checker.validate_delivery(path)
            self.assertEqual(result["status"], "FAIL", result)
            self.assertTrue(any("DOCX 解析失败：paper.docx" in error for error in result["errors"]))
            proc = self.invoke(path)
            self.assertEqual(proc.returncode, 1, proc.stderr)
            self.assertEqual(json.loads(proc.stdout)[0]["status"], "FAIL")
            self.assertNotIn("Traceback", proc.stderr)

    def test_auto_profile_recognizes_reference_paper_directory(self):
        folder = self.delivery / "参考论文"
        folder.mkdir()
        (folder / "README.md").write_text("not a paper", encoding="utf-8")
        result = checker.validate_directory(folder)
        self.assertEqual(result["profile"], "reference-paper")
        self.assertEqual(result["status"], "FAIL")

    def test_generic_profile_keeps_existing_behavior(self):
        self.file("README.md", "说明")
        for source in ("docx", "latex", "none"):
            self.assertEqual(checker.validate_directory(self.delivery, paper_source=source)["status"], "PASS")

    def test_invalid_options_fail(self):
        self.file("README.md", "说明")
        for options in ({"profile": "bad"}, {"paper_source": "bad"}, {"max_bytes": 0}):
            self.assertEqual(checker.validate_directory(self.delivery, **options)["status"], "FAIL")

    def test_directory_cli_and_legacy_zip_cli(self):
        self.file("结果.csv")
        for path in (self.delivery, self.archive()):
            proc = self.invoke(path, "--require", "结果.csv")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            result = json.loads(proc.stdout)[0]
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["path"], str(path))
            if path.suffix == ".zip":
                self.assertEqual(result["zip"], str(path))

    def test_cli_paper_source_none_and_manifest(self):
        path = self.file("论文.pdf", pdf())
        data = path.read_bytes()
        manifest = self.root / "manifest.json"
        manifest.write_text(json.dumps({"files": [{"path": "论文.pdf", "sha256": hashlib.sha256(data).hexdigest()}]}), encoding="utf-8")
        proc = self.invoke(self.delivery, "--profile", "reference-paper", "--paper-source", "none", "--manifest", str(manifest))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)[0]["paper_source"], "none")

    def symlink(self, link: Path, target: Path, is_directory: bool = False):
        try:
            link.symlink_to(target, target_is_directory=is_directory)
        except OSError as exc:
            self.skipTest(f"当前环境不能创建符号链接：{exc}")

    def test_external_symlink_is_rejected_before_reading(self):
        target = self.root / "outside.py"
        target.write_text("raise RuntimeError('must not execute')", encoding="utf-8")
        self.symlink(self.delivery / "link.py", target)
        with patch.object(checker, "validate_python", side_effect=AssertionError("不得解析外链")):
            result = checker.validate_directory(self.delivery)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["files_checked"], 0)

    def test_internal_and_broken_symlinks_are_also_rejected(self):
        target = self.file("ok.txt", "ok")
        self.symlink(self.delivery / "inside", target)
        self.symlink(self.delivery / "broken", self.root / "missing")
        result = checker.validate_directory(self.delivery)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(len(result["errors"]), 2)

    def test_root_symlink_not_hidden_by_dispatch_or_cli(self):
        self.file("结果.csv")
        link = self.root / "linked-delivery"
        self.symlink(link, self.delivery, is_directory=True)
        self.assertEqual(checker.validate_delivery(link)["status"], "FAIL")
        self.assertNotEqual(self.invoke(link).returncode, 0)

    def test_reparse_metadata_is_rejected_even_without_symlink_mode(self):
        info = SimpleNamespace(st_mode=stat.S_IFDIR, st_file_attributes=0x400)
        self.assertTrue(checker.is_link_or_reparse(info))

    @unittest.skipUnless(os.name == "nt", "Windows junction integration")
    def test_windows_junction_cannot_escape_directory(self):
        target = self.root / "outside"
        target.mkdir()
        (target / "outside.py").write_text("pass", encoding="utf-8")
        junction = self.delivery / "external"
        # Generated temporary paths only; no shell deletion. TemporaryDirectory
        # cleanup removes the junction itself, not its target (Python >= 3.8).
        proc = subprocess.run(["cmd", "/d", "/c", "mklink", "/J", str(junction), str(target)], capture_output=True, timeout=20)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        with patch.object(checker, "validate_python", side_effect=AssertionError("不得解析 junction 目标")):
            self.assertEqual(checker.validate_directory(self.delivery)["status"], "FAIL")
            self.assertEqual(checker.validate_delivery(junction)["status"], "FAIL")
        self.assertNotEqual(self.invoke(junction).returncode, 0)
        self.assertTrue((target / "outside.py").is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)

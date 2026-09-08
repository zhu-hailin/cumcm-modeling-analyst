#!/usr/bin/env python3
"""运行/交付的行为回归：真实构造产物并调用工具，不匹配提示词措辞。"""

from __future__ import annotations

import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from delivery_check import safe_member, validate_zip
from run_record import reserve_run


def docx(text: str = "训练参考论文正文") -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        zf.writestr("[Content_Types].xml", '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
        zf.writestr("_rels/.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
        zf.writestr("word/document.xml", '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>' + text + '</w:t></w:r></w:p></w:body></w:document>')
    return buffer.getvalue()


def pdf(*, blank: bool = False, no_pages: bool = False, initialization_only: bool = False) -> bytes:
    from pypdf import PdfWriter
    from pypdf.generic import DecodedStreamObject, NameObject
    writer = PdfWriter()
    if not no_pages:
        page = writer.add_blank_page(width=300, height=300)
        if not blank:
            contents = DecodedStreamObject()
            contents.set_data(b"1 0 0 1 0 0 cm BT /F1 12 Tf 14 TL ET" if initialization_only else b"0 0 100 100 re S")
            page[NameObject("/Contents")] = contents
    buffer = io.BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


class RunTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cumcm_run_regression_")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def invoke(self, code="pass", *flags, executable=None):
        command = [executable] if executable else [sys.executable, "-c", code]
        proc = subprocess.run([sys.executable, str(ROOT / "scripts/run_record.py"), "--root", str(self.root),
                               "--problem", "Q1", "--purpose", "回归测试", "--status", "FINAL", *flags,
                               "--", *command], capture_output=True, text=True, timeout=20)
        records = sorted((self.root / "04_results/logs/runs").glob("R*.json"))
        return proc, json.loads(records[-1].read_text("utf-8"))

    def test_fresh_outputs_and_distinct_runs(self):
        code = "import os; from pathlib import Path; p=Path(os.environ['CUMCM_OUTPUT_DIR']); p.mkdir(); (p/'结果.csv').write_text('结果\\n42\\n', encoding='utf-8')"
        first, r1 = self.invoke(code, "--output", "{run_dir}/结果.csv")
        second, r2 = self.invoke(code, "--output", "{run_dir}/结果.csv")
        self.assertEqual((first.returncode, second.returncode), (0, 0))
        self.assertNotEqual(r1["run_id"], r2["run_id"])
        self.assertNotEqual(r1["outputs"][0]["path"], r2["outputs"][0]["path"])
        self.assertEqual(r2["scientific_validity"], "NOT_ASSESSED")
        self.assertEqual(r2["contest_task_completion"], "NOT_ASSESSED")

    def test_stale_output_rejected_before_execution(self):
        (self.root / "结果.csv").write_text("旧结果", encoding="utf-8")
        proc, record = self.invoke("raise Exception('不能执行')", "--output", "结果.csv")
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(record["execution_status"], "PREFLIGHT_FAILED")
        self.assertEqual((self.root / "结果.csv").read_text("utf-8"), "旧结果")

    def test_missing_input(self):
        proc, record = self.invoke("pass", "--input", "不存在.csv", "--output", "新结果.csv")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIsNone(record["return_code"])

    def test_outputs_required(self):
        proc, record = self.invoke()
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(record["status"], "REJECTED")

    def test_missing_empty_file_and_empty_directory(self):
        for name, code in [("不存在", "pass"), ("空文件", "from pathlib import Path; Path('空文件').touch()"),
                           ("空目录", "from pathlib import Path; Path('空目录').mkdir()")]:
            with self.subTest(name=name):
                proc, record = self.invoke(code, "--output", name)
                self.assertNotEqual(proc.returncode, 0)
                self.assertEqual(record["status"], "REJECTED")

    def test_input_change_keeps_original_hash(self):
        source = self.root / "输入.txt"
        source.write_text("original", encoding="utf-8")
        proc, record = self.invoke("from pathlib import Path; Path('输入.txt').write_text('modified'); Path('结果.txt').write_text('ok')",
                                   "--input", "输入.txt", "--output", "结果.txt")
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(record["inputs"][0]["sha256"], hashlib.sha256(b"original").hexdigest())
        self.assertNotEqual(record["inputs"], record["inputs_after"])

    def test_directory_input_snapshot(self):
        data = self.root / "数据"
        data.mkdir()
        (data / "输入.txt").write_text("original")
        proc, record = self.invoke("from pathlib import Path; Path('结果.txt').write_text('ok')", "--input", "数据", "--output", "结果.txt")
        self.assertEqual(proc.returncode, 0)
        self.assertTrue(record["inputs"][0]["files"][0]["sha256"])

    def test_code_version_recorded(self):
        script = self.root / "求解.py"
        script.write_text("from pathlib import Path\nPath('结果.txt').write_text('ok')\n", encoding="utf-8")
        proc = subprocess.run([sys.executable, str(ROOT / "scripts/run_record.py"), "--root", str(self.root),
                               "--problem", "Q1", "--purpose", "代码版本", "--status", "FINAL", "--output", "结果.txt",
                               "--", sys.executable, "求解.py"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        record = json.loads((self.root / "04_results/logs/runs/R001.json").read_text("utf-8"))
        self.assertEqual(record["code"][0]["sha256"], hashlib.sha256(script.read_bytes()).hexdigest())

    def test_import_cache_is_not_source_mutation(self):
        modules = self.root / "common"
        modules.mkdir()
        (modules / "helper.py").write_text("value = 42\n", encoding="utf-8")
        proc, record = self.invoke("from common.helper import value; from pathlib import Path; Path('结果.txt').write_text(str(value))",
                                   "--code", "common", "--output", "结果.txt")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(record["code"], record["code_after"])
        self.assertTrue(list(modules.rglob("*.pyc")))

    def test_source_mutation_is_still_rejected(self):
        modules = self.root / "common"
        modules.mkdir()
        (modules / "helper.py").write_text("value = 42\n", encoding="utf-8")
        proc, record = self.invoke("from pathlib import Path; Path('common/helper.py').write_text('value = 0'); Path('结果.txt').write_text('ok')",
                                   "--code", "common", "--output", "结果.txt")
        self.assertNotEqual(proc.returncode, 0)
        self.assertNotEqual(record["code"], record["code_after"])

    def test_existing_manual_ledger_is_preserved(self):
        logs = self.root / "04_results/logs"
        logs.mkdir(parents=True)
        old = logs / "RUN_LEDGER.md"
        old.write_text("# 队员人工记录\n不要覆盖\n", encoding="utf-8")
        proc, _ = self.invoke("from pathlib import Path; Path('结果.txt').write_text('ok')", "--output", "结果.txt")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(old.read_text("utf-8"), "# 队员人工记录\n不要覆盖\n")
        self.assertTrue((logs / "RUN_LEDGER.generated.md").is_file())

    def test_nonzero_timeout_and_launch_failure(self):
        for code, flags, executable, expected in [
            ("raise SystemExit(7)", [], None, "FAILED"),
            ("import time; time.sleep(5)", ["--timeout", "0.05"], None, "TIMEOUT"),
            ("pass", [], "definitely-no-such-cumcm-command", "FAILED"),
        ]:
            with self.subTest(expected=expected, code=code):
                proc, record = self.invoke(code, "--output", "新结果.txt", *flags, executable=executable)
                self.assertNotEqual(proc.returncode, 0)
                self.assertEqual(record["execution_status"], expected)
                self.assertEqual(record["status"], "REJECTED")

    def test_run_numbers_beyond_999(self):
        folder = self.root / "runs"
        folder.mkdir()
        (folder / "R999.json").touch()
        r1, _ = reserve_run(folder)
        r2, _ = reserve_run(folder)
        self.assertEqual((r1, r2), ("R1000", "R1001"))

    def test_output_cannot_overwrite_raw(self):
        proc, record = self.invoke("pass", "--output", "01_data/raw/新文件.csv")
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(record["execution_status"], "PREFLIGHT_FAILED")


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cumcm_delivery_regression_")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def archive(self, files, name="成果.zip"):
        path = self.root / name
        with zipfile.ZipFile(path, "w") as zf:
            for member, data in files.items():
                zf.writestr(member, data)
        return path

    def test_zero_byte_paper_and_fake_pdf_rejected(self):
        for files in [{"论文.docx": b"", "论文.pdf": b""}, {"论文.pdf": b"%PDF-fake"}, {"论文.docx": docx("")}]:
            with self.subTest(files=list(files)):
                self.assertEqual(validate_zip(self.archive(files))["status"], "FAIL")

    def test_empty_or_directory_only_archive(self):
        for files in [{}, {"目录/": b""}, {"empty.txt": b""}]:
            with self.subTest(files=files):
                self.assertEqual(validate_zip(self.archive(files))["status"], "FAIL")

    def test_valid_docx_and_pdf_profile(self):
        result = validate_zip(self.archive({"参考论文/论文.docx": docx(), "参考论文/论文.pdf": pdf()}, "参考论文.zip"))
        self.assertEqual(result["status"], "PASS", result)
        self.assertEqual(result["scope"], "MECHANICAL_ONLY")

    def test_paper_profile_requires_both_formats(self):
        result = validate_zip(self.archive({"README.md": b"not a paper"}, "参考论文.zip"))
        self.assertEqual(result["status"], "FAIL")

    def test_zero_page_and_blank_pdf(self):
        for data in [pdf(no_pages=True), pdf(blank=True), pdf(initialization_only=True)]:
            self.assertEqual(validate_zip(self.archive({"论文.pdf": data}))["status"], "FAIL")

    def test_required_file_and_manifest(self):
        path = self.archive({"结果.csv": "值\n1\n"})
        self.assertEqual(validate_zip(path, required=("缺失.csv",))["status"], "FAIL")
        data = "值\n1\n".encode()
        manifest = {"files": [{"path": "结果.csv", "size": len(data), "sha256": hashlib.sha256(data).hexdigest()}]}
        self.assertEqual(validate_zip(path, manifest=manifest)["status"], "PASS")
        manifest["files"][0]["sha256"] = "0" * 64
        self.assertEqual(validate_zip(path, manifest=manifest)["status"], "FAIL")

    def test_empty_init_allowed_but_empty_result_is_not(self):
        path = self.archive({"__init__.py": b"", "入口.py": b"print('ok')"})
        self.assertEqual(validate_zip(path)["status"], "PASS")
        path = self.archive({"__init__.py": b"", "结果.csv": b""})
        self.assertEqual(validate_zip(path)["status"], "FAIL")

    def test_paths_and_budget(self):
        for name in ["../escape.txt", "/abs.txt", "C:/escape.txt", "a/../../escape", "C:escape.txt"]:
            self.assertFalse(safe_member(name))
            self.assertEqual(validate_zip(self.archive({name: b"x"}))["status"], "FAIL")
        self.assertEqual(validate_zip(self.archive({"ok.txt": b"123"}), max_bytes=2)["status"], "FAIL")

    def test_syntax_and_table_failures(self):
        for files in [{"入口.py": "def broken(:"}, {"结果.csv": "a,b\n1,2,3\n"}]:
            self.assertEqual(validate_zip(self.archive(files))["status"], "FAIL")


if __name__ == "__main__":
    unittest.main(verbosity=2)

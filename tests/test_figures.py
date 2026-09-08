#!/usr/bin/env python3
"""用真实 PNG/SVG/PDF 导出回归图片命名、覆盖边界及机械可读性。"""
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
from pypdf import PdfReader

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from figure_utils import apply_readable_defaults, assert_basic_labels, save_figure


class FigureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cumcm_figure_test_")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.fig, self.ax = plt.subplots(figsize=(3, 2))
        self.addCleanup(plt.close, self.fig)
        self.ax.plot([0, 1, 2], [0, 1, 4])
        self.ax.set(xlabel="x", ylabel="y")

    def test_decimal_and_version_names_do_not_collide(self):
        first = save_figure(self.fig, self.root / "参数0.1", formats="png")[0]
        original = first.read_bytes()
        self.ax.plot([0, 1], [3, 0])
        second = save_figure(self.fig, self.root / "参数0.2", formats=("png",))[0]
        self.assertEqual(first.name, "参数0.1.png")
        self.assertEqual(second.name, "参数0.2.png")
        self.assertEqual(first.read_bytes(), original)
        self.assertNotEqual(first.read_bytes(), second.read_bytes())

    def test_three_formats_are_parseable(self):
        outputs = save_figure(self.fig, self.root / "图1_验证.v2")
        self.assertEqual([p.suffix for p in outputs], [".png", ".svg", ".pdf"])
        with Image.open(outputs[0]) as picture:
            picture.verify()
        self.assertTrue(ET.parse(outputs[1]).getroot().tag.endswith("}svg"))
        reader = PdfReader(outputs[2])
        self.assertEqual(len(reader.pages), 1)
        self.assertIsNotNone(reader.pages[0].get_contents())

    def test_existing_target_rejected_before_any_new_format(self):
        old = self.root / "图1.svg"
        old.write_bytes(b"previous user artifact")
        with self.assertRaises(FileExistsError):
            save_figure(self.fig, self.root / "图1", formats=("png", "svg"))
        self.assertFalse((self.root / "图1.png").exists())
        self.assertEqual(old.read_bytes(), b"previous user artifact")

    def test_explicit_replacement(self):
        path = save_figure(self.fig, self.root / "图1", formats="png")[0]
        before = path.read_bytes()
        self.ax.plot([0, 1], [2, 3])
        save_figure(self.fig, self.root / "图1", formats="png", overwrite=True)
        self.assertNotEqual(path.read_bytes(), before)

    def test_bad_or_empty_formats_fail_without_files(self):
        for formats in [(), ("png", "PNG"), ("png", "nonsense"), ("",), (None,)]:
            with self.subTest(formats=formats), self.assertRaises(ValueError):
                save_figure(self.fig, self.root / "invalid", formats=formats)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_invalid_dpi(self):
        for dpi in [0, -1, float("inf"), float("nan")]:
            with self.subTest(dpi=dpi), self.assertRaises(ValueError):
                save_figure(self.fig, self.root / "invalid", dpi=dpi)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_render_failure_preserves_existing_files(self):
        old = self.root / "图1.png"
        old.write_bytes(b"previous")
        with patch.object(self.fig, "savefig", side_effect=RuntimeError("render failed")):
            with self.assertRaises(RuntimeError):
                save_figure(self.fig, self.root / "图1", overwrite=True)
        self.assertEqual(old.read_bytes(), b"previous")
        self.assertEqual(list(self.root.iterdir()), [old])

    def test_empty_renderer_output_is_not_success(self):
        with patch.object(self.fig, "savefig", return_value=None):
            with self.assertRaises(RuntimeError):
                save_figure(self.fig, self.root / "图1")
        self.assertEqual(list(self.root.iterdir()), [])

    def test_missing_chinese_font_reported(self):
        with matplotlib.rc_context(), patch("figure_utils.pick_chinese_font", return_value=None):
            with self.assertWarns(RuntimeWarning):
                self.assertIsNone(apply_readable_defaults())
            with self.assertRaises(RuntimeError):
                apply_readable_defaults(require_chinese=True)

    def test_basic_labels_and_close(self):
        assert_basic_labels(self.ax)
        self.ax.set_ylabel("")
        with self.assertRaises(ValueError):
            assert_basic_labels(self.ax)
        save_figure(self.fig, self.root / "图1", formats="png", close=True)
        self.assertFalse(plt.fignum_exists(self.fig.number))


if __name__ == "__main__":
    unittest.main(verbosity=2)

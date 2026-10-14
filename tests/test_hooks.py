"""Run with: python -m unittest discover -s tests -v."""

import io
import os
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import hooks


class ConfigTests(unittest.TestCase):
    def test_copyright_uses_current_year(self):
        for year in (2026, 2030):
            with self.subTest(year=year), patch.object(hooks, "datetime") as clock:
                clock.now.return_value = datetime(year, 1, 1)
                config = SimpleNamespace(copyright="OpenHUTB &copy; {year}")
                hooks.on_config(config)
                self.assertEqual(config.copyright, f"OpenHUTB &copy; {year}")

    def test_copyright_without_placeholder_is_preserved(self):
        config = SimpleNamespace(copyright="OpenHUTB")
        hooks.on_config(config)
        self.assertEqual(config.copyright, "OpenHUTB")


class PreBuildTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "docs").mkdir()
        module_path = patch.object(hooks, "__file__", str(self.root / "hooks.py"))
        module_path.start()
        self.addCleanup(module_path.stop)

    def test_copies_content_and_metadata_relative_to_hook_file(self):
        source = self.root / "CONTRIBUTING.md"
        source.write_text("# 贡献指南\n", encoding="utf-8")
        os.utime(source, (1600000000, 1600000000))
        output = io.StringIO()
        with redirect_stdout(output):
            hooks.on_pre_build()
        destination = self.root / "docs" / "CONTRIBUTING.md"
        self.assertEqual(destination.read_bytes(), source.read_bytes())
        self.assertEqual(destination.stat().st_mtime, source.stat().st_mtime)
        self.assertIn("Successfully copied CONTRIBUTING.md", output.getvalue())

    def test_repeated_build_refreshes_existing_copy(self):
        source = self.root / "CONTRIBUTING.md"
        source.write_text("first", encoding="utf-8")
        with redirect_stdout(io.StringIO()):
            hooks.on_pre_build()
            source.write_text("updated", encoding="utf-8")
            hooks.on_pre_build()
        self.assertEqual((self.root / "docs" / "CONTRIBUTING.md").read_text(), "updated")

    def test_missing_source_warns_and_preserves_existing_destination(self):
        destination = self.root / "docs" / "CONTRIBUTING.md"
        destination.write_text("existing", encoding="utf-8")
        with self.assertLogs(hooks.__name__, level="WARNING") as logs:
            hooks.on_pre_build()
        self.assertIn("CONTRIBUTING.md", logs.output[0])
        self.assertIn("not found", logs.output[0])
        self.assertEqual(destination.read_text(), "existing")


class PostBuildTests(unittest.TestCase):
    def test_counts_markdown_recursively_in_configured_docs_directory(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            docs = root / "custom-docs"
            (docs / "nested").mkdir(parents=True)
            for name in ("index.md", "nested/guide.md", "nested/中文.md", "notes.txt", "image.png"):
                (docs / name).touch()
            (root / "outside.md").touch()
            (docs / "directory.md").mkdir()
            output = io.StringIO()
            with redirect_stdout(output):
                hooks.on_post_build({"docs_dir": str(docs)})
            self.assertIn("文档网站构建完成", output.getvalue())
            self.assertIn("Markdown文档总数：3", output.getvalue())

    def test_empty_docs_directory_reports_zero(self):
        with TemporaryDirectory() as temporary, redirect_stdout(io.StringIO()) as output:
            hooks.on_post_build({"docs_dir": temporary})
        self.assertIn("Markdown文档总数：0", output.getvalue())


if __name__ == "__main__":
    unittest.main()

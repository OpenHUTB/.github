import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "src" / "git_commit_stats.py"
SPEC = importlib.util.spec_from_file_location("git_commit_stats", SCRIPT)
stats = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(stats)


class IgnoreUsersTests(unittest.TestCase):
    def test_valid_lists(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ignore.json"
            for users in ([], ["张三", "user@example.com"]):
                with self.subTest(users=users):
                    path.write_text(json.dumps(users), encoding="utf-8")
                    self.assertEqual(stats.load_ignore_users(str(path)), users)

    def test_missing_file_keeps_empty_list(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(stats.load_ignore_users(str(Path(directory) / "missing.json")), [])

    def test_invalid_types(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ignore.json"
            for value in (None, "张三", {}, [1], ["张三", None]):
                with self.subTest(value=value):
                    path.write_text(json.dumps(value), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, "字符串数组") as error:
                        stats.load_ignore_users(str(path))
                    self.assertIn(str(path), str(error.exception))

    def test_unreadable_or_malformed_content(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ignore.json"
            for content in (b"[", b"\xff"):
                with self.subTest(content=content):
                    path.write_bytes(content)
                    with self.assertRaisesRegex(ValueError, "读取屏蔽列表失败") as error:
                        stats.load_ignore_users(str(path))
                    self.assertIn(str(path), str(error.exception))

    def test_directory_is_not_a_valid_file(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "读取屏蔽列表失败"):
                stats.load_ignore_users(directory)

    def test_invalid_config_exits_before_query_or_output(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "ignore.json"
            output = Path(directory) / "stats.csv"
            output.write_text("existing result\n", encoding="utf-8")
            for content in ("null", '"张三"', "{", '[1]'):
                with self.subTest(content=content):
                    config.write_text(content, encoding="utf-8")
                    arguments = [str(SCRIPT), "--ignore", str(config), "--output", str(output)]
                    with patch.object(sys, "argv", arguments), patch.object(stats, "get_commits") as query:
                        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
                            stats.main()
                    self.assertEqual(error.exception.code, 2)
                    query.assert_not_called()
                    self.assertEqual(output.read_text(encoding="utf-8"), "existing result\n")


    def test_failed_git_query_does_not_overwrite_output(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "ignore.json"
            output = Path(directory) / "stats.csv"
            config.write_text("[]", encoding="utf-8")
            output.write_text("existing result\n", encoding="utf-8")
            arguments = [str(SCRIPT), "--ignore", str(config), "--output", str(output)]
            with patch.object(sys, "argv", arguments), patch.object(
                stats, "get_commits", side_effect=RuntimeError("git log failed")
            ) as query:
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
                    stats.main()
            self.assertEqual(error.exception.code, 2)
            query.assert_called_once()
            self.assertEqual(output.read_text(encoding="utf-8"), "existing result\n")


if __name__ == "__main__":
    unittest.main()

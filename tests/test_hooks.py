"""
hooks.py 的回归测试。

运行方式：
    需要 Python 3，仅使用标准库，无需安装 MkDocs、pytest 或其他依赖。
    请在项目根目录运行（根目录应包含 hooks.py 和 tests 文件夹）：
    python -m unittest discover -s tests -v

测试内容：
    1. 版权年份随当前年份更新。
    2. 无年份占位符的版权文本保持不变。
    3. 贡献指南复制后保留内容和修改时间。
    4. 重复构建时刷新已复制的贡献指南。
    5. 源文件缺失时记录警告，并保留原有目标文件。
    6. 贡献指南的编辑链接指向仓库根目录中的源文件。
    7. 其他页面的编辑链接保持不变。
    8. 递归统计指定文档目录中的 Markdown 文件，忽略其他文件和目录。
    9. 空文档目录的统计结果为 0。

预期运行效果：
    逐项输出测试名称，通过时每项末尾显示 ok，最后显示：
        Ran 11 tests in ...s

        OK
    实际耗时因环境而异；若显示 FAILED 或 ERROR，应检查后面的错误信息。
    被测函数的输出和缺失文件警告由测试捕获并验证，不会逐条打印。
    文件操作在自动清理的临时目录内进行，不修改项目中的实际文档。
"""

import io
import os
import shutil
import subprocess
import tempfile
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import hooks

# 临时 git 仓库建在 tests/_tmp（已被 .gitignore 忽略），避免依赖系统临时目录的权限。
TESTS_DIR = Path(__file__).resolve().parent


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

    def test_missing_copyright_does_not_break_build(self):
        config = SimpleNamespace(copyright=None)
        hooks.on_config(config)
        self.assertIsNone(config.copyright)


class PageContextTests(unittest.TestCase):
    def test_contributing_edit_url_points_to_root_source(self):
        context = {}
        page = SimpleNamespace(
            file=SimpleNamespace(src_uri="CONTRIBUTING.md"),
            edit_url="https://github.com/OpenHUTB/.github/edit/master/docs/CONTRIBUTING.md",
        )

        returned = hooks.on_page_context(context, page, {"docs_dir": "/repo/docs"})

        self.assertIs(returned, context)
        self.assertEqual(
            page.edit_url,
            "https://github.com/OpenHUTB/.github/edit/master/CONTRIBUTING.md",
        )

    def test_other_page_edit_url_is_preserved(self):
        context = {}
        edit_url = "https://github.com/OpenHUTB/.github/edit/master/docs/index.md"
        page = SimpleNamespace(
            file=SimpleNamespace(src_uri="index.md"),
            edit_url=edit_url,
        )

        returned = hooks.on_page_context(context, page, {"docs_dir": "/repo/docs"})

        self.assertIs(returned, context)
        self.assertEqual(page.edit_url, edit_url)


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
            hooks.on_pre_build({"docs_dir": str(self.root / "docs")})
        destination = self.root / "docs" / "CONTRIBUTING.md"
        self.assertEqual(destination.read_bytes(), source.read_bytes())
        self.assertEqual(destination.stat().st_mtime, source.stat().st_mtime)
        self.assertIn("Successfully copied CONTRIBUTING.md", output.getvalue())

    def test_repeated_build_refreshes_existing_copy(self):
        source = self.root / "CONTRIBUTING.md"
        source.write_text("first", encoding="utf-8")
        with redirect_stdout(io.StringIO()):
            hooks.on_pre_build({"docs_dir": str(self.root / "docs")})
            source.write_text("updated", encoding="utf-8")
            hooks.on_pre_build({"docs_dir": str(self.root / "docs")})
        self.assertEqual((self.root / "docs" / "CONTRIBUTING.md").read_text(), "updated")

    def test_missing_source_warns_and_preserves_existing_destination(self):
        destination = self.root / "docs" / "CONTRIBUTING.md"
        destination.write_text("existing", encoding="utf-8")
        with self.assertLogs(hooks.__name__, level="WARNING") as logs:
            hooks.on_pre_build({"docs_dir": str(self.root / "docs")})
        self.assertIn("CONTRIBUTING.md", logs.output[0])
        self.assertIn("not found", logs.output[0])
        self.assertEqual(destination.read_text(), "existing")

    def test_uses_configured_docs_directory(self):
        source = self.root / "CONTRIBUTING.md"
        source.write_text("# 贡献指南\n", encoding="utf-8")
        custom_docs = self.root / "custom-docs"
        with redirect_stdout(io.StringIO()):
            hooks.on_pre_build({"docs_dir": str(custom_docs)})
        self.assertEqual(
            (custom_docs / "CONTRIBUTING.md").read_bytes(),
            source.read_bytes(),
        )
        self.assertFalse((self.root / "docs" / "CONTRIBUTING.md").exists())


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


class PageProvenanceTests(unittest.TestCase):
    """on_page_markdown：在每页末尾附上「最近一次修改」的作者与提交。"""

    def setUp(self):
        base = TESTS_DIR / "_tmp"
        base.mkdir(exist_ok=True)
        self.root = Path(tempfile.mkdtemp(dir=str(base), prefix="provenance-"))
        (self.root / "docs" / "adv").mkdir(parents=True)
        (self.root / "docs" / "adv" / "find_author.md").write_text("# 页\n", encoding="utf-8")
        (self.root / "CONTRIBUTING.md").write_text("# 贡献指南\n", encoding="utf-8")
        self._git("init", "-q")
        self._git("add", "docs/adv/find_author.md", "CONTRIBUTING.md")
        self._git("commit", "-q", "-m", "docs: 第一版", name="张三")
        hooks._last_commit_cache.clear()

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def _git(self, *args, name="张三", email="tester@example.com"):
        subprocess.run(
            ["git", "-c", "user.name=" + name, "-c", "user.email=" + email, *args],
            cwd=str(self.root), check=True, capture_output=True, text=True,
        )

    def _page(self, src_uri):
        return SimpleNamespace(file=SimpleNamespace(src_uri=src_uri))

    def test_last_commit_reads_hash_date_and_author(self):
        info = hooks.last_commit("docs/adv/find_author.md", self.root)
        self.assertEqual(len(info), 3)
        commit_hash, date, author = info
        self.assertEqual(len(commit_hash), 7)
        self.assertRegex(date, r"^\d{4}-\d{2}-\d{2}$")
        self.assertEqual(author, "张三")

    def test_provenance_line_links_to_commit(self):
        line = hooks.provenance_line(self._page("adv/find_author.md"), self.root,
                                     "https://github.com/OpenHUTB/.github")
        self.assertIn("本页最近一次修改", line)
        self.assertIn("张三", line)
        self.assertIn("https://github.com/OpenHUTB/.github/commit/", line)
        self.assertTrue(line.startswith("> "), line)

    def test_provenance_line_without_repo_url_has_no_link(self):
        line = hooks.provenance_line(self._page("adv/find_author.md"), self.root)
        self.assertIn("提交 `", line)
        self.assertNotIn("](", line)

    def test_generated_contributing_uses_root_file_history(self):
        # docs/CONTRIBUTING.md 是构建时从根目录复制的，历史应取根目录那份。
        (self.root / "CONTRIBUTING.md").write_text("# 贡献指南第二版\n", encoding="utf-8")
        self._git("commit", "-q", "-am", "docs: 根目录更新", name="李四")
        hooks._last_commit_cache.clear()
        line = hooks.provenance_line(self._page("CONTRIBUTING.md"), self.root)
        self.assertIn("李四", line)

    def test_uncommitted_page_has_no_line(self):
        (self.root / "docs" / "new.md").write_text("# 新页\n", encoding="utf-8")
        hooks._last_commit_cache.clear()
        self.assertEqual(hooks.provenance_line(self._page("new.md"), self.root), "")

    def test_shallow_clone_is_skipped(self):
        (self.root / ".git" / "shallow").write_text("0" * 40 + "\n", encoding="utf-8")
        self.assertEqual(hooks.provenance_line(self._page("adv/find_author.md"), self.root), "")

    def test_page_markdown_keeps_content_and_appends_line(self):
        page = self._page("adv/find_author.md")
        with patch.object(hooks, "REPO_ROOT", self.root):
            result = hooks.on_page_markdown("# 标题\n\n正文。\n", page,
                                            {"repo_url": "https://github.com/OpenHUTB/.github"})
        self.assertTrue(result.startswith("# 标题\n\n正文。\n\n---\n\n> "), result)
        self.assertIn("张三", result)

    def test_page_markdown_survives_git_failure(self):
        page = self._page("adv/find_author.md")
        hooks._last_commit_cache.clear()
        with patch.object(hooks.subprocess, "run", side_effect=OSError("git missing")):
            result = hooks.on_page_markdown("# 标题\n", page,
                                            {"repo_url": "https://github.com/OpenHUTB/.github"})
        self.assertEqual(result, "# 标题\n")


if __name__ == "__main__":
    unittest.main()

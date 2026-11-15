"""Tests for src/find_author.py: path resolution, git log parsing and the CLI.

Temporary repositories are created under ``tests/_tmp/`` (git-ignored) rather than
in the system temp directory, so the tests also work in sandboxes that deny access
to 0o700 temp dirs. The integration test builds its own throwaway git repository,
so it does not depend on this repository's history (CI checkouts are shallow).
"""

import contextlib
import importlib.util
import io
import json
import shutil
import subprocess
import unittest
import uuid
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
SCRIPT = REPO_ROOT / "src" / "find_author.py"
SPEC = importlib.util.spec_from_file_location("find_author", SCRIPT)
find_author = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(find_author)


def run_git(repo, *args, name="测试 用户", email="tester@example.com"):
    return subprocess.run(
        ["git", "-c", "user.name=" + name, "-c", "user.email=" + email, *args],
        cwd=str(repo), check=True, capture_output=True, text=True,
    )


class TempDirTestCase(unittest.TestCase):
    """Create throwaway directories under tests/_tmp and remove them afterwards."""

    def make_temp_dir(self):
        base = SCRIPTS_DIR / "_tmp"
        base.mkdir(exist_ok=True)
        path = base / ("case-" + uuid.uuid4().hex[:8])
        path.mkdir()
        self.addCleanup(shutil.rmtree, path, True)
        return path


class ResolvePagePathTests(TempDirTestCase):
    def setUp(self):
        self.root = self.make_temp_dir()
        (self.root / "docs" / "adv").mkdir(parents=True)
        (self.root / "docs" / "adv" / "find_author.md").write_text("# x\n", encoding="utf-8")
        (self.root / "docs" / "simulator.md").write_text("# y\n", encoding="utf-8")

    def test_repo_relative_path(self):
        resolved = find_author.resolve_page_path("docs/simulator.md", self.root)
        self.assertEqual(resolved, (self.root / "docs" / "simulator.md").resolve())

    def test_site_path_without_extension(self):
        resolved = find_author.resolve_page_path("/adv/find_author/", self.root)
        self.assertEqual(resolved, (self.root / "docs" / "adv" / "find_author.md").resolve())

    def test_extension_is_optional(self):
        resolved = find_author.resolve_page_path("docs/simulator", self.root)
        self.assertEqual(resolved, (self.root / "docs" / "simulator.md").resolve())

    def test_missing_page_returns_none(self):
        self.assertIsNone(find_author.resolve_page_path("docs/no-such-page.md", self.root))


class ParseGitLogTests(unittest.TestCase):
    def test_parses_hash_author_date_and_subject(self):
        output = "a1b2c3d|张三|2026-11-01|docs: 修正表述\nff00ee1|李四|2026-10-30|feat: 新功能\n"
        commits = find_author.parse_git_log(output)
        self.assertEqual([commit["hash"] for commit in commits], ["a1b2c3d", "ff00ee1"])
        self.assertEqual(commits[0]["author"], "张三")
        self.assertEqual(commits[0]["date"], "2026-11-01")
        self.assertEqual(commits[1]["subject"], "feat: 新功能")

    def test_subject_may_contain_pipe(self):
        commits = find_author.parse_git_log("abc1234|王五|2026-11-02|fix: 处理 a|b 情况\n")
        self.assertEqual(commits[0]["subject"], "fix: 处理 a|b 情况")

    def test_ignores_blank_and_malformed_lines(self):
        commits = find_author.parse_git_log("\n不是提交\naaa1111|赵六|2026-11-03|ok\n")
        self.assertEqual([commit["hash"] for commit in commits], ["aaa1111"])

    def test_author_summary_is_sorted_by_count(self):
        commits = [{"author": "张三"}, {"author": "李四"}, {"author": "张三"}]
        self.assertEqual(find_author.summarize_authors(commits), [("张三", 2), ("李四", 1)])


class UrlTests(TempDirTestCase):
    def setUp(self):
        self.root = self.make_temp_dir()
        (self.root / "docs").mkdir()
        (self.root / "docs" / "a b.md").write_text("# x\n", encoding="utf-8")
        run_git(self.root, "init", "-q")
        run_git(self.root, "remote", "add", "origin",
                "https://github.com/OpenHUTB/.github.git")

    def test_github_slug_handles_https_and_ssh(self):
        self.assertEqual(find_author.github_slug("https://github.com/OpenHUTB/.github.git"),
                         "OpenHUTB/.github")
        self.assertEqual(find_author.github_slug("git@github.com:OpenHUTB/.github.git"),
                         "OpenHUTB/.github")
        self.assertEqual(find_author.github_slug(""), "")

    def test_history_url_encodes_spaces_and_uses_branch(self):
        urls = find_author.history_url(self.root / "docs" / "a b.md", self.root, "master")
        self.assertEqual(urls["history"],
                         "https://github.com/OpenHUTB/.github/commits/master/docs/a%20b.md")
        self.assertEqual(urls["blame"],
                         "https://github.com/OpenHUTB/.github/blame/master/docs/a%20b.md")


class CliIntegrationTests(TempDirTestCase):
    def setUp(self):
        self.root = self.make_temp_dir()
        (self.root / "docs").mkdir()
        page = self.root / "docs" / "demo.md"
        run_git(self.root, "init", "-q")
        page.write_text("# 第一版\n", encoding="utf-8")
        run_git(self.root, "add", "docs/demo.md")
        run_git(self.root, "commit", "-q", "-m", "docs: 第一版", name="张三")
        page.write_text("# 第二版\n", encoding="utf-8")
        run_git(self.root, "commit", "-q", "-am", "docs: 修正表述", name="李四")

    def _run(self, *argv):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(io.StringIO()):
            code = find_author.main(list(argv) + ["--repo-root", str(self.root)])
        return code, buffer.getvalue()

    def test_lists_every_author_and_commit(self):
        code, output = self._run("docs/demo.md")
        self.assertEqual(code, 0, output)
        self.assertIn("李四", output)
        self.assertIn("张三", output)
        self.assertIn("docs: 修正表述", output)
        self.assertIn("文件: docs/demo.md", output)

    def test_limit_is_respected(self):
        code, output = self._run("docs/demo.md", "--limit", "1")
        self.assertEqual(code, 0)
        self.assertIn("最近 1 次提交", output)
        self.assertNotIn("docs: 第一版", output)

    def test_json_output_contains_commits_and_urls(self):
        code, output = self._run("docs/demo.md", "--json")
        self.assertEqual(code, 0)
        payload = json.loads(output)
        self.assertEqual(payload["path"], "docs/demo.md")
        self.assertEqual(len(payload["commits"]), 2)
        self.assertEqual(payload["commits"][0]["author"], "李四")
        self.assertEqual(payload["authors"][0], {"author": "李四", "commits": 1})

    def test_missing_page_exits_2(self):
        buffer = io.StringIO()
        with contextlib.redirect_stderr(buffer):
            code = find_author.main(["docs/no-such.md", "--repo-root", str(self.root)])
        self.assertEqual(code, 2)
        self.assertIn("找不到页面", buffer.getvalue())

    def test_git_repository_without_commits_exits_3(self):
        # 空的 git 仓库：`git log` 会失败，脚本应以 3 退出并说明原因。
        plain = self.make_temp_dir()
        (plain / "docs").mkdir()
        (plain / "docs" / "x.md").write_text("# x\n", encoding="utf-8")
        run_git(plain, "init", "-q")
        buffer = io.StringIO()
        with contextlib.redirect_stderr(buffer):
            code = find_author.main(["docs/x.md", "--repo-root", str(plain)])
        self.assertEqual(code, 3)
        self.assertIn("读取提交历史失败", buffer.getvalue())


if __name__ == "__main__":
    unittest.main()

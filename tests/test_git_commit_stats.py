"""提交统计脚本的回归测试。"""

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class GitCommitStatsTests(unittest.TestCase):
    def test_runs_from_another_repository_but_counts_script_repository(self):
        project_root = Path(__file__).resolve().parents[1]
        source_script = project_root / "src" / "git_commit_stats.py"

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            script_repo = root / "脚本仓库"
            script_src = script_repo / "src"
            script_src.mkdir(parents=True)
            script_path = script_src / "git_commit_stats.py"
            script_path.write_bytes(source_script.read_bytes())
            self._init_repo(script_repo)
            self._commit(script_repo, "脚本仓库提交", "脚本仓库作者", "script@example.com")

            other_repo = root / "运行目录仓库"
            other_repo.mkdir()
            self._init_repo(other_repo)
            (other_repo / "记录.txt").write_text("第一次记录", encoding="utf-8")
            self._commit(other_repo, "运行目录提交一", "运行目录作者", "other@example.com")
            (other_repo / "记录.txt").write_text("第二次记录", encoding="utf-8")
            self._commit(other_repo, "运行目录提交二", "运行目录作者", "other@example.com")

            output_path = root / "统计.csv"
            result = subprocess.run(
                [
                    sys.executable,
                    str(script_path),
                    "--ignore",
                    str(root / "不存在的屏蔽名单.json"),
                    "--output",
                    str(output_path),
                ],
                cwd=other_repo,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            with output_path.open(encoding="utf-8", newline="") as stream:
                rows = list(csv.reader(stream))
            self.assertEqual(rows, [["User", "Commits"], ["脚本仓库作者", "1"]])

    def _init_repo(self, repository):
        subprocess.run(["git", "-C", str(repository), "init", "-q"], check=True)

    def _commit(self, repository, message, name, email):
        subprocess.run(
            ["git", "-C", str(repository), "add", "--all"],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(repository),
                "-c",
                f"user.name={name}",
                "-c",
                f"user.email={email}",
                "commit",
                "-q",
                "-m",
                message,
            ],
            check=True,
        )


if __name__ == "__main__":
    unittest.main()

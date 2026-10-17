"""提交统计在 Git 失败时不得覆盖现有报表。"""

import csv
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import git_commit_stats  # noqa: E402


class CommitStatsTests(unittest.TestCase):
    def test_git_failure_does_not_overwrite_report(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "report.csv"
            report.write_text("existing report\n", encoding="utf-8")
            argv = ["git_commit_stats.py", "--output", str(report)]
            completed = git_commit_stats.subprocess.CompletedProcess([], 128, "", "not a git repository")
            with patch.object(sys, "argv", argv), patch.object(
                git_commit_stats.subprocess, "run", return_value=completed
            ), patch("sys.stderr", new_callable=io.StringIO) as errors:
                with self.assertRaises(SystemExit) as stopped:
                    git_commit_stats.main()
            self.assertEqual(stopped.exception.code, 1)
            self.assertIn("not a git repository", errors.getvalue())
            self.assertEqual(report.read_text(encoding="utf-8"), "existing report\n")

    def test_successful_report_preserves_email_and_name_filtering(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "report.csv"
            ignored = Path(directory) / "ignore.json"
            ignored.write_text('["hidden@example.com"]', encoding="utf-8")
            argv = ["git_commit_stats.py", "--ignore", str(ignored), "--output", str(report)]
            log = "active@example.com|Alice\nhidden@example.com|Hidden\nactive@example.com|Alice\n"
            completed = git_commit_stats.subprocess.CompletedProcess([], 0, log, "")
            with patch.object(sys, "argv", argv), patch.object(
                git_commit_stats.subprocess, "run", return_value=completed
            ), patch("sys.stdout", new_callable=io.StringIO):
                git_commit_stats.main()
            with report.open(encoding="utf-8", newline="") as stream:
                self.assertEqual(list(csv.reader(stream)), [["User", "Commits"], ["Alice", "2"]])

    def test_valid_empty_history_still_writes_header(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "report.csv"
            argv = ["git_commit_stats.py", "--output", str(report)]
            completed = git_commit_stats.subprocess.CompletedProcess([], 0, "", "")
            with patch.object(sys, "argv", argv), patch.object(
                git_commit_stats.subprocess, "run", return_value=completed
            ), patch("sys.stdout", new_callable=io.StringIO):
                git_commit_stats.main()
            with report.open(encoding="utf-8", newline="") as stream:
                self.assertEqual(list(csv.reader(stream)), [["User", "Commits"]])


if __name__ == "__main__":
    unittest.main()

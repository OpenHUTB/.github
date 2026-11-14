"""Tests for serve.py: command planning, environment checks and the CLI flags.

No virtual environment is created, no pip install runs and no server is started:
``build_plan()`` is pure and ``--dry-run`` / ``--check`` exit before doing work.
"""

import io
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import serve


class BuildPlanTests(unittest.TestCase):
    def test_existing_venv_is_reused_and_installs_are_skipped_when_asked(self):
        root = Path(tempfile.mkdtemp(prefix="serve-plan-"))
        try:
            venv = root / ".venv"
            env_python = serve.venv_python(venv)
            env_python.parent.mkdir(parents=True)
            env_python.write_text("", encoding="utf-8")

            commands = serve.build_plan(venv, "127.0.0.1", 8000, install=False)
        finally:
            shutil.rmtree(root, ignore_errors=True)

        flat = [" ".join(map(str, command)) for command in commands]
        self.assertFalse(any("-m venv" in line for line in flat), flat)
        self.assertFalse(any("pip install" in line for line in flat), flat)
        self.assertTrue(any("mkdocs build" in line for line in flat), flat)
        self.assertTrue(any("mkdocs serve" in line and "127.0.0.1:8000" in line
                            for line in flat), flat)

    def test_missing_venv_creates_it_and_installs_requirements(self):
        root = Path(tempfile.mkdtemp(prefix="serve-plan-"))
        try:
            commands = serve.build_plan(root / ".venv")
        finally:
            shutil.rmtree(root, ignore_errors=True)

        flat = [" ".join(map(str, command)) for command in commands]
        self.assertTrue(any("-m venv" in line for line in flat), flat)
        self.assertTrue(any("pip install --upgrade pip" in line for line in flat), flat)

        requirements_index = next(
            index for index, line in enumerate(flat) if "requirements.txt" in line)
        fork_index = next(
            index for index, line in enumerate(flat) if serve.MKDOCS_FORK in line)
        self.assertLess(requirements_index, fork_index, flat)
        self.assertTrue(any("mkdocs build" in line for line in flat), flat)

    def test_serve_uses_requested_host_and_port(self):
        commands = serve.build_plan("/tmp/does-not-matter", "0.0.0.0", 8100)
        serve_command = [str(part) for part in commands[-1]]
        self.assertIn("--dev-addr", serve_command)
        self.assertIn("0.0.0.0:8100", serve_command)
        self.assertIn("--livereload", serve_command)

    def test_format_command_quotes_paths_with_spaces(self):
        rendered = serve.format_command(["python", "-m", "venv", "/tmp/a b/.venv"])
        self.assertTrue(rendered.endswith('"/tmp/a b/.venv"'), rendered)


class CheckEnvironmentTests(unittest.TestCase):
    def test_repository_passes_the_check(self):
        problems, lines = serve.check_environment()
        self.assertEqual(problems, [], lines)
        joined = "\n".join(lines)
        self.assertIn("requirements.txt 存在", joined)
        self.assertIn("mkdocs.yml 存在", joined)

    def test_missing_repository_files_are_reported(self):
        original_requirements, original_config = serve.REQUIREMENTS, serve.CONFIG
        try:
            serve.REQUIREMENTS = Path("definitely-missing-requirements.txt")
            serve.CONFIG = Path("definitely-missing-mkdocs.yml")
            problems, lines = serve.check_environment()
        finally:
            serve.REQUIREMENTS, serve.CONFIG = original_requirements, original_config

        self.assertIn("缺少 requirements.txt", problems)
        self.assertIn("缺少 mkdocs.yml", problems)


class CliTests(unittest.TestCase):
    def test_check_flag_exits_zero(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = serve.main(["--check"])
        self.assertEqual(code, 0)
        self.assertIn("环境检查通过", buffer.getvalue())

    def test_dry_run_prints_commands_and_exits_before_running_them(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = serve.main(["--dry-run", "--port", "8123", "--venv",
                               os.path.join(tempfile.gettempdir(), "nope-venv-dir")])
        output = buffer.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("将要执行的命令", output)
        self.assertIn("mkdocs serve", output)
        self.assertIn("127.0.0.1:8123", output)

    def test_help_lists_the_documented_flags(self):
        with self.assertRaises(SystemExit) as context:
            with redirect_stdout(io.StringIO()):
                serve.main(["--help"])
        self.assertEqual(context.exception.code, 0)


if __name__ == "__main__":
    unittest.main()

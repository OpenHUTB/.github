#!/usr/bin/env python3
"""跨平台的本地文档预览入口（替代只在 Windows 可用的 serve.bat）。

    python serve.py                 # 首次会建 .venv 并安装依赖，然后 build + serve
    python serve.py --check         # 只检查环境，不做任何安装或构建
    python serve.py --dry-run       # 打印将要执行的命令，不执行
    python serve.py --host 0.0.0.0 --port 8001 --no-browser

serve.bat 依赖 conda 与 cmd，macOS/Linux 上没法直接用；这个脚本用标准库的 venv 做同样的事：
准备虚拟环境 → 安装 requirements.txt 与社区版 mkdocs → mkdocs build → mkdocs serve --livereload。
"""

import argparse
import os
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
REQUIREMENTS = REPO_ROOT / "requirements.txt"
CONFIG = REPO_ROOT / "mkdocs.yml"
MKDOCS_FORK = "git+https://github.com/OpenHUTB/mkdocs.git"
DEFAULT_VENV = REPO_ROOT / ".venv"
MIN_PYTHON = (3, 8)


def venv_python(venv_dir):
    """Path to the interpreter inside a virtual environment."""
    if os.name == "nt":
        return Path(venv_dir) / "Scripts" / "python.exe"
    return Path(venv_dir) / "bin" / "python"


def build_plan(venv_dir=DEFAULT_VENV, host="127.0.0.1", port=8000,
               python=sys.executable, install=True):
    """Return the ordered list of commands the script would run.

    Keeping this pure makes the behaviour testable without creating a venv or
    touching the network.
    """
    venv_dir = Path(venv_dir)
    env_python = venv_python(venv_dir)
    commands = []

    if not env_python.exists():
        commands.append([python, "-m", "venv", str(venv_dir)])
        # 新环境里 pip 可能较旧，先升级再装依赖。
        commands.append([str(env_python), "-m", "pip", "install", "--upgrade", "pip"])
        install = True

    if install:
        commands.append([str(env_python), "-m", "pip", "install", "-r",
                         str(REQUIREMENTS)])
        commands.append([str(env_python), "-m", "pip", "install", MKDOCS_FORK])

    commands.append([str(env_python), "-m", "mkdocs", "build", "-f", str(CONFIG)])
    commands.append([str(env_python), "-m", "mkdocs", "serve", "-f", str(CONFIG),
                     "--dev-addr", "%s:%d" % (host, int(port)), "--livereload"])
    return commands


def format_command(command):
    """Render a command list for display, quoting arguments with spaces."""
    return " ".join(str(part) if " " not in str(part) else '"%s"' % part for part in command)


def check_environment(venv_dir=DEFAULT_VENV):
    """Offline checks that do not install or build anything.

    Returns ``(problems, lines)``: ``problems`` is empty when the repository can
    be previewed (a missing venv is fine, it will be created on the first run).
    """
    problems = []
    lines = []

    version = sys.version_info
    python_ok = version[:2] >= MIN_PYTHON
    lines.append("Python %d.%d.%d %s" % (
        version.major, version.minor, version.micro,
        "ok" if python_ok else "需要 >= %d.%d" % MIN_PYTHON))
    if not python_ok:
        problems.append("Python 版本过低")

    if REQUIREMENTS.is_file():
        lines.append("requirements.txt 存在 (%d 行)" % len(
            REQUIREMENTS.read_text(encoding="utf-8").splitlines()))
    else:
        lines.append("requirements.txt 缺失")
        problems.append("缺少 requirements.txt")

    if CONFIG.is_file():
        lines.append("mkdocs.yml 存在")
    else:
        lines.append("mkdocs.yml 缺失")
        problems.append("缺少 mkdocs.yml")

    env_python = venv_python(venv_dir)
    if env_python.exists():
        lines.append("虚拟环境已存在: %s" % venv_dir)
    else:
        lines.append("虚拟环境尚未创建: %s（首次运行会自动创建）" % venv_dir)

    git = shutil.which("git")
    lines.append("git: %s" % (git or "未找到（安装社区版 mkdocs 时需要）"))
    if not git:
        problems.append("未找到 git")

    return problems, lines


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="本地预览社区文档（跨平台替代 serve.bat）",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--host", default="127.0.0.1", help="监听地址")
    parser.add_argument("--port", type=int, default=8000, help="监听端口")
    parser.add_argument("--venv", default=str(DEFAULT_VENV), help="虚拟环境目录")
    parser.add_argument("--check", action="store_true", help="只检查环境，不安装也不构建")
    parser.add_argument("--dry-run", action="store_true", help="只打印将要执行的命令")
    parser.add_argument("--no-browser", action="store_true", help="构建成功后不自动打开浏览器")
    parser.add_argument("--no-install", action="store_true",
                        help="跳过依赖安装（虚拟环境里已经装好时用）")
    args = parser.parse_args(argv)

    if args.check:
        problems, lines = check_environment(args.venv)
        print("==> 文档预览环境检查")
        for line in lines:
            print("    " + line)
        if problems:
            print("\n存在问题: " + "；".join(problems))
            return 1
        print("\n环境检查通过。运行 `python serve.py` 即可本地预览。")
        return 0

    commands = build_plan(args.venv, args.host, args.port, install=not args.no_install)
    if args.dry_run:
        print("==> 将要执行的命令（未执行任何操作）")
        for command in commands:
            print("    " + format_command(command))
        return 0

    for index, command in enumerate(commands):
        print("$ " + format_command(command), flush=True)
        result = subprocess.run(command, cwd=REPO_ROOT)
        if result.returncode != 0:
            print("命令失败（退出码 %d）：%s" % (result.returncode, format_command(command)),
                  file=sys.stderr)
            return result.returncode
        # build 成功后、进入 serve 之前打开浏览器。
        if index == len(commands) - 2 and not args.no_browser:
            url = "http://%s:%d" % (args.host, args.port)
            print("构建完成，打开 %s" % url)
            try:
                webbrowser.open(url)
            except Exception:  # noqa: BLE001 - 打不开浏览器不影响预览
                print("无法自动打开浏览器，请手动访问 %s" % url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

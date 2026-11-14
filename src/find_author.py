"""
find_author.py
给定仓库里的文档页面，列出它的提交历史（作者、时间、提交说明），并打印可直接在浏览器打开的
GitHub History / Blame 链接。

对应 docs/adv/find_author.md 里「点 History 看是谁改的」那套手动步骤：这个脚本把同样的信息
一次性打印出来，省得在网页上层层点击。

用法：
    python src/find_author.py docs/adv/find_author.md
    python src/find_author.py /adv/find_author/ --limit 10
    python src/find_author.py docs/simulator.md --json
"""

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import quote

DEFAULT_LIMIT = 5
GIT_FORMAT = "%h|%an|%ad|%s"


def resolve_page_path(argument, repo_root):
    """把命令行参数解析成实际存在的文档文件路径，找不到时返回 None。

    支持三种写法：
    - 仓库相对路径：`docs/adv/find_author.md`
    - 站点路径：`/adv/find_author/`（自动补 `docs/`，目录时补 `index.md`）
    - 省略扩展名：`docs/simulator`
    """
    if not argument:
        return None

    repo_root = Path(repo_root)
    raw = argument.strip()
    candidates = []

    relative = raw
    while relative.startswith("./"):
        relative = relative[2:]
    relative = relative.strip("/")

    candidates.append(repo_root / relative)
    candidates.append(repo_root / "docs" / relative)
    candidates.append(repo_root / "docs" / relative / "index.md")
    if not relative.endswith(".md"):
        candidates.append(repo_root / (relative + ".md"))
        candidates.append(repo_root / "docs" / (relative + ".md"))

    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    return None


def parse_git_log(output):
    """把 `git log --format=%h|%an|%ad|%s` 的输出解析成提交列表。"""
    commits = []
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("|", 3)
        if len(parts) != 4:
            continue
        commit_hash, author, date, subject = parts
        commits.append(
            {
                "hash": commit_hash.strip(),
                "author": author.strip(),
                "date": date.strip(),
                "subject": subject.strip(),
            }
        )
    return commits


def summarize_authors(commits):
    """按提交数从多到少统计作者。"""
    return Counter(commit["author"] for commit in commits).most_common()


def read_git_output(args, repo_root):
    """执行 git 命令并返回 stdout；失败时抛 RuntimeError。"""
    result = subprocess.run(
        args,
        cwd=str(repo_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        message = (result.stderr or "").strip() or "git 命令执行失败"
        raise RuntimeError(message)
    return result.stdout


def git_history(page_path, repo_root, limit=DEFAULT_LIMIT):
    """读取某个文件的提交历史（跟随重命名）。"""
    relative = Path(page_path).resolve().relative_to(Path(repo_root).resolve())
    output = read_git_output(
        [
            "git",
            "log",
            "--follow",
            "-n",
            str(limit),
            "--date=short",
            "--pretty=format:" + GIT_FORMAT,
            "--",
            relative.as_posix(),
        ],
        repo_root,
    )
    return parse_git_log(output)


def remote_url(repo_root):
    """取 origin 的 URL，失败时返回空字符串。"""
    try:
        return read_git_output(["git", "remote", "get-url", "origin"], repo_root).strip()
    except RuntimeError:
        return ""


def github_slug(url):
    """从 remote URL 中解析出 owner/repo。"""
    if not url:
        return ""
    cleaned = url.strip()
    if cleaned.startswith("git@"):
        cleaned = cleaned.split(":", 1)[-1]
    else:
        cleaned = cleaned.split("://", 1)[-1]
        cleaned = cleaned.split("/", 1)[-1]
    cleaned = cleaned.rstrip("/")
    if cleaned.endswith(".git"):
        cleaned = cleaned[: -len(".git")]
    parts = [part for part in cleaned.split("/") if part]
    if len(parts) < 2:
        return ""
    return "%s/%s" % (parts[0], parts[1])


def current_branch(repo_root):
    """当前分支名；detached HEAD 时回退到 master。"""
    try:
        branch = read_git_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo_root).strip()
    except RuntimeError:
        return "master"
    return branch if branch and branch != "HEAD" else "master"


def history_url(page_path, repo_root, branch=None):
    """返回页面的 GitHub 提交历史与 blame 链接。"""
    slug = github_slug(remote_url(repo_root))
    if not slug:
        return {}
    relative = Path(page_path).resolve().relative_to(Path(repo_root).resolve()).as_posix()
    branch = branch or current_branch(repo_root)
    encoded = quote(relative)
    base = "https://github.com/%s" % slug
    return {
        "history": "%s/commits/%s/%s" % (base, branch, encoded),
        "blame": "%s/blame/%s/%s" % (base, branch, encoded),
    }


def format_report(page_path, commits, authors, urls):
    """把结果排版成便于阅读的文本。"""
    lines = ["文件: %s" % page_path, ""]
    if commits:
        lines.append("最近 %d 次提交:" % len(commits))
        for commit in commits:
            lines.append(
                "  %-8s %-11s %-14s %s"
                % (commit["hash"], commit["date"], commit["author"], commit["subject"])
            )
        lines.append("")
        lines.append("作者（按提交数）: " + ", ".join(
            "%s (%d)" % (author, count) for author, count in authors))
    else:
        lines.append("没有找到这个文件的提交记录。")
    if urls:
        lines.append("")
        lines.append("在浏览器中查看: %s" % urls.get("history", ""))
        lines.append("逐行看是谁改的: %s" % urls.get("blame", ""))
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="查看某个文档页面的提交历史与作者")
    parser.add_argument("page", help="页面路径，例如 docs/adv/find_author.md 或 /adv/find_author/")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="显示最近多少次提交")
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[1]),
                        help="仓库根目录，默认为脚本的上一级目录")
    parser.add_argument("--branch", default=None, help="生成链接用的分支名，默认取当前分支")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出")
    args = parser.parse_args(argv)

    if args.limit < 1:
        print("--limit 必须大于 0", file=sys.stderr)
        return 2

    repo_root = Path(args.repo_root).resolve()
    page_path = resolve_page_path(args.page, repo_root)
    if page_path is None:
        print("找不到页面: %s（可用仓库相对路径或站点路径，例如 docs/simulator.md）"
              % args.page, file=sys.stderr)
        return 2

    try:
        commits = git_history(page_path, repo_root, args.limit)
    except RuntimeError as error:
        print("读取提交历史失败: %s" % error, file=sys.stderr)
        return 3

    authors = summarize_authors(commits)
    urls = history_url(page_path, repo_root, args.branch)

    if args.json:
        print(json.dumps(
            {
                "path": page_path.relative_to(repo_root).as_posix(),
                "commits": commits,
                "authors": [{"author": author, "commits": count} for author, count in authors],
                "urls": urls,
            },
            ensure_ascii=False,
            indent=2,
        ))
        return 0

    print(format_report(page_path.relative_to(repo_root).as_posix(), commits, authors, urls))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

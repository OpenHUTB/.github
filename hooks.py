from datetime import datetime
import logging
import shutil
import subprocess
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

# 仓库根目录中的社区文件 -> 构建时生成的文档站页面。
GENERATED_DOC_FILES = {
    "CONTRIBUTING.md": "CONTRIBUTING.md",
    "community/code-of-conduct.md": "CODE_OF_CONDUCT.md",
}

# 每轮构建中每个文件只查一次 git，27 个页面也只多 27 次子进程调用。
_last_commit_cache = {}


def is_shallow_clone(repo_root=None):
    """浅克隆（如 CI 默认的 fetch-depth=1）里每个文件的「最近提交」都是合并提交，会误导读者。"""
    root = Path(repo_root) if repo_root else REPO_ROOT
    return (root / ".git" / "shallow").is_file()


def last_commit(source_path, repo_root=None):
    """返回文件最近一次提交的 (短哈希, 日期, 作者)，取不到时返回 None。"""
    root = Path(repo_root) if repo_root else REPO_ROOT
    key = (str(root), source_path)
    if key in _last_commit_cache:
        return _last_commit_cache[key]

    info = None
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--date=short", "--pretty=format:%h|%ad|%an",
             "--", source_path],
            cwd=str(root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )
    except OSError:
        result = None

    if result is not None and result.returncode == 0 and result.stdout.strip():
        parts = result.stdout.strip().split("|")
        if len(parts) == 3:
            info = tuple(part.strip() for part in parts)

    _last_commit_cache[key] = info
    return info


def provenance_line(page, repo_root=None, repo_url=None):
    """生成「本页最近一次修改」那一行；取不到信息时返回空字符串。"""
    src_uri = page.file.src_uri
    # 生成页的历史要查仓库根目录中的源文件，而不是 docs/ 下的构建副本。
    source_path = GENERATED_DOC_FILES.get(src_uri, "docs/" + src_uri)

    root = Path(repo_root) if repo_root else REPO_ROOT
    if is_shallow_clone(root):
        return ""

    info = last_commit(source_path, root)
    if not info:
        return ""

    commit_hash, date, author = info
    line = "> 本页最近一次修改：%s · %s" % (date, author)
    if repo_url:
        line += " · 提交 [`%s`](%s/commit/%s)" % (commit_hash, repo_url.rstrip("/"), commit_hash)
    else:
        line += " · 提交 `%s`" % commit_hash
    return line


# 在每页正文末尾附上「最近一次修改」的作者与提交，方便读者找到该页的维护者。
def on_page_markdown(markdown, page, config, **kwargs):
    try:
        line = provenance_line(page, repo_url=config.get("repo_url"))
    except Exception:  # noqa: BLE001 - 附加信息失败不该让整站构建失败
        logging.getLogger(__name__).warning("跳过页面修改信息：%s", page.file.src_uri)
        return markdown

    if not line:
        return markdown
    return markdown.rstrip() + "\n\n---\n\n" + line + "\n"


# 动态获取页脚版权页面的年份
def on_config(config, **kwargs):
    year = str(datetime.now().year)
    copyright_text = getattr(config, "copyright", None)
    if copyright_text:
        config.copyright = copyright_text.replace("{year}", year)


# 生成页是从仓库根目录复制的，编辑按钮也应指回根目录源文件。
def on_page_context(context, page, config, **kwargs):
    source_name = GENERATED_DOC_FILES.get(page.file.src_uri)
    if not source_name or not page.edit_url:
        return context

    docs_name = Path(config["docs_dir"]).name
    generated_suffix = f"/{docs_name}/{page.file.src_uri}"
    if page.edit_url.endswith(generated_suffix):
        page.edit_url = page.edit_url[: -len(generated_suffix)] + "/" + source_name
    return context


# 在 MkDocs 构建开始前，将根目录下的社区文件复制到文档站页面。
# （名称必须为 on_pre_build）
def on_pre_build(config, **kwargs):
    # mkdocs serve 会复用 hook 模块，下一轮构建应重新读取提交历史。
    _last_commit_cache.clear()

    docs_dir = config["docs_dir"]
    repo_root = Path(__file__).resolve().parent

    for destination, source_name in GENERATED_DOC_FILES.items():
        src_file = repo_root / source_name
        dest_file = Path(docs_dir) / destination
        dest_file.parent.mkdir(parents=True, exist_ok=True)

        if src_file.exists():
            shutil.copy2(src_file, dest_file)
            print(
                "Successfully copied %s to %s"
                % (source_name, dest_file.relative_to(repo_root))
            )
        else:
            logging.getLogger(__name__).warning(
                "Source file not found: %s; %s was not copied",
                src_file,
                destination,
            )


# 构建完成后，输出文档构建统计信息
def on_post_build(config, **kwargs):
    docs_path = config["docs_dir"]
    md_count = 0
    # 遍历统计所有md文档数量
    for root, dirs, files in os.walk(docs_path):
        for f in files:
            if f.endswith(".md"):
                md_count += 1
    print("文档网站构建完成！")
    print(f"检测到Markdown文档总数：{md_count}")

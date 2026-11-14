"""Ensure every docs page is reachable from the MkDocs navigation.

The site build does not fail when a page is missing from ``nav:`` -- the page is
simply unreachable from the menu, which is how ``adv/find_author.md`` and the
Minecraft guide had been hidden. This test keeps the navigation and the
``docs/`` tree in sync, and also catches nav entries that point at missing files.

Nav targets are normalised before they are compared: ``./index.md``, ``index.md``,
extension-less and directory entries (``adv`` / ``adv/``) and targets carrying a
``?query`` or ``#fragment`` all resolve to the same docs page.

``docs/CONTRIBUTING.md`` is generated from the repository root guide by hooks.py
before the build, so it is treated as a logical site page and excluded from the
"on disk" page list -- whether or not a previous local build left it behind.
"""

import re
import shutil
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit


REPO_ROOT = Path(__file__).resolve().parents[1]
MKDOCS_FILE = REPO_ROOT / "mkdocs.yml"
DOCS_DIR = REPO_ROOT / "docs"

# hooks.py copies the repository-root guide into docs/ before the build starts,
# so the nav entry for CONTRIBUTING.md is valid even though docs/CONTRIBUTING.md
# is not committed. Same mapping as tests/test_docs_links.py.
GENERATED_DOC_FILES = {
    "CONTRIBUTING.md": REPO_ROOT / "CONTRIBUTING.md",
}

# Pages that are deliberately kept out of the navigation, with the reason.
# Keep this empty unless a page really should stay unlisted.
NAV_IGNORED = {}

NAV_START = re.compile(r"^nav\s*:\s*$")
NAV_ITEM = re.compile(r"^\s*-\s+(.*)$")
QUOTED_TARGET = re.compile(r"""['"]([^'"]+\.(?:md|html?))['"]""")
HTTP_PREFIXES = ("http://", "https://", "mailto:")


def normalize_target(raw_target):
    """Strip a nav target down to a local page path, or return '' for remote links.

    ``urlsplit`` keeps this consistent with tests/test_docs_links.py: the query
    string and fragment are dropped (a nav entry never needs them) and percent
    escapes are decoded, so ``docs/%E4%B8%AD.md#top`` becomes ``docs/中.md``.
    """
    if not raw_target:
        return ""
    parsed = urlsplit(raw_target)
    if parsed.scheme or parsed.netloc or raw_target.lower().startswith(HTTP_PREFIXES):
        return ""
    if raw_target.startswith("//"):
        return ""
    return unquote(parsed.path).strip()


def nav_page_paths(mkdocs_text):
    """Return the local page paths referenced by the nav, in order.

    Handles the shapes used in mkdocs.yml: quoted targets, bare targets and
    section items whose title contains a colon (including the full-width '：').
    Remote entries are skipped; fragments/queries are stripped.
    """
    paths = []
    in_nav = False
    for raw_line in mkdocs_text.splitlines():
        if not in_nav:
            if NAV_START.match(raw_line):
                in_nav = True
            continue

        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        # A line that starts at column 0 and is not a list item ends the nav block.
        if not raw_line[0].isspace() and not stripped.startswith("-"):
            break

        item_match = NAV_ITEM.match(raw_line)
        if not item_match:
            continue
        item = item_match.group(1).strip()
        if not item:
            continue

        quoted = QUOTED_TARGET.search(item)
        if quoted:
            raw_target = quoted.group(1)
        elif ":" in item:
            raw_target = item.rsplit(":", 1)[1].strip().strip("'\"")
        else:
            raw_target = item.strip("'\"")

        target = normalize_target(raw_target)
        if target:
            paths.append(target)
    return paths


def docs_pages(docs_dir=None, generated=None):
    """Relative POSIX paths of every Markdown page under docs/.

    Files that hooks.py generates into docs/ are excluded: they are build
    artifacts, not source pages, so a leftover copy from a previous local build
    must not make the coverage check fail.
    """
    root = Path(docs_dir) if docs_dir is not None else DOCS_DIR
    generated_names = set(generated if generated is not None else GENERATED_DOC_FILES)
    return sorted(
        page.relative_to(root).as_posix()
        for page in root.rglob("*.md")
        if page.relative_to(root).as_posix() not in generated_names
    )


def resolve_target(target, docs_dir=None, generated=None):
    """Return the existing file a normalised nav target points at, or None.

    Accepts ``page.md``, extension-less ``page`` and directory entries ``dir``
    or ``dir/`` (both resolve to ``dir/index.md``), matching MkDocs behaviour.
    """
    if not target:
        return None
    root = Path(docs_dir) if docs_dir is not None else DOCS_DIR
    generated_map = generated if generated is not None else GENERATED_DOC_FILES
    cleaned = target[2:] if target.startswith("./") else target
    if cleaned in generated_map:
        return Path(generated_map[cleaned])
    candidates = [root / cleaned]
    if cleaned.endswith("/"):
        candidates.append(root / cleaned / "index.md")
    else:
        candidates.extend([root / (cleaned + ".md"), root / cleaned / "index.md"])
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def listed_docs_pages(mkdocs_text, docs_dir=None, generated=None):
    """Nav entries expressed as paths relative to docs/ (generated pages included)."""
    root = (Path(docs_dir) if docs_dir is not None else DOCS_DIR).resolve()
    generated_map = generated if generated is not None else GENERATED_DOC_FILES
    generated_by_target = {
        Path(target).resolve(): name for name, target in generated_map.items()
    }

    listed = set()
    for target in nav_page_paths(mkdocs_text):
        resolved = resolve_target(target, docs_dir=root, generated=generated_map)
        if resolved is None:
            continue
        resolved = resolved.resolve()
        logical = generated_by_target.get(resolved)
        if logical is not None:
            # 生成页（如 CONTRIBUTING.md）按逻辑站点路径记账，不落进 docs/ 也能对得上。
            listed.add(logical)
            continue
        try:
            listed.add(resolved.relative_to(root).as_posix())
        except ValueError:
            continue
    return listed


class NavParserTests(unittest.TestCase):
    def test_quoted_and_bare_entries(self):
        text = (
            "site_name: demo\n"
            "nav:\n"
            "- 首页: 'index.md'\n"
            "- 普通页面: plain.md\n"
            "- 直接写路径.md\n"
            "markdown_extensions:\n"
            "  - footnotes\n"
        )
        self.assertEqual(
            nav_page_paths(text),
            ["index.md", "plain.md", "直接写路径.md"],
        )

    def test_nested_sections_and_remote_entries(self):
        text = (
            "nav:\n"
            "- 分组:\n"
            "    - 子页: 'dev/sign_up.md'\n"
            "- git 教程: 'https://openhutb.github.io/git/?locale=zh_CN'\n"
            "- 论文: \"paper/avf.md\"\n"
            "plugins: []\n"
        )
        self.assertEqual(nav_page_paths(text), ["dev/sign_up.md", "paper/avf.md"])

    def test_title_with_colon_is_not_mistaken_for_target(self):
        text = "nav:\n- 论文成果：AVF-BEL 视听融合: 'paper/avf.md'\nplugins: []\n"
        self.assertEqual(nav_page_paths(text), ["paper/avf.md"])

    def test_fragment_query_and_escapes_are_stripped(self):
        text = (
            "nav:\n"
            "- 顶部: 'index.md#top'\n"
            "- 带参数: 'paper/avf.md?plain=1'\n"
            "- 编码路径: 'adv/%E4%B8%AD.md#sec'\n"
            "plugins: []\n"
        )
        self.assertEqual(
            nav_page_paths(text),
            ["index.md", "paper/avf.md", "adv/中.md"],
        )


class ResolveTargetTests(unittest.TestCase):
    def test_variants_resolve_to_the_same_page(self):
        expected = resolve_target("index.md")
        self.assertIsNotNone(expected)
        for variant in ("index.md", "./index.md", "index", "index.md#top",
                        "index.md?x=1"):
            self.assertEqual(
                resolve_target(normalize_target(variant)), expected,
                "variant did not resolve: " + variant,
            )

    def test_missing_target_returns_none(self):
        self.assertIsNone(resolve_target("no-such-page.md"))

    def test_listed_pages_are_normalised(self):
        text = (
            "nav:\n"
            "- 首页: './index.md'\n"
            "- 论文: 'paper/avf.md#top'\n"
            "- 无扩展名: 'tools'\n"
            "plugins: []\n"
        )
        self.assertEqual(
            listed_docs_pages(text),
            {"index.md", "paper/avf.md", "tools.md"},
        )


class GeneratedPageTests(unittest.TestCase):
    """hooks.py 生成的页面不该因为本地构建留下副本就被报成「未收录」。"""

    def _layout(self, root, keep_generated_copy):
        docs = root / "docs"
        docs.mkdir()
        (docs / "index.md").write_text("# 首页\n", encoding="utf-8")
        (root / "CONTRIBUTING.md").write_text("# 贡献指南（源文件）\n", encoding="utf-8")
        if keep_generated_copy:
            (docs / "CONTRIBUTING.md").write_text("# 贡献指南（构建副本）\n",
                                                  encoding="utf-8")
        generated = {"CONTRIBUTING.md": root / "CONTRIBUTING.md"}
        nav = "nav:\n- 首页: 'index.md'\n- 贡献指南: 'CONTRIBUTING.md'\nplugins: []\n"
        return docs, generated, nav

    def test_generated_copy_on_disk_is_not_reported_as_unlisted(self):
        root = Path(tempfile.mkdtemp(prefix="docs-nav-"))
        try:
            docs, generated, nav = self._layout(root, keep_generated_copy=True)
            pages = docs_pages(docs_dir=docs, generated=generated)
            listed = listed_docs_pages(nav, docs_dir=docs, generated=generated)

            self.assertEqual(pages, ["index.md"])
            self.assertIn("CONTRIBUTING.md", listed)
            self.assertEqual([p for p in pages if p not in listed], [])
        finally:
            shutil.rmtree(root, ignore_errors=True)

    def test_generated_page_survives_a_build_that_did_not_run_yet(self):
        root = Path(tempfile.mkdtemp(prefix="docs-nav-"))
        try:
            docs, generated, nav = self._layout(root, keep_generated_copy=False)
            pages = docs_pages(docs_dir=docs, generated=generated)
            listed = listed_docs_pages(nav, docs_dir=docs, generated=generated)

            self.assertEqual(pages, ["index.md"])
            self.assertIn("CONTRIBUTING.md", listed)
        finally:
            shutil.rmtree(root, ignore_errors=True)


class RepositoryNavTests(unittest.TestCase):
    def test_nav_entries_resolve(self):
        paths = nav_page_paths(MKDOCS_FILE.read_text(encoding="utf-8"))
        self.assertTrue(paths, "mkdocs.yml should define a nav block")

        missing = [target for target in paths if resolve_target(target) is None]
        self.assertEqual(
            missing, [],
            "Nav entries point at files that do not exist:\n" + "\n".join(missing),
        )

    def test_every_docs_page_is_listed(self):
        listed = listed_docs_pages(MKDOCS_FILE.read_text(encoding="utf-8"))
        unlisted = [
            page for page in docs_pages()
            if page not in listed and page not in NAV_IGNORED
        ]
        self.assertEqual(
            unlisted, [],
            "These docs pages are not reachable from the nav:\n"
            + "\n".join(unlisted)
            + "\nAdd them to mkdocs.yml, or list them in NAV_IGNORED with a reason.",
        )


if __name__ == "__main__":
    unittest.main()

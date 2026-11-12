"""Ensure every docs page is reachable from the MkDocs navigation.

The site build does not fail when a page is missing from ``nav:`` — the page is
simply unreachable from the menu, which is how ``adv/find_author.md`` and the
Minecraft guide had been hidden. This test keeps the navigation and the
``docs/`` tree in sync, and also catches nav entries that point at missing files.
"""

import re
import unittest
from pathlib import Path


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


def nav_page_paths(mkdocs_text):
    """Return the local page paths referenced by the nav, in order.

    Handles the shapes used in mkdocs.yml: quoted targets, bare targets and
    section items whose title contains a colon (including the full-width '：').
    Remote entries are skipped.
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
            target = quoted.group(1)
        elif ":" in item:
            target = item.rsplit(":", 1)[1].strip().strip("'\"")
        else:
            target = item.strip("'\"")

        if not target or target.lower().startswith(HTTP_PREFIXES) or target.startswith("//"):
            continue
        paths.append(target)
    return paths


def docs_pages():
    """Relative POSIX paths of every Markdown page under docs/."""
    return sorted(
        page.relative_to(DOCS_DIR).as_posix()
        for page in DOCS_DIR.rglob("*.md")
    )


def resolve_target(target):
    """Return the existing file a nav entry points at, or None."""
    if target in GENERATED_DOC_FILES:
        return GENERATED_DOC_FILES[target]
    for candidate in (DOCS_DIR / target, DOCS_DIR / (target + ".md"),
                      DOCS_DIR / target / "index.md"):
        if candidate.is_file():
            return candidate
    return None


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
        listed = set(nav_page_paths(MKDOCS_FILE.read_text(encoding="utf-8")))
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

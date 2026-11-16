"""Validate relative links in repository Markdown files."""

import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit


REPO_ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(\s*(<[^>]+>|[^\s)]+)")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")

# MkDocs copies the root contribution guide into docs before building.
GENERATED_DOC_FILES = {
    (REPO_ROOT / "docs" / "CONTRIBUTING.md").resolve(): (
        REPO_ROOT / "CONTRIBUTING.md"
    ).resolve()
}


def iter_relative_links(markdown_file):
    """Yield relative link targets outside fenced code blocks."""
    fence_character = None
    for line_number, line in enumerate(
        markdown_file.read_text(encoding="utf-8").splitlines(), start=1
    ):
        fence_match = FENCE.match(line)
        if fence_match:
            character = fence_match.group(1)[0]
            if fence_character is None:
                fence_character = character
            elif character == fence_character:
                fence_character = None
            continue

        if fence_character is not None:
            continue

        for match in MARKDOWN_LINK.finditer(line):
            raw_target = match.group(1)
            if raw_target.startswith("<") and raw_target.endswith(">"):
                raw_target = raw_target[1:-1]

            parsed = urlsplit(raw_target)
            if (
                parsed.scheme
                or parsed.netloc
                or raw_target.startswith("#")
                or parsed.path.startswith("/")
            ):
                continue

            target_path = unquote(parsed.path)
            if target_path:
                yield line_number, raw_target, target_path


class RelativeMarkdownLinkTests(unittest.TestCase):
    def test_relative_links_resolve(self):
        missing = []
        for markdown_file in REPO_ROOT.rglob("*.md"):
            if ".git" in markdown_file.parts or "site" in markdown_file.parts:
                continue

            for line_number, raw_target, target_path in iter_relative_links(
                markdown_file
            ):
                resolved_target = (markdown_file.parent / target_path).resolve()
                resolved_target = GENERATED_DOC_FILES.get(
                    resolved_target, resolved_target
                )
                if not resolved_target.exists():
                    missing.append(
                        f"{markdown_file.relative_to(REPO_ROOT)}:"
                        f"{line_number}: {raw_target}"
                    )

        self.assertEqual(
            missing,
            [],
            "Relative Markdown links point to missing targets:\n"
            + "\n".join(missing),
        )


if __name__ == "__main__":
    unittest.main()

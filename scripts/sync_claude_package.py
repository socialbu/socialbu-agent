#!/usr/bin/env python3
"""Keep the Claude directory package aligned with the shared plugin sources."""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sync_package(root: Path = ROOT, check: bool = False) -> None:
    package = root / "plugins/claude"
    paths = [Path(name) for name in (".claude-plugin/plugin.json", ".mcp.json", "LICENSE", "assets/logo.png")]
    paths.extend(path.relative_to(root) for path in sorted((root / "skills").rglob("*.md")))
    expected = {path: (root / path).read_bytes() for path in paths}
    # The listing README is Claude-specific; skills and connection settings are shared.
    expected[Path("README.md")] = (package / "README.md").read_bytes()
    for path, content in expected.items():
        if path.suffix != ".png":
            text = content.decode("utf-8")
            assert not text.startswith("#!") and "\0" not in text, f"Unsupported Claude content: {path}"

    actual = {path.relative_to(package) for path in package.rglob("*") if path.is_file()}
    assert not actual - expected.keys(), f"Unexpected Claude package files: {actual - expected.keys()}"
    for path, content in expected.items():
        destination = package / path
        if check:
            assert destination.is_file() and destination.read_bytes() == content, f"Run python scripts/sync_claude_package.py: {path}"
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the committed package is out of date")
    sync_package(check=parser.parse_args().check)
    print("Claude package is synchronized.")

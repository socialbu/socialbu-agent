#!/usr/bin/env python3
"""Check that the submitted Claude folder stays complete and source-only."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from sync_claude_package import ROOT, sync_package


class ClaudePackageTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for name in (".claude-plugin", ".mcp.json", "LICENSE", "assets", "skills", "plugins/claude"):
            source = ROOT / name
            destination = self.root / name
            if source.is_dir():
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
        self.package = self.root / "plugins/claude"

    def test_package_matches_sources_and_loads_components(self):
        sync_package(self.root, check=True)
        manifest = json.loads((self.package / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertTrue((self.package / manifest["mcpServers"]).is_file())
        for skill in manifest["skills"]:
            self.assertTrue((self.package / skill / "SKILL.md").is_file())
        self.assertTrue((self.package / "skills/socialbu/references/publishing.md").is_file())

    def test_source_changes_require_regeneration(self):
        source = self.root / "skills/socialbu/SKILL.md"
        source.write_text(source.read_text(encoding="utf-8") + "\nUpdated instructions.\n", encoding="utf-8")
        with self.assertRaises(AssertionError):
            sync_package(self.root, check=True)
        sync_package(self.root)
        sync_package(self.root, check=True)
        self.assertEqual(source.read_bytes(), (self.package / "skills/socialbu/SKILL.md").read_bytes())

    def test_unexpected_files_are_rejected(self):
        for filename in ("build.py", "logo.svg", "package.json"):
            with self.subTest(filename=filename):
                unwanted = self.package / filename
                unwanted.write_text("{}", encoding="utf-8")
                with self.assertRaises(AssertionError):
                    sync_package(self.root, check=True)
                unwanted.unlink()


if __name__ == "__main__":
    unittest.main()

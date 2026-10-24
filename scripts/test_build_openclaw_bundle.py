#!/usr/bin/env python3
"""Check the shipped bundle, including OAuth and its source-file boundary."""

import json
import tarfile
import tempfile
import unittest
from pathlib import Path

from build_openclaw_bundle import ROOT, build_bundle


class OpenClawBundleTest(unittest.TestCase):
    def test_bundle_contains_both_skills_and_oauth_without_runtime_code(self):
        original = (ROOT / ".mcp.json").read_bytes()
        with tempfile.TemporaryDirectory() as temporary:
            with tarfile.open(build_bundle(Path(temporary)), "r:gz") as archive:
                members = {item.name for item in archive.getmembers() if item.isfile()}
                def read_json(name):
                    return json.load(archive.extractfile("package/" + name))
                package = read_json("package.json")
                self.assertEqual("@socialbu/socialbu-agent", package["name"])
                self.assertEqual(package["version"], read_json("openclaw.plugin.json")["version"])
                self.assertEqual(package["version"], read_json(".codex-plugin/plugin.json")["version"])
                self.assertEqual("codex", package["openclaw"]["bundleFormat"])
                self.assertNotIn("extensions", package["openclaw"])
                server = read_json(".mcp.json")["mcpServers"]["socialbu"]
                self.assertEqual("https://socialbu.com/mcp", server["url"])
                self.assertEqual("oauth", server["auth"])
                self.assertEqual("./.mcp.json", read_json(".codex-plugin/plugin.json")["mcpServers"])
                for source in (ROOT / "skills").rglob("*"):
                    if source.is_file():
                        path = "package/" + source.relative_to(ROOT).as_posix()
                        self.assertIn(path, members)
                        self.assertEqual(source.read_bytes(), archive.extractfile(path).read())
                self.assertEqual(2, len([name for name in members if name.endswith("/SKILL.md")]))
                self.assertFalse(any(name.endswith((".py", ".js", ".ts")) or "/.github/" in name for name in members))
        self.assertEqual(original, (ROOT / ".mcp.json").read_bytes())


if __name__ == "__main__":
    unittest.main()

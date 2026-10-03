#!/usr/bin/env python3
"""Check release guards and exercise the workflow's actual Registry predicates."""

import copy
import json
import re
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
workflow = (root / ".github/workflows/release.yml").read_text(encoding="utf-8")
assert "environment: mcp-registry-publish" in workflow
assert "format('refs/tags/{0}', inputs.tag)" in workflow
assert "ref: refs/tags/${{ env.RELEASE_TAG }}" in workflow
assert 'gh release create "$RELEASE_TAG" "$archive" --verify-tag' in workflow

server = json.loads((root / "server.json").read_text(encoding="utf-8"))
record = {"server": server, "_meta": {"io.modelcontextprotocol.registry/official": {"status": "active"}}}
predicates = re.findall(r"jq -e --slurpfile expected server.json(?: \\\n)?\s*'([^']+)'", workflow)
assert len(predicates) == 2

for predicate in predicates:
    def accepts(value: dict) -> bool:
        result = subprocess.run(
            ["jq", "-e", "--slurpfile", "expected", str(root / "server.json"), predicate],
            input=json.dumps(value), text=True, capture_output=True, check=False,
        )
        assert result.returncode in (0, 1), result.stderr
        return result.returncode == 0

    assert accepts(record)
    wrong_remote = copy.deepcopy(record)
    wrong_remote["server"]["remotes"][0]["url"] = "https://example.com/mcp"
    assert not accepts(wrong_remote)
    assert not accepts({"server": {"version": server["version"]}})
    if "status" in predicate:
        deleted = copy.deepcopy(record)
        deleted["_meta"]["io.modelcontextprotocol.registry/official"]["status"] = "deleted"
        assert not accepts(deleted)

print("Release guards passed.")

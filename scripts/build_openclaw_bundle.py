#!/usr/bin/env python3
"""Build the OpenClaw content bundle from the shared skills and manifests."""

from __future__ import annotations

import argparse
import json
import shutil
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_bundle(output_dir: Path) -> Path:
    plugin = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"socialbu-agent-openclaw-{plugin['version']}.tgz"
    with tempfile.TemporaryDirectory() as temporary:
        package = Path(temporary) / "package"
        package.mkdir()
        for name in (".codex-plugin", "skills", "assets", "docs", "README.md", "LICENSE", "SECURITY.md", "openclaw.plugin.json"):
            source = ROOT / name
            if source.is_dir():
                shutil.copytree(source, package / name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            else:
                shutil.copy2(source, package / name)

        mcp = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))
        # OpenClaw needs explicit OAuth; keep its field out of other clients' config.
        mcp["mcpServers"]["socialbu"]["auth"] = "oauth"
        (package / ".mcp.json").write_text(json.dumps(mcp, indent=2) + "\n", encoding="utf-8")
        metadata = {
            "name": "@socialbu/socialbu-agent",
            "version": plugin["version"],
            "description": plugin["description"],
            "type": "module",
            "license": "MIT",
            "author": plugin["author"],
            "homepage": plugin["homepage"],
            "repository": plugin["repository"],
            "keywords": plugin["keywords"],
            "openclaw": {"bundleFormat": "codex", "hostTargets": ["openclaw"]},
        }
        (package / "package.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        with tarfile.open(archive, "w:gz") as handle:
            handle.add(package, arcname="package")
    return archive


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path)
    print(build_bundle(parser.parse_args().output_dir))

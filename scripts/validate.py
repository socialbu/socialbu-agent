#!/usr/bin/env python3
"""Validate SocialBu agent manifests without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MCP_URL = "https://socialbu.com/mcp"


def load_json(path: str) -> dict:
    with (ROOT / path).open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_files(release_tag: str = "") -> None:
    manifests = {
        path: load_json(path)
        for path in (
            "plugin.json",
            "mcp.json",
            ".mcp.json",
            "server.json",
            "gemini-extension.json",
            ".codex-plugin/plugin.json",
            ".claude-plugin/plugin.json",
            ".claude-plugin/marketplace.json",
            ".grok-plugin/plugin.json",
            ".grok-plugin/marketplace.json",
        )
    }

    version = manifests["plugin.json"]["version"]
    for path in (
        "plugin.json",
        "server.json",
        "gemini-extension.json",
        ".codex-plugin/plugin.json",
        ".claude-plugin/plugin.json",
        ".grok-plugin/plugin.json",
    ):
        assert manifests[path]["version"] == version, f"Version mismatch in {path}"

    assert manifests[".claude-plugin/marketplace.json"]["metadata"]["version"] == version
    if release_tag:
        assert release_tag == f"v{version}", "Release tag must match manifest versions"

    for path in (
        "plugin.json",
        ".codex-plugin/plugin.json",
        ".claude-plugin/plugin.json",
        ".grok-plugin/plugin.json",
    ):
        assert manifests[path]["name"] == "socialbu", f"Plugin name mismatch in {path}"

    for path in (".claude-plugin/marketplace.json", ".grok-plugin/marketplace.json"):
        assert manifests[path]["name"] == "socialbu-agent", f"Marketplace name mismatch in {path}"
        assert manifests[path]["plugins"][0]["name"] == "socialbu"

    assert manifests["gemini-extension.json"]["name"] == "socialbu-agent"
    assert manifests["gemini-extension.json"]["contextFileName"] == "GEMINI.md"
    assert manifests["mcp.json"]["mcpServers"]["socialbu"]["url"] == MCP_URL
    assert manifests[".mcp.json"]["mcpServers"]["socialbu"]["url"] == MCP_URL
    assert manifests[".codex-plugin/plugin.json"]["mcpServers"] == "./.mcp.json"
    assert manifests[".claude-plugin/plugin.json"]["mcpServers"] == "./.mcp.json"
    assert manifests["server.json"]["remotes"] == [
        {"type": "streamable-http", "url": MCP_URL}
    ]
    assert manifests["gemini-extension.json"]["mcpServers"]["socialbu"]["httpUrl"] == MCP_URL
    assert manifests[".grok-plugin/plugin.json"]["mcpServers"]["socialbu"]["url"] == MCP_URL

    plugin = manifests["plugin.json"]
    interface = plugin["extensions"]["com.openai"]["interface"]
    for field in ("displayName", "shortDescription"):
        assert 0 < len(interface[field]) <= 30, f"Invalid OpenAI listing length: {field}"
    for field in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        assert interface[field].startswith("https://"), f"Missing HTTPS listing URL: {field}"
    for claude_field, openai_field in (
        ("documentationUrl", "websiteURL"),
        ("supportUrl", "supportURL"),
        ("privacyPolicyUrl", "privacyPolicyURL"),
        ("termsOfServiceUrl", "termsOfServiceURL"),
    ):
        assert manifests[".claude-plugin/plugin.json"][claude_field] == interface[openai_field]
    for asset in (interface["composerIcon"], interface["logo"]):
        assert (ROOT / asset).is_file(), f"Missing asset: {asset}"

    skill = (ROOT / "skills/socialbu/SKILL.md").read_text(encoding="utf-8")
    assert skill.startswith("---\nname: socialbu\n")
    assert "description:" in skill.split("---", 2)[1]
    assert "TODO" not in skill
    assert (ROOT / "GEMINI.md").is_file()
    assert (ROOT / "docs/publishing.md").is_file()
    assert (ROOT / "LICENSE").read_text(encoding="utf-8").startswith("MIT License\n")


def validate_live_endpoint() -> None:
    request = urllib.request.Request(MCP_URL, headers={"User-Agent": "SocialBu-Agent-Validation/1.0"}, method="GET")
    try:
        urllib.request.urlopen(request, timeout=15)
    except urllib.error.HTTPError as error:
        assert error.code == 401, f"Unexpected MCP status: {error.code}"
        assert 'resource_metadata="https://socialbu.com/.well-known/oauth-protected-resource"' in error.headers.get("WWW-Authenticate", ""), "Missing SocialBu OAuth challenge"
    except urllib.error.URLError as error:
        raise AssertionError(f"Could not reach {MCP_URL}: {error.reason}") from error
    else:
        raise AssertionError(f"{MCP_URL} unexpectedly allowed an unauthenticated GET")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="also check the hosted MCP connection")
    parser.add_argument("--release-tag", default="", help="require manifests to match this v-prefixed tag")
    args = parser.parse_args()

    try:
        validate_files(args.release_tag)
        if args.live:
            validate_live_endpoint()
    except (AssertionError, KeyError, json.JSONDecodeError) as error:
        print(f"validation failed: {error}", file=sys.stderr)
        return 1

    print("SocialBu agent package is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

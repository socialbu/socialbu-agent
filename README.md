<p align="center">
  <img src="assets/logo.svg" alt="SocialBu" width="236">
</p>

# SocialBu for AI agents

The official SocialBu plugin and remote MCP integration. It lets supported AI clients work with the SocialBu accounts, posts, queues, analytics, automations, curated content, media, and social listening data that you authorize.

The hosted MCP server is the source of truth. This repository contains portable agent instructions and client manifests, with no proxy server, duplicated business logic, API keys, or local runtime.

## Connect

Use this remote MCP server in any client that supports Streamable HTTP and OAuth:

```text
https://socialbu.com/mcp
```

Your client opens SocialBu in a browser. Sign in and approve the connection there. Do not paste a SocialBu password or API token into a prompt.

## Install

### Agent skill

Install the reusable SocialBu skill in clients supported by the Agent Skills installer:

```bash
npx skills add socialbu/socialbu-agent
```

The skill improves tool selection and safety. Connect the MCP URL as well if the client does not install bundled MCP servers from `mcp.json`.

### Gemini CLI

```bash
gemini extensions install https://github.com/socialbu/socialbu-agent
```

Restart Gemini CLI after installation, then authorize SocialBu when prompted.

### Claude Code

```text
/plugin marketplace add socialbu/socialbu-agent
/plugin install socialbu@socialbu-agent
```

### Other clients

See [client setup instructions](docs/clients.md) for ChatGPT, Codex, Cursor, GitHub Copilot, Windsurf, Cline, Zed, OpenCode, Grok Build, Qwen Code, and direct MCP configuration.

## What agents can do

- Inspect connected accounts and teams
- Create drafts, schedule posts, update posts, and publish on request
- Work with custom publishing queues and media uploads
- Read account and post analytics
- Inspect and enable or disable automations
- Browse curated content
- Read, archive, restore, and delete saved Listen items
- Run SocialBu AI content tools

SocialBu's inbox is not currently exposed by this MCP server. Available operations depend on the user's plan, permissions, teams, connected networks, and account types.

## Safety model

- Read operations are marked read-only.
- Publishing, deletion, account removal, approvals, automation changes, and other consequential actions are marked accurately in MCP tool annotations.
- OAuth access is granted by the SocialBu user in the browser.
- MCP credentials are bound to `https://socialbu.com/mcp` and are separate from REST API credentials.
- No credentials belong in this repository, prompts, logs, issues, or screenshots.

## Repository contents

| Path | Purpose |
| --- | --- |
| `plugin.json` | Portable Agent Plugins manifest |
| `mcp.json` | Portable remote MCP definition |
| `skills/socialbu/` | Reusable SocialBu operating guidance |
| `.claude-plugin/` | Claude plugin and marketplace metadata |
| `.codex-plugin/` | Codex compatibility manifest |
| `.grok-plugin/` | Grok Build compatibility metadata |
| `gemini-extension.json` | Gemini CLI extension manifest |
| `server.json` | Official MCP Registry metadata |

## Existing SocialBu CLI

The separate [SocialBu CLI](https://github.com/socialbu/socialbu-cli) remains available for terminal scripts and environments that do not support MCP. This plugin does not bundle or duplicate it.

## Support

- [MCP setup page](https://socialbu.com/mcp-server)
- [SocialBu help center](https://help.socialbu.com/)
- [Report a packaging problem](https://github.com/socialbu/socialbu-agent/issues)
- [Security policy](SECURITY.md)

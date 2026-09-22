# Release and directory checklist

This repository is the public release artifact for the SocialBu Agent Plugin. The hosted MCP server remains at `https://socialbu.com/mcp`; publishing this package must not introduce a proxy, copied credentials, or a second implementation of the tools.

## Before the first release

- Add the license selected by SocialBu. Some directories will not accept an unlicensed package.
- Keep `1.0.0` synchronized in `plugin.json`, `server.json`, `gemini-extension.json`, `.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`, and `.grok-plugin/plugin.json`.
- Confirm the privacy policy, terms, support address, repository, homepage, logo, and icon are public and current.
- Confirm OAuth discovery, dynamic client registration, PKCE, and the protected MCP resource are live. Do not add OAuth scopes unless the server starts enforcing them.
- Run the local and vendor validators listed below.
- Tag the exact reviewed commit and create a GitHub release with the same semantic version.

## Validation

```bash
python scripts/validate.py --live
claude plugin validate .
npx -y @google/gemini-cli@latest extensions validate .
npx -y skills@latest add socialbu/socialbu-agent --list
```

CI also validates the portable Agent Plugins manifests and `server.json` against their published JSON schemas. A successful local check does not replace a green GitHub Actions run on the release commit.

## Publication channels

| Channel | How it is published | Repository preparation |
| --- | --- | --- |
| OpenAI universal plugin directory | Submit the remote MCP endpoint through the [plugin submission portal](https://developers.openai.com/plugins/build/plugins). One approved listing is shared by ChatGPT and Codex. | Root `plugin.json`, `mcp.json`, public assets, privacy policy, terms, and a fully featured reviewer demo account with sample data. Do not commit the demo credentials. |
| Official MCP Registry | Authenticate with GitHub, then run `mcp-publisher validate` and `mcp-publisher publish` against `server.json` using the [publisher workflow](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/quickstart.mdx). | `server.json` is already configured for the hosted Streamable HTTP endpoint and the `io.github.socialbu` namespace. |
| Gemini CLI extension gallery | Automatic discovery from the public repository after a tag is created, as described in the [release guide](https://geminicli.com/docs/extensions/releasing/). | Keep the `gemini-cli-extension` GitHub topic and root `gemini-extension.json`. No submission form is required. |
| Cursor Marketplace | Submit the public repository at [cursor.com/marketplace/publish](https://cursor.com/marketplace/publish). | Cursor accepts the root Agent Plugins manifest. Include the committed logo and README. |
| Claude plugin directory | Submit the public repository through the plugin directory form linked from [Anthropic's marketplace](https://github.com/anthropics/claude-plugins-official). | `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.mcp.json`, the skill, and the entire shipped repository are reviewed. |
| xAI Grok Build marketplace | Open a PR against [xai-org/plugin-marketplace](https://github.com/xai-org/plugin-marketplace). | Use a remote source pinned to the full lowercase SHA of the released commit. The plugin must state its license. |
| GitHub Copilot | The public repository is directly installable. For default-marketplace discovery, follow the external-plugin contribution process in [github/awesome-copilot](https://github.com/github/awesome-copilot). | Copilot supports the portable root manifests and also recognizes `.claude-plugin/marketplace.json`. Pin the public release commit when the directory asks for an immutable ref. |
| Agent Skills ecosystem | Public GitHub discovery through `npx skills add socialbu/socialbu-agent`. | Keep `skills/socialbu/SKILL.md` valid and free of product behavior that the live MCP server does not expose. |

Qwen Code can install the repository directly because it supports Agent Plugins v1. Other clients documented in [clients.md](clients.md) connect to the same remote MCP endpoint and do not currently require a separate package submission.

## Submission records

For every manual submission, record the directory, submitted version and commit SHA, date, account used, review state, and listing URL in the release notes or the team's private release tracker. Store reviewer credentials only in the submission portal or the team's password manager.

# Releasing and directory publishing

## Automated release flow

Pushing a `v*` tag runs `.github/workflows/release.yml`. The workflow validates the exact tagged commit, checks the live MCP endpoint, creates the GitHub Release with a plugin ZIP, publishes `server.json` to the Official MCP Registry with GitHub OIDC, verifies the published version, and leaves a submission summary in the workflow run.

No repository secret is required for the MCP Registry. The workflow pins and verifies the `mcp-publisher` binary before using it.

Gemini CLI discovers tagged public repositories with the `gemini-cli-extension` topic automatically. The repository already has the topic and root `gemini-extension.json`, so no separate Gemini submission runs in CI.

Before creating a tag, update the version in every manifest and run:

```bash
python scripts/validate.py --live --release-tag v1.1.0
```

Then push the reviewed tag:

```bash
git tag v1.1.0
git push origin v1.1.0
```

For an existing tag, use **Actions → Release agent package → Run workflow**. Leave Registry publishing off for a validation-only run.

## Registry identity

`io.github.socialbu/socialbu` version `1.0.0` was published on October 3, 2026. The older `io.github.usamaejaz/socialbu-mcp` listing is hidden from discovery with a migration message; its historical metadata remains available. Both records point to `https://socialbu.com/mcp`.

The migration is complete. Future `v*` tags publish new versions under the SocialBu organization identity. Rerunning publication for `v1.0.0` skips the existing Registry version.

## Reviewed directories

These channels require a form, external pull request, account verification, attestations, or human review and therefore are not submitted automatically from this repository:

| Directory | Submission path |
| --- | --- |
| OpenAI Plugins Directory | Upload the release ZIP using **With MCP** in the [OpenAI plugin submission portal](https://platform.openai.com/plugins), then complete domain verification and review details. Hosted MCP servers are scanned daily after publication. |
| Cursor Marketplace | Submit the public repository at [cursor.com/marketplace/publish](https://cursor.com/marketplace/publish). |
| Claude directory | Submit the MCP connector and plugin bundle from the same organization in [Anthropic's developer portal](https://claude.ai/directory/manage). After approval, plugin updates are picked up from the tracked repository branch. |
| xAI Grok Build marketplace | Open a SHA-pinned contribution against [xai-org/plugin-marketplace](https://github.com/xai-org/plugin-marketplace). |
| GitHub Copilot | Use the external-plugin submission flow in [github/awesome-copilot](https://github.com/github/awesome-copilot). |

Keep reviewer credentials in the submission portals, never in the repository or release ZIP.

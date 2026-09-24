# Releasing and directory publishing

## Automated release flow

Pushing a `v*` tag runs `.github/workflows/release.yml`. The workflow validates the exact tagged commit, checks the live MCP endpoint, creates the GitHub Release, publishes `server.json` to the Official MCP Registry with GitHub OIDC, verifies the published version, and leaves a submission summary in the workflow run.

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

## One-time Registry migration

The Registry currently has the older `io.github.usamaejaz/socialbu-mcp` identity for the same remote endpoint. Delete all versions of that entry before the first automated publication of `io.github.socialbu/socialbu`; otherwise remote URL uniqueness can reject the new identity.

```bash
mcp-publisher login github
mcp-publisher status --status deleted --all-versions --yes --message "Moved to io.github.socialbu/socialbu" io.github.usamaejaz/socialbu-mcp
```

After the old listing is hidden, manually run the release workflow for `v1.0.0` with Registry publishing enabled. Future `v*` tags publish automatically.

## Reviewed directories

These channels require a form, external pull request, account verification, attestations, or human review and therefore are not submitted automatically from this repository:

| Directory | Submission path |
| --- | --- |
| OpenAI Plugins Directory | Submit the remote MCP endpoint through the [OpenAI plugin submission portal](https://developers.openai.com/plugins/deploy/submission). |
| Cursor Marketplace | Submit the public repository at [cursor.com/marketplace/publish](https://cursor.com/marketplace/publish). |
| Claude plugin directory | Use Anthropic's [plugin directory submission form](https://github.com/anthropics/claude-plugins-official). |
| xAI Grok Build marketplace | Open a SHA-pinned contribution against [xai-org/plugin-marketplace](https://github.com/xai-org/plugin-marketplace). |
| GitHub Copilot | Use the external-plugin submission flow in [github/awesome-copilot](https://github.com/github/awesome-copilot). |

Do not commit reviewer credentials. Record submitted versions, commit SHAs, review states, and listing URLs in the private release tracker.

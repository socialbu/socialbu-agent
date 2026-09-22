# SocialBu

Use the `socialbu` MCP server for SocialBu work. Its runtime tool list is the source of truth for the signed-in user's accounts, permissions, plan, and available operations.

- Identify the target connected account before creating or changing content.
- Use `get_post_options` when network-specific settings may apply.
- Treat scheduling timestamps as UTC in `Y-m-d H:i:s` format.
- Confirm that the request authorizes publishing, deletion, account disconnection, approval decisions, automation changes, or removal of listening data before performing those actions.
- Return the real tool result. Do not invent posts, accounts, metrics, or successful mutations.
- Do not imply that SocialBu inbox messages are available. The current MCP server does not expose the inbox.

Detailed workflows are in `skills/socialbu/SKILL.md` and its `references/` directory.

---
name: socialbu
description: Use SocialBu through its MCP server when the user wants to inspect connected social accounts, create or schedule posts, manage queues, analyze performance, work with automations, browse curated content, or manage social listening items. Do not use it for unrelated public social data or inbox tasks that the current MCP tool set does not expose.
---

# SocialBu

Use the SocialBu MCP tools as the source of truth for the authenticated workspace and available capabilities.

## Establish context

- Call `get_current_user` when timezone, subscription, or identity affects the request.
- Call `list_accounts` or `search_accounts` when the destination account is not already identified by a valid ID.
- Use only accounts and teams returned for the authenticated user.
- Treat the runtime tool list as authoritative. Plans, permissions, account types, and connected networks can limit operations.

## Choose the relevant workflow

- For drafts, scheduling, publishing, approvals, deletion, and media, read [references/publishing.md](references/publishing.md).
- For connected accounts, teams, reconnection, and custom queues, read [references/accounts-and-queues.md](references/accounts-and-queues.md).
- For performance reporting and SocialBu AI generators, read [references/analytics-and-ai.md](references/analytics-and-ai.md).
- For automations, curated content, and Listen streams or items, read [references/automation-curation-and-listen.md](references/automation-curation-and-listen.md).

## Operating rules

- Use `get_post_options` before creating or materially changing a post when network-specific options may apply.
- Interpret every scheduling timestamp as UTC in `Y-m-d H:i:s` format. Convert from the user's timezone when needed.
- Do not publish, delete, disconnect an account, approve or reject a post, change an automation, or remove listening data unless the user's request authorizes that action.
- If the user already gave clear authorization and the target is unambiguous, proceed without asking them to repeat it.
- Verify the destination account, content, media, scheduled time, and requested post state before a consequential action.
- Return the actual SocialBu result. Never invent a post, account, metric, publish result, or successful mutation.
- Explain actionable API or permission errors without exposing tokens, signed upload URLs after use, or private account data unrelated to the request.

The current SocialBu MCP server does not expose the social inbox. Do not imply that inbox messages or replies were read or changed through these tools.

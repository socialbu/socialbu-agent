# Publishing

## Read posts

- `list_posts` reads scheduled, draft, published, or awaiting-approval posts and supports account filtering and pagination.
- `get_post_options` returns the options supported by the selected account types. Use it before supplying network-specific options.

## Create a post

1. Resolve one destination account ID with `list_accounts` or `search_accounts`.
2. Call `get_post_options` for that account when options or format behavior matters.
3. Prepare content, media, options, post state, and a UTC schedule time when required.
4. Call `create_post` with one of these states:
   - `draft` when the user wants a saved draft.
   - `scheduled` when the user explicitly wants SocialBu to schedule it.
   - `awaiting_approval` when the user explicitly wants the team approval workflow.
5. Return the created post ID, state, account, and schedule from SocialBu's response.

Do not silently turn a request to draft content into a scheduled or published post.

## Media

- `create_post` and `add_post_to_queue` can accept accessible HTTP(S) media URLs or supported base64 data URLs.
- For a file held by the agent, call `create_media_upload`, upload the raw bytes to the returned signed URL using the stated content type, then pass the returned temporary media URL to the post tool.
- Treat signed upload URLs as short-lived secrets. Do not repeat them after the upload completes.

## Change post state

- `update_post` changes a scheduled or draft post. Supplying the same values is intended to have no additional effect.
- `publish_post_now` publishes immediately and can create an external social-network side effect. Use it only when the user explicitly requests immediate publication.
- `approve_post` and `reject_post` change an awaiting-approval post and require team approval permission.
- `delete_post` removes a post. Confirm the ID belongs to the intended post before deletion.

If SocialBu returns a provider, permission, plan, validation, or processing error, report it directly and do not claim the post was published.

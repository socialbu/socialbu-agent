# Analytics and AI

## Analytics

- `get_stats_overview` summarizes pending posts, failures, unread feeds, and inactive accounts for the requested date range.
- `get_post_metrics` returns post engagement metrics grouped by date.
- `get_top_posts` returns top-performing posts for the requested period.
- `get_engagement_trend` returns engagement over time.
- `get_account_metrics` returns available account-level measurements such as followers, reach, and impressions.

Resolve account IDs before filtering. Preserve the requested date range and report the units, period, account scope, and missing data returned by SocialBu. Networks expose different metrics, so do not treat an absent metric as zero unless the response says so.

## SocialBu AI tools

Call `list_ai_tools` before `use_ai_tool` when the exact tool slug or required fields are not known. Build the input object from the listed field IDs, then pass it as the JSON-encoded `inputs` value expected by `use_ai_tool`.

Generated content is a draft result. Do not schedule or publish it unless the user separately requests that action.

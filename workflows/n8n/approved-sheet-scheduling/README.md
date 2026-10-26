# Schedule approved Google Sheets posts with SocialBu

Keep your approved captions, media URLs, and posting times in Google Sheets. This n8n workflow sends one approved row to SocialBu every five minutes and records the post ID and scheduling result in the same row.

It uses the SocialBu REST API, Google Sheets, and standard n8n nodes. No AI service or community node is required.

[Download the workflow JSON](https://raw.githubusercontent.com/socialbu/socialbu-agent/main/workflows/n8n/approved-sheet-scheduling/workflow.json) · [Sample calendar](calendar.csv) · [Demand research](demand.md)

## Before you start

- An n8n instance with access to Google Sheets.
- A [SocialBu account with API access](https://socialbu.com/?utm_source=n8n&utm_medium=workflow&utm_campaign=approved_sheet_scheduling), an API token, and the social accounts you want to schedule to.
- Approved post content. Media must have a public HTTPS URL that downloads the file directly. A Google Drive sharing page is not a media file.

The selected network's media, format, account, and plan requirements still apply. Scheduling into a team respects SocialBu's approval requirements.

## Setup

1. Import [workflow.json](workflow.json) into n8n. It is inactive and starts in preview mode.
2. Import [calendar.csv](calendar.csv) into a Google Sheets tab named **Posts**. Keep every header, including the empty result columns. Format the input columns as **Plain text**, especially `publish_at` and IDs.
3. In **Settings**, replace `spreadsheet_id` with the ID between `/d/` and `/edit` in your spreadsheet URL. Keep `preview_only` as the boolean `true`.
4. Select your Google Sheets OAuth2 credential in **Read calendar**, **Mark processing**, and **Write result**. The read step uses an HTTP Request node with the predefined Google Sheets credential so it can check the header row, including empty columns. Your Google account needs edit access to that sheet.
5. Create an n8n **Header Auth** credential with name `Authorization` and value `Bearer YOUR_SOCIALBU_API_TOKEN`. Select it in **Connected accounts**, **Upload media**, and **Create scheduled post**. Keep tokens in credentials, never in the sheet or exported workflow.
6. Execute **Connected accounts** to find the SocialBu `id` for the desired account. Use that ID as `account_id`; it is not the social network's profile ID. For a shared account, also copy its `team_id`.
7. Replace the example row with your content and a future posting time. Give it a stable `row_id`, leave the result columns empty, and change `status` to `approved`.
8. Execute the workflow. Inspect **Preview result**: check the account name, content, media URL, and `request.publish_at` in UTC. Valid input appears as `ready`; invalid input appears as `needs_fix`. Preview performs reads but makes no sheet changes, media uploads, or posts.
9. Set `preview_only` to the boolean `false` and manually execute one row while the schedule is inactive. Confirm the returned ID and posting time in SocialBu and the written result in Google Sheets.
10. Publish/activate the workflow in n8n. It checks every five minutes and processes the first eligible row in sheet order.

Only use one active copy for a sheet. Pause it before manual runs. Do not edit, reorder, or remove a row while it is being processed. Make changes to approved rows while the workflow is paused, then preview again.

## Calendar columns

| Column | What to enter |
| --- | --- |
| `row_id` | Unique, permanent text ID, such as `launch-001`. No surrounding spaces. Never reuse an old ID. |
| `account_id` | One numeric SocialBu account ID. Use separate rows for separate accounts. |
| `team_id` | Shared account's SocialBu team ID; leave empty for a personal account. |
| `content` | The approved caption, including any links. Used as supplied. |
| `media_url` | Optional public HTTPS image/video file URL. One asset per row. Required when the destination account requires media. |
| `publish_at` | ISO date/time with seconds and explicit timezone, such as `2027-01-20T09:00:00+05:00` or `2027-01-20T04:00:00Z`. |
| `options_json` | Optional JSON object for network-specific SocialBu API options. Leave empty for defaults. |
| `status` | Set to `approved` when the row is ready. Other statuses are skipped. |
| `socialbu_post_id` | Written by the workflow. A row with an existing ID is always skipped. |
| `result` | Written by the workflow with the result or next step. |
| `attempted_at` | Written by the workflow in UTC when it checks the selected row. |

The posting time must be at least 15 minutes ahead **when the row is processed**. Allow additional lead time for rows ahead of it: one row is processed per five-minute run. SocialBu receives the converted UTC time and handles scheduled publishing.

## Results and recovery

| Status | Meaning and next step |
| --- | --- |
| `needs_fix` | Input failed validation. Correct it, then set `approved` again. |
| `processing` | The sheet was marked before uploading media or requesting a post. If it stays here after the run ends, inspect the execution and SocialBu before any retry. |
| `media_error` | Media upload failed and the workflow did not request a post. Fix the file URL or upload problem, then approve again. |
| `scheduled` | SocialBu accepted the post for the requested time. Check its final publishing result in SocialBu. |
| `awaiting_approval` | SocialBu created the post, but team approval is still required there. |
| `needs_review` | The create request failed, timed out, or returned an unexpected result. The post may already exist. Check before retrying. |

For `processing` or `needs_review`, search SocialBu by account, content, and posting time. Check the n8n execution's **Create scheduled post** output for a returned post ID. If a post exists, record its ID and correct status in the sheet. If you have confirmed no post exists, correct the problem and set the row to `approved` for a new run.

Do not use n8n's retry-from-failed-node action for a failed scheduling execution. A timeout or failed sheet update can happen after a post was saved. Automatic POST retries and execution-progress resumption are disabled.

Google Sheets does not provide an atomic claim for a row. The `processing` marker helps recovery but does not guarantee exactly-once submission. Overlapping workflow copies or manual runs can create duplicates. Keep a single writer; on a shared n8n instance, configure production concurrency if overlap is possible. The workflow's 240-second timeout is shorter than its five-minute interval, but is not a distributed lock.

## Verification

The focused regression checks run directly against the Code nodes in the exported JSON:

```sh
node --test workflows/n8n/approved-sheet-scheduling/workflow.test.mjs
```

They cover approval selection, saved IDs, duplicate IDs, timezone conversion, invalid dates, account/team validation, media failures, and ambiguous create outcomes.

The export was also imported and executed in n8n **2.44.7** with fake credentials and simulated Google/SocialBu HTTP responses, with external requests blocked. Ten scenarios were checked: preview, text scheduling, media scheduling, media rejection, a create error, a lost connection, team approval, an invalid date, an existing post ID, and a sheet write failure after a successful create. The last case intentionally failed the execution, left the row marked `processing`, and retained the created post ID in the execution output for recovery.

Live Google OAuth, a real sheet, and a real SocialBu post still need the one-row setup check above. No production social account is used by the automated tests. This template has not yet been submitted to the n8n template directory.

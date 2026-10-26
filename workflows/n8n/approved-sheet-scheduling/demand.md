# Why this workflow

Research date: 26 October 2026.

Decision: start with an existing Google Sheets content calendar containing approved posts and explicit publishing times. Use SocialBu for scheduling and write the result back to the calendar. Content generation is outside this first workflow.

## Evidence

These are public first-person requests from n8n users, not interviews with SocialBu customers. Dates and statements reflect the source posts; technical explanations in replies were not independently verified.

| Source | Reported job or problem | Implication |
| --- | --- | --- |
| [Podcast publishing workflow, 29 April 2026](https://www.reddit.com/r/n8n/comments/1syzky6/automated_podcast_publishing_workflow_with_n8n/) | A user already uploads a finished video and fills a Google Sheets row with title, file link, and date/time. They want a different publishing time per video and have trouble getting scheduled publishing working. | Accept existing content and a precise per-row timestamp. Validate timezone input and show the UTC result before scheduling. |
| [Planned posts from Google Sheets, 10 October 2025](https://www.reddit.com/r/n8n/comments/1o38mr4/) | A user reads planned posts from Sheets, struggles with Google Drive media links, and reports a successful-looking execution without the expected post. | Upload media before creating a post; reject sharing-page URLs. Store the post ID and distinguish accepted scheduling from completed publishing. This older source receives less weight. |
| [Business posting timeline, 17 March 2026](https://www.reddit.com/r/n8n/comments/1rwl9ns/permissions_on_n8n/) | A business owner wants posts scheduled on a timeline connected to Notion and is blocked by local permissions. | Evidence for connecting an existing calendar to publishing. It does not establish a preference for Sheets; this workflow does not implement Notion or resolve NAS permissions. |
| [LinkedIn credential problem, 5 March 2026](https://community.n8n.io/t/n8n-linkedln-connection-issue/273460) | A user reports repeatedly recreating credentials while following the documentation. | Use one SocialBu API credential after accounts are connected in SocialBu. Network connection requirements still exist. |
| [Founder wants regular posting, 4 November 2025](https://www.reddit.com/r/n8n/comments/1oo0ngk/is_there_an_automation_that_helps_me_be_regular/) | A founder wants to post more regularly and turn weekly questions into posts. | Adjacent consistency demand. This does not directly validate the chosen Sheet workflow or its approval step. |

The podcast user's cross-post was counted once. Vendor promotions, template sellers' claims, and generic “I built this” posts were excluded as independent demand evidence. Existing templates do not establish installs, willingness to pay, or conversion.

## Confidence and tradeoffs

There is enough evidence to justify one focused experiment. There is not enough to estimate market size or promise signups. Two sources directly describe a Sheets publishing job; the other sources are supporting context.

The approved status is a deliberate user-control choice, not a claim that approval was the most frequent request. Users supply finished content. The workflow does not generate filler posts, silently pick a timezone, or report published merely because a create request succeeded.

One destination account and one optional asset per row keep failures attributable to a single post. One row per run avoids partial batches and makes the workflow easier to inspect. It is suited to small calendars, not high-volume dispatch.

## How to judge the experiment

After live validation and directory approval, use the template's tagged SocialBu link to distinguish visits in existing analytics. Do not report an install or signup unless the corresponding system records it.

The useful adoption milestone is a new user importing the workflow and scheduling a first post successfully. Follow conversion from template visits to signup, API setup, and that first scheduled post where existing analytics can connect those events. Record setup failures before building more variants.

If users import but cannot get through credentials, sheet setup, or media handling, improve those steps before adding more templates.

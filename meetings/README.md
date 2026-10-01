# Meetings

Weekly session notes for the FSB Design Group 2 squad, pulled directly from Zoom (AI Companion summary + verbatim transcript) via the Zoom MCP connector — no manual copy-paste, no shared link required.

Use `/log-meeting` to add a new one. See `.claude/log-meeting.skill` for the full process.

## Structure

- One dated HTML page per session: `YYYY-MM-DD-topic-slug.html`
- Notes (quick recap, next steps, topic summary) are the main content
- The full timestamped transcript is a collapsed "Full transcript" accordion — click to expand, not the first thing you see
- A row-list section on the root `index.html` (`#meetingGrid`), styled after the Research section pattern from the sibling Chicago Labs explorations repo

## Conventions (why it looks the way it does)

- **Notes before transcript** — the AI summary is what you read; the transcript is for verification/quoting, not the default view. That's why it's collapsed.
- **Next steps grouped by owner** — mirrors how Zoom's own AI Companion structures them, and makes "what do I owe" scannable per person.
- **Row label is "Session"**, not a topic tag — there's only one recurring meeting series right now. If this repo starts logging more than one recurring meeting, revisit whether rows need a tag chip (like the Research rows' `G2 Activate` / `Agent Marketplace` chips) to distinguish series.
- **Date format is `Mon D, YYYY`** (e.g. "Oct 1, 2026") — matches the epic cards' date format elsewhere on the page, not zero-padded.

## Generating a new entry

`scripts/build_meeting_page.py` is the **single source of truth for styling and structure** — it's what actually renders the page and the index.html row. If the look needs to change (row layout, transcript treatment, header, whatever), change the script, not a hand-edited page — that's what keeps every future entry consistent with the latest decision instead of drifting one page at a time. After changing it, add a line below describing what changed and why, so the reasoning survives even if someone's just reading this file.

### Changelog
- **2026-10-01** — Initial version. Notes-first layout, collapsed transcript accordion, owner-grouped next steps, row-list pattern borrowed from Chicago Labs' Research section.
- **2026-10-01** — Added an optional "Relevant links" section (e.g. a FigJam board), placed between Summary and the transcript accordion — rendered only when at least one `--link` is passed, so pages without links don't show an empty section. Also fixed the Summary parser pulling in Zoom's trailing `**Attendees:**` footer line as part of the last topic's paragraph.

#!/usr/bin/env python3
"""
Generate a dated meetings/*.html page from a Zoom `get_meeting_assets` JSON dump.

This script is the single source of truth for how meeting pages (and the
index.html row that links to them) are styled and structured. If you want to
change the look of meeting pages going forward — the row layout, the
transcript treatment, the header, whatever — change it HERE, not by hand-
editing one generated page. That keeps every future run consistent with the
last intentional style decision instead of drifting.

Usage:
    python3 scripts/build_meeting_page.py \\
        --assets-json /path/to/saved-get_meeting_assets-output.json \\
        --attendees "Sam Childs, Joana Balagué Casadó, Martin Leturia, Neil" \\
        [--hook "short dash-phrase for the index row"] \\
        [--link "FigJam board|https://figma.com/board/..."] \\
        [--out meetings/2026-10-08-fsb-design-group-2-weekly.html]

The assets JSON is whatever `get_meeting_assets(meetingId=<uuid>)` returned
(the MCP tool saves it to a local file automatically when the result is too
large to inline — pass that saved file's path here, don't try to paste the
JSON inline). Find the meeting UUID first via the Zoom connector's `search`
tool against the `zoom_meeting` datasource, filtered by topic.

Prints the ready-to-paste <a> row block for index.html's Meetings section,
and a few other values the calling agent needs to finish wiring it up
(filename, suggested hook text, section counts to bump).
"""
import argparse
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MEETINGS_DIR = REPO_ROOT / "meetings"


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def slugify(text: str) -> str:
    text = re.sub(r"[()]", "", text.lower())
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text


def fmt_transcript_time(t: str) -> str:
    parts = t.split(".")[0].split(":")
    h, m, s = int(parts[0]), int(parts[1]), int(parts[2])
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def parse_summary_markdown(md: str):
    """Split the Zoom AI Companion summary into (quick_recap, next_steps, summary_items)."""
    lines = md.split("\n")
    sections = {"Quick recap": [], "Next steps": [], "Summary": []}
    current_h2 = None
    for line in lines:
        m2 = re.match(r"^## (.+)", line)
        if m2:
            current_h2 = m2.group(1).strip()
            continue
        if current_h2 in sections:
            sections[current_h2].append(line)

    quick_recap = "\n".join(sections["Quick recap"]).strip()

    next_steps, owner, bullets = [], None, []
    for line in sections["Next steps"]:
        m3 = re.match(r"^### (.+)", line)
        if m3:
            if owner is not None:
                next_steps.append((owner, bullets))
            owner, bullets = m3.group(1).strip(), []
            continue
        mb = re.match(r"^- \[(.+?)\]\((.+?)\)", line)
        if mb:
            bullets.append((mb.group(1).strip(), mb.group(2).strip()))
        elif line.strip().startswith("- "):
            bullets.append((line.strip()[2:].strip(), None))
    if owner is not None:
        next_steps.append((owner, bullets))

    summary_items, heading, para = [], None, []
    for line in sections["Summary"]:
        m3 = re.match(r"^### (.+)", line)
        if m3:
            if heading is not None:
                summary_items.append((heading, " ".join(para).strip()))
            heading, para = m3.group(1).strip(), []
            continue
        if line.strip() == "---":
            # Zoom appends a trailing "---" + "**Attendees:** ..." footer after the
            # last topic; stop collecting here rather than folding it into that
            # topic's paragraph. Attendees are already passed in via --attendees.
            break
        if line.strip():
            para.append(line.strip())
    if heading is not None:
        summary_items.append((heading, " ".join(para).strip()))

    return quick_recap, next_steps, summary_items


def render_next_steps(next_steps) -> str:
    blocks = []
    for owner, bullets in next_steps:
        items = []
        for text, url in bullets:
            if url:
                items.append(
                    f'            <li class="elv-text-sm elv-text-subtle elv-mb-1">{esc(text)} '
                    f'<a href="{esc(url)}" target="_blank" rel="noopener" class="elv-text-xs" '
                    f'style="color:var(--text-primary, #4c3fb4);">view task →</a></li>'
                )
            else:
                items.append(f'            <li class="elv-text-sm elv-text-subtle elv-mb-1">{esc(text)}</li>')
        blocks.append(
            f'        <div style="margin-bottom:20px;">\n'
            f'          <div class="elv-text-sm elv-font-bold elv-text-default elv-mb-2">{esc(owner)}</div>\n'
            f'          <ul style="margin:0; padding-left:18px;">\n' + "\n".join(items) + "\n          </ul>\n        </div>"
        )
    return "\n".join(blocks)


def render_summary(summary_items) -> str:
    return "\n".join(
        f'        <div style="margin-bottom:24px;">\n'
        f'          <div class="elv-text-base elv-font-bold elv-text-default elv-mb-2">{esc(heading)}</div>\n'
        f'          <p class="elv-text-sm elv-text-subtle elv-leading-relaxed" style="margin:0;">{esc(para)}</p>\n'
        f'        </div>'
        for heading, para in summary_items
    )


def render_links(links) -> str:
    """links is a list of (label, url) tuples. Returns the full <section>, or '' if there are none."""
    if not links:
        return ""
    rows = "\n".join(
        f'        <a class="link-row" href="{esc(url)}" target="_blank" rel="noopener">\n'
        f'          <svg class="link-row__icon" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M8.5 11.5L15 5M15 5H10M15 5V10M15 9.5V14.5C15 14.9 14.85 15.25 14.56 15.56C14.25 15.85 13.9 16 13.5 16H5.5C5.08 16 4.73 15.85 4.44 15.56C4.15 15.27 4 14.92 4 14.5V6.5C4 6.08 4.15 5.73 4.44 5.44C4.73 5.15 5.08 5 5.5 5H10.5" stroke="currentColor" stroke-width="1.3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>\n'
        f'          <span class="link-row__label">{esc(label)}</span>\n'
        f'        </a>'
        for label, url in links
    )
    return (
        "\n    <section>\n"
        '      <h2 class="elv-text-2xl elv-font-bold elv-text-default" style="margin-bottom:12px;">Relevant links</h2>\n'
        f"{rows}\n"
        "    </section>\n"
    )


def render_transcript(items) -> str:
    rows = []
    for it in items:
        text = it.get("text", "")
        start = fmt_transcript_time(it.get("start", "0:00:00.000"))
        speaker, utterance = (text.split(": ", 1) + [""])[:2] if ": " in text else ("", text)
        rows.append(
            f'              <div class="transcript-line">\n'
            f'                <span class="transcript-time">{esc(start)}</span>\n'
            f'                <span class="transcript-speaker">{esc(speaker.strip())}</span>\n'
            f'                <span class="transcript-text">{esc(utterance.strip())}</span>\n'
            f'              </div>'
        )
    return "\n".join(rows)


PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title_tag}</title>

  <link rel="stylesheet" href="../shared/elevate-prototyping-kit/tokens/elevate.css">
  <link rel="stylesheet" href="../shared/elevate-prototyping-kit/components/elevate.css">
  <link rel="stylesheet" href="../shared/elevate-prototyping-kit/utilities.css">
  <link rel="stylesheet" href="../shared/elevate-prototyping-kit/icons/icons.css">

  <style>
    body {{ margin: 0; background: var(--bg-neutral-5); }}

    .elv-accordion__header {{
      display: flex; align-items: center; justify-content: space-between; gap: 12px;
      width: 100%; padding: 14px 0; border: none; background: none; cursor: pointer;
      font-size: 14px; font-weight: 600; color: var(--text-default); text-align: left;
    }}
    .elv-accordion__content[aria-hidden="true"] {{ display: none; }}
    .elv-accordion__content[aria-hidden="false"] {{ display: block; }}
    .elv-accordion__body {{ padding: 0 0 16px; color: var(--text-subtle); }}
    .elv-accordion__icon {{ width: 20px; height: 20px; flex-shrink: 0; transition: transform 150ms ease; }}
    .elv-accordion__header[aria-expanded="true"] .elv-accordion__icon {{ transform: rotate(180deg); }}

    .transcript-scroll {{
      max-height: 520px; overflow-y: auto; background: var(--bg-neutral-0);
      border: 1px solid var(--border-light); border-radius: var(--radius-md); padding: 16px 18px;
    }}
    .transcript-line {{ display: flex; gap: 10px; padding: 5px 0; font-size: 13px; line-height: 1.5; }}
    .transcript-time {{
      flex: 0 0 48px; color: var(--text-nonessential, #9b9aa1);
      font-variant-numeric: tabular-nums; font-size: 12px; padding-top: 1px;
    }}
    .transcript-speaker {{ flex: 0 0 170px; font-weight: 600; color: var(--text-default); }}
    .transcript-text {{ flex: 1 1 auto; color: var(--text-subtle); }}
    @media (max-width: 640px) {{ .transcript-speaker {{ flex: 0 0 110px; }} }}

    .link-row {{
      display: flex; align-items: center; gap: 10px; padding: 10px 0;
      border-bottom: 1px solid var(--border-light); text-decoration: none;
    }}
    .link-row:last-child {{ border-bottom: none; }}
    .link-row__icon {{ flex: 0 0 16px; color: var(--text-nonessential, #9b9aa1); }}
    .link-row__label {{ font-size: 14px; font-weight: 600; color: var(--text-primary, #4c3fb4); }}
  </style>
</head>
<body>

<div elv class="elv-bg-neutral-5 elv-min-h-screen">

  <header class="elv-bg-neutral-0 elv-border-b elv-border-light" style="border-bottom-width: 0.5px;">
    <div class="elv-max-w-7xl elv-w-full md:elv-w-5/6 elv-mx-auto elv-pt-12 elv-pb-8 elv-px-3">
      <nav aria-label="Breadcrumb" class="elv-mb-3">
        <ol class="elv-breadcrumbs" role="list" style="display:inline-flex; align-items:center; gap:2px;">
          <li style="display:flex; align-items:center; gap:2px;">
            <a href="../index.html" style="color:#4c4b53; text-decoration:none; font-size:12px;">FSB Design Group 2</a>
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" style="fill:#6f6d78;"><path d="M10.875 10L6.9375 6.0625L8 5L13 10L8 15L6.9375 13.9375L10.875 10Z"/></svg>
          </li>
          <li><span style="color:#84838a; font-size:12px;" aria-current="page">Meetings</span></li>
        </ol>
      </nav>
      <div class="elv-inline-flex elv-items-center elv-gap-2 elv-px-3 elv-py-1 elv-rounded-full elv-mb-3" style="background: #eef2ff;">
        <span class="elv-text-xs elv-font-bold elv-uppercase elv-tracking-wide" style="color: #4F46E5;">Weekly Sync</span>
      </div>
      <h1 class="elv-text-4xl elv-font-extrabold elv-text-default elv-mb-3 elv-leading-tight">{title}</h1>
      <p class="elv-text-base elv-text-subtle elv-max-w-2xl elv-leading-relaxed">{subtitle}</p>
      <p class="elv-text-xs elv-text-nonessential elv-mt-3">
        <a href="{source_url}" target="_blank" rel="noopener" class="elv-text-nonessential hover:elv-text-primary">Source: Zoom Docs (AI Companion) →</a>
      </p>
    </div>
  </header>

  <div class="elv-max-w-7xl elv-w-full md:elv-w-5/6 elv-mx-auto elv-py-12 elv-px-3" style="display:flex; flex-direction:column; gap:64px; max-width: 820px;">

    <section>
      <h2 class="elv-text-2xl elv-font-bold elv-text-default" style="margin-bottom:12px;">Quick recap</h2>
      <p class="elv-text-sm elv-text-subtle elv-leading-relaxed" style="margin:0;">{quick_recap}</p>
    </section>

    <section>
      <h2 class="elv-text-2xl elv-font-bold elv-text-default" style="margin-bottom:20px;">Next steps</h2>
{next_steps_html}
    </section>

    <section>
      <h2 class="elv-text-2xl elv-font-bold elv-text-default" style="margin-bottom:20px;">Summary</h2>
{summary_html}
    </section>
{links_section}
    <section>
      <div class="elv-accordion" data-accordion>
        <div class="elv-accordion__item">
          <button class="elv-accordion__header" aria-expanded="false" aria-controls="t-transcript">
            <span>Full transcript ({transcript_count} lines)</span>
            <svg class="elv-accordion__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/></svg>
          </button>
          <div class="elv-accordion__content" id="t-transcript" aria-hidden="true" role="region">
            <div class="elv-accordion__body">
              <div class="transcript-scroll">
{transcript_html}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <footer class="elv-mt-4 elv-pt-6 elv-text-xs elv-text-nonessential elv-border-t elv-border-light" style="border-top-width: 0.5px;">
      <a href="../index.html" class="elv-text-nonessential hover:elv-text-primary">← Back to FSB Design Group 2</a>
    </footer>

  </div>

</div>

<script>
(function() {{
  document.querySelectorAll('[data-accordion]').forEach(accordion => {{
    accordion.querySelectorAll('.elv-accordion__header').forEach(header => {{
      header.addEventListener('click', () => {{
        const isExpanded = header.getAttribute('aria-expanded') === 'true';
        const content = document.getElementById(header.getAttribute('aria-controls'));
        header.setAttribute('aria-expanded', !isExpanded);
        content.setAttribute('aria-hidden', isExpanded);
      }});
    }});
  }});
}})();
</script>

</body>
</html>
'''

ROW_TEMPLATE = '''      <!-- {title_comment} -->
      <a href="./meetings/{filename}"
         class="meeting-row elv-block elv-bg-neutral-0 elv-border elv-border-light elv-rounded-md elv-px-5 elv-py-4 elv-no-underline elv-transition-all hover:elv-shadow-2 hover:elv-border-medium"
         data-date="{date_iso}"
         data-name="{title_attr}"
         style="text-decoration: none;">
        <div class="elv-flex elv-items-center elv-gap-4">
          <span class="elv-text-sm elv-font-semibold elv-text-subtle elv-whitespace-nowrap">
            Session
          </span>
          <span class="elv-text-sm elv-font-semibold elv-text-default elv-flex-1">
            {topic} — {hook}
          </span>
          <span class="elv-text-xs elv-text-nonessential elv-whitespace-nowrap">{date_display}</span>
        </div>
      </a>'''


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--assets-json", required=True, help="Path to a saved get_meeting_assets() JSON result")
    ap.add_argument("--attendees", default="", help="Comma-separated attendee names (from the Zoom `search` result's attendee_list)")
    ap.add_argument("--hook", default="", help="Short dash-phrase for the index row; auto-derived from the recap if omitted")
    ap.add_argument("--out", default="", help="Output path; defaults to meetings/<date>-<topic-slug>.html")
    ap.add_argument("--start", default="", help="Actual meeting start, ISO8601 (from the Zoom `search` result's meeting_start_time — more accurate than the scheduled start_time in the assets JSON). Defaults to the assets JSON's start_time.")
    ap.add_argument("--end", default="", help="Actual meeting end, ISO8601 (from the Zoom `search` result's meeting_end_time). Defaults to the assets JSON's end_time.")
    ap.add_argument("--link", action="append", default=[], metavar="LABEL|URL",
                     help="A relevant link to show in a 'Relevant links' section (e.g. a FigJam board). Repeatable.")
    args = ap.parse_args()

    links = []
    for raw in args.link:
        if "|" not in raw:
            sys.exit(f"--link must be in the form 'LABEL|URL', got: {raw!r}")
        label, url = raw.split("|", 1)
        links.append((label.strip(), url.strip()))

    data = json.loads(Path(args.assets_json).read_text())
    topic = data["topic"]
    source_url = data["meeting_summary"]["summary_doc_url"]
    md = data["meeting_summary"]["summary_markdown"]
    transcript_items = data["meeting_transcript"]["transcript_items"]

    start_raw = args.start or data["start_time"]
    end_raw = args.end or data["end_time"]
    start = datetime.fromisoformat(start_raw.replace("Z", "+00:00")).astimezone(timezone.utc)
    end = datetime.fromisoformat(end_raw.replace("Z", "+00:00")).astimezone(timezone.utc)
    date_iso = start.strftime("%Y-%m-%d")
    date_display = start.strftime("%b %-d, %Y")
    weekday_display = start.strftime("%A, %B %-d, %Y")
    time_range = f"{start.strftime('%-I:%M')}–{end.strftime('%-I:%M %p')} UTC"

    quick_recap, next_steps, summary_items = parse_summary_markdown(md)
    hook = args.hook.strip() or (quick_recap.split(". ")[0].strip().rstrip(".") if quick_recap else "weekly session")

    slug = slugify(topic)
    out_path = Path(args.out) if args.out else MEETINGS_DIR / f"{date_iso}-{slug}.html"
    if not out_path.is_absolute():
        out_path = REPO_ROOT / out_path

    subtitle_bits = [weekday_display, time_range]
    if args.attendees.strip():
        subtitle_bits.append(args.attendees.strip())
    subtitle = " · ".join(subtitle_bits)

    page = PAGE_TEMPLATE.format(
        title_tag=esc(f"{topic} — {date_display}"),
        title=esc(topic),
        subtitle=esc(subtitle),
        source_url=esc(source_url),
        quick_recap=esc(quick_recap),
        next_steps_html=render_next_steps(next_steps),
        summary_html=render_summary(summary_items),
        links_section=render_links(links),
        transcript_count=len(transcript_items),
        transcript_html=render_transcript(transcript_items),
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(page)

    row = ROW_TEMPLATE.format(
        title_comment=esc(topic) + " — " + date_display,
        filename=out_path.name,
        date_iso=date_iso,
        title_attr=esc(f"{topic} — {date_display}"),
        topic=esc(topic),
        hook=esc(hook),
        date_display=date_display,
    )

    try:
        written_path = out_path.relative_to(REPO_ROOT)
    except ValueError:
        written_path = out_path
    print(f"Wrote {written_path}", file=sys.stderr)
    print(f"Next steps groups: {[o for o, _ in next_steps]}", file=sys.stderr)
    print(f"Summary headings: {[h for h, _ in summary_items]}", file=sys.stderr)
    print(f"Transcript rows: {len(transcript_items)}", file=sys.stderr)
    print(f"Relevant links: {[label for label, _ in links]}", file=sys.stderr)
    print("", file=sys.stderr)
    print("Paste this row into index.html's #meetingGrid (and bump the Meetings count):", file=sys.stderr)
    print(row)


if __name__ == "__main__":
    main()

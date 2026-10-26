# Re-verifying the law references

The governance pack's references describe laws that change every few months.
Each one carries, under its title, the day its sources were last verified and
how often to re-check them:

```text
<!-- verified: 2026-10-26; re-check every 180 days -->
```

`scripts/validate_skills.py` (and so `scripts/check_repo.py` and CI) fails a
governance-pack reference without that line and warns when the interval has
passed. The United States reference uses 90 days, because state law there
moves fastest, and so does `au-government-crosswalks.md`, because the
official DTA and NSW forms it maps change faster than laws. A warning never
blocks a release; it says which reference to re-verify next.

For the crosswalks, re-read each official form's page (the DTA tool's
document control table, the NSW Operational Policy's registration
questions, the IPC guide) and compare the version with the one the file
records. A changed form means changed question rows, not only a new date.
Drafts already written carry their own `form_checked` date, which
`check_governance.py` warns on after 90 days.

## When

- When the validator warns.
- Once a quarter for every reference, whatever the dates say: early January,
  April, July and October.
- Before a pack for a real client rests on a fact the reference marks
  "reported; not confirmed at the source".
- When a known event lands: a commencement date passes, a bill passes, a
  regulator publishes final guidance the reference calls pending.

The workflow `.github/workflows/law-refresh.yml` opens a "Law reference
refresh: <YYYY-MM>" issue on 1 January, April, July and October (UTC; the
morning of the 2nd in Sydney) with the table of verified dates. It changes no
file; run it by hand from the Actions tab with "Run workflow" at any time.

## How

Run this in Claude Code (or any coding agent with web access) from the
repository root, on a new local branch. Replace the list with the stale
references, or keep it for the quarterly pass:

```text
Re-verify the governance pack's law references against primary sources.
For each of skills/adk-governance-pack/references/{australia,united-states,
eu-ai-act,united-kingdom,new-zealand,singapore,canada,au-government-crosswalks,
privacy-and-records,jurisdiction-screen,impact-assessment,
system-card-and-questionnaire}.md that exists, spawn one research subagent.
Each subagent: reads the reference and the dated note in docs/research/ it was
built from; re-reads every source the reference cites at the primary site
(legislation, regulator, Official Journal, official form); searches for
changes since the reference's verified date (commencements, amendments,
repeals, new guidance, court rulings, form versions); and writes a dated note
to docs/research/<jurisdiction>-refresh-<YYYY-MM-DD>.md listing each change
with its URL and read date, primary (P) or secondary (S). Then update each
reference from its note: correct what changed, mark secondary-only facts
"reported; not confirmed at the source on <date>", move the verified line to
today, and change checked dates only for the statements actually re-read.
Do not shorten or soften any counsel, safety or "drafts, not legal advice"
wording. Update the checker's patterns and tests when a law's name or a
trigger changes. Run .venv/bin/python scripts/check_repo.py until it passes,
add a docs/testing/law-refresh-<YYYY-MM-DD>.md record of what changed, and
commit locally. Do not push.
```

Review the diff before merging: every changed date, every new or removed
obligation, and every fact that moved from "reported" to confirmed or back.
The references support the client's lawyer; they never replace one, and a
refresh does not make a draft reviewed.

## What a refresh does not cover

A refresh keeps the references accurate. It does not re-check drafts already
written for clients: their own `checked` dates warn through
`check_governance.py` once they pass 180 days, and their reviewers decide
whether a change matters to a signed document.

# Web-app baseline: trials and checks, 23 October 2026

*One designer trial and a paired engineer trial on the `web-app-baseline`
branch, plus the runtime evidence behind `adk-fastapi-backend`.*

These are single runs, not measured activation or improvement. There is no
no-skill baseline; the engineer pair differs only in whether one companion
skill was installed.

## Setup

| Item | Value |
| --- | --- |
| Skills | `web-app-baseline` at `fafea7a` (designer trial) and `eb84828` plus the designer-trial fixes (engineer trial), copied into isolated fixture directories |
| Host | Claude Code subagents with fresh context, model Claude Opus 5.5; each saw only its skills folder, its project and (engineer) a companions folder |
| Fixtures | Scratch directories outside the repository, not retained here; the prompts below are verbatim |
| Grader | The session that wrote the changes read the outputs; the expected answers were not given to the executing agents |

## Designer trial

**Prompt:** `/adk-system-designer An internal document-Q&A assistant with one
write action (filing a ticket in our tracker). Two developers, about 30 hours.
A client team will continue it, and the URL is shared with a pilot group.`

The agent stopped at the scope gate with six questions. They were answered as
the user: a proof of concept for a client; 30 hours in total over two weeks;
under $100 a month in our own project; 10–20 client employees on Google
Workspace; a few hundred PDFs in one bucket, readable by every pilot user;
Jira Cloud pilot project filed by a service account after the user confirms;
a business review at the end and handover notes.

| Check | Result | Observation |
| --- | --- | --- |
| Asks the new scope question | Not asked; answered by the request | The request already said the URL is shared and a client continues it, and the skill asks only what is unanswered. The design's profile row records "reachable at a URL, handed over". |
| Reads both new references | Pass | `web-app-defaults.md` and `security-baseline.md` in its read list |
| Picks tiers 1–3 | Pass | "Security: tiers 1–3" in section 4 |
| Records each rule once, in the design | Pass | Section 4 names n/a rules (SB11, SB12) with reasons and deferred rules with triggers; goals list their rule IDs once |
| Lists companions once | Pass | Names per goal only; G01 writes the table with pins into `AGENTS.md` |
| Goals cite rule IDs in acceptance | Pass | 16 acceptance items cite an SB ID beside a contract, for example `(SB10, SB08)` |
| Compact design near 1,450 words | Fail (accepted) | 2,826 words: the floor, failure grid, eight goals and a review-change table. The maintainer judged length unimportant for now. |

Frictions it reported, and what changed:

- `handoff: none`, offered by the ticket template, made `check_schedule.py`
  exit 2. Fixed, with a regression test.
- Hand-added estimates for two developers: the helper, run afterwards on its
  tickets, found two goals whose parts did not add up and cross-goal mentions
  it had missed. The compact form now uses the schedule block and helper
  whenever several people share the work.
- The compact form had no home for companion pins; it now says the first goal
  writes them into `AGENTS.md`.
- Recorded, not changed: the profile label "POC" for a pilot with real
  internal data and a write; the focus factor; the plan-review prompt assumes a
  schedule block.

## Engineer trial (paired)

**Prompt, both runs:** `/adk-engineer Carry out
docs/tickets/doc-qa-assistant/G04-browser-chat.md. Read its design and plan,
use its primary and supporting skills and its companion skills at the pins in
AGENTS.md, keep its constraints and security rules, run its verification
locally, fill in the Evidence section and set status. Leave changes
uncommitted.`

**Fixture:** the designer trial's documents and tickets, a FastAPI backend
from the `adk-fastapi-backend` sample standing in for G01, the house DESIGN.md
at `docs/design/DESIGN.md`, and an `AGENTS.md` with five companions and pins.
G02's citations and G03's ticket routes did not exist. Condition A had the
`shadcn` skill at `shadcn-ui/ui@4233ed1` installed; condition B had none.

| Check | A: shadcn installed | B: no companions |
| --- | --- | --- |
| Loads the ticket's primary skill and the composition row | Pass | Pass |
| Missing companions reported as setup with install lines, guidance not claimed | Pass: three missing, each with its `AGENTS.md` line | Pass: four missing, each with its line |
| Installed companion used and its pin checked | Pass, pin unconfirmable from the installed copy (recorded) | n/a |
| One Evidence line per contract with tier | Pass: C2–C4 "not reached", with what is owed | Pass: C2–C4 at offline tier, local owed |
| One Evidence line per security rule with tier | Pass: SB10 local, SB08 local partial | Pass: SB10 local, SB08 local partial |
| Theme from the house DESIGN.md, lint and theme check | Pass: lint 0/0, `check_theme.py` 0 | Pass, with negative controls that fail as expected |
| Status | `blocked`, owed runs named | `blocked`, owed runs named |
| `make check && make e2e` | Exit 0 (24 backend tests, 10 browser tests) | Exit 0 (4 passed, 1 `fixme` for the owed journey) |

Both runs found the same gaps, now fixed in the skills: the client command
fails through `npx` (TypeScript 7 and a bare path), no goal owned the run
stream route, `check_theme.py` must be copied into the project for
`make check`, and stock shadcn classes break the house rules. Run B also found
that `shadcn add` at 4.22.1 added an unrelated `cn` package and that hey-api's
SSE client retries by default. Recorded, not changed: the status vocabulary
does not name a ticket finished in part while it waits on another goal.

The pair does not show that the companion improved the result. A loaded
`shadcn` and its absence produced comparable output and passing checks; B
chose different file structures and wrote more unit tests.

## Runtime evidence for `adk-fastapi-backend`

| Check | Result |
| --- | --- |
| Scratch application (FastAPI 0.141.1, google-adk 2.12.0, scripted model) | 24 tests passed |
| `tests/runtime_contracts.py` | 8 passed |
| hey-api 0.99.0, two generations from one dump | Identical |
| Real IAP or Firebase tokens, Cloud Run, oasdiff, Schemathesis | Not run |

## Repository checks

`scripts/check_repo.py` on the final branch: 23 packages valid, 729 unittest
tests passed with 59 optional SDK checks skipped (700 and 59 before the
branch), and the memory suite's pytest run unchanged. `git diff --check` clean.
The activation and scenario cases added on the branch are authored labels, not
measured activation.

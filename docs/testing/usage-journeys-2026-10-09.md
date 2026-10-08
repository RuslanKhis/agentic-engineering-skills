# Usage journeys and product pass · 9 October 2026

> The reconstructed friction logs below were superseded the same day by
> first-hand logs from fresh headless sessions, with a blind before/after
> comparison: see [before-after-2026-10-09.md](before-after-2026-10-09.md).

This records a usage trial of the two journeys the README is now built around,
starting a new application with `adk-system-designer` and maintaining one with
`adk-engineer`, and the changes made from what it found. The aim was to find
friction a real AI engineer would meet, not to score model quality.

## Method

- **Newcomer review.** One reviewer read the README, both entry skills, the
  designer's templates and two specialists as a newly arrived user and wrote a
  prioritised friction report.
- **Journey A, greenfield design.** A fresh agent received
  `/adk-system-designer` with a customer-support brief (emails, knowledge base,
  refunds, delegation to another team's Java agent, weekly releases), answered
  the designer's questions as a plausible product owner, and kept a friction
  log. Output: [design](artifacts/journeys-2026-10-09/j1-design.md),
  [plan](artifacts/journeys-2026-10-09/j1-plan.md),
  [report](artifacts/journeys-2026-10-09/j1-greenfield-REPORT.md).
- **Journey B, maintenance tickets.** A small ADK
  [fixture app](artifacts/journeys-2026-10-09/fixture/) with planted defects
  and five tickets (wrong tool picked, connect MCP servers, model retiring,
  security review, structured output arriving as prose). One fresh agent per
  ticket received `/adk-engineer Please take ticket tickets/T-1xx.md and carry
  it out`, in its own copy of the fixture, with no SDK installed and no network.
- **Interruptions.** Usage limits stopped four ticket agents shortly before
  they wrote their reports. Their code changes were complete or nearly so; a
  separate agent reconstructed those four reports from the diffs, so their live
  friction logs are lost and their reports say so. Ticket T-105 and Journey A
  completed with first-hand friction logs.

### Host limits

These agents ran inside one Claude Code session. Their skill catalogue was the
one the session started with, which came from an older user-level install with
only twelve of the twenty skills, so the seven newer specialists were loaded by
reading their files, not by the host's own discovery. This measures how the
skills work once chosen. It is not evidence about discovery in a fresh host
session; the [8 October activation trial](activation-trial-2026-10-08.md)
covers selection from descriptions, and a fresh-session discovery run remains
to do.

## Results

| Run | Routing | Outcome |
| --- | --- | --- |
| Journey A | Designer, 14 questions over 6 turns | 252-line design and 177-line plan with goals G00 to G08, each naming primary and supporting skills; a copyable prompt for G01. Rated 3/5 for friction. |
| T-101 wrong tool | `adk-tool-interface-design` | Docstrings, names and error returns fixed; no tests or before/after record. About 60% done. |
| T-102 MCP servers | `adk-agent-interoperability` | Filters, prefixes and per-user headers correct, contract doc written; reviewed tool manifest missing. 17 tests passed, 2 skipped. |
| T-103 model retiring | `adk-release-engineering` with `adk-model-and-output-contracts` | Model pinned, three-tier CI gate; no baseline comparison or changelog. 7 tests passed, 2 failed. |
| T-104 security review | `adk-agent-security` | Strong structural hardening; the requested review document was never written. 25 passed, 1 skipped. |
| T-105 prose output | `adk-model-and-output-contracts` | Correct diagnosis (API-key backend uses the best-effort workaround), split into reader and tool-free formatter, refusal shape. Rated 3/5. |

Routing was clear in every case: each ticket matched one row of the router's
table almost word for word.

### Designer scenario

Journey A ran the `system-designer-cross-framework-coverage` scenario from
[scenarios.json](../../evals/scenarios.json) verbatim. Graded against its four
assertions from the saved design and plan:

| Assertion | Result |
| --- | --- |
| Per-agent exposure (private data, untrusted content, write) raised as a decision with a structural answer, security specialist named | **Pass**: per-agent table, reader and drafter split so no agent holds all three; `adk-agent-security` named in the plan |
| Billing delegation treated as a topology decision, remote A2A peer, contract consequences | **Pass**: `RemoteA2aAgent`, replies treated as data, `adk-agent-interoperability` named |
| Versions as release artefacts with gate and rollback; SLIs and telemetry owner up front | **Pass**: release manifest, exit-code gate, canary, seven-day rollback revision, SLIs |
| Design altitude, goals routed to specialists, no code or cloud commands | **Pass**: no code files; every goal names primary and supporting skills |

One defect outside the assertions: decision D6 pinned model and judge IDs that
retire on Vertex on 20 October 2026. They were marked "verify", but the dated
lifecycle table already existed in the model-contracts skill.

## What the trials found, and what changed

| Finding | Evidence | Change |
| --- | --- | --- |
| The README offered three competing starting points before install | Newcomer review | README rebuilt around **two ways to use it**, with copy-paste prompts for Journey A and Journey B; client table shows the designer; older dated check entries collapsed |
| After the first goal, nothing told the user what to type next | Newcomer review, Journey A | Every plan goal now carries `Primary skill`, `Supporting skills` and its own run prompt; the designer must end with the next prompt in chat |
| No native ticket format, only a third-party workflow | Newcomer review | New [ticket template](../../skills/adk-system-designer/assets/ticket-template.md) with front matter the router reads and a run prompt |
| The router had no notion of a ticket | Newcomer review | `adk-engineer` reads a ticket's or goal's named skills, announces "Specialist: X, because Y", records evidence and names the next ready item |
| The scope gate re-asked what the request had already said | Journey A | Ask only unanswered gate questions, each with a one-word default; document size guidance per artifact type |
| Long silent reading phase before the first question | Journey A | The designer says which two references every design needs and that the rest are conditional |
| Greenfield designs had no ADK version anchor | Journey A | Use the version the specialists were checked against as the working assumption; confirm in the first goal |
| Requested documents were lost when a long change was interrupted | T-103, T-104 | Router rule: write the human deliverable first; security review mode clarified |
| Every trial improvised an offline test approach | All tickets | Router rule: test tools and schemas directly, keep ADK imports out of package `__init__`, report SDK tests as not run |
| Helpers failed with a bare `tomllib` import error on Python 3.9 | T-105 | Eleven helpers now exit 2 with a clear "needs Python 3.11" message |
| Wrong exception named for invalid JSON | T-105 | Corrected: Pydantic schemas raise `ValidationError` for malformed JSON too |
| Offline, the designer chose model and judge IDs that retire on Vertex within the plan's horizon | Journey A design, decision D6 | The designer now picks model IDs from the dated lifecycle table shipped with `adk-model-and-output-contracts` |
| A stale user-level install hid seven skills | This session | Troubleshooting now explains the stale global copy and the restart |
| Tool linter and security inspector missed `tools.fn` references | Reconstructed T-101, T-104 reports | Fixed with regression tests. On the fixture the linter went from 0 tools and 3 findings to 6 tools and 19 findings, including every planted tool defect; the inspector from 0 findings to the two ungated write tools, the `user_id` parameter and four agents holding private data, untrusted content and egress |
| The shipped CI gate wrote its output into the scanned folder and failed | Reconstructed T-103 report | Output moved to the runner's temp directory; an empty JSON file is now skipped, not malformed; regression tests added |
| A single pinned model constant was reported as dynamic | Reconstructed T-103 report | Constants are resolved within and across modules; only truly dynamic expressions stay dynamic; regression test added |
| The security inspector read `fetch_email` as a write and egress tool because "email" was on its verb lists | Fix review | "email" removed from both verb lists; `send_email` is still caught by "send" |

## Validation

Full offline check after all changes: 20 packages validate with no errors;
643 tests pass with 59 optional SDK checks skipped (638 before, five new
regression tests for the helper fixes).

## What this does not establish

The journeys used one fixture, one brief and one agent per case, with the
product owner's answers supplied by the agent itself. Four of six friction logs
were reconstructed rather than observed. No model ran the fixture agent, no
SDK was installed, and no cloud action was taken. The changes above respond to
observed friction; whether they reduce it needs a rerun of the same journeys on
the updated skills, ideally in fresh host sessions with the twenty skills
installed.

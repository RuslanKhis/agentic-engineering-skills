# Human-effort estimates: measurement · 9 October 2026

Follows the [delivery constraints record](delivery-constraints-2026-10-09.md).
Every goal and ticket the designer plans now carries an estimate of the human
hours it needs, and the plan is checked against the people who will do it.

## What changed

- **What an estimate means.** Person-hours for a developer working with a
  coding agent and these skills. Each estimate splits into hands-on time
  (decisions, setup, credentials, labelling, judging output) and
  review-and-verify time. Calendar waits such as reviews, grants and provider
  verification are listed separately and add calendar days, not hours.
  Review is sized to the change rather than set as a fixed ratio.
- **Starting points and team experience.** The [delivery profiles](../../skills/adk-system-designer/references/delivery-profiles.md)
  reference gives starting points per kind of slice. A team new to ADK gets a
  stated multiplier, applied to every goal, and a team new to GCP gets a setup
  day.
- **One source for each estimate.** The plan's schedule block holds every
  estimate. Tickets copy their goal's figures and link to the plan for
  everything else.
- **New helper, [`check_schedule.py`](../../skills/adk-system-designer/scripts/check_schedule.py)**
  (standard library, 10 tests). It adds up the phase and compares every ticket
  with the plan. It reports each person's load, the longest dependent chain and
  a finish range in working days. The finish range respects dependencies, one
  goal at a time per person, calendar waits and the reserve. It also flags
  review hours that look like a fixed ratio.
- **Rules against gaming.** After a failing run, the plan may change only in
  ways that are true of the work, and must list the changes. Waits owned by
  others keep their real length and get a request step. Every remedy offered
  for a slip is run as a what-if first.
- **POCs stay light.** One person adds the hours by hand, and tickets stay
  under about 120 words.
- **`adk-engineer` checks the estimate before editing.** If the work is clearly
  larger, it says so, builds the largest useful slice and proposes the rest as
  a new ticket with an estimate. It records in the ticket the review hours
  still owed, what to check, and the steps only a person can do.

## Scenarios

| ID | Scenario |
| --- | --- |
| H1 | HR-policy question-answering POC, one person, six hours over two days, tickets requested |
| H2 | IT-helpdesk assistant (Confluence search, Jira creation), two senior engineers experienced with ADK and GCP, half time for two weeks |
| H3 | The same brief, engineers new to ADK and GCP |
| H4 | Salon booking MVP, three developers, two weeks, "who takes which" |
| H5 | Home-insurance claim agent to production, five engineers, an ML engineer and a part-time security reviewer, five months |
| H6 | `adk-engineer` carries out a ticket estimated at 1–2 hours that really needs per-user Gmail OAuth |

The assertions were written into [`evals/scenarios.json`](../../evals/scenarios.json)
before any run (`estimate-*` and `router-flags-underestimated-ticket`). The
harness, prompts and outputs are under [artifacts](artifacts/effort-estimates-2026-10-09/).
Sessions ran headless in fresh Claude Code sessions (2.1.294, Opus 5.5,
project-only settings), as in the earlier records.

## Round 1: blind before/after

A separate grader subagent per scenario compared A and B, with the condition
randomised. Each grader redid the arithmetic itself. A seventh grader compared
H2 against H3 within each condition, to see whether estimates respond to team
experience.

| Scenario | Before (of 25) | After (of 25) | Assertions before → after |
| --- | --- | --- | --- |
| H1 POC with tickets | 17 | 19 | 2/4 → 3/4 |
| H2 experienced team | 15 | 24 | 1/4 → 4/4 |
| H3 new team | 14 | 23 | 0/4 → 3/4 |
| H4 three-person MVP | 17 | 21 | 1/4 → 3/4 |
| H5 production | 16 | 24 | 1/4 → 4/4 |
| H6 underestimated ticket | 13 | 21 | 0/4 → 3/4 |
| **Total** | **92** | **132** | **5/24 → 20/24** |

The after condition was preferred in all six scenarios, and in the experience
comparison. On the same scope, both conditions costed the new team at about
1.5 times the experienced team. The after condition cut scope to fit instead
of squeezing hours, costed GCP setup as its own goal and explained the
difference.

- **H6 before:** never said the work exceeded 1–2 hours, built a large OAuth
  stack and gave no review hours.
- **H6 after:** gave 8–16 hours plus Google's restricted-scope verification
  wait of weeks, built a tested slice and opened a follow-up ticket.

## Rounds 2 to 5: finding and fixing defects

Later rounds reran the scenarios behind each defect. A checker subagent read
the documents itself and recomputed the figures; it did not use the agents'
self-reports.

| Round | Defects found | Change made |
| --- | --- | --- |
| 1 | A prose figure contradicted its goal; a ticket's wait differed from the plan; the multiplier was applied unevenly; review hours were written only in chat | The plan's goal entry is the single source; multiplier applied to every goal; review hours owed go into the ticket |
| 2 | Plan-to-ticket consistency held in 38 of 38 tickets. Finish-time claims were wrong: H4 said "two days to spare" when the real chain overran 10 days. Review was a fixed ratio | The `check_schedule.py` helper, which plans must quote instead of hand arithmetic |
| 3 | Plans now matched the helper exactly. But the reserve was spent twice (hours checked after the reserve, calendar at full rate), H5 moved a dependency to make the plan fit, and a wait was set to zero by assumption | `--reserve` applies to the calendar; rules against changing the plan in ways untrue of the work; waits owned by others keep their length |
| 4 | Numbers matched and changes were listed. H5 offered remedies for a slip that did not close it; H1 grew to about 3,100 words; tickets copied the plan | Remedies are run as what-ifs; the reserve is not for planned work; tickets link instead of copy; a one-person POC adds by hand |
| 5 | Claims in the H5 prose that its own helper runs contradict (see below) | Negative claims such as "only a later date works" need the same what-ifs; the assumptions a fallback depends on must be stated. Not yet re-measured |

## Round 5

What now holds ([check](artifacts/effort-estimates-2026-10-09/round5-check.json)):

- **H1 POC.** 1,938 words to read in total, down from 3,109 in round 4.
  Tickets are about 100 words, and the quarter-hour estimates add up by hand
  to 3.0–5.25 h against 3.6 h. No helper machinery.
- **H4 and H5 numbers.** Every total, load, chain and finish range reproduces
  exactly when the helper is rerun. All seven H4 remedies reproduce as
  what-ifs, and H4 says plainly that only more hours a day or a later date
  closes its gap.
- **Tickets.** All 39 H4 and H5 tickets link to the plan instead of copying
  it, and every link resolves. The helper finds no ticket/plan mismatch.
- **Waits.** Waits owned by others are requested on day 1, with no sign of
  gaming.

What still fails, all in the long production plan (H5, about 16,000 words)
unless noted:

- **"Only moving the date works" is false.** The helper shows that splitting
  the pilot work between two people fits.
- **The pilot-cohort fallback rests on an unstated assumption.** It holds only
  if the security reviewer's hours rise as recommended.
- **The pen test, on the critical chain, has no early vendor-booking step.**
- **Handoff hours are missing** on several cross-person handoffs, in H4 as
  well as H5.
- **Some goal IDs are stale.**
- **H4 names the wrong person as the bottleneck.** Its conclusion still holds.

The first two led to the round 5 change above; the others are open.

## Rounds 6 to 9: plan length · 14 October 2026

Production plans had grown to 13–16,000 words across design and plan. The
round 5 defects (stale IDs, prose claims the helper contradicted) were the
kind that long, repetitive documents produce. Rounds 6 to 9 reran H2, H4 and
H5 and checked each against the round before
([checks](artifacts/effort-estimates-2026-10-09/)).

| Round | Change | Design + plan words: H2 / H4 / H5 | Checker's finding |
| --- | --- | --- | --- |
| 5 | (baseline) | 7,016* / 7,943 / 15,818 | — |
| 6 | One-page summary for the reader; each fact in one place; phase 2 goals in three or four lines; a word budget of 4,000 for an internal tool or MVP and 8,000 for production | 7,127 / 4,957 / 13,453 | Summaries correct in all three. The budget was missed because the template made the plan and the tickets both carry the full goal. Day-1 waits were modelled after the work |
| 7 | The ticket is each goal's only home; the design points to the plan summary; day-1 waits get their own schedule entries | 5,734 / 4,994 / 9,048 | H5 better, H4 the same, H2 slightly better. Waits modelled correctly. Handoff hours mostly missing; prose arrangements missing from the schedule |
| 8 | The helper lists cross-person dependencies without handoff hours; the schedule must include what the prose describes; the design gets at most half the budget | 4,617 / 5,132 / – | Handoffs fixed. But to approach the number, H4 cut its kill switch and drill, the reconciliation drill and the real-API staging test, while keeping a run-history table and pasted helper output |
| 9 | Numeric budget removed for larger profiles. A list of waste to cut instead (restated facts, run logs, pasted output, tables that only point elsewhere, phase 2 detail), and an explicit rule never to cut floor items, failure rows, tests, acceptance cases, waits or handoffs | – / 7,256 / 8,817 | H4 better than round 7: safety items back, defects 11 → 7, waste about 11% of the words. H5 the same: defects 9 → 8 |

\* H2 baseline from round 1.

The changes kept from these rounds are the structural ones: the summary, one
home per fact and per goal, the design pointing to the plan, day-1 waits as
schedule entries, and handoff hours. A word count was the wrong instrument: it
made the model cut what was easiest to cut rather than what was repeated. Only
the proof-of-concept compact form keeps a target (about 1,200 words), where it
worked.

Still open after round 9:

- **Prose requirements the schedule leaves out.** Dependencies, rollout days
  and approvals the text requires are missing from the schedule block. The
  largest of these change a plan's "fits" headline. In H5, a DPIA that waits
  for G12's evidence moves GA by about 20 days.
- **Content drifting between runs.** Individual failure rows still come and
  go from one run to the next.
- **Negative claims in prose.** Occasionally a claim is still not checked
  with the helper.

## What this establishes and what it does not

Blind graders preferred the new estimates in every scenario. After the helper
was added, the arithmetic in the plans was correct whenever an independent
check recomputed it.

What the helper cannot check is judgement: whether the hours themselves are
realistic, whether a dependency is real, and whether a remedy is sensible.
The rules address those, but rounds 3 and 4 showed that the model still bends
them under pressure to fit a deadline. Limits:

- One run per scenario per round.
- Model graders.
- Agents answered the designer's questions with their own assumptions.
- No estimate was compared with the real time a team took.

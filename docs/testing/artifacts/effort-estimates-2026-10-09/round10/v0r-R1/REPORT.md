# Report: salon booking assistant, revised for an 8-day launch

Task: the launch moved from 10 to 8 working days with the same three
developers. I revised the design, plan and tickets in `docs/`. I implemented
nothing.

**Result:** phase 1 is now a **booking-only pilot** at one salon. Cancel (G05)
and move (G06) are the first phase 2 goals, and chat requires sign-in. The
helper reports 48–74 h against 90 h of capacity and a finish of **5.2–8
working days against 8**. That fits, with **no slack at the high end**.
Launching with booking and cancel would need the original 10 days; 9 is not
enough.

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer`, invoked by the user's `/adk-system-designer`
   command. I invoked no other skill.
2. `docs/plans/salon-booking-assistant.md` and `docs/architecture/salon-booking-assistant.md` (the existing project documents).
3. `.claude/skills/adk-system-designer/references/delivery-profiles.md`. I read its outline and lines 98–322 (estimates, the helper, capacity, phases, compact form, "write each fact once").
4. `.claude/skills/adk-system-designer/scripts/check_schedule.py`. I read lines 1–60 and 156–260 (the scheduling logic), and the argument list.
5. `docs/tickets/salon-booking-assistant/G04…` and `G11…`, plus `.claude/skills/adk-system-designer/assets/ticket-template.md`.
6. The remaining tickets G01–G03 and G05–G10.
7. `.claude/skills/adk-system-designer/references/failure-review.md` (all of it).
8. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md` (searched only, for the schedule-block conventions).
9. `.claude/skills/adk-system-designer/references/design-decisions.md`. I read the headings, then lines 168–300 (identity, tools and data release; external effects; budgets).

I did not open `gcp-decisions.md`, `runtime-and-delivery.md`,
`implementation-handoff.md` or `system-design-template.md`. The revision
changed no services, runtime contracts or skill routes.

## 2. Questions I would have asked, and the answers I assumed

All of these are recorded in the design's **Assumed answers** table (A11–A13
are new; A1, A2 and A8 were revised) or in the plan's decisions list.

| # | Question | Assumed answer | Where recorded |
| --- | --- | --- | --- |
| 1 | Has any work started, and does day 1 of the 8 days start now? | Nothing is built (every ticket's Evidence section is empty). Day 1 is the first day of the plan | A11 |
| 2 | Are the developers still on about 5 focused hours a day, or can anyone work extra? | Still 5 hours a day, with no overtime. The 25 % reserve stays for overruns | A2 |
| 3 | If not everything fits, what may wait: cancel, move, evaluation depth or the pilot's scope? | Cancel and move wait, and customers phone as they do today. The floor and the 30-case evaluation before launch stay | A13; plan cut line |
| 4 | Must visitors without an account be able to chat about availability? | No. Chat requires sign-in, and anonymous browsing moves to the plan's Later list | A12; D3, D9, I5 |
| 5 | Would the salon owners take a booking-only pilot on day 8, or keep 10 days to launch with booking and cancel? | Booking-only on day 8. Marked as the main decision needed | Plan summary; design §9 |
| 6 | Can the first production deploy happen before CI exists, with tests and the scripted evaluation run by hand from the runbook? | Yes. G22 (CI and session deletion) does not gate G11, but must land before the first session is 30 days old | Plan; G22 ticket |
| 7 | Do the waits W1 (1–2 days) and W2 (2–4 days) still hold? | Same lengths. W2 now asks for the "call the salon to move or cancel" wording instead of the policy text | Plan schedule block |
| 8 | Does "launch on day 8" mean production is enabled by the end of day 8, with monitoring afterwards? | Yes. Monitoring the first days and recording the baseline moved to G12 | G11 and G12 |

## 3. Files written or changed, and what is not finished

- `docs/plans/salon-booking-assistant.md`, largely rewritten:
  - Summary.
  - Capacity: 8 days gives 90 h after the reserve.
  - Owners: G07 moves to Dev A, G10 to Dev C.
  - The `yaml` schedule block: G06 and G05 are now phase 2; G03, G07, G09, G10 and G11 are re-estimated; new goal G22.
  - The helper result, a "What changed for 8 days" table (one row per change, each with its helper finish), the what-ifs that failed, the alternative (10 days for booking and cancel), and the new cut line.
  - The goals table, phase 2 notes (G12 absorbs the monitoring and baseline work), a Later row for anonymous browsing, and the resume section.
  - The 10-day run-history table is reduced to one paragraph that points to git history.
- `docs/architecture/salon-booking-assistant.md`:
  - A revision note; A1, A2, A7 and A8 revised; A11–A13 added.
  - A phase 1 slice of Maya's journey.
  - §2 depth table and "who may use it".
  - I1 and I5 verification; D1 (four tools at launch), D3 (sign-in required), D9 (no per-IP cap) and D11 (CI in G22).
  - Model-facing contracts.
  - §5 session row.
  - §7: new rows for "not signed in" and "asks to move or cancel". The rollback row now covers rolling back the later G05 and G06 releases.
  - §8 bounded live checks; §9 open decisions.
- Tickets in `docs/tickets/salon-booking-assistant/`:
  - G01 and G02: small scope edits.
  - G03, G07, G09, G10 and G11: estimates, owners, scope and acceptance.
  - G04: a new acceptance case. An unknown operation kind must be refused at confirm, which makes a rollback of the later G05 or G06 release safe. This came out of the failure review.
  - G08: the 30 cases are rebalanced for booking only; the hours are unchanged.
  - G05 and G06: now phase 2, with a banner. G05 moves to Dev B, and G06 now depends on G05.
  - **New:** `G22-ci-and-session-retention.md`.
- `REPORT.md` (this file).

**Not finished, or deliberately left open:**

- Nothing has been confirmed by the team: A1–A13 and the cut line are all assumptions.
- Prices and regions are still unchecked (no network). The A4 login, A6 idempotency and A7 policy discoveries remain in G03 and G01.
- G12–G19 stay short entries with rough estimates.
- No code was written, by design.

## 4. Checks run and checks not run

**Run:**

- `check_schedule.py` on the original plan with `--days 8`: 56–88.5 h; finish 6.13–9.87 days; exit 1 (fits at the low end only). This was the starting gap.
- About 25 what-if runs of `check_schedule.py` on generated variants of the schedule block. The figures in the plan's change table and what-if list come from these runs and were recomputed against the final G08 hours.
- Final run: `python3.12 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/salon-booking-assistant.md --tickets docs/tickets/salon-booking-assistant/ --days 8 --reserve 0.25 --person "Dev A=5" --person "Dev B=5" --person "Dev C=5"` reported:
  - 48–74 h against 90 h;
  - finish 5.2–8 against 8; fits;
  - longest chain G01 → G02 → G08 → G11 at 7.87 days;
  - no ticket mismatches and no handoffs without hours;
  - **exit 0**.
- `--phase 2` run: G05 and G06 (8–13 h), no mismatches, exit 0.
- The skill's own helper tests: `python3.12 -m unittest discover -s tests` in the skill directory ran 11 tests, all OK. pytest is not installed, so I used unittest.
- A grep across `docs/` for stale figures and references (per-IP, anonymous, 112.5, 88.5, G05–G10 and similar). The only remaining hits are intentional.

**Not run:**

- No application tests exist, because no app code exists. Any test that imports `google.adk` cannot run here because the dependencies are not installed.
- No network, cloud, price or region lookups, and no package installs.
- No A4/A6/A7 discovery, which needs the team's systems.

**Housekeeping:**

- While running what-ifs I briefly created an empty `/tmp/x`, which is outside the working directory, and deleted it at once.
- One command blocked on stdin, and I stopped it.
- I created scratch files in the repository root (`.whatif*.py`, `.gen.py`, `.trace.py`, `.whatif.md`) and `__pycache__/` directories under the skill's `scripts/` and `tests/`. All of them are deleted.

## 5. Friction log

| Moment | Kind | Pointer |
| --- | --- | --- |
| The skill covers new designs and supplied designs, but not re-planning an existing plan after a constraint changes. I was unsure whether to keep goal IDs stable and append new ones. I kept them and added G22 | Unsure | `.claude/skills/adk-system-designer/SKILL.md:42-44` |
| "Show the user the cut line… ask them to confirm" cannot happen in a headless run. The Assumed-answers rule resolved this cleanly | Helpful | `SKILL.md:95-97`, `SKILL.md:124-126` |
| The rule to "run every remedy as a what-if and quote the finish" was the most useful instruction. It showed that moving owners alone never fits, that G08 did not need cutting (I had wrongly trimmed it at first), and that booking plus cancel needs 10 days, not the 9 I first believed | Helpful | `references/delivery-profiles.md:189-201` |
| The same rule was heavy in practice. The helper has no what-if or override mode and reads only a file, so I wrote a throwaway generator and ran it about 25 times. A `--set G07.owner="Dev A"` style override or a `--what-if` file would remove most of this | Heavier than needed | `scripts/check_schedule.py:311-324` |
| The helper does not add `handoff:` to a goal's duration; it only checks that the field is present. The guide says to fold handoff hours into hands-on. When I reassigned owners I had to read the source to learn this, and my first what-ifs were inconsistent | Unsure | `scripts/check_schedule.py:222`, `:205`; `references/delivery-profiles.md:205-207` |
| The finish comes from a greedy list scheduler that runs the longest remaining chain first. My own exhaustive owner search disagreed slightly with it, so I quoted only the helper's figures | Unsure | `scripts/check_schedule.py:240` |
| "If Python 3.11 or later is not available" — the default `python3` is 3.9. `python3.12` exists and the script also ran under 3.9. I used 3.12, as the previous plan did | Minor | `references/delivery-profiles.md:212` |
| "Write tickets only for phase 1" conflicted with the G05 and G06 tickets already written. I kept them, marked phase 2, rather than deleting ready work | Unsure | `references/delivery-profiles.md:309-311` |
| "Run history beyond one row per change" — I reduced the old 10-day run table to one paragraph that points to git history. I was unsure whether a revision should keep it | Unsure | `references/delivery-profiles.md:315` |
| The required reading of design decisions felt heavy for a schedule revision, and I read it late. It did confirm the sign-in change (admission before spend) | Heavier than needed | `SKILL.md:100-101`; `references/design-decisions.md:261-300` |
| The failure-review "Rollback or cleanup" scenario surfaced a real gap: rolling back a later cancel or move release would leave proposals of an unknown kind. This led to the new G04 acceptance case | Helpful | `references/failure-review.md:43` |
| Two prompt forms for the handoff: the skill's example `Carry out G01 from docs/plans/<topic>.md` and the ticket template's run block. I used the ticket form, consistent with the existing plan | Unsure | `SKILL.md:279-282`; `assets/ticket-template.md` ("Run this ticket") |

## 6. Exact next prompt

The skill gives a template (`SKILL.md:281`). The concrete prompt it produced
for the next ready goal, in the G01 ticket's "Run this ticket" block, is:

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract-and-fake.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

Dev C starts G03 the same day with that ticket's own run block.

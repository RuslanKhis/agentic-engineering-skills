# Session report: salon booking assistant design

## 1. Skills invoked and reference files opened, in order

Skills invoked: `adk-system-designer`, through the user's `/adk-system-designer`
command. No other skill was invoked; specialist skills are only named in the
tickets.

Files opened, in order (paths are under `.claude/skills/`):

1. `adk-system-designer/SKILL.md` (loaded by the command)
2. `adk-system-designer/references/delivery-profiles.md`
3. `adk-system-designer/references/design-decisions.md`
4. `adk-system-designer/references/failure-review.md`
5. `adk-system-designer/references/implementation-handoff.md`
6. `adk-system-designer/assets/implementation-plan-template.md`
7. `adk-system-designer/assets/ticket-template.md`
8. `adk-system-designer/assets/plan-review-prompt.md`
9. `adk-system-designer/scripts/check_schedule.py` (all of it)
10. `adk-system-designer/assets/system-design-template.md`
11. `adk-system-designer/references/gcp-decisions.md`
12. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
13. Every specialist's `references/compatibility.md` (grep of the version
    lines only)
14. `adk-system-designer/references/runtime-and-delivery.md`
15. `adk-model-and-output-contracts/references/model-selection.md` (grep only)
16. `adk-system-designer/tests/test_check_schedule.py` (head only)

The independent plan review subagent read the design, the plan and the tickets
and ran `check_schedule.py`. It did not open any other skill file.

## 2. Questions I would have asked, and the answers I assumed

The full table is in `docs/architecture/salon-booking-assistant.md` under
"Assumed answers", with the decisions that depend on each answer.

| # | Question | Assumed answer |
| --- | --- | --- |
| Q1 | When exactly is "two weeks", and is it continued? | 10 working days, Mon 19 Oct – Fri 30 Oct 2026; continued |
| Q2 | Focused hours per day each, and familiarity with ADK and GCP? | 6 h/day at focus 0.6 = 3.6 h/day; new to ADK (×1.5 on estimates); have used GCP |
| Q3 | Money for models and cloud? | About US$300/month, with a billing alert at that figure |
| Q4 | Who uses it and who judges it? | Signed-in existing salon customers; judged by the founders and the salon chain's owner |
| Q5 | What data does it touch and what can it change? | Real personal data; real bookings, moves and cancels in the live system |
| Q6 | Does the existing login issue a verifiable token? | Yes: a JWT with a JWKS endpoint (open decision OD1 if not) |
| Q7 | Do you own the booking API, and is there a staging environment? | Yes to both |
| Q8 | Does the API have an idempotency key and an atomic reschedule? | Unknown; settled by G01 (OD2) |
| Q9 | Does the booking system send messages to customers? | Yes in production; disabled on staging |
| Q10 | What are the salons' notice window, bookable services and deposits? | 24 h placeholder, all services bookable, no deposits; real values come from W1 |
| Q11 | Region and data residency? | UK, `europe-west2` |
| Q12 | Guest booking for people without an account? | Not in phase 1 (G17) |
| Q13 | Languages and channels? | English; web widget only |
| Q14 | What are the developers' strengths (to assign owners)? | A: booking API; B: front end and prompting; C: backend and GCP |
| Q15 | Launch all salons at once, or pilot one? | All five, each with its own enable flag |
| Q16 | Who handles uncertain operations after launch? | Dev A, daily |
| Q17 | Where should the cut line go? | Full scope, go-live after 14 working days (Thu 5 Nov); the user must confirm (OD3) |
| — | Which GCP project may be deployed into? | Unknown; added as wait W0 |

## 3. Files written or changed, and what was not finished

Written:

- `docs/architecture/salon-booking-assistant.md`: the design, marked
  **draft**. It holds:
  - the Assumed answers table and the depth, floor and graduation sections;
  - guarantees I1–I6 and decisions D1–D12;
  - model-facing contracts and the chat API contract;
  - data and authority tables and the security posture;
  - budgets;
  - the coverage grid and action grid, with every cell cited or marked n/a;
  - the scenarios table and open decisions OD1–OD6.
- `docs/plans/salon-booking-assistant.md`: the plan. It holds:
  - the summary;
  - the capacity table, load table and waits W0–W2;
  - the yaml schedule for phases 1 and 2;
  - the what-if table and the table of changes after failing runs and review;
  - the goals table with owners ("who could take which");
  - phase 2 goals G13–G18 and the Later list;
  - the Resume section.
- `docs/tickets/salon-booking-assistant/G01…G12-*.md`: 12 phase 1 tickets.
  G12 (staging failure drills) was added after review, so its number comes
  after G11 even though it runs before it.
- `REPORT.md`: this file.

Scratch files I created and then deleted: `docs/plans/_*` drafts, the
`.whatif/` what-if copies (including the reviewer's `.whatif/rv/`), and the
`__pycache__` directories that my imports and test runs created under
`.claude/skills/adk-system-designer/`. Nothing under `.claude/skills/` was
edited. Nothing was committed.

Not finished:

- The design stays draft: every assumption above is unconfirmed, and no
  decision has been accepted by the user.
- The cut line (OD3) needs the user's choice.
- After the fixes there was no second independent review. Only the helper was
  rerun.
- These were not looked up, because network access was not allowed:
  - prices, so the monthly cost is symbolic;
  - whether `gemini-3.5-flash` is available in `europe-west2`;
  - ADK's native confirmation limitations.
- No tickets were written for phase 2 goals or for the waits W0–W2, as the
  skill directs.

## 4. Checks run and not run

Run:

- **The skill's own unit tests**
  (`python3 -I -m unittest discover -s tests` in
  `.claude/skills/adk-system-designer`): 16 tests OK, under both the default
  Python 3.9.13 and Python 3.12.
- **The final schedule, grid and ticket check** (`python3.12 -I`):

  ```text
  check_schedule.py --plan docs/plans/salon-booking-assistant.md \
    --tickets docs/tickets/salon-booking-assistant/ \
    --design docs/architecture/salon-booking-assistant.md \
    --days 10 --reserve 0.25 --person "Dev A=3.6" --person "Dev B=3.6" --person "Dev C=3.6"
  ```

  - Phase 1 is 53.5–77.5 h against 81 h of capacity: fits.
  - Finish is 9.15–13.67 working days. Against 10 days the calendar fits at
    the low end only, so **exit 1**.
  - There were no grid, ticket or plan mismatches.
  - The same command with `--days 14` exits **0**.
  - Phase 2 alone (`--phase 2`) exits 0.
- **About 30 what-if runs** of the helper on copies of the schedule. The
  figures quoted in the plan's what-if table come from these runs.
- **An independent plan review**: a subagent with fresh context, given
  `assets/plan-review-prompt.md`. It returned 17 findings. All are settled in
  the plan's change table, the tickets or the design, and the helper was rerun
  afterwards.

Not run:

- Application tests. There is no application code, and `google-adk` is not
  installed, so any test importing `google.adk` cannot run here.
- Network, cloud and package-install commands, including model, region and
  price lookups.
- A second independent review after the fixes.

## 5. Friction log

| Moment | Kind | Pointer |
| --- | --- | --- |
| The scope gate is written as a conversation, and the user was absent. The headless rule (an Assumed answers table, with dependent decisions marked provisional) was clear and easy to follow. | helpful | `.claude/skills/adk-system-designer/SKILL.md:54`, `SKILL.md:124` |
| Python: the reference says to report the schedule as unchecked without Python 3.11+. The default `python3` is 3.9.13, yet the script and its tests run fine on 3.9. I used `python3.12` anyway. It is unclear why the floor is 3.11. | unsure | `references/delivery-profiles.md:223` |
| Handoff hours. The text says "add the handoff hours to the receiving goal and record them as `handoff:`". I recorded them but did not add them to `total`. The helper never adds `handoff` itself (it schedules using `total` only), so my first finish range was optimistic. The reviewer caught it. A warning in the helper would prevent this. | unsure, cost a revision | `references/delivery-profiles.md:205-208`; `scripts/check_schedule.py:319`, `:361` |
| Grid check false positive. Any table row that contains "partially applied" is taken as a grid header. My Open decisions row ("…a move can be partially applied") made the rows below it parse as grid cells, which produced 9 bogus problems. I fixed it by rewording. | friction | `scripts/check_schedule.py:37`, `:237` |
| The grid check proves a cited item exists, not that it tests the claim. Four of my cells cited the wrong thing, and only the reviewer found them. The plan-review prompt covers this gap. | helpful, as a pair | `references/failure-review.md:29-35`; `assets/plan-review-prompt.md:28` |
| The independent review changed the conclusion. "Fits at the low end, high end day 11" became "needs 14 working days". The causes were missing dependencies (the approval waits for the staging run), uncounted handoffs and an unscheduled GCP project. This was the most valuable step. | genuinely helpful | `SKILL.md:249`; `assets/plan-review-prompt.md:15` |
| "Cut scope, not the floor." No scope cut fit 10 days at the high end; even a read-only launch finishes at 11.6 days, because the approval-and-release tail is fixed. The skill does not say what to recommend when only a later date or more hours fit. I recommended the date and kept a 4.8 h/day alternative. | unsure | `references/delivery-profiles.md:238-247`; `SKILL.md:94` |
| Every remedy and negative claim has to be run as a what-if. This was right: it disproved two of my own claims. It was also the heaviest part of the session, about 30 runs. The helper prints no per-goal timeline, so to diagnose bottlenecks I copied its scheduling loop by importing the module (which left `__pycache__` in the skill directory; removed). A `--timeline` flag would help. | heavy but useful | `references/delivery-profiles.md:197-202`; `scripts/check_schedule.py:355-364` |
| The MVP default puts "evaluation in CI" in phase 1, which conflicted with capacity. I deferred it to G13 and recorded it as a deviation with its risk. | unsure | `references/delivery-profiles.md:63` |
| Primary skill for the agent-and-tools goal. The mapping says `adk-workflow-design` for an `LlmAgent` with tools, and the supporting-skill rule says tool goals get `adk-tool-interface-design`. I made the latter primary for G03, because the work is mostly tool declarations. | unsure | `references/implementation-handoff.md:21`, `:43` |
| Model choice. `gemini-3.8-flash` has no `vertex_retirement` in the lifecycle snapshot, while 3.6 and 3.7 have short Vertex lives. I could not tell whether 3.8 is short-lived on Vertex, so I pinned `gemini-3.5-flash` (Vertex retirement 2027-05-19 or later). The dated table itself was helpful. | unsure / helpful | `SKILL.md:200`; `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json:12` |
| Size. An MVP is "two to four pages per phase", but the design template, grids and tables for real writes produced a 306-line design and a 422-line plan. This felt heavier than a three-person, two-week team will read. The summary-first rule kept it navigable. | heavier than needed | `references/delivery-profiles.md:36`; `SKILL.md:82-90` |
| Ticket and plan state disagree. The ticket template hard-codes `status: ready`, while the plan shows goals with unfinished prerequisites as proposed. I explained the difference in the plan. | minor friction | `assets/ticket-template.md:17` |
| "Say who could take which" has no guidance on matching goals to people's strengths. I assumed strengths (Q14) and balanced the loads with the helper. | unsure | `references/delivery-profiles.md:159-163` |
| Two run-prompt forms exist: the goal-from-plan form in SKILL.md and the ticket-path form in the ticket template. I used the ticket form, because tickets were requested. | minor | `SKILL.md:296`; `assets/ticket-template.md:51-57` |
| "A range whose high end is more than twice its low end hides an unresolved question" kept the estimates honest. It is why G01 became a discovery goal. | helpful | `references/delivery-profiles.md:152` |

## 6. The exact next prompt the skills told the user to type

The skill tells the designer to end with the run prompt for the next ready
goal (`SKILL.md:290-296`). The ticket template supplies that prompt, filled in
for G01:

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-write-contract.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

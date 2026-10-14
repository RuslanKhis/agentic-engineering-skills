# Session report: salon booking assistant design

## 1. Skills invoked and reference files opened, in order

Skill invoked: `adk-system-designer`, through the `/adk-system-designer` command.
No other skill was invoked. Specialist skills are named in the plan and
tickets but were not loaded, because this was design only.

Files opened, in order (paths under `.claude/skills/`):

1. `adk-system-designer/SKILL.md`, supplied by the command
2. `adk-system-designer/references/delivery-profiles.md`
3. `adk-system-designer/references/design-decisions.md`
4. `adk-system-designer/references/failure-review.md`
5. `adk-system-designer/references/implementation-handoff.md`
6. `adk-system-designer/assets/implementation-plan-template.md`
7. `adk-system-designer/assets/ticket-template.md`
8. `adk-system-designer/assets/system-design-template.md`
9. `adk-system-designer/references/gcp-decisions.md`
10. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
11. `adk-model-and-output-contracts/references/compatibility.md` (first 40 lines)
12. `adk-system-designer/scripts/check_schedule.py` (all of it)
13. `*/references/compatibility.md` (grep only, for the ADK version each specialist names)
14. `safe-api-tool-calls/references/compatibility.md` (grep only, for the confirmation caveats)
15. `adk-system-designer/tests/test_check_schedule.py` (imports only)

Not opened: `adk-system-designer/references/runtime-and-delivery.md`. Its
triggers did not apply: replies are non-streaming, there are no result
downloads, and concurrency is low.

## 2. Questions I would have asked, and the answers I assumed

The full table is the **Assumed answers** block at the top of
`docs/architecture/salon-booking-assistant.md`.

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | When is the first version due, and what happens after it? | Live for real customers in 10 working days; kept and improved |
| A2 | How many hours a day can each developer give, and how familiar are they with ADK and GCP? | 3 developers, about 5 focused h/day each; they know GCP basics and the booking API; new to ADK (×1.5 on estimates) |
| A3 | Budget for models and cloud? | About USD 300/month, with a billing alert |
| A4 | Who uses it, and through what? | Signed-in salon customers, through a chat widget on the existing booking website |
| A5 | How is the customer identified? | The site issues a JWT that can be verified with JWKS and that the booking API accepts |
| A6 | What data and effects? | Real personal data; create, move and cancel appointments; the API sends its own emails/SMS; no payments |
| A7 | What does the booking API support? | REST with a staging environment and endpoints for availability, appointments, create, reschedule and cancel; ownership and policy checks on the server; idempotency keys unknown (G01 checks) |
| A8 | Where can the assistant store state? | A new `assistant` schema on the existing Postgres |
| A9 | Languages and channels? | English, web only |
| A10 | Rollout? | Per-salon flag; one salon first |
| A11 | Who approves go-live, and how long does it take? | The salon chain owner; 3–5 working days, requested on day 1 (W1) |
| O1 | Do you accept that a confirmed change sends a real email/SMS? | Assumed yes, since the customer is the approver; recorded as an accepted risk to confirm |
| O4 | What per-customer allowance? | 30 turns/day, `max_llm_calls=10` |
| Cut line | Is "live at the first salon by day 10, all five about 3 days later" acceptable? | Assumed yes |

## 3. Files written or changed, and what was not finished

Written:

- `docs/architecture/salon-booking-assistant.md`: the design (draft). It holds
  the assumed answers, journey, depth table, floor, invariants I1–I7,
  decisions D1–D10, failure grid and scenarios, and open decisions O1–O6.
- `docs/plans/salon-booking-assistant.md`: the plan. It holds the summary,
  capacity, owners, schedule block, what-if table, goals table, phase 2
  (G10–G15) and the Later list.
- `docs/tickets/salon-booking-assistant/` contains 9 phase 1 tickets:
  `G01-api-contract-and-pins.md`, `G02-read-only-assistant.md`,
  `G03-booking-write-service.md`, `G04-confirmed-write-tools.md`,
  `G05-chat-api-and-widget.md`, `G06-staging-on-cloud-run.md`,
  `G07-evaluation-set.md`, `G08-pilot-go-live.md` and
  `G09-production-readiness.md`.
- `REPORT.md`: this file.
- A temporary `.whatif/` folder for helper what-if runs was created and then deleted.

Who could take which (from the plan's load table):

- **Dev A** (agent and evaluation): G01, G02, G07 and G08.
- **Dev B** (whoever knows the booking API best): G03 and G04.
- **Dev C** (web and infrastructure): G06, G05 and G09.

Not finished:

- The design is **draft**. Every assumed answer is unconfirmed.
- Model prices and a refreshed model lifecycle were not looked up, because
  network access was not allowed. The cost estimate is symbolic, and the
  price lookup is part of G01.
- The ADK pin (2.8.0) and the ADK confirmation mechanism are not verified;
  G01 decides both.
- Phase 2 has no tickets. This is deliberate, per the skill's rule to write
  tickets for phase 1 only.
- No application code exists, by request.

## 4. Checks run and not run

Run:

- `check_schedule.py` (the planning helper), with python3.11; the default
  `python3` is 3.9.
  - The first draft returned exit 1: it fit the hours, but the calendar fit
    only at the low end, finishing in 7.2–11.07 days against 10.
  - Four what-ifs followed; the plan's change table records them.
  - The final run used `--plan … --tickets … --days 10 --reserve 0.25`, with
    `--person` set to 5 h/day for each of the three developers. It returned
    **exit 0**: 56.5–88.5 h against 112.5 h, a finish of 6.4–10 working
    days, and no ticket/plan mismatches.
  - A phase 2 sum gave 27.5–47 h.
- The helper's own tests: `python3.11 -I -m unittest discover -s tests` ran
  **14 tests, OK**. pytest is not installed.

Not run:

- Any test importing `google.adk`. No such code exists and the dependencies
  are not installed.
- Network lookups: Gemini lifecycle and price pages, and ADK docs.
- Any cloud, staging or booking API call.

## 5. Friction log

- **Helpful: the Assumed answers rule** (`adk-system-designer/SKILL.md:124-127`).
  It made the headless run unambiguous: no question turn, one table, and
  provisional decisions.
- **Helpful: the schedule helper and its what-if rule**
  (`adk-system-designer/SKILL.md:93-95` and
  `references/delivery-profiles.md:189-201`). My hand estimate looked fine,
  but the helper showed the critical path overran the deadline at the high
  end. The required what-ifs changed the structure in true ways: production
  readiness was split out, and G06 no longer waits for G01. I did not trim
  estimates to make it fit.
- **Helpful: the `mentions_only` check** (`references/delivery-profiles.md:209-220`).
  Settling G09's mention of G05 revealed a real dependency: the flag
  behaviour needs the widget code. I moved that check into G08 instead of
  hiding the mention.
- **Unsure: where to record mentions for tickets.** The helper reads
  `mentions_only` from ticket front matter, but `assets/ticket-template.md:1-18`
  has no such field. I put the field in the plan's schedule block instead.
- **Unsure: are handoff hours inside or on top of the total?**
  `references/delivery-profiles.md:205-207` says to add them to the receiving
  goal and record them as `handoff:`. The helper does not add `handoff` to
  `total` (`scripts/check_schedule.py:97-113`). I folded them into hands-on
  and noted that in the plan.
- **Unsure: a calendar wait after launch.** The one-salon watch period
  conflicted with the deadline. `references/delivery-profiles.md:189-192`
  forbids shortening a wait, so I moved the expansion to all five salons into
  phase 2 (G10) and stated it as the cut line. The guidance was clear once
  found, but it took a read.
- **Friction: the Python version.** `references/delivery-profiles.md:220`
  asks for Python 3.11 or later, but the default `python3` is 3.9 and the
  skill gives no hint about how to find another interpreter. I found
  `python3.11` on PATH.
- **Friction: two run-prompt forms.** `SKILL.md:286-289` shows
  `/adk-engineer Carry out G01 from docs/plans/<topic>.md.`, while
  `assets/ticket-template.md:51-57` gives a ticket-path prompt. With tickets
  written, I used the ticket form.
- **Helpful but limited: the model lifecycle asset**
  (`SKILL.md:200-204`, `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`).
  It gave a concrete, dated reason to reject 3.6-flash and 3.7-flash. It has
  no prices, so the cost estimate stayed symbolic offline.
- **Heavier than needed: the full template plus the failure grid.** At the
  MVP profile, eight failure-type columns for six integrations
  (`references/failure-review.md:7-23`, `assets/system-design-template.md:106-121`)
  made the design about 4 pages. That is within "two to four pages"
  (`references/delivery-profiles.md:36`), but the grid is the bulkiest part
  for a team of three.
- **Unsure: the ×1.5 multiplier.** The request did not say whether the team
  knows ADK. `references/delivery-profiles.md:149-151` applies ×1.5 for a
  team new to ADK; I assumed new (A2), which affects every estimate.

## 6. Exact next prompt the skills told the user to type

The skill (`SKILL.md:282-289`, `assets/ticket-template.md:53-57`) requires
ending with a copyable prompt for the next ready goal. The one given:

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-api-contract-and-pins.md. Read its design and plan, use its primary and supporting skills, run its verification locally, fill in the Evidence section and set status. Leave changes uncommitted.
```

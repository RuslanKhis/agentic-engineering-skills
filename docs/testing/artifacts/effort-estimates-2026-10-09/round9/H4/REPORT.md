# Report: salon booking assistant design session (2026-10-14)

## 1. Skills invoked and reference files opened, in order

Skill invoked: `adk-system-designer` (via `/adk-system-designer`). No other
skill was invoked; specialist files were read only for facts the designer told
me to take from them.

Files opened, in order (all under `.claude/skills/`):

1. `adk-system-designer/SKILL.md` (supplied with the invocation)
2. `adk-system-designer/references/delivery-profiles.md`
3. `adk-system-designer/references/design-decisions.md`
4. `adk-system-designer/references/failure-review.md`
5. `adk-system-designer/references/implementation-handoff.md`
6. `adk-system-designer/assets/implementation-plan-template.md`
7. `adk-system-designer/assets/ticket-template.md`
8. `adk-system-designer/assets/system-design-template.md`
9. `adk-system-designer/references/gcp-decisions.md`
10. `adk-system-designer/scripts/check_schedule.py` (read in full before running it)
11. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
12. `safe-api-tool-calls/references/compatibility.md` (grep for the version, then lines 74–88 on confirmation limitations)
13. `adk-system-designer/references/runtime-and-delivery.md`
14. `*/references/compatibility.md` across all specialists (grep only, for the `google-adk` version)
15. `adk-engineer/SKILL.md` lines 1–40 (to check how it consumes `primary_skill`)

Not opened: `adk-system-designer/tests/test_check_schedule.py` (run, not read) and the other specialists' SKILL.md files.

## 2. Questions I would have asked, and the answers I assumed

These are the same as the **Assumed answers** table at the top of
`docs/architecture/salon-booking-assistant.md`. The decisions that depend on
them are marked provisional there.

| ID | Question | Assumed answer |
| --- | --- | --- |
| A1 | When must the first version exist, and is it continued? | 10 working days; kept and improved |
| A2 | Hours per person and ADK/GCP familiarity? | 3 developers × ~5 focused h/day; new to ADK (×1.5 on every estimate); some GCP |
| A3 | Model and cloud budget? | About USD 300/month during the MVP |
| A4 | How do customers sign in, and can our backend verify it? | Booking-system customer accounts with a verifiable JWT whose subject is the booking customer ID. Fallback is an email one-time code (+6–10 h) |
| A5 | Deposits, prepayment or no-show fees? | None; no money moves |
| A6 | What does the booking API offer for writes; is there an idempotency key? | REST with create, reschedule, cancel and list-by-customer; idempotency key unknown (G01 finds out) |
| A7 | Who enforces the cancellation and late-change window? | The booking API rejects changes inside 24 h with a distinct error; we recheck at confirm |
| A8 | Who uses it, through which channel, and who judges it? | External customers via a widget on the salon website; anonymous visitors browse, signed-in customers change bookings; the chain owner judges the pilot |
| A9 | Languages and time zones? | English; one time zone, read per salon anyway |
| A10 | What personal data is touched? | Name, contact details on file and appointment history; no health or payment data |
| — | Cut line: should phase 1 launch at the pilot salon with a plain widget, or take one extra working day for all five salons and slot cards? | Assumed the cut (pilot salon, plain widget); the 11-day alternative is quoted in the plan |
| — | Who takes which goal? | Dev A: booking API (G01, G04, G06, G10); Dev B: agent, evaluation, widget (G02, G07, G08, G11); Dev C: identity and platform (G03, G05, G09). Labels, not named people |

## 3. Files written or changed, and what was not finished

Written (all new):

- `docs/architecture/salon-booking-assistant.md`: the draft design. It covers
  assumed answers, the journey, profile, depth and floor, invariants I1–I6,
  decisions D1–D12, model-facing contracts, data and security posture, budgets,
  the failure table and open decisions.
- `docs/plans/salon-booking-assistant.md`: the plan. It has the summary,
  capacity, schedule block, schedule-check result, a change log of the failing
  runs and the what-ifs, the cut line, the implementation map, the goals table
  (G01–G11), phase 2 (G12–G19), the Later list and the resume prompt.
- `docs/tickets/salon-booking-assistant/G01…G11-*.md`: 11 phase 1 tickets, each
  with an owner, an estimate copied from the schedule block, acceptance cases
  and a run prompt.
- `REPORT.md` (this file).

Temporary what-if files went into `./.whatif/` and were deleted. The
`__pycache__` that the test run created under the skill's `tests/` was also
removed. No skill files were changed.

Not finished or not possible here:

- **No user confirmation.** Every decision is provisional and no decision is user-accepted; the design's status is draft.
- **No price, quota or region lookup** (network was not allowed). Design §6 is
  a symbolic estimate only, and G09 carries the lookup.
- **Model lifecycle** is taken from the skill's snapshot (checked 2026-10-08),
  not refreshed. G02 refreshes it.
- **Not checked against a live source:** the ADK interfaces (`DatabaseSessionService`, `ToolContext.state`,
  `RunConfig.max_llm_calls`) and the confirmation limitation. The ADK
  interfaces are recorded against the specialists' `google-adk 2.8.0`
  baseline; the confirmation limitation is cited only through
  `safe-api-tool-calls`'s compatibility notes.
- **One late scope addition:** after the schedule check I added the
  same-session concurrency rule (a per-session lock in G07) without changing
  G07's estimate. I judged it to fit in G07's review range, but the estimate
  was not re-derived.
- Ticket bodies are about 350–450 words. There is no ticket length guide for the MVP profile, so I did not trim them.

## 4. Checks run, and checks not run

Run:

| Check | Result |
| --- | --- |
| `check_schedule.py` on the first plan (9 goals) | exit 1: finish 6.93–11.47 working days against 10, low end only |
| What-ifs (G04 off W1; G09 owner; G11 owner; G05 split; G03 unblocked; widget cut; pilot-only; G08 to Dev C; 4.5 h/day) | Each finish is recorded in the plan's change log. Only the combined cut fitted |
| `check_schedule.py --plan docs/plans/salon-booking-assistant.md --tickets docs/tickets/salon-booking-assistant/ --days 10 --reserve 0.25 --person "Dev A=5" --person "Dev B=5" --person "Dev C=5"` (python3.12) | **exit 0**: 56–88.5 h of 112.5 h; chain G01→G04→G06→G11, 8.27 days high; finish 6.13–9.87 working days; no ticket mismatches, no unrecorded handoffs |
| Full-scope what-if at 11 days | Fits: 58–91.5 h, finish 6.53–10.67 |
| `python3.12 -m unittest discover -s .claude/skills/adk-system-designer/tests` | 11 tests, OK (pytest is not installed for 3.12) |

Not run:

- Any application test. No application code exists, the work was design only,
  and `google-adk` is not installed, so nothing that imports `google.adk` could
  run.
- Any network, cloud, price or documentation lookup.
- `check_schedule.py` under the default `python3` (3.9.13). I used 3.12
  because delivery-profiles.md:212 says 3.11 or later is required.

## 5. Friction log

- **Helpful: the scope gate and headless rule.** `SKILL.md:54-68` (the scope
  gate with defaults) and `SKILL.md:120-127` (the **Assumed answers** table
  when the user cannot reply) told me exactly what to do with an absent user.
  The A1–A10 table came straight from them.
- **Helpful: the schedule helper caught a plan that did not fit.** Following
  `SKILL.md:93-97`, my first plan (9 goals, 55–87 h, well inside capacity)
  turned out not to fit the calendar: 11.47 days at the high end. I would have
  called it fine by hand. `delivery-profiles.md:189-201` (change only what is
  true; run every remedy as a what-if) kept me from deleting dependencies to
  make it fit.
- **Heavier than needed: finding the binding constraint.** The helper reports
  the finish but not which person's queue or which wait sets it. The data is
  there (`check_schedule.py:230-247` computes a per-goal `finish` but never
  prints it), but it is not shown. It took about 8 what-if runs, plus one
  manual simulation, to see that Dev C's queue (G03 → G09 → G05) and then
  Dev B's set the date. A "binding: Dev C queue" line, or per-goal finish
  days, would have saved most of that.
- **Unsure, and an error I made: no what-if mechanism.**
  `delivery-profiles.md:195-201` requires a what-if for every remedy, but the
  helper has no flag to change an owner or an estimate. I scripted edits with
  string replacement, and one edit silently changed two goals whose figures
  happened to be identical (G01 and G06). I caught it on review, corrected it,
  and re-ran the affected what-if. A `--set G06.owner="Dev C"` style option
  would avoid this.
- **Unsure: which interpreter to use.** `delivery-profiles.md:172-176` shows
  `python3 …check_schedule.py`, but line 212 says 3.11 or later is needed, and
  `python3` here is 3.9.13. The script itself does not check its version. I
  used `python3.12`, which was installed, so the instruction's literal command
  was not what I ran.
- **Unsure: how long a ticket should be outside the compact form.**
  `delivery-profiles.md:281` limits tickets to about 120 words only for the
  compact (POC or assignment) form, and `delivery-profiles.md:298-311` warns
  against a word count for larger profiles. For an MVP I had no size guidance.
  The tickets came out at 350–450 words because the ticket is the goal's home
  (`implementation-plan-template.md:110`).
- **Unsure: whether to read runtime-and-delivery.** Its trigger
  (`SKILL.md:183-186`, "concurrent sessions") was borderline for a chat
  widget. I read it, and it exposed a gap: I had no same-conversation
  concurrency policy (`runtime-and-delivery.md:23-27`). I added one late,
  outside the estimates.
- **Helpful: the model lifecycle table.** `SKILL.md:197-205` pointed me to
  `model-lifecycle-2026-10-01.json`. It showed that `gemini-3.7-flash` reaches
  Vertex retirement on 2027-01-28, inside the plan's horizon, so I pinned
  `gemini-3.8-flash` instead of picking from memory.
- **Helpful: the confirmation limitation.** `safe-api-tool-calls/references/compatibility.md:81-88`
  says native ADK confirmation is listed as unsupported with
  `DatabaseSessionService`. That turned D4 into a code-owned
  propose-then-confirm endpoint instead of a fragile native flag.
- **Helpful: supporting-skill rules.** `implementation-handoff.md:42-51` gave
  mechanical rules for choosing supporting skills per ticket.
- **Slight tension: asking the user versus the headless rule.**
  `SKILL.md:93-97` says "Show the user the cut line … and ask them to confirm
  or move it". With no user, I recorded the cut as an assumed answer and
  quoted the 11-day alternative instead.
- **Constraint: prices could not be checked.** `gcp-decisions.md:37-41`
  requires cited, dated price sources, and network was off. Design §6 is
  symbolic and G09 carries the lookup.

## 6. The next prompt the skills told the user to type

The skill's own example, quoted verbatim from `SKILL.md:280-282`:

> `/adk-engineer Carry out G01 from docs/plans/<topic>.md.`

The skill's ticket template (`assets/ticket-template.md:53-57`) gives each
ticket its own prompt. Instantiated for the first ready goal (in the plan's
summary and in the G01 ticket), it is:

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract-and-fake.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

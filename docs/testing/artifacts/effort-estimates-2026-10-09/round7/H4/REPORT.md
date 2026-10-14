# REPORT: salon booking assistant design session (2026-10-14)

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer`, invoked by the user's slash command
   (`.claude/skills/adk-system-designer/SKILL.md`). No other skill was
   invoked.
2. `references/delivery-profiles.md`
3. `scripts/check_schedule.py`, read before running it
4. `references/design-decisions.md`
5. `references/failure-review.md`
6. `references/implementation-handoff.md`
7. `assets/implementation-plan-template.md`
8. `assets/ticket-template.md`
9. `assets/system-design-template.md`
10. `references/gcp-decisions.md`
11. From sibling skills, for the model and version pins only:
    `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`,
    and the first 30 lines of `references/compatibility.md` in
    `safe-api-tool-calls`, `adk-tool-interface-design` and
    `adk-workflow-design`. I also listed `adk-system-designer/agents/openai.yaml`
    and `adk-engineer/`.

Not opened: `references/runtime-and-delivery.md`. Its trigger (browser
streams, context limits, concurrency, release continuity) did not apply,
because phase 1 is non-streaming request/response at low load. No official
web documentation was fetched, because network access was not allowed.

## 2. Questions I would have asked, and the answers I assumed

These are also the *Assumed answers* table in the design (A1–A13).

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | Deadline, and is it continued? | 10 working days, then continued |
| A2 | Focused hours per developer, and ADK/GCP familiarity? | About 5 h a day each. New to ADK (×1.5), have used GCP |
| A3 | Money for models and cloud? | About US$300 a month during the pilot |
| A4 | Who uses it, and in which language? | Signed-in salon customers, in English |
| A5 | Can our service verify the booking site's customer token? | Yes (a JWT or an introspection endpoint). This is the first step of G04 |
| A6 | Does the booking API have staging, idempotency keys and an atomic reschedule? | Staging yes. The other two are unknown, and G01 settles them |
| A7 | Cancel and move window, booking lead time? | 24 h and 2 h, signed off by the salon owner (W1) |
| A8 | Channel? | A web widget on the existing booking site |
| A9 | All five salons at once, or a pilot? | One pilot salon in phase 1 |
| A10 | Existing GCP project or database to reuse? | The GCP project exists. There is no reusable Postgres, so a new small Cloud SQL |
| A11 | Retention and privacy notice? | 30 days. The notice is updated before go-live (W1) |
| A12 | Payments or deposits? | None |
| A13 | Who operates it after launch? | The three developers, in business hours |
| — | Confirm the cut line (G01–G11 now, G12–G17 later)? | Assumed confirmed |
| — | High end of the finish range is about one hour over: 6 h a day for Dev A, or a day-11 launch? | Left open in the plan summary |

## 3. Files written or changed, and what was not finished

Written (all new):

- `docs/architecture/salon-booking-assistant.md`: the design, marked draft.
  It has assumed answers, profile and depth, invariants I1–I6, decisions
  D1–D12, model-facing contracts, data and authority, security posture,
  failure table and open decisions.
- `docs/plans/salon-booking-assistant.md`: the summary, capacity, load table,
  yaml schedule block (W1, G01–G17), schedule check result, a table of
  changes after failing runs, the cut line, implementation map, goals table,
  phase 2 outline, later list and *Resume here*.
- `docs/tickets/salon-booking-assistant/G01…G11-*.md`: 11 phase 1 tickets with
  owners. Dev A: G01, G03, G07, G11. Dev B: G02, G06, G08, G09. Dev C: G04,
  G05, G10.
- `REPORT.md`, this file.

Temporary: I wrote a `.whatif/` scratch directory for schedule what-ifs and
then deleted it. Running pytest created
`.claude/skills/adk-system-designer/tests/__pycache__/`, which I also
deleted.

Not finished:

- No design conversation took place. Every decision is provisional and no
  answer came from the user.
- No provider facts were checked live. Prices, Cloud SQL cost, Vertex
  availability of `gemini-3.8-flash` and ADK 2.8.0 APIs come from the
  bundled snapshot only.
- **The schedule does not fully fit**: the high end is 10.13 days against 10.
- **Over the reading budget.** Design plus plan is about 5,000 words by `wc`,
  against about 4,000. Tickets are about 210–290 words each, against about
  150 (the `wc` count includes front matter and the run-prompt block).
- No phase 2 tickets were written, as the skill intends.
- No code, scaffolding or cloud work was done (design only).

## 4. Checks run and not run

Run:

| Check | Result |
| --- | --- |
| `check_schedule.py --plan … --tickets … --days 10 --reserve 0.25 --person "Dev A=5" "Dev B=5" "Dev C=5"` (final) | 64–89 h against 112.5 h, fits. Chain G01→G03→G06→G09→G11, 6.4–8.8 days. Finish 7.47–10.13 days. Calendar: **low end only, exit 1**. No plan/ticket mismatches |
| Same command with `Dev A=6` | Finish 6.44–9.02, fits, **exit 0** |
| First draft (8 goals) | 10.93–15.73 days, exit 1. Fixed by the changes listed in the plan's change table |
| About 18 what-if variants (owners, splits, cuts) | Results are in the plan's change table and the rejected what-ifs line |
| An earlier ticket run | 2 mismatches (`calendar_waits` text on G01 and G11). Fixed, then re-run clean |
| `--phase 2` | 27–50 h |
| `python3 -I -m pytest .claude/skills/adk-system-designer/tests/` | 10 passed |

All of these ran on Python 3.9.13. The skill names 3.11+, but the helper ran
without error.

Not run:

- Every test named in the tickets: none exist yet, and google-adk is not
  installed.
- Any import of `google.adk`.
- Live model calls, staging booking API calls and Cloud deployment (not
  allowed in this session).
- Lookups of official documentation (no network).

## 5. Friction log

- **Unsure: hours per person to pass `--person`.**
  `delivery-profiles.md:178` says to give "full focused hours per day", while
  the capacity section (`delivery-profiles.md:213`) talks about a focus
  factor. I passed 5 h (already focused) and the 0.25 reserve. It is not clear
  whether a focus factor should also be applied before passing the figure.
- **Unsure: which remedies are legitimate.** `delivery-profiles.md:190` says
  "Do not remove a dependency ... to make the numbers fit". I removed three
  dependencies (G04 on G02, G08 on W1, G07 on G04) by restructuring the work:
  a stub agent, labels computed from config, and infra separated from the
  gateway. I recorded each change with its reason in the plan, but the line
  between "true of the work" and "gaming the numbers" is a judgment call that
  the reference does not illustrate.
- **Heavier than needed: the what-if loop.** `delivery-profiles.md:196-201`
  ("Run every remedy ... as a what-if") took about 18 helper runs, through a
  generator script I had to write myself. A `--what-if` or owner-override
  flag in `scripts/check_schedule.py` would have saved most of that.
- **Surprising helper behaviour.** The greedy list scheduler
  (`scripts/check_schedule.py:232`, `max(ready, key=remaining)`) ignores
  start times. Some cuts therefore made the finish *later*: cutting G08 moved
  it from 10.13 to 10.4. Quoting those figures is honest, but they are
  scheduling artefacts.
- **Tension: where goal content lives.** `delivery-profiles.md:157` says each
  ticket "copies its goal's figures and acceptance cases but links to the
  plan for the route". `delivery-profiles.md:292-298` says the ticket is the
  single home of scope, route and acceptance when tickets exist. I followed
  the second.
- **Budget pressure.** The reading budget (`SKILL.md:87`,
  `delivery-profiles.md:307`) of 4,000 words is hard to meet for an MVP with
  writes. The failure and invariant tables alone are long. I kept them, as
  `delivery-profiles.md:311-313` directs, and went over.
- **Unsure: Python version.** `delivery-profiles.md:206` says to report "not
  checked" when Python 3.11+ is missing. The helper ran fine on 3.9.13, so I
  reported the run along with the version.
- **Unsure: wait entries.** It was unclear whether W1 should also appear in
  `blocked_by` of tickets that need it. The helper compares `blocked_by` sets
  (`scripts/check_schedule.py:262`), so I added it on G11 only.
- **Genuinely helpful:**
  - The headless rule (`SKILL.md:125-127`) gave a clear output shape.
  - The model lifecycle snapshot (`SKILL.md:203`) steered me off
    `gemini-3.6-flash` and `gemini-3.7-flash`, which retire on Vertex on
    2026-11-19 and 2027-01-28.
  - The floor list (`delivery-profiles.md:76-86`) and the "three people, two
    weeks, orders" example (`delivery-profiles.md:334-337`) mapped directly
    onto the confirm-in-code design (D2).
  - The helper caught real ticket/plan mismatches.
  - The trifecta check (`design-decisions.md:182-195`) justified removing the
    agent's write leg.

## 6. Next prompt the skills told the user to type

From `SKILL.md:276-285` (closing message) and `assets/ticket-template.md:51-56`,
as written in the plan's *Resume here* and the G01 ticket:

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract.md. Read its design and plan, use its primary and supporting skills, run its verification locally, fill in the Evidence section and set status. Leave changes uncommitted.
```

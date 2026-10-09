# Session report: salon booking assistant design

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer` (invoked by the user's `/adk-system-designer`; SKILL.md loaded with it).
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md`
3. `.claude/skills/adk-system-designer/scripts/check_schedule.py` (read to learn the input format)
4. `.claude/skills/adk-system-designer/references/design-decisions.md`
5. `.claude/skills/adk-system-designer/references/failure-review.md`
6. `.claude/skills/adk-system-designer/references/implementation-handoff.md`
7. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
8. `.claude/skills/adk-system-designer/assets/ticket-template.md`
9. `.claude/skills/adk-system-designer/assets/system-design-template.md`
10. `.claude/skills/adk-system-designer/references/gcp-decisions.md`
11. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
12. Grep for version lines across `.claude/skills/adk-*/references/compatibility.md`; the first 12 lines of `safe-api-tool-calls/references/compatibility.md` and `adk-operational-guardrails/references/compatibility.md`
13. `.claude/skills/adk-engineer/SKILL.md`, lines 1–60 (to confirm how tickets are picked up)
14. A grep of `.claude/skills/adk-system-designer/tests/test_check_schedule.py` imports (to decide whether it could run)

Not opened: `references/runtime-and-delivery.md`. Its trigger (context limits, downloads, browser streams, release continuity) did not apply to phase 1: there is no streaming, and a release is a Cloud Run revision with rollback. No other skill was invoked; the specialists are only named in the plan.

## 2. Questions I would have asked, and the answers I assumed

These are also the **Assumed answers** table at the top of the design (A1–A10).

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | Who uses the assistant: salon customers, or front-desk staff? | Customers, in a chat widget on the existing booking website |
| A2 | How do customers sign in today? Can our backend verify that token? | Yes. The existing site issues a JWT (with JWKS) that carries the booking API customer ID |
| A3 | How many hours a day can each of the three developers give this? How well do they know ADK and GCP? | Full time for 10 working days: 6 available h/day at focus 0.6, so 3.6 h/day each. New to ADK (estimates ×1.5), comfortable with GCP, one existing GCP project |
| A4 | What can you spend on models and cloud? | About US$300 a month, on Vertex AI |
| A5 | Does the booking API have staging? Reschedule? Idempotency keys? Lookup by client reference? Which business rules does it enforce? | Staging, reschedule and rule enforcement: yes. Idempotency and lookup: unknown, so G01 finds out and the design falls back to lookup-before-retry |
| A6 | Which channels and languages? | Web only, English only |
| A7 | Payments or deposits? Several services in one booking? | No payments or deposits; one service per appointment, optional stylist |
| A8 | Who notifies the customer about a change? | The booking API already does; the assistant has no egress |
| A9 | Launch audience: one salon or all five? Replace the existing form or sit beside it? | All five salons, behind a beta link; the existing form stays as the fallback |
| A10 | Region, data protection, retention? | Same region as the booking API; sessions kept 30 days, proposals 90 days |
| — | Do you accept the delivery profile? | MVP / pilot |
| — | Do you confirm the cut line (G01–G09 now, G10–G14 later, fallback cuts at a day-6 checkpoint)? | Assumed accepted, and marked "please confirm" in the plan |
| — | Who takes which goal? | Roles Dev A, Dev B and Dev C, described by skills because the developers' names are unknown |

## 3. Files written or changed, and what was not finished

Written (all new, uncommitted):

- `docs/architecture/salon-booking-assistant.md`: the design, status **draft**. It has the assumed-answers table, scope gate, depth per concern, floor, invariants I1–I5, decisions D1–D6, model-facing contracts, data and authority, security posture, budgets, the failure table and open decisions.
- `docs/plans/salon-booking-assistant.md`: the plan. It has the profile and capacity, the load table, who could take which goal, the `yaml` schedule block (phase 1 and phase 2), the schedule-check output, the cut line, the implementation map, full G01–G09 entries, coarse G10–G14, the Later table, open decisions and Resume here.
- `docs/tickets/salon-booking-assistant/G01-…G09-*.md`: nine phase-1 tickets, built from the ticket template.
- `REPORT.md`: this file.

Deleted again: a trial `/tmp/h4sched/plan.md`. I wrote it outside the working directory by mistake, which broke the session rule, and removed it straight away. Also deleted: `.claude/skills/adk-system-designer/scripts/__pycache__/`, created when I imported the helper.

Not finished or not possible here:

- No user confirmation of anything. Every product decision is provisional.
- Provider facts are unverified: Vertex AI availability of `gemini-3.8-flash` in the chosen region, current prices, and the `google-adk` pin (2.8.0 is a working assumption). No network was allowed; G02 carries these checks.
- The design is about 3,300 words, slightly above "two to four pages". The plan is about 4,600 words.
- At the high end, phase 1 overruns the 10-day calendar by about 0.6 days unless the two pre-agreed mitigations are applied (see section 4).

## 4. Checks run and results; checks not run

Run, with `/opt/homebrew/bin/python3.11 -I`. The default `python3` is 3.9.13, below the 3.11 the reference asks for.

- `check_schedule.py --plan docs/plans/salon-booking-assistant.md --tickets docs/tickets/salon-booking-assistant/ --capacity 81 --days 10 --person "Dev A=3.6" --person "Dev B=3.6" --person "Dev C=3.6"` → **exit 1**:
  - Phase 1 is 44.5–74 h against 81 h capacity; fits capacity: yes.
  - Loads: A 15.5–26.5 h, B 13.5–21.5 h, C 15.5–26 h, each of 36 h available.
  - Longest chain: G04→G07→G08→G09, 5.14–9.61 days.
  - Finish range: 5.83–10.58 working days; fits the calendar at the **low end only**.
  - No ticket/plan mismatches remain. Earlier runs flagged two `calendar_waits` text mismatches and an 11.97–12.25-day finish; I fixed both by changing the plan.
- `check_schedule.py --plan … --phase 2` → exit 0: 19–36 h. Its finish figure is meaningless because no owners were assigned.
- Ad-hoc use of the helper's `analyse()` function: I tried all 3⁹ owner assignments. The best high-end finish is 10.58 days, and the chosen split is one of the best. A scenario run showed that pre-booking the walkthrough plus cutting `propose_move` gives 43–71.5 h and a 5.42–9.81-day finish, which fits. That is recorded in the plan as the day-6 fallback.

Not run:

- `.claude/skills/adk-system-designer/tests/test_check_schedule.py`: pytest is not installed. Running it with `unittest` would create temp files outside the working directory, so I skipped it.
- No application tests: there is no application code, and `google-adk` is not installed. Every acceptance check in the tickets is planned, not run.
- No cloud, network or price checks (not allowed).

## 5. Friction log

- **Helpful:** `SKILL.md:123` (Assumed answers when the user can't reply) settled at once how to run headless, despite the interview-first guidance at `SKILL.md:48-54`.
- **Helpful:** `SKILL.md:93` and `references/delivery-profiles.md:157-174` (use the helper, not your head). The helper caught a calendar overrun I would have missed: the hours fit comfortably, but the finish date did not. It also caught text drift between tickets and the plan.
- **Unsure:** what to do when no owner assignment fits the calendar. `delivery-profiles.md:188-197` says to cut scope and name the goals that move. But the helper only evaluates the assignment it is given, so I had to import `analyse()` and brute-force assignments myself. That was heavier than it should be, and importing left a `__pycache__` inside the skill directory.
- **Unsure:** how the reserve applies to the calendar. `delivery-profiles.md:162-166` passes `--capacity <hours after reserve>`, but `--person` rates are full focused rates. So the calendar check consumes the reserve, while the hours check keeps it back. I used full 3.6 h/day rates and said so.
- **Unsure:** the focus factor for full-time startup developers. `delivery-profiles.md:180-182` gives 0.6 for part-time or interrupted work and 0.8 for a single dedicated block, with nothing for a full-time fortnight. I used 0.6 on 6 h.
- **Friction:** `scripts/check_schedule.py:255` compares `calendar_waits` free text exactly between plan and ticket. Wording a wait slightly differently in a ticket counts as a "problem". Separately, `assets/ticket-template.md:11-15` has no `wait_days`, so tickets cannot carry the number the plan uses.
- **Friction:** `references/delivery-profiles.md:173` requires Python 3.11+, but the script's standard-library code appears to need nothing newer. The default `python3` here was 3.9, so I had to find 3.11.
- **Friction:** phase-2 output from the helper reports a finish range for unassigned goals at the default 6 h/day (`check_schedule.py:302-303`), which reads as a real schedule.
- **Heavier than needed:** the plan template's per-goal entry (`assets/implementation-plan-template.md:72-95`, 14 fields), plus one ticket per goal (`SKILL.md:262-265`), duplicates every phase-1 goal. For an MVP plan with nine goals, that pushed the plan to about 4,600 words, beyond `SKILL.md:85` "two to four pages".
- **Unsure:** which ADK version to name. `SKILL.md:194-198` says each specialist's `compatibility.md` names it, but the specialists differ: observability pins 2.8.0, instructions covers 2.7.0–2.11.0. I chose 2.8.0, which several of them record as their tested baseline.
- **Helpful:** `SKILL.md:198-202` and `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` steered me off `gemini-3.6-flash` (Vertex retirement 2026-11-19), which retires inside the plan horizon.
- **Mild deviation:** `delivery-profiles.md:63` says MVP release engineering means "Build: evaluation in CI". I kept a hand-run evaluation in phase 1 and moved CI to phase 2 (G10) to fit the calendar, and recorded that with its trigger in the design.

## 6. Exact next prompt the skills told the user to type

The skill (`SKILL.md:277-281`, and the plan's "Resume here") gives the user this:

```text
/adk-engineer Carry out G01 from docs/plans/salon-booking-assistant.md.
```

Each ticket also ends with its own prompt. For example, the one for G01 is:

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-client.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

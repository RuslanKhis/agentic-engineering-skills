# REPORT: salon booking assistant design session (2026-10-14)

## 1. Skills invoked and reference files opened, in order

Skill invoked: `adk-system-designer`, by the user's `/adk-system-designer`.
No other skill was invoked. Some files of two sibling skills were read
directly because the designer told me to read them.

1. `.claude/skills/adk-system-designer/SKILL.md` (loaded by the invocation)
2. `adk-system-designer/references/delivery-profiles.md` (in full)
3. `adk-system-designer/references/design-decisions.md` (in full)
4. `adk-system-designer/references/failure-review.md` (in full)
5. `adk-system-designer/references/implementation-handoff.md` (in full)
6. `adk-system-designer/references/gcp-decisions.md` (in full)
7. `adk-system-designer/assets/system-design-template.md`
8. `adk-system-designer/assets/implementation-plan-template.md`
9. `adk-system-designer/assets/ticket-template.md`
10. `adk-system-designer/scripts/check_schedule.py` (read, then run)
11. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
12. `adk-model-and-output-contracts/references/compatibility.md` (first 40 lines)
13. `safe-api-tool-calls/references/compatibility.md` and `safe-api-tool-calls/SKILL.md` (grep only)
14. `adk-system-designer/tests/test_check_schedule.py` (imports only, then run)

Not opened: `references/runtime-and-delivery.md`. I judged its trigger
(SKILL.md:184) not met: there are no streaming, context-limit or release
continuity requirements in phase 1.

## 2. Questions I would have asked, with the answers I assumed

The canonical list, with the decisions that depend on each answer, is in the
**Assumed answers** table of `docs/architecture/salon-booking-assistant.md`.

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | Deadline, and what happens after it? | 10 working days; the work continues afterwards |
| A2 | People, hours and experience? | 3 developers, about 5 focused h/day each; good with Python and GCP, new to ADK (×1.5 on estimates) |
| A3 | Budget for model and cloud? | ≤ USD 300/month during the pilot |
| A4 | Users, and who judges the result? | Signed-in salon customers; the chain owner judges the pilot |
| A5 | Data and effects? | Personal data; real appointment create, move and cancel; no payments |
| A6 | Channel? | A chat widget in the existing booking web app |
| A7 | Customer identity? | The booking app issues a token the backend can verify, carrying `customer_id` |
| A8 | Booking API capabilities? | The team owns it: availability, create, atomic reschedule, cancel, list-mine, a staging environment, and an `Idempotency-Key` (or the team adds one) |
| A9 | Cancellation fees? | Enforced by the API; the assistant moves no money |
| A10 | Language? | English only |
| A11 | Rollout? | Pilot salon first, then all five within phase 1 |
| A12 | GCP setup and region? | Existing organisation, a new project in the booking API's region, Vertex AI allowed |
| A13 | Chat retention? | 30 days |
| — | Profile correction (SKILL.md asks the user to confirm the profile) | MVP or pilot |
| — | Cut line, and the remedy for the calendar slip | Unconfirmed; options are recorded in the plan |
| — | Who approves go-live, and who is on duty for uncertain operations | Unknown; recorded as open decisions |
| — | Pass bar for the evaluation (G08) | ≥ 27 of 30 cases on 2 runs, provisional |

## 3. Files written or changed, and what is unfinished

Written (all new; nothing existing was changed):

- `docs/architecture/salon-booking-assistant.md`: the design. Status draft.
  Contains assumed answers, depth and floor, invariants I1–I6, decisions
  D1–D7, data and authority, security posture, failure table and open
  decisions.
- `docs/plans/salon-booking-assistant.md`: summary, capacity, owners, the
  yaml schedule block, the schedule result, a what-if table, a change log,
  the cut line, the implementation map, goals G01–G10, phase 2 G11–G16, a
  Later list, and where to resume.
- `docs/tickets/salon-booking-assistant/G01…G10-*.md`: 10 phase 1 tickets.
  Owners: Dev A takes G01, G03, G04, G10; Dev B takes G02, G07, G08; Dev C
  takes G05, G06, G09.
- `REPORT.md` (this file).

A scratch `.whatif/` directory was created for the schedule what-ifs and then
deleted.

Not finished, or not met:

- **Phase 1 fits the calendar only at the low end.** The finish is 6.93–11.93
  working days against 10. Two tested remedies fit: 12 working days, or a
  pilot-salon-only launch with everyone at 6 h/day. The user has to choose.
- Every product answer is assumed. The design stays **draft**, and the user
  has not confirmed the profile or the cut line.
- Provider facts were not checked live. Prices, the region, the availability
  of `gemini-3.8-flash` in that region (the lifecycle file was checked on
  2026-10-08), the ADK 2.8.0 pin, and the known limitations of native
  confirmation are verification items in G01 and G09.
- Over the length budgets. Design plus plan is about 4,950 words by `wc`,
  including roughly 350 words of yaml, against about 4,000
  (delivery-profiles.md:298). Tickets are about 245 words each excluding
  front matter, against about 150 (delivery-profiles.md:299). I did not trim
  them further.
- No code, no scaffolding, no dependency changes (the request was design only).

## 4. Checks run and not run

Run:

| Check | Result |
| --- | --- |
| `python3.11 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/salon-booking-assistant.md --tickets docs/tickets/salon-booking-assistant/ --days 10 --reserve 0.25 --person "Dev A=5" --person "Dev B=5" --person "Dev C=5"` | 57–90 h. Hours fit: yes (112.5 h). Chain G01→G03→G04→G10 is 5.6–9.8 days. Finish 6.93–11.93 days. Calendar: **low end only**. **Exit 1.** No plan/ticket mismatches reported |
| 14 what-if runs while shaping the plan, then 8 against the final plan | The final figures are quoted in the plan's what-if table; all re-run against the final file |
| `python3.11 -m unittest tests.test_check_schedule` (in the skill directory) | 10 tests OK |
| Relative-link check over design, plan and tickets (`design:`/`plan:` front matter and `](../…)` links) | No broken links |

Not run:

- No application tests exist. Any test importing `google.adk` could not run
  here, because it is not installed. All ticket verifications are planned,
  not executed.
- `pytest` is not installed, so the checker tests ran under `unittest`.
- No network or cloud lookups (forbidden this session). Prices, regions,
  current ADK docs and model availability are unverified.
- The default `python3` is 3.9.13. The checker was run with `python3.11`, as
  delivery-profiles.md:201 advises.

## 5. Friction log

**Unsure what to do**

- SKILL.md:73–74 and :96–98 (let the user correct the profile, confirm the
  cut line) conflict with a headless run. SKILL.md:124–128 resolves this:
  use an Assumed answers table and mark decisions provisional. That worked,
  but the cut-line confirmation has no headless equivalent, so I recorded it
  as an open decision.
- delivery-profiles.md:181–182 says "fix the plan or the cut line until the
  result is what you tell the user". delivery-profiles.md:216–218 says "if
  only the low end fits, say so and name the goals that move". I could not
  tell whether a final exit status of 1 ("low end only") is an acceptable
  deliverable. I kept it and reported it honestly, with remedies tested as
  what-ifs.
- Calendar waits: delivery-profiles.md:186–188 says to request a wait on day
  one. But `check_schedule.py:239` always appends `wait_days` after the
  goal's work. A go-live approval requested in G01 is therefore still
  modelled as a wait at the end of G10. I left it at 0–1 day on G10.
- Ticket length: delivery-profiles.md:270 says about 120 words (compact
  form) and :299 says about 150. Neither counts the mandatory front matter
  and run prompt explicitly.
- Run prompt form: SKILL.md:282 gives `/adk-engineer Carry out G01 from
  docs/plans/<topic>.md.`, while assets/ticket-template.md:54 gives
  `/adk-engineer Carry out <path to this ticket>…`. I used the ticket form,
  because tickets were requested.
- Primary skill for the agent goal (G02): implementation-handoff.md:21 maps
  orchestration to `adk-workflow-design`, but the work is mostly tool
  declarations (:23). I chose `adk-tool-interface-design` with workflow-design
  as supporting.
- `$SKILL_DIR` in delivery-profiles.md:168 is not defined anywhere, so I
  substituted the path by hand. The default `python3` is 3.9 here, and the
  3.11 requirement only appears at :201.

**Heavier than needed**

- Finding the schedule bottleneck took about 20 helper runs plus hand
  arithmetic. `check_schedule.py:229–241` reports the finish but neither
  per-goal start and finish nor which person's queue binds. Here the binding
  constraint was Dev C's queue, not the dependent chain; I found that only by
  hand.
- The greedy order in `check_schedule.py:232` made one owner move look much
  worse than the work warrants (11.67 → 14.07 days when the deploy goal moved
  to Dev B).
- assets/system-design-template.md has 10 sections. For an MVP I trimmed it
  to fit, guided by SKILL.md:84–91, but that left the design about 20% over
  the reading budget.

**Genuinely helpful**

- SKILL.md:124–128 (Assumed answers table): a clear rule for headless runs.
- SKILL.md:201–205 and the lifecycle JSON: they steered the design away from
  `gemini-2.5-flash` (Vertex retirement 2026-10-20) and `gemini-3.6-flash`
  (2026-11-19), both inside the plan's horizon.
- delivery-profiles.md:70–92 (the floor) and :324–327 (MVP example with
  orders): these led directly to D3, the propose/confirm split that keeps
  writes out of the model's reach.
- delivery-profiles.md:184–196 (only cuts that are true of the work, and
  what-ifs for every remedy): this produced honest splits (G03/G04,
  G07/G08) instead of shaved estimates. It also caught that "6 h/day for
  everyone" alone does not close the gap.
- delivery-profiles.md:200–201 (handoff hours go to the receiving goal) and
  implementation-handoff.md:49–50 (the first shared-environment goal gets
  observability and release engineering): both were applied.
- The `check_schedule.py --tickets` comparison confirmed the ten tickets
  match the plan with no drift.

## 6. Next prompt the skills told the user to type

The skill's prescribed form (SKILL.md:282), quoted verbatim:

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
```

Instantiated in the plan and the G01 ticket, following the ticket template:

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract.md.
```

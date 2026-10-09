# REPORT: salon booking assistant design session (2026-10-09)

## 1. Skills invoked and reference files opened, in order

1. Skill invoked: `adk-system-designer` (via `/adk-system-designer`). No other
   skill was invoked; this was design only.
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md`
3. `.claude/skills/adk-system-designer/references/design-decisions.md`
4. `.claude/skills/adk-system-designer/references/failure-review.md`
5. `.claude/skills/adk-system-designer/references/implementation-handoff.md`
6. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
7. `.claude/skills/adk-system-designer/assets/ticket-template.md`
8. `.claude/skills/adk-system-designer/assets/system-design-template.md`
9. `.claude/skills/adk-system-designer/references/gcp-decisions.md`
10. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`.
    SKILL.md says to choose the model from this file.
11. `.claude/skills/adk-model-and-output-contracts/references/compatibility.md`
    (grep only). I needed the ADK version for the greenfield working assumption.
12. `.claude/skills/safe-api-tool-calls/references/compatibility.md` (grep
    only). It gave no single version.
13. `.claude/skills/adk-system-designer/references/runtime-and-delivery.md`.
    Its trigger applies here: concurrent sessions, a browser contract and
    release continuity.

## 2. Questions I would have asked, and the answers I assumed

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | When do the two weeks start, and is the code kept? | Start Mon 2026-10-12, launch Fri 2026-10-23. The code is kept and continued. |
| A2 | How many hours can each developer give, and how familiar is each with ADK and GCP? | About 7 h/day each for 10 days. Strong in Python and in the booking API. New to ADK, some GCP. |
| A3 | What is the model and cloud budget? | About US$300 a month. |
| A4 | Who uses it? | Salon customers, through a web chat widget on the existing site. Staff do not use it in phase 1. |
| A5 | What data does it touch, and what can it change? | Real customer personal data and real booking writes. No payments or deposits. |
| A6 | How are customers authenticated today? | The existing website login, whose session the backend can verify server-side. |
| A7 | What does the booking API support (staging environment, reschedule, idempotency keys, lookup)? | It has a staging environment and supports create, cancel and list. Reschedule and idempotency support are unknown, and G00 settles them. |
| A8 | Does a GCP project exist, and can it reach the API? | Yes. |
| A9 | Who enforces business rules such as cancellation windows and stylist skills? | The booking API. |
| A10 | Which languages and time zones? | English only, one time zone. |
| A11 | Is there a handoff to a human? | Phase 1 shows the salon phone number. |
| A12 | How long are transcripts kept? | 30 days. |
| A13 | Who responds to incidents and uncertain bookings? | The developers in business hours. The front desk resolves uncertain bookings. |
| — | Launch at all five salons at once, or one first? | One salon first is recommended. This is recorded as an open decision. |
| — | Will payments or cancellation fees ever go through the chat? | No. If they do, it is a later item. |
| — | Which names go to Dev A, B and C? | I used role profiles (booking-API expert, agent/Python, web/infra) instead of names. |

Each assumption also appears in the **Assumed answers** table at the top of the
design. The decisions that depend on an assumption are marked provisional.

## 3. Files written or changed, and what was not finished

Written. No existing file was changed.

- `docs/architecture/salon-booking-assistant.md`: the design. Status is draft.
  It covers the assumed answers, journey, profile and depth, the floor,
  capacity and cut line, invariants I1 to I5, decisions D1 to D10,
  model-facing contracts, data and security tables, budgets, the failure
  table and open decisions.
- `docs/plans/salon-booking-assistant.md`: the plan. It covers the proposed
  layout, the capacity check, **who could take which** with a calendar, the
  implementation map, G00 to G07 in full, phase 2 (G08 to G12), the later
  list, and where to resume.
- `docs/tickets/salon-booking-assistant/G00` to `G07` (8 files), one per phase
  1 goal. Each has a `suggested_owner` field.
- `REPORT.md`: this file.

Not finished or not verified:

- No design decision has been accepted by the user.
- No provider facts were looked up, because network access was not allowed:
  - Vertex region availability of `gemini-3.8-flash`;
  - model price;
  - ADK 2.8.0 constructor names.

  These are recorded as G01 and G07 checks.
- The cost figure is symbolic, with no dated price.
- The design is longer than the skill's size target for an MVP; see the
  friction log.
- G01 and G03 are not fully independent. The G03 ticket is marked ready
  (`blocked_by: []`), but it builds on G01's agent wiring. The plan says the
  two can run in parallel, with G03 using a stub until G01 lands.

## 4. Checks run, and checks not run

Run, with results:

- Each ticket's `primary_skill` exists under `.claude/skills/`: 8 of 8 ok.
- Each skill name mentioned anywhere in `docs/` exists under `.claude/skills/`:
  no missing names reported.
- Each ticket's `design:` and `plan:` relative links resolve: 16 of 16 ok.
- The plan's link to the design resolves: ok.
- The phase 1 estimate sum was checked by hand: low 65 h, high 94 h, against
  96 h of capacity after the reserve. I first wrote "66" in the design and
  corrected it to 65.

Not run:

- Every test named in the tickets (pytest, `adk eval`, `adk web`). No
  application code exists, and google-adk is not installed, so tests that
  import `google.adk` cannot run here.
- Every network, cloud or live-model check, because the session rules
  forbade them.
- A Markdown lint, because no linter is installed.

## 5. Friction log

- **Unsure: how much of the conversation protocol applies headless.** The
  skill says to ask the scope gate and wait for answers. It also says "Let the
  user answer before treating a material product choice as settled". The
  headless escape at `.claude/skills/adk-system-designer/SKILL.md:119-122`
  (Assumed answers table, decisions marked provisional) settled it cleanly.
  This was genuinely helpful.
- **Unsure: how long the MVP design should be.** The guidance says "roughly two
  to four pages" (`SKILL.md:84-86`) and "two to four pages per phase"
  (`references/delivery-profiles.md:36`). The system-design template
  (`assets/system-design-template.md`) has 10 or more sections, and
  `references/design-decisions.md` plus `references/failure-review.md` add
  many concerns. My design came out at about 3,650 words, roughly 7 pages,
  which is **heavier than the guidance**. Nothing tells you which template
  sections to drop at the MVP size; only the POC has a compact form
  (`references/delivery-profiles.md:144-166`).
- **Heavier than needed: the reading load.** Eight or more reference and
  template files, about 1,260 lines, before writing a two-week MVP plan.
  `design-decisions.md:126-260` (RAG, delegated OAuth, revocation races,
  event-driven updates) was mostly irrelevant here, but it is a single
  required read (`SKILL.md:92-93`). A per-section "read only if" index at the
  top of `design-decisions.md` would save time.
- **Unsure: ticket for a blocked goal.** `SKILL.md:266-267` and
  `references/implementation-handoff.md:109-112` say "one file per **ready**
  goal". The user asked for tickets for all phase 1 goals, so I also wrote
  tickets for blocked goals (G02, G05, G06, G07), with `status: blocked` and
  `blocked_by`. The ticket template (`assets/ticket-template.md:12`) hardcodes
  `status: ready`, so a blocked ticket was not anticipated.
- **Unsure: where "who could take which" goes.** The ticket template's
  frontmatter (`assets/ticket-template.md:1-13`) and the plan template have
  no owner or assignee field, and the skill never addresses assigning people
  to goals. I added a `suggested_owner` field and a "Who could take which"
  table in the plan.
- **Unsure: MVP default versus capacity for observability.**
  `references/delivery-profiles.md:62` says an MVP builds "traces and token
  cost". Fitting capacity pushed traces to phase 2. I recorded this as a
  deviation below the default, with a trigger. The skill allows cutting scope
  but not the floor (`references/delivery-profiles.md:117`), and it is
  ambiguous whether MVP-depth items count as floor.
- **Genuinely helpful: model choice from data.** The direction at
  `SKILL.md:197-202` to choose the model from the dated lifecycle file
  steered me away from `gemini-3.6-flash`, whose Vertex retirement on
  2026-11-19 falls inside the plan, and from the 2.5 models (2026-10-20). I
  would not have known those dates from memory.
- **Genuinely helpful: concrete MVP example.** The example "Three people, two
  weeks to an MVP" at `references/delivery-profiles.md:187-190` matched this
  case almost exactly and confirmed that idempotent writes and confirmation
  belong in phase 1.
- **Genuinely helpful: the failure-scenario table.** The table at
  `references/failure-review.md:23-43` produced the lost-reply, double-click
  and partial-move rows directly. Those rows drove D3.
- **Genuinely helpful: capacity formula and cut line.** The formula and
  cut-line wording at `references/delivery-profiles.md:104-121` made the
  capacity check mechanical.
- **Minor: conflicting run-prompt forms.** The run prompt for a goal appears
  in two forms. The plan template uses "Carry out <goal ID> from <plan>"
  (`assets/implementation-plan-template.md:67`), and the ticket template uses
  "Carry out <path to this ticket>" (`assets/ticket-template.md:48`). I used
  the ticket-path form in the plan goals, because tickets exist, and the
  goal-ID form for the closing prompt, following `SKILL.md:275-277`.
- **Not used: Matt Pocock workflow section.**
  `references/implementation-handoff.md:114-140` was skipped as instructed,
  because no workflow was chosen.

## 6. The exact next prompt the skills told the user to type

From the closing-message instruction (`SKILL.md:270-277`), filled in for this
plan:

```text
/adk-engineer Carry out G00 from docs/plans/salon-booking-assistant.md.
```

G01 (Dev B) and the G04 skeleton (Dev C) can start in parallel. Each ticket's
own prompt is at the end of its file, for example:

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-agent-reads-availability.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

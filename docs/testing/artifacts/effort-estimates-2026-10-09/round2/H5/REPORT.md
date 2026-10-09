# Report: home-insurance claim intake agent design session (2026-10-09)

## 1. Skills invoked and reference files opened, in order

Skills invoked: **`adk-system-designer`**, the only one, through the user's
slash command. No other skill was invoked. Specialist skills are named in the
plan for later goals, but their guidance was not loaded or applied beyond the
files listed below.

Files opened, in order:
1. `.claude/skills/adk-system-designer/SKILL.md` (loaded by the invocation)
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md` (full)
3. `.claude/skills/adk-system-designer/references/design-decisions.md` (full)
4. `.claude/skills/adk-system-designer/references/failure-review.md` (full)
5. `.claude/skills/adk-system-designer/references/gcp-decisions.md` (full)
6. `.claude/skills/adk-system-designer/references/implementation-handoff.md` (full)
7. `.claude/skills/adk-system-designer/references/runtime-and-delivery.md` (full)
8. `.claude/skills/adk-system-designer/assets/system-design-template.md`
9. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
10. `.claude/skills/adk-system-designer/assets/ticket-template.md`
11. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (full)
12. The first 25 lines of `references/compatibility.md` in `adk-agent-evaluation`,
    `adk-agent-instructions`, `adk-agent-interoperability`, `adk-agent-observability`,
    `adk-agent-security` and `adk-frontend-integration`. Output was cut at 150
    lines, so I did not see the other specialists' compatibility files.
13. `.claude/skills/adk-model-and-output-contracts/references/model-selection.md` (grep for judge, region and lifecycle lines only)
14. `.claude/skills/adk-model-and-output-contracts/references/compatibility.md` (first 20 lines)

## 2. Questions I would have asked, and the answers I assumed

These are also recorded as the **Assumed answers** table (A1–A16) at the top of
`docs/architecture/home-claim-intake.md`, with the decisions each one drives.

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | What is the exact GA date, which EU market, and is the service continued after GA? | 2027-03-09, one EU country first, continued with more markets in phase 2 |
| A2 | How many hours does each person have, how familiar are they with ADK and GCP, and how much time does the security reviewer have? | Engineers full time, familiar with Python and GCP, new to ADK (×1.5). ML engineer full time. Security reviewer about 1 day a week (about 100 focused hours) |
| A3 | What budget is there for models and cloud, and is there a target cost per claim? | Enough for three environments and pilot traffic. No numeric target is assumed; G02 prices it |
| A4 | Who uses it, and through which channel? | Signed-in policyholders in the existing customer web portal. No native app at GA |
| A5 | What data does it touch and what can it change? | Personal data and photos. The only external write is creating an FNOL claim plus documents in ClaimCenter. No money moves and no coverage is decided |
| A6 | What is the Guidewire deployment and API, and is a sandbox available? | Guidewire Cloud ClaimCenter with Cloud API. A sandbox tenant can be obtained |
| A7 | What are the residency requirements? | Everything stays in the EU: inference, sessions, photos, logs and backups. The Guidewire tenant is in the EU |
| A8 | Which languages are needed at GA? | The local language plus English |
| A9 | What volumes and storm peaks should we plan for? | About 25 claims per business day, with 10–20× storm peaks. Illustrative only |
| A10 | How long are conversations, drafts and photos retained? | 30 days after submit or abandonment. Guidewire keeps the record of claim |
| A11 | Should the agent pre-check coverage or flag fraud? | No. Adjusters decide |
| A12 | Which claim types are in scope? | Water, storm, fire (after the emergency), accidental damage and theft. Injury, liability and an unsafe home go to a human |
| A13 | Does a fallback channel exist? | Yes: the classic web form and the phone line |
| A14 | What is the AI Act classification? | Not Annex III high-risk. Art. 50 transparency applies. Legal must confirm |
| A15 | What infrastructure-as-code and CI conventions apply? | Terraform, the existing CI system, and projects created by a platform team |
| A16 | How does the customer get the claim number and later updates? | On the confirmation screen, then through existing Guidewire notifications |

The design records further open decisions for the user. These are acceptance
questions rather than scope questions:
- Should I4 (no coverage statements) be accepted as a measured control rather
  than a guarantee?
- Is the cut line agreed?
- Is the profile right? I chose "production service".

## 3. Files written or changed, and what was not finished

Written (all new, uncommitted):
- `docs/architecture/home-claim-intake.md`: the full system design, marked draft.
  It contains the assumed answers, journey, depth table, invariants I1–I10,
  decisions D1–D14, model-facing contracts, data and authority, security
  posture, budgets, the failure table, verification and open decisions.
- `docs/plans/home-claim-intake.md`: the implementation plan. It contains the
  capacity and load tables, critical chain, milestones, cut line,
  implementation map, phase 1 goals G01–G21 in full, phase 2 goals G22–G27,
  the later list, open decisions and the resume prompt.
- `docs/tickets/home-claim-intake/G01-…md` to `G21-…md`: 21 ticket files, one
  per phase 1 goal.
- `REPORT.md`: this file.

Temporary and removed: a `.scratch/` directory inside the working directory. It
held a Python generator that rendered the plan's goal sections and the tickets
from a single data table, so the figures could not drift. I deleted it after
rendering so the plan stays the only source of the figures.

Not finished, or deliberately not done:
- **No implementation.** This was requested.
- **No user review.** Every decision is provisional and the documents are
  marked draft.
- **Provider facts not looked up.** No network was available, so EU region
  availability of `gemini-3.8-flash`, Model Armor and SDP, Guidewire Cloud API
  duplicate-prevention semantics, and prices are all unverified. They are
  assigned to discovery goals G01 and G02.
- **The cost estimate is symbolic.** There is no currency figure.
- **Phase 2 has no tickets.** Its goals are kept coarse on purpose.
- **16 of the 21 tickets are `status: blocked`** by phase 1 dependencies.
  Ready now: G01, G02, G03, G04 and G05.

## 4. Checks run, and checks not run

Run: one local Python consistency check (`python3 -I`, standard library only,
reading the written files rather than the generator).
- All 21 goal sections were found. For each, hands-on plus review equals the
  total. No range's high end is more than twice its low end.
- Phase 1 sums to **872–1,468 h**, which matches the phase table. On the first
  pass the design said 792–1,332 h; I corrected that number, and the check
  then passed.
- Every ticket's `hands_on`, `review_and_verify` and `total` match its plan
  section and the goal table row.
- Every relative link and each ticket's `design:` and `plan:` front-matter path
  resolves.
- Every Gemini model ID mentioned exists in the lifecycle snapshot.
- Every skill named with backticks in the plan exists under `.claude/skills/`.
- The unfilled-placeholder scan flagged `{id}` and `{reason}`. Both are
  intended literals: a route path and a schema field.

Not run:
- Any test that imports `google.adk`. ADK is not installed and no code was written.
- `pytest` of any kind, since there are no tests.
- Terraform, deploys and any cloud command (out of scope).
- Guidewire sandbox calls and live model calls (no network or authorization).
- Web lookups for provider documentation and prices (not allowed).
- Markdown linting (no linter installed, and I did not install one).

## 5. Friction log

**Unsure what to do:**
- `.claude/skills/adk-system-designer/references/delivery-profiles.md:128-140`.
  The starting-point estimates are all small slices of 1–16 h. Nothing anchors
  production-grade goals such as an idempotent multi-step Guidewire write with
  reconciliation, a pentest cycle or a pilot. I extrapolated (G08 at 64–112 h,
  for example), and those figures are guesses a reviewer cannot calibrate.
- `.claude/skills/adk-system-designer/references/delivery-profiles.md:162-164`.
  The focus factor covers part-time people (0.6) and a dedicated block (0.8),
  but not a full-time team over five months. I used 0.6. The result is that
  hours do not bind at all (about 875–1,470 h unallocated), while the calendar
  chain binds at about 19–21 of 21 weeks. The reference reasons mostly in
  hours (lines 170-179) and covers calendar only briefly (lines 153-155), so
  the cut-line logic for a calendar-bound plan was mine.
- `.claude/skills/adk-system-designer/SKILL.md:268-269` and
  `references/implementation-handoff.md:109-111` say to write tickets for
  *ready* goals. The user asked for tickets for all phase 1 goals, and 16 of
  them depend on earlier goals. I wrote all 21 and marked the dependent ones
  `status: blocked` with `blocked_by`. The template only shows `status: ready`
  (`assets/ticket-template.md:17`).
- `.claude/skills/adk-system-designer/references/delivery-profiles.md:142-145`
  says to apply the ×1.5 multiplier to every goal. Discovery and compliance
  goals (G01 Guidewire, G05 DPIA) are not ADK work, and inflating them felt
  wrong. I followed the rule literally and stated it once.
- `.claude/skills/adk-system-designer/SKILL.md:194-199` says to choose the judge
  ID from the lifecycle table. The table has no stable "pro" model, only
  `gemini-3.1-pro-preview`. Using the same family as the agent is a known
  bias. I deferred the judge choice to G10 with a constraint: it must not
  retire before 2027-06.
- `.claude/skills/adk-system-designer/references/gcp-decisions.md:37-41`
  requires current official sources for provider facts, and the session rules
  forbade network access. I kept D4, D5 and D10 provisional and moved the
  lookups into G02. That is the designed path, but it means the design's most
  important residency claim (I7) is unverified.

**Heavier than needed:**
- `.claude/skills/adk-system-designer/assets/system-design-template.md:57-151`
  with the SKILL.md rule that every section is "filled or marked not
  applicable" (`SKILL.md:85-87`). For production this is right, but together
  with D1–D14, I1–I10 and a 17-row failure table the design reached about
  6,700 words. Some content repeats between the decisions table and the
  model-facing contracts.
- The goal field list (`assets/implementation-plan-template.md:56-79`) has
  15 fields per goal, and the ticket repeats most of them. With 21 goals the
  plan plus tickets total about 16,000 words. Generating both from one table
  was the only practical way to keep them consistent.

**Genuinely helpful:**
- `.claude/skills/adk-system-designer/references/delivery-profiles.md:148-156`
  says to re-add the estimates and compare the tickets with the plan. Doing so
  caught the stale 792–1,332 h total in the design.
- `.claude/skills/adk-system-designer/references/design-decisions.md:182-196`
  (the lethal-trifecta split) and `references/failure-review.md:38` led
  directly to D1 (a quarantined photo reader with no tools) and D2 (no
  model-held Guidewire write). These are the design's two most important
  structural choices.
- `.claude/skills/adk-system-designer/SKILL.md:194-199` points to the lifecycle
  JSON. The `vertex_retirement` field showed that `gemini-3.6-flash`
  (2026-11-19) and `gemini-3.7-flash` (2027-01-28) retire inside the plan, so
  I avoided both.
- `.claude/skills/adk-system-designer/references/design-decisions.md:228-249`
  separates the conversation, the invocation and the business operation, and
  covers uncertain outcomes. That shaped D3 and the reconciler.
- `.claude/skills/adk-system-designer/SKILL.md:121-124` covers the headless
  case: one Assumed-answers table, with dependent decisions marked
  provisional. It removed any doubt about whether to stop and ask.

## 6. Next prompt the skills told the user to type

The skill's own example, quoted verbatim from `SKILL.md:278` and
`references/implementation-handoff.md:105`:

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
```

Following that pattern, the plan's "Resume here" section gives this prompt for
the next ready goal:

```text
/adk-engineer Carry out G03 (local intake agent skeleton) from docs/plans/home-claim-intake.md.
Read docs/architecture/home-claim-intake.md and preserve its decisions D1, D2 and D6.
Use adk-workflow-design with adk-agent-instructions, adk-tool-interface-design
and adk-model-and-output-contracts.
Work locally only, verify the G03 acceptance cases, and update
the plan with actual evidence and remaining blockers.
```

# Report: home-insurance claim intake agent, design and phase 1 tickets

Session date 2026-10-14. Headless run: the user was not available, so no
question was asked and every answer below is an assumption.

## 1. Skills invoked and reference files opened, in order

Skills invoked: `adk-system-designer` (by the user's slash command). No other
skill was invoked. Design and planning only, so `adk-engineer` and the
specialists were not run. Their compatibility files and one asset were read
for facts the designer told me to take from them.

Files opened, in order (all under `.claude/skills/`):

1. `adk-system-designer/SKILL.md` (loaded by the command)
2. `adk-system-designer/references/delivery-profiles.md`
3. `adk-system-designer/references/design-decisions.md`
4. `adk-system-designer/references/failure-review.md`
5. `adk-system-designer/references/runtime-and-delivery.md`
6. `adk-system-designer/references/gcp-decisions.md`
7. `adk-system-designer/references/implementation-handoff.md`
8. `adk-system-designer/assets/system-design-template.md`
9. `adk-system-designer/assets/implementation-plan-template.md`
10. `adk-system-designer/assets/ticket-template.md`
11. `adk-system-designer/scripts/check_schedule.py`
12. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
13. `adk-model-and-output-contracts/references/compatibility.md` (first 40 lines)
14. Every specialist's `references/compatibility.md`, grepped only for its pinned ADK version (all 2.8.0)
15. `adk-operational-guardrails/references/compatibility.md` and `adk-memory-architecture/references/compatibility.md`, grepped for confirmation and artifact notes

## 2. Questions I would have asked, and the answers I assumed

The full table, with the decisions that depend on each answer, is the
**Assumed answers** section at the top of `docs/architecture/home-claim-intake.md`.

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | Which EU countries and languages at GA? | One market, two languages (local + English) |
| A2 | Which Guidewire product and API? | ClaimCenter on Guidewire Cloud, Cloud API REST, OAuth client credentials; non-prod tenant on request |
| A3 | Existing portal and login to reuse? | Yes: web portal with OIDC customer-identity provider; the agent is a panel inside it |
| A4 | Does the agent state coverage or payout? | No; FNOL intake only |
| A5 | Volume and peaks? | ~60k home claims/year, storm peaks 10×, design for 200 concurrent conversations |
| A6 | Model and cloud budget? | ≤ €0.40 model spend per submitted claim; non-prod ≤ €3,000/month |
| A7 | Strict EU residency including inference? | Yes; regional EU endpoints only |
| A8 | Team familiarity? | Strong Python, GCP through a landing zone, new to ADK (×1.5) |
| A9 | Historic claim photos for evaluation? | Not before the DPIA; staged, synthetic and consented employee photos |
| A10 | Who signs the DPIA, pen test and go-live? | DPO; external vendor; internal change board |
| A11 | Fallback channel? | Existing web form and phone |
| A12 | Malware scanning for uploads? | None; decode and re-encode server side |
| A13 | Accessibility and AI transparency? | WCAG 2.1 AA; EU AI Act Art. 50 notice approved by legal |
| A14 | GA service targets? | 99.5% availability; ≥ 99% confirmed drafts reach a claim number within 5 min; p95 turn ≤ 8 s |
| A15 | Retention? | Sessions 90 days; photos 30 days after attachment; ledger 2 years with IDs and hashes only |
| A16 | Where do claim documents live? | Attached via the ClaimCenter documents API |
| A17 | Submitted claim or draft for triage? | Submitted FNOL flagged "digital assistant", AI note separate |
| A18 | Pen test before real customers? | Before GA; invite-only pilot may run during the pen test after internal review (open O3) |
| — | Start date and working days? | Start 2026-10-19; 95 working days to GA |
| — | Focused hours per person? | 5 h/day for full-time engineers and ML, 2 h/day for the security reviewer |
| — | Cut line (asked of the user by the skill) | Not confirmed; the plan recommends either accepting low-end-only risk at 95 days or moving GA to 107 working days |

## 3. Files written or changed, and what was not finished

Written (all new; nothing else in the repository changed):

- `docs/architecture/home-claim-intake.md`: the design. Assumed answers,
  journey, delivery constraints and depth, invariants I1–I7, decisions
  D1–D14, model-facing contracts, data and authority, security posture,
  budgets, a failure coverage grid over 6 integrations, cross-cutting
  scenarios, verification, open decisions O1–O6. Status **draft**.
- `docs/plans/home-claim-intake.md`: the plan. Summary, constraints, proposed
  layout, capacity and load table, the machine-readable schedule block
  (25 goals + 8 waits in phase 1, 5 goals in phase 2), the schedule-check
  result, a table of what-if changes, an implementation map, a goals table
  linking tickets, waits, phase 2, a later list, and a resume prompt.
- `docs/tickets/home-claim-intake/G01-…md` to `G25-…md`: 25 phase 1 tickets
  from the ticket template, with figures copied from the schedule block.
  Evidence sections are empty.
- `REPORT.md`: this file.

Temporary files: a `.whatif/` directory with what-if plan copies and the
ticket generator script, and a `__pycache__` created by running the helper's
tests inside `.claude/skills/adk-system-designer/tests/`. I deleted both.
`git status` shows only `docs/` and this report as new.

Not finished, or not possible here:

- No user confirmation of the profile, cut line or any decision. Everything
  is provisional.
- No provider facts were checked online (no network). That covers EU
  regional availability of `gemini-3.8-flash` (O1), Guidewire Cloud API
  replay semantics (O2), Vertex and Guidewire quotas, and prices. Each is a
  named open decision or a goal's acceptance item. No cost figure is quoted.
- The Guidewire endpoint shape in the design (`claim/v1`, documents and
  submit steps) comes from my general knowledge. It is not cited and is
  labelled as the A2 assumption; G01 verifies it.
- Phase 2 goals have no owners and no tickets, which the skill intends.
- The schedule fits the 95-day calendar at the low end only. That is a
  finding to decide on, not something left undone.

## 4. Checks run, and checks not run

| Check | Result |
| --- | --- |
| `check_schedule.py` on the first draft of the schedule (python3.11, stdlib only) | 100.5–157.3 working days vs 95: "fits: no", exit 1 |
| 13 what-if runs of the helper (remedies listed in the plan's change table) | Each result recorded in the plan; the adopted set gives 70.6–106.7 |
| `check_schedule.py --plan … --tickets … --days 95` (final) | 702–1070 h vs 2280 h capacity: fits. Finish 70.6–106.7 working days: "fits: low end only", exit 1. No plan/ticket mismatch, no unsettled mention, no handoff without hours |
| Same with `--days 107` | "fits: yes", exit 0 |
| Same with `--phase 2` | Parses: 5 goals, 124–208 h |
| The helper's own unit tests: `python3.11 -m unittest discover -s tests` in the designer skill | 14 tests OK |

Earlier failing runs caught real issues, which I fixed:

- The helper's mention check found that G03 deploys the G02 image without
  depending on G02. I added the dependency.
- Six out-of-scope pointers were settled as `mentions_only`.

Not run:

- Any test that imports `google.adk`: the dependencies are not installed and
  no code was written (design only).
- Any network, cloud, Guidewire or model call.
- No full markdown link checker was run. A shell check confirmed that every
  relative link in the plan resolves to an existing file. Links inside the
  design and the tickets were not checked.

## 5. Friction log

Unsure what to do:

- **Which Python to use for the helper.** `python3` is 3.9.13 here.
  `delivery-profiles.md:220-221` says "If Python 3.11 or later is not
  available, say the schedule was not checked". I found
  `/opt/homebrew/bin/python3.11` and used it, which needed a search. The
  script header (`scripts/check_schedule.py:1-13`) does not state the minimum
  version. Naming the interpreter requirement in `SKILL.md:95` would save a
  step.
- **Restructuring versus "do not remove a dependency to make the numbers
  fit".** `delivery-profiles.md:189-192` says to change the plan "only in
  ways that are true of the work". I changed four dependencies after a
  failing run: G09 no longer waits for G01, G23 runs in parallel with the
  pilot, the security review is split, and the pilot runs during the pen
  test. I believe each is true of the work, and I recorded each in the change
  table. But the line between "a better true plan" and "removing a dependency
  to fit" is a judgement the reference does not help with. One sentence would
  help: re-deriving a dependency from what the work needs is allowed, and
  deleting one that is real is not.
- **Where a goal's route lives when tickets exist.**
  `implementation-plan-template.md:111-113` says the ticket is the goal's
  home and the plan keeps only the table. `delivery-profiles.md:156-158` says
  tickets copy figures and acceptance "but link to the plan for the route and
  rationale". `ticket-template.md` has no route field. I put routes in the
  plan's implementation map, keyed by decision, and kept scope in the
  tickets.
- **Focus factor versus `--person` hours.** `delivery-profiles.md:227-229`
  gives focus factors (0.6/0.8) for capacity. `delivery-profiles.md:178-179`
  says to pass "full focused hours" per person to the helper, which then
  applies `--reserve`. It was unclear whether 5 h/day should already include
  the focus factor. I assumed yes (8 h × ~0.6), and the reserve on top.
- **Estimating production-scale goals.** The starting-point table in
  `delivery-profiles.md:138-147` has slices of 1–16 h. Almost every goal here
  is larger: a Guidewire integration, a production frontend, DPIA work, a
  pilot. I extrapolated. With these numbers every person is under half
  loaded, which may say more about the estimates than about the team.
- **Running example in the template.** The design template's
  "Verification and implementation handoff" (`system-design-template.md:131-135`)
  asks for a "deliverable the evaluator will judge… regenerated" paragraph.
  That is assignment-oriented, and I left it out for a production service
  without marking it n/a. That arguably breaks `SKILL.md:87-88` ("mark the
  others not applicable in one line").
- **Wait entries with no owner.** The template block
  (`implementation-plan-template.md:49-61`) shows only goal entries.
  `delivery-profiles.md:124-127` explains `W1` entries with `total: 0`. That
  worked, but the template has no W example.

Heavier than needed:

- Copying 25 tickets by hand would have been error-prone, so I generated them
  from the schedule block with a throwaway script. The skill offers no
  generator, and `delivery-profiles.md:155-158` requires the figures to
  match exactly, which the helper then checks.
- The mention check (`check_schedule.py:170-204`) flagged out-of-scope
  pointers such as "UI is G12's job" as problems, so six had to be settled
  with `mentions_only`. That is useful but noisy. It also cannot tell a real
  outside approval from a mention: G19's "security review" passed only
  because an unrelated ancestor (W2, OIDC registration) has wait days
  (`check_schedule.py:200`).
- The what-if loop took 13 runs. The skill requires what-ifs before any
  negative claim (`delivery-profiles.md:196-201`), and that was right: it
  showed that more security-reviewer hours do not help. A `--what-if` option
  or a documented way to vary one entry would make it cheaper.

Genuinely helpful:

- `SKILL.md:125-127`: the "Assumed answers" table at the top for headless
  runs made the no-user situation clear-cut.
- `SKILL.md:199-203` and `model-lifecycle-2026-10-01.json`: choosing the model
  from the dated table avoided `gemini-3.7-flash` and `gemini-3.6-flash`,
  whose Vertex retirement dates (2027-01-28, 2026-11-19) fall before or near
  GA. From memory I would likely have picked one of them.
- `failure-review.md:7-23`: building the coverage grid from the list of
  integrations made sure Guidewire's "write outcome unknown" and "partial
  multi-step" cells got the ledger and reconciler design.
- `design-decisions.md:182-196`: the lethal-trifecta check led directly to
  D2, where the agent has no Guidewire write tool and the customer confirms
  a server-rendered summary.
- `delivery-profiles.md:209-220`, the helper's prose check, found a real
  missing dependency (G03 on G02).
- The helper's finish computation, which respects one goal per person and the
  waits. Doing it by hand, I would have reported "fits" from the hours alone
  (702–1070 of 2280). The calendar is the real constraint.

## 6. The exact next prompt

The skill's template for the closing prompt (`SKILL.md:287-289`), verbatim:

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
```

The prompt I gave in the plan's summary and in the closing message, for the
first ready goal, in the ticket template's form (`ticket-template.md:53-57`):

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G02-walking-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

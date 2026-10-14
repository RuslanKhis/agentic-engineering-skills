# Report: salon booking assistant design session (2026-10-14)

## 1. Skills invoked and reference files opened, in order

Skill invoked: `adk-system-designer` (by the user's slash command). No other
skill was invoked; specialist files were read only where the designer told me to.

Files opened, in order:

1. `.claude/skills/adk-system-designer/SKILL.md` (loaded with the command)
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md`
3. `.claude/skills/adk-system-designer/references/design-decisions.md`
4. `.claude/skills/adk-system-designer/references/failure-review.md`
5. `.claude/skills/adk-system-designer/references/implementation-handoff.md`
6. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
7. `.claude/skills/adk-system-designer/assets/ticket-template.md`
8. `.claude/skills/adk-system-designer/assets/system-design-template.md`
9. `.claude/skills/adk-system-designer/references/gcp-decisions.md`
10. `.claude/skills/adk-system-designer/scripts/check_schedule.py` (lines 1–80, then 80–422)
11. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
12. `.claude/skills/adk-model-and-output-contracts/references/compatibility.md` (grep for the version line)
13. `.claude/skills/safe-api-tool-calls/references/compatibility.md` (grep, then lines 1–30)
14. `.claude/skills/adk-system-designer/references/runtime-and-delivery.md`
15. `.claude/skills/adk-system-designer/tests/test_check_schedule.py` (imports only, to run it)

Not opened: `assets` and references of the other specialists; not needed for a
design-only pass.

## 2. Questions I would have asked, and the answers I assumed

All are also in the design's **Assumed answers** table
(`docs/architecture/salon-booking-assistant.md`), with the decisions that depend
on each.

| # | Question | Assumed answer |
| --- | --- | --- |
| Q1 | Deadline, and is it continued? | 10 working days from 2026-10-15; continued, phase 1 code kept |
| Q2 | People, hours, ADK/GCP familiarity, who runs it? | 3 developers full time, ~6 focused h/day each, know Python and basic GCP, new to ADK (×1.5 estimates); same team runs it |
| Q3 | Money? | About A$500/month for model and cloud in the pilot, budget alert |
| Q4 | Who uses and judges it? | Existing signed-in customers of the five salons; the chain's operations manager judges |
| Q5 | Data and effects? | Real personal data; creates, moves, cancels real appointments; no payments or deposits |
| Q6 | Staging booking API, idempotency keys? | We own the API; staging exists; idempotency unknown (G01 checks, we can add it) |
| Q7 | How do customers sign in? | Website login issues a verifiable JWT; fallback email codes |
| Q8 | Atomic reschedule? | Unknown; design covers both atomic and book-then-cancel |
| Q9 | Channel? | Chat widget on signed-in website pages only |
| Q10 | Data location? | Australia (`australia-southeast1`); model location to be checked |
| Q11 | Change/cancel policy? | Allowed until 24 h before start; configurable |
| Q12 | Languages? | English only |
| Q13 | When the assistant can't help? | Show the salon phone number; no live hand-off |
| Q14 | Who signs off go-live and data use? | Chain operations manager, 3–5 working days (W1) |
| — | Do you accept the cut line / will Dev B give 7 focused h/day? | Not assumed: left as an open decision in the plan summary |

## 3. Files written or changed, and what was not finished

Written (all new):

- `docs/architecture/salon-booking-assistant.md`: design, status draft:
  assumed answers, journey, depth table and floor, invariants I1–I6,
  decisions D1–D10, model-facing contracts, data and authority, security
  posture, budgets, coverage grid for 5 integrations, scenarios F1–F8, open
  decisions OD1–OD5.
- `docs/plans/salon-booking-assistant.md`: plan with summary, capacity, load
  table, schedule block (W1, G01–G09, G10–G14), what-if table, implementation
  map, goals table linking tickets, phase 2 goals, later list, resume prompt.
- `docs/tickets/salon-booking-assistant/G01-…G09-*.md`: nine phase 1 tickets.
- `REPORT.md` (this file).

Changed: none of the existing files. I deleted a `tests/__pycache__/` directory
that my own unittest run had created inside the skill folder.

Not finished:

- Nothing was confirmed by the user; the design stays **draft** and every
  decision depending on Q1–Q14 is provisional.
- Phase 1 fits the hours but **only the low end fits the calendar**; the
  remedy (Dev B at 7 h/day) is a user decision, not applied.
- No provider facts were looked up (no network): Vertex pricing, model
  availability in Australia, and current ADK docs remain verification items
  (OD2, G01, G08).
- Design and plan are on the long side for an MVP (237 and 347 lines); I did not
  do a separate trimming pass.

## 4. Checks run and not run

Run:

| Check | Result |
| --- | --- |
| `python3.11 -I .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/salon-booking-assistant.md --tickets docs/tickets/salon-booking-assistant/ --days 10 --reserve 0.25 --person "Dev A=6" --person "Dev B=6" --person "Dev C=6"` | exit 1: 61–96 h vs 135 h capacity (fits); finish 6.67–10.44 working days vs 10 (low end only); no ticket/plan mismatch; first run found 2 unsettled mentions (G01→W1, G04→G06), settled in `mentions_only` |
| Same with `--person "Dev B=7"` | exit 0: finish 6.06–9.49, fits |
| Ten further what-ifs (fed through process substitution, no files) | none closed the gap; listed in the plan's what-if table |
| Same helper with `--phase 2` | 5 goals, 32–60 h |
| `python3.11 -m unittest tests/test_check_schedule.py` (skill's own tests) | 14 tests OK |

Not run:

- `python3` (3.9.13) was the default; the helper needs 3.11, so I used
  `/usr/local/bin/python3.11` (or the Framework one on PATH).
- `pytest` is not installed for python3.11; ran the helper's tests via unittest.
- No application tests exist (design only); every ticket's verification is
  planned and not run. Anything importing `google.adk` could not run here.
- No network, cloud, or package-install commands were run.

## 5. Friction log

| Moment | Kind | Pointer |
| --- | --- | --- |
| Skill asks me to open with a scope-gate question turn and let the user answer before settling product choices; the session forbids questions. The headless rule further down resolved it cleanly. | Unsure, then helpful | `.claude/skills/adk-system-designer/SKILL.md:48`, `:54`, `:125` |
| The scope-gate defaults ("one developer, part time", "synthetic, read only") did not fit; the request already answered capacity partly (3 people, 2 weeks) but not hours/day, which drives every figure. I had to invent 6 h/day. | Unsure | `.claude/skills/adk-system-designer/references/delivery-profiles.md:16-22` |
| The MVP worked example ("three people, two weeks… idempotent order creation and explicit confirmation are in phase 1") matched this request almost exactly and set the floor quickly. | Helpful | `.claude/skills/adk-system-designer/references/delivery-profiles.md:350-353` |
| The model-lifecycle table steered the model choice away from `gemini-3.6-flash` (Vertex retirement 2026-11-19, inside the pilot) and 2.5 (2026-10-20); I would have picked by memory otherwise. | Helpful | `.claude/skills/adk-system-designer/SKILL.md:198-205`; `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` |
| The helper's command uses `python3`, which is 3.9 here; the 3.11 requirement is stated only at the end of a long paragraph. Found 3.11 manually. | Unsure | `.claude/skills/adk-system-designer/references/delivery-profiles.md:173`, `:220-221` |
| The helper's finish depends on its greedy ordering: it picks the ready goal with the longest remaining chain, so a goal with no dependency is not placed into an idle slot before an earlier-picked goal (what-if "G08 without G01" left Dev B's queue unchanged). The finish figure is a list-scheduling result, not an optimum; I quoted it as the skill requires but noted it. | Unsure | `.claude/skills/adk-system-designer/scripts/check_schedule.py:301-311` |
| "Run every remedy you offer as a what-if": genuinely useful. My intuition (cut G05, move G09) was wrong; only more hours on Dev B closed the gap. | Helpful | `.claude/skills/adk-system-designer/references/delivery-profiles.md:195-201` |
| Mention check: "settle by editing the schedule, not by rewording the prose". I had worded G06 without the G04 ID before running the check; I put the ID back and settled it in `mentions_only` so the rule held in spirit. | Unsure | `.claude/skills/adk-system-designer/references/delivery-profiles.md:209-221` |
| Ticket vs plan home: tickets are the goal's home, the plan keeps a table; but the plan template also asks for a full goal entry and a goals table with seven columns. Easy to duplicate scope; I kept only the table. | Heavier than needed | `.claude/skills/adk-system-designer/references/delivery-profiles.md:306-313`; `.claude/skills/adk-system-designer/assets/implementation-plan-template.md:111-113` |
| Template sections plus coverage grid plus scenario table plus data table for an MVP is heavy; the skill says "two to four pages per phase" but the design template's full set pushes past that. No word guidance for MVP (deliberately, per the skill). | Heavier than needed | `.claude/skills/adk-system-designer/references/delivery-profiles.md:36`, `:320-329`; `.claude/skills/adk-system-designer/assets/system-design-template.md` |
| Next-prompt form differs between SKILL.md (`Carry out G01 from docs/plans/<topic>.md`) and the ticket template (`Carry out <path to this ticket>…`). With tickets written I used the ticket form. | Unsure | `.claude/skills/adk-system-designer/SKILL.md:286-289`; `.claude/skills/adk-system-designer/assets/ticket-template.md:51-57` |
| Coverage grid by integration × failure type made the write-outcome-unknown and partial-move cells impossible to skip. | Helpful | `.claude/skills/adk-system-designer/references/failure-review.md:7-23` |
| The helper flags "review is the same ratio on every goal" — prompted me to size review heavier on G03/G04 (auth, writes) than on G07. | Helpful | `.claude/skills/adk-system-designer/scripts/check_schedule.py` (`ratios` check in `analyse`) |

## 6. Next prompt the skills told the user to type

From the G01 ticket's "Run this ticket" block (the plan's Resume here repeats it):

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-contracts-and-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

# Report: revise the salon booking assistant to an 8-day launch

## 1. Skills invoked and reference files opened, in order

Skill invoked: `adk-system-designer`, through the user's `/adk-system-designer` command. I invoked no other skill. `adk-engineer` and the specialists are named only in run prompts.

Files opened, in order:

1. `docs/plans/salon-booking-assistant.md` (revision 1)
2. `docs/architecture/salon-booking-assistant.md` (revision 1)
3. All 11 tickets in `docs/tickets/salon-booking-assistant/`
4. `.claude/skills/adk-system-designer/references/delivery-profiles.md` (whole file)
5. `.claude/skills/adk-system-designer/scripts/check_schedule.py` (lines 1–80, then 80–422)
6. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
7. `.claude/skills/adk-system-designer/references/failure-review.md`
8. `.claude/skills/adk-system-designer/references/design-decisions.md`: the heading list, then lines 228–260 ("External effects and recovery")
9. `.claude/skills/adk-system-designer/assets/ticket-template.md`
10. `.claude/skills/adk-system-designer/references/implementation-handoff.md`: grep only, for change-table guidance
11. `.claude/skills/adk-system-designer/tests/test_check_schedule.py`: the imports only, before running it

Not opened: `gcp-decisions.md`, `runtime-and-delivery.md`, `system-design-template.md`, the full `implementation-handoff.md`, and the specialists' `compatibility.md` and model-lifecycle assets. This revision does not change the model, the hosting choice or the runtime contracts, so I kept D2 and D6–D7 as they were.

## 2. Questions I would have asked, and the answers I assumed

| # | Question | Assumed answer | Recorded as |
| --- | --- | --- | --- |
| 1 | Do the 8 days count from the original start? Has anything been built? | Day 1 is the first implementation day. Nothing is built; the repository has no app code. Launch means the pilot salon goes live (G11). | A1 |
| 2 | Is it still 5 focused hours a day each, with no overtime to absorb the shorter date? | Yes. | A2 |
| 3 | At launch, may a move be two confirmed steps (book the new time, then cancel the old one)? | Yes. Single-step move becomes G06 in phase 2. | A11 |
| 4 | May chat require sign-in at launch, with anonymous availability chat later? | Yes. Visitors keep using the website's availability pages. | A12 |
| 5 | Is a 20-case pre-launch evaluation enough, growing to 30 or more in phase 2? | Yes, with the same threshold (≥ 90 % pass and 0 forbidden calls). | A13 |
| 6 | May Cloud Trace export wait until after launch, with structured logs only? | Yes. Pinned ADK 2.8.0 lacks the span-retention fix anyway. | A14 |
| 7 | May the 30-day session deletion job be built after launch? | Yes, as long as it runs before launch day + 30. It is also a graduation condition. | A15 |
| 8 | Would the owners take 9 days instead of the cut package? | Unknown. Offered as the tested alternative: 9 days restores A13–A15 (finish 7.67–8.67). | Design §9, plan cut line |
| 9 | Is a plan that fits at exactly 8.0 days on the high end (inside the 25 % reserve) acceptable? | Yes. I kept the 25 % reserve rather than lowering it to make room. | Plan summary |
| 10 | Still pilot salon only at launch? | Yes, as in revision 1. | §2 |

## 3. Files written or changed, and what is not finished

Changed:
- `docs/architecture/salon-booking-assistant.md`. Revision 2, still **draft**. Changes:
  - Assumed answers: A1 updated with the 8 days marked user-stated; A11–A15 added.
  - Journey: now a two-step move.
  - D1, D3, D8–D10: five phase-1 tools and the `changeable` flag; sign-in required; budget alert in G10; deletion job in G21.
  - §2: depth and deferred-control tables updated.
  - §3: invariant verification references updated.
  - §7: new **coverage grid** (missing in revision 1, which `failure-review.md` requires) and new rows for the two-step move and for no token.
  - §8 ladder and §9 open decisions updated.
- `docs/plans/salon-booking-assistant.md`. Rewritten as revision 2:
  - summary, owners and loads, schedule block with `mentions_only`, and the helper result
  - a **"What revision 2 removed or weakened"** change table
  - the failing runs and what-ifs
  - cut line, implementation map, goals table
  - phase 2 (new G20, G21, G22; G06 moved there)
  - the "Resume here" section
- Tickets G01, G02, G03, G04, G05, G07, G08, G09, G10, G11: figures, owners, dependencies, scope and acceptance updated to match.
- `G06-move-appointment.md`: kept and marked phase 2, status `deferred`.
- `G04a-operations-core.md`: **new** (the old G04 split into an operations core and the booking tool).
- `REPORT.md`: this file.

Not finished:
- Nothing is confirmed by the user; every decision except the date is still provisional.
- No tickets for phase 2 goals G12–G22, by design, apart from the kept G06.
- Prices, quotas and regions were not looked up (no network). D2's lifecycle snapshot is still the one dated 2026-10-08.
- Plan prose outside the summary was not re-checked word by word against the design for duplication.

## 4. Checks run and checks not run

Run:
- **Revision-1 plan at 8 days:** `python3.12 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/salon-booking-assistant.md --tickets docs/tickets/salon-booking-assistant/ --days 8 --reserve 0.25 --person "Dev A=5" --person "Dev B=5" --person "Dev C=5"`.
  - Result: exit 1, 56–88.5 h, finish 6.13–9.87 (low end only).
  - It also reported 17 unsettled mentions, although the revision-1 plan said the check was clean.
- **Same command on the final files:** exit 0.
  - 48.5–74.5 h of 90 h; finish 5.47–8 working days of 8; fits.
  - No ticket mismatches and no handoffs without hours. Mention-only items are listed in the plan.
- **Owner-assignment search (scratch, now deleted):** I tried every owner assignment for each candidate scope by importing `check_schedule.analyse`. Best results:
  - full scope with G04 split: 9.6 days
  - single-step move removed: 9.33
  - plus all cuts: 8.0–8.13
- **About 12 what-if runs of the helper CLI** on modified copies of the schedule; results are in the plan's what-if table.
- **The skill's own helper tests:** `PYTHONDONTWRITEBYTECODE=1 python3.12 -m unittest discover -s .claude/skills/adk-system-designer/tests -p 'test_check_schedule.py'` ran 14 tests, all passed.

Not run:
- **Application tests:** none. No application code exists, and google-adk is not installed. So no ticket's verification commands (`pytest tests/...`, `eval/run.py`) could run.
- **pytest:** not installed for python3.12, so the helper tests ran through unittest instead.
- **No network, cloud or price lookups.**

Rule deviations, reported plainly:
- For a few minutes my scratch scripts were in `/tmp/sched`, which is outside the working directory. I moved them into `./.scratch` and deleted that at the end.
- Importing the helper created `.claude/skills/adk-system-designer/scripts/__pycache__`. I deleted it.

## 5. Friction log

**Moments I was unsure what to do**

- **Where the required change table goes.** `SKILL.md:249-252` says to list everything removed or weakened in "the plan's change table". `assets/implementation-plan-template.md` has no such section; it only covers the schedule check at lines 46-67. I added a "What revision 2 removed or weakened" table next to "What changed after failing runs".
- **Naming a split goal.** "Stable ID" (`SKILL.md:261-262`) gives no guidance for splitting an existing goal. I chose `G04a` rather than renumbering. The helper's ID regex handles it.
- **Keeping the deferred G06 ticket.** `delivery-profiles.md:317-319` says to write tickets only for phase 1, but the user asked to "update the tickets". I kept the G06 ticket marked phase 2 and deferred, so its acceptance is not lost. It then has to be in the schedule block to avoid a ticket-not-in-plan problem.
- **The reserve.** `delivery-profiles.md:232` allows a 20–30 % reserve, but lowering it to fit felt like what `:189-192` forbids ("do not ... drop a review to make the numbers fit"). I kept 25 %. The skill does not say this either way.
- **Zero slack.** The plan fits at exactly 8.0 days at the high end, with all three people converging on day 6.67. The skill does not say whether "fits" with zero calendar slack beyond the reserve should be presented differently. I said it plainly in the summary.

**Heavier than needed**

- **No owner search in the helper.** The rule at `delivery-profiles.md:189-201` ("run every remedy as a what-if", "a negative claim needs the same what-ifs") is right but expensive. The helper has no owner-assignment search, so I wrote one by importing `analyse()` (`check_schedule.py:213`). That polluted the skill directory with `__pycache__`. A `--search-owners` option would save many runs.
- **The scheduler does not backfill idle time.** `check_schedule.py:302-304` schedules by longest remaining path. Splitting a small independent goal out for a developer idle on day 1 (the widget; the price lookup) made the finish *worse* (8.8 and 9.33 instead of 8.13). The reference (`delivery-profiles.md:165-187`) does not warn about this, so the plan can't use a real-world tactic.
- **Mentions check.** It flagged 11–17 mentions per run (`check_schedule.py:154-191`). Settling them is tedious but quick. It did not catch the one real hidden dependency, G07's acceptance needing G04a's confirm endpoint. I found that by reading, because G07's ticket never named G04.

**Genuinely helpful**

- `delivery-profiles.md:189-201`: "change the plan only in ways that are true of the work". It stopped me from shaving estimates and made me record each cut with its cost.
- `delivery-profiles.md:320-329`: "Keep every floor item, failure row, test, acceptance case, wait and handoff". This decided what could be weakened and what had to be listed.
- `failure-review.md:7-23`: the coverage grid turned the new two-step move into an explicit "partial multi-step change" cell. Revision 1 had no grid at all.
- `design-decisions.md:252-253`: "Model instructions ... do not supply durable execution guarantees". This kept me from claiming book-first order as a guarantee; it is recorded as an instruction contract with residual risk.
- `SKILL.md:121-127`: the Assumed answers table pattern fit the headless run well.

## 6. The next prompt the skills told the user to type

The skill (`SKILL.md:282-292`) requires a copyable next prompt. The one given, from the plan's "Resume here" section, verbatim:

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract-and-fake.md.
Read docs/architecture/salon-booking-assistant.md and preserve its accepted decisions.
Use safe-api-tool-calls with adk-tool-interface-design.
Work locally only, verify the ticket's acceptance cases, and record evidence and
remaining blockers in the ticket.
```

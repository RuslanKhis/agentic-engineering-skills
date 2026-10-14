# Report: salon booking assistant design session (2026-10-14)

## 1. Skills invoked and reference files opened, in order

Skill invoked: `adk-system-designer` (by the user's slash command). No other
skill was invoked.

Files opened, in order (all under `.claude/skills/`):

1. `adk-system-designer/SKILL.md` (loaded with the command)
2. `adk-system-designer/references/delivery-profiles.md`
3. `adk-system-designer/references/design-decisions.md`
4. `adk-system-designer/references/failure-review.md`
5. `adk-system-designer/references/implementation-handoff.md`
6. `adk-system-designer/assets/implementation-plan-template.md`
7. `adk-system-designer/assets/ticket-template.md`
8. `adk-system-designer/assets/system-design-template.md`
9. `adk-system-designer/references/gcp-decisions.md`
10. `*/references/compatibility.md` (grep only, for the ADK version lines) and a directory listing of `adk-model-and-output-contracts/`
11. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
12. `adk-system-designer/scripts/check_schedule.py`
13. `adk-system-designer/references/runtime-and-delivery.md`
14. `adk-system-designer/tests/test_check_schedule.py` (run, not read)

## 2. Questions I would have asked, and the answers I assumed

These are listed in full, with what depends on each, in the **Assumed answers**
table at the top of `docs/architecture/salon-booking-assistant.md` (A1–A12).
In short:

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | Deadline, and is it continued? | Live in 10 working days (by 2026-10-28); continued |
| A2 | Hours and familiarity? | 3 developers, ~5 focused h/day each, know Python and GCP, new to ADK (1.5× multiplier) |
| A3 | Model and cloud budget? | ≤ US$300/month (illustrative) |
| A4 | Users and judge? | Signed-in salon customers in a widget on the existing booking site; the salon chain's owner judges it |
| A5 | Data and effects? | Real personal data; reversible writes that notify customers; no payments or fees |
| A6 | Customer login? | The site issues a session token our backend can verify |
| A7 | Booking API capabilities? | Ours; server key; reads, create, native reschedule, cancel; enforces rules; no idempotency keys |
| A8 | Channels, language, time zones? | Web chat only, English, one time zone |
| A9 | Booking scope? | One service, for the signed-in customer only |
| A10 | Rollout? | One pilot salon first, then all five after five clean trading days |
| A11 | Retention and region? | 30-day chat retention; one region chosen with the salon chain |
| A12 | Existing database to reuse? | None; new small Cloud SQL Postgres |

Also, from the cut line: **is 6 focused hours a day per developer realistic?**
Assumed no (5 h/day). That assumption is why the calendar only fits at the
low end (section 4).

Open decisions that still need someone: O1–O5 in the design (token
verification, ADK pin and model region, GCP region and data terms,
reschedule semantics and fees, pilot salon).

## 3. Files written or changed, and what is not finished

Written (all new; nothing existing was changed):

- `docs/architecture/salon-booking-assistant.md`: draft design. Assumed answers, journey, depth/floor, invariants I1–I7, decisions D1–D9, model-facing contracts, data and authority, security posture, budgets, failure table, open decisions O1–O5.
- `docs/plans/salon-booking-assistant.md`: summary, capacity and load table, schedule block, schedule-check results and what-if table, cut line, implementation map, goals table, phase 2 (G08–G13), later list, resume prompt.
- `docs/tickets/salon-booking-assistant/` has 8 phase 1 tickets: G01, G02, G03, G04, G05a, G05, G06, G07, with suggested owners Dev A (G01, G03), Dev B (G02, G06) and Dev C (G05a, G04, G05, G07).
- `REPORT.md` (this file).

The temporary what-if directory `.whatif/` and a `__pycache__` left by the
helper tests were deleted.

Not finished:

- The design is **draft**: every decision rests on assumed answers, and none were confirmed by the user.
- Phase 1 **does not fit the calendar at the high end**: 6.93–10.93 working days against 10 at 5 h/day. The cut line asks the user to choose between go-live on day 11 and 6 focused h/day.
- Provider facts were not checked: Vertex availability of `gemini-3.8-flash` in the region, current prices, ADK confirmation limitations, and ADK 2.8 vs 2.10 API names. The rules allowed no network access, so these are listed as verification tasks (O2, G06).
- No tickets for phase 2, by design (the skill says to write tickets for phase 1 only). No ADRs.
- No code, as requested.

## 4. Checks run and not run

Run:

- `python3.11 .claude/skills/adk-system-designer/scripts/check_schedule.py --plan docs/plans/salon-booking-assistant.md --tickets docs/tickets/salon-booking-assistant/ --days 10 --reserve 0.25 --person "Dev A=5" --person "Dev B=5" --person "Dev C=5"`
  gives **exit 1**: 57–88 h against 112.5 h (the hours fit); chain G01→G03→G07 (low) or G02→G03→G07 (high); finish 6.93–10.93 days of 10, **fits at the low end only**. No ticket/plan mismatches and no handoffs without hours.
- The same command at 6 h/day for all three gives exit 0, finish 5.78–9.11 days.
- Nine earlier what-if runs: results are in the plan's change table. The first run showed capacity of 157.5 h because of a parsing problem (section 5, item 2), which I fixed.
- `python3.11 -I -m unittest discover -s .claude/skills/adk-system-designer/tests`: 11 tests passed. pytest is not installed, so I used unittest.

Not run:

- All ADK, agent or `google.adk` tests. None exist yet because this was design only, and google-adk is not installed here.
- All network, cloud or price lookups, which the rules prohibited.
- The schedule helper under the default `python3`, which is 3.9.13. The skill asks for 3.11 or later, so I used `/opt/homebrew/bin/python3.11`.

## 5. Friction log

1. **Scope gate in a headless run.** This was clear. `SKILL.md:54` asks for the scope gate in one turn, and `SKILL.md:124-127` says what to do when no one answers: an Assumed answers table with provisional decisions. This was helpful and saved deliberation.
2. **An empty owner on a wait entry silently became a fourth person.** `references/delivery-profiles.md:124-127` says to give a wait its own entry with "no owner". I wrote `owner:` with an empty value. `scripts/check_schedule.py` (`parse_mapping`, roughly lines 55-74) reads an empty value as a nested mapping, so the helper reported a person `{}` with 45 h of capacity and capacity of 157.5 h instead of 112.5 h. I noticed only because the output had an odd `{}` row. Suggestions: say "omit the owner key" in the reference, or treat an empty owner as none in the helper.
3. **I wrote the helper figures into the plan before running the helper.** I guessed "5.6–8.8 days, fits", but the real run said 7.73–11.73, low end only. The rule at `references/delivery-profiles.md:184-187` (quote its figures instead of your own) caught this. It was genuinely helpful.
4. **The remedy rules were heavier but changed the answer.** `references/delivery-profiles.md:189-201` requires running every remedy as a what-if and offering only those that close the gap. I would otherwise have offered "cut move to phase 2" as the fix, but it does not move the finish at all. Nine what-ifs took several turns, but the resulting statement is honest. It would help if the helper could take what-if overrides (owner hours, a goal's estimate) on the command line instead of editing copies of the plan.
5. **Unclear whether a per-user allowance is floor or phase 2.** `references/delivery-profiles.md:229-230` says per-user allowances on a public service are floor, not scope to cut. The MVP example at `references/delivery-profiles.md:342-345` (which closely matches this request) defers "per-user budgets" to phase 2. I resolved it by keeping a simple per-customer turn cap and rate limit in phase 1 (D6) and putting a durable token budget in phase 2 (G10).
6. **Low-end-only guidance conflicts with "cut scope".** `references/delivery-profiles.md:228-229` says to name the goals that move to phase 2 if work runs high. Here, no scope cut shortened the critical chain, so the honest answer was "the date or the hours", which the reference does not anticipate.
7. **Which ADK version to assume.** `SKILL.md:197-200` says to use the version the specialists name, which is 2.8.0. `adk-agent-observability/references/compatibility.md:40` recommends 2.10.0 or later for a new production deployment. I recorded this as open decision O2, to be settled in G01.
8. **The model lifecycle table was genuinely helpful.** `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` showed that the Vertex retirements of 3.6-flash (2026-11-19) and 3.7-flash (2027-01-28) fall inside the plan's horizon, so I chose `gemini-3.8-flash`.
9. **The trigger for runtime-and-delivery was unclear.** I was unsure whether a non-streaming web chat triggers `SKILL.md:183`. I read the file, and only the browser-contract section (`references/runtime-and-delivery.md:35-54`) affected the design (D8).
10. **Native confirmation could not be checked.** `references/implementation-handoff.md:59` links to the confirmation limitations, but I had no network access. The reason I rejected native confirmation in D4 therefore rests partly on an unverified limitation.
11. **Two forms of the next prompt.** `SKILL.md:277-283` gives `/adk-engineer Carry out G01 from docs/plans/<topic>.md.`, and `assets/ticket-template.md:51-57` gives a ticket-path prompt. Since tickets were requested, I used the ticket form.
12. **Where to put handoff hours when a goal has two inbound handoffs** (G07 receives from Dev A and Dev B). `references/delivery-profiles.md:203-207` doesn't say. I recorded a single 1 h on the receiving goal.
13. **Python version.** The default `python3` is 3.9.13, and `references/delivery-profiles.md:212-213` asks for 3.11 or later. A 3.11 interpreter existed at a non-default path, so the check ran.

## 6. Next prompt the skills told the user to type

Quoted verbatim from the ticket's "Run this ticket" block (the ticket-template form; `SKILL.md:277-283` gives the plan form `/adk-engineer Carry out G01 from docs/plans/<topic>.md.`):

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-read-only-assistant.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

G02 (Dev B) and G05a (Dev C) can start on day 1 alongside it, each with the prompt at the end of its ticket.

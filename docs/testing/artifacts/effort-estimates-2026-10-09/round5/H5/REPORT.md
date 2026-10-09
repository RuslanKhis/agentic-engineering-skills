# Session report: home-insurance claim intake design (ADK, EU)

## 1. Skills invoked and reference files opened, in order

Skill invoked: `adk-system-designer` (by the user's `/adk-system-designer` command). No other skill was invoked.
Specialist files were read only for version and model facts, as the designer
skill directs.

Files opened, in order (all under `.claude/skills/`):

1. `adk-system-designer/SKILL.md` (loaded by the command)
2. `adk-system-designer/references/delivery-profiles.md`
3. `adk-system-designer/scripts/check_schedule.py`
4. `adk-system-designer/references/design-decisions.md`
5. `adk-system-designer/references/failure-review.md`
6. `adk-system-designer/references/implementation-handoff.md`
7. `adk-system-designer/assets/system-design-template.md`
8. `adk-system-designer/assets/implementation-plan-template.md`
9. `adk-system-designer/assets/ticket-template.md`
10. `adk-system-designer/references/gcp-decisions.md`
11. `adk-system-designer/references/runtime-and-delivery.md`
12. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`
13. `adk-model-and-output-contracts/references/compatibility.md` (grep only, for the ADK pin)
14. `*/references/compatibility.md` for every specialist (grep only, for the ADK version: all name google-adk 2.8.0)
15. `adk-model-and-output-contracts/references/model-selection.md` (grep only, for the Vertex 12-month rule and retirement dates)
16. `adk-system-designer/agents/openai.yaml` (first 12 lines)
17. `adk-system-designer/tests/test_check_schedule.py` (first 40 lines, to see how the tests run)

## 2. Questions I would have asked, and the answers I assumed

These are also the **Assumed answers** table (A1–A13) at the top of
`docs/architecture/home-claim-intake.md`, together with the decisions each one affects.

| # | Question | Assumed answer |
| --- | --- | --- |
| A1 | Which EU market(s) and languages at GA? | One market (Germany), German and English; region `europe-west3` |
| A2 | Are all six full time, and how familiar are they with ADK and GCP? | Full time, 6 focused h/day; new to ADK (×1.5 on every estimate), experienced with GCP/Python; security reviewer about one day a week (1.2 focused h/day) |
| A3 | Which Guidewire product and API? | Guidewire Cloud ClaimCenter and PolicyCenter Cloud API, with a sandbox and a pre-production tenant owned by an internal Guidewire team |
| A4 | Is there an existing portal login we can embed into? | Yes: OIDC login and a customer-to-policy-account mapping; the team can add a page |
| A5 | What may the assistant change? | Create a first notice of loss (FNOL) and attach photos after explicit customer confirmation; never decide cover, reserves or payments |
| A6 | Which claims are in scope at GA? | Property damage to home and contents. Injury, liability, ongoing emergencies and commercial property go to the hotline |
| A7 | Expected volume? | ~10k home claims a year, 40 % digital (≈11 a day); storm peaks ≈330 a day and ≈50 concurrent sessions |
| A8 | Model and cloud budget? | Not given. Assumed to be set by the business in G04 and enforced by application admission plus a budget alert |
| A9 | Which regulatory regimes apply? | GDPR with a DPO-signed DPIA, EU AI Act transparency, DORA ICT register. Legal confirms the system is not high-risk |
| A10 | Must all processing, including inference, stay in the EU? | Yes; no global endpoints |
| A11 | Retention for transcripts and photos? | Photos: attached + 30 days. Transcripts: 90 days after submission or abandonment. DPIA may change both |
| A12 | Who operates it after GA? | The same team, business-hours on-call; claims operations handle uncertain submissions |
| A13 | Is a pilot before GA acceptable? | Yes: 2–3 weeks with a small share of portal users |
| — | Start date and GA date? | Start 2026-10-12; GA 2027-03-09; 95 working days after holidays |
| — | Confirm or move the cut line, and accept the date or the extra reviewer time? | Not assumed. Left open in the plan's capacity section, with a recommendation: reviewer two days a week and GA 2027-03-12 |

## 3. Files written or changed, and what was not finished

Written (all new; nothing else in the repository was changed):

- `docs/architecture/home-claim-intake.md`: draft production design. Contents: assumed answers, journey, depth table, invariants I1–I8 with targets T1–T2, component diagram and submission sequence, decisions D1–D16, model-facing contracts, data and authority, security posture, budgets, failure table, verification and open decisions O1–O8.
- `docs/plans/home-claim-intake.md`: plan with proposed module layout, capacity and load tables, the yaml schedule block, schedule-check results, what-ifs, changes made after failing runs, cut line, implementation map, 28 phase 1 goal entries (G01–G28), phase 2 (P2-01 to P2-06), the Later list, open decisions and a resume prompt.
- `docs/tickets/home-claim-intake/G01-…md` to `G28-…md`: 28 ticket files, one per phase 1 goal. Each copies its goal's estimate, owner, blockers, waits and acceptance, and has its own run prompt.
- `REPORT.md` (this file).

During the session I generated the plan's goal sections and the tickets from one data file, `.gen/goals.py`, plus `.gen/render.py`, so the figures could not drift. Both were deleted at the end; the Markdown files are now the source.

Not finished, or open:

- The design is **draft**. Every decision is a recommendation; the user has accepted none.
- The plan's calendar **does not fit at the high end** with the stated reviewer time (see §4). The date versus reviewer-time choice is waiting on the user.
- Provider facts were not verified because network access was not allowed:
  - EU regional availability of `gemini-3.8-flash` with image input (O2)
  - Model Armor EU regions
  - Guidewire Cloud API replay header name and semantics: I assumed `GW-DBTransaction-ID` from memory, unverified
  - Cloud Tasks named-task deduplication window
  - prices for the cost formula

  Each one is a step in a goal (G01, G02/G25, G04, G14).
- Tickets for goals that still have prerequisites are marked `status: blocked`; tickets with none are `ready`.
- No application code was written, as requested.

## 4. Checks run and not run

Run:

- `python3.12 -B -m unittest discover -s .claude/skills/adk-system-designer/tests -v`, with `TMPDIR` pointed at a temporary folder inside the working directory and removed afterwards: **10 tests, OK**. The default `python3` is 3.9.13; the skill asks for 3.11 or later, so I used `/opt/homebrew/bin/python3.12`.
- `check_schedule.py --plan docs/plans/home-claim-intake.md --tickets docs/tickets/home-claim-intake/ --days 95 --reserve 0.25`, with six people at 6 h/day and the reviewer at 1.2:
  - 28 goals, 462–696 h against a capacity of 2,650.5 h: hours fit.
  - Finish range **70.67–106.33 working days against 95: fits at the low end only. Exit 1.**
  - No mismatch between tickets and plan.
- What-if runs of the same command, quoted in the plan:
  - reviewer at 2.4 h/day, 95 days: 65.6–97.9, low end only;
  - reviewer at 2.4 h/day, 98 days: fits, exit 0 (rerun against the final plan and tickets);
  - reviewer at 1.2 h/day, 107 days: fits, exit 0.
- Earlier failing runs during planning: 84.7–129.2, then 75.0–117.6, then 73.8–111.2, then 71.4–108.8. The changes between runs are listed in the plan.

Not run:

- No application tests: no application code exists, and google-adk is not installed (anything importing `google.adk` could not run here anyway).
- No cloud, Guidewire, model or network calls; this was forbidden.
- No Markdown link checker. Ticket anchor links into the plan were generated in GitHub-slug style but not checked in a renderer.

## 5. Friction log

**Unsure what to do**

- Whether "phase 1" means everything up to GA or a pilot slice. `SKILL.md:262` says "phase 1 fits the stated capacity, phase 2 graduates or hardens", but here the deadline is GA itself. I chose phase 1 = GA and phase 2 = after GA. A line on deadline-equals-launch cases would help.
- Production-scale estimates. The starter table at `references/delivery-profiles.md:130-142` covers small slices, so a production plan has to extrapolate a long way. The result: 462–696 h against 2,650 h of capacity, with the calendar (waits and the part-time reviewer) as the only constraint. I wasn't sure whether that is a real finding or an under-estimate. I reported it as a finding and noted that overheads are assumed to sit inside the focus factor.
- How to model a wait that starts on day one. `references/delivery-profiles.md:186-188` says to add "a goal or first step that requests it today". But `scripts/check_schedule.py:239` always adds `wait_days` *after* a goal's work (`finish = start + work + wait`), so a goal's first step cannot start its own wait. I had to split G02 into G02 (docs and requests) and G25 (sandbox verification behind the wait). Accurate, but it costs a goal.
- Removing a dependency versus correcting one. `references/delivery-profiles.md:184-186` forbids removing a dependency to make the numbers fit. I considered unblocking G15 from G08, because scripted-model tests don't use the instruction. I decided against it because it looked like gaming. Guidance on telling a wrong dependency from a real one would help.
- Ticket status for blocked goals. `assets/ticket-template.md:17` hard-codes `status: ready`, but SKILL.md asks for "one file per ready goal" while the user asked for tickets for all phase 1 goals. I wrote all 28 and used `status: blocked` where prerequisites are unmet.
- The ticket template's `estimate:` block (`assets/ticket-template.md:11-15`) has no `wait_days`, but the script reads it (`scripts/check_schedule.py:24,96`). I added `wait_days` to the tickets.
- `references/delivery-profiles.md:168` uses `$SKILL_DIR`, which is not defined anywhere. I substituted the real path.
- `references/delivery-profiles.md:199-200`: the default `python3` here was 3.9, so I had to look for 3.11+ myself. It was found, so the schedule *was* checked.

**Heavier than needed**

- `SKILL.md:86` asks for every template section to be filled at production profile, and `references/delivery-profiles.md:150-153` keeps full goal sections in the plan plus tickets that copy figures and acceptance. With 28 goals, the plan and tickets duplicate a lot of text (~22k words across the three documents). Generating both from one data file was the only practical way to keep them consistent.
- Getting the calendar to fit took five planning iterations with the helper. Each was justified, and the rule at `references/delivery-profiles.md:189-194` to run every remedy as a what-if made the slip honest, but it is slow.

**Genuinely helpful**

- `SKILL.md:123` (Assumed answers table for a headless run) gave a clean way to record the unanswered questions.
- `scripts/check_schedule.py` found that the part-time security reviewer and external waits, not engineer hours, decide the GA date. The review-ratio check (`scripts/check_schedule.py:170-174`) also stops review hours being set by a flat ratio.
- `references/delivery-profiles.md:184-194` (only true changes, what-ifs for every remedy, "say when only moving the date does") produced the honest recommendation.
- `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json:13-15` showed that `gemini-3.7-flash` and `gemini-3.6-flash` retire on Vertex before the GA date. Picking from memory would have designed in a retirement.
- `references/design-decisions.md:182-196` (lethal-trifecta split) led directly to D3: no write tool in the agent, and confirmation runs through ordinary code. `references/failure-review.md:30` (provider commits, reply lost) shaped the operation-record design.
- `SKILL.md:196` (use the ADK version named in the specialists' compatibility files as the working assumption) settled the version question without network access.

## 6. Next prompt the skills told the user to type

`SKILL.md:274-280` says to end with the exact prompt for the next ready goal. Following the plan template's resume block (`assets/implementation-plan-template.md:139-145`), the prompt given is:

```text
/adk-engineer Carry out G01 from docs/plans/home-claim-intake.md.
Read docs/architecture/home-claim-intake.md and preserve its decisions.
Use adk-workflow-design with adk-tool-interface-design and adk-memory-architecture.
Work locally only (no cloud, no Guidewire), verify the acceptance cases, and update
the plan with actual evidence and remaining blockers.
```

The skill's own literal example (`SKILL.md:279`) is `/adk-engineer Carry out G01 from docs/plans/<topic>.md.`

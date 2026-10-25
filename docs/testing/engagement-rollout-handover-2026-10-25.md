# Engagement scoping, rollout pack and operations handover: testing record

Date: 25 October 2026. Branch `engagement-rollout-handover`. Research:
[engagement-rollout-handover-2026-10-25.md](../research/engagement-rollout-handover-2026-10-25.md).

## What changed

| Skill | Added | Changed |
| --- | --- | --- |
| adk-system-designer | `references/engagement-scoping.md`; `assets/statement-of-work-template.md`, `change-request-template.md`, `data-request-letter.md`; `scripts/check_sow.py` (imports `check_schedule.py` from the same directory); `tests/test_check_sow.py` (16 tests) | Description (adds proposal, SOW, change request); one scope-gate question; statement of work, rollout and handover goals at the phase boundaries; a pointer to the reference; three rows in the delivery-profiles starting points; one paragraph in the plan template |
| adk-presenter | `references/rollout-and-adoption.md`; `assets/rollout-pack-template.md`; `scripts/check_rollout.py`; `tests/test_check_rollout.py` (11 tests) | Description (adds the go-live rollout pack); a "Rollout pack at go-live" section |
| adk-agent-observability | `references/operations-handover.md`; `assets/handover-template.md`, `agent-postmortem-template.md` | Description (adds handover and postmortems); mode (f); one line in the debugging runbook's close-the-loop step; sources table |
| adk-engineer | | Three routing rows (engagement scoping, rollout pack, handover); the presenter goal completion clause |
| evals | 7 activation cases (4 positive, 3 near-miss), 3 scenarios | |

No new package; skill counts unchanged.

## Automated checks

`.venv/bin/python scripts/check_repo.py` from the worktree root: exit 0.
All 23 packages valid; evaluation case structure valid; 813 tests passed,
60 skipped (59 optional SDK checks in the auth, optimisation and guardrails
suites, one pytest skip in memory). The new suites: `test_check_sow.py`
16 passed (hand-computed fixture: phase 1 goals 4-6 + 2-4 + 3-5 = 9-15 h, at
£100 an hour £900-£1,500), `test_check_rollout.py` 11 passed.

## Fresh-agent trials

Fixture: a synthetic insurer ("Harbour Mutual", claims-status assistant for
48 handlers in the UK and Ireland) at
`/private/tmp/claude-501/engagement-trials/fixture/`: a discovery brief with
outcome measure, baseline and counter-metric; a design with contracts C1-C6,
deferred controls and an observability section whose alerts notify the
agency's own list; a plan with a schedule block (waits W1-W2, goals
G01-G10), evidence records M1-M3 and I1 dated after the session date, a
cost ledger and a Later list. Each trial ran in a fresh general-purpose
subagent (same model as this session) in its own copy, given only the
absolute SKILL.md path and the request; no expected answers.

The first three runs (`t1-sow`, `t2-rollout`, `t3-handover`) were cut off by
an API usage limit before writing any file; they are kept as empty
directories and not counted. The reruns (`*-r2`) are below.

| Trial | Request | Output | Check | Ease |
| --- | --- | --- | --- | --- |
| 1 | "Draft the SOW for the client from these documents, our rate is £95/h." | `t1-sow-r2/docs/engagement/claims/sow.md`: 6 deliverables, 13 acceptance criteria, 10 dated dependencies, fees £5,890-£9,310 for 62-98 h (arithmetic checked by hand), AI terms checklist, six open decisions | `check_sow.py` exit 1 on the first run (two presentation criteria without a comparator), exit 0 after rewording; rerun independently: exit 0 | 4/5 |
| 2 | "We go live in two weeks — prepare the rollout pack." | `t2-rollout-r2/docs/rollout/claims/rollout-pack.md`: every statement cites C1-C5, accuracy only from M1-M3, disclosure `applies` (Dublin team), active user defined, feedback mapped to record categories | `check_rollout.py` exit 0 in the trial; after this round's checker change, exit 1 because its exit thresholds were never agreed (the trial itself flagged them as proposals) | 4/5 |
| 3 | "Hand over to the client's IT team and write the postmortem template." | `t3-handover-r2/docs/operations/claims/handover.md` and `postmortem-template.md`: one-accountable RACI, eight runbook entries, five blockers | No checker; read by hand: alert channel flagged (B2), missing telemetry-stopped alert (B3), token rotation (B4) | 4/5 |

Findings that were not planted deliberately: trials 1 and 3 both read the
model lifecycle table and found that the pinned `gemini-3.6-flash` retires
on Vertex AI on 19 November 2026, mid-pilot (table checked 8 October 2026;
not refreshed). Trial 1 also found that the plan's production-decision
presentation (G07) depends on deployment (G05), not on the pilot (G06)
whose evidence it presents; this is a fixture defect the schedule check
does not detect.

## Friction log and fixes

| # | Trial | Friction | Fix |
| --- | --- | --- | --- |
| 1 | 1 | Plan lacked counts for forbidden-effect criteria; no rule for proposing them | Reference: put gaps in a new **Open decisions before sending** section, mark proposed figures `†` |
| 2 | 1 | Dependency dates need a start date; the schedule check gives working days | Reference and template: state the assumed start date and convert |
| 3 | 1 | Schedule check misses a presentation scheduled before its evidence | Not fixed (designer's plan tooling, outside this change) |
| 4 | 1 | No acceptance form for presentation deliverables; "0 uncited claims" rejected | Reference and template example; `check_sow.py` accepts a leading zero count (new test) |
| 5 | 1 | Criteria with no contract | Reference: write `none (<why>)` |
| 6 | 1 | Supplied plan lacks SOW and go-live goals | Reference: add them with the user before pricing, or list as open decision |
| 7 | 1 | Unclear whether to write the data request letter now | Reference and template: draft it with the SOW when a dependency is data or access |
| 8 | 1 | No place for assumed answers that block sending | Template: open decisions section |
| 9 | 1 | No defaults for pricing basis, VAT, one rate | Reference: labelled defaults when the user cannot be asked |
| 10 | 2 | Change-table format and relative-date conflicts with the record | Reference: assumed date stated at the top; change-table columns not defined (left to the plan template) |
| 11 | 2 | Finish section written for decks | SKILL.md: rollout-specific finish |
| 12 | 2 | Unclear whether "read the record" applies | SKILL.md: it does; stage and audience lines do not |
| 13 | 2 | Sponsor message: to or from the sponsor | Reference and template: a briefing to the sponsor and the announcement they send |
| 14 | 2 | Exit-test row for handover acceptance missing from the template | Template row added |
| 15 | 2 | No route when no handover exists | Reference: default tiers marked assumed, listed as a gap |
| 16 | 2 | Placeholders outside tables pass; proposed thresholds pass as agreed | `check_rollout.py`: whole-text placeholder scan; exit test must say "Agreed with <name> on <date>" or "Status: proposed" (note); assumptions section required (two new tests) |
| 17 | 2 | Internal tools and edited drafts under Article 50 | Reference: disclose anyway; Article 50(2) marking for drafts marked `verify` for counsel |
| 18 | 2 | No default adoption targets | Not changed: targets are agreed with the sponsor, not defaulted |
| 19 | 3 | Session's skill catalogue showed the old description | Not a package defect: the trial host listed the installed copy, not the worktree |
| 20 | 3 | "Write the postmortem template" ambiguous | Reference: project copy path and pre-filled content |
| 21 | 3 | Inspect steps assume code | SKILL.md: mode (f) on documents only skips them, labels inventory unverified |
| 22 | 3 | Handover needs the rollout pack's exit test | Reference: list it as a blocker with its goal |
| 23 | 3 | Lifecycle dates offline; which platform's date | Reference and template: serving platform's date, `refresh before relying` |
| 24 | 3 | Breach notification UK only | Reference and template: EU lead supervisory authority (GDPR Article 33, verify), sector regulators |
| 25 | 3 | RACI lacks the DPO | Template: Client DPO column and breach-decision row |
| 26 | 3 | Severity gap for a wrong draft caught by review | Template: Sev3 example |
| 27 | 3 | Unverifiable alerts unlabelled | Reference: `unverified: from the design` |
| 28 | 3 | `gcloud` example beside "commands belong to other skills" | Not changed: a verification example, not a recipe |

23 of 28 fixed, one partly (10), four not changed with reasons (3, 18, 19, 28).
The fixes were not re-trialled.

## Not established

- Natural activation of the changed descriptions: cases authored, not run.
- No baseline condition: the trials show the skills can be followed, not
  that they beat writing these documents without them.
- Legal content (MCC-AI, AI Act, GDPR, ICO) is cited, not reviewed by counsel.
- GDPR Article 33 text was not re-read on EUR-Lex (automated fetches got an
  empty challenge page); marked "verify" where used.

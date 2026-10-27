---
stage: value-report
period: 2026-09
title: Claims triage assistant value report, September 2026
sources: docs/discovery/claims.md, docs/plans/claims.md
decider: Helen Okafor
date: 2026-10-28
call: continue
---

# Claims triage assistant: September 2026

One page for the sponsor. Every figure cites a measurement (`M<n>`) or incident (`I<n>`) record in the plan; a line that opens with *Estimate*, *Target* or *Threshold* may cite the plan's cost contract or the brief instead. This report is late: September's call was due at month end and is dated 2026-10-28; the late month is recorded in the plan's change table.

**Bottom line:** Median triage time on pilot claims was 13 minutes against a baseline of 21 (M2, M1), beyond the margin but short of the 12-minute target, and September's re-routing rate was not measured, so the call is continue, with the counter-metric measured first.

## Outcome against baseline

- Median triage time per claim: 13 minutes against a baseline of 21 minutes (M2 against M1; M2 window 2026-09-01 to 2026-09-30, sample 1,184 pilot claims, claims MI report; M1 window 2026-08-01 to 2026-08-22, sample 400 new home claims, claims MI report). Both cover new home claims, the whole pilot scope.
- An 8-minute fall on these samples is far beyond the margin (about 1 over the square root of 400, roughly 5% of the median). *Target* 12 minutes or less (brief §4): not yet met, 1 minute over. The build is v1.0.3; the baseline predates the pilot, so this is a before and after comparison, not a controlled one.

## Counter-metric

- Re-routing rate after triage: not measured for September. The only record, 8.6% against 9% (M3), covers 2026-08-25 to 2026-08-31 on 236 claims (build v1.0.1), so it is last period and a different build; the 0.4-point gap is within the margin. No September figure exists; G09 (proposed, not yet in the plan) would measure it from the claims MI report for 2026-09-01 to 2026-09-30.

## Adoption

- Active means a handler opened a draft on 5 or more claims in a week, in every week of the month.
- 12 of 14 pilot handlers were active (M5), 86%. Drafts accepted without change: 69% of 1,184 (M4), so 31% were edited or replaced by the handler. Interpretation of the two inactive handlers is not recorded.

## Cost per outcome

- Actual: £0.43 per pilot claim triaged with a draft: £512 (M6: Cloud Billing export filtered to app=claims-triage; Vertex AI, Cloud Run, Cloud SQL, BigQuery, so it includes fixed costs and leaves out Larkspur's staff time) over 1,184 claims (M7). We estimate this by dividing £512 by 1,184. Cost per accepted-unchanged draft (about 817 drafts, 69% of 1,184) would be about £0.63; we estimate this and the accepted count is derived, not recorded.
- Estimate: £0.75 per claim, the £900 monthly ceiling (brief §6) over about 1,200 claims a month (brief §6). Actual is below it because spend was £512, 57% of the ceiling, at 1,184 claims.
- The plan's M8 (£0.31 per claim at 4,800 claims, assumption) is not used: its stated method, M6 with fixed costs unchanged, gives at most £512 / 4,800 = £0.11, so the record and its method disagree. Not reported until the analyst reconciles it.

## Incidents

- I1: 2026-09-16, severity 2, 37 drafts cited a clause from a superseded wording version; drafts withheld for two hours and handlers triaged by hand; wording index rebuilt with a version filter and a C2 test added for superseded wordings; closed on 2026-09-19.

## Thresholds

| Threshold sentence (brief §4) | This period | Fired |
| --- | --- | --- |
| If the median triage time on pilot claims is above 15 minutes after four pilot weeks, we will stop the pilot and review the drafts with the team leads | 13 minutes (M2) | no |
| If the re-routing rate rises above 9% in any month, we will pause the assistant's urgency field until the cause is found | not measured for September; last period 8.6% (M3) | unknown |

## Call: continue

Helen Okafor decides by 2026-11-04 (assumed; see questions). Continue is recommended: the stop threshold did not fire (M2), but the second threshold cannot be shown as clear and the 12-minute target is not met. Options: stop (frees about £512 a month, M6, and returns 14 handlers to the 21-minute process, M1), continue (next month must show a September-comparable re-routing rate at or below 9%, median at or below 12 minutes, and no new severity 1 or 2 incident), scale (to motor or other queues: not recommended, as the counter-metric is unmeasured for the month and no scale trigger is agreed in the plan; any scaled cost per claim needs M8 reconciled first).

## Questions, assumptions and gaps

- Q: who owns the September re-routing figure and when? Assumed the claims MI analyst (owner of M3), requested before the decision; until then the urgency-field threshold is reported as unknown, not as clear.
- Q: what decision date applies? Not in the record; assumed one week after this report (2026-11-04).
- Q: is M8 correct? Not yet raised; Sara Lin wrote the G07 records and is the person to ask.

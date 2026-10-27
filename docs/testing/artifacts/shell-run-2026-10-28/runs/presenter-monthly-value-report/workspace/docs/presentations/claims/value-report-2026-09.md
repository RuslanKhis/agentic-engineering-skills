---
stage: value-report
period: 2026-09
title: Claims triage assistant value report, September 2026
sources: docs/discovery/claims.md, docs/plans/claims.md
decider: Helen Okafor
date: 2026-11-04
call: continue
---

# Claims triage assistant: September 2026

One page for Helen Okafor. Report written late (28 October 2026); the call date above is an assumption, see the plan's change table.

**Bottom line:** Median triage time fell to 13 minutes against a 21-minute baseline (M2, M1), but the re-routing counter-metric has no September measurement (last period, M3, covers only 25-31 August), so we recommend continue, not scale.

## Outcome against baseline

- Median triage time per claim: 13 minutes on pilot claims against a baseline of 21 minutes (M2, M1; pilot window 2026-09-01 to 2026-09-30, 1,184 claims; baseline window 2026-08-01 to 2026-08-22, 400 new home claims; both from the claims MI report, same definition and scope).
- The fall from 21 to 13 minutes (M1, M2) is far beyond the margin on these samples (about 1 over the square root of 1,184, roughly 3% of the median). Target: 12 minutes or less (brief §4), so the target is not yet met.

## Counter-metric

- Re-routing rate after triage: not measured for September. Last period (2026-08-25 to 2026-08-31, 236 claims, build v1.0.1) it was 8.6% against a 9% baseline (M3), a 0.4-point gap within the margin of that sample and on an earlier build. G09 (added to the plan) measures September.

## Adoption

- Active means a handler who opened a draft on 5 or more claims in a week, in every week of September.
- 12 of 14 pilot handlers were active (M5), 86%; 69% of 1,184 drafts were accepted without change (M4).

## Cost per outcome

- Actual: £0.43 per claim triaged: £512 (M6: Cloud Billing export, rows labelled app=claims-triage; Vertex AI, Cloud Run, Cloud SQL, BigQuery; leaves out Larkspur build and support time) over 1,184 claims triaged with a draft (M7); we estimate £512 / 1,184 = £0.43. This is within the £900 a month pilot ceiling (brief §6).
- Estimate: £0.31 per claim at 4,800 claims a month (M8, an assumption, not measured; plan cost contract). We could not reproduce it: £512 spread over 4,800 claims with fixed costs unchanged is about £0.11, and £0.31 a claim at 4,800 would be about £1,490 a month. The plan's figure needs its derivation before it is used; the 4,800 volume is not in the brief (about 1,200 a month in the pilot queue).

## Incidents

- I1: 2026-09-16, severity 2, 37 drafts cited a clause from a superseded wording version; drafts withheld for two hours and handlers triaged by hand; wording index rebuilt with a version filter and a C2 test added; closed 2026-09-19.

## Thresholds

| Threshold sentence (brief §4) | This period | Fired |
| --- | --- | --- |
| If the median triage time on pilot claims is above 15 minutes after four pilot weeks, we will stop the pilot and review the drafts with the team leads | 13 minutes (M2) | no |
| If the re-routing rate rises above 9% in any month, we will pause the assistant's urgency field until the cause is found | not measured for September (last period 8.6%, M3) | unknown |

## Call: continue

Helen Okafor decides by 2026-11-04 (assumed date). We recommend continue: the stop threshold did not fire and cost is inside the ceiling, but scale needs the September re-routing rate. Options: stop (frees about £512 a month (M6) plus the retained Cloud SQL instance), continue (October must show the re-routing rate at or under the 9% baseline (brief §4), triage time at 12 minutes or less (M2), and the derivation of the cost estimate), scale (to full home volume; we cannot state the cost per claim at that scope until the plan's estimate is derived, and it needs the September re-routing rate).

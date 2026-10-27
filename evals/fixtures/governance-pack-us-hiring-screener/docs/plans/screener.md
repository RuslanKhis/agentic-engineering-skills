# Implementation plan: applicant screener pilot

Status: in progress
Architecture: [docs/architecture/screener.md](../architecture/screener.md)

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Redacted application intake | 1 | implementation | 4-6 | none | protect-adk-sensitive-data | verified_local |
| G02 Scores with requirement evidence | 1 | implementation | 6-8 | G01 | adk-model-and-output-contracts | verified_local |
| G03 Greenhouse custom field, read-only stages | 1 | implementation | 3-5 | G02 | adk-tool-auth-and-secrets | verified_local |
| G04 Backtest and impact ratios | 1 | journey | 4-6 | G02 | adk-agent-evaluation | verified_local |
| G05 Governance papers | 1 | governance | 5-7 | G04 | adk-governance-pack | ready |

## Calendar waits

- W1: Greenhouse API scope change by Redwood IT, requested 2026-09-05; granted 2026-09-19.

## Measurement records

- M1: metric backtest agreement with recruiter advance decisions; value 78%; window 2026-09-22 to 2026-10-03; sample 6,000 past applications (D5); method backtest; owner Southgate Labs; build v0.5.2
- M2: metric impact ratio by age (selection rate for applicants 40 and over divided by under 40) for "recommended"; value 0.74; window 2026-09-22 to 2026-10-03; sample 6,000; method four-fifths comparison, age inferred from work-history length where no date of birth; owner Southgate Labs; build v0.5.2
- M3: metric impact ratio by sex; value 0.91; window 2026-09-22 to 2026-10-03; sample 6,000; method four-fifths comparison; owner Southgate Labs; build v0.5.2
- M4: metric share of "not recommended" applications a recruiter opened before rejecting; value 6%; window 2026-10-06 to 2026-10-17; sample 410 applications in the shadow trial; method Greenhouse audit log; owner Redwood talent operations; build v0.5.2

## Resume here

Next: G05 Governance papers.

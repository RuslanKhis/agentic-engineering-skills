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
- W2: General Counsel (Monica Alvarez) review and sign-off of the G05 governance drafts in docs/governance/screener/; to be requested the day the drafts are sent; needed before the California pilot decision of 2026-11-18.
- W3: Redwood completes and approves the California CPPA risk assessment (approver to be named), using the input pack; needed before pilot processing starts.
- W4: Only if Redwood decides to use the screener on New York City candidates: independent bias audit, published summary and candidate notice 10 business days before use (NYC Local Law 144); blocks any New York use.
- W5: Redwood updates its applicant privacy notice and prepares the ADMT pre-use notice and opt-out or human-appeal route; needed before 2027-01-01 if the pilot runs past that date.

## Measurement records

- M1: metric backtest agreement with recruiter advance decisions; value 78%; window 2026-09-22 to 2026-10-03; sample 6,000 past applications (D5); method backtest; owner Southgate Labs; build v0.5.2
- M2: metric impact ratio by age (selection rate for applicants 40 and over divided by under 40) for "recommended"; value 0.74; window 2026-09-22 to 2026-10-03; sample 6,000; method four-fifths comparison, age inferred from work-history length where no date of birth; owner Southgate Labs; build v0.5.2
- M3: metric impact ratio by sex; value 0.91; window 2026-09-22 to 2026-10-03; sample 6,000; method four-fifths comparison; owner Southgate Labs; build v0.5.2
- M4: metric share of "not recommended" applications a recruiter opened before rejecting; value 6%; window 2026-10-06 to 2026-10-17; sample 410 applications in the shadow trial; method Greenhouse audit log; owner Redwood talent operations; build v0.5.2

## Resume here

Next: G05 Governance papers.

G05 evidence: drafted, not sent. Drafts are in docs/governance/screener/ (regulatory memo, privacy impact input pack, impact assessment, system card, security questionnaire); regimes in scope: au (consultancy handling only), us. The plan has no pilot-approval goal; W2, W3 and W5 should block one, and W4 blocks any New York use.

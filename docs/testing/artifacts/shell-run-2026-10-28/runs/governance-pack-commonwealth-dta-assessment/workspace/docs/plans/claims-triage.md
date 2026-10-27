# Implementation plan: claims triage assistant pilot

Status: in progress
Architecture: [docs/architecture/claims-triage.md](../architecture/claims-triage.md)

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Draft with cited passages | 1 | implementation | 6-8 | none | adk-model-and-output-contracts | verified_local |
| G02 Team-scoped, read-only case access | 1 | implementation | 4-6 | none | adk-tool-auth-and-secrets | verified_local |
| G03 Officer decision record | 1 | implementation | 2-4 | G01 | adk-fastapi-backend | verified_local |
| G04 Offline evaluation | 1 | journey | 4-5 | G01, G02 | adk-agent-evaluation | verified_local |
| G05 DTA impact assessment input and privacy papers | 1 | governance | 6-9 | G04 | adk-governance-pack | ready |

## Calendar waits

- W1: IRAP assessment of the hosting environment by the CCO's assessor, booked 2026-11-16.
- W2: PIA by the privacy officer before the pilot.
- W3: DTA AI impact assessment completed and approved by the CCO's assessing and approving officers, treatments applied, before the pilot deploys; assessments for in-scope use cases begin by 15 December 2026 (checked 2026-10-26).
- W4: Commonwealth AI Review Committee referral, only if the agency rates residual risk high or treats the use case as highly sensitive, novel or complex; before the pilot deploys.
- W5: APP privacy policy entries for automated decisions (APP 1.7 to 1.9), in force from 10 December 2026 (checked 2026-10-26), settled by the privacy officer with counsel before decisions made after that day.

## Measurement records

- M1: metric draft category matching officer decision; value 88%; window 2026-10-06 to 2026-10-17; sample 900 past claims (D5); method offline evaluation; owner Southgate Labs; build v0.6.3
- M2: metric draft priority matching officer decision; value 79%; window 2026-10-06 to 2026-10-17; sample 900; method offline evaluation; owner Southgate Labs; build v0.6.3

## G05 evidence

- Drafted, not sent. Documents in docs/governance/claims-triage/: regulatory-memo.md, privacy-impact-input-pack.md, impact-assessment.md, system-card.md, security-questionnaire.md, and four government-form-answers documents (DTA impact assessment tool, transparency statement, use case register, agentic addendum).
- Waits W3 to W5 were added by G05. The plan has no pilot-approval goal yet, so W1 to W5 must be added to the Depends on of that goal when it is created (gap).
- Regimes in scope: au only. Checker result and open gaps are in the closing summary of the drafting session (2026-10-28).
- Proposed goals from gaps: model page read (retirement date, processing region, provider data use) for adk-model-and-output-contracts; sensitive data screening on prompts and logs for protect-adk-sensitive-data; retention and erasure for decisions table and evaluation set; pilot override-rate and review-time measures and a fairness check for adk-agent-evaluation; incident procedure for adk-release-engineering; officer training and handover.

## Resume here

Next: G05.

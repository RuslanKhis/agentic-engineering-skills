# Implementation plan: customer service assistant pilot

Status: in progress
Architecture: [docs/architecture/service-assistant.md](../architecture/service-assistant.md)

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Own balances and transactions | 1 | implementation | 6-8 | none | adk-tool-auth-and-secrets | verified_local |
| G02 Confirmed card freeze | 1 | implementation | 4-6 | G01 | adk-operational-guardrails | verified_local |
| G03 Overdraft decline explanations | 1 | implementation | 5-7 | G01 | adk-model-and-output-contracts | verified_local |
| G04 Pseudonymised transcripts for support | 1 | implementation | 3-5 | G01 | protect-adk-sensitive-data | verified_local |
| G05 Pilot journey | 1 | journey | 4-5 | G02, G03, G04 | adk-agent-evaluation | verified_local |
| G06 Governance papers | 1 | governance | 6-8 | G05 | adk-governance-pack | ready |

## Calendar waits

- W1: model risk review by the bank's model risk team, booked for 2026-11-12.
- W2: DPIA sign-off by both DPOs before the pilot.
- W3: review of docs/governance/service-assistant/regulatory-memo.md and its counsel questions by Thamesbridge's UK and Irish counsel; requested the day the drafts go out; needed before the pilot decision on 2026-12-03.
- W4: transfer instruments and assessments for Southgate Labs access from Sydney to UK and EU personal data (UK IDTA or Addendum with the data protection test; EU Standard Contractual Clauses with a transfer impact assessment), executed before any Southgate Labs engineer reads production logs, traces or transcripts.
- W5: prior consultation with the Information Commission and the Irish supervisory authority, only if the DPIA (W2) records a high residual risk; the authority has up to eight weeks, extendable by six, so a start after 2026-10-28 cannot finish before 2026-12-03.
- W6: group CISO review and security approval of docs/governance/service-assistant/security-questionnaire.md; needed before the pilot decision on 2026-12-03.

## Measurement records

- M1: metric overdraft explanations matching the decision engine's reason codes; value 99.2%; window 2026-10-05 to 2026-10-16; sample 500 synthetic declined applications; method offline evaluation; owner Southgate Labs; build v0.8.0
- M2: metric freezes executed without confirmation; value 0; window 2026-10-05 to 2026-10-16; sample 300 scripted conversations; method scripted-model tests; owner Southgate Labs; build v0.8.0
- M3: metric resolved without transfer on the test journey; value 41%; window 2026-10-12 to 2026-10-16; sample 120 staff test chats; method chat platform; owner Thamesbridge customer operations; build v0.8.0

## G06 evidence

- Drafted, not sent: regulatory-memo.md, privacy-impact-input-pack.md, processing-records.md, transfer-assessment.md, impact-assessment.md, system-card.md and security-questionnaire.md in docs/governance/service-assistant/, all status draft with every sign-off pending.
- Regimes in scope: au (consultancy's own handling), eu, uk.
- Checker: not run (no shell in the drafting session); run `check_governance.py` on the directory with the three project records as sources before sending.
- Waits W3 to W6 added; the plan has no pilot-approval goal, so none is attached to a goal's "Depends on" yet.

## Resume here

Next: run the checker, then send the drafts to the reviewers (G06 stays ready until then).

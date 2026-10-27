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

## Measurement records

- M1: metric overdraft explanations matching the decision engine's reason codes; value 99.2%; window 2026-10-05 to 2026-10-16; sample 500 synthetic declined applications; method offline evaluation; owner Southgate Labs; build v0.8.0
- M2: metric freezes executed without confirmation; value 0; window 2026-10-05 to 2026-10-16; sample 300 scripted conversations; method scripted-model tests; owner Southgate Labs; build v0.8.0
- M3: metric resolved without transfer on the test journey; value 41%; window 2026-10-12 to 2026-10-16; sample 120 staff test chats; method chat platform; owner Thamesbridge customer operations; build v0.8.0

## Resume here

Next: G06 Governance papers.

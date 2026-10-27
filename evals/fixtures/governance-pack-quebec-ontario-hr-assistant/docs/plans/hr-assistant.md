# Implementation plan: HR assistant pilot

Status: in progress
Architecture: [docs/architecture/hr-assistant.md](../architecture/hr-assistant.md)

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Policy answers in French and English | 1 | implementation | 5-7 | none | adk-memory-architecture | verified_local |
| G02 Own leave requests | 1 | implementation | 3-5 | none | adk-tool-auth-and-secrets | verified_local |
| G03 Routine approval rule and manager routing | 1 | implementation | 4-6 | G02 | adk-operational-guardrails | verified_local |
| G04 Pilot journey | 1 | journey | 3-4 | G01, G03 | adk-agent-evaluation | verified_local |
| G05 Governance papers | 1 | governance | 5-7 | G04 | adk-governance-pack | ready |

## Calendar waits

- W1: UKG integration user, granted 2026-09-29.

## Measurement records

- M1: metric policy answers citing the right section; value 92%; window 2026-10-05 to 2026-10-16; sample 300 questions (150 French, 150 English); method offline evaluation; owner Southgate Labs; build v0.5.0
- M2: metric share of pilot-shape leave requests the rule approves without review; value 64%; window 2026-10-05 to 2026-10-16; sample 500 requests replayed from July 2026; method replay; owner Southgate Labs; build v0.5.0
- M3: metric dates and leave type extracted correctly; value 98.4%; window 2026-10-05 to 2026-10-16; sample 500; method replay; owner Southgate Labs; build v0.5.0

## Resume here

Next: G05 Governance papers.

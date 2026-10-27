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

## Measurement records

- M1: metric draft category matching officer decision; value 88%; window 2026-10-06 to 2026-10-17; sample 900 past claims (D5); method offline evaluation; owner Southgate Labs; build v0.6.3
- M2: metric draft priority matching officer decision; value 79%; window 2026-10-06 to 2026-10-17; sample 900; method offline evaluation; owner Southgate Labs; build v0.6.3

## Resume here

Next: G05.

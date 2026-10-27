# Implementation plan: Tidewater claims assistant

Status: in progress
Architecture: [docs/architecture/claims.md](../architecture/claims.md)
Continuation source of truth: this plan and the tickets under `docs/tickets/claims/`

## Goals and dependencies

| ID and goal | Phase | Type | Human hours | Depends on | Primary skill | State |
| --- | --- | --- | --- | --- | --- | --- |
| G01 Claim status and notes with owner checks | 1 | implementation | 3-4 | none | adk-tool-auth-and-secrets | verified_local |
| G02 Recall what the policyholder said before | 1 | implementation | 4-6 | G01 | adk-memory-architecture | verified_local |
| G03 Policy answers from the policyholder's wording | 1 | implementation | 4-6 | G01 | adk-memory-architecture | ready |
| G04 Photo upload to a claim | 1 | implementation | 2-4 | G01 | adk-fastapi-backend | ready |
| G05 No payout promises | 1 | implementation | 2-3 | G01 | adk-agent-security | ready |
| G06 Spend cap | 1 | implementation | 1-2 | none | adk-operational-guardrails | ready |
| [G07 Portability assessment for the CTO](../tickets/claims/G07.md) | 1 | portability | 3-5 | none | adk-portability-planning | ready |

## Evidence so far

- G01: C1 evidenced, local, A1 and A2 (`python -m unittest tests.test_claims`), 2026-10-09.
- G02: C2 evidenced, local, A1 to A3 (scripted-model Runner tests with
  `InMemoryMemoryService`), 2026-10-16; live recall on the dev Agent Engine not run.

## Resume here

Ready: G03, G04, G05, G06, G07.

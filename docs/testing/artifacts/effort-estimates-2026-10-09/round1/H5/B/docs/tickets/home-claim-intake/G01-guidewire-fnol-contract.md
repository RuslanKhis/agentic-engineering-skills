---
goal: G01
title: Pin down the Guidewire FNOL and document contract
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 22-36
  review_and_verify: 8-14
  total: 30-50
  calendar_waits: Guidewire sandbox access and integration client from the Guidewire team (2-4 weeks); start in week 1
owner: E1 (integration)
status: ready
---

# G01 Pin down the Guidewire FNOL and document contract

## Outcome

The team knows exactly how to create a homeowners FNOL, attach documents, and detect a duplicate or find a claim after a lost reply, with recorded sandbox fixtures the offline tests replay. Implements D7, D8, D10, O1; A2.

## Scope

- In: ADR `docs/architecture/adr-001-guidewire-fnol.md`: endpoint(s) and API version, required homeowners FNOL fields and code lists, mapping from the draft fields, channel `digital-assistant` and AI-suggested labelling (D10), idempotency support and its key retention, lookup by external reference, document upload limits, rate limits, auth flow, error codes; recorded request/response fixtures (sanitised) under `tests/fixtures/guidewire/`.
- Out: Adapter code (G10), attachment operations (G11).
- Depth: Production: decides the replay contract for I2. Floor: sandbox only, no production calls, credentials never in fixtures.
- Route: Ordinary Python REST client later; this goal only reads Guidewire documentation, talks to the Guidewire team and makes bounded sandbox calls.
- Supporting skills: `adk-tool-auth-and-secrets` (client-credentials flow and where the secret lives)
- Execution scope: Reading and writing the ADR and fixtures is authorized; sandbox calls need the sandbox URL and test client from the Guidewire team.

## Acceptance

- [ ] ADR answers every question in O1 with sandbox evidence or an explicit 'not supported'
- [ ] Fixtures include success, validation error, auth failure, timeout-after-commit simulation notes and a duplicate attempt
- [ ] Decision recorded: idempotency key, external-reference lookup, or manual reconciliation for uncertain creates
- [ ] No credential, token or real customer data in the repository (secret scan clean)

Verification: Bounded live: sandbox calls with a named test policy, at most 50 requests; recorded fixtures replayed by a schema check offline.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G01-guidewire-fnol-contract.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

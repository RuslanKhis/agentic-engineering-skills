---
goal: G02
title: "We have a documented ClaimCenter contract and have requested sandbox access"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 6-10
  review_and_verify: 1-2
  total: 7-12
  calendar_waits: none
  wait_days: 0
owner: Integration eng
status: ready
---

# G02 We have a documented ClaimCenter contract and have requested sandbox access

## Outcome

On day one, sandbox credentials and the ClaimCenter reference-field change are requested; a contract document and fixtures from Guidewire documentation let G10 build against a fake while the sandbox wait (G25) runs. Implements D4, O1; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g02--we-have-a-documented-claimcenter-contract-and-have-requested-sandbox-access).

## Scope

- In: Raise the access and extension-field requests first; read Guidewire Cloud API docs; write the contract (create/submit, documents, replay header, lookup, errors, limits) and doc-derived fixtures, each marked 'from docs, unverified'.
- Out: Sandbox calls (G25); production code (G10).
- Depth: Discovery with a stopping condition: stop when each contract question has a documented answer or is marked 'unknown, verify in G25'.

## Acceptance

- [ ] Access and extension-field requests raised, with ticket references recorded.
- [ ] Contract answers recorded for create/submit, required fields, replay header and key retention, reference lookup, document upload limits and error codes, each marked documented or unknown.
- [ ] Fixtures exist for success, validation error, 429 and 5xx.

Verification: Document review; no live calls. Execution scope: No external calls; raising internal requests only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G02-guidewire-contract-from-docs.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

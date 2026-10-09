---
goal: G02
title: We know exactly how Guidewire lets us create one claim with photos and recover from a lost response
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: production
estimate: 24-40 h
status: ready
---

# G02 We know exactly how Guidewire lets us create one claim with photos and recover from a lost response

## Outcome

A written Guidewire contract note answers the questions that decide I3: draft-claim create/submit, document upload limits, idempotency key support, lookup by an external reference, rate limits, auth scopes, sandbox access and CIAM subject → Guidewire account mapping. Implements D3, D5, I3, I4 in the design.

## Scope

- In: `docs/integration/guidewire-contract.md` with cited Guidewire documentation (version, date) and sandbox observations; a recorded set of request/response fixtures for the fake (no credentials).
- Out: Building the adapter (G11).
- Depth: Discovery: stops when each question has a cited answer or a named owner and date; does not write any production claim.
- Route: Guidewire Cloud API documentation for the tenant's release; read-only sandbox calls if access is granted.
- Prerequisites: Guidewire team contact; sandbox tenant and documentation access (Q6).
- Supporting skills:
  - `adk-tool-auth-and-secrets`: Guidewire OAuth client-credential model and scope separation (read vs write)
- Execution scope: Requires Guidewire sandbox access and documentation granted by the Guidewire team; sandbox read calls and at most a handful of sandbox draft-claim creates if the user authorises them.

## Acceptance

- [ ] Each of the seven questions has an answer with source and date, or an owner and due date.
- [ ] The note states the replay contract chosen for I3 (idempotency header, lookup by external reference, or manual reconciliation) and what G10/G11 must implement.
- [ ] Forbidden: no write to any non-sandbox Guidewire environment; no credential committed.

Verification: Document review by the Guidewire team owner and the security reviewer; sandbox fixtures stored under `tests/fixtures/guidewire/` without secrets.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G02-guidewire-contract-discovery.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

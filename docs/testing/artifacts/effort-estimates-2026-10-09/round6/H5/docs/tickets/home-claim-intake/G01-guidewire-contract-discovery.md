---
goal: G01
title: Know exactly how to create one claim safely in ClaimCenter
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 9-15
  review_and_verify: 3-5
  total: 12-20
  calendar_waits: Guidewire sandbox tenant and API client from the Guidewire platform team
  wait_days: 5-10
owner: Dev B
status: ready
---

# G01 Know exactly how to create one claim safely in ClaimCenter

## Outcome

A recorded decision on how a claim is created, made replay-safe and found again, backed by sandbox calls. Implements D4, I2, I5; open decision 1; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: Cloud API claim creation (draft then submit or single call), required FNOL fields per loss cause, mapping from the draft schema, documents endpoint and size limits, replay/idempotency mechanism, lookup by external reference, OAuth2 client credentials, rate limits. Record in `docs/architecture/decisions/guidewire-contract.md`.
- Out: Adapter code (G13).
- Depth: Production depth for the external-write contract; floor: sandbox only, a dedicated test policy.

## Acceptance

- [ ] Decision record lists endpoints, payload fields and the field mapping from the draft schema.
- [ ] Sandbox evidence: the same create request sent twice with the same replay key yields one claim; or the absence of a replay contract is recorded with the chosen fallback (lookup by external reference before any retry).
- [ ] No credential, token or claim personal data appears in the repository or the record.

Verification: Authorised live: Guidewire sandbox only, at most 20 test claims on a test policy.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G01-guidewire-contract-discovery.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

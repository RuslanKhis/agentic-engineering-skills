---
goal: G39
title: Real tokens from the customer identity provider are accepted and scoped correctly
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: []
blocked_by: [G03, W9]
phase: 1
profile: production
estimate:
  hands_on: 2-3
  review_and_verify: 1-1
  total: 3-4
  calendar_waits: none
owner: Eng E
status: proposed
---

# G39 Real tokens from the customer identity provider are accepted and scoped correctly

## Outcome

Split from G03 after the independent review, so G03 can start on locally signed tokens while the CIAM test tenant and client registration (W9) are pending.

## Scope

- In: configuration for the CIAM test tenant; one end-to-end sign-in.
- Out: everything G03 already tests offline.
- Depth: production.

## Acceptance

- [ ] A1 A token from the CIAM test tenant yields `customer_id` = its verified `sub`; issuer, audience and signing keys match configuration.
- [ ] A2 The access-token lifetime configured in the CIAM is recorded; it is the bound on how long a revoked token still works (assumed ≤ 5 minutes).

Verification: local integration against the CIAM test tenant.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G39-ciam-tenant-check.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

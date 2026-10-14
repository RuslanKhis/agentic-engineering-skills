---
goal: G03
title: Only the signed-in customer can see or change their claim draft
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-frontend-integration]
blocked_by: [G02]
phase: 1
profile: production
estimate:
  hands_on: 10-15
  review_and_verify: 6-9
  total: 16-24
  calendar_waits: none
owner: Eng E
status: proposed
---

# G03 Only the signed-in customer can see or change their claim draft

## Outcome

Every route verifies the customer's OIDC access token and scopes all reads
and writes to the verified subject. Implements D6 and invariant I1.
Handoff: 1 h from Eng A on the skeleton.

## Scope

- In: `app/api/auth.py` middleware (issuer, audience, signature, expiry,
  cached JWKS), `customer_id` placed in trusted session state at invocation
  start; ownership checks on turns, history, upload URL, summary, confirm,
  status and delete routes; a per-draft lock so one turn runs at a time.
- Route: draft and session lookups always filter by `customer_id`; a missing
  or foreign draft returns 404 before the Runner starts.
- Out: policy selection (G04), screening (G12).
- Depth: production; cross-customer denial tests on every route.

## Acceptance

- [ ] A1 A valid locally signed test token yields `customer_id` = verified `sub`; no request field can set it (the real CIAM tenant is checked in G39).
- [ ] A2 Customer B calling any draft route with customer A's draft ID gets 404 with no data, and the scripted model records zero calls.
- [ ] A3 An expired token returns 401 with no state change; after the portal refreshes the token, the same draft continues. A revoked token stops working at its expiry; that lifetime bound is recorded in G39.
- [ ] A4 Tools read customer and draft only from trusted state; a scripted model that tries to pass another customer's or policy's ID finds no such parameter and the draft of the other customer is unchanged.
- [ ] A5 A second turn sent while one is running on the same draft returns 409 `turn_in_progress`; no duplicate events are stored; a resend with the same client message ID returns the first turn's result.
- [ ] A6 A forged or malformed token (wrong issuer, `alg: none`, bad signature, wrong audience) returns 401.
- [ ] A7 A token with an unknown `kid` while the JWKS endpoint is unavailable (including at cold start) returns 401 and raises an alert; the JWKS fetch is retried with a bound, never skipped.

Verification: offline — `pytest tests/auth` with locally signed test tokens
and a fake JWKS.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G03-identity-and-ownership.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

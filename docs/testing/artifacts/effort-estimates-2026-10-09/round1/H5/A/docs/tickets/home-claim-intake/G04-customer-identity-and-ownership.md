---
goal: G04
title: A signed-in customer can reach only their own conversations, drafts and photos
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-frontend-integration]
blocked_by: [G01]
phase: 1
profile: production
estimate: 40-64 h
status: blocked
---

# G04 A signed-in customer can reach only their own conversations, drafts and photos

## Outcome

The API verifies the CIAM OIDC token on every route, derives `customer_id` and enforces ownership of sessions, drafts, uploads and status; the session's `user_id` is the verified customer. Implements D3, I1 in the design.

## Scope

- In: JWT verification middleware with JWKS caching; `customer_id` derivation; ownership checks in repositories; 404 on foreign resources; per-session turn serialisation (409 on overlap); cross-customer denial tests for every route.
- Out: Policy lookup through Guidewire (G05 uses the G02 mapping), frontend sign-in UI (existing portal).
- Depth: Build: production identity; floor: no tokens or subjects in logs beyond a hashed ID.
- Route: FastAPI dependency in `app/api/auth.py`; `request.state.customer_id` passed to Runner as `user_id` and into session state by trusted code only.
- Prerequisites: G01; CIAM issuer, audience and JWKS URL for a test tenant (or a local test issuer).
- Supporting skills:
  - `adk-frontend-integration`: authorised send, history, reconnect, upload, submit and status routes as one contract
- Execution scope: Local only: repository files, local Postgres/containers, scripted models and fake Guidewire. No cloud, IAM, Guidewire or paid model calls.

## Acceptance

- [ ] A valid token for customer A creates and continues A's session.
- [ ] Customer B using A's session, draft, upload or status ID receives 404 and no model call occurs (asserted on the scripted model).
- [ ] Forbidden: an expired, wrong-audience or unsigned token reaches no route except health.

Verification: Offline tests with a locally generated signing key and JWKS fixture.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G04-customer-identity-and-ownership.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

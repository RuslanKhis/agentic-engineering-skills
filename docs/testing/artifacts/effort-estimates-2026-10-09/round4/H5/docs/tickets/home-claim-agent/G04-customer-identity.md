---
goal: G04
title: A signed-in customer sees and changes only their own claim drafts and policies
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-tool-interface-design]
blocked_by: [G03]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 18-30
  review_and_verify: 10-16
  total: 28-46
  calendar_waits: none on this goal's path: CIAM staging client requested on day 1, needed before G24
  wait_days: 0
owner: Eng A
status: proposed
---

# G04 A signed-in customer sees and changes only their own claim drafts and policies

## Outcome

Implements D5 and I1: identity comes from a verified OIDC token, never from the model or the browser's choice of ID.

## Scope

- In: FastAPI auth dependency with JWKS verification replacing the G03 stub; owner checks on session, draft, photo, confirm and status routes; `list_my_policies` through a policy adapter (fake + staging).
- Out: CIAM production client; cross-customer adversarial cases beyond the route suite (G14).
- Depth: Build at production depth. Floor: no ID from model arguments; tokens never logged.

## Acceptance

- [ ] Customer B receives 404 on every route and resource belonging to customer A
- [ ] An expired, wrong-issuer or wrong-audience token is rejected
- [ ] A customer ID written into a chat message changes nothing (tools take no identity argument)
- [ ] `list_my_policies` returns exactly the adapter's policies for the verified customer

Verification: Offline and local integration with a test JWKS; staging CIAM check deferred to G24 prerequisites.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G04-customer-identity.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

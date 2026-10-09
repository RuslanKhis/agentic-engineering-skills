---
goal: G05
title: Customers see and change only their own claims data
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-tool-interface-design]
blocked_by: [G04]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 12-20
  review_and_verify: 12-20
  total: 24-40
  calendar_waits: CIAM client registration and the policy API credentials (1-2 weeks)
owner: E3
status: blocked
---

# G05 Customers see and change only their own claims data

## Outcome

Every route derives the customer from a verified portal token, and nobody can reach another customer's session, draft, photo or policy. Implements D4, I1.

## Scope

- In: OIDC verification middleware (issuer, audience, signature, expiry); subject as Runner `user_id` and owner key; owner checks on session, draft, photo, submit and operation routes; `list_my_policies` tool reading the existing policy API in code; 404 for foreign IDs.
- Out: Delegated access (brokers, joint holders) - later.
- Depth: Build. Floor: tools take no customer argument.
- Route: FastAPI dependency for token verification; trusted owner placed where tools read it (confirm the ToolContext accessor in G04's pin).
- Supporting skills: `adk-tool-interface-design` (`list_my_policies` declaration and bounded result)
- Execution scope: Local only; CIAM test client needed for a later integration check.

## Acceptance

- [ ] Valid token for customer A lists only A's policies
- [ ] Customer B using A's session, draft, photo or operation ID gets 404 and no model call is made
- [ ] Expired, wrong-audience or unsigned tokens get 401
- [ ] Model-supplied customer or policy IDs outside the list are rejected by code

Verification: Offline: pytest with locally signed test tokens and a fake policy API.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G05-customer-identity-and-scope.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

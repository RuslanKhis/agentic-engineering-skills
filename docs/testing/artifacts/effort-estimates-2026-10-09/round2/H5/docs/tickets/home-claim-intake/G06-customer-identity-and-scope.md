---
goal: G06
title: A signed-in customer sees only their own policies and drafts
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-agent-security]
blocked_by: [G03]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (x1.5 ADK multiplier included)
  hands_on: 22–38
  review_and_verify: 10–18
  total: 32–56
  calendar_waits: OIDC client registration with the portal IdP team, 1–2 weeks
owner: E4
status: blocked
---

# G06 A signed-in customer sees only their own policies and drafts

## Outcome

Every request carries a verified `customer_id`; tools and routes are scoped by it; policy ownership comes from the policy lookup. D9, I1.

## Scope

- In: FastAPI middleware verifying ID token (issuer, audience, signature via JWKS, expiry); trusted state injection before `Runner.run_async`; owner checks on session, draft and photo routes; `select_policy` index validation; policy lookup adapter against the G01 fake.
- Out: Photo routes themselves (G07); Guidewire write (G08).
- Depth: Production; security reviewer reads the middleware and repository scoping. Floor: no identity in model arguments.
- Route: Middleware → `customer_id` in request context → session created with owner; repository functions take `customer_id` as a required argument.
- Supporting skills: `adk-agent-security` (cross-customer denial cases and capability check on tools)
- Execution scope: IdP test tenant only.

## Acceptance

- [ ] Valid token: customer lists only their policies and resumes only their sessions
- [ ] Another customer's session, draft or photo ID returns 404 on every route; tool call with a foreign policy index returns `not_found`
- [ ] Expired, wrong-audience and unsigned tokens are rejected before any session read
- [ ] Captured model request contains no token or customer ID

Verification: Offline tests with a local JWKS; local integration with the IdP test tenant.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G06-customer-identity-and-scope.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

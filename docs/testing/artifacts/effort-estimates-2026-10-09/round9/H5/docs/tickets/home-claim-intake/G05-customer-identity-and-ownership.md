---
goal: G05
title: Signed-in customers only ever see their own sessions and policies
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-memory-architecture, adk-tool-interface-design]
blocked_by: [G01, G03]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 18-30
  review_and_verify: 8-14
  total: 26-44
  calendar_waits: none
owner: Lead
status: blocked
---

# G05 Signed-in customers only ever see their own sessions and policies

## Outcome

Implements I1 and D6: authority comes from the verified portal token, never from model arguments or caller-supplied IDs.

## Scope

- In: Middleware that verifies the CIAM OIDC token (issuer, audience, signature, expiry), derives `customer_id`, creates or loads the session with an ownership check, writes trusted state, `before_tool_callback` scope check, `get_my_home_policies` against the policy API (fake locally).
- Out: Photo ownership (G07). Erasure (G12).
- Depth: Production depth for authorization. Returns 404 for others' IDs.

Supporting skills and why:
- adk-memory-architecture (DatabaseSessionService ownership)
- adk-tool-interface-design (`get_my_home_policies` declaration)

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] Customer A can create and resume their own session and list their own home policies.
- [ ] Customer B, holding A's session ID, gets 404, and no model call or policy read happens (asserted on the fakes).
- [ ] An expired, wrong-audience or unsigned token is rejected before the Runner is invoked.
- [ ] A scripted model calling a tool with another customer's policy number gets an error result, and nothing is read.

Verification: Offline: pytest with two test identities and a local JWKS. Local integration: Postgres restart keeps session ownership.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G05-customer-identity-and-ownership.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

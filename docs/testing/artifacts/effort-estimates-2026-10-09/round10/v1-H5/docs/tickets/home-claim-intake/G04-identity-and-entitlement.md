---
goal: G04
title: A signed-in customer sees and files against only their own policies
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-agent-security]
blocked_by: [G02, W2]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 18-28
  review_and_verify: 8-12
  total: 26-40
  calendar_waits: none on this goal; waits on W2 before it
owner: Eng E
mentions_only: [G12]
status: blocked
---

# G04 A signed-in customer sees and files against only their own policies

## Outcome

Implements D4 and invariant I1: an ASGI middleware verifies the CIAM OIDC
token, derives `customer_id`, loads the customer's entitled home policies and
places both in session state before the Runner runs. Sessions are bound to
their owner.

## Scope

- In: token verification (issuer, audience, expiry, signature via JWKS with
  caching); session ownership check on every route; entitlement lookup
  behind an interface with a fake now and the Guidewire read wired in G10;
  `get_policy_summary` tool reading only trusted state; fail closed when the
  CIAM provider or entitlement read is unavailable; 2 h handoff from Eng A.
- Out: confirm-time recheck (G09); browser login UX (G12).
- Depth: production; careful review of the authorization path.

## Acceptance

- [ ] A valid token for customer A reaches the agent with A's policies in state.
- [ ] Customer B using A's session ID gets 403 and no model call is made.
- [ ] Expired, wrong-audience and unsigned tokens get 401.
- [ ] No tool accepts a customer or policy identifier from the model; a scripted model passing one has no effect.
- [ ] Entitlement read unavailable → fail closed with the form link.

Verification: offline tests with a local JWKS and fake entitlement service;
one authorised check against the CIAM test tenant after W2.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G04-identity-and-entitlement.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

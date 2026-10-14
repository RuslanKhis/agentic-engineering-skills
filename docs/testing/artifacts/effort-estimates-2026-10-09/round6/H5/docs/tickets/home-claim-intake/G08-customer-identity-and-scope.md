---
goal: G08
title: Let a signed-in customer act only on their own policies and drafts
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-agent-security]
blocked_by: [G06]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 11-18
  review_and_verify: 5-8
  total: 16-26
  calendar_waits: OIDC client registration in the customer identity provider
  wait_days: 3-5
owner: Dev C
status: blocked
---

# G08 Let a signed-in customer act only on their own policies and drafts

## Outcome

The gateway verifies the portal token, derives `customer_id`, lists active home policies and puts the chosen policy summary in trusted state. Implements D5, I1; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: Token verification middleware, policy API client, `before_tool_callback` scope check, trusted state keys.
- Out: Upload routes (G09), UI (G14).
- Depth: Production; authorisation boundary reviewed in G17.

## Acceptance

- [ ] Valid token returns the customer's own active policies; expired or tampered token gets 401.
- [ ] Customer A cannot read B's session, draft or photo: 404, nothing in body or logs.
- [ ] Customer or policy IDs supplied in tool arguments are ignored; an inactive policy cannot be selected.

Verification: Offline tests with a fake IdP and policy API.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G08-customer-identity-and-scope.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

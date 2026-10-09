---
goal: G05
title: "A signed-in customer sees and files against only their own policies and drafts"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-tool-interface-design]
blocked_by: [G01]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 12-18
  review_and_verify: 8-12
  total: 20-30
  calendar_waits: Test OIDC client in the portal identity provider
  wait_days: 2-5
owner: Security eng
status: blocked
---

# G05 A signed-in customer sees and files against only their own policies and drafts

## Outcome

Every API route and agent tool works from the verified customer, and another customer's IDs are refused. Implements D5, I1; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g05--a-signed-in-customer-sees-and-files-against-only-their-own-policies-and-drafts).

## Scope

- In: OIDC middleware; subject-to-account mapping; trusted session state with `customer_id` and policies; `get_my_policies` against a PolicyCenter fake then sandbox; owner checks on session, draft and photo routes.
- Out: Guidewire write (G10, G28); browser API and page (G12, G27).
- Depth: Build with careful review: authorization boundary.

## Acceptance

- [ ] Customer A lists only A's policies; supplying B's session, draft or photo ID returns 404.
- [ ] A scripted model passing B's policy number to a tool cannot read or attach it.
- [ ] Expired or wrongly signed token is rejected before the Runner runs.

Verification: Offline cross-customer tests; local integration with the test IdP client. Execution scope: Local plus portal test IdP; no production identities.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G05-customer-identity-and-scope.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

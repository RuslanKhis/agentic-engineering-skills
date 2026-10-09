---
goal: G03
title: Signed-in customers get their own sessions
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-memory-architecture, adk-frontend-integration]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-6
  review_and_verify: 2-3
  total: 6-9
  calendar_waits: none
  wait_days: 0
owner: Dev C
status: blocked
---

# G03 Signed-in customers get their own sessions

## Outcome

Only the verified customer can use a conversation, and it survives a restart. I1, D3, D7, D8. Route and rationale: [plan, G03](../../plans/salon-booking-assistant.md#g03--signed-in-customers-get-their-own-sessions).

## Scope

- In: `gateway.py` routes per the plan's JSON contract; token verification per G01; session owner check; `DatabaseSessionService` on local Postgres; 409 on overlapping turns
- Out: confirm logic (G04), hosting (G09)
- Depth: build; cross-customer denial tests

## Acceptance

- [ ] A process restart keeps the conversation
- [ ] Invalid token → 401; a second turn while one runs → 409
- [ ] Customer B using customer A's session ID → 403 and no model call

Verification: local integration with Postgres in a container and a real process restart.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G03-identity-and-sessions.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

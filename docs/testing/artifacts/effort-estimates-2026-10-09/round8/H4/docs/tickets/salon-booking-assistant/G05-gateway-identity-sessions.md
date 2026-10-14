---
goal: G05
title: Only the signed-in customer can use their conversation and their appointments
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-memory-architecture, adk-operational-guardrails]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 6-9
  review_and_verify: 3-5
  total: 9-14
  calendar_waits: none
owner: Dev A
status: blocked
---

# G05 Only the signed-in customer can use their conversation and their appointments

## Outcome

Implements D3, D5, D8 and D10 and guarantees I1 and I6 at the HTTP boundary.

## Scope

- In: `gateway/app.py`: `POST /turns` and `POST /operations/{id}/confirm`; token verification through the booking API; `user_id = customer_id`; `DatabaseSessionService`; per-session advisory lock (409 on overlap); 40 turns per customer per day; JSON contract `{messages, cards, turn_status}`; the token held in request memory only.
- Out: The browser panel (G06).
- Depth: Build. Review is careful: this is the authorization boundary.

## Acceptance

- [ ] A valid token reaches its own session; another customer's session ID returns 404 with no model call
- [ ] Turns survive a process restart; an overlapping turn returns 409
- [ ] The token is absent from stored events and logs (grep test); the 41st turn of the day is refused politely

Verification: local integration: real process restart, disposable Postgres, G01 fake.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G05-gateway-identity-sessions.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

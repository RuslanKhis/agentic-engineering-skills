---
goal: G04
title: Customer identity and per-customer scope
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: []
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 5-8
  review_and_verify: 3-4
  total: 8-12
  calendar_waits: none
owner: Dev C
status: ready
---

# G04 Customer identity and per-customer scope

## Outcome

Only a signed-in customer can see or change appointments, and only their own. Implements D4 and I1.

## Scope

- In:
  - Middleware verifies the website's session token (A6) and maps it to the booking API's `customer_id`.
  - It creates or loads the ADK session keyed by `customer_id` and `session_id`, and refuses another customer's session.
  - Anonymous visitors can browse services and free slots only.
- Out: Phone or OTP sign-in (O1 fallback) and staff identity.
- Depth: MVP Build. The verification key lives in Secret Manager in cloud environments and in an untracked env file locally. `customer_id` is never a model or tool argument.
- Implementation route: A FastAPI dependency in `app/auth.py`. The trusted `customer_id` goes into session state under an `app:`/`temp:`-safe key that model-facing code never writes. Confirm the state-prefix semantics on the pin. Tools read it from `ToolContext.state`.
- Prerequisites: The site's token format (A6). If A6 is false, stop and record O1. Phone OTP would add about 8–12 h and move G09 to the start of phase 2, which needs the user's decision.
- Supporting skills: None
- Execution scope: Local.

## Acceptance

- [ ] A valid token reaches the agent with the right `customer_id`.
- [ ] An expired or forged token returns 401.
- [ ] Customer A presenting B's `session_id` gets 404.
- [ ] "I am customer 123" in the chat does not change scope.
- [ ] An anonymous visitor can search slots but receives no appointment data and cannot create a proposal.

Verification: Offline `pytest tests/test_auth.py` with locally signed test tokens.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G04-customer-identity-and-per-customer-scope.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

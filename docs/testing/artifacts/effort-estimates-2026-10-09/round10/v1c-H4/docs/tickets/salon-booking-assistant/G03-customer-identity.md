---
goal: G03
title: Only the signed-in customer can use their conversation and appointments
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-agent-security]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 5-9
  review_and_verify: 2-4
  total: 7-13
  calendar_waits: none
owner: Dev C
status: proposed
---

# G03 Only the signed-in customer can use their conversation and appointments

## Outcome

The backend knows who the customer is from the website's login, never from
the model or the browser's claims, and refuses another customer's session or
appointment (D3, I1). Includes 1 h handoff from Dev A on G01's token findings.

## Scope

- In: middleware verifying signature, issuer, audience and expiry against a
  cached key set; `customer_id` written to ADK session state at session
  creation; session ownership check on every route; fallback path (email
  one-time code through the booking API) only if G01 found no verifiable
  token, with the extra hours recorded in Evidence.
- Out: guest access, staff accounts, the widget.
- Depth: build; careful review because it is the authorization boundary.

## Acceptance

- [ ] Valid token → session created with that `customer_id` in state.
- [ ] Expired, unsigned, wrong-audience and malformed tokens → 401, no model
      call.
- [ ] Customer B using customer A's session ID → 403; customer B proposing on
      A's appointment ID → refused by tool and executor; booking API fake
      records no read of A's data.

Verification: offline tests with locally generated test keys.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G03-customer-identity.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

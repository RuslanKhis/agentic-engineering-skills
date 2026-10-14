---
goal: G03
title: Signed-in customer is identified from the existing login
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-agent-security]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 5-8
  review_and_verify: 2-3
  total: 7-11
  calendar_waits: none
owner: Dev C
status: ready
---

# G03 Signed-in customer is identified from the existing login

## Outcome

The backend knows which booking-system customer is chatting, from the salon site's existing login, and nothing the browser or the model sends can change that. Settles A4; implements D3 and the enforcement half of I1.

## Scope

- In: Day 1: find out how the salon site's login issues tokens (issuer, signing keys, audience, subject = booking customer ID?) and record it in the design's A4 row. `app/auth.py`: a FastAPI dependency `verified_customer()` that checks signature, issuer, audience and expiry and returns `customer_id` or anonymous; session ownership helpers (`create_session_for(customer)`, `load_session(session_id, customer)` refusing a mismatch).
- Out: Wiring into the chat endpoint (G07); proposal ownership checks (G04–G06 use the same `customer_id`).
- Depth: Build. Floor: no signing secret in code; tokens never logged. If A4 fails (no verifiable token), stop and record the email one-time-code fallback as a decision for the team: +6–10 h, crosses the cut line.
- Notes: Send the W1 request on day 1 (GCP project with billing and Vertex AI, staging booking-API key, test customer and salon).
- Execution scope: Local; reading the login system's configuration is within the team's own systems.

## Acceptance

- [ ] Valid token → `customer_id` equal to the booking customer ID; anonymous request → anonymous with read-only rights.
- [ ] Expired, wrong-issuer, wrong-audience and tampered tokens are refused with 401 and no session is created.
- [ ] Loading customer A's session ID with customer B's token is refused, and no event from A's session is returned.

Verification: Offline: `pytest tests/test_auth.py` with locally generated test keys; no google.adk import needed except the session-ownership test.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G03-customer-identity.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

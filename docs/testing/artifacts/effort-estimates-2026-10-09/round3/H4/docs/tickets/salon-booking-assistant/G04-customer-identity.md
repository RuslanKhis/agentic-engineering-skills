---
goal: G04
title: Signed-in customers only see their own data
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-frontend-integration]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted, team new to ADK (x1.5 included)
  hands_on: 3.5-6
  review_and_verify: 2.5-4
  total: 6-10
  calendar_waits: none
owner: Dev C
status: ready
---

# G04 Signed-in customers only see their own data

## Outcome

The gateway accepts only a valid site token, binds each session to its customer and writes `customer_id`, `salon_tz` and `today` to state in code. Implements D2 and I1.

## Scope

- In: `app/gateway.py`: FastAPI app, JWT verification against the site's JWKS, `/chat` around the Runner, session create/resume with an owner check
- Out: allowance (G07), widget (G05), any new login method
- Depth: issuer, audience and expiry checked; a caller-supplied session ID never grants access; if the site token cannot be verified server-side, stop and raise the magic-link alternative

## Acceptance

- [ ] A valid token for customer A starts and resumes A's session
- [ ] Missing, expired or wrong-audience token returns 401; B resuming A's session ID returns 403 with no events
- [ ] State keys cannot be set from the request body; naming A's appointment ID while signed in as B reads nothing of A's

Verification: `pytest tests/test_gateway_auth.py` offline with locally signed test tokens and a scripted model.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G04-customer-identity.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

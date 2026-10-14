---
goal: G04
title: A signed-in customer only ever sees and changes their own appointments
design: ../../architecture/salon-booking.md
plan: ../../plans/salon-booking.md
primary_skill: adk-tool-auth-and-secrets
supporting_skills: [adk-frontend-integration]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-6
  review_and_verify: 2-4
  total: 6-10
  calendar_waits: none
owner: Dev C
status: blocked
---

# G04 A signed-in customer only ever sees and changes their own appointments

## Outcome

The gateway verifies the website's customer token, derives `customer_id` and
binds sessions to it, so I1 holds before any model call. Implements D3.
Includes 1 h handoff from Dev B (G01). If G01 shows the site's sign-in cannot
be verified, stop and re-estimate with the one-time-code fallback before
building.

## Scope

- In: `app/gateway.py` FastAPI dependency that verifies the token (signature,
  expiry, audience) with the key from configuration; writes `customer_id` into
  session state under a key the model cannot set; session lookup refuses a
  session owned by another customer; `list_my_appointments` and ownership
  checks read only that state.
- Out: the confirm endpoint's owner recheck (G05 uses this dependency), widget
  sign-in UX (G06).
- Depth: MVP Build. Floor: verification key from config, never logged.

## Acceptance

- [ ] Valid token → `/chat` runs with `customer_id` in state; expired or forged token → 401 with no model call
- [ ] Customer B using customer A's session ID → 404, no events returned, no model call
- [ ] Tool asked (by a scripted model) for an appointment ID belonging to another customer → "not found", and the fake API shows only a read scoped to the caller
- [ ] A user message containing `customer_id=...` does not change state (test)

Verification: offline `pytest tests/test_identity.py` with tokens signed by a test key.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking/G04-customer-identity-scope.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

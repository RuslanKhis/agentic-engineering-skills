---
goal: G01
title: The booking API can take a safe, once-only write from the assistant
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: []
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 5-8
  review_and_verify: 2-3
  total: 7-11
  calendar_waits: none
owner: Dev A
status: ready
---

# G01 The booking API can take a safe, once-only write from the assistant

## Outcome

The booking API (our existing service, its own repository) accepts an `Idempotency-Key` on create, reschedule and cancel, lets the assistant look an operation up by that key, and the assistant's service account can act only on a stated customer's appointments. Settles A6 and A7 for D3, D4 and D11. Dev A also sends the W1 sign-off request to the chain owner today.

## Scope

- In:
  - Inspect create/reschedule/cancel handlers, auth and staging data; write `docs/booking-api-contract.md` in this repo with endpoints, error codes (409 slot taken, 404, policy refusal), idempotency semantics (key scope, retention ≥ 24 h, changed-payload rejection), JWT issuer/audience/JWKS URL, cancellation policy source
  - If idempotency keys are missing: add them in the booking API (store key → request hash → response), with tests there
  - Service account credential for the assistant, scoped to read + the three writes
  - Staging tenant with the five salons, services, stylists and test customers
- Out: Assistant code (G02–G04); Reconciliation job (G14)
- Depth: Build: idempotency is the floor for I3. Kept: no production data in staging. Deferred: background reconciler (G14).

## Acceptance

- [ ] `docs/booking-api-contract.md` answers every row of the design's open-decisions table for A6 and A7, each with the file or endpoint that proves it
- [ ] Repeating a create with the same key and payload returns the original appointment; the same key with a different payload returns a 4xx; staging shows one appointment
- [ ] A write for customer X with the service credential and customer Y's appointment ID is refused
- [ ] W1 request sent to the chain owner (date recorded)

Verification: Booking API's own test suite (local); one bounded staging check of the replay case with a test customer.

Route and rationale: the design decisions named above and the plan's implementation map. Module paths are proposed.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-readiness.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

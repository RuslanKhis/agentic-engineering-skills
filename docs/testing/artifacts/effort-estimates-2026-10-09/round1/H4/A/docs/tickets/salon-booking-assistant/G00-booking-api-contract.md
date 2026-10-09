---
goal: G00
title: We know exactly what the booking API guarantees
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets (how a customer session is verified)]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate: 3-5 h
suggested_owner: Dev A (knows the booking API)
status: ready
---

# G00 We know exactly what the booking API guarantees

## Outcome

Answers assumptions A6 and A7 with evidence so D3 (exactly-once writes, move strategy) and D4 (customer identity) become final. Unblocks G02 and confirms G03.

## Scope

- In: Probe scripts against the **staging** booking API; new note docs/architecture/booking-api-contract.md covering availability, create, cancel, reschedule (exists?), list-by-customer, idempotency keys (supported? retention?), conflict and rule-violation error codes, timeouts and rate limits, session verification method, real bookings per salon per day; update A6/A7/D3 rows in the design.
- Out: Any application code (G01, G02). Production API calls.
- Depth: Discovery with a 5 h stopping point; unknowns left at the stop are recorded as risks with their effect on G02. Credentials stay in local env, never in the repo.

## Acceptance

- [ ] Each A7 question has a yes/no answer backed by a redacted request/response sample.
- [ ] Move strategy chosen (reschedule endpoint or create-then-cancel) and the reconciliation lookup for a lost create reply identified.
- [ ] No credential, token or real customer data appears in the note or committed files.

Verification: Review of the note by Dev A and Dev B (offline; staging probes only).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G00-booking-api-contract.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

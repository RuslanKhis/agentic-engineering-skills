---
goal: G01
title: We know exactly how the booking API books, moves, cancels and replays
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 2-4
  review_and_verify: 1-1
  total: 3-5
  calendar_waits: none
owner: Dev A
status: ready
---

# G01 We know exactly how the booking API books, moves, cancels and replays

## Outcome

Discovery. Settles D5 (is a move one atomic reschedule call?) and D6 (replay
contract) and open decision OD2, so the write path is built on facts.

## Scope

- In: write `docs/architecture/booking-api-contract.md` answering:
  Q1 idempotency key support, its scope and retention; Q2 reschedule
  atomicity; Q3 how an outcome is looked up after a timeout; Q4 error codes
  for slot taken, outside notice window, validation, auth, 429 (with or
  without `Retry-After`) and 5xx; Q5 service credential type, scope and
  rotation; Q6 whether staging sends SMS or email to anyone; Q7 rate limits and
  typical latency; Q8 which fields are free text written by people.
- Out: building the adapter; changing the booking API (if a key or an atomic
  reschedule is missing, record the cost of adding it as a proposal).
- Depth: discovery only; staging calls only, with a test customer.
- Stopping condition: every question answered with evidence, or marked
  unknown with its consequence for D5/D6, within 5 hours.

## Acceptance

- [ ] A1 The contract note answers Q1–Q8, each with evidence (a path in the
  booking API repository or a recorded staging call) or "unknown" plus the
  consequence.
- [ ] A2 On staging, one create, one reschedule and one cancel for a test
  customer are recorded, including a repeated create with the same key if keys
  exist; staging is confirmed to send no messages to real people.
- [ ] A3 D5 and D6 in the design are marked confirmed or revised, and any
  change to the write path is written into the dependent tickets before they
  start.

Verification: authorised live calls to the staging booking API only.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-write-contract.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

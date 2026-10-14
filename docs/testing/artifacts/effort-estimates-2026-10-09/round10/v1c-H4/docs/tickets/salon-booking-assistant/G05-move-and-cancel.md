---
goal: G05
title: Customers move or cancel their own appointment, with the 24-hour rule enforced
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: []
blocked_by: [G04]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-6
  review_and_verify: 2-3
  total: 6-9
  calendar_waits: none
owner: Dev A
status: proposed
---

# G05 Customers move or cancel their own appointment, with the 24-hour rule enforced

## Outcome

Maya's "move Thursday to Saturday 10:30" and "cancel my Thursday cut" go
through the same confirm path, once each, and changes inside 24 hours are
refused with the salon's phone number (D5, I5).

## Scope

- In: move and cancel in the executor; atomic reschedule, or book-new then
  cancel-old with both steps on the operation record and a `partial` state
  (design F3); 24-hour policy check in the salon's time zone, value from
  configuration (final value comes from W1, which G09 waits for).
- Out: fees, waitlists.
- Depth: build.

## Acceptance

- [ ] Move and cancel each produce one API change on confirm, including on
      double confirm.
- [ ] Two-step move where the cancel fails → operation `partial`, card says
      the new time is booked and the salon will fix the old one; the new
      appointment is never cancelled automatically.
- [ ] 23 h 59 m before start → refused, no API call; 24 h 01 m → allowed.
- [ ] Another customer's appointment ID → refused, no API call.

Verification: offline tests against the G01 fake and a local Postgres.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G05-move-and-cancel.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

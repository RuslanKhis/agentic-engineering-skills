---
goal: G01
title: The booking API contract is written down and a fake implements it
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-4
  review_and_verify: 1-2
  total: 4-6
  calendar_waits: none
owner: Dev A
status: ready
---

# G01 The booking API contract is written down and a fake implements it

## Outcome

Everyone builds against one agreed contract from day 1, and the open A6 questions are answered (D3, D4).

## Scope

- In: `docs/contracts/booking-api.md`: token verification, salons and services, availability (slot IDs, time zone), list my appointments, create, reschedule or cancel-plus-create, cancel, error codes and the cancellation-policy error, idempotency-key support. `tests/fakes/booking_api.py`: an in-memory fake with switches for conflict, timeout-after-commit and 5xx. Pin `google-adk` (2.8.0 unless the team chooses otherwise) and the model ID in a proposed `pyproject.toml`, and confirm the pin against the ADK interfaces named in the design.
- Out: Project skeleton and CI (G02); the operations table (G03).
- Depth: Discovery plus a fake only. Make no change to the real booking API in this goal; if it needs idempotency-key support, record that as a decision for the user.

## Acceptance

- [ ] The contract answers every A6 question in the design, each with its source (code path or API owner)
- [ ] The fake reproduces conflict, timeout-after-commit and a policy refusal on request
- [ ] The design's Open decisions table is updated, and any answer that changes D2 or D4 is flagged

Verification: offline: `pytest tests/fakes` (standard library and pytest only).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-booking-api-contract-and-fake.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

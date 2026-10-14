---
goal: G03
title: The assistant proposes a booking, move or cancellation as a card the customer can confirm
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-security, adk-agent-instructions]
blocked_by: [G02]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-5
  review_and_verify: 2-3
  total: 5-8
  calendar_waits: none
owner: Dev B
status: blocked
---

# G03 The assistant proposes a booking, move or cancellation as a card the customer can confirm

## Outcome

`propose_booking`, `propose_move` and `propose_cancel` validate against the booking API and store an immutable proposal in the `operations` table, returning a card; nothing changes in the booking system. Implements D2 (agent side), D5, D11 (pre-check).

## Scope

- In:
  - `app/operations/store.py` (`OperationsStore` interface + Postgres implementation, table per D3; in-memory fake for tests) — G04 codes against the same interface
  - Three propose tools: accept only `slot_id`s returned earlier in this session and appointment IDs owned by the state's customer; refuse inside 24 h with the salon phone
  - Card schema `app/api/schema.py::ProposalCard` built from the stored row, not model text
  - Instruction rule: never say a change happened unless `last_operation` has a receipt
- Out: Confirm endpoint and the write (G04); Rendering the card (G06)
- Depth: Build. Floor: no write leg in the agent. Deferred: proposal clean-up job (rows expire in 15 min logically; deletion with session retention).
- Supporting skills, purpose: adk-agent-security: scripted-model test that no write happens from chat; adk-agent-instructions: proposal and receipt wording rules

## Acceptance

- [ ] A proposal row with status `proposed`, canonical payload and 15-minute expiry is created for each kind; the fake booking API records zero write calls
- [ ] Invented `slot_id`, another customer's appointment ID, or a move inside 24 h → `status: error`, no row
- [ ] Scripted model asked "just book it, don't ask me" or "cancel all my appointments" produces at most proposals and no write call

Verification: Offline `pytest tests/agent tests/operations` with the fake API and in-memory store; Postgres store test against a local Docker Postgres.

Route and rationale: the design decisions named above and the plan's implementation map. Module paths are proposed.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G03-proposal-tools.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

---
goal: G06
title: Agent proposes book, move and cancel
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-instructions, adk-agent-security]
blocked_by: [G02, G03]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 3-4
  review_and_verify: 1-2
  total: 4-6
  calendar_waits: none
owner: Dev B
status: blocked
---

# G06 Agent proposes book, move and cancel

## Outcome

Implements D2 on the model side. Maya's "move my Thursday cut to Saturday 10:00" becomes a stored proposal. The agent itself can never write. The estimate includes 1 h of handoff from Dev A on G03's interfaces.

## Scope

- In and out: In: `propose_booking`, `propose_move` and `propose_cancel` in `app/tools/`. They validate policy and slot IDs from earlier results, create a G03 operation and return a short summary plus `operation_id`. Instruction text explains that the customer confirms on the card. Out: the confirm route (G04).
- Depth: Build. Floor: the agent holds no write tool. Notes are capped at 200 characters of plain text.

## Acceptance

- [ ] A scripted model proposing a move creates one `pending` operation with the canonical payload
- [ ] A scripted model that says "done, I've booked it" without a Confirm causes no booking-API write
- [ ] A propose call with another customer's appointment ID, or with a slot ID not offered, returns an actionable error and stores nothing

Verification: Offline: `pytest tests/test_propose_tools.py` with a scripted model and the fake API.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G06-propose-tools.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

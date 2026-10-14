---
goal: G04
title: The customer books, moves or cancels by chat, and nothing changes until she confirms the exact details
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design, adk-agent-instructions, adk-agent-security]
blocked_by: [G02, G03]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 5-8
  review_and_verify: 3-5
  total: 8-13
  calendar_waits: none
owner: Dev B
status: blocked
---

# G04 The customer books, moves or cancels by chat, and nothing changes until she confirms the exact details

## Outcome

Three write tools, `book_appointment`, `move_appointment` and
`cancel_appointment`, are added to the agent from G02. Each resolves concrete
slot and appointment IDs. Each asks for confirmation with a summary built by
code (salon, service, stylist, old and new time) and a payload hash. Ownership
and the slot are rechecked just before calling the G03 service (D3, I1, I2).
Includes 1 h of handoff from G02.

## Scope

- In: the tools, the mechanism chosen in G01, an instruction update to always
  resolve then propose, and a typed confirmation object in the event stream
  for the widget to render.
- Out: rendering the card in the browser (the chat API and widget goal).
- Depth: MVP build; the floor is that the model cannot confirm on the
  customer's behalf.

## Acceptance

- [ ] Scripted model: "move my Thursday cut to 10:00 Saturday", confirmed. The G03 service is called once with the exact IDs shown in the summary.
- [ ] Rejected confirmation, a missing one, or one whose payload hash differs gives zero calls to the G03 service.
- [ ] Forbidden: the model types "yes, confirmed" as text, a model-supplied foreign appointment ID, or a cancel of an appointment owned by another customer each give zero write calls and a denial result.
- [ ] Slot taken between the card and the confirmation gives `slot_taken` with fresh options.
- [ ] Local integration: the process restarts between the confirmation request and the reply, and the operation completes once (Postgres sessions).

Verification: `pytest tests/tools` offline with a scripted model. A
restart test against local Postgres.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G04-confirmed-write-tools.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

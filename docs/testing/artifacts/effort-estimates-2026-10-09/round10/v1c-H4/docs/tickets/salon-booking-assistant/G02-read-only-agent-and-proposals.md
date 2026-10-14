---
goal: G02
title: Agent answers availability and my-appointments questions and drafts proposals
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-instructions, adk-model-and-output-contracts]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-6
  review_and_verify: 1-2
  total: 5-8
  calendar_waits: none
owner: Dev B
status: proposed
---

# G02 Agent answers availability and my-appointments questions and drafts proposals

## Outcome

Maya can ask "what's free with Sam on Saturday morning?" or "when is my next
appointment?" and get correct answers from the booking API, and asking to
book, move or cancel produces a stored proposal, never a change (D1, D2, D4,
D9). Includes 1 h handoff from Dev A on G01's contracts.

## Scope

- In: `LlmAgent` factory with the six tools named in the design's
  model-facing contracts; prompt file with date, salon list and time zones
  injected from state; tool results allow-listed and bounded; read timeouts
  and one retry; `customer_id` read from session state only; proposals
  written through the G01 store interface (in-memory here).
- Out: HTTP API, identity verification, executing writes, durable storage.
- Depth: pinned `gemini-3.8-flash`; no `output_schema`.

## Acceptance

- [ ] Scripted-model test: each read tool returns allow-listed fields only; a
      stylist bio or customer note never appears in a tool result.
- [ ] Scripted-model test: calling every tool, including `propose_*`, causes
      zero write calls on the booking API fake.
- [ ] Tool declarations contain no customer identifier parameter; declaration
      dump and byte size recorded.
- [ ] Booking API timeout returns `{status: "unavailable"}` and the agent
      offers the salon's phone number.

Verification: offline Runner tests with a scripted model; not run in this
session (google-adk not installed).

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G02-read-only-agent-and-proposals.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

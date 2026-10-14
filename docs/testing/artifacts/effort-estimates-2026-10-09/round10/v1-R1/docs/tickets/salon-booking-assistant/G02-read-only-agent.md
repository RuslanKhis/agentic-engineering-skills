---
goal: G02
title: Customer asks about services, free slots and their appointments
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
status: blocked
---

# G02 Customer asks about services, free slots and their appointments

## Outcome

A signed-in customer chatting locally can ask what services a salon offers, find free slots with a stylist on a day, and list their own upcoming appointments. Implements D1 (read tools), D2, D12 and the `max_llm_calls` part of D9.

## Scope

- In: `app/agent.py` (one `LlmAgent`), `app/tools/read.py` with `list_salons_and_services`, `find_free_slots`, `list_my_appointments` (reads `customer_id` from `ToolContext.state`, never from arguments; projected results per D10, at most 10 slots per call; a `changeable` field left `null` until the cancel goal fills it), `app/context.py` (today, salon time zone and hours into state), `prompts/booking_agent/instruction.md` v1, `app/config.py` with the model pin and `RunConfig(max_llm_calls=8)`, `release.json` skeleton. Confirm `google-adk==2.8.0` against the chosen pin and refresh the model lifecycle snapshot. Handoff from Dev A (G01's client and fake) included: 0.5 h.
- Out: Proposal tools and the `changeable` rule (later goals), chat API, evaluation set.
- Depth: Build. Floor: pinned model and ADK; call cap. Output schema deliberately not used (design §4 model-facing contracts).
- Execution scope: Local; one live smoke needs a Vertex AI credential from W1 and is optional for this ticket.

## Acceptance

- [ ] Scripted-model Runner test: "what's free with Sam on Thursday afternoon" calls `find_free_slots` with the salon, stylist and an ISO date resolved from the injected today, and returns ≤ 10 slots.
- [ ] `list_my_appointments` with no `customer_id` in state returns `{status: "sign_in_required"}` (defence in depth; the chat API already refuses unauthenticated turns); with customer A it returns only A's appointments from the fake.
- [ ] A scripted model that loops on tools stops at 8 model calls with the designed refusal; the captured request shows exactly the read tool declarations and no phone or email fields in any tool result.

Verification: Offline: `pytest tests/test_agent_read.py` with a scripted model and the G01 fake. Needs google-adk installed; one bounded live smoke (≤ 10 calls) on the pinned model when credentials exist.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G02-read-only-agent.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

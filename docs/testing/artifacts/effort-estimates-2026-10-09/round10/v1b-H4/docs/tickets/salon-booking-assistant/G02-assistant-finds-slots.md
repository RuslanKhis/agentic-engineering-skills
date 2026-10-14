---
goal: G02
title: Assistant finds services and free slots
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-workflow-design
supporting_skills: [adk-tool-interface-design, adk-agent-instructions, adk-model-and-output-contracts]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-5
  review_and_verify: 1-2
  total: 4-7
  calendar_waits: none
owner: Dev B
status: blocked
---

# G02 Assistant finds services and free slots

## Outcome

A customer asking "cut at Northside Thursday after 5" gets up to three real
free slots from the booking API, in salon local time, without the assistant
inventing times. Implements D1, D7 and the read half of D8.

## Scope

- In: `app/agent.py` factory returning one `LlmAgent` with
  `list_salons_and_services` and `find_slots` (contracts in the design's
  model-facing table); instruction text in `app/prompts/booking_assistant.md`
  with today's date and salon list injected from code; `RunConfig(max_llm_calls=8)`
  wherever the Runner is built; pin `google-adk` (confirm 2.8.0 or record the
  chosen pin) and pin the Gemini model ID from the lifecycle table in
  `adk-model-and-output-contracts`, recording its retirement date in the design
  (O2). Look up and record the model's price with date. Includes 1 h handoff
  from Dev A on the client interface.
- Out: write tools (G04), the HTTP API (G05).
- Depth: MVP. Floor: pinned model, call cap, no secrets in prompt.

## Acceptance

- [ ] Scripted-model Runner test: `find_slots` is called with IDs from the
      catalogue, and the reply lists only slots the fake returned.
- [ ] With the fake returning `unavailable`, the reply gives the salon phone
      number and no invented slots.
- [ ] Captured model request shows 2 tool declarations, the injected date and
      no API key; declared bytes recorded.
- [ ] An invocation that would exceed 8 model calls stops with the designed
      apology.
- [ ] `adk web` demo on the fake works with the pinned model (bounded live,
      ≤ 20 calls).

Verification: `pytest tests/test_agent_read.py` offline; one bounded live
session recorded in Evidence.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G02-assistant-finds-slots.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

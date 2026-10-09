---
goal: G08
title: Spend and abuse limits, content-free telemetry
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-operational-guardrails
supporting_skills: [protect-adk-sensitive-data, adk-agent-observability]
blocked_by: [G06]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 1-2
  review_and_verify: 2-3
  total: 3-5
  calendar_waits: none
owner: Dev B
status: blocked
---

# G08 Spend and abuse limits, content-free telemetry

## Outcome

A runaway or abusive conversation stops politely with the salon phone number; logs and traces carry no message content. Invariant I5; floor.

## Scope

- In: `RunConfig(max_llm_calls=12)`; per-customer 60 messages/day counter in Postgres; per-IP rate limit; `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false`; structured logs of operation outcomes and token counts; written budget-alert steps for G10.
- Out: SLO alerts (G14), screening services (later).
- Depth: Build at MVP depth; billing budget is an alert, not a cap, and is documented as such.

## Acceptance

- [ ] A scripted looping model stops at 12 calls with the designed message
- [ ] The 61st message of the day is refused before any model call
- [ ] An in-memory exporter shows spans with the session ID and no message text

Verification: `pytest tests/test_limits.py tests/test_telemetry.py` (offline).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G08-limits-and-telemetry.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

---
goal: G07
title: Spend limits, allowance and PII-safe logging
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-operational-guardrails
supporting_skills: [protect-adk-sensitive-data]
blocked_by: [G04]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted, team new to ADK (x1.5 included)
  hands_on: 2-3.5
  review_and_verify: 1-1.5
  total: 3-5
  calendar_waits: none
owner: Dev A
status: blocked
---

# G07 Spend limits, allowance and PII-safe logging

## Outcome

A conversation cannot loop or run up cost, and logs hold no message content. Implements I5 and A10.

## Scope

- In: `RunConfig(max_llm_calls=12)` wiring; allowance table with atomic admission (60 turns per customer per day); structured logger with a field allow-list; 30-day session deletion query
- Out: Model Armor / SDP screening (later); billing budget alert (G08)
- Depth: floor plus the MVP per-customer allowance

## Acceptance

- [ ] A normal conversation passes admission and is logged with session ID and token counts
- [ ] A scripted model calling tools forever stops at 12 calls with the fallback message; the 61st turn of the day is refused
- [ ] A captured log of a full conversation contains no message text, phone or email

Verification: `pytest tests/test_guardrails.py` offline.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G07-guardrails-and-logging.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

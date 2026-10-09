---
goal: G06
title: Write and label 30 evaluation conversations
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: []
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-6
  review_and_verify: 1-2
  total: 5-8
  calendar_waits: pilot salon manager approves the expected outcomes
owner: Dev B
status: ready
---

# G06 Write and label 30 evaluation conversations

## Outcome

A labelled set that defines what "books the right slot" means for this chain. G10 uses it, and it becomes evidence for I5.

## Scope

- In:
  30 cases in `eval/cases/` with a fixed clock and fake-API fixtures:
  - 15 happy paths across the five salons: relative dates, time zones, stylist preference, move and cancel.
  - 8 ambiguous requests where the right answer is a clarifying question.
  - 7 forbidden or edge cases: another customer's booking; cancelling inside the policy window; "book without asking me"; an off-topic request; a price question with no data; a slot in the past; a salon that doesn't exist.
  Each case has the expected proposal fields, or "clarify" or "refuse".
- Out: The runner and the measurement (G10).
- Depth: MVP, an evaluation set. Prose quality is not judged in phase 1.
- Implementation route: Case files in the format G10's runner reads. Use ADK eval-set JSON if G02 confirms it fits the 2.8.0 pin, otherwise YAML read by a pytest runner.
- Prerequisites: None. Salon, service and stylist names come from the booking API's staging data or the G01 fake.
- Supporting skills: None
- Execution scope: Local.

## Acceptance

- [ ] 30 cases with the distribution above.
- [ ] Every expected outcome is approved by the pilot salon's manager, recorded with date and name or role.
- [ ] No real customer data appears in a case.

Verification: A schema check on the case files (`pytest tests/test_eval_cases.py`), offline.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G06-write-and-label-30-evaluation-conversations.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

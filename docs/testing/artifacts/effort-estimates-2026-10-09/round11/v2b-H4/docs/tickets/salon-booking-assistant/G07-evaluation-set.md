---
goal: G07
title: We know how often the assistant proposes the right change before customers use it
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-instructions, adk-agent-security]
blocked_by: [G03, W3]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 7-10
  review_and_verify: 2-3
  total: 9-13
  calendar_waits: none
owner: Dev B
status: blocked
---

# G07 We know how often the assistant proposes the right change before customers use it

## Outcome

A labelled set of realistic conversations, a runner against the pinned model
with the fake booking API, a measured result and prompt fixes. Includes 1 h
handoff from Dev A. Mostly human time: writing and judging cases.

## Scope

- In: `tests/eval/cases/`, runner, `tests/eval/RESULTS.md`, instruction edits.
- Out: CI gate (phase 2), adversarial suite beyond four cases (phase 2).
- Depth: MVP. Eval runs never call confirm; cost limit USD 5 per full run (assumed).

## Acceptance

- [ ] A1 At least 30 labelled cases: book 8, move 6, cancel 6, clarification 4, out of scope 2, adversarial 4 (another customer's appointment ID, "cancel everything", injected note text, request to reveal instructions); each with the expected proposal or the expected absence of one.
- [ ] A2 Live run, 3 repeats per case: correct proposal rate ≥ 85 % on book/move/cancel (assumed bar), zero proposals for another customer, zero proposals the customer did not ask for in adversarial cases.
- [ ] A3 Deterministic assertion: no case leads to a write on the fake.
- [ ] A4 Each run records model ID, prompt file hash, google-adk version, date, token totals and cost.
- [ ] A5 Every instruction change is followed by a full rerun; RESULTS.md lists before/after per change.

Verification: `python tests/eval/run.py --repeats 3` (live Vertex AI calls under the team's project; bounded by the cost limit).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G07-evaluation-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

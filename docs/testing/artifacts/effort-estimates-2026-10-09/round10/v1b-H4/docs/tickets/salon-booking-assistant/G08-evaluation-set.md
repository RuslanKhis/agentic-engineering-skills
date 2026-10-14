---
goal: G08
title: Evaluation set and runner
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-security]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 5-7
  review_and_verify: 1-2
  total: 6-9
  calendar_waits: none
owner: Dev A
status: ready
---

# G08 Evaluation set and runner

## Outcome

The team can measure, before launch and after every prompt or model change,
whether the assistant finds the right slots and proposes the right booking.
Implements the "core judgment, measured" depth row.

## Scope

- In: `evals/cases/*.yaml`, 25 labelled conversations written from the real
  service catalogue and the journey: 12 booking (vague times, stylist named,
  closed day, fully booked), 5 out-of-scope (prices, parking, complaints),
  4 move/cancel requests (expected: polite phone handoff in phase 1), 4
  adversarial (claims to be staff, asks for another customer's booking, text
  asking to skip confirmation, injection in a fake service description).
  Each case labels the expected tool calls, the expected proposal fields and
  forbidden effects. `evals/run.py` runs cases through any agent factory
  (stub now; G02's agent and G04's tools once merged) on the fake API, with
  repeats and a cost cap, writing `evals/results/<date>.jsonl` and
  `evals/README.md` (latest result per case).
- Out: CI gate (G14), judge-model metrics.
- Depth: MVP. Deterministic checks on tool calls and fake writes; no LLM judge.

## Acceptance

- [ ] Runner executes all 25 cases against the stub agent and reports
      pass/fail/missing per case with exit code ≠ 0 on any forbidden effect.
- [ ] Every adversarial case asserts 0 fake writes and 0 disclosure of
      another customer's data.
- [ ] Labels reviewed by one other developer (counted in review hours).

Verification: `python evals/run.py --agent stub` offline; the live run with
the pinned model happens in G09.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G08-evaluation-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

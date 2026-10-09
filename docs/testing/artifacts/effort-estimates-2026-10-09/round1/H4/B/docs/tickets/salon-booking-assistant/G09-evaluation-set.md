---
goal: G09
title: Thirty-conversation evaluation set
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-instructions, adk-agent-security]
blocked_by: [G02, G05 (write cases)]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 5-7
  review_and_verify: 3-5
  total: 8-12
  calendar_waits: none
owner: Dev B (Dev A and Dev C label 5 cases each)
status: blocked
---

# G09 Thirty-conversation evaluation set

## Outcome

A repeatable run shows how often the assistant chooses the right tools and proposal on realistic requests. D1; I1, I2.

## Scope

- In: `evals/`: 30 cases (8 book, 6 move, 5 cancel, 4 ambiguous dates or stylists, 3 out of scope, 4 adversarial), expected tool calls and proposal fields, forbidden assertions, a runner with at most 3 repeats and logged cost, `evals/REPORT.md`.
- Out: CI gate (G12), production-sample cases (G15).
- Depth: Build; run manually before each deploy in phase 1.

## Acceptance

- [ ] Cases validate against the pinned ADK's evaluation models; the report gives pass rate per category
- [ ] Every adversarial forbidden assertion passes (no proposal for another customer, no success claim without an operation)
- [ ] Proposal correctness at or above 25/30 (provisional target) before G10's public step, or the gap is reported

Verification: `python -m evals.run --repeats 3` (bounded live: at most 90 conversations on a named Vertex project).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G09-evaluation-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

---
goal: G09
title: Measured run and model freeze
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-model-and-output-contracts]
blocked_by: [G06, G08]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 2-3
  review_and_verify: 1
  total: 3-4
  calendar_waits: none
owner: Dev B
status: blocked
---

# G09 Measured run and model freeze

## Outcome

Measures the full agent (read and propose tools) on G08, compares `gemini-3.8-flash` with `gemini-3.5-flash`, and freezes D8 with tokens per completed change.

## Scope

- In and out: In: two runs per model, a results summary in `evals/RESULTS.md`, the chosen model ID pinned in config, and the cost per completed change written into the design. Out: the CI gate (G12).
- Depth: Build. The spend cap for the run is set in advance (A3).

## Acceptance

- [ ] A score per case for both models, with the chosen model and the reason recorded
- [ ] Zero forbidden effects (unconfirmed writes, other customers' data) on either model, or a ticket opened that blocks G11
- [ ] Tokens and calls per completed change recorded

Verification: Live model against the fake API, two models × 30 cases × 2 runs.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G09-measured-run.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

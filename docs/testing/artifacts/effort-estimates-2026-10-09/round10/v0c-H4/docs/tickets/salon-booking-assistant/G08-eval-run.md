---
goal: G08
title: We know how well the assistant handles real requests before customers see it
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-instructions, adk-model-and-output-contracts]
blocked_by: [G03, G07]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-4
  review_and_verify: 1-2
  total: 4-6
  calendar_waits: none
owner: Dev B
status: blocked
---

# G08 We know how well the assistant handles real requests before customers see it

## Outcome

`evals/run.py` runs G07's cases through the real agent and tools against the fake API, scores trajectory, proposal fields and forbidden effects, and writes `evals/REPORT.md`. Iterate the instruction until the agreed bar is met. Verifies I2, I5, D10.

## Scope

- In:
  - Runner and deterministic scorers (forbidden effects are hard failures)
  - One live run with `gemini-3.8-flash` (≈ 30 conversations, ≤ 300 model calls)
  - Instruction fixes, each re-run on all cases
- Out: CI wiring (G10)
- Depth: Build. Floor: pinned model; bounded live spend.
- Supporting skills, purpose: adk-agent-instructions: fix instruction issues the run reveals; adk-model-and-output-contracts: escalate settings only on measured failures

## Acceptance

- [ ] `evals/REPORT.md` lists every case with pass/fail, and failed and missing runs are counted, not dropped
- [ ] Zero forbidden effects across all cases (hard bar)
- [ ] Provisional bar, to confirm with the team: ≥ 90 % of cases with the right proposal or clarification

Verification: Offline scorer tests; one bounded live run against Vertex (record request count and cost).

Route and rationale: the design decisions named above and the plan's implementation map. Module paths are proposed.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G08-eval-run.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

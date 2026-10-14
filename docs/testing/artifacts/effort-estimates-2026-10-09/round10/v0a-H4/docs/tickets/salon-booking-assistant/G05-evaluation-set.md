---
goal: G05
title: The team can measure whether the assistant picks the right action on 30 realistic requests
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-instructions]
blocked_by: [G01, G05a]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted, 1.5x new-to-ADK applied; includes 1 h handoff from Dev A
  hands_on: 4-5
  review_and_verify: 1-2
  total: 5-7
  calendar_waits: none
owner: Dev C
status: blocked
---

# G05 Evaluation runner and first measured result

## Outcome

A runner over the fake booking API scores G05a's thirty cases for tool
choice, argument correctness and forbidden effects, giving the measured
"core judgment" the MVP needs (I5; security posture cases).

## Scope

- In: runner over `evals/cases/` (G05a); `evals/summary.md`; one
  instruction iteration from error analysis. Write cases run once G03 lands
  (in G07 if not before).
- Out: labelling (G05a), CI gate (G09), production samples (later).
- Depth: MVP Build with an evaluation set. Floor: bounded live model calls
  (≤ 30 cases × 3 repeats per run), pinned model.

## Acceptance

- [ ] Each case asserts expected tool and key arguments, and that no write reaches the fake API without confirm.
- [ ] Adversarial cases pass 3/3 repeats.
- [ ] `evals/summary.md` records pass rate per category, model ID and prompt version; launch threshold proposed (e.g. ≥ 90 % overall, 100 % adversarial).

Verification: local run against Vertex AI with the fake booking API, if
authorized; deterministic assertions offline with a scripted model.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G05-evaluation-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

---
goal: G07
title: We can measure whether the assistant captures claims correctly
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-model-and-output-contracts]
blocked_by: [W5, G02, G06]
phase: 1
profile: production
estimate:
  hands_on: 30-45
  review_and_verify: 6-9
  total: 36-54
  calendar_waits: none
owner: ML
status: proposed
---

# G07 We can measure whether the assistant captures claims correctly

## Outcome

A labelled evaluation set with photos and a runner that scores field
accuracy, turns to completion and forbidden statements, so T3 can be
measured. Starts once W5 grants anonymised FNOL samples; synthetic personas
can be written before. Handoff: 1 h from Eng A on the skeleton.

## Scope

- In: `evals/cases/` (dev and held-out), `evals/run.py` using ADK user
  simulation or scripted customer turns, `evals/summary.md`, licensed or
  synthetic damage photo sets, label guide.
- Out: iteration on failures (G23); CI gate (G19).
- Depth: production; the held-out set is run only at release points.

## Acceptance

- [ ] A1 At least 80 cases (60 dev, 20 held-out) across loss causes, both languages, photo sets, coverage questions, human-handoff requests and injection attempts, each with labelled required fields; the set is stored with a content hash.
- [ ] A2 The runner reports per case: field accuracy, turns to complete, forbidden-statement count; a case that did not run is reported missing, never passed.
- [ ] A3 The judge (pinned `gemini-3.8-flash`) agrees with human labels on at least 30 transcripts; agreement is reported and disagreements reviewed.
- [ ] A4 A baseline for G06's `intake-v1` and the cost of one full run are recorded; a run stops at a per-run spend cap.
- [ ] A5 No real customer data enters the set beyond the scope approved in W5; the anonymisation check is documented.

Verification: bounded live — `python evals/run.py --set dev` under the
non-prod cap; offline unit tests of the scorers.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G07-evaluation-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

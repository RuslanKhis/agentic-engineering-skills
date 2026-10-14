---
goal: G13
title: Measure whether the assistant collects the right facts
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-instructions]
blocked_by: [G05]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 50-76
  review_and_verify: 8-12
  total: 58-88
  calendar_waits: none
owner: ML Eng
status: blocked
---

# G13 Measure whether the assistant collects the right facts

## Outcome

A labelled set of synthetic German and English claim conversations and photos, with a runner and metrics for field accuracy, checklist completion, coverage-statement violations (I5) and emergency recall (I9). Also records the phone-channel baseline for the product outcome.

## Scope

- In: at least 80 cases per language reviewed by a claims handler, photo set without real customer data, runner with deterministic metrics and a pinned judge for tone.
- Out: CI gate wiring (G20).
- Depth: build.

## Acceptance

- [ ] The runner reports each metric per language and lists failed and missing cases
- [ ] Zero real customer data in the set (checked by the DPO checklist)
- [ ] Baseline callback rate and time-to-FNOL from the phone channel are recorded with their source

Verification: Offline plus a cost-capped live run.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G13-evaluation-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

---
goal: G14
title: Choose and pin the model with evidence
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: adk-model-and-output-contracts
supporting_skills: [adk-agent-evaluation]
blocked_by: [G06, G07, G08, G13]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 18-30
  review_and_verify: 4-8
  total: 22-38
  calendar_waits: none
owner: ML Eng
status: blocked
---

# G14 Choose and pin the model with evidence

## Outcome

Resolve O1 and confirm D7: EU availability and lifecycle of `gemini-3.8-flash` and one alternative, a side-by-side on the G13 set, thinking and temperature settings, and the pinned IDs in the manifest.

## Scope

- In: dated sources, comparison report, chosen settings, next retirement date in the team calendar.
- Out: failover (later).
- Depth: discovery then configuration; stop when a model meets the G13 thresholds in an EU region.

## Acceptance

- [ ] The report shows metrics and cost per completed claim for both candidates on the same set
- [ ] The manifest has no alias IDs
- [ ] If no candidate is available in the EU, the design's D2/D7 are flagged for decision instead of a silent change

Verification: Bounded live runs with a spend cap.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G14-model-choice.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

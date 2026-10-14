---
goal: G02
title: Confirm the model, screening services and ADK pin are available and compliant in the EU
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-model-and-output-contracts
supporting_skills: [protect-adk-sensitive-data, deploy-adk-on-google-cloud]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 5-9
  review_and_verify: 2-3
  total: 7-12
  calendar_waits: Vertex AI EU quota and model-access request
  wait_days: 3-5
owner: ML
status: ready
---

# G02 Confirm the model, screening services and ADK pin are available and compliant in the EU

## Outcome

The design's provisional model, region, screening and ADK version choices are confirmed or replaced with dated sources. Implements D6, D7, D8, I6; open decision 2; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: Refresh the model lifecycle snapshot; check `gemini-3.8-flash` on Vertex AI in an EU region, Model Armor and Sensitive Data Protection regional availability, data-residency and ML-processing terms, quota; current prices with date to fill the design's cost section; choose the ADK pin (≥ 2.10.0 recommended).
- Out: Provisioning (G03).
- Depth: Production; floor: no customer data in test calls.

## Acceptance

- [ ] Decision record cites each source with URL and access date.
- [ ] If `gemini-3.8-flash` is not served in the chosen EU region, an alternative stable model with no retirement before 2027-09 is named and D7 updated.
- [ ] Quota granted or request ID recorded; cost per claim range written into the design's budget section.

Verification: Documentation plus at most 10 synthetic test calls to the EU endpoint.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G02-eu-model-residency-and-adk-pin.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

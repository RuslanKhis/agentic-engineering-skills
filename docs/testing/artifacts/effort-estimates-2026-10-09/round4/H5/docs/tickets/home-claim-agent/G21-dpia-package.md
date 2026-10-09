---
goal: G21
title: The DPO has what they need to sign off the DPIA
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: protect-adk-sensitive-data
supporting_skills: []
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 12-20
  review_and_verify: 4-8
  total: 16-28
  calendar_waits: DPO review and sign-off of the DPIA
  wait_days: 20-30
owner: Security reviewer
status: ready
---

# G21 The DPO has what they need to sign off the DPIA

## Outcome

Starts the 20-30 day DPIA wait early; carries A10 to A13 and AI Act questions to the DPO and legal.

## Scope

- In: Data-flow, processors (Google, Guidewire), residency, retention, minimisation, photo blurring question; AI Act classification and disclosure questions to legal.
- Out: DPO's decision itself (calendar wait).
- Depth: Floor: no real data in the package.

## Acceptance

- [ ] The package is submitted and the date recorded
- [ ] Legal has the AI Act questions with a date
- [ ] The DPO's conditions, when they arrive, become goals or Later items
- [ ] The design's assumed answers A10-A13 are updated with the outcome

Verification: Document evidence only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G21-dpia-package.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

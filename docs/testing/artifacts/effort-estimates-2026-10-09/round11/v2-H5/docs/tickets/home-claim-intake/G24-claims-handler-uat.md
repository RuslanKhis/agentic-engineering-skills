---
goal: G24
title: Claims handlers confirm the assistant's claims are at least as complete as today's
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-frontend-integration]
blocked_by: [G09, G11, G16, G25, W15, W16]
phase: 1
profile: production
estimate:
  hands_on: 12-18
  review_and_verify: 4-6
  total: 16-24
  calendar_waits: none
owner: Eng D
status: proposed
---

# G24 Claims handlers confirm the assistant's claims are at least as complete as today's

## Outcome

User acceptance in staging against Guidewire non-prod (handlers booked in
W16; their review window is W17, after this goal), and the completeness
baseline for the benefit hypothesis in the design. Handoff: 1 h from Eng B.

## Scope

- In: test scripts for internal testers, a completeness rubric agreed with
  claims operations, a comparison sample of current web-form claims,
  feedback triage.
- Out: production measurement (G17 business metric after GA).
- Depth: production.

## Acceptance

- [ ] A1 At least five claims handlers review at least 40 staging claims filed by testers; the completeness score is compared with the same rubric on 40 current web-form claims and reported.
- [ ] A2 Every feedback item is triaged; items marked blocking are fixed or recorded in the plan with the reason they do not block.

Verification: authorised staging and Guidewire non-prod.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G24-claims-handler-uat.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

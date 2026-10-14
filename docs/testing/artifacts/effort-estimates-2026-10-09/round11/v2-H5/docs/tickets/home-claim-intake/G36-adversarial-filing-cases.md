---
goal: G36
title: Hostile input cannot change the policy or file a claim, shown on the real filing path
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: [safe-api-tool-calls]
blocked_by: [G04, G08, G14]
phase: 1
profile: production
estimate:
  hands_on: 3-4
  review_and_verify: 1-2
  total: 4-6
  calendar_waits: none
owner: Eng A
status: proposed
---

# G36 Hostile input cannot change the policy or file a claim, shown on the real filing path

## Outcome

The adversarial cases of G14 that need policy selection (G04) and the operation store (G08), split out after the independent review. Handoff: 1 h from Eng B.

## Scope

- In: adversarial cases in `tests/adversarial/filing/`.
- Out: the rest of the suite (G14).
- Depth: production.

## Acceptance

- [ ] A1 Instructions in messages and photos that try to change the selected policy or file the claim leave the policy unchanged and no submission operation; asserted on stored state.
- [ ] A2 A scripted model that calls tools with a confirmed (locked) draft's ID changes nothing and creates no operation.

Verification: offline scripted-model tests with the G01 fake.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G36-adversarial-filing-cases.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

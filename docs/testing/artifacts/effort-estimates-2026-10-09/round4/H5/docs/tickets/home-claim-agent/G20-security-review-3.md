---
goal: G20
title: Security review: adversarial suite and pen-test scope
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: adk-agent-security
supporting_skills: []
blocked_by: [G14, G18, G19]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 5-9
  review_and_verify: 1-3
  total: 6-12
  calendar_waits: none
  wait_days: 0
owner: Security reviewer
status: proposed
---

# G20 Security review: adversarial suite and pen-test scope

## Outcome

Third pass: reviews G14, closes or accepts earlier findings, sends the pen-test scope.

## Scope

- In: Review of G14; status of all findings; pen-test scope document.
- Out: Pen test itself (G28).
- Depth: Independent reviewer.

## Acceptance

- [ ] No open high finding before staff use (G24)
- [ ] Accepted risks are written with owner and end condition
- [ ] The pen-test scope has been sent
- [ ] The adversarial suite covers each forbidden action in the design

Verification: Document and test review.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G20-security-review-3.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

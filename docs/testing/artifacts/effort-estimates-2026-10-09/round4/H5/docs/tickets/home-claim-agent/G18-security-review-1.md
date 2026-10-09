---
goal: G18
title: Security review: design, identity and confirm binding
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: adk-agent-security
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G04, G09]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 6-10
  review_and_verify: 2-4
  total: 8-14
  calendar_waits: none
  wait_days: 0
owner: Security reviewer
status: proposed
---

# G18 Security review: design, identity and confirm binding

## Outcome

First of three review passes so the part-time reviewer follows the work as it lands; also books the pen test.

## Scope

- In: Review of the design, G04 and G09; findings list with severities; pen-test booking for G28.
- Out: Passes 2 and 3 (G19, G20).
- Depth: Independent reviewer (not the authors).

## Acceptance

- [ ] A findings list with severities exists for the design, G04 and G09
- [ ] High findings have an owner and target date
- [ ] Pen-test dates are confirmed in writing
- [ ] No secret or customer data is in the findings

Verification: Document review plus reading tests; no live access needed.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G18-security-review-1.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

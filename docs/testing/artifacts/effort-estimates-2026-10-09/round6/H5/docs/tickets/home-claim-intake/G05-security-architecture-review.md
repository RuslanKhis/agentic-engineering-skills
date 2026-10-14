---
goal: G05
title: Have the security reviewer accept or amend the agent's structure before code hardens
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: []
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 8-12
  review_and_verify: 2-3
  total: 10-15
  calendar_waits: none
  wait_days: 0
owner: Sec
status: ready
---

# G05 Have the security reviewer accept or amend the agent's structure before code hardens

## Outcome

The trifecta resolution, tool tiers, confirm binding and adversarial case list are reviewed and agreed. Implements D1, D3, D4, D5; design security posture; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: Review of the design; adversarial case list for G20; OWASP LLM mapping.
- Out: Implementation review (G17), pen test (G24).
- Depth: Production threat model depth.

## Acceptance

- [ ] Written review with each finding tied to a decision ID and OWASP LLM ID.
- [ ] Adversarial case list for G20 agreed.
- [ ] Any change recorded in the design as superseding the earlier decision.

Verification: Document review.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G05-security-architecture-review.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

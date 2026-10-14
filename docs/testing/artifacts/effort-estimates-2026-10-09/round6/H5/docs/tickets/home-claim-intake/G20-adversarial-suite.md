---
goal: G20
title: Prove the agent cannot be talked into forbidden actions
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-security
supporting_skills: [adk-agent-evaluation]
blocked_by: [G05, G11, G13]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 14-23
  review_and_verify: 6-9
  total: 20-32
  calendar_waits: none
  wait_days: 0
owner: Dev E
status: blocked
---

# G20 Prove the agent cannot be talked into forbidden actions

## Outcome

The adversarial cases agreed in G05 run in CI and assert the forbidden action never runs. Implements D1, D3, I1, I4, I7; route and rationale in the [plan](../../plans/home-claim-intake.md), entry for this goal ID.

## Scope

- In: Scripted-model attacks, injected photos, forged confirms, cross-customer attempts; OWASP mapping.
- Out: Pen test (G24).
- Depth: Production adversarial depth.

## Acceptance

- [ ] Scripted attempts to submit, read another customer's draft or state coverage never reach a forbidden call.
- [ ] An injected photo leaves tools and draft unchanged.
- [ ] Every case maps to an OWASP LLM ID and runs in CI.

Verification: Offline deterministic; bounded live subset.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G20-adversarial-suite.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

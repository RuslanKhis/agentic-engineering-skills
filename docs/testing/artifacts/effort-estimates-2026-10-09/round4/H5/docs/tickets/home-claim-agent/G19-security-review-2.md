---
goal: G19
title: Security review: submitter worker and sensitive-data boundaries
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: adk-agent-security
supporting_skills: [protect-adk-sensitive-data]
blocked_by: [G10, G13]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 4-8
  review_and_verify: 2-2
  total: 6-10
  calendar_waits: none
  wait_days: 0
owner: Security reviewer
status: proposed
---

# G19 Security review: submitter worker and sensitive-data boundaries

## Outcome

Second review pass on G10 and G13.

## Scope

- In: Review of the worker's identity, secret access, replay logic and SDP placement.
- Out: Pass 3 (G20).
- Depth: Independent reviewer.

## Acceptance

- [ ] A findings list for G10 and G13 exists
- [ ] `gateway-sa` is shown unable to read the Guidewire secret
- [ ] SDP fail-closed behaviour is confirmed in tests
- [ ] High findings have owners

Verification: Document and test review.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G19-security-review-2.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

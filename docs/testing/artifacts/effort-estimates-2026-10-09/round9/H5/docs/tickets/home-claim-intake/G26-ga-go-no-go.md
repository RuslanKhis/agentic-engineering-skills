---
goal: G26
title: Decide and execute GA in Germany
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-release-engineering
supporting_skills: [adk-agent-security]
blocked_by: [G22, G27, W3, W7]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 10-19
  review_and_verify: 4-7
  total: 14-26
  calendar_waits: none
owner: Lead
status: blocked
---

# G26 Decide and execute GA in Germany

## Outcome

Graduation conditions in the design are met, and the flag opens to all eligible customers.

## Scope

- In: Pen-test (W3) critical/high fixes, the G27 pilot evidence against thresholds, staged ramp (e.g. 10 % → 50 % → 100 %) with rollback criteria decided beforehand, final DPIA confirmation.
- Out: Phase 2 items.
- Depth: Production.

Supporting skills and why:
- adk-agent-security (pen-test remediation)

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] The go/no-go record lists each graduation condition with its evidence link.
- [ ] No open critical/high pen-test finding.
- [ ] Ramp thresholds and rollback criteria are written before traffic moves. Each step's comparable sample is recorded.

Verification: Authorised live: production, with named approvers.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G26-ga-go-no-go.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

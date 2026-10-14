---
goal: G21
title: Launch the pilot to a limited group of real customers
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-release-engineering
supporting_skills: [adk-agent-observability]
blocked_by: [G12, G14, G15, G16, G17, G18, G19, G20, G22, G23, G24, G25, W1, W6]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 10-18
  review_and_verify: 4-6
  total: 14-24
  calendar_waits: none
owner: Lead
status: blocked
---

# G21 Launch the pilot to a limited group of real customers

## Outcome

The first real customers file claims. W7 (the pilot run) starts.

## Scope

- In: Feature flag for about 2 % of eligible portal customers (assumption), production traffic split with the previous revision ready, go-live checklist confirming W1, W6, G14, G25 and the G17 gate pass, internal staff dry run first, comms to the claims team.
- Out: Quality review (G27). GA (G26).
- Depth: Production.

Supporting skills and why:
- adk-agent-observability (pilot dashboards)

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] The DPIA sign-off (W1) and the legal wording approval (W6) are recorded before the flag opens.
- [ ] An internal dry run files one real-format claim to production, which is then withdrawn by the claims team per the agreed procedure.
- [ ] A rollback to the previous revision was rehearsed in G22 and the command is in the runbook.

Verification: Authorised live: production, with named approvers.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G21-pilot-launch.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

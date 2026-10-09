---
goal: G20
title: Closed pilot with real customers, then GA go/no-go
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-release-engineering
supporting_skills: [adk-agent-evaluation, adk-agent-observability]
blocked_by: [G03, G11, G12, G13, G14, G17, G18, G19]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 60-106
  review_and_verify: 20-34
  total: 80-140
  calendar_waits: DPIA sign-off (G03), pen-test findings closed (G14), claims-ops sign-off; pilot runs at least 4 calendar weeks
owner: E2 (lead), whole team
status: blocked
---

# G20 Closed pilot with real customers, then GA go/no-go

## Outcome

About 200 invited customers file real claims; handlers review them; the team decides GA on measured quality, outcomes and SLOs. Implements Outcome measures, A10, A12, A16.

## Scope

- In: Pilot cohort and flag; handler feedback form; baseline vs phone/form for call-backs, time to FNOL, corrections; redacted pilot samples into the eval set; go/no-go criteria; GA canary.
- Out: Additional markets.
- Depth: Production done: SLOs, gates and recovery tested in production.
- Route: Feature flag in the portal; metrics from G17; samples via G18 process.
- Supporting skills: `adk-agent-evaluation` (pilot samples to eval cases); `adk-agent-observability` (pilot SLO and outcome dashboards)
- Execution scope: Production pilot requires the product owner's go and the DPIA sign-off.

## Acceptance

- [ ] Pilot claims all created once; reconciliation backlog zero at end
- [ ] Handler correction rate not above the form baseline (or decision recorded)
- [ ] SLOs met for 2 weeks or targets revised with the product owner
- [ ] Signed go/no-go record with open risks

Verification: Production pilot evidence, authorized by the product owner.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G20-pilot-and-ga-readiness.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

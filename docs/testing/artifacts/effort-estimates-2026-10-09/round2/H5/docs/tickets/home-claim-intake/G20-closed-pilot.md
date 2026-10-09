---
goal: G20
title: A pilot cohort of real customers files claims in production
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-release-engineering]
blocked_by: [G08, G11, G12, G13, G14, G15, G16]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (x1.5 ADK multiplier included)
  hands_on: 32–54
  review_and_verify: 16–26
  total: 48–80
  calendar_waits: DPIA sign-off (G05); pentest closure (G15); production Guidewire integration user and change approval (CAB) 1–2 weeks; pilot runs at least 3 calendar weeks
owner: E1
status: blocked
---

# G20 A pilot cohort of real customers files claims in production

## Outcome

Staff first, then a feature-flagged cohort of customers use the assistant in production; claims ops review every agent-filed claim daily; outcome metrics are compared with the baseline.

## Scope

- In: Production deploy; pilot flag; daily review procedure; feedback capture; outcome and guardrail measurement.
- Out: General availability (G21).
- Depth: Production. Floor: graduation conditions in the design met before the first customer.
- Route: Promotion through the G14 pipeline; production secrets and Guidewire user.
- Supporting skills: `adk-agent-observability` (pilot SLIs and daily review); `adk-release-engineering` (production promotion and rollback readiness)
- Execution scope: Production only after the CAB approval and DPIA sign-off; the user names the cohort.

## Acceptance

- [ ] Graduation checklist signed before the first customer session
- [ ] Pilot SLIs and outcome metrics reported weekly against baseline
- [ ] Every agent-filed pilot claim reviewed; misfile rate recorded

Verification: Production evidence under the approved change.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G20-closed-pilot.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

---
goal: G11
title: Staging rehearsal and launch at the five salons
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-evaluation]
blocked_by: [G05, G06, G07, G09, G10]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-5
  review_and_verify: 1-2
  total: 4-7
  calendar_waits: none
  wait_days: 0
owner: Dev C
status: blocked
---

# G11 Staging rehearsal and launch at the five salons

## Outcome

Real signed-in customers book, move and cancel at the five salons: the MVP's "done". Route and rationale: [plan, G11](../../plans/salon-booking-assistant.md#g11--staging-rehearsal-and-launch-at-the-five-salons).

## Scope

- In: Maya's journey and the G07 set against the staging booking API through the hosted widget; enable one salon, then the other four after a clean day
- Out: phase 2 (G12–G18)
- Depth: MVP; floor checked before go-live

## Acceptance

- [ ] Book, move and cancel succeed on staging with references; G07 pass rate not below baseline
- [ ] The first production change is confirmed in the booking system by a manager; rollback path known to all three developers
- [ ] No production change happens before the staging rehearsal passes

Verification: authorized live staging and production checks (needs the team's go-ahead).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G11-launch.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

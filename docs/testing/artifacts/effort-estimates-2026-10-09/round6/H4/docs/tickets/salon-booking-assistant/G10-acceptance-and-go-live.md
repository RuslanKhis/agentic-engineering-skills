---
goal: G10
title: Customers at the pilot salon, then all five, use the assistant
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-release-engineering
supporting_skills: [adk-agent-observability]
blocked_by: [G04, G06, G08, G09]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted; copied from the plan
  hands_on: 4-6
  review_and_verify: 2-3
  total: 6-9
  calendar_waits: chain owner go-live approval, requested on day 1 in G01
owner: Dev A
status: blocked
---

# G10 Customers at the pilot salon, then all five, use the assistant

## Outcome

Run the staging acceptance end to end, demo it to the chain owner, and go live with a per-salon flag as the kill switch.

## Scope

- In: Staging run of the G04–G06 acceptance cases with the real staging booking API
- In: Demo, then approval (calendar wait); enable the pilot salon; enable the other four on the last day if there are no `uncertain` or `partial` operations
- In: On-duty developer named for uncertain operations
- Out: Out: first-week review (G16)
- Depth: MVP depth with the floor kept (design §Delivery constraints); route in the plan's implementation map.

## Acceptance

- [ ] The acceptance script passes on staging, with evidence linked
- [ ] Turning the flag off hides the widget for that salon within 1 min
- [ ] No production enablement without the recorded approval and the user's go-ahead

Verification: authorised staging run; production only after approval.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G10-acceptance-and-go-live.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

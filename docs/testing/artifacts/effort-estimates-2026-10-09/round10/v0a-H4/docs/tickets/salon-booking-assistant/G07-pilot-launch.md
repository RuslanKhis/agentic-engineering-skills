---
goal: G07
title: Customers of the pilot salon use the assistant for real bookings
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-release-engineering
supporting_skills: [adk-agent-evaluation, adk-agent-security, deploy-adk-on-google-cloud]
blocked_by: [G03, G04, G05, G06, W1]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted, 1.5x new-to-ADK applied; includes 1 h handoff from Dev A and Dev B
  hands_on: 6-9
  review_and_verify: 2-3
  total: 8-12
  calendar_waits: none
owner: Dev C
status: blocked
---

# G07 Pilot launch at one salon

## Outcome

The assistant goes live for signed-in customers of the pilot salon (O5) after
an end-to-end staging run, the full evaluation set at its threshold, a
rollback rehearsal and the salon chain's sign-off (W1).

## Scope

- In: staging run of the journey (widget → gateway → agent → confirm → staging
  booking API) for book, move, cancel; full G05 set including write and
  adversarial cases; rollback to the previous revision rehearsed; privacy
  notice text live; pilot flag on; one-page runbook (uncertain proposals,
  rollback, kill switch = widget flag off).
- Out: other four salons (G08), CI gate (G09).
- Depth: MVP. Floor: launch only with W1 signed off and adversarial cases
  at 100 %.

## Acceptance

- [ ] End-to-end staging run: each kind completes with one booking API write and the booking system's notification.
- [ ] Evaluation set at or above the threshold recorded in G05; adversarial 100 %.
- [ ] Rollback rehearsal: traffic back on the previous revision in under 5 minutes.
- [ ] Widget flag off hides the assistant within one page load (kill switch).
- [ ] W1 sign-off recorded.

Verification: authorized staging and production checks; evaluation run with
recorded model and prompt versions.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G07-pilot-launch.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

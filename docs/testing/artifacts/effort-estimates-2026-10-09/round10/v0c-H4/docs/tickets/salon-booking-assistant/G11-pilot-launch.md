---
goal: G11
title: Customers of the pilot salon, then all five, book, move and cancel through the assistant
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-model-and-output-contracts]
blocked_by: [G03, G04, G06, G10, W1]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 5-7
  review_and_verify: 2-3
  total: 7-10
  calendar_waits: pilot-salon soak of 1-2 working days before enabling all five
owner: Dev A
status: blocked
---

# G11 Customers of the pilot salon, then all five, book, move and cancel through the assistant

## Outcome

End-to-end staging walkthrough with the salon manager, production deploy through G10's gate, the widget enabled for the pilot salon, then for all five after the soak with no wrong change. Delivers the MVP. All three developers attend the walkthrough (their time is inside this estimate). 1 h handoff on the release candidate.

## Scope

- In:
  - Staging end-to-end on real staging data: book, move, cancel, slot taken, inside 24 h, double click
  - Production project resources mirroring staging; production booking API credential; kill switch tested
  - Enable pilot salon; review every operation daily during the soak; enable remaining four
- Out: Outcome measurement (G15); SLO alerts (G13)
- Depth: Build. Floor: all five floor items verified in production config. Accepted risks: none.
- Supporting skills, purpose: adk-agent-observability: launch dashboard for operations by status and cost per conversation; adk-model-and-output-contracts: re-check gemini-3.8-flash lifecycle before launch

## Acceptance

- [ ] Salon manager completes the walkthrough on staging and signs off (W1 also received)
- [ ] In production, the first pilot bookings show one appointment per confirmed operation and zero `uncertain` left unresolved after the runbook
- [ ] Kill switch turns the widget off within one minute without a deploy
- [ ] Model lifecycle re-checked and recorded; no retirement inside the next 3 months

Verification: Authorised live: staging walkthrough, then production at the pilot salon; requires explicit go-ahead for the production deploy.

Route and rationale: the design decisions named above and the plan's implementation map. Module paths are proposed.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G11-pilot-launch.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

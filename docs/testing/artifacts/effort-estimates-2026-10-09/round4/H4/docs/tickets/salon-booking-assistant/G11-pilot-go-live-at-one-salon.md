---
goal: G11
title: Pilot go-live at one salon
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability]
blocked_by: [G03, G05, G08, G09, G10]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-5
  review_and_verify: 1-1
  total: 4-6
  calendar_waits: pilot salon agrees the go-live day and briefs staff
owner: Dev A
status: blocked
---

# G11 Pilot go-live at one salon

## Outcome

Real customers of one salon use the assistant, and the team reviews every failed or uncertain operation daily. This is the profile's "done".

## Scope

- In:
  - Set `ENABLED_SALONS` to the pilot salon.
  - Add the "Book with our assistant" link on that salon's page.
  - A 30-minute staff walkthrough covering what assistant bookings look like and whom to call.
  - Run G10's set against the production model configuration before switching on.
  - A daily review using `ops/daily_review.sql`: `uncertain` and `failed` operations, refusals, and cost per completed change.
- Out: Other salons (G12) and alerting (G16).
- Depth: MVP: real users complete the journey safely, and the team sees failures and cost.
- Implementation route: Configuration and queries only. No new modules.
- Prerequisites: G03, G05, G08, G09 and G10.
- Supporting skills: Adk-agent-observability, for the daily review from traces and the operations table.
- Execution scope: Requires the team's explicit go-ahead for production traffic.

## Acceptance

- [ ] The first real booking, move and cancellation are each seen in the booking system by staff.
- [ ] Zero duplicate appointments.
- [ ] Every `uncertain` operation is reconciled within one business day.
- [ ] Cost per completed change is recorded.
- [ ] The kill switch is tested once in production.

Verification: Production evidence, recorded in this goal.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G11-pilot-go-live-at-one-salon.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

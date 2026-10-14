---
goal: G11
title: Pilot go-live at one salon
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [deploy-adk-on-google-cloud, adk-agent-observability]
blocked_by: [G03, G04, G07, G08, G09, G10]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-4
  review_and_verify: 1-1.5
  total: 4-5.5
  calendar_waits: none
owner: Dev B
status: blocked
---

# G11 Pilot go-live at one salon

## Outcome

Signed-in customers of the pilot salon see availability and book through the assistant, and the team can see failures and cost from the first booking. Delivers the MVP's 'done' for phase 1 (8-day revision: booking only).

## Scope

- In: Final live evaluation run (G08) on the release candidate; run the unit tests and `eval/run.py --scripted` by hand if G22's CI is not yet in place; deploy the agent to staging and run a booking end to end with the W1 test customer; deploy to production enabled for the pilot salon only (salon allow-list in config); check the first production booking's trace for token count and operation status.
- Out: Cancel (G05) and move (G06); the first days' monitoring and baseline numbers (G12); other four salons (G12); slot cards (G13).
- Depth: Build. Floor: launch only if G08 meets its threshold with 0 forbidden calls; kill switch tested in G10.
- Notes: Pick up G04 and G07 from Dev A and G09 and G10 from Dev C; handoff 1 h included.
- Execution scope: Needs the team's go-live approval and W2.

## Acceptance

- [ ] The live evaluation on the release candidate meets the G08 threshold with 0 forbidden calls; the result is linked.
- [ ] Staging: the agent served by Cloud Run completes a booking for the test customer; production: one staff-assisted real booking at the pilot salon succeeds, appears in the salon's calendar, and its trace shows the token count and `succeeded` status without message text.
- [ ] A customer of another salon is told the assistant is not yet available there, and a request to move or cancel gets the salon's phone number; in both cases no proposal is created.

Verification: Authorised live and hosted: staging, then production for the pilot salon.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G11-pilot-go-live.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

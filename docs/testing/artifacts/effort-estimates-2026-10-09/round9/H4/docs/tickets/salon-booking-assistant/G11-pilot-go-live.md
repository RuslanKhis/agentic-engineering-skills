---
goal: G11
title: Pilot go-live at one salon
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [deploy-adk-on-google-cloud, adk-agent-observability]
blocked_by: [G05, G06, G07, G08, G09, G10]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-4
  review_and_verify: 1-2
  total: 4-6
  calendar_waits: none
owner: Dev B
status: blocked
---

# G11 Pilot go-live at one salon

## Outcome

Real customers of the pilot salon book, move and cancel their own appointments through the assistant, and the team can see completion, failures and cost. Delivers the MVP's 'done' for phase 1.

## Scope

- In: Final live evaluation run (G08) on the release candidate; deploy the agent to staging and run Maya's journey plus book and cancel end to end; deploy to production enabled for the pilot salon only (salon allow-list in config); first-day monitoring of traces, token cost per completed operation and any `uncertain` operation; record baseline numbers (completion, latency, cost) in `eval/README.md` and design §6.
- Out: Other four salons (G12), slot cards (G13).
- Depth: Build. Floor: launch only if G08 meets its threshold with 0 forbidden calls; kill switch tested in G10.
- Notes: Pick up G05, G06, G09 and G10 from other owners; handoff 1 h included.
- Execution scope: Needs the team's go-live approval and W2.

## Acceptance

- [ ] The live evaluation on the release candidate meets the G08 threshold with 0 forbidden calls; the result is linked.
- [ ] Staging: the agent served by Cloud Run completes Maya's move, a booking and a cancellation; production: one staff-assisted real booking at the pilot salon succeeds and appears in the salon's calendar.
- [ ] A customer of another salon is told the assistant is not yet available there, and no proposal is created.

Verification: Authorised live and hosted: staging, then production for the pilot salon.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G11-pilot-go-live.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

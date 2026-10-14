---
goal: G09
title: The pilot salon's customers can use the assistant
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-release-engineering
supporting_skills: [deploy-adk-on-google-cloud, adk-agent-evaluation]
blocked_by: [G04, G06, G07, G08, W1]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-5
  review_and_verify: 1-2
  total: 5-7
  calendar_waits: W1 sign-off before go-live
owner: Dev C
status: blocked
---

# G09 The pilot salon's customers can use the assistant

## Outcome

The integrated build runs on staging, then serves the pilot salon in production, with a rollback rehearsed and a staff runbook for `uncertain` operations.

## Scope

- In: Deploy G04 and G06 to staging; run G07 there and record the result; rehearse a rollback to the previous revision; write the staff runbook (find `uncertain` operations, check the appointment, tell the customer); go live for the pilot salon after W1; record a one-week baseline of completed versus abandoned proposals.
- Out: Other salons (G13).
- Depth: Minimal release engineering: manual evaluation run and revision rollback.

## Acceptance

- [ ] The G07 results on staging are recorded with the release manifest
- [ ] The rollback rehearsal restores the previous revision with operations intact
- [ ] No go-live before W1 is recorded

Verification: authorized live: production go-live needs the user's explicit approval.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G09-pilot-release.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

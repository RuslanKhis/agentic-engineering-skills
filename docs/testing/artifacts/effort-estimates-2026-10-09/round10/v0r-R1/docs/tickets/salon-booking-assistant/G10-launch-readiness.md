---
goal: G10
title: Launch readiness: runbook, drills and staff briefing
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [safe-api-tool-calls]
blocked_by: [G09, W2]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 2-3
  review_and_verify: 1-1
  total: 3-4
  calendar_waits: none
owner: Dev C
status: blocked
---

# G10 Launch readiness: runbook, drills and staff briefing

## Outcome

Whoever is on call can stop the assistant, roll it back and resolve an uncertain booking, and the pilot salon's staff know what customers will see. Supports the failure table in design §7.

## Scope

- In: `docs/runbook/salon-booking-assistant.md`: kill switch on and off, rollback, listing and reconciling `uncertain` operations by hand, the salon phone escalation, and the pre-deploy step that runs the unit tests and `eval/run.py --scripted` by hand until G22's CI exists. A drill in staging of the kill switch, rollback and a forced uncertain booking. A 30-minute staff briefing at the pilot salon, using the W2 wording: the assistant books; moves and cancellations still come by phone until G05 and G06. The forced uncertain booking is also the staging write check that G06 used to carry.
- Out: Automated reconciliation (G18).
- Depth: Minimal (MVP): manual runbook; automation is phase 2.
- Notes: Moved from Dev A to Dev C in the 8-day revision, so the platform's builder runs the drill; no handoff. The uncertain-booking drill uses G04's operations module (Dev A reviews the drill log).
- Execution scope: Needs G09's staging environment and W2.

## Acceptance

- [ ] The drill log shows the kill switch stopping model calls within 1 minute, a rollback, and a forced uncertain booking resolved to exactly one booking.
- [ ] The W2 sign-off (wording, the "call the salon to move or cancel" text, pilot salon) is recorded with its date.
- [ ] The runbook names the on-call person for each pilot day.

Verification: Authorised cloud: staging only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G10-launch-readiness.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

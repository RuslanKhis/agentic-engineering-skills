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
  hands_on: 3-4
  review_and_verify: 1-1
  total: 4-5
  calendar_waits: none
owner: Dev A
status: blocked
---

# G10 Launch readiness: runbook, drills and staff briefing

## Outcome

Whoever is on call can stop the assistant, roll it back and resolve an uncertain booking, spend alerts reach the team, and the pilot salon's staff know what customers will see. Supports the failure table in design §7 and the spend floor (D9).

## Scope

- In: `docs/runbook/salon-booking-assistant.md`: kill switch on and off, rollback, listing and reconciling `uncertain` operations by hand, a customer left with two appointments after a failed two-step move, the salon phone escalation. Billing budget alert at 50/90/100 % of A3 with the team as recipients (moved from G09; needs billing permission from W1). A drill in staging with the W1 test customer: a forced uncertain booking through the dispatcher resolved to exactly one booking, the kill switch and a rollback (at most 10 staging writes). A 30-minute staff briefing at the pilot salon, using the W2 wording and policy text.
- Out: Automated reconciliation (G18).
- Depth: Minimal (MVP): manual runbook; automation is phase 2.
- Notes: Pick up G09's platform from Dev C; handoff 0.5 h included. Of the old G06 staging check, the forced timeout lives here (the forced booking also proves create on staging); cancel and the two-step move on staging are in G11.
- Execution scope: Needs G09's staging environment, W1's staging key and test customer, and W2.

## Acceptance

- [ ] The drill log shows a forced uncertain booking resolved to exactly one booking (with its staging booking ID), the kill switch stopping model calls within 1 minute, and a rollback; the budget readback shows the three thresholds and recipients.
- [ ] The W2 sign-off (wording, policy text, pilot salon) is recorded with its date.
- [ ] The runbook names the on-call person for each pilot day.

Verification: Authorised cloud: staging only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G10-launch-readiness.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

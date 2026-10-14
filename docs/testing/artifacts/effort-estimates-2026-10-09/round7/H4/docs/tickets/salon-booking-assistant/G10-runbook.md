---
goal: G10
title: Runbook, kill switch drill, staff briefing
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability]
blocked_by: [G07]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 2-3
  review_and_verify: 1
  total: 3-4
  calendar_waits: none
owner: Dev C
status: blocked
---

# G10 Runbook, kill switch drill, staff briefing

## Outcome

The team and the pilot salon know what to do when an operation is `uncertain`, the model fails or cost spikes.

## Scope

- In and out: In: `docs/runbook.md` covering how to find an operation by ID, reconcile it against the booking API, flip `ASSISTANT_ENABLED`, roll back a revision, and who is on duty; a one-page briefing for salon staff. Out: alerts (G13).
- Depth: Minimal at MVP depth.

## Acceptance

- [ ] Kill switch drill on staging: flipped, then the phone-number message appears, then restored
- [ ] A staged `uncertain` operation is reconciled by following the runbook alone
- [ ] The runbook contains no secrets and no customer data

Verification: Authorised live on staging.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G10-runbook.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

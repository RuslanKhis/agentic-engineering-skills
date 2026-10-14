---
goal: G11
title: Customers of all five salons can use the assistant
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-release-engineering]
blocked_by: [G10, G12, W2]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 2-2
  review_and_verify: 0-1
  total: 2-3
  calendar_waits: none
owner: Dev A
status: ready
---

# G11 Customers of all five salons can use the assistant

## Outcome

After the salon chain's approval (W2), production serves the image verified on
staging, the widget is released on the production site and the salons are
enabled.

## Scope

- In: production deploy of the verified image, widget release on the existing
  site, enabling salon flags, a production smoke test.
- Out: first-week figures and alerting (phase 2, G14).
- Depth: Build; the per-salon flags are the rollback.

## Acceptance

- [ ] A1 A staff member's customer account books, moves and cancels a real
  appointment at one salon through the production widget; the salon's booking
  system shows each step; the test appointment ends cancelled.
- [ ] A2 The kill switch is tested off and on in production.
- [ ] A3 Release record in the plan: image digest, model ID, prompt version,
  tool schema hash and secret versions.

Verification: authorised production deployment; real appointment created and
cancelled by a staff account.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G11-go-live.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

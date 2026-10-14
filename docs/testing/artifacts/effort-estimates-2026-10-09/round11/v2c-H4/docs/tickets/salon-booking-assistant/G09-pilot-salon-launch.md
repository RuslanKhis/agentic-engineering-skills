---
goal: G09
title: Customers of the pilot salon book, move and cancel in production
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-release-engineering, adk-agent-observability]
blocked_by: [G08, W1, W2]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 1-1.5
  review_and_verify: 0.5-1
  total: 1.5-2.5
  calendar_waits: W1 and W2
owner: Dev C
status: blocked
---

# G09 Customers of the pilot salon book, move and cancel in production

## Outcome

The release verified in G08 serves production with only the pilot salon's
flag on, after the salon chain signed off the rules, privacy notice and pilot
salon (W1) and the customer-facing wording (W2).

## Scope

- In: production deploy of the G08 release, the production booking-API
  credential in Secret Manager, the pilot flag, a production readback.
- Out: other four salons and the first-real-booking review (G10).
- Depth: MVP; floor: kill switch tested in production before the flag goes on.

## Acceptance

- [ ] A1 W1 and W2 sign-offs recorded with date and name; rule values in configuration match W1.
- [ ] A2 Production serves the release whose manifest (G07/A3) matches the one verified in G08; the previous revision is kept for rollback.
- [ ] A3 With the global flag off, production returns 503 "assistant off"; then only the pilot salon's flag is turned on and `GET /config` shows the other four off.
- [ ] A4 A team member's own customer account opens the widget on the pilot salon's production page and gets a reply with slots; no booking is made in this check.

Verification: authorised production readback for the pilot salon only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G09-pilot-salon-launch.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

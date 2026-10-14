---
goal: G10
title: Customers of all five salons can book, move and cancel in production
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [safe-api-tool-calls, adk-agent-observability]
blocked_by: [W1, W2, G07, G09]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 5-7
  review_and_verify: 2-3
  total: 7-10
  calendar_waits: none beyond W1 and W2
owner: Dev B
status: blocked
---

# G10 Customers of all five salons can book, move and cancel in production

## Outcome

Real bookings on staging, a fault drill, the booking API changes released to
production, go-live for signed-in customers, and a front-desk runbook.
Includes 1 h handoff from Dev A.

## Scope

- In: staging walkthrough, fault drill with the adapter's staging toggle, production release of the booking API changes, runbook in `docs/runbooks/`, production enablement, baseline numbers.
- Out: the first-week review of operations (phase 2, G11), automatic reconciliation, SLO alerts.
- Depth: MVP. Production enablement only after the W1 sign-off is recorded.

## Acceptance

- [ ] A1 On staging through the chat page: one book, one move and one cancel; the staging booking API shows exactly the expected appointments; traces show tool spans.
- [ ] A2 Lost-response drill on staging with the fault toggle shows "checking", settles by lookup, and leaves no duplicate.
- [ ] A3 The chain's go-live sign-off (W1) and the published privacy notice line are recorded; the booking API changes are released to production; then production is enabled.
- [ ] A4 Front-desk runbook covers finding and resolving `unknown` and `partial` operations, and who flips the kill switch; one front-desk person has walked through it in the session booked in W2.
- [ ] A5 Baseline recorded: phone-made changes per week from the booking API before launch.

Verification: authorised live checks on staging, then production.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G10-staging-e2e-and-go-live.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

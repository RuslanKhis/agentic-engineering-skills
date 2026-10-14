---
goal: G08
title: Customers of the first salon can book, move and cancel by chat
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-evaluation, adk-agent-observability]
blocked_by: [G04, G05, G07, G09, W1]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 2.5-3.5
  review_and_verify: 1-1.5
  total: 3.5-5
  calendar_waits: W1 sign-off before go-live
owner: Dev A
status: blocked
---

# G08 Customers of the first salon can book, move and cancel by chat

## Outcome

The release that passed G07 on staging is promoted to production and the first
salon's flag is switched on. Wording, policies and the privacy notice were
approved through W1, and open decision O1 was accepted. Includes 1 h of
handoff from G04, G05 and G09.

## Scope

- In: a full G07 run on staging with the write tools and the widget, compared
  with the baseline. A production smoke test with a test customer (book, move,
  cancel). Switching on salon 1. Measuring complete-reply latency (p50, p95)
  and tokens per turn from traces for the first 2 days. Recording them in the
  plan.
- Out: switching on the other four salons (G10, after 3 clean days).
- Depth: MVP; the floor is W1 approval, rollback ready, and the kill switch
  tested in production.

## Acceptance

- [ ] G07 pass rate on staging is at or above the baseline, and every adversarial case passes.
- [ ] The production smoke test leaves three ledger rows in `succeeded` and the test customer's appointments match.
- [ ] With only salon 1 flagged on, a test customer of another salon gets the "not available yet" message.
- [ ] The kill switch in production returns the fallback message within a minute of being toggled.
- [ ] Forbidden: no salon other than salon 1 is enabled.

Verification: authorised production deploy with the readback and smoke
results recorded in Evidence.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G08-pilot-go-live.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

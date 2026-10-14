---
goal: G11
title: Pilot salon goes live
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-evaluation, adk-release-engineering]
blocked_by: [G05, G07, G09, G10, W1]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 4-5
  review_and_verify: 1-2
  total: 5-7
  calendar_waits: none
owner: Dev A
status: blocked
---

# G11 Pilot salon goes live

## Outcome

Implements D12. Signed-in customers of the pilot salon can book, move and cancel through the assistant.

## Scope

- In and out: In: deploy the integrated build (G03–G06) to staging; rehearse the full journey against the staging booking API; a go/no-go checklist (G09 results, W1 sign-off, privacy notice live, budget alert, runbook); enable the pilot salon flag in prod. Out: the other four salons (G17).
- Depth: Build. Floor checked one last time: no secrets in code or logs, Confirm before every write, pinned model, spend stop.

## Acceptance

- [ ] On staging, the book, move and cancel journeys each produce exactly one booking-API change, visible in the staging salon calendar
- [ ] A double click and a forced timeout on staging still give one change
- [ ] Customers of the other four salons see the phone-number message, and no prod write happens before the flag

Verification: Authorised live: staging rehearsal, then prod enablement with the team's go-ahead.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G11-pilot-go-live.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

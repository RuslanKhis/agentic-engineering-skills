---
goal: G10
title: Customers of the pilot salon book, move and cancel through the website chat
design: ../../architecture/salon-booking.md
plan: ../../plans/salon-booking.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-evaluation, safe-api-tool-calls]
blocked_by: [G05, G06, G07, G08, G09, W1]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-4
  review_and_verify: 1-2
  total: 4-6
  calendar_waits: none
owner: Dev C
status: blocked
---

# G10 Customers of the pilot salon book, move and cancel through the website chat

## Outcome

The finished service released to production with only the pilot salon enabled.
Implements D11. Depends on W1 (operations manager's sign-off). Includes 1 h
handoff from Dev A and Dev B.

## Scope

- In: final eval run (G07) and full adversarial run (G09) on the release
  candidate; end-to-end in staging against the booking sandbox: book, move,
  cancel, slot taken, timeout-after-commit; production release with manifest;
  widget embedded on the live site for the pilot salon only; staff runbook (how
  to see and resolve `uncertain` operations, how to flip the kill switch, who
  to call); go-live checklist with criteria for enabling the other four salons
  (proposed: 3 trading days, ≥ 20 confirmed operations, zero unresolved
  `uncertain` older than 1 day, no I1/I2 incident); measure p50 complete reply.
- Out: the four-salon rollout itself (G14), alerts (G12).
- Depth: MVP. Floor: previous revision kept ready; kill switch tested in production.
- Execution scope: production deploy and site embed need the operations manager's go-ahead (W1).

## Acceptance

- [ ] Eval and adversarial runs recorded for the release's manifest; no I2/I4 failures
- [ ] Staging end-to-end on the sandbox: each scenario's API state matches the card shown
- [ ] Kill switch flipped off and on in production, observed in the widget
- [ ] Runbook and checklist reviewed by the operations manager
- [ ] A test customer at a non-pilot salon sees the fallback message, not the assistant

Verification: authorised live in staging and production; record commands and results in Evidence.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking/G10-pilot-go-live.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

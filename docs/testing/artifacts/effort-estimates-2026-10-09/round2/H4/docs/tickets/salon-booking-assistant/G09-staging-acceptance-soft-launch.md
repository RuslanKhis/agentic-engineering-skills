---
goal: G09
title: Staging acceptance and soft launch
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-observability]
blocked_by: [G01, G02, G03, G04, G05, G06, G07, G08, salon operations sign-off]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted (1.5x new-to-ADK multiplier applied); copied from the plan
  hands_on: 3–5
  review_and_verify: 1.5–2.5
  total: 4.5–7.5
  calendar_waits: salon operations sign-off on wording and cancellation policy (1–3 days; request it on day 1)
owner: Dev B
status: blocked
---

# G09 Staging acceptance and soft launch

## Outcome

real customers at one salon, then all five, use the assistant; the team has a baseline. Design "Outcome to improve".

## Scope

- In: G06 live run against staging (≤200 model calls); end-to-end book/move/cancel by each developer on staging; record the salon's current phone volume for these requests as the baseline; enable the flag for one salon, watch logs for 2 days, then the other four; written runbook (disable flag, roll back, reconcile an `uncertain` proposal).
- Route: feature flag, Cloud Run prod.
- Prerequisites: G01–G08; salon sign-off.
- Depth: MVP; launch decision is the team's. Floor kept: no secrets in code or logs, model pinned, no booking change without the customer's Confirm, spend stop. Later controls: see the plan's phase 2 goals G10–G16.
- Supporting skills: `adk-agent-observability` (what to watch during the soft launch)

## Acceptance

- [ ] eval pass rate recorded and agreed by the team (assumed bar: ≥18/20 with both security cases passing)
- [ ] three staging journeys complete with correct receipts
- [ ] runbook tried once
- [ ] flag on for one salon

Verification: authorized live and hosted checks only. Execution scope: needs the team's go decision; changes real appointments only for consenting test customers until the flag is on.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G09-staging-acceptance-soft-launch.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

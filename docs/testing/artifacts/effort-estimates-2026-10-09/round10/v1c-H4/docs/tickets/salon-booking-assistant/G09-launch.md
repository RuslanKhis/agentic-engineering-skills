---
goal: G09
title: Customers of the five salons can use the assistant on the live website
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, safe-api-tool-calls]
blocked_by: [G04, G05, G06, G07, G08, W1]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 5-7
  review_and_verify: 2-3
  total: 7-10
  calendar_waits: W1 sign-off before production switch-on
owner: Dev A
status: proposed
---

# G09 Customers of the five salons can use the assistant on the live website

## Outcome

The pieces are joined on staging against the staging booking API, checked end
to end, then switched on for customers after the operations manager's
sign-off. Includes 2 h handoff from Dev B (environment) and Dev C (widget).

## Scope

- In: join the real confirm route into the widget; end-to-end journey on
  staging; fault drill (lost response, partial move) on staging; production
  configuration; one real test appointment per salon on the test stylist,
  created and cancelled with the operations manager's consent; widget enabled
  for one salon on day 1, all five on day 2 if no `uncertain` or `partial`
  operations; runbook: reconcile `uncertain`/`partial`, operator stop,
  rollback; baseline phone-change count if the chain supplies it.
- Out: SLO alerting and CI gate (phase 2).
- Depth: build; go/no-go uses the evaluation report.

## Acceptance

- [ ] Journey from the design (move Thursday to Saturday) passes on staging
      in a real browser.
- [ ] Fault drill: lost response reconciled to one appointment; partial move
      visible in the runbook query.
- [ ] Test appointments created and cancelled in each salon; no other real
      appointment touched.
- [ ] Operator stop tested in production: zero model calls while set.

Verification: authorised live checks on staging, then production with the
sign-off; not run in this session.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G09-launch.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

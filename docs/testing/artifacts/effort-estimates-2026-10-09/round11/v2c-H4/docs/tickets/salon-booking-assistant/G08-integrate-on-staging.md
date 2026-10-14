---
goal: G08
title: Book, move and cancel work end to end on deployed staging
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [deploy-adk-on-google-cloud, safe-api-tool-calls, adk-agent-security]
blocked_by: [G02, G03, G04, G05, G06, G07]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 6-8
  review_and_verify: 1.5-2.5
  total: 7.5-10.5
  calendar_waits: none
owner: Dev C
status: blocked
---

# G08 Book, move and cancel work end to end on deployed staging

## Outcome

The tracks meet: propose tools (G02), gateway (G03), executor (G04), widget
(G06) and pipeline (G07), checked with the evaluation set (G05). Includes 2 h
of handoff from Dev A and Dev B. Ends with a staging build ready for the
pilot launch in G09.

## Scope

- In: wiring `/proposals/{id}/confirm` and `/operations/{id}` to the executor;
  deploying through G07's pipeline; the first agent run against booking API
  staging; end-to-end and adversarial checks; eval rerun; trying the runbook.
- Out: production launch (G09), other four salons (G10), staff screen (later).
- Depth: MVP; floor checked end to end.

## Acceptance

- [ ] A1 On deployed staging, after `scripts/seed_staging.py`, a test customer books, moves and cancels through the widget; the booking system shows each effect once and its own notifications go to the test inbox only.
- [ ] A2 Adversarial pass on staging: another customer's session ID, "cancel all", confirm after expiry, double confirm, injected instructions in the customer's text, salon flag off; each gives the designed result, the booking API audit log shows no forbidden write, and the uncertain/partial alerts fire from the real executor.
- [ ] A3 G05's evaluation set rerun against deployed staging (after reseeding) meets G05's threshold; results stored.
- [ ] A4 The team tries each procedure in G07's runbook (G07/A7) once on staging: reconcile an injected uncertain operation, flip the kill switch, roll back a revision.

Verification: authorised live checks on booking API staging and the staging
Cloud Run service only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G08-integrate-on-staging.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

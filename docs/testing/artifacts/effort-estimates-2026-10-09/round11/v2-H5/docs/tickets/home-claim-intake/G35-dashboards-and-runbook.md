---
goal: G35
title: On-call has dashboards from real staging traffic and a rehearsed runbook
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-observability
supporting_skills: [adk-operational-guardrails]
blocked_by: [G09, G12, G17, G18]
phase: 1
profile: production
estimate:
  hands_on: 4-5
  review_and_verify: 1-2
  total: 5-7
  calendar_waits: none
owner: Eng C
status: proposed
---

# G35 On-call has dashboards from real staging traffic and a rehearsed runbook

## Outcome

The parts of D14 that need the whole filing path: dashboards on staging traffic and a runbook walked through once. Split from G17 after the independent review, because they need photo transfer (G09), screening (G12) and the kill switch (G18). Handoff: 2 h from Eng B and Eng A.

## Scope

- In: dashboards, runbook `docs/runbooks/claim-intake.md` (erasure section comes from G33).
- Out: the exporter and alerts (G17).
- Depth: production.

## Acceptance

- [ ] A1 Dashboards show confirmed→filed ratio, confirm→claim-number latency, photo attachment latency, turn latency, tool error rate by tool and tokens per filed claim from staging traffic.
- [ ] A2 The runbook covers uncertain-operation reconciliation, Guidewire outage, model or screening outage and the kill switch, and is walked through once by someone other than its author.

Verification: authorised staging.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G35-dashboards-and-runbook.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

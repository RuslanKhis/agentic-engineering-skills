---
goal: G11
title: Photos and transcript reach the claim, and uncertain work is reconciled
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-agent-observability]
blocked_by: [G10]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 22-38
  review_and_verify: 18-32
  total: 40-70
  calendar_waits: none beyond G01
owner: E1
status: blocked
---

# G11 Photos and transcript reach the claim, and uncertain work is reconciled

## Outcome

After a claim is created its photos and transcript are attached, pending or uncertain operations finish without duplicates, and operators see what is stuck. Implements D8, D10, failure table.

## Scope

- In: Per-document operations; transcript document of the customer-visible conversation; reconciler Cloud Run job (lookup-before-redispatch, pending dispatch when Guidewire recovers, attachment retries, after N failures a claim note); operator status query and runbook.
- Out: Dashboards (G17).
- Depth: Build.
- Route: Cloud Run job sharing the `ops/` module; scheduled by Cloud Scheduler (provisioned in G16).
- Supporting skills: `adk-agent-observability` (operation-age metric and correlation IDs)
- Execution scope: Local; sandbox with the G01 client.

## Acceptance

- [ ] Claim with 6 photos ends with 6 attached documents and a transcript
- [ ] Guidewire down at submit: operation pending, dispatched once after recovery
- [ ] Uncertain create found by lookup is marked confirmed without a second create
- [ ] Attachment failing N times leaves a claim note and an operator-visible record

Verification: Offline with fake Guidewire and an injected clock; bounded live sandbox run.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G11-attachments-and-reconciler.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

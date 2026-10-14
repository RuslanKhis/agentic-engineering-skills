---
goal: G11
title: The customer reviews exactly what will be filed, confirms it and follows its status
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: [G08, G10]
phase: 1
profile: production
estimate:
  hands_on: 16-24
  review_and_verify: 4-6
  total: 20-30
  calendar_waits: none
owner: Eng D
status: proposed
---

# G11 The customer reviews exactly what will be filed, confirms it and follows its status

## Outcome

Server-rendered summary, confirm bound to the draft version, and a status
page driven by the operation record. Implements D8 and D12, invariant I7.
Handoff: 1 h from Eng B on the confirm and status API.

## Scope

- In: summary screen (fields, policy, photo list) from
  `GET /v1/drafts/{id}/summary`; confirm button sending version and hash;
  status page and portal claim list entry.
- Out: email notifications (existing portal mechanism, unchanged).
- Depth: production.

## Acceptance

- [ ] A1 The summary is rendered from the server's draft version *n*, never from model text; Confirm sends `version` and `summary_hash`.
- [ ] A2 The status page shows only operation states (pending, filed with claim number, photos partly attached, needs attention), read from the status API.
- [ ] A3 Editing after the summary creates version *n+1* and requires a new confirmation; a stale confirm shows the updated summary.
- [ ] A4 The confirm button disables after one click; a second request (another tab) shows the same operation.
- [ ] A5 After confirm the draft is locked: further edits and photo uploads to it are refused with a pointer to adding documents to the filed claim.

Verification: local integration — Playwright against the local API with the
G01 fake behind the worker.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G11-portal-confirm-status.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

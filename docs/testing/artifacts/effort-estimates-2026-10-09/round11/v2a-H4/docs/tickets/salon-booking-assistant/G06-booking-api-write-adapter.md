---
goal: G06
title: Confirmed changes reach the real booking API on staging
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets, adk-operational-guardrails]
blocked_by: [G01, G02, G04]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 4.5-5.5
  review_and_verify: 1.5-2.5
  total: 6-8
  calendar_waits: none
owner: Dev A
status: ready
---

# G06 Confirmed changes reach the real booking API on staging

## Outcome

The write adapter implements book, move and cancel on the contract G01
recorded; the confirm and status routes are mounted on the chat API behind its
authentication (handoff from Dev C on the app); operators can stop dispatch
and resolve stuck operations. Implements D5, D6 and the operator side of D4.

## Scope

- In: write adapter, error mapping, idempotency key or lookup reconciliation
  per D6, credential loading, route mounting, kill switch on confirm, operator
  script, operation payload retention.
- Out: deployment.
- Depth: Build; staging only.

## Acceptance

- [ ] A1 On staging, book → move → cancel for a test customer each succeed
  through the confirm route and show correctly in the staging booking system.
- [ ] A2 The same `operation_id` dispatched twice on staging yields one
  appointment (by key, or by the lookup finding the first before any second
  create).
- [ ] A3 Slot taken, outside notice window, validation, 401, 429 and 5xx
  responses map to the operation statuses of the design (D4).
- [ ] A4 The service credential comes from Secret Manager or the environment
  at startup, never from code, prompts or logs; rotation is a new secret
  version plus restart, written in the README.
- [ ] A5 A malformed provider response (missing fields, HTML error page) on a
  write is treated as outcome unknown and reconciled; on a read it is an
  error; raw payloads never reach the model.
- [ ] A6 With the kill switch off, confirm refuses new dispatches while
  reconciliation of `uncertain` operations still runs.
- [ ] A7 `ops_cli list --status uncertain,dispatching` and
  `ops_cli resolve <id> --status succeeded|failed --note` work for operators;
  neither is reachable by the agent or the chat API.
- [ ] A8 Operation payload details older than 30 days are purged; ID, status
  and booking reference are kept.

Verification: offline tests on recorded responses; authorised live calls to
staging.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G06-booking-api-write-adapter.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

---
goal: G09
title: One confirmed draft creates exactly one claim
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G01, G05]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 30-46
  review_and_verify: 12-18
  total: 42-64
  calendar_waits: none
owner: Eng B
status: blocked
---

# G09 One confirmed draft creates exactly one claim

## Outcome

A Guidewire client and worker logic that create the FNOL with our operation ID as external reference, search before any re-send, attach photo documents as child operations and record receipts. Implements D5, I2, against a fake built from G01.

## Scope

- In: `app/guidewire/client.py`, `app/worker/submit.py`, operation states `pending/sent/uncertain/succeeded/rejected`, policy re-check (I1), fake server in tests.
- Out: confirm route (G11), sandbox (G10).
- Depth: build; no retry without reconciliation.

## Acceptance

- [ ] Happy path records claim number and document receipts
- [ ] Commit followed by a lost reply, a 5xx and a worker restart each end with exactly one claim on the fake
- [ ] A cancelled policy or address mismatch makes no create call and records `rejected`

Verification: Offline: fake Guidewire with fault injection.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G09-guidewire-adapter.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

---
goal: G10
title: A confirmed claim is filed exactly once, even when Guidewire times out or the customer double-clicks
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-operational-guardrails]
blocked_by: [G05, G06]
phase: 1
profile: production
estimate: 120-180 h
status: blocked
---

# G10 A confirmed claim is filed exactly once, even when Guidewire times out or the customer double-clicks

## Outcome

`POST /claims/{draft}/submit` binds confirmation to `{version, payload_hash}`, creates one durable operation, dispatches it, and a worker files the claim through `GuidewireClient` with per-photo sub-operations, fencing and reconciliation of uncertain outcomes — proven against a fake Guidewire. Implements D5, I2, I3, I4, I5 in the design.

## Scope

- In: `operations` and `document_ops` tables; `ClaimPayloadBuilder`; submit and status endpoints; worker handler with lease and fencing token; `FakeGuidewire` with failure injection (timeout after commit, document failure, 429, 5xx); ops reconciliation queue view (minimal).
- Out: Real Guidewire adapter (G11), Cloud Tasks provisioning (G16 — use an in-process queue adapter locally).
- Depth: Build: full replay and reconciliation; floor: no model involvement in submission.
- Route: `app/claims/operations.py`, `worker/handler.py`, `app/guidewire/fake.py`; queue adapter interface with Cloud Tasks implementation configured in G16.
- Prerequisites: G05, G06; G02 for the real replay contract (the fake models lookup-by-external-reference until then).
- Supporting skills:
  - `adk-operational-guardrails`: confirmation bound to draft version and payload hash; exemption of confirmed work from admission limits
- Execution scope: Local only: repository files, local Postgres/containers, scripted models and fake Guidewire. No cloud, IAM, Guidewire or paid model calls.

## Acceptance

- [ ] Happy path: one claim, all photos attached, status `SUBMITTED` with claim number.
- [ ] Fake commits then drops the response; worker retries: exactly one claim exists and status ends `SUBMITTED`; a document failure leaves the claim and shows that photo `FAILED`, then a retry attaches it once.
- [ ] Forbidden: a changed draft after confirmation returns 409 and no operation; double submit creates one operation; a stale worker's commit is rejected by the fencing check.

Verification: Offline deterministic tests with failure injection and two concurrent workers on local Postgres.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G10-confirmation-and-submission.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

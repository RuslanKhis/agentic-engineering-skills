---
goal: G06
title: Pressing Submit creates exactly one ClaimCenter claim with all photos, even when things fail
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets, adk-operational-guardrails]
blocked_by: [G01]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (team new to ADK, x1.5 included)
  hands_on: 28-42
  review_and_verify: 12-18
  total: 40-60
  calendar_waits: none
owner: Eng A
status: blocked
---

# G06 Pressing Submit creates exactly one ClaimCenter claim with all photos, even when things fail

## Outcome

Implements D5 and invariants I2 and I3.

## Scope

- In:
  - Confirm endpoint: freeze draft version, store hash, recheck policy, insert ledger row and enqueue task in one transaction
  - Worker with per-step records: create claim (external reference = `submission_id`), upload each document with its own key, submit
  - Reconciliation by external reference; `needs_reconciliation` state; status endpoint
  - Guidewire adapter with a fake built from G01 recordings; worker-only credential
- Out: Production client and ops queue UI (G14)
- Depth: Build at production write semantics against a fake; sandbox only in G12.

## Acceptance

- [ ] A duplicate Submit yields one ledger row and one claim
- [ ] A lost response after create is reconciled without a second create
- [ ] A failing photo upload is retried on its own key; the claim number is still shown
- [ ] Editing a draft after confirmation requires a new confirmation
- [ ] The chat-api service account cannot read the Guidewire secret

Verification: Offline failure matrix against the fake; local integration with Postgres and a worker restart.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G06-submission-ledger-and-guidewire-adapter.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

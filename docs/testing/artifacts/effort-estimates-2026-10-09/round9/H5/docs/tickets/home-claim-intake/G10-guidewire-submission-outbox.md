---
goal: G10
title: A confirmed draft becomes exactly one Guidewire claim, even through timeouts
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-operational-guardrails, adk-tool-auth-and-secrets]
blocked_by: [G02, G04, G06, W2]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 36-56
  review_and_verify: 12-20
  total: 48-76
  calendar_waits: W2
owner: Integration
status: blocked
---

# G10 A confirmed draft becomes exactly one Guidewire claim, even through timeouts

## Outcome

Implements D3, D4, I2 and I3, the most consequential effect in the system.

## Scope

- In: `/confirm` (hash-bound, idempotent on `draft_id`), `SubmissionOperation` table and states (PENDING, CREATED, UNCERTAIN, FAILED_VALIDATION), Cloud Tasks enqueue named by `op_id`, `submit-worker` with lookup-before-create, timeouts inside the task deadline, classified retries, reconciler, `/submissions/{op_id}` status. Applies the G02 contract.
- Out: Photo attachments (G23). Alerts (G16).
- Depth: Production depth: full replay and reconciliation. The submission path's own forbidden-effect tests live here.

Supporting skills and why:
- adk-operational-guardrails (confirmation bound to draft version)
- adk-tool-auth-and-secrets (Guidewire client credentials)

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] Confirm → exactly one claim in the fake and in the **Guidewire sandbox**, with claim number shown.
- [ ] Commit-then-timeout: state UNCERTAIN, then the reconciler finds the claim by `op_id`. No second create is attempted (asserted on the fake's call log).
- [ ] Double confirm, two tabs, and a worker restart mid-call still produce one claim.
- [ ] The draft edited after confirm is refused on hash mismatch, and the customer is asked to reconfirm.
- [ ] A scripted model asking to 'submit now' creates no operation row (no submit tool exists).

Verification: Offline with the G02 fake. Authorised live: Guidewire sandbox only (W2), with the tenant named when run.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G10-guidewire-submission-outbox.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

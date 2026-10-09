---
goal: G08
title: Confirming the summary creates exactly one ClaimCenter claim with photos
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets, adk-operational-guardrails]
blocked_by: [G01, G06, G07]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (x1.5 ADK multiplier included)
  hands_on: 44–76
  review_and_verify: 20–36
  total: 64–112
  calendar_waits: none beyond G01
owner: E1
status: blocked
---

# G08 Confirming the summary creates exactly one ClaimCenter claim with photos

## Outcome

`/submit` turns a confirmed draft version into one claim, submits it, uploads photo documents as sub-operations and shows the claim number; lost replies are reconciled. D2, D3, I2, I3, I9.

## Scope

- In: `submission_operation` + `photo_upload_operation` tables; Guidewire adapter (create, submit, add document, lookup by external reference); canonical payload + hash; re-check of ownership and policy status; reconciler job; AI-generated note on the claim; fake adapter with the G01 fixtures and a fault matrix.
- Out: Status follow-up journey (G23); production tenant (G20).
- Depth: Production: full replay and reconciliation. Floor: customer confirmation of the exact version; model has no path to this code.
- Route: HTTP endpoint (not an ADK tool) → transaction claims/loads operation → adapter → state machine pending → created → submitted → documents_done → confirmed, with uncertain at any network failure.
- Supporting skills: `adk-tool-auth-and-secrets` (Guidewire client credentials from Secret Manager, token caching and rotation); `adk-operational-guardrails` (confirmation bound to draft version hash and re-check before the effect)
- Execution scope: Guidewire sandbox only.

## Acceptance

- [ ] Happy path on the sandbox: one claim with 4 documents and the AI-generated note; UI receives claim number
- [ ] Fault matrix on the fake: timeout after commit, 5xx before commit, double submit, restart between steps, changed payload for same version — each yields at most one claim and the designed state
- [ ] Stale version hash returns 409 with no adapter call
- [ ] Reconciler resolves an `uncertain` operation by external-reference lookup without a new create

Verification: Offline fault-matrix tests; authorised live run on the Guidewire sandbox.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G08-guidewire-submission-operation.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

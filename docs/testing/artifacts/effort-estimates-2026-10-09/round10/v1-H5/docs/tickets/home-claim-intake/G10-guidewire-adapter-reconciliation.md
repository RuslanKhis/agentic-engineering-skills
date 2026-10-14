---
goal: G10
title: Confirmed claims really appear in Guidewire, and uncertain ones are resolved
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G01, G09]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 20-30
  review_and_verify: 6-10
  total: 26-40
  calendar_waits: none
owner: Eng B
status: blocked
---

# G10 Confirmed claims really appear in Guidewire, and uncertain ones are resolved

## Outcome

The real Guidewire adapter behind G09's interface, built to G01's contract,
plus the scheduled reconciler and the ops queue. Completes D3; wires the
entitlement read for G04's interface.

## Scope

- In: adapter for create, attach, submit, lookup and the policy read; error
  classification from G01; OAuth client-credentials token handling with
  refresh; reconciler (Cloud Run job) resolving `UNCERTAIN` and partial rows
  by lookup, never blind replay; ops queue table and a minimal view after
  1 h unresolved; the AI-summary note kept separate from the customer's
  statement (A17).
- Out: load (G20); handler-side Guidewire changes (O5).
- Depth: production.

## Acceptance

- [ ] On non-prod, a confirmed synthetic draft becomes a submitted claim with photos attached.
- [ ] A discarded create response is resolved by the reconciler to the existing claim with no duplicate.
- [ ] A row stopped after `CREATED` is completed from that step.
- [ ] An expired Guidewire token is refreshed without losing the ledger row; a revoked client pauses the executor and alerts.
- [ ] Recorded G01 fixtures replay offline in CI.

Verification: offline fixture tests; authorised bounded runs on the
Guidewire non-prod tenant with synthetic data.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G10-guidewire-adapter-reconciliation.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

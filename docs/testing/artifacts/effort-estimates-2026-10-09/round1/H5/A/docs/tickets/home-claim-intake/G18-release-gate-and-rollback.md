---
goal: G18
title: Every release is one versioned bundle that passes the evaluation gate and can be rolled back together
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-release-engineering
supporting_skills: [adk-agent-evaluation]
blocked_by: [G08, G16]
phase: 1
profile: production
estimate: 64-100 h
status: blocked
---

# G18 Every release is one versioned bundle that passes the evaluation gate and can be rolled back together

## Outcome

A release manifest (image digest, prompt version, model and judge IDs, tool schema hash, eval-set hash, secret versions), a CI gate that fails by exit code, a canary procedure with pre-agreed thresholds and a rehearsed joint rollback. Implements D10 in the design.

## Scope

- In: `release/manifest.json` generation; CI job parsing eval results (do not rely on the CLI exit code); canary at 5% for 24 h; rollback rehearsal in staging.
- Out: Model migration (P2-03).
- Depth: Build: canary and joint rollback; cut-line option 3: manual canary if phase 1 runs high.
- Route: CI runner; Cloud Run tagged revisions and traffic split.
- Prerequisites: G08, G16.
- Supporting skills:
  - `adk-agent-evaluation`: gate thresholds and repeat policy from G08
- Execution scope: CI locally or in the existing CI; staging rehearsal needs authorisation.

## Acceptance

- [ ] A prompt change that drops dev-set completeness below threshold fails CI.
- [ ] Rollback in staging restores the previous image, prompt, model ID and tool schema together, verified from the readback.
- [ ] Forbidden: a manifest containing a model alias or a missing eval run is rejected.

Verification: CI run; authorised staging canary and rollback rehearsal.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G18-release-gate-and-rollback.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

---
goal: G18
title: Every release is gated on evaluation and can roll back as one unit
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-release-engineering
supporting_skills: [adk-agent-evaluation]
blocked_by: [G09, G16]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 22-38
  review_and_verify: 18-32
  total: 40-70
  calendar_waits: none
owner: ML engineer with E2
status: blocked
---

# G18 Every release is gated on evaluation and can roll back as one unit

## Outcome

Prompt, model, tool schema and image ship and roll back together, and a quality drop stops promotion. Implements D6, release section, O6.

## Scope

- In: Release manifest; CI gate (deterministic every PR, judge eval nightly and pre-promotion, cost ceiling per run); canary 5/50/100 % with pre-set thresholds; joint rollback; model retirement calendar entry.
- Out: Production sample refresh loop (phase 2).
- Depth: Build: canary and joint rollback.
- Route: CI workflow + Cloud Run traffic splitting.
- Supporting skills: `adk-agent-evaluation` (gate metrics and thresholds)
- Execution scope: CI and staging.

## Acceptance

- [ ] A prompt change that raises forbidden-statement rate fails the gate by exit code
- [ ] Manifest has no model alias and records eval-set hash
- [ ] Canary rollback restores previous image and prompt together
- [ ] A missing eval run is reported as missing, not passed

Verification: CI run on a test branch; staging canary rehearsal.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G18-release-gate-and-canary.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

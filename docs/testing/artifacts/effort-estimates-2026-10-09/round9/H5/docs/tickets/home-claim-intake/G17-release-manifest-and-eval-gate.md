---
goal: G17
title: Every release records what it is and passes the evaluation gate
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-release-engineering
supporting_skills: [adk-agent-evaluation]
blocked_by: [G04, G09]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 18-30
  review_and_verify: 6-10
  total: 24-40
  calendar_waits: none
owner: Frontend
status: blocked
---

# G17 Every release records what it is and passes the evaluation gate

## Outcome

Implements D13.

## Scope

- In: `release/manifest.json` (image digest, prompt version, model and judge IDs, tool-schema hash, eval-set hash, secret versions), CI: deterministic tests plus G13 suite on every PR, G09 eval before promotion with thresholds and a cost cap. A missing run is reported as missing.
- Out: Canary execution (G21).
- Depth: Build.

Supporting skills and why:
- adk-agent-evaluation (gate thresholds)

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] The manifest has no model alias and no unknown fields (CI check).
- [ ] A threshold breach or a missing eval run fails the gate by exit code.
- [ ] A prompt change without an eval run cannot be promoted.

Verification: CI on a branch with a deliberately failing case.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G17-release-manifest-and-eval-gate.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

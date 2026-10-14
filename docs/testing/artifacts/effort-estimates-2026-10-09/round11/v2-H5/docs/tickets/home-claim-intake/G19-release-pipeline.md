---
goal: G19
title: Every release is gated, recorded as one unit and can be rolled back together
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-release-engineering
supporting_skills: [adk-agent-evaluation]
blocked_by: [G07, G14, G16, G17]
phase: 1
profile: production
estimate:
  hands_on: 18-26
  review_and_verify: 6-9
  total: 24-35
  calendar_waits: none
owner: ML
status: proposed
---

# G19 Every release is gated, recorded as one unit and can be rolled back together

## Outcome

Implements D15: CI gate, release manifest, canary and joint rollback.
Handoff: 2 h from Eng C on the environments.

## Scope

- In: CI workflow (unit, scripted-model and adversarial tests on every
  change; evaluation dev subset on release branches), `release/manifest.yaml`
  generation, traffic-split steps with thresholds, rollback script.
- Out: production launch (G22).
- Depth: production.

## Acceptance

- [ ] A1 The CI gate fails by exit code when a test fails, when the evaluation subset falls below its threshold, or when an evaluation run is missing.
- [ ] A2 The manifest records image digest, prompt version, model and judge IDs, tool-schema hash, eval-set hash and secret versions; a check rejects aliases and unknown fields.
- [ ] A3 A staged release 5 % → 50 % → 100 % uses thresholds written before traffic moves; a rehearsed rollback restores the previous revision, prompt and configuration together within 10 minutes.
- [ ] A4 A session-schema change is rehearsed with old and new revisions serving the same database; sessions continue across both.

Verification: CI run on a branch; authorised staging rehearsal.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G19-release-pipeline.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

---
goal: G14
title: Every release is one recorded bundle that passes gates and rolls back together
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-release-engineering
supporting_skills: [adk-agent-evaluation]
blocked_by: [G04, G10]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (x1.5 ADK multiplier included)
  hands_on: 32–54
  review_and_verify: 16–26
  total: 48–80
  calendar_waits: none
owner: E5
status: blocked
---

# G14 Every release is one recorded bundle that passes gates and rolls back together

## Outcome

A release manifest, a deterministic CI gate on every PR, the eval gate before promotion with the pinned judge, manual staged traffic on Cloud Run, joint rollback and a model-lifecycle calendar. D12.

## Scope

- In: Manifest generation in CI; gate scripts failing by exit code; promotion pipeline dev → staging → prod with manual traffic steps; rollback command; calendar entries for model retirement checks.
- Out: Automated canary analysis (G22).
- Depth: Production with manual staged rollout. Floor: no alias model IDs (manifest check).
- Route: CI on the org's system; Cloud Run revisions and traffic tags.
- Supporting skills: `adk-agent-evaluation` (eval gate thresholds, repeats and cost policy)
- Execution scope: CI, dev and staging.

## Acceptance

- [ ] Manifest lists image digest, prompt version, model IDs, schema hashes, eval-set hash and secret versions; an alias model ID fails the check
- [ ] A missing eval run is reported as missing, not passed
- [ ] Rollback in staging restores the previous bundle (image, prompt, model config) in one step

Verification: CI runs; staging rollback rehearsal.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G14-release-manifest-and-gates.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

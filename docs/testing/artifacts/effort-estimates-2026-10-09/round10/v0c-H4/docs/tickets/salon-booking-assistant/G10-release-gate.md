---
goal: G10
title: Every release is gated by tests and the evaluation, and can be rolled back as one unit
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-release-engineering
supporting_skills: [adk-agent-evaluation]
blocked_by: [G08, G09]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-6
  review_and_verify: 1-2
  total: 5-8
  calendar_waits: none
owner: Dev B
status: blocked
---

# G10 Every release is gated by tests and the evaluation, and can be rolled back as one unit

## Outcome

CI runs offline tests on every PR and the evaluation on release candidates, fails by exit code, writes `release-manifest.json` (image digest, prompt version, model ID, tool schema hash, eval-set hash, secret versions) and deploys to staging; rollback is "route traffic to the previous revision with its manifest". Implements D12. 1 h handoff from Dev C on the deploy script.

## Scope

- In:
  - CI workflow, manifest writer, eval-gate script with a cost ceiling per run
  - Rollback procedure in `docs/runbook.md`
- Out: Canary (later); Production-derived cases (G12)
- Depth: Build: evaluation in CI at MVP depth. Deferred: canary and judge-based metrics.
- Supporting skills, purpose: adk-agent-evaluation: CI run policy and cost limit

## Acceptance

- [ ] A PR that breaks a tool test fails CI
- [ ] A release candidate with a seeded instruction regression fails the eval gate by exit code; a run that did not happen is reported as missing, not passed
- [ ] Rollback in staging to the previous revision is rehearsed once and its manifest matches

Verification: CI run on the repository; authorised staging rollback rehearsal.

Route and rationale: the design decisions named above and the plan's implementation map. Module paths are proposed.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G10-release-gate.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

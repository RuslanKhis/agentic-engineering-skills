---
goal: G17
title: Every change is gated by tests and evaluation, and releases roll out and back as one unit
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-release-engineering
supporting_skills: [adk-agent-evaluation]
blocked_by: [G03, G06, G07, G08]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 24-36
  review_and_verify: 6-10
  total: 30-46
  calendar_waits: none
owner: Eng D
status: blocked
---

# G17 Every change is gated by tests and evaluation, and releases roll out and back as one unit

## Outcome

Implements D13: a release manifest, a CI gate failing by exit code, a staged
Cloud Run rollout with thresholds, and a joint rollback; plus the model
retirement calendar.

## Scope

- In: manifest recording image digest, prompt versions, model and judge IDs,
  tool-schema hash, eval-set hash, secret versions; gate with deterministic
  tests and photo-set scores on every change, judge metrics nightly with the
  judge pinned; canary 5% → 25% → 100% with thresholds decided beforehand;
  previous revision kept 7 days; calendar entry for the model's next
  lifecycle check; 2 h handoff from Eng A and ML.
- Out: conversation cases (added by the conversation-set goal).
- Depth: production.

## Acceptance

- [ ] A prompt change without a manifest update fails CI.
- [ ] A missing eval run is reported as missing evidence and blocks promotion.
- [ ] A staging canary with a deliberately failing candidate is rolled back automatically, and image, prompt and model return together.
- [ ] The manifest contains no model alias.

Verification: CI runs in the dev project; authorised staging rollout drill.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G17-release-ci-gate.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

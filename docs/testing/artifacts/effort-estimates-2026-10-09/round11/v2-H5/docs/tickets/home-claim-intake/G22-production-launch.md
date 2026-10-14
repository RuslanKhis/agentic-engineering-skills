---
goal: G22
title: Customers in Germany can file home claims with the assistant
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-release-engineering, adk-agent-observability]
blocked_by: [G19, W6, W7, W14]
phase: 1
profile: production
estimate:
  hands_on: 18-26
  review_and_verify: 6-9
  total: 24-35
  calendar_waits: none
owner: Eng C
status: proposed
---

# G22 Customers in Germany can file home claims with the assistant

## Outcome

Production deploy from a manifest and a staged rollout to all German portal
customers by 2027-03-15, after go-live approval (W6) and with production
Guidewire credentials (W7). Handoff: 2 h from the ML engineer on the
release pipeline.

## Scope

- In: production apply, deploy from the manifest, smoke test, staged
  rollout by portal feature flag, hypercare rota.
- Out: second market (phase 2 G27).
- Depth: production; the smoke-test claim follows the procedure claims
  operations approved in W6.

## Acceptance

- [ ] A1 Production runs the manifest's exact revision; a readback confirms region, model ID, prompt version and secret versions.
- [ ] A2 One smoke-test claim on a designated test policy is filed and then closed by claims operations under their approved procedure; status and photos are correct.
- [ ] A3 Rollout goes staff → 5 % → 50 % → 100 % of portal customers using the thresholds from G19; each step's numbers are recorded (the soak time per step is wait W11, after this goal).
- [ ] A4 The hypercare rota and runbook are handed to on-call; the kill switch is tested in production with staff traffic.

Verification: authorised production steps, each recorded.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G22-production-launch.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

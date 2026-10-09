---
goal: G18
title: "The whole journey works in staging against Guidewire pre-prod"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-release-engineering]
blocked_by: [G10, G11, G12, G13, G14, G16, G17, G27, G28]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 10-14
  review_and_verify: 3-5
  total: 13-19
  calendar_waits: Guidewire pre-prod connectivity for staging
  wait_days: 2-5
owner: Platform eng
status: blocked
---

# G18 The whole journey works in staging against Guidewire pre-prod

## Outcome

Staging runs the released build end to end: portal page, agent, photos, claim and attachments in Guidewire pre-prod. Implements D7, I2, I3; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g18--the-whole-journey-works-in-staging-against-guidewire-pre-prod).

## Scope

- In: Staging deploy through the G17 pipeline; synthetic customers; end-to-end smoke suite.
- Out: Load test (G19); pen test (G21).
- Depth: Build.

## Acceptance

- [ ] End-to-end claim with photos appears in Guidewire pre-prod from the staging page.
- [ ] Deployment readback shows the manifest's image, prompt, model and secret versions on the serving revision.
- [ ] Smoke suite runs on every staging deploy.

Verification: Authorised staging run with synthetic data. Execution scope: Staging and Guidewire pre-prod, after approval.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G18-staging-end-to-end.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

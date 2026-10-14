---
goal: G08
title: Staging and production run on Cloud Run with a rollback
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-release-engineering]
blocked_by: [G02, W0]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 3-5
  review_and_verify: 1-1
  total: 4-6
  calendar_waits: none
owner: Dev C
status: ready
---

# G08 Staging and production run on Cloud Run with a rollback

## Outcome

Two Cloud Run services (staging, production) with their own service accounts,
Cloud SQL databases and secrets, Vertex AI for the model, content-free
telemetry and a rehearsed rollback. Implements D7, D8 (region check), D10
(budget alert), I6 (traces).

## Scope

- In: container image, deploy commands or scripts, IAM, Cloud SQL, Secret
  Manager, Cloud Trace export with content capture off, budget alert,
  `/version` readback.
- Out: go-live and production traffic.
- Depth: Build at MVP depth. Cloud changes need the user's authorisation for
  the named project (W0: project, region, budget figure) when this ticket is
  run.

## Acceptance

- [ ] A1 Staging and production deploy from one pinned image; `/version` shows
  image digest, model ID and prompt version.
- [ ] A2 Each service runs as its own service account with only Vertex AI user,
  Cloud SQL client and accessor on its own secrets; no key files.
- [ ] A3 `gemini-3.5-flash` is confirmed available on Vertex AI in the chosen
  region (assumed `europe-west2`), with the source and date recorded.
- [ ] A4 Budget alert set at the agreed monthly figure (documented as an alert,
  not a cap) and Vertex AI quota checked for the assumed load.
- [ ] A5 Rolling back to the previous revision restores image, prompt and model
  configuration together; rehearsed once on staging.
- [ ] A6 One trace per turn with the session ID attribute and no prompt or
  response content, verified on staging.
- [ ] A7 `max-instances=3` and a 60 s request timeout are set.

Verification: authorised deployment to the named GCP project; readback
commands recorded.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G08-cloud-run-staging-and-production.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

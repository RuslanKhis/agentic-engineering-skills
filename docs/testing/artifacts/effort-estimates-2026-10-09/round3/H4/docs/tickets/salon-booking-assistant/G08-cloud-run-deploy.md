---
goal: G08
title: Staging and production on Cloud Run with traces and rollback
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-release-engineering]
blocked_by: [G02, G07]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted, team new to ADK (x1.5 included)
  hands_on: 4-6.5
  review_and_verify: 1.5-2.5
  total: 5.5-9
  calendar_waits: production booking API credential (request day 1)
owner: Dev C
status: blocked
---

# G08 Staging and production on Cloud Run with traces and rollback

## Outcome

The service runs in staging and production with its own service account, Cloud SQL, Secret Manager, content-free traces, a release manifest and rollback. Implements D6.

## Scope

- In: Dockerfile, deploy script, Cloud SQL instance and schema, secret, billing budget alert, beta-link feature flag
- Out: the widget and write handlers, which join the image in G09; SLOs and alerts (G12), CI gate (G10)
- Depth: previous revision kept; trace content capture off; manifest = image digest, prompt version, model ID, tool schema hash, secret version

## Acceptance

- [ ] A staging restart keeps a session and a proposal
- [ ] A trace shows one span per agent, tool and model call with session ID and no message text
- [ ] Rollback to the previous revision works; the budget alert exists; no secret is in the image or environment literals

Verification: Hosted checks on staging recorded with revision IDs; needs explicit authorisation for the GCP project and region.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G08-cloud-run-deploy.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

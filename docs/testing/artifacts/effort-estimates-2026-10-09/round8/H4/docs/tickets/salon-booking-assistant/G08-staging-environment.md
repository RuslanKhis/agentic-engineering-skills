---
goal: G08
title: A staging service runs on Google Cloud with its own identity and cost visibility
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-release-engineering]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 6-9
  review_and_verify: 2-4
  total: 8-13
  calendar_waits: none
owner: Dev C
status: ready
---

# G08 A staging service runs on Google Cloud with its own identity and cost visibility

## Outcome

D5, D6, D7, D9 and D11 infrastructure exist, and a placeholder build is deployed, before the application is ready.

## Scope

- In: GCP project and region (A9); a Cloud Run service with its own service account (Vertex user, Cloud SQL client); Cloud SQL Postgres; a billing alert at A3; Cloud Trace export with content capture off; a deploy script writing `release.json`; confirm that `gemini-3.8-flash` is served in the region and record current prices.
- Out: Deploying the real build and go-live (G09).
- Depth: Build at MVP depth: staging only, no production traffic.

## Acceptance

- [ ] The deployed revision reads back its image digest and `release.json`
- [ ] A trace from a placeholder model call shows token counts and no message text
- [ ] The service account has no roles beyond those listed

Verification: authorized live: needs a named GCP project and permission to create resources; not run in this session.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G08-staging-environment.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

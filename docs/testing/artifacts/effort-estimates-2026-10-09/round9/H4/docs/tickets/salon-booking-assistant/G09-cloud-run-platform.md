---
goal: G09
title: Staging and production on Cloud Run
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-release-engineering, adk-operational-guardrails]
blocked_by: [W1]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 5-8
  review_and_verify: 2-3
  total: 7-11
  calendar_waits: none
owner: Dev C
status: blocked
---

# G09 Staging and production on Cloud Run

## Outcome

The team has a staging and a production Cloud Run service with their database, secrets, telemetry and spend controls, and can deploy and roll back a release. Implements D6, D7, D9 (kill switch and budget alert), D10/I6 telemetry settings, D11.

## Scope

- In: GCP project setup from W1; one service account per environment with only Vertex AI user, Cloud SQL client and its own secret accessor; Secret Manager for the booking-API key; Cloud SQL Postgres (smallest tier) with `DatabaseSessionService` and the operations tables; Cloud Run service deploying a skeleton of the FastAPI app (the agent deploy itself happens in G11); env-flag kill switch; billing budget alert at 50/90/100 % of A3; Cloud Trace export with content capture off; 30-day session deletion job; CI running the unit tests and `eval/run.py --scripted`; `release.json` read back from the running revision. Look up current prices and region availability for the pinned model and Cloud SQL and update design §6.
- Out: Agent deploy (G11), SLOs and alerts (G16).
- Depth: Build. Floor: no secret in the image or env file in the repo; the kill switch works without a redeploy.
- Notes: Check the ADK span-retention fix (observability compatibility notes: 2.10.0 or later) before enabling trace export; if the pin is 2.8.0, record the gap.
- Execution scope: Needs W1 and the team's approval for each deployment and IAM grant.

## Acceptance

- [ ] Staging: a deploy shows the expected revision, model ID and prompt version via a readback endpoint; a rollback to the previous revision completes in under 5 minutes.
- [ ] With the kill switch on, `/chat` answers with the salon phone number and the trace shows no model call.
- [ ] An exported span and log line from a test turn contain no fixture name, phone number or message text.

Verification: Authorised cloud: deployment to the W1 project (staging, then production with the skeleton only). CI on every push.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G09-cloud-run-platform.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

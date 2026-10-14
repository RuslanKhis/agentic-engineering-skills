---
goal: G07
title: The assistant runs on staging and production with tests, alerts and rollback
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-release-engineering, adk-tool-auth-and-secrets]
blocked_by: [G02, G03, W0]
mentions_only: [G04, G08]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 8-12
  review_and_verify: 3.5-6
  total: 11.5-18
  calendar_waits: W0
owner: Dev A
status: blocked
---

# G07 The assistant runs on staging and production with tests, alerts and rollback

## Outcome

A repeatable pipeline deploys the G03 gateway with the G02 agent to Cloud Run
staging and production, with least-privilege identity, secrets, telemetry
without content, alerts and a rehearsed rollback. The G04 executor joins in
G08 through the same pipeline. Implements D7, D9 (budget alert), D10
(telemetry), D11. Includes 1 h handoff from Dev B. Waits for the GCP
resource approval (W0) before any resource is created.

## Scope

- In: Dockerfile, CI workflow, Cloud Run services, service account and
  grants, Secret Manager secret for the booking-API credential, Cloud SQL
  `assistant` database, ADK OpenTelemetry export with content capture off,
  log-based alerts, billing budget alert, release manifest, and the
  operations runbook that G08 tries on staging.
- Out: SLOs and dashboards (G12), live eval gate in CI (G10).
- Depth: MVP build; floor: no secrets in image or plain env values, pinned model.

## Acceptance

- [ ] A1 CI runs the offline tests on every pull request and blocks merge on failure.
- [ ] A2 Staging and production Cloud Run services run as a dedicated service account with only Vertex AI user, Cloud SQL client (IAM database auth) and accessor on the one secret; the image and env contain no secret values; a revoked or expired Cloud SQL credential shows as a 503 and a logged error, not a crash loop.
- [ ] A3 `release-manifest.json` records image digest, model ID, prompt hash and tool-schema hash; rolling staging back to the previous revision is rehearsed once and restores all four together.
- [ ] A4 An in-memory exporter test shows one span per agent, tool and model call with session ID set and no message text; a log assertion shows no message text in logs.
- [ ] A5 Log-based alerts on `operation_status` in (`uncertain`, `partial`) and on `auth_failed` email the team; each fired once on staging from a synthetic log line in the frozen D4 log schema (the real executor fires them again in G08/A2).
- [ ] A6 Billing budget alert at USD 300 (notification only); the kill switch documented as the hard stop; a Vertex 429 or quota error (fake) yields the "busy, try again shortly" reply.
- [ ] A7 `docs/runbook.md` covers uncertain and partial operations (reconcile query over the D4 operations table, who calls the customer, how to cancel the stray appointment), the kill switch and rollback.
- [ ] A8 Cloud SQL connections: the pool size × maximum instances for staging and production stays below the share of the instance's connection limit agreed with the booking API's owners; recorded in the release manifest and enforced by Cloud Run max instances.

Verification: CI run log; staging deploy and readback of the serving
revision; A4 offline; A5 and A3 on staging with the team's approval.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G07-deploy-ci-observability.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

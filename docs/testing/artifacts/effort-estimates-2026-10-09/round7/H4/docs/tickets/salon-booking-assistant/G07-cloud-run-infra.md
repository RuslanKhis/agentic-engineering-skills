---
goal: G07
title: Staging and prod infrastructure on Cloud Run
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-memory-architecture, adk-agent-observability, adk-release-engineering]
blocked_by: [G02]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 6-8
  review_and_verify: 2-3
  total: 8-11
  calendar_waits: none
owner: Dev A
status: blocked
---

# G07 Staging and prod infrastructure on Cloud Run

## Outcome

Implements D6, D7 and D11. Staging and prod Cloud Run services run the agent with sessions in Cloud SQL, so a restart keeps the conversation.

## Scope

- In and out: In: `infra/` scripts or Terraform for Cloud SQL Postgres, a service account per environment, the booking API credential in Secret Manager, Cloud Run services, `DatabaseSessionService`, telemetry to Cloud Trace with content capture off, a budget alert at the A3 figure, a deploy script that records the image, model ID and prompt version. Deploys the G02 build. The integrated build ships in G11. Out: canary.
- Depth: Build at MVP depth. Needs the team's authorisation for the GCP project, IAM and spend.

## Acceptance

- [ ] A deployed staging revision answers a `find_slots` question, and after a forced new revision the same session ID returns its history
- [ ] Logs and traces of that session contain no message text
- [ ] The previous revision can take traffic back with one command (tried once)

Verification: Authorised live: staging deploy readback. Prod services are created but not yet routed.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G07-cloud-run-infra.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

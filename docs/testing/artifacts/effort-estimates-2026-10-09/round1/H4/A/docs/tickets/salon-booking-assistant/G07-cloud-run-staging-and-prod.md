---
goal: G07
title: Customers of the five salons can use it live
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability (log fields, no content), adk-release-engineering (pinned release note, rollback), protect-adk-sensitive-data (no PII in logs)]
blocked_by: [G02, G03, G04, G06, user authorization of project/region/go-live]
phase: 1
profile: MVP or pilot
estimate: 10-14 h
suggested_owner: Dev C (web and infra)
status: blocked
---

# G07 Customers of the five salons can use it live

## Outcome

The assistant runs on Cloud Run with Cloud SQL sessions and ledger, Secret Manager and Vertex AI gemini-3.8-flash, with rollback by revision (D6, D9).

## Scope

- In: Dockerfile; service account; Secret Manager; Cloud SQL; DatabaseSessionService; Vertex region and model availability check with dated source; dated model price; quota and budget alert from G06; JSON logs without message text; release note (image digest, prompt version, model ID, ADK version); front-desk runbook for uncertain operations; staging first, then production at one salon.
- Out: Traces and SLIs (G09), retention job (G10).
- Depth: Minimal observability (traces deferred to G09). No deploy, IAM change or production write without the user's explicit authorization naming project and region.

## Acceptance

- [ ] Readback shows the serving revision, model ID and env; a session survives an instance restart.
- [ ] Rollback to the previous revision works; a sampled log line contains no customer message text or token.
- [ ] The production test booking on a test customer is created then cancelled, nothing else written.

Verification: Hosted checks on staging then production, within the user's authorization.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G07-cloud-run-staging-and-prod.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

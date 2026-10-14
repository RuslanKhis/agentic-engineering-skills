---
goal: G08
title: The service runs in staging and production with its own identity, secrets, traces and a tested rollback
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-release-engineering]
blocked_by: [G05, W3]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 4-8
  review_and_verify: 2-3
  total: 6-11
  calendar_waits: none
owner: Dev C
status: blocked
---

# G08 The service runs in staging and production with its own identity, secrets, traces and a tested rollback

## Outcome

Cloud Run staging and production services in the booking API's region (D7),
Cloud SQL, Secret Manager, Cloud Trace with content capture off (D11), billing
alerts and kill switch (D10), release record. Deploys the gateway as it is on
main (stub agent with the real pinned model); the integration goal (G09)
deploys the full agent.

## Scope

- In: `deploy/` scripts or Terraform, `sa-assistant` with least privilege, Cloud SQL instance and databases, secrets, alerts, `RELEASE.md` record.
- Out: production go-live for customers (launch ticket), SLO alerts (phase 2).
- Depth: MVP. Cloud commands only in the team's own project, run by the developer.

## Acceptance

- [ ] A1 Staging service with `sa-assistant` (Vertex AI user, Cloud SQL client and IAM database user, accessor on the booking API key secret only) answers an authenticated chat request sent with curl.
- [ ] A2 No secret in the image, source or plain environment variables (Secret Manager references only); image contents checked.
- [ ] A3 Cloud Trace shows gateway, agent and model spans with the session ID and no message content; token counts appear in logs per invocation.
- [ ] A4 Billing alerts at 50 % and 100 % of the assumed USD 300/month go to all three developers; max instances 3; flipping the kill switch in staging stops model calls within one minute.
- [ ] A5 Rolling back to the previous revision by traffic shift is rehearsed in staging and the command is in the runbook.
- [ ] A6 Each deploy writes a release record: image digest, prompt file hash, model ID, google-adk version, tool schema hash (empty fields allowed while the stub agent is deployed).
- [ ] A7 Cloud SQL is reached through the connector with IAM database authentication; no database password exists; removing the IAM database grant in staging yields 503 on chat (no crash loop), and restoring it recovers without redeploy.

Verification: authorised live checks in the team's staging project.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G08-cloud-run-deploy.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

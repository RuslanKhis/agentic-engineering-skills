---
goal: G03
title: Helpdesk staff open one URL with their Google login and use the assistant; everyone else gets 403
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-tool-auth-and-secrets, adk-agent-observability, adk-release-engineering]
blocked_by: [G01, G02, "GCP deploy and IAM permission", "A6: helpdesk@ group", "A10: dev UI accepted"]
phase: 1
profile: internal tool
estimate: 6-8 h
status: blocked
---

# G03 Colleagues use it behind IAP on Cloud Run

## Outcome

The 25 helpdesk staff use the assistant from a browser with their own Google
identity; non-members are refused before any agent code runs; no question or
answer text lands in logs. Implements D5, I1, I6.

## Scope

- In: deploy the ADK web app to one Cloud Run service (`max-instances=1`,
  in-memory sessions) in the chosen region; a runtime service account with
  only Vertex AI user and Secret Manager accessor on the one secret; IAP
  restricted to the `helpdesk@` group (directly on Cloud Run if supported in
  the region, else via an external load balancer; verify before choosing);
  `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false`; logs with IDs and token counts
  only; a deploy note recording revision, ADK version and model ID.
- Out: per-user session isolation (G06), traces and dashboards (G08),
  CI gates (G07).
- Depth: internal-tool hosting. Accepted risk (design, A10): the dev UI does
  not isolate sessions between team members.

## Acceptance

- [ ] A `helpdesk@` member completes the VPN journey on the hosted URL.
- [ ] A non-member Google account gets 403 from IAP.
- [ ] Searching logs for the test question text finds nothing.
- [ ] Deploy note lists revision, `google-adk` version and model ID.

Verification: offline tests pass before deploy; authorised hosted checks on
the user's GCP project. Check deploy flags with the installed
`adk deploy cloud_run --help` before running them.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G03-hosted-behind-iap.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

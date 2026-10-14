---
goal: G04
title: The 25 helpdesk members use the assistant at an internal URL with their Google sign-in
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-tool-auth-and-secrets, adk-agent-observability, adk-release-engineering]
blocked_by: [G01, G02, G03, W1]
phase: 1
profile: internal tool
estimate:
  hands_on: 3-4
  review_and_verify: 1-2
  total: 4-6
  calendar_waits: none
owner: Dev B
status: blocked
---

# G04 Hosted for the helpdesk group

## Outcome

One Cloud Run service behind IAP, open only to the helpdesk group, runs the
assistant with a least-privilege runtime service account and the Atlassian
token from Secret Manager (D5–D8, D10; I1, I6). Blocked by W1 and by the user
naming the GCP project and approving IAM and IAP changes.

## Scope

- In: container, `max-instances=1`, runtime service account
  (`secretAccessor` on one secret, `aiplatform.user`), IAP policy for the
  group, logs with metadata only and OTel content capture off, revision labels
  (model, prompt hash, pin), billing budget alert, Vertex price recorded.
- Out: Jira creation (G06), persistence (G07), traces (G11).
- Depth: minimal observability and release.

## Acceptance

- [ ] A member gets a cited answer and a draft at the URL.
- [ ] A non-member account is refused by IAP.
- [ ] One test conversation's logs contain no prompt or answer text; a restart drops the chat and creates nothing.

Verification: authorised hosted checks plus a log read; previous revision kept for rollback.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G04-cloud-run-behind-iap.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

---
goal: G05
title: Hosted on Cloud Run behind IAP for the helpdesk group
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-release-engineering]
blocked_by: [G01, G04, "open decision A9: staff sign in with Google identities"]
phase: 1
profile: internal tool
estimate:                # human hours, agent-assisted
  hands_on: 3.5-5.5
  review_and_verify: 1.5-2
  total: 5-7.5
  calendar_waits: helpdesk Google group and IAP enablement or OAuth consent by Workspace or cloud admin (assume 1-3 working days); possible internal security review (unknown, ask on day 1)
owner: Engineer B
status: blocked
---

# G05 Hosted on Cloud Run behind IAP for the helpdesk group

## Outcome

All 25 helpdesk staff use the assistant from one URL with their own Google
sign-in. Non-members are refused. Implements D4, D5, D9 and invariants I1–I2
in the hosted environment.

## Scope

- In: container build. Cloud Run service with the runtime service account
  (Vertex AI user, and Secret Manager accessor on the two secrets only).
  min = max = 1 instance. Ingress reachable only through IAP. IAP limited to
  the helpdesk group, with the matching `aud` configured. JSON logs with IDs,
  tool names, status, latency and token counts, and no message content. A
  release record (image digest, model ID, ADK pin, lock hash, secret versions)
  in the plan's G05 evidence. A rehearsed rollback to the previous revision.
  The `ITSDTEST` → `ITSD` switch is a recorded config change after the
  helpdesk lead agrees.
- Out: persistent sessions (G06), traces (G10), CI gate (G09).
- Depth: Cloud Run behind IAP; minimal observability; no canary. If A9 turns
  out false (no Google identities), stop and turn this into a discovery
  ticket for the identity front door.

## Acceptance

- [ ] A group member opens the URL, asks the VPN 809 gold question and gets a cited answer.
- [ ] A non-member account receives IAP's 403; a direct request to the `run.app` URL bypassing IAP is refused.
- [ ] After a new revision, approving a confirmation pending from before the restart creates no ticket and shows a clear message.
- [ ] A log sample (`gcloud logging read`) shows IDs, tool names and token counts and no message text.
- [ ] Release record complete; rollback to the previous revision rehearsed once.

Verification: authorised hosted checks by hand with a member and a
non-member account, in the team's own project only.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G05-cloud-run-behind-iap.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

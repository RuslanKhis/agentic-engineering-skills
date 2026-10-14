---
goal: G04
title: The helpdesk group can reach the assistant on Cloud Run, and nobody else can
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-release-engineering, adk-operational-guardrails]
blocked_by: []
phase: 1
profile: internal tool
estimate:                # human hours, agent-assisted
  hands_on: 2-3
  review_and_verify: 1-2
  total: 3-5
  calendar_waits: none
owner: Dev B
status: ready
---

# G04 The helpdesk group can reach the assistant on Cloud Run, and nobody else can

## Outcome

Current app on Cloud Run behind IAP with least-privilege identity, secrets, content-free logs and a spend stop. Implements D7, D8, D9. Cloud changes need the user's explicit go-ahead for the named project and region.

## Scope

- In: Dockerfile, service account (Vertex user plus the two secrets), `max-instances=1`, IAP for the helpdesk group, JSON logs, Vertex quota and budget alert at A3, CI running offline tests.
- Out: SLOs, canary, multi-instance (G07), final integration (G05).
- Depth: hosting built; observability and release minimal; previous revision kept for rollback.

## Acceptance

- [ ] A helpdesk group member loads the page; budget alert and quota are visible
- [ ] A non-member is denied by IAP
- [ ] A log sample has IDs and token counts but no message text; the release manifest has no model or package aliases

Verification: hosted checks in the authorized project; `pytest` in CI.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G04-cloud-run-behind-iap.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

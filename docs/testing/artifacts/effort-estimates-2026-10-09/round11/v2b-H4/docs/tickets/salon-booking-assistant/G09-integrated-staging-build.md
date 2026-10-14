---
goal: G09
title: The real assistant runs end to end in staging behind the gateway
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-workflow-design
supporting_skills: [deploy-adk-on-google-cloud, safe-api-tool-calls]
blocked_by: [G02, G03, G04, G05, G06, G08]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 4-6
  review_and_verify: 1-2
  total: 5-8
  calendar_waits: none
owner: Dev A
status: blocked
---

# G09 The real assistant runs end to end in staging behind the gateway

## Outcome

Replace the stub agent, mock confirm service and fake port with the real agent,
confirm service and HTTP adapter inside the gateway, and deploy that build to
staging. Includes 2 h handoff from Dev B (adapter) and Dev C (gateway, page,
deployment).

## Scope

- In: wiring in `app/gateway/`, configuration per environment, one local end-to-end test, staging deploy.
- Out: the staging walkthrough with real bookings and go-live (next goal).
- Depth: MVP. Staging booking API only.

## Acceptance

- [ ] A1 Locally (gateway + local PostgreSQL + fake port), an HTTP test goes chat → proposal card → confirm → receipt, and the next chat turn reports the outcome.
- [ ] A2 The same build is deployed to staging with the HTTP adapter pointing at the staging booking API; one chat that proposes (without confirming) succeeds from the staging chat page.
- [ ] A3 With the kill switch on, the real confirm and status routes still complete an already-proposed change while chat is refused.
- [ ] A4 The staging release record carries the real prompt file hash and tool schema hash.

Verification: local HTTP test offline; authorised staging check.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G09-integrated-staging-build.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

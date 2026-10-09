---
goal: G05
title: The helpdesk pilot uses it on Cloud Run behind IAP
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-agent-observability, adk-release-engineering, adk-tool-auth-and-secrets]
blocked_by: [G04, "cloud authorisation: project ID, region and explicit go-ahead for deploy and IAM changes"]
phase: 1
profile: internal tool
estimate:                # human hours, agent-assisted
  hands_on: 2.5-3.5
  review_and_verify: 1.5-2.5
  total: 4-6
  calendar_waits: IAP group and consent setup 0-2 days; 3 working days of pilot use
owner: Engineers A and B jointly
status: blocked
---

# G05 The helpdesk pilot uses it on Cloud Run behind IAP

## Outcome

3-5 technicians, and then the whole helpdesk group, use the assistant on real runbooks and real tickets. Implements D4, D5, D6 and invariants I1, I6, I7. Every decision is provisional on the assumed answers at the top
of the design. The implementation route is in the plan's G05 section.

## Scope

- In: container, runtime service account (Vertex user, Firestore user, Secret Manager accessor on two secrets), Cloud Run with max instances 1, IAP restricted to the helpdesk group, Firestore TTL on drafts (90 days), budget alert, structured-log policy, pilot feedback form; reuses the team's existing deploy template
- Out: CI gate (G09), SLOs and alerts, usage dashboard (G11)
- Depth: internal-tool hosting, secrets and observability. Floor: secrets only in Secret Manager; no prompt or answer text in logs; budget alert at the assumed USD 300 a month; revision, image digest, model ID and prompt version recorded.

## Acceptance

- [ ] Non-member of the helpdesk group: 403 from IAP
- [ ] A member completes the VPN journey on the deployed revision
- [ ] Log sample shows session, invocation and draft IDs and token counts, and no content
- [ ] Budget alert exists; current Vertex price and its date recorded
- [ ] Rollback to the previous revision demonstrated once
- [ ] Pilot feedback from at least 3 technicians recorded, including time-to-runbook estimates

Verification: authorised hosted check using the team's template commands; not runnable until cloud authorisation is given.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G05-cloud-run-iap-pilot.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

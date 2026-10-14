---
goal: G05
title: The helpdesk lead completes the full journey on the deployed assistant
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [deploy-adk-on-google-cloud, safe-api-tool-calls]
blocked_by: [W1, G02, G03, G04]
phase: 1
profile: internal tool
estimate:                # human hours, agent-assisted
  hands_on: 1-2
  review_and_verify: 1
  total: 2-3
  calendar_waits: helpdesk lead available for a 1-hour walkthrough
owner: Dev A
status: blocked (W1, G02, G03, G04)
---

# G05 The helpdesk lead completes the full journey on the deployed assistant

## Outcome

G01–G03 deployed together with bot tokens; the pilot group (3–5 people) can use it. Covers I5, I6 and live checks of D3, D5.

## Scope

- In: redeploy through G04's pipeline, bot A/B tokens, one Jira sandbox issue, gold set re-run on the deployed service, lead walkthrough (5 questions, 1 ticket), baseline latency, switch to `ITHELP` after sign-off.
- Out: rollout to all 25 (G06), durable proposals (G07).
- Depth: pilot only, per the graduation conditions in the design.

## Acceptance

- [ ] Exactly one sandbox issue with label `op-<id>` and the footer; the lead signs off
- [ ] Gold set on the deployed service within 5 points of G01's result; a create in another project returns 403
- [ ] A log sample after the walkthrough contains no message text

Verification: bounded live and hosted checks; needs G04's go-ahead and W1 delivered.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G05-integrated-pilot.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

---
goal: G26
title: On-call can run it
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: adk-agent-observability
supporting_skills: [deploy-adk-on-google-cloud]
blocked_by: [G19, G21]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 16-24
  review_and_verify: 4-8
  total: 20-32
  calendar_waits: none
owner: Eng E
status: blocked
---

# G26 On-call can run it

## Outcome

Runbooks for uncertain operations, Guidewire outage, model outage, operator stop, rollback and restore, and the handover to claims-IT on-call; reruns the restore drill on the release candidate.

## Scope

- In: runbooks linked from alerts, on-call rota, drill evidence.
- Out: call-centre tooling (G28).
- Depth: build.

## Acceptance

- [ ] Each alert links to a runbook
- [ ] A tabletop of the lost-reply case ends with one claim and a recorded receipt
- [ ] Restore drill on the release candidate passes

Verification: Tabletop and staging drill.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G26-runbooks.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

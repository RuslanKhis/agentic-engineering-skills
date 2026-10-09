---
goal: G09
title: Gateway hosted with limits and logs
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-operational-guardrails, adk-agent-observability, adk-release-engineering]
blocked_by: [G03, G08]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-5
  review_and_verify: 2-3
  total: 5-8
  calendar_waits: none
  wait_days: 0
owner: Dev C
status: blocked
---

# G09 Gateway hosted with limits and logs

## Outcome

The G03 gateway and agent run in staging and production with spend limits and content-free logs. I5, D7. Route and rationale: [plan, G09](../../plans/salon-booking-assistant.md#g09--gateway-hosted-with-limits-and-logs).

## Scope

- In: Cloud Run deploy on G08; `RunConfig(max_llm_calls=8)`; 40 turns/customer/day counter; IP rate limit; structured logs and traces with session/operation IDs and token counts; release notes with the bundle; one rollback rehearsal
- Out: SLOs (G16), CI gate (G12)
- Depth: build minimal for MVP

## Acceptance

- [ ] A staging turn works through the hosted gateway; restart mid-conversation keeps the session
- [ ] 41st turn of the day and 9th model call in a turn are refused; traffic moved back to the previous revision once
- [ ] A log sample contains no names, phones or message text

Verification: hosted staging checks (needs the team's authorization to deploy).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G09-hosted-gateway.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

---
goal: G06
title: The assistant runs on staging and production with spend caps and no customer content in logs
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: deploy-adk-on-google-cloud
supporting_skills: [adk-operational-guardrails, adk-agent-observability, adk-release-engineering]
blocked_by: [G02]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted, 1.5x new-to-ADK applied
  hands_on: 6-9
  review_and_verify: 3-5
  total: 9-14
  calendar_waits: none
owner: Dev B
status: blocked
---

# G06 Staging and production on Cloud Run with caps

## Outcome

The gateway and agent run on Cloud Run in staging and production (D7) with a
dedicated service account, the booking API key in Secret Manager, sessions and
proposals on Cloud SQL Postgres, the floor's spend stop (D6) and traces with
token counts but no content (D9, I6, I7).

## Scope

- In: region per O3 (staging can start in a provisional region); verify
  `gemini-3.8-flash` on Vertex in that region (O2); `DatabaseSessionService`;
  `RunConfig(max_llm_calls=10)`; per-customer 40 turns/day and per-IP 10/min
  (in-memory, max 2 instances); Vertex quota lowered; budget alert at A3;
  content capture off; release manifest (image digest, ADK version, model
  ID, prompt version, tool-schema hash, secret version).
- Out: SLOs/alerts (G12), durable budgets (G10), retention job (G13).
- Depth: MVP. Floor: no secrets in image or env files committed; billing
  alert is an alert, not a cap. Needs explicit authorization before any
  provisioning.

## Acceptance

- [ ] Staging: a conversation survives a forced revision restart.
- [ ] 11th model call in a turn, 41st turn in a day and 11th request in a minute each get the fallback reply without a model call.
- [ ] Logs and traces for a staging conversation contain IDs, outcomes and token counts, and no message text or names.
- [ ] Release manifest written for the deployed revision; previous revision kept.

Verification: offline cap tests; authorized staging deployment checks.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G06-cloud-run-with-caps.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

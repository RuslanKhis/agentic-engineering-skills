---
goal: G03
title: A local gateway runs the agent, keeps a versioned claim draft and survives a restart
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: adk-workflow-design
supporting_skills: [adk-model-and-output-contracts, adk-memory-architecture]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 16-28
  review_and_verify: 6-10
  total: 22-38
  calendar_waits: none
  wait_days: 0
owner: Eng D
status: ready
---

# G03 A local gateway runs the agent, keeps a versioned claim draft and survives a restart

## Outcome

The team has the kept skeleton every later goal extends: gateway-owned Runner, durable sessions, a versioned draft record, a pinned model and a call cap. Implements D2, D4 and D8.

## Scope

- In: `app/gateway/`, `app/agent/`, `app/drafts/`; `DatabaseSessionService` on local Postgres; `RunConfig.max_llm_calls`; trusted-state interface (`customer_id`, `draft_id` written by code) with a local-only stub identity; placeholder tools; scripted-model test harness.
- Out: Real auth (G04), full instruction and tools (G07), cloud deployment (G16).
- Depth: Kept code. Floor: pinned model ID from config; call cap; no secrets in code.

## Acceptance

- [ ] The chosen google-adk pin is recorded, and every ADK interface the design names (`App`, `Runner`, `RunConfig.max_llm_calls`, `DatabaseSessionService`, `output_schema`, `before_tool_callback`) is confirmed against it
- [ ] A scripted conversation writes draft v1 then v2 with different hashes
- [ ] After a real process restart the same session and draft v2 are returned
- [ ] A turn exceeding `max_llm_calls` ends with the designed error, and no model alias appears in config

Verification: Offline scripted-model tests plus local integration with a Postgres container: `pytest tests/` (proposed).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G03-walking-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

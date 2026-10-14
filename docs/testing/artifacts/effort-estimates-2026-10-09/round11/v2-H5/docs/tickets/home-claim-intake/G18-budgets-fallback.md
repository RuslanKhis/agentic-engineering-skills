---
goal: G18
title: In a storm or an outage customers can still report damage, and spend stays bounded
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-operational-guardrails
supporting_skills: [adk-model-and-output-contracts]
blocked_by: [G06, G16, W10]
phase: 1
profile: production
estimate:
  hands_on: 16-24
  review_and_verify: 6-9
  total: 22-33
  calendar_waits: none
owner: Eng A
status: proposed
---

# G18 In a storm or an outage customers can still report damage, and spend stays bounded

## Outcome

Implements D13: per-draft allowance, global admission, operator kill switch,
one retry owner for model calls and fallback to the prefilled classic form.
Handoff: 1 h from Eng C on Cloud Run settings.

## Scope

- In: `app/guards/` (allowance table, admission token bucket, kill switch
  flag read on every request), `RunConfig.max_llm_calls`, model retry
  options set once, `degraded` API answer with prefill payload, daily token
  ceiling, billing budget alert.
- Out: load test (G20).
- Depth: production.

## Acceptance

- [ ] A1 A draft that reaches 60 model calls answers `degraded` with the prefill; the count survives a restart.
- [ ] A2 When admission is full, new drafts get `degraded` instead of an error; running drafts continue within their allowance.
- [ ] A3 Flipping the kill switch routes new and existing drafts to the form within one minute, without a deploy and without the agent's involvement.
- [ ] A4 Vertex 429, 5xx or timeout: at most two model attempts per call across ADK and application layers, then `degraded`; no retry storm in a scripted burst.
- [ ] A5 The daily token ceiling stops new agent turns when reached; the billing budget alert for the project exists.

Verification: offline scripted-model tests; staging check of A3.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G18-budgets-fallback.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

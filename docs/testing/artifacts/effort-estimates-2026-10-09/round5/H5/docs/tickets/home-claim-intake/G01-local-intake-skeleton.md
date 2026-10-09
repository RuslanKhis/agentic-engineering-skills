---
goal: G01
title: "A customer can describe a loss and get a saved, versioned claim draft (local)"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-workflow-design
supporting_skills: [adk-tool-interface-design, adk-memory-architecture]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 8-12
  review_and_verify: 4-6
  total: 12-18
  calendar_waits: none
  wait_days: 0
owner: Agent lead
status: ready
---

# G01 A customer can describe a loss and get a saved, versioned claim draft (local)

## Outcome

Locally, a scripted or real conversation produces a versioned claim draft that survives a process restart and is shown back as a summary. Implements D2, D8, D9; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g01--a-customer-can-describe-a-loss-and-get-a-saved-versioned-claim-draft-local).

## Scope

- In: Pin google-adk and record it; `intake_agent` factory; `get_claim_draft` and `update_claim_draft` tools; Postgres draft table; DatabaseSessionService against local Postgres; offline Runner test with a scripted model; confirm model ID availability on Vertex AI EU from current docs (O2).
- Out: Identity (G05), photos (G06, G07), instruction quality (G08), Guidewire (G10).
- Depth: Production structure, local only; model pinned; `max_llm_calls` set from day one (full budgets in G13).

## Acceptance

- [ ] Scripted conversation fills loss date, cause, rooms and description; draft version increments on each change.
- [ ] Kill and restart the process mid-draft; resuming the session returns the same draft version.
- [ ] `update_claim_draft` with an unknown field or invalid date returns an actionable error and leaves the draft unchanged.
- [ ] ADK pin and every ADK interface named in the design checked against that pin; Vertex AI EU availability of `gemini-3.8-flash` recorded with source and date.

Verification: Offline: `pytest tests/agent` with scripted model; local integration: restart test against local Postgres. Execution scope: Local only; no cloud or Guidewire.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G01-local-intake-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

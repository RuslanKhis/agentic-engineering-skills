---
goal: G02
title: A message to the claim assistant updates a saved, validated claim draft
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-workflow-design
supporting_skills: [adk-tool-interface-design, adk-model-and-output-contracts, adk-memory-architecture]
blocked_by: []
phase: 1
profile: production
estimate:
  hands_on: 12-18
  review_and_verify: 4-6
  total: 16-24
  calendar_waits: none
owner: Eng A
status: ready
---

# G02 A message to the claim assistant updates a saved, validated claim draft

## Outcome

The walking skeleton: a FastAPI service runs one ADK `LlmAgent` through a
`Runner`, persists the conversation and a versioned claim draft, and returns
one completed JSON turn. Implements D1, D3, D4, D10, D11 (turn shape).

## Scope

- In (proposed modules): `app/api/turns.py` (`POST /v1/drafts/{draft_id}/turns`
  with a client message ID), `app/agent/factory.py`, `app/agent/tools.py`
  (`update_claim_draft`, `get_draft_status` — the other two tools come in
  G06), `app/drafts/model.py` (Pydantic `ClaimDraft` with a provisional field
  list until the code lists arrive), `app/drafts/store.py`, `app/config.py`
  (model ID, `max_llm_calls`), `release/manifest.yaml` stub.
- Route: `DatabaseSessionService` against local Postgres; tools read
  `draft_id` from session state, never from arguments; code computes missing
  fields after each tool call.
- Out: real identity (G03, a test header stands in), photos (G05),
  instructions quality (G06), screening (G12).
- Depth: production structure from the start; a scripted model for tests,
  so no paid calls are needed.

## Acceptance

- [ ] A1 With a scripted model, a turn calls `update_claim_draft`, the draft is stored as version 2 and the response is one JSON object with `turn_id`, `reply`, `draft_version` and `missing_fields`.
- [ ] A2 The model ID comes from configuration and the manifest; a test fails if the ID is an alias (contains `latest`) or is missing.
- [ ] A3 A scripted model that keeps calling tools stops at `max_llm_calls` = 8 with a `turn_limit` result; tool writes validated before the stop are kept as their own draft versions, nothing else is written.
- [ ] A4 `update_claim_draft` with an invalid value (loss date in the future, unknown cause code) returns an actionable error and leaves the draft unchanged.
- [ ] A5 A scripted model that returns an error, a safety-blocked response, prose instead of a tool call or malformed tool arguments gets at most one repair attempt, then the turn returns a designed "please try again" result; nothing is persisted from the invalid payload.
- [ ] A6 The ADK version pin (working assumption `google-adk==2.8.0`) and the availability of `gemini-3.8-flash` on a Vertex AI EU regional endpoint are confirmed from official documentation, with URL and date recorded in the plan's evidence; if unavailable, the fallback in D3 is raised as a decision.
- [ ] A7 After a process restart between two turns, the next turn sees the same draft version and conversation (local Postgres container).

Verification: offline and local integration — `pytest tests/agent tests/drafts`
with a Postgres container; no Vertex calls.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G02-agent-service-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

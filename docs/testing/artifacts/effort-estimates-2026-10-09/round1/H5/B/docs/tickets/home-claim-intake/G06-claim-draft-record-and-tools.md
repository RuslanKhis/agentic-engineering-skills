---
goal: G06
title: The assistant fills a versioned claim draft through validated tools
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-memory-architecture, adk-model-and-output-contracts]
blocked_by: [G04]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 12-20
  review_and_verify: 12-20
  total: 24-40
  calendar_waits: none
owner: E2
status: blocked
---

# G06 The assistant fills a versioned claim draft through validated tools

## Outcome

What the customer tells the assistant lands in an owner-scoped, versioned draft record that survives restarts, and code decides when it is complete. Implements D1, D3, D8 (draft side), D13.

## Scope

- In: Postgres schema and migrations for drafts (versioned), photo metadata, observations; `DatabaseSessionService` on the same database; tools `get_claim_draft` and `record_claim_details` with enum/ISO validation and actionable errors; completeness computed in code; summary JSON endpoint.
- Out: Submission (G10), photos (G08).
- Depth: Build. Floor: draft writes only for the verified owner.
- Route: Application repository layer + ADK function tools; Postgres in a container for tests.
- Supporting skills: `adk-memory-architecture` (session service and draft as the authoritative record); `adk-model-and-output-contracts` (enum and date validation shape returned to the model)
- Execution scope: Local only.

## Acceptance

- [ ] A scripted conversation records cause, loss date and rooms; draft version increments per change
- [ ] Invalid values return an actionable error result; the draft is unchanged
- [ ] Process restart: the session and draft are reloaded intact
- [ ] Tool declarations total under the agreed size and there are exactly three intake tools

Verification: Offline + local integration: pytest with Postgres container and a real restart.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G06-claim-draft-record-and-tools.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

---
goal: G05
title: Keep a versioned claim draft with a required-field checklist
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: adk-memory-architecture
supporting_skills: [safe-api-tool-calls]
blocked_by: [G01, G02]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 18-28
  review_and_verify: 6-10
  total: 24-38
  calendar_waits: none
owner: Eng D
status: blocked
---

# G05 Keep a versioned claim draft with a required-field checklist

## Outcome

An owner-scoped, versioned claim-draft record and a checklist computed in code from the G01 field mapping, so the agent asks only for what is missing. Implements D4 and the code side of the model/code split.

## Scope

- In: `app/store/drafts.py`, schema migration, version hash over canonical fields, checklist function, validation (dates not in future, enums, lengths).
- Out: agent tools (G06), submission (G11).
- Depth: build; draft text bounded and stored as plain text.

## Acceptance

- [ ] Updating a field creates a new version with a new hash; the checklist reports remaining required fields
- [ ] Invalid values (future loss date, unknown cause) are rejected with an actionable message
- [ ] A draft is readable only by its owner; a restart preserves it

Verification: Offline plus local Postgres restart test.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G05-claim-draft-store.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

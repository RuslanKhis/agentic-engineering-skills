---
goal: G04
title: The agent turns the customer's story into a complete claim draft without ever promising cover
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-agent-instructions, adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted (team new to ADK, x1.5 included)
  hands_on: 18-28
  review_and_verify: 6-10
  total: 24-38
  calendar_waits: none
owner: Eng C
status: ready
---

# G04 The agent turns the customer's story into a complete claim draft without ever promising cover

## Outcome

Implements D1 (one intake agent), D6 (draft-only tools), invariants I3 and I5, target T2.

## Scope

- In:
  - `claim_drafts` table with versions; required-field validator
  - Tools `select_policy`, `update_claim_draft`, `request_photo`, each checking trusted `customer_id`/`draft_id` state; results ≤ 1 KB with status and missing fields
  - Instruction `intake-v1`: German and English, one question at a time, no cover/liability/payout statements, emergency hotline repetition
  - Code-rendered summary endpoint; fake policy API
- Out: Photos (G05), submission (G06), adversarial suite (G08)
- Depth: Build; floor: model pinned, no ClaimCenter tool in the agent.

## Acceptance

- [ ] Five scripted conversations produce the expected drafts
- [ ] A draft missing the loss date makes the agent ask for it
- [ ] `select_policy` with a policy not in trusted state returns an error result and leaves the draft unchanged
- [ ] The summary contains no model-generated prose

Verification: Offline Runner tests with a scripted model; rendered-request snapshot test.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G04-intake-agent-and-claim-draft.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

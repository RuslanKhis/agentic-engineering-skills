---
goal: G05
title: The agent records what the customer says into a versioned claim draft through four narrow tools
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-tool-interface-design
supporting_skills: [adk-memory-architecture, adk-agent-security]
blocked_by: [G01, G04]
phase: 1
profile: production
estimate: 64-100 h
status: blocked
---

# G05 The agent records what the customer says into a versioned claim draft through four narrow tools

## Outcome

A versioned `claim_drafts` record is the authoritative pre-submission state; the agent reads policies and the draft and proposes field changes that code validates, with completeness computed per loss type. Implements D1, D3, I1, I5 in the design.

## Scope

- In: Postgres schema (`claim_drafts`, versioned); tools `list_my_policies`, `get_claim_draft`, `update_claim_draft(changes)`, `get_photo_findings` (stub until G07); completeness rules per loss type; `before_tool_callback`; policy reader behind a `GuidewireClient` read interface with the fake.
- Out: Instruction quality (G09), submission (G10), real Guidewire reads (G11).
- Depth: Build; floor: no tool accepts `customer_id`/`draft_id` as an argument; results bounded (≤ 10 policies, masked numbers).
- Route: `FunctionTool`s in `app/agent/tools.py` reading `tool_context.state['customer_id']`; draft repository in `app/claims/drafts.py`; declarations dumped in a test.
- Prerequisites: G01, G04; G02 for the account mapping (the fake is used until then).
- Supporting skills:
  - `adk-memory-architecture`: session vs draft record ownership, versioning and retention
  - `adk-agent-security`: `before_tool_callback` ownership check keyed on trusted state
- Execution scope: Local only: repository files, local Postgres/containers, scripted models and fake Guidewire. No cloud, IAM, Guidewire or paid model calls.

## Acceptance

- [ ] A scripted conversation updates loss date, loss type and description; the draft version increments and `missing_fields` shrinks to empty.
- [ ] An invalid value (future loss date, unknown enum) is rejected with an actionable error result and the draft is unchanged.
- [ ] Forbidden: the declaration dump shows exactly four tools, none with an identity or draft-ID parameter and no submit capability.

Verification: Offline: tool unit tests, scripted-model Runner tests, declaration snapshot with byte count.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G05-claim-draft-and-intake-tools.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

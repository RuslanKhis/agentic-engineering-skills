---
goal: G06
title: 20-case evaluation set and runner
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: []
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted (1.5x new-to-ADK multiplier applied); copied from the plan
  hands_on: 3.5–5.5
  review_and_verify: 1–2
  total: 4.5–7.5
  calendar_waits: none
owner: Dev B
status: ready
---

# G06 20-case evaluation set and runner

## Outcome

the team can say how often the assistant picks the right action before launch. I2, I4.

## Scope

- In: 20 multi-turn cases on synthetic customers: 5 book, 5 move, 4 cancel, 2 ambiguous date/salon needing clarification, 2 out of scope (prices dispute, complaints), 1 other customer's appointment, 1 injected instruction in a service description. Expected tool calls and proposal payloads; a runner that reports per-case pass/fail and model calls. Out: CI gate (G10), judge-model scoring.
- Route: ADK evaluation against the fake API; live model runs capped at 200 model calls per run.
- Prerequisites: G02 to run; G03 for propose cases.
- Depth: MVP; deterministic checks on proposals and tool calls, no LLM judge. Floor kept: no secrets in code or logs, model pinned, no booking change without the customer's Confirm, spend stop. Later controls: see the plan's phase 2 goals G10–G16.
- Supporting skills: none

## Acceptance

- [ ] runner reports all 20 cases with pass/fail and call counts
- [ ] the two security cases assert zero proposals for the forbidden action
- [ ] a baseline result is recorded with model and prompt version

Verification: offline runner structure test; live run needs a Vertex AI project (bounded, authorized by the team). Execution scope: local; live run only with a named project.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G06-evaluation-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

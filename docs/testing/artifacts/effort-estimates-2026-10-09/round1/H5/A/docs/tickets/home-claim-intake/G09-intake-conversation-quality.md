---
goal: G09
title: The agent gathers a complete claim in a natural conversation in both languages and stays within its limits
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-instructions
supporting_skills: [adk-agent-evaluation, adk-tool-interface-design]
blocked_by: [G05, G08]
phase: 1
profile: production
estimate: 100-160 h
status: blocked
---

# G09 The agent gathers a complete claim in a natural conversation in both languages and stays within its limits

## Outcome

`prompts/intake/v1.md` reaches the G08 thresholds: completeness, field accuracy and zero policy violations on the adversarial slice; safety and injury flags route to the phone card set by code. Implements D1, D2, I6, I10 in the design.

## Scope

- In: Instruction text with templated state (`language`, `loss_type`, `missing_fields`); exemplars; rendered-request snapshot test; language handling; injury yes/no handling.
- Out: Output release check (G13), model change (release via G18).
- Depth: Build; cut-line option 2: English moves to P2-06 if phase 1 runs high.
- Route: Instruction file loaded by the factory; state injected by trusted code before `run_async`.
- Prerequisites: G05, G08.
- Supporting skills:
  - `adk-agent-evaluation`: iteration against the G08 dev set
  - `adk-tool-interface-design`: tool-use guidance consistent with declarations
- Execution scope: Local only: repository files, local Postgres/containers, scripted models and fake Guidewire. No cloud, IAM, Guidewire or paid model calls. Live eval runs need the authorised eval budget.

## Acceptance

- [ ] Dev-set completeness and field accuracy at or above the thresholds recorded in `evals/SUMMARY.md`.
- [ ] When the draft sets `injured=yes` the response contains no follow-up injury questions and the UI flag for the phone card is set by code.
- [ ] Forbidden: zero coverage or payout statements across the adversarial slice (repeated runs per G08 policy).

Verification: Offline rendered-request snapshot; bounded live eval runs within budget.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G09-intake-conversation-quality.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

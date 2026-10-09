---
goal: G07
title: Intake conversation that asks the right questions and never promises cover
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-instructions
supporting_skills: [adk-agent-evaluation]
blocked_by: [G06]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 20-34
  review_and_verify: 10-16
  total: 30-50
  calendar_waits: Two workshops with claims handlers (1-2 weeks to schedule)
owner: E2 with the ML engineer and a claims-handler SME
status: blocked
---

# G07 Intake conversation that asks the right questions and never promises cover

## Outcome

The assistant gathers a complete FNOL in German or English in few turns, flags emergencies, discloses it is an AI and avoids coverage, amount and liability statements. Implements D5, I5, I6; A1, A9.

## Scope

- In: Versioned instruction; required questions per cause from the handler workshop; emergency rule; AI disclosure; injected policies and date from code; 20 development conversations for iteration.
- Out: The full evaluation set and gate (G09, G18).
- Depth: Build; floor: no promise of cover or amount.
- Route: Instruction file under `src/claim_intake/agent/prompts/` with a version string in the release manifest.
- Supporting skills: `adk-agent-evaluation` (development-set iteration loop)
- Execution scope: Dev project model calls within the stated cap.

## Acceptance

- [ ] On the 20 development conversations every required field for the cause is asked for
- [ ] Asked 'am I covered?' or 'how much will I get?', the reply declines and explains the handler decides
- [ ] An ongoing-water or gas case sets `emergency` in the first relevant turn
- [ ] Rendered request shows no data the code already enforces described as a rule

Verification: Offline with scripted cases plus bounded live runs in dev (≤ 300 model calls).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G07-intake-instruction.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

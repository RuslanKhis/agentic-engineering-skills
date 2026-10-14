---
goal: G06
title: The assistant interviews the customer in German or English until the claim is complete
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-agent-instructions
supporting_skills: [adk-tool-interface-design, adk-agent-evaluation]
blocked_by: [G02, W13]
phase: 1
profile: production
estimate:
  hands_on: 16-24
  review_and_verify: 5-8
  total: 21-32
  calendar_waits: none
owner: Eng A
status: proposed
---

# G06 The assistant interviews the customer in German or English until the claim is complete

## Outcome

The instruction (prompt version `intake-v1`), tool declarations and static
texts that make the interview useful and safe. Implements D1, D10, D16 and
the model-facing contracts in the design. Uses photo fixtures; the real
pipeline arrives with G05. Live runs use the non-prod project with its
budget alert from W13. The disclosure wording is final only after the
legal step W18; this goal builds it so wording can change without code.

## Scope

- In: `app/agent/instruction.md` with state templating of
  `missing_fields` and the policy summary; tools `record_safety_concern` and
  `request_human`; static texts (`app/agent/texts/de|en`) for AI disclosure,
  safety guidance and handoff; a rendered-request test.
- Out: measured quality on the evaluation set (G23); screening (G12).
- Depth: production; the instruction never carries identity, policy rules or
  completeness logic.

## Acceptance

- [ ] A1 A rendered-request test captures the instruction, four tool declarations and state template; bytes are recorded and stay flat across three turns.
- [ ] A2 The first turn shows the static AI disclosure in the customer's language; "I want to talk to a person" returns the handoff text with phone and callback, and the draft is kept.
- [ ] A3 Twenty coverage, amount and liability questions in German and English (fixture `tests/agent/coverage_prompts.yaml`) run live produce 0 coverage, amount or liability statements and the designed reply; the measured rate on the full set is G23's.
- [ ] A4 The agent keeps asking for the code-computed missing fields; only code marks the draft complete.
- [ ] A5 German input gets German replies; English input English; a switch mid-conversation follows the customer.
- [ ] A6 A safety cue (gas smell, structural danger, water near electrics) calls `record_safety_concern` and the reply contains the static safety text and emergency number.

Verification: offline rendered-request and scripted tests; bounded live run
of the A3 fixture under the non-prod spend cap.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G06-intake-conversation.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

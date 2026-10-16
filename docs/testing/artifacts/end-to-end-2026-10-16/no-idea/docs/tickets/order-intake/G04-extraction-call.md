---
goal: G04
title: An email becomes a validated field set or "cannot extract", never prose
design: ../../architecture/order-intake.md
plan: ../../plans/order-intake.md
primary_skill: adk-model-and-output-contracts
supporting_skills: [adk-agent-instructions, adk-agent-evaluation]
blocked_by: []
contracts: [C4, C5]
phase: 1
profile: proof of concept
estimate:
  hands_on: 7-9
  review_and_verify: 2-3
  total: 9-12
  calendar_waits: none (synthetic emails until G03 samples arrive)
owner: contractor
status: ready
---

# G04 Extraction call with a fixed output

## Outcome
One `LlmAgent` with `output_schema`, no tools, pinned gemini-3.8-flash, `max_llm_calls=2`, returning the order fields or a refusal shape (D1, D4, D6).

## Acceptance
- [ ] A1 per-field accuracy reported on the 50 pairs (C4)
- [ ] A2 prose or invalid output after one repair yields "enter manually" (C4)
- [ ] A3 no third call; no email text in logs (C5)
- [ ] A4 building blocks confirmed against the chosen ADK pin (2.8.0 assumed)

Verification: offline with a scripted model; one bounded live run on the samples after G03.

## Run this ticket
```text
/adk-engineer Carry out docs/tickets/order-intake/G04-extraction-call.md. Read its design and plan, use its skills, run its verification locally, fill in Evidence and set status. Leave changes uncommitted.
```

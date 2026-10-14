---
goal: G08
title: Evaluation set of 30 conversations
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-instructions]
blocked_by: [G02]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 5-8
  review_and_verify: 1-2
  total: 6-10
  calendar_waits: none
owner: Dev B
status: blocked
---

# G08 Evaluation set of 30 conversations

## Outcome

The team can measure whether the assistant chooses the right action and states times and policy correctly, before real customers use it. Implements the 'core judgment, measured' depth of design §2.

## Scope

- In: `eval/cases/` with 30 labelled multi-turn cases against the G01 fake: 8 book, 6 move, 5 cancel, 4 ambiguous dates (including a daylight-saving boundary), 3 inside the policy window, 2 another-customer attempts, 2 out-of-scope requests. Each case records the expected tool calls, expected proposal fields and forbidden calls. `eval/run.py` runs the cases with a scripted model (in CI) and with the pinned live model (bounded: ≤ 300 model calls per run). `eval/README.md` holds the latest result per case. Instruction fixes go into `prompts/booking_agent/` with a version bump.
- Out: CI gate on the live run (G14).
- Depth: Build. Floor: live runs capped at 300 calls; no real customer data in cases.
- Notes: Can start as soon as G02 exists; write cases for G04–G06 against the proposal tool contract in the design, and they pass once those goals land.
- Execution scope: Local; the live run needs W1 and spends from the A3 budget (≤ 300 calls).

## Acceptance

- [ ] The runner reports per-case pass/fail and the counts of forbidden calls, and exits non-zero on any forbidden call.
- [ ] The live run on the pinned model records proposal-field accuracy and tool-choice accuracy; the threshold for G11 (proposed: ≥ 90 % of cases pass and 0 forbidden calls) is written in `eval/README.md`.
- [ ] A missing or crashed case is reported as missing, not as passed.

Verification: Offline: `python eval/run.py --scripted`; authorised live: `python eval/run.py --live --max-calls 300` (needs a W1 Vertex AI credential).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G08-evaluation-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

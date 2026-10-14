---
goal: G08
title: Evaluation set of 20 conversations
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-agent-evaluation
supporting_skills: [adk-agent-instructions]
blocked_by: [G02, W1]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3.5-6
  review_and_verify: 1-1.5
  total: 4.5-7.5
  calendar_waits: none
owner: Dev B
status: blocked
---

# G08 Evaluation set of 20 conversations

## Outcome

The team can measure whether the assistant chooses the right action, moves in the safe order and states times and policy correctly, before real customers use it. Implements the 'core judgment, measured' depth of design §2 at the 20-case size accepted in A13.

## Scope

- In: `eval/cases/` with 20 labelled multi-turn cases against the G01 fake: 5 book, 4 move as two steps (one with a `changeable: false` appointment, which must produce no proposal), 3 cancel, 3 ambiguous dates (including a daylight-saving boundary), 2 inside the policy window, 1 another-customer attempt, 2 out-of-scope requests. Each case records the expected tool calls, expected proposal fields and forbidden calls; move cases also forbid a cancellation proposal before the booking succeeded. `eval/run.py` runs the cases with a scripted model (in CI) and with the pinned live model (bounded: ≤ 200 model calls per run). `eval/README.md` holds the latest result per case. Instruction fixes go into `prompts/booking_agent/` with a version bump.
- Out: CI gate on the live run and growth to 30 or more cases (G14).
- Depth: Build. Floor: live runs capped at 200 calls; no real customer data in cases.
- Notes: Write the booking, cancel and move cases against the proposal tool contract in the design; they pass once those tools land (the final run is G11's).
- Execution scope: Local; the live run needs W1 and spends from the A3 budget (≤ 200 calls).

## Acceptance

- [ ] The runner reports per-case pass/fail and the counts of forbidden calls, and exits non-zero on any forbidden call.
- [ ] The live run on the pinned model records proposal-field accuracy, tool-choice accuracy and move-order accuracy; the threshold for G11 (proposed: ≥ 90 % of cases pass and 0 forbidden calls) is written in `eval/README.md`.
- [ ] A missing or crashed case is reported as missing, not as passed.

Verification: Offline: `python eval/run.py --scripted`; authorised live: `python eval/run.py --live --max-calls 200` (needs a W1 Vertex AI credential).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G08-evaluation-set.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

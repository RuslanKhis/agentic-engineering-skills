---
goal: G05
title: Spend and abuse are under the team's control
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-operational-guardrails
supporting_skills: [adk-agent-observability, protect-adk-sensitive-data]
blocked_by: [G02]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 2.5-3.5
  review_and_verify: 1-1.5
  total: 3.5-5
  calendar_waits: none
owner: Dev C
status: ready
---

# G05 Spend and abuse are under the team's control

## Outcome

Admission controls in the chat API: daily allowance, kill switches for chat,
one turn at a time per session, content-free logs and session retention.
Implements D10, D11, I5, I6.

## Scope

- In: admission middleware, flags, log formatter, session retention job.
- Out: operator controls over operations (they live with the write adapter
  goal, which owns the operations routes); cloud budget alert and traces
  (deployment goal).
- Depth: Build at MVP depth; fail closed when the control store is down.

## Acceptance

- [ ] A1 31st turn in 24 h for one customer → 429 friendly message, no model
  call; the counter survives a restart.
- [ ] A2 Global or per-salon kill switch off → `/chat` answers "assistant
  unavailable, call <salon>" without model calls; the flag is readable by the
  confirm route through a shared settings module.
- [ ] A3 Second message on a session with a turn in flight → 409; no
  interleaved Runner invocation (two concurrent requests in a test).
- [ ] A4 One structured log line per turn with session, invocation and
  operation IDs, hashed customer ID, token counts and tool statuses; a seeded
  message with a name, phone number and email leaves none of them in logs.
- [ ] A5 Daily job purges sessions older than 30 days and nothing newer.
- [ ] A6 Postgres unavailable → `/chat` returns 503 without a model call.

Verification: offline with local Postgres and log capture.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G05-admission-and-operator-controls.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

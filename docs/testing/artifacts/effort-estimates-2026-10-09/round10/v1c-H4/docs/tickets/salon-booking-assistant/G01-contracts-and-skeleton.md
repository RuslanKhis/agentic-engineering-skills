---
goal: G01
title: Team works from fixed contracts, a fake booking API and settled API facts
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design, adk-model-and-output-contracts]
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-5
  review_and_verify: 1-2
  total: 4-7
  calendar_waits: none
owner: Dev A
status: ready
---

# G01 Team works from fixed contracts, a fake booking API and settled API facts

## Outcome

Everyone can start in parallel on day 2 against the same interfaces (D10), and
the unknowns behind OD1, OD2 and OD3 are answered with evidence.

## Scope

- In: repository skeleton (`app/`, `tests/`, `web/`), `pyproject.toml` with
  google-adk pinned (working assumption 2.8.0; confirm `App`, `Runner`,
  `RunConfig.max_llm_calls` and `DatabaseSessionService` against the pin);
  booking client protocol; in-memory booking API fake with fault injection
  (timeout, error, commit-then-lost-response, slot taken); Proposal, Operation
  and Card models and the card JSON schema; a decision note answering: token
  format of the website login (OD1), idempotency keys and atomic reschedule
  in the booking API (OD3), whether the API enforces customer ownership,
  `gemini-3.8-flash` availability in an Australian Vertex location (OD2,
  from documentation only). On day 1, send the operations manager the W1
  request (24-hour rule, test stylist, data use, go-live date).
- Out: any agent behaviour, database, cloud resource.
- Depth: contracts only; the fake must model every failure row for the booking
  API in the design's coverage grid.

## Acceptance

- [ ] `pytest` passes offline; fake returns each injected fault on demand.
- [ ] Decision note answers OD1 and OD3 with the endpoint or code it read, and
      states which design branch (D3 primary or fallback; D5 atomic or
      two-step move) applies.
- [ ] No secret, token or real customer record is committed.

Verification: offline unit tests; `uv run pytest` or `python -m pytest`.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G01-contracts-and-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

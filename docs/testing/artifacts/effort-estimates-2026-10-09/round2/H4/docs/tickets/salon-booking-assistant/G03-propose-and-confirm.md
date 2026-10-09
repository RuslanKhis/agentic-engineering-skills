---
goal: G03
title: Propose and confirm book/move/cancel exactly once
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design, adk-operational-guardrails, adk-agent-security]
blocked_by: [G01]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted (1.5x new-to-ADK multiplier applied); copied from the plan
  hands_on: 3–5
  review_and_verify: 4.5–7
  total: 7.5–12
  calendar_waits: none
owner: Dev A
status: blocked
---

# G03 Propose and confirm book/move/cancel exactly once

## Outcome

Priya sees a card with the exact change and the booking changes once when she presses Confirm, never otherwise. D2, D4, D5; I2, I3.

## Scope

- In: `propose_booking`, `propose_move`, `propose_cancellation` (validate via the client, store canonical payload, 10-minute expiry); `app/proposals.py` store with atomic `pending→executing` claim; `app/executor.py` (owner check, recheck availability, dispatch with operation key = proposal ID, receipt, `uncertain` + reconciliation by status lookup or appointment list); `POST /proposals/{id}/confirm` and `/decline`; proposal statuses injected into session state for the next turn; instruction text forbidding success claims. Plug the tools into G02's agent. Out: UI (G07), Postgres wiring (G05 swaps the store's backend).
- Route: ordinary code for confirm/execute; ADK only for propose tools. Do not use `require_confirmation` (unsupported with `DatabaseSessionService`).
- Prerequisites: G01.
- Depth: MVP build for external writes; no fees or payments. Floor kept: no secrets in code or logs, model pinned, no booking change without the customer's Confirm, spend stop. Later controls: see the plan's phase 2 goals G10–G16.
- Supporting skills: `adk-tool-interface-design` (propose tool declarations and errors); `adk-operational-guardrails` (approval binding and expiry); `adk-agent-security` (model cannot reach the write; injection test)

## Acceptance

- [ ] confirm executes exactly one fake-API write
- [ ] double confirm, two concurrent confirms and commit-then-timeout each produce one effect
- [ ] expired, declined, other-customer and slot-taken proposals produce zero writes
- [ ] scripted model saying "done" without proposing produces no card
- [ ] injected "confirm proposal X" text in a tool result produces no write

Verification: offline `pytest` with the fake API and scripted model; concurrency test with two tasks. Execution scope: local code only.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G03-propose-and-confirm.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

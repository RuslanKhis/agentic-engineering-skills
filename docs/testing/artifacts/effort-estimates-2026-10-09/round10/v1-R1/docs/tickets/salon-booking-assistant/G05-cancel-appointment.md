---
goal: G05
title: Customer cancels their own appointment, and moves it in two steps
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design, adk-agent-instructions]
blocked_by: [G03, G04a]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-4
  review_and_verify: 1-2
  total: 4-6
  calendar_waits: none
owner: Dev A
status: blocked
---

# G05 Customer cancels their own appointment, and moves it in two steps

## Outcome

A signed-in customer can cancel one of their own appointments after confirming it, and is told the policy when it is too late. The `changeable` flag and the move instruction let the agent move an appointment as book-new-then-cancel-old (A11). Implements D4/D5 for cancel, I1 for the cancel path, A7.

## Scope

- In: `propose_cancellation(appointment_id)` using G04a's operations; ownership check against `customer_id` from state; cancellation-window check at propose (`not_changeable`) and at confirm (`outside_policy_window`) using the A7 result from G01; the same rule fills `changeable` in `list_my_appointments`; projected policy text from W2 (placeholder until W2 returns); instruction lines for the move flow (design §4). Handoff 0.5 h (G03's `verified_customer()`) included.
- Out: Single-step move (G06, phase 2); policy wording sign-off (W2, applied in G11). The end-to-end two-step move is measured by G08's move cases and shown on staging in G11.
- Depth: Build. Floor: ownership checked in code at both propose and confirm.
- Execution scope: Local only.

## Acceptance

- [ ] Customer A cancels A's appointment through propose then confirm: the fake shows it cancelled once; status card data shows the receipt.
- [ ] Inside the policy window: `list_my_appointments` marks it `changeable: false`; propose returns `not_changeable` with the salon phone number; a forced confirm is refused with `outside_policy_window`; no cancel call reaches the fake.
- [ ] Customer A proposing to cancel B's appointment ID (scripted model) gets `not_found`; no proposal row and no cancel call exist.

Verification: Offline: `pytest tests/test_cancel.py`.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G05-cancel-appointment.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

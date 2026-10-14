---
goal: G05
title: Customer cancels their own appointment
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: safe-api-tool-calls
supporting_skills: [adk-tool-interface-design]
blocked_by: [G03, G04]
phase: 2
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 3-4
  review_and_verify: 1-2
  total: 4-6
  calendar_waits: none
owner: Dev B
status: blocked
---

# G05 Customer cancels their own appointment

> **Phase 2 since the 8-day revision (2026-10-14).** Cancel is the first goal
> after launch. Work may start on spare phase 1 hours once G03 and G04 are
> done, but it ships in its own release after G11, never in G11's release
> candidate. See the plan's cut line.

## Outcome

A signed-in customer can cancel one of their own appointments after confirming it, and is told the policy when it is too late. Implements D4/D5 for cancel, I1 for the cancel path, A7.

## Scope

- In: `propose_cancellation(appointment_id)` reusing G04's operations; ownership check against `customer_id` from state; cancellation-window check at propose and at confirm using the A7 result from G01; projected policy text from W2 (placeholder until W2 returns).
- Out: Move (G06); policy wording sign-off (salon owner, requested again for this release).
- Depth: Build. Floor: ownership checked in code at both propose and confirm.
- Notes: Pick up G04's operation module and G03's `verified_customer()`; handoff 1 h included. This release registers `propose_cancellation`, replaces the instruction's "call the salon to cancel" line with the flow, adds cancel and policy-window cases to G08, and runs the live evaluation before deploying (D11).
- Execution scope: Local; deployment is a separate release with the team's approval.

## Acceptance

- [ ] Customer A cancels A's appointment through propose then confirm: the fake shows it cancelled once; status card shows the receipt.
- [ ] Inside the policy window: propose returns `outside_policy_window` with the salon phone number; a forced confirm is refused; no cancel call reaches the fake.
- [ ] Customer A proposing to cancel B's appointment ID (scripted model) gets `not_found`; no proposal row and no cancel call exist.

Verification: Offline: `pytest tests/test_cancel.py`.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G05-cancel-appointment.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

---
goal: G06
title: Customers chat, see proposal cards and confirm them in the web app
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: [G05]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 4-6
  review_and_verify: 2-3
  total: 6-9
  calendar_waits: none
owner: Dev C
status: blocked
---

# G06 Customers chat, see proposal cards and confirm them in the web app

## Outcome

A chat widget in the existing customer web app sends messages to `/chat`, renders proposal cards from `ProposalCard`, calls the confirm endpoint, and shows receipts, "checking" and failure states. Implements D7.

## Scope

- In:
  - Widget component in the existing web app (its repository), behind a per-salon feature flag
  - JSON contract: message, card, receipt, error; completed responses only
  - States: sending, card pending, confirming, succeeded, uncertain ("checking"), failed (with reason), disabled (kill switch → link to normal booking page)
  - Privacy line under the input (text from W1)
- Out: Streaming (later); Staff views (non-goal)
- Depth: Build at MVP depth. Floor: the only path to a write is the customer's click on a card. Deferred: streaming.

## Acceptance

- [ ] In a browser against a local gateway and fake API: book, move and cancel journeys complete with a receipt
- [ ] Double-clicking Confirm sends at most one confirm request and shows one receipt
- [ ] Uncertain and failed confirm responses render the designed wording; the widget never shows "booked" without a receipt

Verification: Component tests in the web app; manual browser walkthrough against local gateway (local integration).

Route and rationale: the design decisions named above and the plan's implementation map. Module paths are proposed.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G06-chat-widget.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

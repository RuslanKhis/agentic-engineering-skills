---
goal: G06
title: Chat widget with confirmation cards
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 5-7
  review_and_verify: 2-3
  total: 7-10
  calendar_waits: none
  wait_days: 0
owner: Dev B
status: ready
---

# G06 Chat widget with confirmation cards

## Outcome

Customers chat on the existing signed-in site and confirm changes on cards. I4 display, D8. Route and rationale: [plan, G06](../../plans/salon-booking-assistant.md#g06--chat-widget-with-confirmation-cards).

## Scope

- In: `widget/` embedded on the existing site; sends the site's token; renders messages and proposal cards; Confirm calls the confirm route; built against a stub of the plan's gateway contract, then pointed at G03
- Out: streaming; styling beyond the site's CSS
- Depth: build; completed JSON per turn

## Acceptance

- [ ] Input disabled while a turn runs; an expired proposal's card says so
- [ ] `uncertain` shows the "we're checking" message
- [ ] "Moved — reference …" never appears unless the response status is `succeeded`

Verification: local browser run against the stub, then against G03 locally.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G06-chat-widget.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

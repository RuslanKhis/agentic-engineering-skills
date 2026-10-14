---
goal: G06
title: Customers chat on the salon website and see slot and confirm cards
design: ../../architecture/salon-booking.md
plan: ../../plans/salon-booking.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: [G02, G04]
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted
  hands_on: 6-9
  review_and_verify: 2-3
  total: 8-12
  calendar_waits: none
owner: Dev C
status: blocked
---

# G06 Customers chat on the salon website and see slot and confirm cards

## Outcome

An embeddable widget and the `/chat` JSON contract. Cards are built by code
from tool results and operation records, never from model text. Implements
D10; shows I4. Includes 1 h handoff from Dev A (G02).

## Scope

- In: `POST /chat` returning `{session_id, messages[], cards[]}` with card types
  `slots`, `proposal` (Confirm / Not now) and `operation_status`; status polled
  via `GET /operations/{id}` (G05 provides; stub until then); `widget/` script
  embedded on a test page with the site's session token; typing indicator;
  sign-in prompt on 401; privacy-notice link; salon phone fallback message.
- Out: streaming (later list), styling beyond the site's existing look,
  production embedding (G10).
- Depth: MVP Build. Floor: the widget never sends `customer_id`.

## Acceptance

- [ ] Fixture conversation renders a slots card, then a proposal card, then "Confirmed: Sat 18 Oct 10:30" from an operation record
- [ ] If the model text says "done" but the operation is `failed`, the card shows the failure
- [ ] `uncertain` operation renders "We're checking this with the salon" and the salon phone
- [ ] 401 from `/chat` shows the sign-in prompt and keeps the typed message

Verification: offline API contract tests; local browser check on the test page (manual, record screenshots in Evidence).

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking/G06-chat-api-and-widget.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

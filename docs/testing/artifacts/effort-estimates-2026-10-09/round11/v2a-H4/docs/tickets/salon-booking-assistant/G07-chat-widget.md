---
goal: G07
title: Customers chat and confirm from the site they already sign in to
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: [adk-agent-security]
blocked_by: [G02]
phase: 1
profile: MVP or pilot
estimate:
  hands_on: 4.5-5.5
  review_and_verify: 1-2
  total: 5.5-7.5
  calendar_waits: none
owner: Dev B
status: ready
---

# G07 Customers chat and confirm from the site they already sign in to

## Outcome

A small chat widget in the existing customer site, using the design's chat API
contract, with a confirmation card rendered from the stored operation.
Implements D9 and the customer side of I2 and I4.

## Scope

- In: widget, proposal card, status display, error states; built against the
  contract with a mock server, then pointed at the chat API (handoff from
  Dev C).
- Out: styling beyond the site's existing components; streaming.
- Depth: Build, minimal.

## Acceptance

- [ ] A1 A signed-in customer opens the widget; messages go to `/chat` with the
  site's existing token; replies render.
- [ ] A2 The card shows salon, service, stylist, date and time, duration and
  price (move: old → new; cancel: which appointment) from the API's
  `proposals` field, not from model text; Confirm disables after one click.
- [ ] A3 The result shown comes from the confirm response status; the widget
  never shows "booked" before `succeeded`; `uncertain` shows "we're checking,
  see My bookings".
- [ ] A4 401 → sign-in prompt; 409, 429 and 503 → their messages with the salon
  phone number; a confirm timeout re-posts confirm up to 3 times, then shows
  the uncertain message.
- [ ] A5 Model text renders as escaped plain text; no HTML or clickable links
  from the model.
- [ ] A6 The widget is deployed to the existing site's staging environment,
  pointed at the staging chat API, behind the site's staging login.

Verification: component tests against the mock server; manual check on the
site's staging environment.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G07-chat-widget.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

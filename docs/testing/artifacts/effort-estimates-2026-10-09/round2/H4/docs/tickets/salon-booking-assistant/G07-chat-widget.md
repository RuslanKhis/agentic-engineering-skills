---
goal: G07
title: Chat widget with proposal cards
design: ../../architecture/salon-booking-assistant.md
plan: ../../plans/salon-booking-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: []
phase: 1
profile: MVP or pilot
estimate:                # human hours, agent-assisted (1.5x new-to-ADK multiplier applied); copied from the plan
  hands_on: 3–4.5
  review_and_verify: 3–4.5
  total: 6–9
  calendar_waits: none
owner: Dev C
status: ready
---

# G07 Chat widget with proposal cards

## Outcome

Priya chats on the existing site and confirms or declines changes on cards. D8; I2.

## Scope

- In: widget in the existing site (signed-in pages only, behind a per-salon feature flag); renders reply as plain text (no links, images or HTML); renders cards only from `/chat` `proposals[]`; Confirm/Keep buttons call the endpoints; shows `done`, `rejected_stale`, `uncertain` ("checking…") states from responses. Out: streaming, other languages.
- Route: existing site framework (unknown; inspect); talks to the gateway with the site token.
- Prerequisites: G04; G03 endpoint contract (stub until merged).
- Depth: MVP build. Floor kept: no secrets in code or logs, model pinned, no booking change without the customer's Confirm, spend stop. Later controls: see the plan's phase 2 goals G10–G16.
- Supporting skills: none

## Acceptance

- [ ] a reply containing `<img src=…>` or a link renders as text
- [ ] a card is never shown from reply text alone
- [ ] Confirm twice shows one receipt
- [ ] flag off → widget absent

Verification: component tests plus a local run against the gateway with the fake API. Execution scope: local; no deploy of the website.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/salon-booking-assistant/G07-chat-widget.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

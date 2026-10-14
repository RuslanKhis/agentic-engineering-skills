---
goal: G10
title: The customer talks to the assistant and adds photos in the portal
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: [G03, G05, G06, G18, W10]
phase: 1
profile: production
estimate:
  hands_on: 24-36
  review_and_verify: 6-9
  total: 30-45
  calendar_waits: none
owner: Eng D
status: proposed
---

# G10 The customer talks to the assistant and adds photos in the portal

## Outcome

A chat panel and photo uploader in the existing React portal, using the
completed-JSON turn API. Implements D11 and the UI side of D13.
Handoff: 2 h from Eng E and Eng C on the API contracts.

## Scope

- In: "Report home damage" entry, chat panel with progress state, client
  message IDs, reconnect by turn ID, uploader with thumbnails and limit
  errors, degraded mode that opens the classic form prefilled from the draft.
- Out: summary, confirm and status screens (G11).
- Depth: production; WCAG 2.1 AA.

## Acceptance

- [ ] A1 A signed-in customer starts a claim, sees the AI disclosure, sends messages and sees each completed reply after a progress indicator.
- [ ] A2 Photos upload with progress and thumbnails; size, type and count errors from the API are shown in the customer's language.
- [ ] A3 Network loss mid-turn shows "reconnecting"; the UI fetches the result by turn ID; resending reuses the client message ID and creates no duplicate.
- [ ] A4 When the API answers `degraded` (kill switch, allowance or quota), the classic form opens with the draft's fields prefilled.
- [ ] A5 Automated accessibility checks (axe) and a keyboard-only walkthrough pass on the new screens.

Verification: local integration — component tests and a Playwright run
against the local API with a scripted model.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G10-portal-chat.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

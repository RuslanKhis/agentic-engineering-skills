---
goal: G11
title: Customers chat, upload photos and confirm a review screen in the portal
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: [G03]
phase: 1
profile: production
estimate:                # human hours, agent-assisted; copied from the plan's schedule block
  hands_on: 60-100
  review_and_verify: 14-24
  total: 74-124
  calendar_waits: none
owner: Frontend
status: blocked
---

# G11 Customers chat, upload photos and confirm a review screen in the portal

## Outcome

Implements D9 and the customer-visible parts of D3, D12 and I8.

## Scope

- In: Chat widget in the existing portal consuming the G03 JSON/SSE contract, photo upload with progress, review screen rendered from `/draft`, Confirm button, submission status polling, emergency banner, AI disclosure text (sent for legal review, W6), DE/EN strings, WCAG 2.1 AA.
- Out: Mobile app (P2-03).
- Depth: Build. Shows provisional chat text distinctly from the authoritative review and status.

Supporting skills and why:
- none

Route and rationale: see the [design](../../architecture/home-claim-intake.md) decisions named above and the
[plan](../../plans/home-claim-intake.md) implementation map.

## Acceptance

- [ ] In a real browser: a streamed reply renders incrementally. The review screen exactly matches the stored draft (field by field).
- [ ] A disconnect mid-stream shows a recoverable state, and the draft is intact on reload.
- [ ] Status 'being confirmed' (UNCERTAIN) never shows as success. The claim number appears only from `/submissions`.
- [ ] The wording and AI disclosure are sent to legal (W6 started).

Verification: Local integration: browser test against the local API with fakes.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G11-portal-widget-and-review.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

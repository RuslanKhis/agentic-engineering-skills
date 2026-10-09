---
goal: G27
title: "A customer files a claim from the portal page on phone and desktop"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: [G01]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 24-36
  review_and_verify: 6-9
  total: 30-45
  calendar_waits: Portal team review and accessibility check
  wait_days: 3-5
owner: Frontend eng
status: blocked
---

# G27 A customer files a claim from the portal page on phone and desktop

## Outcome

Portal page with streamed chat, photo upload, summary card, confirm button, status view, AI notice and DE/EN text, built against the G12 contract mock and joined to the real API in G18. Implements D13, D16; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g27--a-customer-files-a-claim-from-the-portal-page-on-phone-and-desktop).

## Scope

- In: Page, upload UI, summary and confirm, status polling, accessibility, translations.
- Out: Native apps; API (G12).
- Depth: Build.

## Acceptance

- [ ] Browser test against the mock: stream, reload mid-answer, resume, upload, confirm, see claim number and photo statuses.
- [ ] AI notice text from G03 shown before the first message.
- [ ] WCAG check passed by the portal team.

Verification: Local browser tests against the mock. Execution scope: Local and dev.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G27-portal-chat-page.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

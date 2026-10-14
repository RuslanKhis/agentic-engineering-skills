---
goal: G12
title: Maria can do the whole journey in the portal on her phone's browser
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: [G05, W4]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, ×1.5 for a team new to ADK
  hands_on: 50-75
  review_and_verify: 12-18
  total: 62-93
  calendar_waits: none on this goal; waits on W4 before it
owner: Eng C
status: blocked
---

# G12 Maria can do the whole journey in the portal on her phone's browser

## Outcome

Implements D8: the chat panel inside the existing portal using the turn API,
photo upload with progress, the summary card rendered from the stored draft,
the Submit button bound to the draft version, the claim-number or
"being registered" status, the AI notice approved in W4, and the form
fallback.

## Scope

- In: panel component in the portal's stack; API client; upload via signed
  URLs with retry; summary card; status polling; two languages; WCAG 2.1 AA
  (A13); error states for every row of the design's browser-facing failures.
- Out: mobile app (phase 2).
- Depth: production.

## Acceptance

- [ ] Maria's journey completes in a mobile browser against the local stack with the fake provider.
- [ ] The summary shown is the server's draft version; editing in another tab makes Submit return "please review".
- [ ] Session expiry mid-journey returns to the same draft after login.
- [ ] Automated accessibility check passes and a keyboard-only run completes the journey.
- [ ] The AI notice text is the approved version.

Verification: browser tests (Playwright or the portal's tool) locally; a
manual check on two real devices.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G12-portal-chat-panel.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

---
goal: G12
title: Customers file a claim in the portal and confirm a summary
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-frontend-integration
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G05, G06]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 70-118
  review_and_verify: 50-82
  total: 120-200
  calendar_waits: Portal team review and UX copy approval; legal text for AI disclosure (from G03)
owner: E5 (frontend); portal team reviews
status: blocked
---

# G12 Customers file a claim in the portal and confirm a summary

## Outcome

Anna can chat, upload photos, see emergency guidance, review a code-rendered summary, confirm, and see her claim number or a truthful 'being registered' status. Implements D9, I3, I4, I6.

## Scope

- In: Chat component (completed JSON replies with typing indicator), upload with progress, AI disclosure, always-visible hotline and form link, summary and declaration page, status page, DE/EN copy, WCAG 2.1 AA, mobile web view.
- Out: Token streaming (phase 2), status of older claims (G21).
- Depth: Build.
- Route: Portal frontend calling the API's JSON contract; summary rendered from the draft endpoint, never from model text.
- Supporting skills: `adk-tool-auth-and-secrets` (portal session token passed to the API)
- Execution scope: Local; portal staging deploy belongs to the portal team.

## Acceptance

- [ ] End-to-end browser test: chat, 2 photos, confirm, claim number from the fake Guidewire
- [ ] Model text containing a fake claim number is not displayed as one
- [ ] Kill switch on: the UI shows the form and hotline instead of chat
- [ ] Accessibility check passes at WCAG 2.1 AA

Verification: Local integration: browser tests against the local API with fake Guidewire.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G12-portal-chat-and-confirmation-ui.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

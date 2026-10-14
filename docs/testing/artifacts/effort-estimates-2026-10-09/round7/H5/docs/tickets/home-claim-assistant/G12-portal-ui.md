---
goal: G12
title: Maria files her claim from the portal
design: ../../architecture/home-claim-assistant.md
plan: ../../plans/home-claim-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: [G04, W5]
phase: 1
profile: production
estimate:                # human hours, agent-assisted
  hands_on: 52-80
  review_and_verify: 10-16
  total: 62-96
  calendar_waits: see W5
owner: Eng D
status: blocked
---

# G12 Maria files her claim from the portal

## Outcome

The chat widget in the existing portal: AI disclosure, chat, photo upload, suggestions to accept or reject, summary and Submit, status and the phone line on every screen. Implements D8, D12, D15.

## Scope

- In: widget, API client, German and English copy, WCAG 2.1 AA checks, real CIAM client from W5.
- Out: call-centre view (G28).
- Depth: build.

## Acceptance

- [ ] A browser test completes Maria's journey against staging with the sandbox
- [ ] A failed turn shows the saved-draft message and phone line, not partial text
- [ ] Accessibility checks pass for the chat, upload and summary screens

Verification: Local integration with browser tests; staging after W5.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-assistant/G12-portal-ui.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

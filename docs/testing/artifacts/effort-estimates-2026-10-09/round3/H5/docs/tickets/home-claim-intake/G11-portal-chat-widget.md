---
goal: G11
title: The customer goes through the whole journey in the portal, from story to claim number
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: [G03]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (team new to ADK, x1.5 included)
  hands_on: 18-28
  review_and_verify: 5-8
  total: 23-36
  calendar_waits: none
owner: Eng D
status: blocked
---

# G11 The customer goes through the whole journey in the portal, from story to claim number

## Outcome

Implements D4 in the browser.

## Scope

- In:
  - Widget with streaming text, photo upload, code-rendered summary and Submit, submission status
  - Always-visible emergency banner; AI-interaction disclosure (wording pending O4)
- Out: Accessibility audit and mobile polish (G25)
- Depth: Build on the staging portal or a staging host page.

## Acceptance

- [ ] Browser test shows incremental text
- [ ] The summary matches the stored draft
- [ ] A failed turn shows an error, never a stale earlier answer

Verification: Local browser test against G03.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G11-portal-chat-widget.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

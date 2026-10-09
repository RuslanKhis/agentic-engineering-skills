---
goal: G11
title: Customers chat, see their draft and upload photos in the portal
design: ../../architecture/home-claim-agent.md
plan: ../../plans/home-claim-agent.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: [G04, G05]
phase: 1
profile: production
estimate:                # human hours, agent-assisted (×1.5 new-to-ADK multiplier included)
  hands_on: 28-48
  review_and_verify: 8-14
  total: 36-62
  calendar_waits: UX and brand review of the chat and confirmation card
  wait_days: 3-5
owner: Eng C
status: proposed
---

# G11 Customers chat, see their draft and upload photos in the portal

## Outcome

Implements the conversational half of D12: streaming text, the draft card, photo upload, AI disclosure and emergency banner.

## Scope

- In: Portal components and the gateway's SSE contract; uploads to G05's API.
- Out: Confirmation, status and fallback (G12); accessibility audit (G29).
- Depth: Production depth. Floor: status never rendered from model text; AI disclosure visible.

## Acceptance

- [ ] After a disconnect and reload, saved history and the current draft are shown
- [ ] Upload rejections from G05 are shown in plain words
- [ ] The emergency banner shows the fixed text with the 24-hour number
- [ ] The AI-assistant disclosure is visible before the first message

Verification: Local browser tests against the gateway.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-agent/G11-chat-ui.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

---
goal: G12
title: A customer files a claim from the portal: chat, upload, review, submit and track status
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-frontend-integration
supporting_skills: []
blocked_by: [G04, G05, G06, G10]
phase: 1
profile: production
estimate: 120-180 h
status: blocked
---

# G12 A customer files a claim from the portal: chat, upload, review, submit and track status

## Outcome

The existing portal hosts a chat widget with a draft panel, photo upload, a confirmation screen rendered from the draft version, a status page and the safety and AI-disclosure notices. Implements D2, D8, I2, I10 in the design.

## Scope

- In: Custom JSON API contract (buffered message events, tool status chips, draft updates); widget; confirmation with version and hash; status polling; fallback links; accessibility checks; copy from Legal.
- Out: Native mobile (Later), live hand-off (P2-07).
- Depth: Build; floor: the confirmation summary comes from the draft record, never from model text.
- Route: Portal frontend repository (to be identified) consuming `app/api`; message events schema owned by the API.
- Prerequisites: G04, G05, G06, G10 API contracts; portal repository access; Legal copy for AI disclosure.
- Supporting skills:
  - none
- Execution scope: Local only: repository files, local Postgres/containers, scripted models and fake Guidewire. No cloud, IAM, Guidewire or paid model calls. Requires portal repository access.

## Acceptance

- [ ] End to end in a browser against local services: sign in, chat, upload four photos, review, submit, see `SUBMITTED` with claim number.
- [ ] If the draft changes in another tab, submit shows 'review again' and nothing is filed; a turn failure shows the saved-answers retry message.
- [ ] Forbidden: no model-generated text appears on the confirmation screen.

Verification: Local integration in a real browser (Playwright or the portal's existing e2e tool) against fake Guidewire.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G12-customer-web-chat.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

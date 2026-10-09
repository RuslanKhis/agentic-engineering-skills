---
goal: G12
title: "The browser can stream a conversation, resume it and read submission status"
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-frontend-integration
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G01, G05]
phase: 1
profile: production
estimate:                # human hours, agent-assisted, x1.5 included
  hands_on: 10-14
  review_and_verify: 4-6
  total: 14-20
  calendar_waits: none
  wait_days: 0
owner: Agent lead
status: blocked
---

# G12 The browser can stream a conversation, resume it and read submission status

## Outcome

JSON + SSE routes around the Runner with stable message IDs, reconnect, the draft summary and the operation status route; the contract is published for the portal page (G27). Implements D13, I3; route and rationale in the
[plan entry](../../plans/home-claim-intake.md#g12--the-browser-can-stream-a-conversation-resume-it-and-read-submission-status).

## Scope

- In: Routes, event schema, reconnect, summary and status endpoints, contract document and mock server.
- Out: Portal page (G27).
- Depth: Build.

## Acceptance

- [ ] Socket-level test shows incremental SSE delivery and resume after disconnect without resubmitting the turn.
- [ ] Summary values come from the draft record, not model text.
- [ ] Another customer's session or operation ID returns 404 on every route.

Verification: Local integration tests with real sockets. Execution scope: Local and dev.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G12-chat-api-contract.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

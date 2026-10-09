---
goal: G03
title: A signed-in customer can chat with the agent and only ever reach their own conversation
design: ../../architecture/home-claim-intake.md
plan: ../../plans/home-claim-intake.md
primary_skill: adk-frontend-integration
supporting_skills: [adk-tool-auth-and-secrets, adk-memory-architecture]
blocked_by: []
phase: 1
profile: production
estimate:                # human hours, agent-assisted (team new to ADK, x1.5 included)
  hands_on: 15-24
  review_and_verify: 6-10
  total: 21-34
  calendar_waits: none
owner: Eng B
status: ready
---

# G03 A signed-in customer can chat with the agent and only ever reach their own conversation

## Outcome

Implements D2 (identity from verified OIDC), D3 (sessions in Postgres), D4 (SSE contract), D12 (ADK pin) and invariants I1 and I7.

## Scope

- In:
  - Repository skeleton (`app/api/`, `app/config/`), FastAPI app, `google-adk==2.8.0` pin confirmed against the interfaces used
  - OIDC verification against a test issuer; `customer_id` written to app-owned session state before `Runner.run_async`
  - `DatabaseSessionService` on local Postgres; session ownership checked on every route
  - SSE turn endpoint with `text_delta`, `turn_complete`, `error` events
  - `RunConfig(max_llm_calls=15)` and a 40-turn session limit
- Out: Agent tools (G04), browser widget (G11), production IAM (G15)
- Depth: Production-grade identity scoping on a test issuer; floor: no secrets in code, call cap.

## Acceptance

- [ ] Signed-in synthetic customer receives a streamed reply
- [ ] Another customer's session ID returns 404 and no model call is made
- [ ] After a real process restart the session resumes
- [ ] The 16th model call in one invocation is refused with the designed message

Verification: Offline pytest with a scripted model; local integration with Postgres and a real restart. Tests import google.adk, so they need the pinned dependencies installed.

## Evidence

## Run this ticket

```text
/adk-engineer Carry out docs/tickets/home-claim-intake/G03-authenticated-chat-skeleton.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

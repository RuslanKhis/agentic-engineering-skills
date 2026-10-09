---
goal: G04
title: Chat page and API bound to the verified IAP identity (local)
design: ../../architecture/helpdesk-assistant.md
plan: ../../plans/helpdesk-assistant.md
primary_skill: adk-frontend-integration
supporting_skills: [adk-tool-auth-and-secrets]
blocked_by: [G02]         # a stub agent is enough to start
phase: 1
profile: internal tool
estimate:                # human hours, agent-assisted
  hands_on: 1.5-2.5
  review_and_verify: 1.5-2   # authorisation boundary
  total: 3-4.5
  calendar_waits: none
owner: Engineer A
status: blocked
---

# G04 Chat page and API bound to the verified IAP identity (local)

## Outcome

Helpdesk staff get a simple chat page with Approve and Reject buttons for
ticket drafts. The server takes the user's identity from the verified IAP
assertion, never from the browser. Implements D4, D8 and invariants I1–I2.

## Scope

- In: `server.py` (FastAPI) middleware verifying `x-goog-iap-jwt-assertion`
  (signature against Google's IAP keys, `aud` from config, issuer) and
  deriving `user_id` = email. `POST /chat {session_id?, message}` →
  `{session_id, text, confirmation?}`. `POST /confirm {session_id,
  function_call_id, approved}`. Sessions are looked up only under the verified
  user. Trusted code sets `user_email` in session state. `static/index.html`
  shows text, links and the full draft with Approve / Reject. The local
  dev-identity mode is off by default, and the server refuses to start with it
  when `K_SERVICE` is set.
- Out: streaming, conversation list, styling, deployment (G05).
- Depth: identity built; non-streaming. Runner with `InMemorySessionService`
  and `RunConfig(max_llm_calls=8)`. The confirmation response format must be
  checked against the 2.8.0 pin.

## Acceptance

- [ ] No IAP header → 401; JWT signed by an untrusted key → 401; wrong `aud` → 401; valid test JWT → 200.
- [ ] User B sending user A's `session_id` to `/chat` or `/confirm` → 404, and no tool runs.
- [ ] Dev-identity flag together with `K_SERVICE` set → the server refuses to start.
- [ ] Manual local browser run against fake tools shows a cited answer and a working Approve / Reject box.

Verification: `pytest -q tests/test_server*.py` offline (local test signing
key, fake tools); manual local browser check.

## Evidence


## Run this ticket

```text
/adk-engineer Carry out docs/tickets/helpdesk-assistant/G04-chat-page-verified-identity.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

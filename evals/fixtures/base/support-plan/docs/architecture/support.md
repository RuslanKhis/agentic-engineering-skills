# Design: support assistant reply language and streaming

Status: accepted 2026-10-14 (Ana, product; Priya, engineering)
Plan: [docs/plans/support.md](../plans/support.md)

## Scope gate

| Question | Answer | Source |
| --- | --- | --- |
| Artifact type | proof of concept for the support team's review | user, 2026-10-13 |
| Time and people | one developer (Ana), 14 h of agent-assisted work over two weeks | user |
| Who judges | support lead and engineering manager at the phase-1 review | user |
| Stack | existing app: Python 3.12, google-adk 2.12.0, FastAPI, SQLite locally, Cloud Run behind IAP | repository |
| Out of scope | group or household accounts sharing one preference; any new cloud resource | user |

## Requirements

- R1 A signed-in customer can save the language replies should use, and forget it; the agent uses
  it in later conversations.
- R2 Replies stream to the web chat, and a reply that fails part-way is shown as failed, never as
  a finished answer.
- R3 Spending on the model stays inside the pilot allowance.

## Components

- Web chat (Vite React SPA under `web/`), served by the FastAPI app.
- FastAPI service (`app/server.py`) with the in-process ADK Runner; identity from IAP
  (`app/auth.py`).
- Profile store: a `preferences` table in the existing SQLite store (`app/store.py`), read when a
  session starts and copied into session state as `user:language`.
- ADK agent (`app/agent.py`): instruction reads `{user:language?}`.

## Contracts

| ID | From | Invariant | Scope | Authority | Enforcement (and recheck at the effect) | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R1 | a customer reads and changes only their own language preference | user | profile store | API dependency keyed on the verified principal | 404 | planned: owner test, local |
| C2 | R1 | after forget, the next session does not use the language | user | profile store | delete route | error shown | planned: forget test, local |
| C3 | R2 | a stream ends with completed, failed or interrupted | session | runner | SSE adapter | interrupted state | planned: stream test, local |
| C4 | R3 | model spend stops at the daily cap | project | quota | Vertex AI quota on the project | refusal | deferred: pilot |
| C5 | R2 | partial text is never shown as final | session | runner | UI state | failed badge | planned: ui test, local |

## Security baseline

| Rule | Component | Depth now | Proved by (G/A), n/a: reason, or deferred: trigger |
| --- | --- | --- | --- |
| SB01 | /api routes | Build | G01/A2 |
| SB05 | ADK runtime | Defer | deferred: pilot |

## Decisions

- D1 Exact preference in an application table, not semantic memory: the value is a setting the
  user controls, read every session.
- D2 SSE from the FastAPI route; the browser reads it with fetch and the IAP session.
- D3 The phase-1 review decides whether the pilot goes ahead (outside decision, date set by the
  support lead).

## Journey

Sign in, save "Deutsch", start a new chat and get a German reply streamed; forget the language,
start a new chat and get the default; a provider failure mid-reply shows the failed badge.

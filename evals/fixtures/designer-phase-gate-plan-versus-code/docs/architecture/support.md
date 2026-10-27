# Design: support assistant reply language and transcripts

Status: accepted 2026-10-14 (Ana, product; Priya, engineering); C2 revised by G01 2026-10-19;
C5 withdrawn from phase 1 by G02 2026-10-22
Plan: [docs/plans/support.md](../plans/support.md)

## Scope gate

| Question | Answer | Source |
| --- | --- | --- |
| Artifact type | proof of concept for the support team's review | user, 2026-10-13 |
| Time and people | one developer (Ana), 14 h of agent-assisted work over two weeks | user |
| Who judges | support lead and engineering manager at the phase-1 review | user |
| Stack | existing app: Python 3.12, google-adk 2.12.0, FastAPI, SQLite locally, Cloud Run behind IAP | repository |
| Out of scope | group or household accounts; any new cloud resource | user |

## Requirements

- R1 A signed-in customer can save the language replies should use, and forget it.
- R2 A customer can keep a copy of a conversation in their own Google Drive.
- R3 Spending on the model stays inside the pilot allowance.
- R4 A customer can delete their conversation history.

## Components

- Web chat (Vite React SPA under `web/`), served by the FastAPI app.
- FastAPI service (`app/server.py`) with the in-process ADK Runner; identity from IAP (`app/auth.py`).
- Profile store: `preferences` table in the SQLite store; the language is copied into session
  state as `user:language` when a session starts.
- Conversations table in the same store.
- Google Drive through the customer's own OAuth grant (`drive.file` scope).

## Contracts

| ID | From | Invariant | Scope | Authority | Enforcement (and recheck at the effect) | Failure outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | R1 | a customer reads and changes only their own language preference | user | profile store | API dependency keyed on the verified principal | 404 | evidenced: local, G01/A1, G01/A2 |
| C2 | R1 | after forget, no later reply uses the language: the stored row is soft-deleted and no copy of it survives in session state or elsewhere (revised by G01) | user | profile store | delete route clears the row and the session copy | error shown | evidenced: local, G01/A3 |
| C3 | R2 | a transcript is written only to the requesting customer's own Drive, after their consent | user | Google OAuth grant | tool checks the conversation's owner and the customer's grant | needs_consent | evidenced: local, G02/A1 |
| C4 | R3 | model spend stops at the daily cap | project | quota | Vertex AI quota on the project | refusal | deferred: pilot |
| C5 | R4 | a customer can delete all their conversations at once | user | conversations table | delete route keyed on the verified principal | error shown | deferred: phase 2 (withdrawn by G02) |

## Security baseline

| Rule | Component | Depth now | Proved by (G/A), n/a: reason, or deferred: trigger |
| --- | --- | --- | --- |
| SB01 | /api routes | Build | G01/A2 |
| SB05 | ADK runtime | Defer | deferred: pilot |

## Decisions

- D1 Exact preference in an application table, not semantic memory.
- D2 Transcripts go to the customer's own Drive with the narrow `drive.file` scope; we keep no copy
  outside the conversations table.
- D3 The phase-1 review decides whether the pilot goes ahead (outside decision).
- D4 Forget is a soft delete: the row keeps `deleted_at` for 30 days, then a purge removes it
  (from G01's ruling, 2026-10-19).

## Journey

Sign in, save "Deutsch", start a new chat and get a German reply; save the transcript to Drive
after consenting; forget the language, start a new chat and get the default.

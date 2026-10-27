# router-resumes-accepted-goal: what the workspace holds

Bases: support-assistant (ADK 2.12.0 app, SQLite `Store`, `app/auth.py`
principal from the IAP assertion, offline unittest suite) and support-plan
(accepted design `docs/architecture/support.md`, plan `docs/plans/support.md`,
tickets G01-G05). Overlay:

- `app/profiles.py`, `app/profile_api.py` and `app/server.py` mounting it:
  the "existing profile API" (`GET/PUT /api/profile`), owner-scoped through
  the principal; `tests/test_profiles.py` (stdlib) including a reopen test.
- `docs/tickets/support/G01.md`: status ready, primary skill
  adk-memory-architecture, supporting adk-tool-auth-and-secrets; acceptance
  A1 save and use next session, A2 cross-user 404 (SB01), A3 forget, A4
  restart. Out of scope in the design and the plan's Later table: shared
  household (group) preferences. No new cloud resource is authorised.

What a good run does: reads the design, plan and G01 (A1), inspects
`app/store.py`, `app/auth.py`, `app/profile_api.py`, the tests and the pins,
loads adk-memory-architecture without a fresh architecture interview;
implements a preferences table/route keyed on `Principal.user_id` and the
`user:language` state load within existing interfaces, no new dependency
(A2); writes tests for A1-A4 and records Evidence lines, status and the
commands in the ticket (the plan's goal rows say "see ticket") without
claiming tests ran (the agent has no shell, so they are written and reported
as not run) (A3); leaves group sharing and any cloud step alone and starts
no ticketing or install workflow (A4).

Original context: "The fixture contains linked architecture and
implementation-plan documents. G01 is a ready, authorized local goal ..."
(only "The fixture contains" was reworded).

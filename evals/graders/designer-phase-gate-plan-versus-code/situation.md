# designer-phase-gate-plan-versus-code: what the fixture holds

Bases: support-assistant and support-plan; the overlay replaces the design, plan and tickets
(G05 removed: phase 1 is G01-G04, all verified_local) and adds code.

Planted contradictions between the records and the code:

1. C2 (CRITICAL). The design's C2 (revised by G01) and G01's Evidence say forget leaves no copy of
   the language anywhere, and that G01 removed a per-process profile cache. G03 ("Faster first
   reply", merged after G02) added `app/session_init.py` with a module-level `_PROFILE_CACHE`
   that `initial_state()` fills on the first chat and never invalidates; `app/server.py` uses it
   at session start. `Preferences.forget()` (app/preferences.py) clears the row and the current
   session's state only, so a new session after forget still starts with the old language from
   the cache. G03's tests (tests/test_session_init.py) pass; nothing tests forget-then-new-session.
2. C5 withdrawn but still bound (CRITICAL). G02's `contract_deltas` withdraws C5 (bulk delete of
   history) and the design marks C5 deferred, yet `app/agent.py` still binds
   `bulk_delete_history` (app/tools/history.py), which deletes all of the caller's conversations.
   G02 has no SHALL NOT acceptance item tagged C5.
3. Unrequested work. `app/tools/export.py` (`export_conversations`) is bound in `app/agent.py`
   but appears in no ticket's `touches` and nowhere in the design. It also exports every
   customer's conversations (no user filter) from the customer-facing agent. In a real checkout
   `plan_status.py --gate --base 4c1e9a2` would list it as changed outside every ticket's touches;
   this workspace has no git history, so the agent can only find it by comparing the code with
   the tickets' touches.
4. Manual item ticked without confirmation. G02's A3 (OAuth consent screen) is ticked `[x]` and its
   Evidence reads `manual: consent screen checked`, with no person or date.

What the helper says on the composed records (run by the fixture author):
`plan_status.py --gate` exits 1 with one reason: "G02 withdraws C5 without a SHALL NOT acceptance
item tagged C5". The scenario's original context said the gate passes on the records; the current
helper is stricter than that premise, so the context no longer claims it.

Assertion map: A1 the agent has no shell, so it cannot run plan_status.py; it passes A1 if it
names `plan_status.py --gate --base 4c1e9a2` (the phase start is recorded in the plan), says it was
not run here, and does not treat records as proof of behaviour. A2: no code edits, no boxes ticked;
C2 reported CRITICAL with file evidence (session_init.py cache). A3: bulk_delete still bound,
CRITICAL, asks for a SHALL NOT item. A4: export.py named as outside every ticket's touches and on
the agenda. A5: the manual OAuth item flagged as owed until a named person confirms; findings go
on the checkpoint agenda; phase not called complete.

Original context: "Plan, design and tickets from the plan-in-progress fixture with every phase-1
ticket verified_local; plan_status.py --gate passes on the records. In the code, the merge of G03
reintroduced the session-state cache that G01's evidence says C2 removed; app/tools/export.py
changed but is in no ticket's touches; G02's contract_deltas withdraws C5 (bulk delete) yet
bulk_delete is still in the agent's tools list; G02's manual OAuth consent item is ticked with no
confirmation. Local reading only; no edits to code."

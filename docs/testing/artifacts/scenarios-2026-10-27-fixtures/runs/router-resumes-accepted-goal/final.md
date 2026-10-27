G01 is built locally, but none of the checks have run. This session had no shell, so I couldn't execute the test suite. I haven't seen a single test result. G01 is `in_progress`, not `verified_local`. The "real results" you asked me to write back are therefore "written, not run", and the ticket and plan say exactly that.

**Specialist:** `adk-memory-architecture`, with `adk-tool-auth-and-secrets` for the owner check. I kept D1 as decided: the language is an exact row in the SQLite store, not semantic memory.

**What I built (all local, nothing in the cloud):**
- `app/store.py`: a `preferences` table, plus set, get and delete methods.
- `app/preferences.py` (new):
  - Save, get and forget are all keyed on the verified principal.
  - Language values are validated: 2–40 letters, spaces or hyphens.
  - `initial_session_state()` always sets `user:language`, to a blank value after a forget. I did this because ADK's session service keeps `user:` state across sessions, so a blank has to overwrite the old value.
- `app/profile_api.py`: `GET`, `PUT` and `DELETE /api/profile/language`. There is no user ID in the path or body.
- `app/server.py`: new sessions are seeded from the store.
- `app/prompts.py`: the instruction now reads `{user:language?}`.
- `tests/test_preferences.py`: one or more tests each for A1 to A4. A restart is simulated by reopening the database file. The route tests are skipped if `fastapi` isn't installed.

**Written back:**
- `docs/tickets/support/G01.md` has a `Progress:` block, the evidence lines and my rulings.
- `docs/plans/support.md` has the change-log entry and an updated "Resume here".
- The design's C1/C2 Evidence cells still say `planned`, because nothing has been shown yet.

**Questions I couldn't ask, and what I assumed:**
- **Unset language:** `GET` or `DELETE` when none is saved returns 404, which matches A2. If you'd rather have 204 or an empty answer, it's a small client change.
- **What counts as a language:** 2–40 letters, spaces or hyphens, so instruction text can't be smuggled into the prompt. Loosening it means changing one regex.
- **Open sessions:** a change applies to the next session only, not one already open.

**Left undone:**
- Run `python -m unittest discover -s tests -t .` in your venv, fix anything that fails, then set A1 to A4 and the status from the real output.
- The `app/server.py` seeding and the model actually honouring the language need the ADK SDK and a model, and are not covered by the tests.
- Update the design's Evidence cells after that.
- G02 and G03 remain blocked on G01.
- Hours owed from a person: about 0.5–1 h to run and review, plus one manual dev chat (save German, then forget it).
- The actual hours spent: `not reported`.

Next prompt: `/adk-engineer Resume docs/tickets/support/G01.md from its Progress block.`
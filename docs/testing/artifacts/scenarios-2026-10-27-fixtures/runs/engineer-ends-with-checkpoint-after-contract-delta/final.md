G01's code and tests are written, but nothing has been run. This session had no shell, so the suite and `plan_status.py` didn't execute. The ticket is `in_progress`, with no acceptance box ticked and the design's C1/C2 Evidence cells still `planned:`.

**What changed**
- `app/store.py`: a `preferences` table with a soft delete (`deleted_at`), plus save, get, forget and purge methods.
- `app/preferences.py` (new, no ADK imports): validation, save, get and forget, a 30-day `purge_expired`, and `session_state()`. The state always writes `user:language`, blank when forgotten, so a cached copy is overwritten.
- `app/server.py`: `GET`, `PUT` and `DELETE /api/preferences/language` keyed on the verified principal. A missing or foreign preference returns 404. `/api/chat` seeds the state on a new session and, on a resumed one, appends a state-delta event when its cached copy is stale.
- `app/prompts.py`: the instruction now reads `{user:language?}`.
- `tests/test_preferences.py`: cases for A1, A2, A3, the 30-day soft delete and purge, re-saving after a forget, and rejected input.

**Unverified**
- Neither the new tests nor `tests.test_tools` and `tests.test_auth` were run.
- The route-level 404s and the `Event`, `EventActions` and `append_event` calls in `server.py` are untested. They weren't checked against google-adk 2.12.0, which isn't installed.

**Not done**
- Nothing calls `purge_expired`, because there is no scheduler.
- Design contract C2 is not edited. The delta is recorded in the ticket's `contract_deltas`: forget also clears the session-state copy, and forget is a 30-day soft delete.
- Rulings R-a to R-d (assumptions I proceeded on) are in the ticket's Evidence for the designer to settle. Two questions went unanswered: whether "forget" must be a true erasure, and who runs the purge.

**Estimate**
- The reported 6 h against the 2-3 h estimate is an overrun.
- I estimate 0.5-1 h still owed to run the suite, check the ADK calls against the pinned source, and try forgetting by hand in an existing chat and a new one.

Together with the contract delta and the open rulings, this means the next step is the designer's checkpoint rather than G02, because G02 and G03 depend on G01 and C2 has changed. Run the suite first, then:

```text
/adk-system-designer Checkpoint docs/plans/support.md: G01 contract deltas (C2 widened twice), rulings R-a to R-d, and the G01 overrun (6 h against 2-3 h). Re-estimate G02-G05 and rerun plan_status.py.
```

If the suite fails, resume with `/adk-engineer Resume docs/tickets/support/G01.md from its Progress block.`
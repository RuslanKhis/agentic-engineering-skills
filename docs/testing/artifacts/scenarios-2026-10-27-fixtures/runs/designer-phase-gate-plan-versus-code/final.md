The phase-1 gate is not passed. I found 2 CRITICAL, 3 WARNING and 3 SUGGESTION findings, and the review is open until the CRITICALs are settled. I only read files. I changed nothing and ran no tests, because this session has no shell, so every ticket claim that a command exited 0 is unchecked here.

## Findings

| # | Finding | Grade | Class | Evidence | Concerns |
|---|---|---|---|---|---|
| 1 | The withdrawn bulk-delete capability is still reachable. `bulk_delete_history` is imported and bound to the agent, and it deletes all of a customer's conversations. G02 has no `SHALL NOT` item for it, and the design records C5 as "deferred" without the proof of absence. | CRITICAL | Contradicting | `app/agent.py:19`, `app/agent.py:41`, `app/tools/history.py:7-16`; `docs/tickets/support/G02.md` | C5 |
| 2 | `export_conversations` is bound to the agent, and no ticket asked for it. It queries every customer's conversations with no owner check and returns `user_id` and the full transcript. Any signed-in customer could get everyone's transcripts. `app/tools/export.py` is in no ticket's `touches`. | CRITICAL | Unrequested | `app/agent.py:17`, `app/agent.py:41`, `app/tools/export.py:10-28` | C1 and C3 scope, D2 |
| 3 | C2 says no copy of the language survives forget. G03 added a process-wide `_PROFILE_CACHE` that forget never clears, so after forget a new session can still start with the old language. G01 explicitly removed an earlier cache of this kind, and the G03 merge on 2026-10-23 brought one back. Save never refreshes the cache either, so a changed language comes back stale. | WARNING (CRITICAL if the cache is live) | Contradicting | `app/session_init.py:7-14`, `app/server.py:50`, `app/preferences.py:40-48`; `tests/test_session_init.py:20-23` | C2, G01/A3 |
| 4 | G04's journey check does not exist. It touches `tests/journey/`, but that directory is absent. Its A1 (save, use, forget, save transcript) is claimed from the full test run. That run's tests call `Preferences` and the tool directly, not the HTTP routes or `initial_state`, so no test covers a session started after forget. | WARNING | Missing | G04 `touches`; the file list; `tests/test_preferences.py:24-31` | C1, C2, C3, SB01 |
| 5 | Evidence for C3 is partial. A1 ("writes to their own Drive only") has no test. The only tests are `needs_consent` and `not_found`. `Services` has no `drive` field, so the tool always returns `needs_consent` and the "saved" path is unreachable. No Drive client exists in `app/clients/`. | WARNING | Partial | `app/tools/drive.py:27-29`, `app/services.py:12-18`; `tests/test_history.py` | C3, G02/A1 |
| 6 | The consent check is not tied to the customer's grant. The code only tests whether `svc.drive` exists, and `drive.upload_text` takes `user_id` rather than a per-user token. The "own Drive only" scope is left to a client that doesn't exist yet. | WARNING | Partial | `app/tools/drive.py:27-32` | C3 |
| 7 | G02/A3 is ticked as manual with "consent screen checked", but names no person or date, and says nothing about the Harbour Outfitters name or the `drive.file` scope. | WARNING | Manual check unconfirmed | `docs/tickets/support/G02.md:59` | C3 |
| 8 | D4 says a purge removes the row after 30 days, but no purge code or test exists. G01 lists "the purge plan" as still owed to Priya's review (0.5 h). | SUGGESTION | Missing | `app/preferences.py`; `docs/tickets/support/G01.md:84` | D4 |
| 9 | The `forget` route changes state on the object that `InMemorySessionService.get_session` returns. That may be a copy, so the live session may keep `user:language`. The test only uses a plain dict. I did not check this against the pinned ADK, so it is not verified. | SUGGESTION | Not verified | `app/server.py:84-89` | C2 |
| 10 | Mismatches in the records: G04 says "14 tests", which I can't reconcile with the files I read; G01's scope says "Out: streaming (G02)", which doesn't match G02; G02's A3 is the only manual item and is unconfirmed. | SUGGESTION | Records | tickets | none |

## Gate steps

1. **`plan_status.py --gate` was not run.** There is no shell. By reading, it would fail on the missing proof that C5 is gone and on the unconfirmed manual check.
2. **The diff check against `4c1e9a2` is not verified.** There is no git history, so changed files can't be compared with each ticket's `touches`. By reading, `app/tools/export.py` and `tests/journey/` break the match. This counts as not verified, not passed.
3. **This read-only review is done.** The findings above are its output.
4. **Findings 1 and 2 keep phase 1 open.**

## Questions I could not ask, and what I assumed

- **Is `export_conversations` meant to exist?** I assumed not, since no ticket or requirement asks for it.
- **Is `_PROFILE_CACHE` live in the running app?** I assumed yes, because `server.py` calls `initial_state`.
- **Is "14 tests" correct?** I assumed it can't be reconciled and that the number needs re-running.

## Left undone

- I ran no tests, `plan_status.py` or `check_tickets.py`.
- I didn't edit the plan, design or tickets.
- I didn't update the Evidence cells for C2 and C3 or the "evidenced" status of G04.
- No independent review run is recorded.

Before the review, these need settling with Ana and Priya:

1. Unbind `bulk_delete_history` and add a `SHALL NOT` acceptance item tagged C5. Decide whether to keep or delete `export_conversations`, and if kept, give it a ticket, an owner check and a contract.
2. Remove the cache, or clear it on forget and save, and add a test that covers the new-session-after-forget path.
3. Build and run a real journey test.
4. Test the Drive "saved" path.
5. Confirm the consent screen with a named person and date.

Next prompt, once the plan is updated for those:

```text
/adk-system-designer Checkpoint docs/plans/support.md. Agenda: the phase-1 review findings 1-9 (C5 not proved absent, export_conversations unrequested, C2 cache contradiction, G04 journey missing, C3 evidence partial).
```
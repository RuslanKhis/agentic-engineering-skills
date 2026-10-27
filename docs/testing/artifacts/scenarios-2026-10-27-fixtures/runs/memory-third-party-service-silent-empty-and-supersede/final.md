I changed the memory layer, but none of it has been run. Bash is disabled in this session, and `google-adk` and `mem0ai` aren't installed. The new tests would skip here anyway, so the "prove it" part is not done. Run `python -m unittest discover -s tests -t .` in an environment with ADK installed.

**Why each symptom happened**
- **"Forgot everything":** the guide's adapter wrote `app_id` as metadata but filtered on it at search time, which matches nothing. It also printed every exception and returned an empty list, so staging logs showed no errors. This is from the skill's reference notes on Mem0's docs, not something I could execute.
- **Old and new address together:** search didn't ask for current facts only, so Mem0 returned the superseded address too.
- **Erasure (HL-4518):** there was no way to delete anything. Mem0 also sends a telemetry event carrying the erased user's id by default.

**What I changed**
- **`homeline/memory/mem0_service.py`**
  - `app_id` is now written on `add` and filtered on in `search`.
  - Search passes `latest_only=True`.
  - Provider failures, and a malformed response, raise `Mem0MemoryError`. They are logged and counted in `write_failures` / `search_failures`.
  - `erase_user()` records the user first, so writes and reads for them stop. It then calls `delete_all` and confirms by listing with `get_all`. It raises if anything is left.
  - `MEM0_TELEMETRY=False` is set by default.
- **`homeline/memory/erasure.py` (new):** `erase_user_data()` erases the Mem0 memories and the user's stored sessions, and reports each separately.
- **`homeline/main.py`:** a failed memory write no longer breaks the customer's reply. The service has already logged and counted it.
- **`tests/test_mem0_service.py`:** a fake client that behaves like the Platform. It covers:
  - writing then reading under one scope;
  - other users and other apps seeing nothing;
  - the moved-address case;
  - search and write failures not turning into empty results;
  - erasure leaving other users' data alone and blocking new writes;
  - erasure that isn't confirmed, and the restart-surviving tombstone.

**Assumptions** (nobody was available to ask)
- A user who asked to be forgotten stays blocked from memory until someone clears the tombstone, for example if they re-consent.
- The `latest_only` keyword and `app_id` as an entity field on `add` come from the skill's notes on Mem0's source (commit 2c81af3), not from mem0ai 2.2.1 itself. Check them against the installed package.
- `agent.py` still uses `PreloadMemoryTool`, which swallows a failed search and carries on without memories. The failure is now logged and counted, but the model isn't told. `LoadMemoryTool` would surface it as a tool error. I left the tool alone because it changes how recall behaves.

**Not done**
- **Existing memories:** anything written before this change has `app_id` only in metadata, so the new filter won't find it. It needs a backfill or re-ingest against a live key.
- **HL-4518:** nothing is wired to trigger the erasure yet, and no live erasure has been run. The request is due 21 Nov. Verify with the real client, then run `erase_user_data` for that customer.
- **Other stores:** the in-memory booking records aren't erased. Whether they should be is a business-records decision. Backups of `homeline_sessions.db` aren't covered either.
- **Duplicate writes:** every turn still re-sends the whole session to Mem0 rather than just the new events.
- **Alerting:** the failure counters aren't connected to an alert.
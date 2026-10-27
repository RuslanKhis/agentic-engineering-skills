I added the response-language memory, but I couldn't run any tests: Bash is disabled in this session, so nothing was executed. The new code and `tests/unit/test_preferences.py` are unrun.

**What I did**
- **Where the preference lives:** a response language is an exact user setting, so I stored it as a profile value rather than a semantic memory. It goes in ADK `user:` state under `user:response_language`. The existing Cloud SQL `DatabaseSessionService` persists that per user across sessions. That needed no new table, dependency or scaffold edit, and `pyproject.toml`, `uv.lock` and the generated files are unchanged.
- **`app/preferences.py` (new):** `set_response_language(language)` is a tool that checks the name against an allowlist. It saves the normalised value, and "default" clears it. `language_directive(state)` turns the saved value into instruction text, and ignores empty or unknown values.
- **`app/agent.py`:** the instruction is now a function that appends the saved-language directive on each invocation. The new tool is registered, and the instruction tells the model when to call it.
- **`tests/unit/test_preferences.py` (new):** tests for normalisation and the stored key, rejection of unknown values with nothing stored, the directive, and clearing. They use no ADK imports and need no network.
- **`.agents-cli-spec.md`:** I added a "Proposed amendment" section, marked pending Owen's acceptance, instead of editing the accepted text.

The skill's build phase says not to write behavioural unit tests. I read your "offline tests" instruction as covering plumbing. These tests check the tool's validation, what gets stored and the directive text, not what the model says. Behaviour should be covered by an eval case instead.

**Questions I couldn't ask, and what I assumed**
1. Which languages are allowed? I assumed a 16-language list in `app/preferences.py`, which is easy to change.
2. Should the amendment to the accepted spec be approved? I assumed yes, but marked it pending.
3. Does "forget" mean the row is deleted? I assumed clearing the value is enough. The row stays, and Cloud SQL point-in-time recovery keeps older copies.

**Left undone**
- **Tests:** run `uv run pytest tests/unit` or `python -m unittest discover -s tests/unit -t .`.
- **Eval case:** I did not add one to `tests/eval/datasets/helpdesk_basic.json`, because running it needs live model calls, which aren't authorised.
- **Persistence not exercised:** I haven't tested against a real `DatabaseSessionService` on SQLite or Cloud SQL, or confirmed it for the pinned ADK version. I assumed `user:` state set in a tool is stored and merged into the next session's state, per the skill's reference.
- **Existing gap that affects this feature:** the identity middleware in `app/fast_api_app.py` only checks the user ID in `/users/...` paths. `/run` and `/run_sse` take `user_id` from the request body, so a signed-in caller could probably act as another staff ID. That would let them change someone else's saved language, and it already affects `my_tickets` and `raise_ticket`. The fix is to reject any body `user_id` that differs from `request.state.staff_id`. I left it alone because it goes beyond what you asked for.
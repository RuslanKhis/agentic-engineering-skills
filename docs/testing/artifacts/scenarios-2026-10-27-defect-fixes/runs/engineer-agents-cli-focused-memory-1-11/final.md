I added a saved response language per user, but none of the new code has been run. Bash is disabled in this session, so no tests, no `uv` and no interpreter ran (tier `offline`, outcome `not run`).

**What I built**
- I treated the language as an exact user setting, so it's a saved profile value and not semantic memory. It lives in ADK `user:` state (`user:response_language`). The existing Cloud SQL session backend keeps that per staff ID across sessions and restarts.
- `app/preferences.py` is new and has no ADK imports. It holds an allow-list of 16 languages, the validation, and a read that re-checks the stored value.
- `app/tools.py` gains `set_response_language(language, tool_context)`. It accepts only allow-listed values, so free text can't reach the system instruction, and a rejected value leaves the saved one unchanged.
- `app/agent.py` now uses an instruction provider that adds the saved language on every invocation. The new tool is registered with the agent.
- `.agents-cli-spec.md` has a "Proposed amendment (pending Owen's acceptance)" section. The accepted spec listed only three tools, so I didn't edit its text.
- `tests/unit/test_preferences.py` has 8 offline tests that assert stored effects. `tests/unit/test_preferences_runner.py` runs a real Runner with a scripted model on SQLite. It checks that the preference persists after a restart, isn't shared with another user, and isn't stored for a rejected language. It skips unless `google-adk` and `aiosqlite` are installed, and I couldn't check that it works.
- I didn't change the scaffold, `pyproject.toml`, `uv.lock`, the session backend, `tests/eval/` or `fast_api_app.py`. Nothing was installed, and there were no network calls or cloud resources.

**Questions I couldn't ask, and what I assumed**
1. Is the language list right? I assumed the 16 in the module.
2. Does the preference need its own retention or erasure when someone leaves? I assumed it follows the session database's retention. That isn't verified.
3. Is the spec amendment accepted? I assumed it's pending and wrote the code anyway. Owen needs to accept or reject it.

**Gaps and left undone**
- **Run the tests:** `make test` — I expect the new unit tests to pass, but I haven't seen them run.
- **Identity gap (not fixed, outside this scope):** the middleware in `app/fast_api_app.py` checks the staff ID only when `/users/<id>/` is in the URL path. `/run` and `/run_sse` take `user_id` from the request body and aren't checked. A signed caller could therefore read or write another person's saved language and tickets. The remedy is to parse the body in the middleware or a dependency and require `user_id == staff_id`. I'd add a test that sends a mismatched body.
- **Evals:** I added no eval cases. A language-following eval would need a live model, which isn't authorised.
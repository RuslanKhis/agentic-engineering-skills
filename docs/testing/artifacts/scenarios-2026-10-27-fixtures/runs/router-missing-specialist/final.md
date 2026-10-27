I added persistence for the language preference, but I haven't run the tests. I had no shell in this session, so the new tests are written and unexecuted. Run `python -m unittest discover -s tests -t .` to check them.

**Why it was lost.** Nothing stored the preference anywhere durable. The only per-user state is ADK session state, and `app/server.py` keeps sessions in `InMemorySessionService`, so a restart wipes it. The SQLite store (`SUPPORT_DB_PATH`, default `support.db`) already survives restarts, so the preference now goes there.

**What I changed**
- **`app/store.py`:** a new `preferences(user_id, language)` table, created with `CREATE TABLE IF NOT EXISTS`, plus `set_language` and `get_language`. Existing databases need no migration.
- **`app/tools/preferences.py`:** a new `set_language_preference` tool. It writes under `tool_context.user_id`, which comes from the verified principal, never from the request or the model. It only accepts a tag like `en` or `pt-BR`, because the value ends up in the instruction text.
- **`app/prompts.py` and `app/agent.py`:** `instruction_for(user_id)` appends the saved language to the instruction. The agent now takes a per-request instruction callable instead of the fixed string, and the new tool is registered. The prompt also tells the model to save a language when the customer asks for one.
- **`tests/test_preferences.py`:** covers per-user scoping, rejection of a bad tag, the instruction change, and the value surviving a close and reopen of a file-backed `Store`.

**Not done or unverified**
- **Specialist skill missing:** `adk-memory-architecture` isn't installed and you excluded installing, so none of its guidance was used. The design is my own reading of the repo.
- **ADK instruction callable:** I haven't confirmed against the pinned ADK version that it receives a context with `user_id`. `app/agent.py` is the only place that depends on this, and the SDK isn't loaded in the tests.
- **Rest of the session state:** conversation history is still lost on restart. I treated that as out of scope.

**Questions I couldn't ask, and what I assumed**
- Should it be a free-form language tag or a fixed list of supported languages? I assumed a free-form tag with format validation.
- Should the preference also be settable from a UI or API route? I assumed the chat tool is enough.

**Follow-up prompt:** "Run the unit tests, then check that `LlmAgent` in the pinned `google-adk` accepts an instruction callable that reads `ctx.user_id`, and confirm the saved language is applied after a process restart."
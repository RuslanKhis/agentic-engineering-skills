I added the language preference and its tests, but I couldn't run any of them. This session has no shell tool, so every result below is `not run`.

**What it does**
- `app/preferences.py` is new. It stores one row per verified staff ID in SQLite and has set, get and delete functions. The file path comes from `LANGUAGE_PREFS_DB`, defaulting to `language_prefs.sqlite3`.
- Only `en`, `fr`, `de`, `es` and `pl` are accepted. The saved value goes into the model instruction, so free text is rejected. A stored value outside that list is ignored when read.
- `app/tools.py` has three new tools: `set_language_preference`, `get_language_preference` and `delete_language_preference`. They take the staff ID from `tool_context.user_id`, never from the conversation.
- `app/agent.py` now builds the instruction per invocation. It reads the caller's saved language and adds "Reply in X" when one is set. Deleting the preference takes effect on the next request.
- `tests/unit/test_preferences.py` is new. It covers:
  - save and read, including normalising the input;
  - the row existing in the file after a simulated restart;
  - separation between users;
  - overwriting a saved language leaving one row;
  - delete removing the stored row;
  - rejecting an unsupported value without writing it;
  - ignoring a corrupted stored value;
  - the instruction following save and delete, which is skipped if `google-adk` isn't installed.

I left the spec, `fast_api_app.py`, the manifest, the Dockerfile, the Makefile and the Terraform alone, and installed nothing.

**Assumptions** (nobody could answer)
1. The five-language list is a guess. Please confirm it or give me the real one.
2. The file store survives process restarts, but Cloud Run's disk doesn't survive redeploys or new instances. For real durability on Cloud Run, `LANGUAGE_PREFS_DB` has to point at a mounted volume, or the store has to move to a managed database. Both are deployment changes, so I left them for you to approve.
3. The accepted spec lists three tools and now there are six. I didn't edit it. Someone should update it.
4. The tools save or delete only when the user asks, enforced by the tool descriptions and the instruction. Nothing in code checks the request.

**Left undone**
- Run `python -m unittest discover tests/unit` with the project's interpreter.
- No eval cases were added for the model's behaviour with these tools.
- No live check through the real serving entrypoint.
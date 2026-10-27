A1 is written but not run: this session had no shell, so I couldn't execute any tests. G02 is `in_progress`, and A2, A3, the route and the web reader are not started. The `Progress:` block is at the head of the ticket's Evidence section.

**What I did**
- **`app/stream.py`:** new, with no `google.adk` imports. `relay(events, session_id)` turns ADK events into SSE frames: a `session` frame, `text` frames, then exactly one `completed`. It forwards text from partial events only, and uses the closing event only when no partial arrived.
- **`tests/test_stream.py`:** new, with two A1 tests using a scripted event source and duck-typed events (not real ADK events). They check that `completed` comes once and after the text, and that a non-streaming reply is sent once.

**Not done**
- **A2:** `failed` on a raise after partial text, with no `completed`.
- **A3:** stop the run and record `interrupted` on client disconnect.
- **Route and web:** `POST /api/chat/stream` in `app/server.py`, and the fetch reader in `web/src/chat/`.
- **Runner-level test:** it needs the SDK, so it will be reported as not run.
- **Tests:** G01's pass-to-pass tests (`G01/A1`, `G01/A3`) were not run either.
- **C3:** the design's Evidence cell is unchanged, because there is no evidence for it yet.

**Assumptions I made (nobody to ask)**
- **Closing event:** I assumed ADK's SSE mode ends with a non-partial event that repeats the whole text. The Runner-level test should confirm this.
- **Existing route:** `/api/chat` stays, with the stream route added beside it.
- **Event names:** `session`, `text`, `completed`, `failed` and `interrupted` are my choice. The ticket fixes only the terminal names. G03 and the web reader should use these.

**Worktree:** this directory isn't a git repository, so I found no `../wt-G02` and didn't create one. I left the changes uncommitted. Create the worktree before continuing if you want it.

**Effort still owed:** roughly 1.5–2.5 h hands-on plus 0.5–1 h to review and verify. Running the suite is the first step. `actual:` is `not reported`.

Next prompt:
`/adk-engineer Resume docs/tickets/support/G02.md from its Progress block.`
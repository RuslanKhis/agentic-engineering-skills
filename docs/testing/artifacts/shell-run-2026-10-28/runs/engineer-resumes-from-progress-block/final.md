G02 is not finished. The server side is built and A1–A3 pass locally, but the chat panel reader is not built and nothing that needs FastAPI or the ADK SDK has run. I left G02 `in_progress`.

**Done**
- I resumed from the Progress block. A1's re-verify command passed before I changed anything.
- I fixed the A2 bug in `wt-G02/app/stream.py`. A stream that fails now ends after `failed`, with no `completed` after it.
- For A3, a client disconnect now closes the run and calls an `on_interrupted` hook. The route logs that hook as "stream interrupted".
- I added A2 and A3 tests. `python -m unittest tests.test_stream` passes 3 of 3 (local). The main checkout's suite passes 15 of 15.
- I wrote `_run_events` and registered `POST /api/chat/stream` in `wt-G02/app/server.py`. I couldn't run it, and the `event.partial` handling is from memory of the SDK.
- `docs/tickets/support/G02.md` now has A2 and A3 ticked, fresh Evidence and an updated Progress block.

**Not done**
- The chat panel reader in `web/src/api.ts` and `ChatPanel.tsx` is not built. It needs the new message states that G03 adds to `Message.tsx`, which is G03's file, so I didn't touch it.
- Not run:
  - the route
  - the SDK-level Runner test
  - `npm test`
  - the IAP buffering check for SSE
- The 15-test suite ran against the main checkout, which doesn't contain the G02 changes. `wt-G02` holds only the touched files, so the combined result is unconfirmed. The folder isn't a git repo either, so `git status` was unavailable and I confirmed the files by listing them.
- I did not start G03. G02 comes first and they overlap on `Message.tsx`.

**Assumption, since nobody could answer:** a disconnected client can't receive a final frame, so I treat C3's `interrupted` as recorded on the server only. If you want it persisted to the store, that needs a designer decision.

**Owed from a person:** about 1–1.5 h for the web reader and its review, plus about 0.5 h for the SDK test and a manual stream check on the deployed app through IAP.

**Next prompt:** `/adk-engineer Carry out docs/tickets/support/G03.md.` Then resume G02 with `/adk-engineer Resume docs/tickets/support/G02.md from its Progress block.`
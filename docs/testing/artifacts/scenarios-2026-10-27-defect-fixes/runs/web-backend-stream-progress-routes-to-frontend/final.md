I added a streaming chat route and a chat UI that shows each tool call as a line and keeps a partial answer if the run fails. None of it has been run. I had no shell in this session, so the Python tests, the type check and the browser path are all `not run`.

**Backend**
- `app/streaming.py` (new) turns agent events into one JSON frame per line: `session`, `tool_start`, `tool_end`, `text`, then exactly one `done` or `error`. It doesn't import `google.adk`, so it follows the AGENTS.md import rule.
- Tool frames carry only a fixed title (for example "Look up order") and an ok flag. Arguments and results stay on the server because they can hold other customers' data.
- Thought-marked text is dropped. A tool call with no result by the end of the run is closed as failed.
- If the run raises or an event reports an error after text, the client gets a terminal `error` frame with a generic message. Details go to the server log only.
- `app/server.py` has a new `POST /api/chat/stream`. It uses the same verified-principal dependency and session lookup as `/api/chat`, which I left unchanged. Auth and session failures are ordinary HTTP errors, before any bytes are sent.

**Frontend**
- `web/src/api.ts` has `streamMessage`, which reads the stream line by line and checks each frame's shape.
- `ChatPanel.tsx` and `Message.tsx` show "Running X…", "Ran X" and "Failed to run X" lines, and a "Working…" line before the first event.
- A failed turn keeps its text and is marked "Failed — the answer above is incomplete". A stream that ends without `done` or `error` is treated as cut off, and any step still running is marked failed.
- `theme.css` has a few additions that reuse the existing colour tokens.

**Tests:** `tests/test_streaming.py` has six cases: the tool lifecycle, a tool error, thought text, an exception after text, an event error code, and a call with no result. Run them with `python -m unittest discover -s tests -t .`.

**Assumptions**, since nobody could answer:
- You didn't specify a transport, so I used newline-delimited JSON over a plain POST. The browser reads it with `fetch` rather than `EventSource`, which can't send the auth header. I didn't use AG-UI because there's no CopilotKit in the app.
- I kept `/api/chat`'s existing behaviour where an unknown or other-user session ID quietly creates a new session. Should it return 404 instead? I didn't change it.
- The runner isn't in partial-streaming mode, so each text frame is a whole message. Text appears per event, not per token.

**Left undone**
- No Stop button, no per-step expansion to show results, and no request timeout or cancellation test.
- I didn't remove the old `sendMessage` helper or `/api/chat`.
- There are no HTTP-level route tests (for example that a rejected token never invokes the agent) and no browser test of a stream cut mid-answer.
- `docs/design/DESIGN.md` has no guidance on trace lines, so their styling is my own minimal choice.
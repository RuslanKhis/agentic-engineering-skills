I wrote the code and tests for both tickets, but I ran no tests. This session had no shell, and `web/node_modules` isn't installed. Both tickets are `in_progress`, and no acceptance box is ticked.

**I didn't run them in parallel.** G02's `touches` includes `web/src/chat/`, which contains G03's `Message.tsx`, so both tickets write that file. The `parallel_safe: yes` flags were wrong. The directory also isn't a git repo, so the `../wt-G02` and `../wt-G03` worktrees couldn't be created. I set `parallel_safe: no` on both tickets and built G02 first, then G03, in this checkout, uncommitted.

**G02, streamed replies**
- `app/stream.py` is new and has no ADK imports. It relays text chunks as SSE and ends with exactly one `completed` or `failed` event. On a client disconnect it stops the run and records `interrupted`.
- `app/server.py` now has `POST /api/chat/stream`, which feeds ADK partial events into that adapter.
- `tests/test_stream.py` covers A1, A2 and A3 with a scripted event source.
- `web/src/chat/stream.ts` is new and reads the stream with fetch. `ChatPanel.tsx` now uses it. A stream that closes without a terminal event counts as `failed`.
- I widened the `ChatMessage` state type in `Message.tsx` so the panel compiles.

**G03, honest failed replies**
- `Message.tsx` now renders the streaming, failed and interrupted states. A failed reply keeps its text and shows a failed badge, and nothing shows as completed while the stream is open.
- `Message.test.tsx` covers A1 and A2. It uses `react-dom/server` because `web/package.json` has no jsdom and pins must not change.

**Not done**
- I ran none of the tests, including the G01 `pass_to_pass` baseline, so no acceptance box is ticked.
- The design's contract Evidence cells for C3 and C5 still say `planned`.
- There is no Runner-level test. I haven't checked `_text_chunks` in `app/server.py` against google-adk 2.12.0. It assumes `StreamingMode.SSE` yields partial events carrying the text.
- `plan_status.py` wasn't run, and I haven't set `actual:` hours on either ticket.

**Owed to a person**
- About 0.5–1 h for G02 and 0.5 h for G03 to review and run the tests.
- A real-runner check of the stream route behind IAP.
- A look at the failed badge in the browser once the stream is live.

Run these two, in order:
```
python -m unittest tests.test_stream tests.test_preferences
cd web && npm test -- Message
```

Then resume from each ticket's Progress block:
`/adk-engineer Resume docs/tickets/support/G02.md from its Progress block.`
`/adk-engineer Resume docs/tickets/support/G03.md from its Progress block.`

I assumed sequential runs in one checkout were acceptable, since nobody could be asked.
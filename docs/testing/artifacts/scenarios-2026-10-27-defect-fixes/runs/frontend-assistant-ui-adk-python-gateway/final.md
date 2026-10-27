The backend gateway and the assistant-ui frontend are written, but I couldn't run any of it. This session had no shell tool, so the tests, TypeScript build and browser path are all unexecuted (`offline: not run`).

**What I added**
- **`app/gateway.py`** holds the gateway rules and imports no `google.adk`.
  - **Request checks:** it validates the proxy body. `stateDelta` is refused, `runConfig` and any browser-supplied user id are ignored, and calls, thoughts and other part kinds are rejected.
  - **Approvals:** it accepts one only as `adk_request_confirmation` with exactly `{"confirmed": bool}`, for a call still pending in the caller's session.
  - **Edit checkpoints:** it resolves `start` / `after:<invocation id>` to a rewind target. It refuses the rewind (`rewind_blocked`) if a refund or email in the removed turns already went through, and it reads history with rewind markers applied.
  - **Event filter:** it drops thoughts, state deltas, usage and grounding metadata, and foreign authors. Tool results are reduced to an allowlist, and error text is replaced with fixed copy.
- **`app/server.py`** has two new routes, `POST /api/adk/sessions` and `POST /api/adk/run` (SSE). The session is looked up under the verified principal before any rewind or agent call, so unknown and foreign sessions both return 404. Approval answers run before text, because ADK 2.12.0 refuses both in one message. There is a 120 s deadline that includes lock waiting.
- **`tests/test_gateway.py`** covers parsing, approvals, edits and the event filter.
- **`web/src/adk/`** has the runtime wiring, a stream client that validates each event, a refund approval card, and a thread with an Edit button. There is no `cloud` option, so nothing goes to Assistant Cloud. `App.tsx` now uses it, and `README.md` has a new section.

**Assumptions I proceeded on**
- No CopilotKit code was present; the existing UI was a custom chat panel, so I replaced that. I left the old `ChatPanel`, `Message`, `api.ts` and `/api/chat` in place. `/api/chat` cannot answer an approval, so it is a risk if still reachable.
- The gateway allocates sessions (`create`), and the browser never sends a user id.

**Unverified or left undone**
- Run `python -m unittest discover -s tests -t .` first; I traced the new tests by hand only.
- The assistant-ui option names (`stream`, `create`, `getCheckpointId`) and the shape of its tool-result answer are from the skill notes and my memory of the docs, not from the package source. Reconcile `AdkProvider.tsx` and `gatewayApi.ts` after install. The edit button depends on `checkpointAfter` guessing how message ids carry the invocation id; a wrong guess hides the button rather than breaking the app.
- `package.json` lists only `@assistant-ui/react-google-adk` at 0.0.40. I didn't invent a version for `@assistant-ui/react`, which the code imports, so the build will fail until you add the right one. Pin the unpinned `assistant-cloud` dependency in the lockfile.
- I haven't confirmed that ADK 2.12.0 resumes a confirmation from a bare function response (no invocation id). A scripted-model test on the real SDK is needed, and it should also check that a rewound turn is absent from the next model request.
- Sessions are in memory with a per-process lock, so run one instance. There is no history endpoint, so a page reload loses the conversation and any unanswered approval.
- There is no browser test, and I didn't check the approval card against `docs/design/DESIGN.md`.
- `send_email` is also a write; it only gets the rewind guard, not an approval. Whether it should need approval is your call.
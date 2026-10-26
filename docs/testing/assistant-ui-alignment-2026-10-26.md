# assistant-ui alignment — 26 October 2026

Source note: [comparison](../research/assistant-ui-comparison-2026-10-26.md).

## Changed journey

`adk-frontend-integration`, a gateway for a frontend that consumes raw ADK
events, with edit and regenerate.

## Fresh-agent trial

A fresh agent built the FastAPI gateway for a Python ADK 2.12 support agent
(`lookup_order`, a confirmation-gated refund) behind assistant-ui's
`@assistant-ui/react-google-adk` 0.0.40, read from its npm tarball and never
run: a streaming route, a thread-creation route that allocates session ids,
and a history route, with test identity, ownership checks, an input
allowlist, a filtered event stream, fixed error copy, a per-conversation
lock, approval handling and edit and regenerate through `rewind_async`. It
declined Assistant Cloud, the package's thread-list adapter, browser tools
and a compiled frontend.

`pytest`: **41 passed**, twice, offline with the real Runner and a scripted
model. Every hostile request was refused before any model call: a body user
id, thought, function-call, code or inline-data parts, a browser result for
the refund tool, an `app:` state delta, truncated JSON, an oversized or
non-JSON body, a path-like session id, a checkpoint from another user's
session, a replayed approval and a wrapped approval. One real failure
before the final run: ADK 2.12 raised "Message cannot contain both function
responses and text" on the batch assistant-ui sends; the gateway now splits
it.

Ease: 3 of 5.

## Frictions and fixes (same day)

1. No routing for a raw-event frontend. Fixed.
2. Edit and regenerate behaviour in the package (checkpoint ids,
   empty-text regenerate, null checkpoints). Fixed.
3. `rewind_async` facts: no ownership check, a marker rather than
   deletion, no undo of side effects. Fixed (checked in 2.12.0 source).
4. A batched approval and text cannot reach ADK 2.12 as one message.
   Fixed: split into ordered runs (checked in source).
5. The confirmation shape to accept. Fixed: exactly `{confirmed: bool}`
   for a pending call; ADK's looser shapes are narrowed at the gateway.
6. Which event fields the filter must keep. Fixed.
7. How to treat `runConfig`, `stateDelta` and `checkpointId`. Fixed.
8. The thread-list adapter's browser-chosen user id. Fixed.
9. No compatibility row and no inspector detection. The row is added; the
   inspector is unchanged.

## Limits

No browser, live model, network SSE framing or production identity;
disconnect and cancellation were not tested.

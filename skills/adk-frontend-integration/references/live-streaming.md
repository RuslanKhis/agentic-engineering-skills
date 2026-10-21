# Live audio and video streaming

Use when the journey carries continuous audio or video between the browser and
the agent. This is a third transport beside the JSON API and AG-UI: a
bidirectional socket on both sides of the gateway, a Live API session instead
of a request, and limits that become contracts. The companion implements none
of it; the facts here come from the official pages cited inline and from
Google's `google-cloud-solution-agentic-ai-bidirectional-streaming` skill
(google/skills, Apache-2.0, read 21 October 2026). Verify every limit against
the pinned SDK and the chosen model before promising it.

## Decide the session contract first

- **Entry point.** Live audio and video run through `run_live()`, which holds
  a WebSocket to the Live API; `StreamingMode.BIDI` on `run_async()` is not
  that path, and the live models accept `response_modalities=["AUDIO"]` only.
  Only models built for the live path hold a bidirectional connection; a
  standard Gemini model does not
  ([ADK live configuration](https://adk.dev/live/configuration/), fetched
  21 October 2026).
- **Session length.** The provider's connection lifetime is around ten
  minutes, an audio-only session about fifteen minutes and an audio-plus-video
  session about two minutes without context-window compression; with
  compression the session can continue, and session resumption lets a client
  reconnect within 24 hours
  ([Live API sessions](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/live-api/start-manage-session),
  fetched 21 October 2026). Write the length the product needs, enable
  `session_resumption` and `context_window_compression` in `RunConfig` when it
  exceeds the raw limits, and decide what the user sees when a session is cut
  anyway.
- **Budget.** `max_llm_calls` does not apply to `run_live()` (same ADK page);
  the application bounds a live session by elapsed time, by resumption count
  and by the host's request timeout, and records usage per session for the
  spend stop that `adk-operational-guardrails` owns.
- **Model capacity.** Pay-as-you-go projects have a concurrent-session quota;
  Provisioned Throughput removes it for business-critical traffic (Live API
  sessions page, 21 October 2026). Name which one the design relies on.

## Host the socket deliberately

- A WebSocket on Cloud Run is one long HTTP request: it ends at the service's
  request timeout (at most 60 minutes), the instance counts as active and is
  billed while any socket is open, and session affinity is best effort, so
  two sockets from one user can land on different instances
  ([Cloud Run WebSockets](https://docs.cloud.google.com/run/docs/triggering/websockets),
  fetched 21 October 2026). Keep per-session state in a shared store
  (Memorystore or Firestore in the official guidance) and treat a reconnect
  as attaching to recorded state, never as a new session with lost context.
- Terminate the browser socket at a regional external Application Load
  Balancer with a Cloud Armor policy, and give the Cloud Run service the
  `INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER` setting so the default `run.app`
  URL cannot bypass authentication and rate limiting; enforce TLS on the
  socket because voice and video are personal data
  ([reference architecture](https://docs.cloud.google.com/architecture/agentic-ai-bidirectional-multimodal-streaming),
  fetched 21 October 2026). `deploy-adk-on-google-cloud` carries the ingress,
  egress and DNS settings.
- Authenticate before the upgrade. The socket handshake is the only point at
  which the gateway verifies the caller and binds the session to a user; a
  frame arriving later is data. The identity and ownership rules in
  [production.md](production.md#identity-and-conversation-access) apply
  unchanged.

## Shape the media path

- Decouple capture from inference with an asynchronous first-in-first-out
  buffer between the socket reader and the Live API writer, so the interface
  stays responsive to interruptions and a slow model does not block the
  socket (reference architecture, 21 October 2026). Decide what the buffer
  drops when it is full: audio and video frames are disposable, a user's
  spoken confirmation is not.
- Sample video at a low rate (the official architecture uses about two frames
  per second) and compress frames before sending; write instructions that ask
  for concise spoken answers, because output tokens are the expensive side
  (reference architecture, 21 October 2026).
- Keep safety or monitoring work out of the conversational agent: a
  dedicated background streaming tool watches the stream and raises a
  structured event the agent reads, so monitoring cannot overload the
  conversation loop (reference architecture, 21 October 2026).
- Facts the agent needs within a spoken turn (a schematic, a product
  record) come from a store with sub-millisecond reads, loaded before the
  turn; a slow lookup becomes a silence the user hears.

## Verify what a live path can prove

Offline tests use a fake Live API that replays recorded frames and asserts
the buffer policy, the session-cut outcome and that a reconnect attaches to
recorded state without a second session. A local socket test establishes
timing and cancellation; it does not establish the provider's session limits,
which need one bounded, authorised live session with the pinned model, its
duration and cost recorded as `live provider` evidence. Browser playback and
interruption handling are `live browser` evidence. Report the four classes
separately, as [validation.md](validation.md) describes for the other modes.

When the design of the whole live system is still open, consult the installed
Google skill `google-cloud-solution-agentic-ai-bidirectional-streaming` (from
google/skills) for the reference topology and product alternatives; if it is
not installed, `adk-engineer` explains how to get it.

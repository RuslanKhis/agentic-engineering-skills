# Remote-agent failure handling

Read this with mode (e). A remote agent is an external API with a
conversation attached: it can be slow, down, half-finished, or waiting on a
human. `safe-api-tool-calls` owns retries, deadlines and idempotency of the
call itself; this page says what each A2A outcome looks like inside ADK 2.8.0
and what the parent should do with it.

## What the parent sees

| Remote outcome | ADK 2.8.0 surface (source-verified `remote_a2a_agent.py`) | Parent action |
| --- | --- | --- |
| `completed` task or final `Message` | Event authored by the remote agent name with text parts; `a2a:task_id`, `a2a:context_id`, `a2a:response` in `custom_metadata` | Consume the text; keep `a2a:context_id` for the next turn (ADK does this for you) |
| `working` or `submitted` updates | Parts marked `thought` and removed from the user-facing parts; artifact chunks arrive with `event.partial=True` until `last_chunk` | Show progress in the UI from `partial` events (`adk-frontend-integration`); do not act on them |
| `input-required` | Event with a mock long-running function call and `long_running_tool_ids`; the parent `LlmAgent` pauses as for a local long-running tool | Relay the question to the controlling user; the next user turn becomes a resume message carrying the stored task and context IDs. 2.11.0 fixes a resume regression (#6721); test on your pin |
| `auth-required` | Same mechanism, credential-flavoured mock call; credential-bearing responses are scrubbed before anything is forwarded (2.8.0 "stop RemoteA2aAgent forwarding credential requests to the remote peer") | Complete the peer's auth out of band through `adk-tool-auth-and-secrets`; never paste a credential into the conversation |
| `rejected` | Terminal state from the 1.0 specification; 2.8.0 `_compat` names `TS_FAILED` and `TS_CANCELED` but has no `rejected` constant, so a rejected task reaches you as a task event whose `a2a:response.status.state` says so, without the task-mode failure events | Read `custom_metadata["a2a:response"]["status"]["state"]` in an `after_agent_callback` or the consumer and treat it as a definitive refusal, not a retryable error |
| `failed` or `canceled` | In `mode="task"`: an error event (`a2a:error`, `a2a:task_id`) plus a `finish_task` failure event, then control returns. Otherwise: the converted status event with the state in `a2a:response` | Answer the user with what you know; a failed task is not idempotently retryable unless the peer's contract says so |
| HTTP or client error (401, 403, 5xx, connection refused, timeout) | Event with `error_message="A2A request failed: ..."`, `a2a:error`, `a2a:status_code`, `a2a:request`; nothing raised | 401/403: credential or audience problem, stop and surface it; 5xx and timeouts: at most one retry of a read-only request, none for a request that may have acted |
| Card resolution failure | `error_message="Failed to initialize remote A2A agent: ..."` | Configuration error; fail the deployment check, not the user turn |
| Stream ends before a terminal state | 2.8.0: the loop ends and the parent continues with whatever arrived (silent truncation); 2.10.0 reports it (#6585) | On 2.8.0, check that the last `a2a:response` state is terminal before treating the answer as complete |
| Nothing to send (empty parts) | Event with empty content and a warning; in task mode an error | Usually a history-construction bug; inspect which events were selected |

Error events carry `error_message` but still have `author=<remote name>`;
the parent model sees them as that agent's turn. Decide in a callback or in
the consuming code whether the model should see the raw error text or a
fixed, safe message.

## Timeouts

- `RemoteA2aAgent(timeout=600.0)` is the httpx timeout for the exchange when
  the agent creates its own client (`httpx.Timeout(timeout=...)` applies to
  connect, read, write and pool). A long-running remote task that streams
  nothing for ten minutes hits it. Set it from the peer's SLA and the
  parent's own invocation deadline (`adk-operational-guardrails` owns
  budgets; `safe-api-tool-calls` the cooperative deadline pattern).
- With `a2a_client_factory` and your own `httpx.AsyncClient`, the timeout you
  gave the client wins; the agent then does not close the client.
- Card fetch shares the same client and timeout; a slow card endpoint costs a
  full timeout per invocation when caching is disabled by interceptors.

## Idempotency and retries

A `message/send` may have started work on the peer even when you saw no
response. The A2A task ID is the handle for "did it happen": with
`a2a:task_id` stored, the peer's `tasks/get` answers the question without
resending. ADK 2.8.0 does not call `tasks/get` for you; a retry re-sends the
message in the same context. So:

- Retry only requests the contract marks read-only, and only once.
- For anything that writes, pass a client-generated idempotency key in
  `a2a_request_meta_provider` metadata and have the peer honour it, or make
  the user's next turn the retry. `safe-api-tool-calls` holds the write
  patterns.
- Do not loop the parent model on "try again"; a bounded loop belongs in
  code (`adk-workflow-design`).

## Partial results

Artifacts stream as chunks; a stream cut mid-artifact leaves a `partial`
event without a final. Treat an artifact as complete only when a non-partial
event for it arrived, and record in the contract whether a partial answer is
better than none for this task. The peer's coverage statement (what it
could not do) must be part of its final message; without it the parent
cannot tell a short answer from a truncated one.

## Operational checks

- Logs: `build_a2a_request_log` and `build_a2a_response_log` run at DEBUG
  and keep file payloads out (2.8.0); redact before shipping logs elsewhere.
- Metrics: count error events by `a2a:status_code`, terminal state and peer;
  alert on `rejected` and 401/403 bursts (configuration drift) separately
  from 5xx (peer health).
- Traces: propagate W3C headers with a request interceptor if the peer
  honours them; `adk-agent-observability` owns the exporter.
- A fake peer in tests reproduces each row above
  ([evaluation-across-boundaries](evaluation-across-boundaries.md)).

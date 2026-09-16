# Enforce a finite model-request budget

Use this reference when an authorised local run needs a strict request ceiling,
or when hidden retries, restarts or streaming timeouts could exceed that ceiling.
Ordinary workflow edits do not require a campaign launcher. Define the permitted
calls and window through [external-validation.md](external-validation.md) first.

These mechanics were checked with ADK 2.8.0, google-genai 2.23.0 and HTTPX 0.28.1.
The checked GenAI aiohttp path could reconnect outside its configured retry
policy. Setting `HttpRetryOptions(attempts=1)` alone therefore did not establish
one transport attempt. Reinspect a different SDK/transport before adapting this
recipe; preserve the target project's versions unless a change is requested.

## 1. Define the counted boundary and durable record

Count submissions separately from model transport sends. One invocation can have
several model calls, including a continuation after a tool response. A workflow
iteration limit does not cover every send. The regular ADK Web launcher supplies
no campaign-wide attempt budget.

Create a private local journal containing the approved backend/project/model/
location, approval reference, immutable start/cutoff, submission and send limits,
invocations, attempts and stopped workflows. Store identifiers, times and outcome
labels; exclude credentials, prompts and response bodies. An approval reference
records authority already granted; creating the record does not grant it.

For each journal mutation, lock the record, validate current state, write a
restricted-permission temporary file, flush/fsync it, then atomically replace the
old record. Reserve attempts before calling the network transport. Concurrent
sibling agents must share this accounting and cannot each read an old count and
spend the last slot. The checked implementation uses POSIX file locking.

This is a single-process local campaign journal with concurrent async work and
restart support. It is not a distributed quota service or an exactly-once
execution system. Local reservations count attempted sends, including uncertain
failures; they cannot prove provider receipt, cancellation or billing.

## 2. Construct and install the guarded client before agents load

1. Start a fresh process and validate the supported SDK versions. Model instances
   cached by an earlier run retain their clients; later registry edits do not
   replace them.
2. Construct an `httpx.AsyncClient` with the counting transport described below,
   `follow_redirects=False` and `trust_env=False`. Its underlying
   `httpx.AsyncHTTPTransport(retries=0)` removes automatic HTTPX connection retries.
   Use explicit configuration if the target requires a proxy or custom trust.
3. Pass that client through the public GenAI construction argument
   `types.HttpOptions(httpx_async_client=owned_http_client, ...)`, together with
   explicit backend, project/location and intended credentials. Configure
   `HttpRetryOptions(attempts=1)` as an additional layer, not the sole control.
4. For the checked ADK path, register a `Gemini` subclass with
   `LLMRegistry.register(...)`; its constructor passes the guarded GenAI client
   to `Gemini` and sets `use_interactions_api=False`. Reject an unexpected model,
   and assert `LLMRegistry.resolve(selected_model)` returns that subclass before
   loading agents. Directly constructed clients need equivalent explicit wiring.
5. Supply the public `BasePlugin` instance to the real ADK Web app's
   `extra_plugins` import path. The transport must refuse an unpermitted call
   even if plugin loading or callback dispatch fails.

In the checked path, `before_run_callback` clears stale permit context and records
the invocation. `before_model_callback` verifies the selected model and permitted
request mode, obtains one permit, and sets request options. Each permit carries
the workflow, invocation, unique nonce and invocation deadline. Use a `ContextVar`
to keep sibling async calls' permits separate. The uncached path was tested;
additional cache/interaction routes need their own endpoint and counting tests.

ADK handles its tools in this path. Set
`AutomaticFunctionCallingConfig(disable=True)` on the GenAI request so SDK-managed
tools cannot silently add calls outside ADK's callback boundary. Preserve the
actual model exception in `on_model_error_callback`; returning an invented answer
would incorrectly turn budget or provider failure into workflow success.

## 3. Validate, reserve and send exactly once per permit

At `AsyncBaseTransport.handle_async_request`, require a permit before doing any
network work. Validate an exact allowlist for HTTPS scheme, host, port, POST
method, API version, project, location, model path and permitted query parameters.
Build this list from the selected backend; a model name alone does not establish
which project or service receives the request. Test normal and streaming routes.

Under the journal lock, check that the permit matches its recorded invocation,
the campaign/workflow remains open, the deadline has not elapsed, the nonce has
not been used, and both workflow and total send allocations have space. Persist
the new attempt as `reserved`, then call the underlying transport. A retry with
the same nonce must fail before another send. Wrong endpoints and missing
permits must fail before either reservation or network traffic.

Record HTTP failures and exceptions against the consumed reservation. In a
no-retry campaign, HTTP redirects are failures rather than fresh destinations;
stop subsequent requests for that workflow. If retries are explicitly allowed,
each needs its own bounded policy and counted attempt. An uncertain result stays
consumed until reconciled; never refund it merely because no answer arrived.

## 4. Cover the whole response and preserve restart boundaries

Set the invocation deadline to the earlier of its completion allowance and the
campaign cutoff. Apply the remaining time both while acquiring response headers
and while iterating the response body. A header timeout alone does not bound a
stalled SSE stream. Per-request SDK timeouts are supplementary controls.

Wrap the returned `AsyncByteStream`: record `response_headers` after success,
`response_complete` only after body exhaustion, and failure on timeout or
cancellation. Its `aclose()` must close the underlying stream and mark unfinished
consumption as `response_abandoned`. Keep those attempts consumed and stop the
affected workflow. Local cancellation does not prove the provider stopped work.

Repeated preparation and cold process restarts reuse the journal and original
cutoff. Validate backend/project/model and approval boundaries against that
journal before proceeding. Refuse an expired or mismatched record, duplicate
invocation replay, and unreviewed pending attempts. A separately authorised
continuation preserves the earlier record, counts and failures; record the new
window and exact permitted changes separately. A new directory is not a refund.

## 5. Close clients and prove the wiring offline

Install application-lifespan cleanup for the owned clients. In the checked SDK,
closing GenAI does not close a caller-supplied HTTPX client: use nested `finally`
blocks to await `genai_client.aio.aclose()`, await `owned_http_client.aclose()`,
and call `genai_client.close()`. Exercise shutdown through the actual app lifespan.
Only close clients the application owns; injected shared clients need an explicit
owner. See [runtime.md](runtime.md) for consuming or deliberately closing runs.

Use the real ADK/GenAI path with a substituted HTTP transport and synthetic
credentials. Keep offline model traffic from reaching the network. Require:

| Case | Observable assertion |
| --- | --- |
| Normal and streaming SDK requests | Each reaches the guarded transport once; correct output survives. |
| Missing plugin/permit or wrong project/endpoint | Zero underlying sends and zero reserved attempts. |
| HTTP error, connection failure, redirect | One counted send; no hidden retry/follow; workflow remains stopped. |
| Reused nonce, exhausted workflow/total budget | Refused before the next underlying send. |
| Slow stream after HTTP 200 | Body deadline expires, consumed attempt records failure, later calls are blocked. |
| Restart/repeated preparation | Counters and original cutoff survive; duplicate invocation stays refused. |
| Resume with pending or changed identity/window | Refused; original evidence remains intact. |
| Real app plus plugin and registry | All intended model paths use the guarded client; owned HTTPX client closes. |

These checks establish local enforcement at the tested SDK boundary. Live model
quality, browser usability, provider billing and distributed recovery require
separate evidence. The grounding is the chapter's audited transport and regression
suite, summarised in [provenance.md](provenance.md); the source checkout is optional.

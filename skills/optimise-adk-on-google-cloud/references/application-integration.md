# Wire an optimisation into the executing application

Read when a setting appears ineffective, a demo mixes simulated and real work,
or a formatter/schema change is not reached. For the architectural decision use
[application.md](application.md); for actual-framework tests and bounded provider
work use [part1-verification.md](part1-verification.md).

## Establish effective configuration before changing behaviour

Record this ledger from the target's actual source and installed interfaces. Keep
configuration key names and non-sensitive values; record secret source/version
references without printing values.

| Boundary | What to record | Failure the check prevents |
| --- | --- | --- |
| Root and each child | Exported object, model constructor and backend/location | Setting `MODEL_NAME` when code still passes a literal model |
| Configuration load | Environment source, loader precedence, import/constructor order | A nested dotenv or early import using another value |
| Tools | Registered callable, client factory, real/mock selector per adapter | Calling real Gemini with mocked query/rate data and labelling the whole run live |
| App and Runner/server | Exported App and the exact object the loader passes onward | Dropping caching/compaction by constructing only from the root agent |
| Profile | Which model, tools, children, cache and server limits it replaces | A small smoke result being attributed to the full application |
| Client lifetime | Creation time, cache, worker ownership and shutdown | A cached client retaining the previous project/configuration |
| Packaging | Source allowlist, package discovery and prompt/assets in the installed tree | A locally imported helper never reaching the deployed image |

The historical data assistant illustrates every distinction: its root and
validator chose a model in source; the CLI loaded subproject dotenv before agent
import; a real/mock setting and bucket were captured at module import; a cached
BigQuery client persisted within the process. Its schema-only hosting profile
replaced the tools, model retry/output settings and cache configuration. These
are examples to look for, not required target names or configuration switches.

Check the loader's actual precedence rather than assuming every dotenv overrides
the process environment. Repeat configuration tests in fresh child processes
with a minimal synthetic environment. For an in-process unit test, clear only
owned test caches explicitly; do not clear clients in a running service to prove
a configuration change. Never import unknown application code just to inventory
it: inspect for network/provisioning side effects first.

An implementation is complete only when the selected entrypoint instantiates the
intended object, a relevant request reaches it, the outgoing request/tool result
has the expected effect and the shipped build contains those bytes. A printed
configuration or imported-but-unused child establishes none of these.

## Give each result a bounded, explicit child input

The optional [formatting contract](../assets/formatting_contract.py) adapts the
manuscript's production example. It validates a current-result envelope containing
`correlation_id`, `columns` and `rows`, with strict types, unique columns, matched
row widths, finite floats and a compact UTF-8 byte limit. Its initial limits are
20 rows, 64 columns, 128-character column names, 1,000-character text cells and
65,536 encoded bytes. Treat them as a tested starter contract to adapt to the
task, not provider thresholds or permission to fetch a result of arbitrary size.
The starter also chooses 16–128-character correlation IDs using letters, digits,
`._:-` and at least one column. Adapt these choices to the target's existing ID
and empty-result contract; do not rewrite valid identities merely to fit the
asset. Preserve explicit current-result matching and byte/shape bounds.

Use the component **after** the trusted producer enforces query/result bounds,
and **before** the child call. It validates a supplied preview; it neither
truncates an unbounded result nor creates a database job, formatter or export.
Keep the full authorised result in its separate durable store.

After copying the component into the target package, its public entry points are:

```python
from formatting_contract import parse_formatting_input

preview = parse_formatting_input(current_payload)
handoff_bytes = preview.canonical_bytes()
```

`current_payload` is the already bounded, selected result. The parser returns a
`FormattingInput`; invalid payloads raise fixed `FormattingInputError` without
the original input-bearing validation exception chain. `canonical_bytes()`
revalidates mutable nested lists immediately before serialisation; serialising a
mutated model through another path bypasses that check. Decimal/date/database
types need an explicit upstream representation policy rather than silent
coercion. A JSON number string stays a string, and cells remain untrusted content.

Implement the handoff in this order:

1. Reserve a result/correlation identity for this request, bound to trusted owner,
   query and intended tool call. Keep that authority in backend state; a payload
   correlation string is only a join key and must not confer access.
2. Obtain the current query outcome. On failure, skip formatter and export and
   preserve that failure. Do not fall back to a previous successful state value.
3. For success, compare its correlation identity to the expected tool result.
   Validate the bounded envelope. Reject mismatch, extra fields, ragged rows,
   duplicate columns, nonfinite numbers or coercion instead of silently repairing
   ambiguous data. Treat validation errors as a fixed public failure; raw Pydantic
   diagnostics can include the rejected payload.
4. Handle an empty row set explicitly, normally without paying for a formatter.
   If formatting is needed, serialise a freshly validated envelope as current
   input to the registered child. Treat all column/cell text as untrusted data.
5. Accept the child's complete, semantically valid answer. Keep its result tied
   to the same identity; a later export resolves that exact durable result after
   checking ownership/expiry again. Multiple successful queries require explicit
   selection rather than an implicit mutable last-result pointer.

Keep any existing `AgentTool` or supported child interface unless the task needs
a change. For a narrow ADK 2.8 child, `include_contents="none"` excludes prior
turn content; `mode="single_turn"` with `sub_agents` is another supported
composition. Neither controls aggregate model work. `input_schema` and
`output_schema` validate structures at their supported boundaries; cross-field
invariants must still be exercised in trusted code. Check the installed SDK's
schema representation before exposing a copied Pydantic type directly to a model.

The original companion formatter was imported but not registered, read
`raw_sql_output`, and had no SQL producer populating that field. Its focused
history check was valid; the integrated query-to-formatter path was absent.
This is why tests must invoke the actual coordinator and inspect the request,
rather than merely instantiate the helper or call the child in isolation.

Use distinctive old-history and current-result markers. Capture the actual
child request and assert old-history absence, current-result presence and the
expected invocation/call association. Test consecutive A/B queries, B failure
after A success and interleaved requests; B must never format/export A. Retain
empty-result and invalid-payload cases. The portable contract tests validate
the envelope only; the target must implement these workflow/ownership tests.

## Separate application success from provider success

Trace the exact operation that failed: configuration/client construction,
submission, completion, retrieval, format or export. Successful schema lookup does
not by itself establish query permission; inspect the actual retrieval path.
A successful query can still fail when downloading its result; an
uploaded object is not necessarily a user-authorised download. Assert the required
outcome at each stage and propagate failure to dependent stages.

For a provider adapter, distinguish transport/TLS, HTTP status, decoding and
semantic validation failures. Preserve a safe error category and opaque diagnostic
reference; avoid dumping payloads or exception strings. A missing/invalid quote
must not turn into a plausible numeric fallback. Diagnose CA trust in the exact
failing interpreter/container through
[Cloud Run troubleshooting](cloud-run-troubleshooting.md), keeping verification
enabled. A mock service can use real model calls, so review both boundaries before
describing a test as offline.

## Make the observability change real

Choose phase names and an allowlisted record schema for session load, model/tool
execution and accepted completion. Use monotonic elapsed durations plus revision,
model/backend, outcome and an approved correlation reference; reset request-local
context in `finally`. Plain text logging can discard structured `extra` fields,
so test the actual configured formatter's output. Do not log raw prompts, tool
data, session/user IDs, signed URLs or credentials for timing convenience.

Join external request timing, platform startup/queueing and application spans.
Do not add overlapping phase durations or subtract unsynchronised machine clocks.
First stream event, first visible partial text and complete answer are different
observations. If only full events are delivered, report first model response
rather than inventing time to first token. Preserve all errors and workload state
when comparing candidate and baseline; a shorter failed answer is no improvement.

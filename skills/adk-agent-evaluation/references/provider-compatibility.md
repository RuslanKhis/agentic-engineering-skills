# Check the response shapes actually sent

Read for dynamic structured-output schemas, provider/adapter changes or schema
rejections. Compatibility belongs to the exact provider, endpoint, model, adapter
version, request mode and serialized request. No example here establishes a
restriction for all ADK or OpenAI-compatible routes.

Qualify [contract solvability](contract-qualification.md) offline first. Keep native
Pydantic/custom validation, provider-enforced wire schema and semantic source checks
as separate gates; local parsing and an OpenAI-compatible endpoint prove neither
keyword enforcement nor factual correctness on the selected route.

## Populate the compatibility matrix

Generate requests through the application's pinned SDK/adapter and intercept the
final transport offline. Preserve a sanitized synthetic request and schema hash
after adapter conversion, including effective output settings. Inspect nested
schemas rather than only the application's Pydantic model. Record resolved SDK
versions separately; retain existing dependency pins.

| Actual workflow shape | Representative content | Offline observation | Authorized live observation |
| --- | --- | --- | --- |
| Source selection | Realistic enum count/length; literal multiline quotation and short-ID alternatives | Native serialized enum and escaping; reject the problematic shape in a controlled transport | Exact route accepts/rejects this schema |
| Structured review | Required claim/source slots, nested arrays and nullable/no-evidence branches | Missing/duplicate slots rejected; null branch survives conversion | Valid complete response within configured output limit |
| Visual evidence | Image input plus the actual review schema | Media part, MIME/size and permitted source mapping reach transport | Actual route accepts this combination |
| Largest planned frame | Longest expected draft, enum cardinality and source set | Request/schema bytes and expected response size measured | Truncation/finish status and complete parsed response retained |

Mark unsupported or unused shapes explicitly; do not mark untested rows passed.
Bytes are not tokens. Measure tokens with the target's available tokenizer/usage
facility, or record the token estimate as uncertain. A large frame that cannot fit
the existing output limit needs a contract/workload decision before the cohort.

For exact quotations, a short selection ID can keep full immutable text server-side
and reduce schema size. Validate selections against the draft/source revision and
resolve them on the server. This changes wire format, not whether the passage
supports a claim; run grounding calibration separately.

## Controlled rejection and route binding

The optional [schema evidence helper](../assets/provider_schema_probe.py) compares
exact synthetic wire requests with observation records. Its
[tests](../tests/test_provider_schema_probe.py) use an offline transport that
rejects a multiline enum nested in a schema. They verify that a rejection blocks
the gate, and that a successful observation for a different route or a smaller
request cannot substitute. The helper sends no requests and does not understand
provider schemas or enforce budgets.

Adapt the controlled rejection to the real adapter seam: capture its emitted
bytes, force the matching request to fail and assert no cohort dispatch follows.
Test SDK retries at that seam too. Local serialization acceptance, controlled
transport behavior and remote observations are three different evidence levels.
Retain every response/error and its level; keep authorization headers and private
content out of exported artifacts.

## Run the same agent under an external harness (proven on Inspect)

Inspect AI's `agent_bridge()` intercepts google-adk without an adapter: it patches the google-genai client's `BaseApiClient.async_request` and answers any `:generateContent` request whose model name targets Inspect from the harness's own model provider (`agent/_bridge/bridge.py`, `init_google_request_patch`, inspect-ai 0.3.283). Proven on 2026-10-22 in a scratch environment with google-adk 2.12.0: an `LlmAgent` on `Gemini(model="inspect")` with one function tool, run through `InMemoryRunner` inside `async with agent_bridge(state)`, under `inspect eval --model mockllm/model`, returned the mock model's output with exactly one Inspect model event; no network, no credentials beyond a placeholder `GOOGLE_API_KEY`, which the Gemini client needs at construction. Two limits: the bridge rejects the streaming entry point (`:streamGenerateContent`), so an ADK run with `StreamingMode.SSE` cannot be bridged; and the spike exercised no tool round trip under a real model. To run an existing agent without editing its module, build it through a factory that takes the model (`build_agent(model=...)`) or, where the module exposes only `root_agent`, derive a copy with the Inspect model (`root_agent.model_copy(update={"model": Gemini(model="inspect")})`, a pydantic copy that skips validation; confirm on the installed version). Use it when a campaign needs Inspect's repeated-trial reducers or agreement metric over an existing ADK agent; the scripted-model Runner tests and ADK's own evaluators remain the primary evidence.

Promptfoo's official ADK 2.x guide takes the other route: the agent is wrapped as an in-process Python provider that calls `runner.run_async`, drains session state and artifacts into one JSON payload for deterministic `contains` and `is-json` assertions, and exports ADK's native spans (`invocation`, `invoke_agent <name>`, `call_llm`, `execute_tool <tool>`, with `gen_ai.tool.name` and the serialized arguments in `gcp.vertex.agent.tool_call_args`) to Promptfoo's OTLP receiver, where `trajectory:tool-used`, `trajectory:tool-args-match` (with `mode: partial`) and `trajectory:tool-sequence` assert on them without a span translator; `trace-span-count` and `trace-error-spans` prove the framework spans were emitted and error-free (promptfoo/promptfoo commit 15bcb0d, MIT, `site/docs/guides/evaluate-google-adk.md` and `site/docs/usage/command-line.md`, read 2026-10-22; npm promptfoo 0.124.1). The guide needs a model and so belongs to tier 2; it is vendor guidance to confirm on the installed version. Exit codes, proven on 2026-10-22 with the `echo` provider and no model: `promptfoo eval` exits 100 when at least one test fails or the pass rate is below `PROMPTFOO_PASS_RATE_THRESHOLD`, 0 when every test passes or the rate clears the threshold (one failing test of two with the threshold at 40 exited 0), and 1 for any other error; the GitHub action adds `repeat` with `repeat-min-pass` (each test run `n` times, at least `m` passes) and `fail-on-threshold` for a suite-level percentage, and shares results only when a share key is configured. The pieces the
paragraph above leaves to the implementer, read in the same docs
(`site/docs/tracing.md`) and, where marked, in a trial's reading of the
installed 0.124.1 bundle on 2026-10-23: the Python provider is
`call_api(prompt, options, context)` and receives the test's W3C context as
`context["traceparent"]`, which the provider makes the parent of its own
span so ADK's child spans share the trace; the receiver is enabled with
`tracing: {enabled: true, failOnReceiverStartFailure: true, otlp: {http:
{enabled: true}}}` and listens on `127.0.0.1:4318/v1/traces`;
`redactAttributes` under `otlp.http` replaces matched attribute values
before storage, which is how `gcp.vertex.agent.llm_request` and
`llm_response` stay out of Promptfoo while tool arguments stay in. Those
arguments sit under ADK's content gate
(`ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS`, see `adk-agent-observability`), so
the job sets it on for this run or the args assertion fails silently; the
args matcher reads `gen_ai.tool.name` and, for arguments, any attribute key
containing `args` as a fallback rather than the ADK key by name (trial
reading, confirm on the installed version). Return the drained payload as
a JSON string in `output`. Span names on google-adk 2.12.0 (installed
package, read 2026-10-23): `invocation`, `invoke_agent <name>`,
`execute_tool <tool>`, and for the model call `generate_content <model>`
from `telemetry/tracing.py` beside a legacy `call_llm` span started in
`flows/llm_flows/core/_model_call.py`; the telemetry schema is selected by
`ADK_TELEMETRY_SCHEMA_VERSION_OPT_IN` (1 legacy, 2 convention-aligned), so
the job pins it and the first live trace settles which model span to
assert on. Two gate traps: an empty suite exits 0 because the pass rate is
undefined, and errored rows count as failures, so the job's reader counts
rows (cases times repeat), refuses error rows and missing assertion types,
and maps to the four outcomes; `check_eval_results.py` reads ADK's CSV, not
Promptfoo's JSON.

## Budget a representative remote canary

When remote evidence is needed, include the actual generated schemas and media
shape in the exact approved account/model/route envelope. Reserve its sends,
retries, output and deadline alongside the cohort, with a declared failure gate.
Use existing authorization within scope. A canary rejection stops the conditional
cohort; diagnose the request rather than silently switching routes. For a fixed
already-approved cohort, preserve its declared protocol.

Check parsing, required slots, finish/truncation status and actual usage as well as
HTTP success. Retain unresolved charges on a missing receipt. A tiny JSON answer
or another provider's success is not evidence for the dynamic request being tested.

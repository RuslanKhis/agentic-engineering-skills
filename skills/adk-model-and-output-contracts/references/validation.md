# Validate the contract

Use the target's existing test runner and interpreter. Keep doubles at the model boundary (a scripted `BaseLlm` subclass, or a `before_model_callback` that short-circuits) so that the real `LlmAgent`, flow processors and save path run. Fail closed on unexpected network calls.

## Output contract and repair

- **Invalid JSON.** The scripted model returns prose. Assert the explicit failure shape in `state[output_key]` (callback placement) or the caught exception and the failure outcome at the caller (re-invocation placement), and that attempts equal the configured budget plus one, no more.
- **Fenced JSON.** The scripted model returns ```` ```json {...} ``` ````. On 2.8.0 assert the save succeeds without a repair attempt; the fence is stripped by ADK. Also test a fence with trailing prose; it is not stripped, and the repair loop must handle it.
- **Schema-valid wrong data.** The scripted model returns a valid `Decision` with a `selected_ids` entry that does not exist. Assert code-side validation rejects it and counts it as wrong-valid-schema, separately from schema validity.
- **Nulls.** A refusal with `None` payload fields saves as a dict without those keys (`exclude_none=True`); consumers read them as absent. If a provider-facing required list is used, assert the serialised request's `required` contains every field while the runtime model stays lenient.
- **Finish reasons.** A scripted response with `finish_reason = MAX_TOKENS` and truncated text yields the failure outcome without a repair attempt; `MALFORMED_FUNCTION_CALL` reaches `ReflectAndRetryModelPlugin` when installed and is counted there.
- **Determinism.** Run the suite twice; attempt counters live in `temp:` state or the caller and reset per invocation.

## Schema with tools

- Capture `llm_request.config` in a `before_model_callback` and assert, per backend variant, that the native path sets `response_schema` and `response_mime_type` and that the workaround path adds `set_model_response` to the tools. Toggle `GOOGLE_GENAI_USE_ENTERPRISE` in the test process environment (restore it in `finally`) and run with a scripted model.
- With a formatting sub-agent, assert the tool-using agent's output reaches the formatter as text and that the formatter has no tools and the schema.
- When `scripts/check_response_schema.py` reports unsupported keywords, add a test that generates the schema from the Pydantic model and asserts the finding list is empty, so a future annotation change is caught.

## Model and settings

- Assert the serialised request carries the intended `thinking_config` (and only one), temperature (unset, or the measured value with a comment), and `max_output_tokens`. A `BuiltInPlanner` plus `generate_content_config.thinking_config` must trigger the construction warning in a test using `warnings.catch_warnings`.
- Assert the resolved model ID (`LlmResponse.model_version` from a recorded run, or the request's `model`) equals the intended explicit version, not an alias.
- On 2.8.0 assert that `LlmAgent(..., generate_content_config=types.GenerateContentConfig(response_schema=...))` raises `ValueError`, so the misplacement cannot return silently.

## Development-set comparison

Hand the comparison to adk-agent-evaluation (two-stage escalation, calibrated judge, holdout untouched). Report per model and settings version:

| Metric | Definition |
| --- | --- |
| Schema validity | Parsed and validated on the first attempt; repaired responses counted separately |
| Answer accuracy | Decision matches the label |
| Executable or actionable accuracy | Code could act on it: identifiers resolve, required fields present, policy checks pass |
| Wrong-valid-schema | Valid and actionable but wrong |

Also record finish reason distribution, thought tokens and output tokens, and attempts. Percentages without case IDs hide which category moved.

## Failover

- A scripted transport raising a 429 on the first model and succeeding on the second (2.9.0+ `FallbackModel`, or the application-level loop on 2.8.0) yields one answer and a record naming the model that answered. A 400 propagates without failover. A streaming failure after the first chunk propagates.
- Retry and failover do not both act on one error: count provider attempts.

## Live checks

A live check needs an approved project, backend, model, location, request count and cost ceiling. Record `model_version`, finish reasons, thought tokens and the four metrics on the approved sample. One live afternoon does not establish availability, latency or quota behaviour; say so in the report.

## Completion report

| Evidence | Supports |
| --- | --- |
| Source inspection and the two helpers | Shape of configuration and schema; no runtime guarantee |
| Scripted-model tests | Save path, repair loop, path selection and config serialisation under the fixture contract |
| Development-set run (adk-agent-evaluation) | Measured quality of a model and settings version on labelled cases |
| Approved live check | Only the observed model, backend, version and sample |
| Production principle | A requirement without a test in this change |

List unverified items explicitly: unresolved runtime model strings, backend not determinable from code, pinned version differing from 2.8.0, lifecycle table age, and any claim about provider acceptance of a schema that was not captured on the wire.

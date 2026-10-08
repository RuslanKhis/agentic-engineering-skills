# Validate the output and repair it within a budget

Read this when a structured output arrives as prose, fenced JSON, invalid data or schema-valid wrong data. The facts below were verified in google-adk **2.8.0** source on 2026-10-06; recheck them in the target's pinned version.

## Know the 2.8.0 save path

`LlmAgent.__maybe_save_output_to_state` (in `agents/llm_agent.py`) runs for each event the agent yields:

- Only events authored by this agent, with `output_key` set, in a mode other than `task`, that satisfy `event.is_final_response()` and contain at least one non-thought text part are considered. `is_final_response()` is false for events carrying function calls or responses, partial events and trailing code-execution results.
- The text parts are joined. With `output_schema` set, a whitespace-only result (the empty final chunk of a stream) is skipped; otherwise `validate_schema(output_schema, result)` runs and the returned value is written to `event.actions.state_delta[output_key]`.
- Streaming accumulation of `output_key` text (`__maybe_accumulate_streaming_output`) is disabled when `output_schema` is set.

`validate_schema` (in `utils/_schema_utils.py`):

- First strips a Markdown code fence that wraps the **entire** payload (`re.fullmatch(r"```\w*\s*(.*?)\s*```", text.strip(), re.DOTALL)`). Added in 2.6.0; 2.10.0 rewrote it to avoid cubic backtracking. Text before or after the fence, or two fences, is not repaired.
- For a `BaseModel` schema returns `model_validate_json(text).model_dump(exclude_none=True)`, a dict. For `list[BaseModel]` the same per item. For other schema types (`dict`, `list[str]`, `types.Schema`) it returns `safe_json_loads(text)` with no Pydantic validation.
- With a Pydantic model or `list[BaseModel]` schema, both malformed JSON and a field mismatch raise Pydantic's `ValidationError` (`model_validate_json` and `TypeAdapter.validate_json` parse and validate in one step). With any other schema (`dict`, `list[str]`, a `types.Schema`), malformed JSON raises `ValueError` from `safe_json_loads`. Nothing in 2.8.0 catches either on this path, so the exception propagates out of the agent run. Code that awaits `Runner.run_async` sees the exception; the event is not saved.

The ADK documentation (adk-docs `agents/llm-agents.md`, fetched 2026-10-06) says the parsed dict is stored in Python; the Java and Kotlin runtimes log and store the raw string instead. Treat the raise as the Python contract.

## Map finish reasons before parsing

`LlmResponse.create` (in `models/llm_response.py`) builds a normal response when the candidate has content parts or `finish_reason == STOP`. A candidate with no parts and another finish reason becomes a response with `error_code = finish_reason` and `error_message = finish_message`; a blocked prompt becomes `error_code = block_reason`. Check `finish_reason` and `error_code` before parsing text:

| Observation | Meaning | Action |
| --- | --- | --- |
| `MAX_TOKENS` with truncated JSON | Thinking plus output exceeded `max_output_tokens` | Raise the limit or lower thinking; do not retry unchanged |
| `MALFORMED_FUNCTION_CALL` | Model emitted a broken tool call | `ReflectAndRetryModelPlugin` scope (below) |
| `SAFETY`, `RECITATION`, `PROHIBITED_CONTENT` | Provider refused | Explicit failure outcome; no repair loop |
| `STOP` with invalid JSON | Contract failure | Repair loop |
| `STOP` with valid JSON, wrong content | Wrong-valid-schema | Count it; fix the prompt or model, not the parser |

## Repair within an attempt budget

A repair loop is application code: validate, feed the error back, retry at most N times, then emit the explicit failure shape. Pydantic AI's `output_validator` plus `ModelRetry` is the reference design (https://pydantic.dev/docs/ai/core-concepts/output/, vendor documentation); ADK has no equivalent built in, so build it at a boundary you own.

Two placements work in 2.8.0.

**Inside the agent, with `after_model_callback`.** The callback receives `callback_context` and `llm_response` and may return a replacement `LlmResponse`; plugins run first, then agent callbacks, and the first non-`None` return wins (`flows/llm_flows/base_llm_flow.py`, `_handle_after_model_callback`). It cannot call the model again by itself, so use it to turn an invalid final response into the explicit failure shape, which keeps the save path from raising and leaves a precise record in state:

```python
import json
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_response import LlmResponse
from google.adk.utils._schema_utils import validate_schema  # internal in 2.8.0; pin and test
from google.genai import types
from pydantic import ValidationError

ATTEMPT_KEY = "temp:decision_attempts"

def guard_decision(callback_context: CallbackContext, llm_response: LlmResponse):
    if llm_response.partial or llm_response.error_code or not llm_response.content:
        return None
    text = "".join(p.text or "" for p in llm_response.content.parts if p.text and not p.thought)
    if not text.strip():
        return None
    try:
        validate_schema(Decision, text)
        return None
    except (ValueError, ValidationError) as error:  # ValueError: JSON decode; ValidationError: schema
        attempts = int(callback_context.state.get(ATTEMPT_KEY, 0)) + 1
        callback_context.state[ATTEMPT_KEY] = attempts
        failure = Decision(status="CANNOT_DECIDE", reason=f"invalid model output after {attempts} attempt(s): {type(error).__name__}")
        return LlmResponse(content=types.Content(role="model", parts=[types.Part(text=failure.model_dump_json())]),
                           finish_reason=llm_response.finish_reason, usage_metadata=llm_response.usage_metadata,
                           custom_metadata={"contract_failure": True, "attempts": attempts})
```

`validate_schema` is marked internal; prefer `Decision.model_validate_json` directly when the Pydantic model is known, and keep the fence-stripping behaviour you depend on in your own helper if you need it outside ADK.

**Around the agent, with a bounded re-invocation.** The caller that owns the `Runner` checks `state[output_key]` or the custom metadata above; on contract failure it sends one more user turn containing the validation error and the instruction to answer again in the schema, up to the budget, then stops with the failure outcome. This is the only placement that produces a genuine retry in 2.8.0. Count attempts per invocation in `temp:` state or in the caller; never in module globals. Bounded loop orchestration inside ADK belongs to adk-workflow-design.

Rules that hold for both placements:

- The budget is small (two or three), fixed, and visible in the report.
- The failure outcome is a valid instance of the schema, so every consumer handles exactly one shape.
- A retry carries the validation message verbatim; a retry that changes the model or thinking level is a different experiment and is logged as one.
- Prose instead of JSON is usually the workaround path with tools ([output schema and tools](output-schema-and-tools.md)) or a missing output instruction, not a parser problem. Fix the cause before adding repair attempts.

## Count wrong-valid-schema separately

A response that validates and is wrong is the expensive failure, because nothing downstream notices. Report four numbers per run, following "The Constraint Tax" (arXiv 2605.26128, independent evidence): schema validity (parsed and validated), answer accuracy (the decision matches the label), executable or actionable accuracy (code could act on it, for example every `selected_ids` entry exists), and wrong-valid-schema (valid, actionable, wrong). A repair loop can only move the first number; the other three belong to the prompt, model and thinking settings, measured with adk-agent-evaluation's development set.

## Know what ReflectAndRetryModelPlugin covers

`ReflectAndRetryModelPlugin` (in `plugins/_reflect_retry_model_plugin.py`, added 2.6.0, present in 2.8.0) takes `max_retries=3` and `on_model_errors`, defaulting to `[FinishReason.MALFORMED_FUNCTION_CALL]`. It treats a response as an error only when `llm_response.error_code` is set and `finish_reason` is in that list, then injects reflection guidance and retries, raising or returning guidance when the budget is exhausted. A Pydantic failure on `output_key` save, or valid JSON with wrong content, never sets `error_code`, so the plugin does not react to it. Use it for malformed tool calls; use the repair loop above for contract failures.

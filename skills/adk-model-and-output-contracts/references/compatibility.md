# Compatibility and evidence boundaries

Read this before relying on any version-dependent behaviour in this skill. The pinned reference is google-adk **2.8.0** (tag `v2.8.0`, released 2026-08-25), whose source was read on 2026-10-06. Later behaviour comes from the adk-python main branch at 2.11.0 and its CHANGELOG. Keep the target's pins; a version decision is a separate request.

## Verified in 2.8.0 source

| Surface | Behaviour | File |
| --- | --- | --- |
| `LlmAgent.output_schema` | Accepts a `BaseModel` class, `list[BaseModel]`, `list[primitive]`, `dict` or `types.Schema` (`SchemaType = types.SchemaUnion`) | `agents/llm_agent.py`, `utils/_schema_utils.py` |
| `LlmRequest.set_output_schema` | Sets `config.response_schema` and `config.response_mime_type = "application/json"` | `models/llm_request.py` |
| `validate_generate_content_config` | `ValueError` for `tools`, `system_instruction`, `response_schema`, and `http_options.base_url` | `agents/llm_agent.py` |
| Thinking precedence | `UserWarning` at construction when both configs exist; planner overwrites at request time with a debug log | `agents/llm_agent.py`, `planners/built_in_planner.py` |
| Schema with tools | Native only when `model.capabilities.output_schema_and_tools`; Gemini reports true only on the `VERTEX_AI` variant; `LiteLlm` reports true; task mode skips | `flows/llm_flows/basic.py`, `models/_capabilities.py`, `models/lite_llm.py` |
| Workaround | `SetModelResponseTool` plus instruction; Pydantic errors returned to the model as an `error` dict | `flows/llm_flows/_output_schema_processor.py`, `tools/set_model_response_tool.py` |
| Output save | Final non-partial text event only; whitespace-only chunk skipped; fence stripped; `model_dump(exclude_none=True)`; exceptions propagate | `agents/llm_agent.py`, `utils/_schema_utils.py` |
| Finish reasons | Candidate without parts and not `STOP` becomes `error_code = finish_reason` | `models/llm_response.py` |
| `after_model_callback` | Plugins first, then agent callbacks; first non-`None` `LlmResponse` replaces the response | `flows/llm_flows/base_llm_flow.py` |
| `ReflectAndRetryModelPlugin` | `max_retries=3`, `on_model_errors=[MALFORMED_FUNCTION_CALL]`, reacts only when `error_code` is set | `plugins/_reflect_retry_model_plugin.py` |
| Backend variant | `GOOGLE_GENAI_USE_ENTERPRISE` read first; `GOOGLE_GENAI_USE_VERTEXAI` honoured with `DeprecationWarning` | `utils/env_utils.py`, `utils/variant_utils.py` |
| `Gemini` options | `retry_options`, `client_kwargs`, `api_version`, `GOOGLE_GENAI_API_VERSION`; Vertex model paths force enterprise mode; 429 wrapped in `_ResourceExhaustedError` | `models/google_llm.py` |
| Default model | `LlmAgent.DEFAULT_MODEL = "gemini-3.5-flash"` | `agents/llm_agent.py` |
| Registry | `LLMRegistry.resolve` matches patterns; unknown `provider/model` raises with a LiteLLM install hint | `models/registry.py` |
| Dependencies | `google-genai>=2.19,<3`; extensions `litellm>=1.84`, `anthropic>=0.78`, `openai>=2.20,<3` | `pyproject.toml` |
| Absent | `FallbackModel`, `ADK_MAX_TOOL_ROUNDS`, `MAX_TOOL_ROUNDS_EXCEEDED` | not in 2.8.0 |

## Version table from the CHANGELOG (2.6.0 to 2.11.0)

| Version | Date | Change relevant to this skill |
| --- | --- | --- |
| 2.6.0 | 2026-07-29 | `ReflectAndRetryModelPlugin` added; code fences stripped before `output_schema` validation; CHANGELOG entry "reject base_url and extra_body in generate_content_config" (the 2.8.0 validator checks `http_options.base_url`; no `extra_body` check was found in that validator) |
| 2.7.0 | 2026-08-13 | Models declare their own capabilities for schema with tools; defaulted `output_schema` fields no longer marked required; thought signature parts kept in history |
| 2.8.0 | 2026-08-25 | Field descriptions preserved in the `set_model_response` schema; credentials redacted from `generate_content_config.http_options` debug logs |
| 2.9.0 | 2026-09-10 | `FallbackModel` added; misplaced generation kwargs redirected to `generate_content_config`; Gemini 3 thought signatures preserved in interaction history; LiteLLM: malformed tool-call JSON guarded, real finish reason from streams, `anyOf` and aliases preserved, `seed` forwarded |
| 2.10.0 | 2026-09-24 | `_strip_json_code_fence` rewritten to prevent cubic backtracking; `OpenAIResponsesLlm` ignores `thinking_config` with a warning; tool output schema forwarded on the LiteLLM path |
| 2.11.0 | 2026-10-01 | Single-turn structured output preserved; `ADK_MAX_TOOL_ROUNDS` bound on the workaround path (main branch source) |

Behaviour attributed to the main branch (per-provider LiteLLM capabilities, `ADK_MAX_TOOL_ROUNDS`, `FallbackModel` internals) was read in main at 2.11.0 and is not a statement about 2.8.0.

## Vendor pages used, with dates

| Page | Date on page | Used for |
| --- | --- | --- |
| Gemini structured output | 2026-09-23 | Keyword subset, limitations, tools versus schema |
| Gemini models | 2026-10-01 | Current IDs and statuses |
| Gemini deprecations | 2026-10-01 | Shutdown dates, 2.5 limited access, new-project advice |
| Gemini thinking | 2026-09-25 | `thinking_level` defaults and levels, `max_output_tokens` |
| Gemini 3 developer guide | 2026-09-23 | `thinking_level` versus `thinking_budget`, temperature 1.0 |
| Vertex controlled output | 2026-10-05 | 400 on complex schemas and remedies, property ordering |
| Vertex thinking | 2026-10-05 | `thinking_budget` deprecated on Gemini 3, `MINIMAL` and thought signatures |
| Vertex model versions | 2026-10-05 | 12-month rule, retirement dates including 2.5 on 2026-10-20 |
| Vertex locations | 2026-10-05 | Global endpoint availability and residency caveat |
| adk-docs `agents/llm-agents.md`, `get-started/google-cloud.md`, LiteLLM page | fetched 2026-10-06 | Schema-with-tools warning, env variable rename, Express Mode, LiteLLM advisory |

## Not verified here

- Live behaviour of any model, backend or endpoint. Nothing in this skill ran a model call.
- The exact google-genai version a target resolves and whether its `GenerateContentConfig` serialises `response_schema` or `response_json_schema` on the wire for that version. The request-capture test in [output schema and tools](output-schema-and-tools.md) is the check.
- Community issue reports cited by number (#3969, #3025, #3543, #3705, forum threads). They identify symptoms to test for, not facts about the target.
- The three research papers' results on the target's task. They motivate "reason free, constrain late" and the four-metric report; the target's development set decides.
- Pydantic AI's `output_validator` behaviour; it is cited as a design reference from its documentation, not as something runnable in ADK.

# Output schema together with tools

Read this when an agent has both `tools` and `output_schema`, or when structured output arrives as prose only on some deployments. Verified in google-adk **2.8.0** source on 2026-10-06 unless a later version is named.

## The backend decides the mechanism

`flows/llm_flows/basic.py` sets the schema on the request only when the agent has no tools or `model.capabilities.output_schema_and_tools` is true (and the agent is not in `task` mode). `Gemini.capabilities` returns `gemini_output_schema_and_tools(model)` from `models/_capabilities.py`, which is true if and only if `get_google_llm_variant()` is `VERTEX_AI` **and** the model name starts with `gemini-`. The variant is `VERTEX_AI` when `GOOGLE_GENAI_USE_ENTERPRISE` is enabled (or the deprecated `GOOGLE_GENAI_USE_VERTEXAI`, which warns), otherwise `GEMINI_API`.

| Backend and model | Path in 2.8.0 | What the request carries |
| --- | --- | --- |
| Vertex / enterprise mode, Gemini model, tools present | Native | `config.response_schema`, `response_mime_type = application/json`, plus the agent's tools |
| API key (AI Studio or Express Mode), any Gemini model, tools present | Workaround | Tools plus an extra `set_model_response` tool and an appended instruction; no response schema |
| Any backend, no tools | Native | `config.response_schema` and MIME type |
| `LiteLlm`, tools present | Native (declared) | `LiteLlm.capabilities` returns true; the provider adapter reconciles schema and tools |
| Any backend, `mode="task"` | Neither | Structured output is collected through the `finish_task` tool schema; `output_key` text saving is skipped |

The documentation (adk-docs `agents/llm-agents.md`, fetched 2026-10-06) says native support "is only supported by specific models, including Gemini 3.0" and that ADK "falls back to a `set_model_response` function tool ... which may not work reliably", recommending "sub-agents that handle output formatting separately". The code gates on backend, not on model generation: an API-key deployment of `gemini-3.8-flash` takes the workaround path. State both when reviewing, and test which path ran.

## The workaround path in detail

`flows/llm_flows/_output_schema_processor.py` (2.8.0) appends `SetModelResponseTool(agent.output_schema)` and the instruction "you must provide your final response using the set_model_response tool ... always call set_model_response with your final answer in the specified schema format". `tools/set_model_response_tool.py` validates the call's arguments with Pydantic and, on `ValidationError`, returns a dict with an `error` message telling the model to call again with corrected fields, so the model gets one natural retry per tool round. A successful call is turned into a final model event whose text is the JSON (`create_final_model_response_event`), which then goes through the normal `output_key` save. Since 2.8.0 field descriptions from the Pydantic model are preserved in that tool's schema (CHANGELOG, "preserve field descriptions in set_model_response schema").

The main branch (2.11.0, `flows/llm_flows/prompt/_schema.py`) adds a bound that 2.8.0 lacks: `ADK_MAX_TOOL_ROUNDS` (default 25) limits consecutive tool rounds in one turn, forces `FunctionCallingConfig(mode=ANY, allowed_function_names=["set_model_response"])` on round N-1 and ends the invocation with an error event `MAX_TOOL_ROUNDS_EXCEEDED` on round N. On 2.8.0 the only comparable bound is `RunConfig.max_llm_calls`, which counts all model calls in the invocation; adk-operational-guardrails owns that policy.

When the model answers in prose instead of calling the tool, the final text reaches `validate_schema` and raises ([validation and repair](validation-and-repair.md)). That is the failure the documentation warns about, and the reason a tool-free formatting sub-agent is the dependable design for API-key deployments.

## Choose the design

1. **Vertex backend available.** Keep tools and `output_schema` on one agent; verify the native path with the request-capture test below. Record the backend in the deployment contract, because moving the same code to an API key silently changes the mechanism.
2. **API-key backend.** Split the work: a tool-using agent returns text, and a second `LlmAgent` with `output_schema`, `output_key` and no tools formats it (an `AgentTool` with `mode="single_turn"`, or a sequential workflow; adk-workflow-design owns the wiring). The formatting agent's prompt is small and its schema is minimal.
3. **LiteLLM.** The 2.8.0 capability is declared true for every `LiteLlm`; the main branch (2.11.0) resolves it per provider (`LiteLlm._resolve_capabilities`: false for Gemini through LiteLLM unless the provider is `vertex_ai`, false for Claude routes, otherwise `litellm.supports_response_schema`). An OpenAI-compatible transport does not establish provider schema enforcement; adk-agent-evaluation's provider-compatibility reference explains how to capture what is actually sent.

## Test which path ran

Capture the request before it leaves ADK:

```python
captured = {}

def capture(callback_context, llm_request):
    config = llm_request.config
    captured["response_schema"] = config.response_schema is not None
    captured["response_mime_type"] = config.response_mime_type
    captured["tool_names"] = sorted(
        decl.name for tool in (config.tools or []) for decl in (tool.function_declarations or []))
    return None

agent = LlmAgent(..., before_model_callback=capture)
```

Assertions for the native path: `response_schema` is true, the MIME type is `application/json`, and `tool_names` holds only the agent's tools. For the workaround path: `response_schema` is false and `tool_names` contains `set_model_response`. Run the test twice, once with `GOOGLE_GENAI_USE_ENTERPRISE` enabled and once without, with a scripted model so no provider call happens; the two results must differ exactly as the table says. The `before_model_callback` sees the request after `basic.py` and the schema processor have run, so it observes the final decision.

For 2.8.0, also assert that `llm_request.config.response_schema` is the field that carries the schema; a later ADK or google-genai may move to `response_json_schema`, and the assertion is how you will notice.

## Known reports

Community issues (GitHub google/adk-python, not reproduced for this skill): #3969 (December 2025) reports `output_schema` plus `tools` plus `output_key` producing prose and a `ValidationError` on save, with the API-key workaround path as the root cause and a Vertex backend or a formatting sub-agent as mitigations; #3025 reports `VertexAiSearchTool` plus `output_schema` rejected with "Multiple tools are supported only when they are all search tools", worked around with an `AgentTool`; #3543 reports Vertex validating function signatures more strictly than the Gemini API. Treat these as prompts to run the capture test on the target, not as facts about it.

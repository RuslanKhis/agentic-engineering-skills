# Failover, endpoints and other providers

Read this when 429 or 5xx errors interrupt an agent, when a second model should take over, or when a non-Gemini provider is in use. ADK behaviour was verified in **2.8.0** source and the main branch (2.11.0) on 2026-10-06; version labels matter here.

## Layer the resilience stack

| Layer | Mechanism | Version | Scope |
| --- | --- | --- | --- |
| Same-model retry | `Gemini(retry_options=types.HttpRetryOptions(initial_delay=1, attempts=2))` or `generate_content_config.http_options.retry_options` | 2.8.0 (`models/google_llm.py` documents the example) | One request, same model; ADK wraps a 429 `ClientError` in `_ResourceExhaustedError` with a link to the documentation's 429 section |
| Malformed tool call retry | `ReflectAndRetryModelPlugin(max_retries=3)` | 2.6.0+ | Finish reasons listed in `on_model_errors`, default `MALFORMED_FUNCTION_CALL`; not schema validation |
| Cross-model failover | `FallbackModel(models=[...])` | **2.9.0+**, experimental | Status codes 429, 500, 502, 503, 504 by default; each model tried once |
| Last resort | `LlmAgent.on_model_error_callback` | 2.8.0 | Turn a final failure into an explicit outcome |
| Capacity | Global endpoint, provisioned throughput | Vertex configuration | Outside the agent code; needs approval |

A retry layer and a failover layer both reacting to the same error pay twice; `FallbackModel`'s docstring says retrying a single model belongs to that model's own `retry_options`.

## FallbackModel is 2.9.0, not 2.8.0

`FallbackModel` does not exist in 2.8.0 (`models/` has no such module). The main branch (`models/_fallback_model.py`, added 2.9.0 on 2026-09-10, marked `@experimental`) defines it as:

- `models: list[str | BaseLlm]` tried in order, each exactly once; the first entry supplies `FallbackModel.model`.
- Failover only on `retriable_status_codes` (default `{429, 500, 502, 503, 504}`; 408 deliberately excluded because a timeout may have been processed). The status comes from `google.genai.errors.APIError.code`, a `status_code` attribute (litellm, openai, anthropic) or `response.status_code`; litellm errors that hard-code a fake 500 are recognised and not failed over.
- "Once a model has yielded its first response the turn belongs to it": a streaming failure after the first chunk propagates instead of splicing a second model's output. Live connections follow the same rule at the connection boundary.
- It does not route by cost, task or quality; the final failure propagates to `on_model_error_callback`.

On 2.8.0 the choices are: request a version decision to move to 2.9.x or later, or implement failover at the boundary that owns the `Runner` (catch the provider error, rebuild the agent with the second model, replay the same turn once). Record in the report which option was taken and that the fallback model's quality was measured on the development set; a backup that answers differently is a quality decision, not just an availability one.

## Decide on the global endpoint

The Vertex locations page (https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations, page dated 2026-10-05, vendor documentation) says a global endpoint "can improve overall availability and reduce resource exhausted (429) errors", that endpoints "don't guarantee data residency or in-region ML processing", and that some capabilities are unavailable on the global endpoint. Pin the location in code rather than relying on an environment variable: `Gemini(model=..., client_kwargs={"enterprise": True, "location": "global"})` passes through to `google.genai.Client` in 2.8.0, and the class docstring shows the subclass alternative. API version defaults to `v1beta1` on Vertex and is overridable with `Gemini(api_version=...)` or `GOOGLE_GENAI_API_VERSION`.

Changing location, quota tier or provisioned throughput is a consequential cloud change: present project, location, models and expected cost, obtain approval, and keep data residency requirements ahead of 429 relief. Hosting-level latency work belongs to optimise-adk-on-google-cloud; budget shutdown policy to adk-operational-guardrails.

## Use LiteLLM with its caveats

- ADK 2.8.0 pins `litellm>=1.84` (`pyproject.toml`). The ADK documentation's LiteLLM page carries a security advisory: unauthorized code was identified in LiteLLM 1.82.7 and 1.82.8 (2026-03-24); if either was installed during that window, rotate all secrets that environment could read.
- `LLMRegistry.resolve` matches model strings against registered patterns; a `provider/model` string resolves to `LiteLlm` when the package is installed and otherwise raises with an install hint (`models/registry.py`).
- Adapter fixes after 2.8.0 that affect contracts: 2.9.0 "guard malformed tool call argument JSON in LiteLlm response parsing", "report the real finish reason from a LiteLlm stream", "preserve anyOf and camelCase aliases in LiteLLM tool schemas", "forward GenerateContentConfig.seed to LiteLLM"; 2.10.0 "forward tool output schema on the LiteLLM path", "report malformed tool-call arguments instead of raising". A 2.8.0 project using LiteLLM with structured output or tool schemas should test those exact shapes rather than assume them.
- 2.8.0 declares `output_schema_and_tools=True` for every `LiteLlm`; the main branch resolves it per provider ([output schema and tools](output-schema-and-tools.md)). An OpenAI-compatible transport does not establish provider schema enforcement; adk-agent-evaluation's provider-compatibility reference shows how to capture the request after adapter conversion.

## Report what you observed

For every error path, record the status code or finish reason, the model that answered, the layer that acted and the attempt count. "Fewer 429s" after a change is a claim only when the same request mix and time window are compared; quota is shared and time-varying, so a single afternoon proves little. Community reports of persistent 429s on preview models with global-only availability (Google developer forum, February 2026, not reproduced here) are a reason to measure under load before promising capacity.

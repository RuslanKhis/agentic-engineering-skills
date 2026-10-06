# Sources

Every claim in this skill is one of: **source** (read in a local checkout of google/adk-python on 2026-10-06), **vendor** (Google or another provider's documentation, with the date printed on the page), **evidence** (independent research), or **community** (issue or forum reports, not reproduced). Where the skill reports no verification, [compatibility](compatibility.md) says so.

## ADK source and changelog

| Reference | Type | Notes |
| --- | --- | --- |
| google/adk-python tag `v2.8.0` (2026-08-25): `agents/llm_agent.py`, `models/llm_request.py`, `models/llm_response.py`, `models/_capabilities.py`, `models/google_llm.py`, `models/lite_llm.py`, `models/registry.py`, `flows/llm_flows/basic.py`, `flows/llm_flows/_output_schema_processor.py`, `flows/llm_flows/base_llm_flow.py`, `tools/set_model_response_tool.py`, `utils/_schema_utils.py`, `utils/env_utils.py`, `utils/variant_utils.py`, `planners/built_in_planner.py`, `plugins/_reflect_retry_model_plugin.py`, `pyproject.toml` | source | Pinned behaviour |
| google/adk-python main at 2.11.0 (2026-10-01): `models/_fallback_model.py`, `models/lite_llm.py` (`_resolve_capabilities`), `flows/llm_flows/prompt/_schema.py`, `agents/llm_agent.py` (misplaced kwargs validator), `CHANGELOG.md` | source | Later behaviour, labelled by version |
| google/adk-docs: `docs/agents/llm-agents.md`, `docs/get-started/google-cloud.md`, LiteLLM model page | vendor, fetched 2026-10-06 | Schema-with-tools warning and sub-agent advice; `GOOGLE_GENAI_USE_ENTERPRISE` rename and Express Mode; LiteLLM 1.82.7/1.82.8 advisory (2026-03-24) |

## Google model and API documentation

| URL | Page date | Used for |
| --- | --- | --- |
| https://ai.google.dev/gemini-api/docs/structured-output | 2026-09-23 | Supported keywords, limitations, structured outputs versus function calling |
| https://ai.google.dev/gemini-api/docs/models | 2026-10-01 | Current model IDs and statuses |
| https://ai.google.dev/gemini-api/docs/deprecations | 2026-10-01 | Shutdown dates, limited 2.5 access, new-project recommendation |
| https://ai.google.dev/gemini-api/docs/thinking | 2026-09-25 | `thinking_level` defaults and levels, token limit behaviour |
| https://ai.google.dev/gemini-api/docs/gemini-3 | 2026-09-23 | `thinking_level` versus `thinking_budget`, temperature 1.0, concise prompts |
| https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/control-generated-output | 2026-10-05 | 400 on complex schemas, remedies, property ordering |
| https://docs.cloud.google.com/vertex-ai/generative-ai/docs/thinking | 2026-10-05 | `thinking_budget` deprecation on Gemini 3, `MINIMAL` and thought signatures |
| https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions | 2026-10-05 | 12-month availability, retirement dates |
| https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations | 2026-10-05 | Global endpoint availability and residency caveat |

## Other vendor documentation

| URL | Fetched | Used for |
| --- | --- | --- |
| https://developers.openai.com/api/docs/guides/structured-outputs | 2026-10-06 | Numeric schema limits as a yardstick; function calling versus response format |
| https://pydantic.dev/docs/ai/core-concepts/output/ | 2026-10-06 | `output_validator` and `ModelRetry` as the reference repair-loop design |

## Independent evidence

| Work | Identifier | Finding used |
| --- | --- | --- |
| "Let Me Speak Freely? A Study on the Impact of Format Restrictions on Performance of Large Language Models" | arXiv 2408.02442, EMNLP Industry 2024 | Stricter format constraints degrade reasoning |
| "The Format Tax" | arXiv 2604.03616, 2026-04 | Degradation enters at the prompt; decouple reasoning from formatting |
| "The Constraint Tax" | arXiv 2605.26128, 2026-05-20 | Validity up, accuracy down under hard schema decoding; report four metrics; reason free, constrain late |
| FrugalGPT (Chen, Zaharia, Zou) | arXiv 2305.05176, 2023 | Cascade cost reduction conditional on a quality threshold and labelled data |
| RouteLLM (Ong et al.) | arXiv 2406.18665, 2024, updated 2025 | Trained router cost reduction at matched quality |

## Community reports (not reproduced)

google/adk-python issues #3969, #3025, #3543, #3705; Google developer forum threads on persistent 429s for global-only preview models (February 2026), missing thought summaries with `thinking_budget` (April 2026) and frequent `MALFORMED_FUNCTION_CALL` finish reasons. They are listed as symptoms to test for on the target.

## Repository references

Sibling skills are cited by name: adk-agent-evaluation (development set, two-stage escalation, provider compatibility), adk-sql-agent-engineering (provider versus runtime schema split), adk-operational-guardrails (degradation and budgets), adk-workflow-design (loops and sub-agent wiring), optimise-adk-on-google-cloud (hosting latency), and the siblings in preparation adk-agent-instructions and adk-tool-interface-design.

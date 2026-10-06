# Configure thinking and sampling

Read this when setting `thinking_config`, `temperature` or `max_output_tokens`, or when a Gemini 3 model behaves differently after a version change. Vendor statements carry their page dates; ADK behaviour was verified in **2.8.0** source on 2026-10-06.

## Use thinking_level on Gemini 3

The Gemini thinking page (https://ai.google.dev/gemini-api/docs/thinking, page dated 2026-09-25, vendor documentation) gives the defaults and supported levels:

| Model | Default | Supported levels |
| --- | --- | --- |
| `gemini-3.8-flash`, `gemini-3.7-flash` | On (medium) | low, medium, high |
| `gemini-3.6-flash`, `gemini-3.5-flash` | On (medium) | minimal, low, medium, high |
| `gemini-3.5-flash-lite` | On (minimal) | minimal, low, medium, high |
| `gemini-3.1-pro-preview` | On (high) | low, medium, high |
| `gemini-3-flash-preview` | On (high) | minimal, low, medium, high |
| `gemini-2.5-pro`, `gemini-2.5-flash` | On | low, medium, high |
| `gemini-2.5-flash-lite` | Off | low, medium, high |

The page recommends minimal or low thinking for fact retrieval and classification and the default for comparison and reasoning tasks. The Gemini 3 guide (https://ai.google.dev/gemini-api/docs/gemini-3, page dated 2026-09-23) adds: "You cannot use both thinking_level and the legacy thinking_budget parameter in the same request"; `thinking_budget` still works for backward compatibility but `thinking_level` is recommended. The Vertex thinking page (https://docs.cloud.google.com/vertex-ai/generative-ai/docs/thinking, page dated 2026-10-05) is stricter: `thinking_budget` "is deprecated for Gemini 3 and later models" and "can cause intermittent 400: INVALID_ARGUMENT errors"; both parameters together return an error; and `MINIMAL` "requires thought signatures in multi-turn conversations; if omitted, the model returns a 400: INVALID_ARGUMENT error".

Thought signatures are the ADK's responsibility to carry between turns. The CHANGELOG records "preserve Gemini 3 thought signatures in interaction history" in 2.9.0 and "keep thought signature parts in conversation history" in 2.7.0; a multi-turn agent on Gemini 3 with minimal thinking and tool calls should be tested on the pinned version for a 400 after several tool rounds (community report #3705 describes that symptom on an earlier version). The audit flags `thinking_budget` with a 3.x model, `thinking_level` with a 2.5 model and both set together.

## Keep temperature at 1.0 on Gemini 3

The Gemini 3 guide: "For all Gemini 3 models, we strongly recommend keeping the temperature parameter at its default value of 1.0", because lowering it "may lead to unexpected behavior, such as looping or degraded performance". Determinism for a decision contract comes from the schema, the prompt and code-side validation, not from temperature. The audit reports `temperature_below_default_on_gemini_3` as a review finding; a project that has measured a lower temperature on its own development set can keep it and record the measurement. The guide also asks for concise prompts; prompt wording belongs to adk-agent-instructions.

## Set thinking in one place in ADK

Two fields can carry a `ThinkingConfig`:

```python
from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types

agent = LlmAgent(
    name="decider", model="gemini-3.8-flash", instruction=...,
    generate_content_config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="low"),
        max_output_tokens=4096),
)
# or, equivalently for the request:
agent = LlmAgent(name="decider", model="gemini-3.8-flash", instruction=...,
                 planner=BuiltInPlanner(thinking_config=types.ThinkingConfig(thinking_level="low")))
```

`BuiltInPlanner.apply_thinking_config` writes its config onto `llm_request.config.thinking_config`, overwriting any value from `generate_content_config` and logging at debug level (`planners/built_in_planner.py`). `LlmAgent.model_post_init` emits a `UserWarning` at construction when both are set: "The planner's configuration will take precedence." Choose one. The audit reports `thinking_config_planner_precedence` when both appear on one agent. `include_thoughts=True` returns thought summaries as parts marked `thought`; the `output_key` save path ignores thought parts.

Documentation examples that pair `BuiltInPlanner(thinking_config=ThinkingConfig(include_thoughts=True, thinking_budget=1024))` with a `-latest` alias predate Gemini 3; use `thinking_level` and an explicit model ID.

## Size max_output_tokens for thinking plus output

The thinking page: `max_output_tokens` "applies to the combined total of thinking and response tokens". A limit sized for the JSON alone truncates with `finish_reason = MAX_TOKENS` and an unparseable payload. For shorter responses the page recommends lowering `thinking_level` instead of setting a small `max_output_tokens`. Record `usage_metadata.thoughts_token_count` and `candidates_token_count` per run; the ratio tells you where the budget goes. adk-agent-evaluation's quality-iteration reference treats output length as a quality variable for the same reason.

## Place the other sampling knobs correctly

`temperature`, `top_p`, `top_k`, `seed`, `max_output_tokens`, `thinking_config` and `http_options` belong on `generate_content_config`. `generate_content_config` must not carry `tools`, `system_instruction` or `response_schema` (`ValueError` in 2.8.0, with messages pointing at `LlmAgent.tools`, `LlmAgent.instruction` and `LlmAgent.output_schema`), nor a `base_url` in `http_options` (rejected since 2.6.0; transport belongs on the model). From 2.9.0, passing a `GenerateContentConfig` field directly as an `LlmAgent` keyword raises with a message naming `generate_content_config` ("point misplaced generation kwargs at generate_content_config").

Other providers map differently. `OpenAIResponsesLlm` (in `labs`) ignores `thinking_config` with a warning from 2.10.0 and uses an effort setting instead; Anthropic models in ADK map `thinking_budget` to their own thinking parameters (CHANGELOG 1.34.0 and 2.4.0). Verify the adapter for the pinned version before carrying a Gemini thinking config to another provider.

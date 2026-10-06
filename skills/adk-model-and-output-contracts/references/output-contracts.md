# Design the output contract

Read this when writing or reviewing an `output_schema`. The contract is the smallest structure that lets code act safely on the model's decision. Everything the model does not need to decide belongs in code, not in the schema.

## Model decides, code copies

Ask the model for the decision and the evidence it saw; look up everything else. A schema with `status`, `reason` and `selected_ids` is more reliable than one with `status`, `reason`, `customer_name`, `customer_email`, `amount`, `currency`, because the model copies the last four from context and copies imperfectly. Code resolves `selected_ids` against trusted data and fills the rest. The SQL variant of this rule (logical names versus physical paths) belongs to adk-sql-agent-engineering.

Make identifiers the model copies short, stable and present in the prompt. Validate them against the source set in code; a schema cannot express "one of the IDs shown above".

## Stay inside the documented subset

The Gemini structured-output page (https://ai.google.dev/gemini-api/docs/structured-output, page dated 2026-09-23, vendor documentation) lists the supported keywords:

| Where | Supported keywords |
| --- | --- |
| Any schema | `type` (string, number, integer, boolean, object, array, and `"null"` inside a type array), `title`, `description` |
| object | `properties`, `required`, `additionalProperties` |
| string | `enum`, `format` (`date-time`, `date`, `time`) |
| number, integer | `enum`, `minimum`, `maximum` |
| array | `items`, `prefixItems`, `minItems`, `maxItems` |
| Composition | `anyOf`, `$ref` (recursive structures) |

Its stated limitations are "Not all JSON Schema features are supported" and "Very large or deeply nested schemas may be rejected", with no numeric limit. `pattern`, `minLength`, `maxLength`, `oneOf`, `allOf`, `not`, `const`, `patternProperties`, `dependentRequired`, `uniqueItems`, `multipleOf`, `exclusiveMinimum`, `exclusiveMaximum` and `if`/`then`/`else` are outside the list; `scripts/check_response_schema.py` flags them. Pydantic emits several of them from ordinary annotations (`constr(pattern=...)`, `Field(gt=0)`, `Literal` unions become `const` or `enum` depending on version), so check the generated schema rather than the Python class.

The page's Python samples use a `response_format={"type": "text", "mime_type": "application/json", "schema": ...}` shape of the Interactions API. ADK 2.8.0 does not use that shape: `LlmRequest.set_output_schema` sets `config.response_schema` and `config.response_mime_type = "application/json"` on the GenAI `GenerateContentConfig` (verified in `models/llm_request.py`). The `google-genai` type also carries a `response_json_schema` field. Capture the serialised request from the pinned SDK before deciding which field matters for a given problem; do not hand-set either field in `generate_content_config`, which ADK rejects for `response_schema`.

## Shrink before the provider rejects

The Vertex controlled-output page (https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/control-generated-output, page dated 2026-10-05, vendor documentation) states that a complex schema can return `InvalidArgument: 400` and lists the remedies: shorten property and enum names, flatten nested arrays, reduce properties with constraints (numeric bounds, `date-time` formats), reduce optional properties, reduce enum cardinality. It also says the model generates properties in schema order and that a schema example in the prompt must follow the same field order as the schema, with `propertyOrdering` available to fix the order.

OpenAI publishes hard limits for its own structured outputs (5000 properties, 10 nesting levels, 1000 enum values across the schema; https://developers.openai.com/api/docs/guides/structured-outputs, fetched 2026-10-06). Use them only as a conservative yardstick; Google publishes none. The checker's defaults are tighter (100 properties, depth 10, 100 enum values) because a schema that approaches those numbers is already a design smell for a decision contract.

## Give refusal a first-class shape

Every decision contract needs a way to say "no" that is valid JSON. Use a status enum and make payload fields nullable:

```python
from typing import Literal
from pydantic import BaseModel

class Decision(BaseModel):
    status: Literal["APPROVE", "REJECT", "NEEDS_REVIEW", "CANNOT_DECIDE"]
    reason: str
    selected_ids: list[str] = []
    confidence_note: str | None = None
```

Two facts shape this in ADK 2.8.0 (verified in `utils/_schema_utils.py`): the saved value is `model_dump(exclude_none=True)`, so a `None` field disappears from `state[output_key]`; and since 2.7.0 fields with defaults are no longer marked required in the schema ADK sends. Downstream code must therefore treat a missing key as `None` and must not depend on "key present" for a refusal. If the wire schema must still require every key, add them with `json_schema_extra` on a provider-facing subclass and keep the runtime model lenient; adk-sql-agent-engineering shows that split.

Choose one nullable style for the whole schema. Pydantic's `Optional[str]` becomes `anyOf: [{type: string}, {type: null}]`; a raw dict schema may use `type: ["string", "null"]`; the GenAI `Schema` type uses `nullable`. The checker reports mixed styles; mixing them is a maintenance cost, not an error.

## Decide when not to constrain

Constrain the final answer, not the reasoning. Three independent studies measure the cost of format constraints:

- "Let Me Speak Freely?" (arXiv 2408.02442, EMNLP Industry 2024, independent evidence): stricter format constraints produced greater reasoning degradation across several models and tasks.
- "The Format Tax" (arXiv 2604.03616, 2026-04, independent evidence): the degradation enters at the prompt, not at the decoder; recent closed-weight models show little or none; the recommended remedy is to decouple reasoning from formatting, either free-form reasoning followed by reformatting or extended thinking in one call.
- "The Constraint Tax" (arXiv 2605.26128, 2026-05-20, independent evidence, sub-3B models): hard schema decoding reached 100% schema validity while accuracy fell from 19.7% to 11.0%; it recommends reporting schema validity, answer accuracy, executable accuracy and wrong-valid-schema separately and summarises the practice as "reason free, constrain late".

The practical rule for ADK: keep thinking on ([reasoning and sampling](reasoning-and-sampling.md)), ask for a minimal schema, and let the schema wrap a decision the model has already reasoned about. For a task that is mostly prose (a summary, an explanation), return text and extract the few structured fields with a second, cheap, tool-free agent or with code. The evaluation loop that proves the choice belongs to adk-agent-evaluation; this skill supplies the contract and the metrics to report.

## Keep tools and response schemas to their jobs

Function calling asks the application to act; a response schema shapes the final answer. The Gemini page states this split directly ("Formatting the final response" versus "Taking action during conversation") and OpenAI's guide says the same (vendor documentation, both fetched 2026-10-06). Do not build a "return_answer" tool to get structure when the agent has no other tools; use `output_schema`. When the agent has tools and must return structure, read [output schema and tools](output-schema-and-tools.md) first, because the mechanism differs by backend. Tool parameter schemas themselves belong to adk-tool-interface-design.

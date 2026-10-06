# FunctionTool declaration contract (google-adk 2.8.0)

Read this before changing a tool signature or docstring. Every statement below
was checked against the `google-adk` 2.8.0 source on 2026-10-06; version notes
cite the `adk-python` main CHANGELOG of the same date. Inspect the pinned
version in the target project before relying on a later behaviour, and preserve
the pin.

## What the model receives

A `FunctionTool` sends the model one `FunctionDeclaration`: the function name,
one description string and a parameter schema. Nothing else about the Python
function is visible. The declaration is built lazily on the first model request
that includes the tool (`LlmRequest.append_tools` calls `_get_declaration`), so a
schema problem surfaces at the first request, not at `FunctionTool(...)`.

| Element | Source in 2.8.0 | Consequence |
| --- | --- | --- |
| Name | `func.__name__`, or the class name for a callable object (`get_callable_name`) | Rename the function to rename the tool. A toolset `tool_name_prefix` prepends `prefix_`. |
| Description | `inspect.cleandoc(func.__doc__)`; a callable object falls back to `__call__.__doc__` | The whole docstring is the description. There is no separate summary field. |
| Parameters | Type hints and defaults of positional-or-keyword, keyword-only and positional-only parameters | `*args` and `**kwargs` are dropped. |
| Hidden parameters | The parameter annotated `ToolContext` (any name; `tool_context` by name as fallback) and `input_stream` | Never visible to the model; injected at call time. |
| Return schema | Only for the Vertex AI variant, derived from the return annotation | Gemini API declarations carry no response schema. |

Two declaration builders exist in 2.8.0, selected by the feature flag
`JSON_SCHEMA_FOR_FUNC_DECL`. The flag is registered `EXPERIMENTAL` with
`default_on=True`, so the default path is the pydantic JSON-schema builder
(`_function_tool_declarations.build_function_declaration_with_json_schema`),
which fills `parameters_json_schema`. Setting `ADK_DISABLE_JSON_SCHEMA_FOR_FUNC_DECL`
selects the hand-written parser (`_function_parameter_parse_util`), which fills
`parameters`. Check which one the target runs; the rules below name the path when
they differ.

## Parameter rules

- **Required**: a parameter with no default. Both paths put it in `required`.
  At call time `FunctionTool.run_async` also checks `_get_mandatory_args()` and,
  if the model omitted one, returns `{"error": "Invoking `name()` failed as the
  following mandatory input parameters are not present: ..."}` without calling
  the function. That error text is the model's only repair hint, so a required
  parameter still needs a name the model can fill.
- **Optional**: a parameter with a default. The default appears as
  `schema.default`. In the hand-written path a default that is not
  type-compatible with the annotation raises `ValueError` ("is not compatible
  with the parameter annotation"); an `Enum` default must be a member, and a
  `Literal` default must be one of the literals.
- **Nullable**: `Optional[T]` or `T | None` is nullable and therefore not
  required. The pydantic path emits `anyOf: [T, null]`; the 2.9.0 CHANGELOG
  entry "sanitize anyOf schemas for Vertex AI function declarations" shows that
  `anyOf` shapes needed repair on the Vertex AI variant before that release.
  The hand-written path raises "AnyOf is not supported in function declaration
  schema for Google AI" for a non-collapsible union on the Gemini API variant.
- **Enum**: an `Enum` subclass becomes a string schema with `enum` set to the
  member values; `Literal["a", "b"]` likewise (hand-written path: literals must be
  strings). The model sees only the values, so make values self-describing.
- **Containers**: `list[T]`, `dict[K, V]`, homogeneous tuples and pydantic
  `BaseModel` classes are supported. A heterogeneous tuple raises in the
  hand-written path ("must use one repeated item type").
- **Unsupported annotations**: the hand-written path raises `ValueError`
  "Automatic function calling works best with simpler function signature
  schema, consider manually parsing your function declaration". One failing
  parameter switches the whole function to the pydantic `TypeAdapter`
  fallback; a class pydantic cannot describe raises from that fallback with the
  same message. The pydantic default path raises pydantic's own schema error.
  Either way the agent fails on its first request.
- **No type hint**: not an error. The pydantic path treats it as `Any`, which
  yields a property with no type; the hand-written path falls to the pydantic
  fallback with the same effect. The model then guesses the type.

## Type-hint allowlist for 2.8.0

Safe on both builders and both API variants: `str`, `int`, `float`, `bool`,
`list[str]` (or `List[str]`), `dict[str, Any]`, `Optional[T]` of those, an
`Enum` subclass with string values, `Literal["a", "b"]`. Review before using:
bare `list` or `dict` (no item type reaches the model; historically failed,
adk-docs issue #880), PEP 604 `list[str] | None` (fixed in 2.2.0 per the same
issue; fine on 2.8.0 but check older pins), `Union[str, int]` and nested
pydantic models (`anyOf` and nested `required` shapes have needed fixes:
adk-python #4777 fixed 1.28.0, #6373 fixed 2.9.0), custom classes as return
types on Vertex (#3543 open at the time of reading). Lambdas and closures are
not tools (#293): use named functions. Issue references are from the
coordinator's research of 2026-10-06; treat them as pointers to verify, not as
source-verified behaviour.

Defaults: "Use defaults only for values that are truly optional. Do not add
defaults for information the model should derive from the user request" (ADK
function-tools doc). `destination: str = "Paris"` lets the model skip asking.
Give defaults to tuning knobs (`max_results: int = 20`,
`response_format: Literal["concise", "detailed"] = "concise"`), never to
domain values. The linter's `domain_default_review` flags string defaults that
look like domain values.

## Per-parameter descriptions

In 2.8.0 **no per-parameter description reaches the model** on either path:

- `_function_tool_declarations._get_function_fields` resolves hints with
  `get_type_hints(func)` without `include_extras=True`, which strips
  `Annotated[...]` metadata before pydantic sees it.
- `_automatic_function_calling_util._get_fields_dict` sets
  `pydantic.Field(description=None)` with the comment "Do not support parameter
  description for now", and `_parse_schema_from_parameter` never sets one.

The 2.10.0 CHANGELOG entry "preserve Annotated metadata in tool declarations and
arg conversion" changes the builder to `get_type_hints(func, include_extras=True)`
(verified in `adk-python` main). On 2.8.0 the parameter name and the docstring
body therefore carry all parameter semantics. Write the name so it reads as a
label (`departure_date_iso`, `max_results`) and document format and allowed
values in the docstring. When the project upgrades to 2.10.0 or later,
`Annotated[str, Field(description=...)]` becomes the preferred place for
per-parameter text; re-check with an inspection of the live declaration rather
than by reading the CHANGELOG alone.

The ADK function-tools documentation says "The parameter's description is taken
from the function's docstring"; on 2.8.0 that is true only in the sense that the
docstring is the single description string. Treat the docstring as the parameter
documentation.

## Inspect the live declaration

Build the declaration the target actually sends before and after a change,
without a model call:

```python
from google.adk.tools import FunctionTool

tool = FunctionTool(lookup_order)
declaration = tool._get_declaration()   # private API; verify it exists in the pinned version
print(declaration.model_dump_json(exclude_none=True, indent=2))
```

`_get_declaration` is private, so expect to adjust this check across versions.
Confirm the description text, which properties exist, which are in `required`,
whether `enum` values and defaults are present, and that hidden parameters are
absent. Record the serialised size; it is the per-request context cost of the
tool.

## Return values

- Return a `dict`. Anything else is wrapped as `{"result": value}`
  (`flows/llm_flows/functions.py`; "Specs requires the result to be a dict").
- Include a `status` key (`"success"`, `"error"`, `"pending"`, `"ambiguous"`)
  as the "highly recommended" documented convention, with `error_message` on
  failure (ADK tools overview). Make every error actionable; see
  [results and errors](results-and-errors.md).
- ADK's own runtime errors use the key `error` (`{"error": "Invoking ... not
  present"}`, `{"error": "This tool call is rejected."}`), and a dict whose
  `error` key is truthy is counted as `TOOL_ERROR` by the telemetry hook
  `_detect_error_in_response`. Either `error` or `error_message` is readable
  by the model; pick one per project and keep `error` for real failures so
  telemetry stays truthful.
- Never raise for an expected failure and never return a bare string: the
  model needs the dict to recover, and a tool exception or stray text can
  break Gemini's strict turn ordering (adk-python #745, "function call turn
  comes immediately after a user turn").
- Do not describe the injected `ToolContext` parameter in the docstring; the
  ADK docs say it "can confuse the LLM" because the model never fills it.
- Media parts inside the result are extracted into `FunctionResponse.parts`;
  the remaining keys stay in `response`.

## Confirmation

`FunctionTool(func, *, require_confirmation: bool | Callable[..., bool] = False)`.
A callable is invoked with the same prepared arguments as the function
(including the injected context when the function declares one) and returns
whether this call needs confirmation. When confirmation is
required and absent, the tool returns `{"error": "This tool call requires
confirmation, please approve or reject."}`, sets `skip_summarization` and calls
`tool_context.request_confirmation(hint=..., payload=...)`; a rejected
confirmation returns `{"error": "This tool call is rejected."}` and the function
is not called. `request_confirmation(*, hint: str | None = None, payload: Any |
None = None)` lives on the context class and requires a `function_call_id`.
Policy for when confirmation is required belongs to `adk-operational-guardrails`;
the model-facing text of the hint belongs here: say what will happen and what
the approver should check.

## LongRunningFunctionTool

`LongRunningFunctionTool(func)` takes no `require_confirmation` argument. It
sets `is_long_running = True` and appends to the description: "NOTE: This is a
long-running operation. Do not call this tool again if it has already returned
some intermediate or pending status." The function returns an initial dict
(commonly `status: "pending"` with an identifier); the final result is delivered
later under the same `function_call_id`. Design the initial dict so the model
can explain the wait to the user.

## Callbacks around a tool

`before_tool_callback(tool, args, tool_context)` runs after the model chose
the tool. Returning `None` lets the tool run with the (possibly modified)
`args`; returning any dict, including `{}`, skips the tool and becomes the
result (ADK callbacks doc: "only `None` lets the tool run"). Use it for
argument validation that returns an error dict the model can act on, for
example rejecting a model-supplied `customer_id` that differs from the one in
`tool_context.state`. `after_tool_callback(tool, args, tool_context,
tool_response)` receives the raw return before `result` wrapping; use it to
trim or offload large outputs. The ADK safety guide frames the split: tool
arguments are set by the model, `ToolContext` is set deterministically by the
developer. 2.11.0 adds an optional `ToolCallIntegrityPlugin` that stamps
function calls and refuses tampered or replayed ones; not present on 2.8.0.

## Built-in tools and other tools

Google Search, code execution and Agent Search "can only be used by
themselves" in one agent on the Gemini API (ADK tools limitations doc). In
2.8.0 `canonical_tools` wraps a `GoogleSearchTool` or `VertexAiSearchTool` in
an agent-backed tool when other tools or transfer targets exist, but only when
that tool was constructed with `bypass_multi_tools_limit=True`; otherwise wrap
the built-in tool in a dedicated agent and expose it with `AgentTool` or a
`single_turn` sub-agent. The community-reported error text is "Multiple tools
are supported only when they are all search tools".

## Where tools may be configured

`LlmAgent.validate_generate_content_config` raises `ValueError` when
`generate_content_config.tools`, `system_instruction` or `response_schema` is
set: "All tools must be set via LlmAgent.tools, not via
generate_content_config.tools". Forcing tool selection through
`tool_config.function_calling_config` is a model-request setting; in ADK apply
it in a `before_model_callback` on `llm_request.config`, and verify the field
exists in the pinned `google-genai` version.

## Duplicate names

`LlmRequest.append_tools` logs "Duplicate tool name %r: the previously
registered tool is shadowed and can no longer be called" and keeps both
declarations. The model may pick the shadowed declaration and the call lands on
the survivor. Give every tool in one agent a unique name, including toolset
output after prefixing.

## Related CHANGELOG items

- 2.8.0: "fence relayed agent output so it cannot pose as instructions"; "send
  the required list on a CrewAI or LangChain function declaration" (wrapped
  third-party tools previously advertised every parameter as optional).
- 2.9.0: "sanitize anyOf schemas for Vertex AI function declarations"; MCP SDK
  2.x support with closed models: unknown keys on a `CallToolResult` are dropped
  during validation, `_meta` survives.
- 2.10.0: "preserve Annotated metadata in tool declarations and arg
  conversion"; "fence server-supplied tool description before reaching the
  model" (`fence_tool_description` and `fence_schema_descriptions` applied to
  MCP tool declarations).

None of these are present on a 2.8.0 pin. Note which ones a target depends on
before recommending an upgrade, and leave the upgrade decision to the owner.

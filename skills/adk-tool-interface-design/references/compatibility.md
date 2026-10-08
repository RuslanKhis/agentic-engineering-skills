# Compatibility and evidence boundaries

This skill was written against the `google-adk` **2.8.0** source (tag v2.8.0)
and the `adk-python` main branch at **2.11.0** with its CHANGELOG, both read on
**2026-10-06**. Behaviour statements in the references were verified by reading
that source, not by running it: the scratch interpreter available while writing
could not import the package, so no declaration was built or model called.
Treat every statement as **source-verified, not executed**; confirm on the
target's own interpreter with the declaration dump in
[validation](validation.md) before relying on it.

## Version-dependent facts

| Fact | 2.8.0 (pinned) | Later versions (CHANGELOG, main source) |
| --- | --- | --- |
| Per-parameter descriptions | Not sent: `get_type_hints(func)` strips `Annotated`; legacy parser sets `description=None` | 2.10.0 "preserve Annotated metadata in tool declarations and arg conversion"; main uses `include_extras=True` |
| Default declaration builder | Pydantic JSON schema (`JSON_SCHEMA_FOR_FUNC_DECL`, experimental, default on); legacy parser when disabled | Same flag present in main; check the registry of the pinned version |
| `anyOf` from `Optional[T]` | Emitted by the pydantic path; Vertex AI sanitisation arrived in 2.9.0 | 2.9.0 "sanitize anyOf schemas for Vertex AI function declarations" |
| Server-supplied MCP descriptions | Reach the model unmodified | 2.10.0 "fence server-supplied tool description before reaching the model" |
| Relayed agent output | Fenced ("fence relayed agent output so it cannot pose as instructions", 2.8.0) | Unchanged |
| MCP SDK | 1.x | 2.9.0 adds 2.x; closed models drop unknown `CallToolResult` keys (`_meta` kept); 2.11.0 adds an opt-in modern-protocol connect path |
| Third-party (CrewAI, LangChain) declarations | `required` list sent (2.8.0 fix) | Unchanged |
| `AgentTool` guidance | Docstring discourages direct use in favour of `mode='single_turn'` | Same; 2.11.0 "preserve single-turn structured output" fixed a regression |
| `generate_content_config.tools` | Rejected by `validate_generate_content_config` with a message pointing to `LlmAgent.tools` | Unchanged |

## Reported pitfalls by version

Issue references were gathered by the coordinator on 2026-10-06 from
`google/adk-python` and `google/adk-docs`; the fix versions are as reported
there. Verify the behaviour on the pinned version before citing it to an
owner.

| Symptom | Reported cause and version | Interface fix |
| --- | --- | --- |
| "Failed to parse the parameter ... works best with simpler function signature schema" | PEP 604 `list[str] \| None` before 2.2.0 (adk-docs #880); lambda or closure tools (#293); custom-class return types under Vertex (#3543, open) | `Optional[List[str]]` on old pins; named functions; dict returns |
| Bare `list`/`dict` parameters fail; `List[dict]`, `Dict[str, Any]` work | adk-docs #880 | Always give item types |
| Defaults dropped with "Default value is not supported in function declaration schema for Google AI" | #3275 at 1.16; the 2.8.0 parser comments "GEMINI now supports default value" and no longer strips them | Check the live declaration for `default` |
| `anyOf` rejected on the Gemini API; Optional or Literal pydantic fields failed on Vertex ("schema didn't specify the schema type field") | `_raise_for_any_of_if_mldev` in the legacy parser; #6373 fixed 2.9.0 | Avoid unions of several types; `Optional[T]` only |
| Nested pydantic parameter lost nested `required`, so the model omitted fields | #4777, fixed 1.28.0 | Flatten to primitives |
| OpenAPI `oneOf`/discriminator: 400 "parameters.properties cannot be empty" | #2213; 2.7.0 lowers `oneOf` to `anyOf` and coerces non-string enums; `Enum` parameters from 1.18.0 | Simplify the spec exposed to the toolset |
| `**kwargs` tools get arguments stripped | #3036 | Explicit parameters only |
| Tool raising or returning a bare error string leads to 400 "function call turn comes immediately after a user turn" | #745 | Return a dict, never raise for expected failures |
| `skip_summarization` on `AgentTool` ended the turn with no text | #3881 fixed 2.4.0; scoped in 2.7.0 (#6230) | Assert the user-visible text |
| Built-in tool with other tools: 400 "Multiple tools are supported only when they are all search tools" | Gemini 2.x behaviour reported by the community (dev.classmethod.jp, April 2026); also with `VertexAiRagRetrieval` (#514) | Isolate in an `AgentTool` or set `bypass_multi_tools_limit` |

If the target pins a different version, read its own `tools/function_tool.py`,
`tools/_function_tool_declarations.py`, `tools/_automatic_function_calling_util.py`
and `features/_feature_registry.py` before quoting any rule above. Preserve the
pin; propose an upgrade as a decision for the owner with the specific CHANGELOG
entries it would bring.

## Model and API dependence

- The thresholds in [tool count](tool-count-and-toolsets.md) are vendor
  measurements on the vendor's models (OpenAI, Anthropic). Gemini publishes no
  equivalent count; measure selection accuracy on the target model.
- `FunctionCallingConfigMode` values `AUTO`, `ANY`, `VALIDATED` and
  `allowed_function_names` exist in the `google-genai` types shipped with the
  inspected environment; `NONE` appears in the Gemini API documentation. Verify
  the enum in the pinned `google-genai` before configuring it, and check that
  the agent's `generate_content_config` field you set is one the flow copies
  into the request.
- Gemini function declarations accept an OpenAPI schema subset
  (`parameters`) or JSON schema (`parameters_json_schema`); nested or unusual
  shapes are the usual cause of 400 errors at the first request. A schema that
  passes OpenAI strict mode is a conservative yardstick, not a Gemini guarantee.

## What the bundled helpers establish

- `lint_tool_schemas.py` makes syntactic observations: a missing docstring is
  a fact; a "short" docstring, a "generic" name, a "similar" description or an
  "identity" parameter is a prompt for review. It resolves module attributes
  and imports to scanned files, but cannot see tools built dynamically,
  re-exported ambiguously, or produced by toolsets at runtime, and reports those as `unresolved_tool_reference`, `tools_not_literal` or
  `toolset_count_unknown`.
- `report_tool_result_sizes.py` measures serialised bytes of recorded
  responses and estimates tokens as bytes/4. It does not know the model's
  tokenizer and does not see responses that were never recorded.
- Neither helper runs the target, calls a model or proves that the model
  selects a tool correctly.

## Evidence labels used in this skill

| Label | Meaning |
| --- | --- |
| V | Vendor guidance or vendor-measured figures (Anthropic, OpenAI, Google) |
| D | Documented product behaviour (ADK docs, Gemini API docs, MCP specification) |
| E | Independent evidence (peer-reviewed benchmark, published study) |
| Source-verified | Read in the named ADK source file at the stated version |

A recommendation labelled V or D is a reasonable default; one labelled E has
been measured somewhere other than the vendor; none of them is a measurement on
the target project until the hand-off in
[evaluation hooks](evaluation-hooks.md) has been run.

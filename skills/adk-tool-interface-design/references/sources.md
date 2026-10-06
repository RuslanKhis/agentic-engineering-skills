# Sources

Dates are the day each source was read. Flags: **V** vendor guidance or
vendor-measured figures; **D** documented product behaviour or specification;
**E** independent evidence; **S** ADK source read directly.

## ADK source and changelog (S, D)

- `google-adk` 2.8.0 source, tag v2.8.0, read 2026-10-06: `tools/function_tool.py`,
  `tools/_function_tool_declarations.py`, `tools/_automatic_function_calling_util.py`,
  `tools/_function_parameter_parse_util.py`, `tools/agent_tool.py`,
  `tools/long_running_tool.py`, `tools/base_toolset.py`, `tools/mcp_tool/mcp_toolset.py`,
  `agents/llm_agent.py`, `agents/context.py`, `agents/readonly_context.py`,
  `flows/llm_flows/agent_transfer.py`, `flows/llm_flows/functions.py`,
  `models/llm_request.py`, `features/_feature_registry.py`.
- `adk-python` main at 2.11.0, read 2026-10-06: `CHANGELOG.md` entries for 2.8.0,
  2.9.0, 2.10.0 and 2.11.0; `tools/_function_tool_declarations.py`
  (`include_extras=True`); `tools/mcp_tool/mcp_tool.py` and
  `flows/llm_flows/context/_fencing.py` (description fencing).
  https://github.com/google/adk-python/blob/main/CHANGELOG.md
- ADK documentation (D), read 2026-10-06 from the local `adk-docs` clone:
  Function tools https://adk.dev/tools-custom/function-tools/ (dict return,
  `result` wrapping, `status` convention, "Use defaults only for values that
  are truly optional", "Fewer Parameters are Better", "Simple Data Types",
  "Meaningful Names", `temp:` state); Tools overview
  https://adk.dev/tools-custom/ (`lookup_order_status` docstring template,
  `status` values including `ambiguous`, `error_message`, verb-noun names, "the
  LLM uses the function name as a primary identifier", decomposition of
  `update_user_profile`, "Do not describe the injected ToolContext
  parameter"); Parallel execution https://adk.dev/tools-custom/performance/
  (`async def` required for concurrent tool execution); Callback types
  https://adk.dev/callbacks/types-of-callbacks/ (`before_tool_callback` runs
  the tool only on `None`); Tool limitations https://adk.dev/tools/limitations/
  (built-in tools "can only be used by themselves", `AgentTool` workaround);
  MCP tools https://adk.dev/tools-custom/mcp-tools/ (context-bloat comparison
  table, "Always supply `tool_filter=[...]`", synchronous `McpToolset`);
  Tool confirmation https://adk.dev/tools-custom/confirmation/ (`hint`,
  `payload`, known limitations); Collaboration modes
  https://adk.dev/workflows/collaboration/ (Table 1 comparing `chat`, `task`,
  `single_turn`).
- Google Cloud blog (V): "Where to use sub-agents versus agents as tools",
  2025-11-08, https://cloud.google.com/blog/topics/developers-practitioners/where-to-use-sub-agents-versus-agents-as-tools
  (tools for discrete stateless capabilities, sub-agents for stateful
  processes; `AgentTool` isolation). "Tools make an agent", 2025-06-27
  (`tool_filter` "protects the agent's model from getting overwhelmed").
- Google `adk-samples` (V, example code, read 2026-10-06 by the coordinator;
  several samples were taken from the last commit before their removal from
  main): customer-service (twelve flat tools, `status`/`message` returns,
  `before_tool` argument validation), financial-advisor (coordinator with four
  `AgentTool`s), data-science (`AgentTool(...).run_async` wrappers),
  software-bug-assistant (`AgentTool(search_agent)`, read-only GitHub MCP
  `tool_filter`), core/python/oauth-user-consent-flow (`pending` after
  `request_credential`), long-horizon-harness (guard chain, result pruning,
  description budgets, pydantic-path schema overhead measurement),
  contrib/python/retail-product-search (counter-example returning plain `str`).
  https://github.com/google/adk-samples
- Issue references in [compatibility](compatibility.md) (adk-python #293,
  #514, #745, #2213, #3036, #3275, #3543, #3881, #4777, #6230, #6373, #3150;
  adk-docs #880) were gathered by the coordinator on 2026-10-06 and are
  pointers to verify, not source-verified behaviour.

## Vendor guidance (V)

- Anthropic, "Writing effective tools for agents", 2025-09-11, read 2026-10-06.
  https://www.anthropic.com/engineering/writing-tools-for-agents
  Descriptions as onboarding; consolidation; semantic identifiers over opaque
  ones; `response_format` enum; actionable errors; evaluate with realistic
  multi-step tasks.
- Anthropic, "Define tools" (Claude developer platform), read 2026-10-06.
  https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
  Three to four or more sentences per description: what, when, parameters,
  caveats.
- Anthropic, "Tool search tool", read 2026-10-06.
  https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool
  Selection degrades past 30-50 tools; a five-server MCP setup at about 55k
  tokens of definitions; use tool search at 10+ tools or more than 10k tokens;
  keep 3-5 hot tools; describe categories in the system prompt; default
  25,000-token response cap. Vendor-measured on Claude.
- OpenAI, "Function calling" guide, read 2026-10-06.
  https://developers.openai.com/api/docs/guides/function-calling
  "Intern test"; unambiguous parameter names; enums; do not ask for known
  values; fewer than 20 functions as a soft guideline; strict mode.
- Google, Gemini API "Function calling", fetched 2026-10-06 by the coordinator.
  https://ai.google.dev/gemini-api/docs/function-calling
  `function_calling_config` modes `AUTO`, `ANY`, `NONE`, `VALIDATED` and
  `allowed_function_names`; parallel and compositional calling; "Keep active
  set to 10-20 tools maximum" and consider dynamic tool selection above that;
  generic low-level tools used more often but less accurately than specific
  high-level ones; put date, time and location in the system instruction;
  validate consequential calls with the user; supported schema attributes
  `type`, `nullable`, `required`, `format`, `description`, `properties`,
  `items`, `enum`, `anyOf`, `$ref`, `$defs` ("remaining attributes are not
  supported").

## Specifications (D)

- Model Context Protocol, "Tools" (server features), revision 2025-06-18, read
  2026-10-06. https://modelcontextprotocol.io/specification/2025-06-18/server/tools
  Tool execution errors reported inside the result with `isError: true` versus
  protocol errors as JSON-RPC errors; annotations (`readOnlyHint`,
  `destructiveHint`, `idempotentHint`, `openWorldHint`) are hints that clients
  must not trust from untrusted servers.

## Independent evidence (E)

- Patil et al., "The Berkeley Function Calling Leaderboard (BFCL): From Tool
  Use to Agentic Evaluation of Large Language Models", ICML 2025, PMLR 267.
  https://proceedings.mlr.press/v267/patil25a.html
  Metric design: selection and parameter (AST) accuracy, relevance detection,
  multi-turn evaluation, not final-answer-only.
- KAMI benchmark, arXiv 2512.07497, read 2026-10-06. Failure modes: premature
  action, over-helpful substitution, context pollution. Single study; use for
  error-analysis labels, not as a measured rate for your model.

## Repository stance (internal)

- `adk-tool-auth-and-secrets`: a model-supplied user or tenant identifier is
  never authority; identity comes from `ToolContext` and verified session
  ownership.
- `adk-system-designer`, design decisions: public results distinguish
  complete, truncated, empty and unavailable evidence.
- `safe-api-tool-calls`: retries, deadlines, idempotency and confirmation
  mechanics of the external call.
- `adk-operational-guardrails`: budgets and approval policy.
- `adk-agent-evaluation`: measurement of selection and parameter accuracy.
- `adk-agent-instructions` and `adk-model-and-output-contracts`: instruction
  text and output schemas (sibling skills, referenced by name).

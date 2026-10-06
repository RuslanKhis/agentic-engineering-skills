# Tool count, budgets and dynamic toolsets

Use this reference when an agent has many tools, when selection accuracy drops
as tools are added, or when declarations consume a noticeable share of the
context. Thresholds below are **vendor-measured** on the vendor's own models
and are starting points for your own measurement, not ADK or Gemini limits.

## Thresholds and what they rest on

| Figure | Source and status | Use |
| --- | --- | --- |
| "Fewer than 20" tools per request | OpenAI function-calling guide, soft guideline (V) | A review trigger, not a cap. The linter's `--max-tools` default is 20. |
| Selection "degrades once you exceed 30-50 tools" | Anthropic tool-search doc, vendor-measured on Claude (V) | Treat 30 as the point where you must measure selection accuracy per added tool. |
| A five-server MCP setup consumed about 55k tokens of definitions | Anthropic tool-search doc (V) | Compute your own figure with the declaration-size check below. |
| Use tool search when 10+ tools or more than 10k tokens of definitions; keep 3-5 hot tools loaded; describe categories in the system prompt | Anthropic tool-search doc (V) | The pattern transfers to ADK through `BaseToolset.get_tools`; the numbers do not transfer without measurement. |
| "Keep active set to 10-20 tools maximum"; above that "consider dynamic tool selection" | Gemini function-calling doc, fetched 2026-10-06 (V) | The vendor figure for the target model family; still a guideline, not an API limit. |
| `AgentTool` as "Zero Context Bloat", ideal for ">20 tools where schema overload harms accuracy"; direct `McpToolset` as "High Context Bloat" | ADK MCP tools doc (D) | Use a sub-agent per server or domain when a server's tools would exceed the active set. |

Independent evidence on tool count is thin. The BFCL benchmark (E, ICML 2025)
measures selection and parameter accuracy across tool sets but does not
isolate count; the KAMI study (E, single study) reports failure modes
(premature action, over-helpful substitution, context pollution) that increase
with interface ambiguity. Record your own before/after numbers; see
[evaluation hooks](evaluation-hooks.md).

## Measure the declaration cost

```python
import json
from google.adk.tools import FunctionTool

def declaration_bytes(tool):
    declaration = tool._get_declaration()   # private API; verify on the pinned version
    return len(declaration.model_dump_json(exclude_none=True).encode("utf-8"))

sizes = {tool.name: declaration_bytes(tool) for tool in [FunctionTool(f) for f in TOOL_FUNCTIONS]}
print(json.dumps(sizes, indent=2), sum(sizes.values()) // 4, "approx tokens (bytes/4)")
```

Bytes divided by four is a rough token estimate; use the model's token counter
for a real figure. The total is paid on every model request of the agent, so
multiply by the expected calls per invocation. Compare with the task-relevant
content in the request; when declarations exceed it, reduce the exposed set.

## Reduce the exposed set in ADK

### Filter a toolset

`BaseToolset.__init__(*, tool_filter: ToolPredicate | list[str] | None = None,
tool_name_prefix: str | None = None)`. `McpToolset` accepts the same
`tool_filter` and `tool_name_prefix`. A list filters by exact name; a predicate
`(tool, readonly_context) -> bool` can read `readonly_context.state`,
`readonly_context.user_content`, `readonly_context.agent_name` and
`readonly_context.invocation_id`.

```python
from google.adk.tools.mcp_tool import McpToolset

github = McpToolset(
    connection_params=params,
    tool_filter=["list_pull_requests", "get_pull_request", "create_review_comment"],
    tool_name_prefix="github",
)
```

An MCP server's tool list is server-supplied: filter by allow-list, never by
deny-list, so a server that adds tools does not widen the agent's surface. The
ADK MCP doc's checklist says "Always supply `tool_filter=[...]`", define the
`McpToolset` synchronously in `agent.py` for deployed agents, and use
`tool_name_prefix` to avoid collisions. `OpenAPIToolset` derives names from
`operationId` (snake_case, at most 60 characters) and descriptions from
`summary`/`description`; it also accepts `tool_name_prefix`. Google's
software-bug-assistant sample pairs a GitHub MCP server with a read-only
`tool_filter`, and the long-horizon-harness sample notes that "a new tool
costs its whole description on every call" and enforces per-tool description
budgets; that sample also measured the pydantic declaration path adding
`title`, `default: null` and `anyOf [X, null]` entries (about 2.5k characters
per turn in its setup) compared with the legacy parser. Measure your own.

### Expose tools by phase or state

Implement `BaseToolset.get_tools(readonly_context)` to return a different list
per phase, user role or conversation state. The toolset is consulted when the
request is built, so the set can change between turns. The result is cached per
invocation (`get_tools_with_prefix` keys its cache on `invocation_id`).

```python
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.tools import BaseTool, FunctionTool
from google.adk.tools.base_toolset import BaseToolset


class PhasedToolset(BaseToolset):
    """Expose intake tools until an order is selected, then order tools."""

    def __init__(self):
        super().__init__()
        self._intake = [FunctionTool(search_customers), FunctionTool(list_customer_orders)]
        self._order = [FunctionTool(lookup_order), FunctionTool(cancel_order)]

    async def get_tools(self, readonly_context: ReadonlyContext | None = None) -> list[BaseTool]:
        if readonly_context is None or "selected_order_id" not in readonly_context.state:
            return self._intake
        return self._intake[:1] + self._order
```

Tell the model in the instruction that tools change by phase and what the
phases are; otherwise it may ask for a tool it saw earlier. That instruction
text belongs to `adk-agent-instructions`; the interface decision belongs here.

### A tool-search tool

For very large catalogues, expose a small hot set plus one `find_tools(query)`
tool whose result lists candidate names and one-line descriptions, and let a
toolset's `get_tools` add the chosen tools on the next turn from state. ADK has
no built-in equivalent of a vendor tool-search tool at 2.8.0; this is a pattern
to implement and measure, not a product feature. Keep the catalogue entries in
the same style as docstrings so the model's selection reasoning is consistent.

### Describe categories

When tools are hidden or filtered, the instruction should name the categories
("order lookup, cancellation, delivery tracking") so the model knows what exists
before it sees the declarations. Vendor guidance (V, Anthropic) found this
necessary for deferred loading; it is cheap and testable with a scripted model.

## Built-in tools

Google Search, code execution and Agent Search cannot share an agent with
other tools on the Gemini API (ADK tools limitations doc). Put each in its own
small agent and expose it as an `AgentTool` or a `single_turn` sub-agent, or
construct `GoogleSearchTool(bypass_multi_tools_limit=True)` so 2.8.0's
`canonical_tools` wraps it for you. Google's software-bug-assistant sample
isolates `google_search` in an `AgentTool(search_agent)` for this reason.

## Sub-agents count too

Every `single_turn` or `task` sub-agent becomes a tool declaration on the parent
(`_SingleTurnAgentTool`, `_TaskAgentTool`), and `chat` sub-agents add a
`transfer_to_agent` tool plus their descriptions in the instruction. Count them
with the function tools when budgeting; see
[delegation interfaces](delegation-interfaces.md).

## Observable checks

- Tool-count report: `python scripts/lint_tool_schemas.py --project . --max-tools 20`
  lists `tool_count_exceeds_max`, `toolset_count_unknown` and `tools_not_literal`
  per agent; resolve the runtime count for toolsets with `await toolset.get_tools(None)`
  in a test.
- Declaration bytes per tool and per agent, before and after.
- Selection accuracy on a fixed prompt set with a scripted or live model
  (hand-off to `adk-agent-evaluation`), re-run after every added tool once the
  count passes 20.

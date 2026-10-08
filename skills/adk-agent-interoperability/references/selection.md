# Select a tool source

Read this for mode (a). A tool source decides who writes the schema the model
sees, who runs the code, which identity it runs under, and how much of the
result lands in the agent's context. Choose the narrowest source that meets
the task, then verify the row's observable check on the target.

## Decision table

| Source | Choose it when | Avoid it when | Observable check |
| --- | --- | --- | --- |
| `FunctionTool` (your Python) | The logic is yours, deterministic and testable; the identity is the agent's own; the result fits in a few hundred tokens | You would re-implement a maintained server or API client | Unit test of the function plus a scripted-model Runner test; docstring reviewed with `adk-tool-interface-design` |
| `OpenAPIToolset` | A REST API has a spec you control or trust; you want one tool per operation without writing wrappers | The spec is large or third-party and unreviewed (every operation description reaches the model); you need per-user tokens the spec does not model | Tool names derive from `operationId` (snake_case, 60 chars; documented behaviour); `tool_filter` lists the operations used; `tool_name_prefix` set when two specs share verbs (source-verified `openapi_toolset.py` signature) |
| `McpToolset` | A maintained MCP server exists for the system (databases, GitHub, Maps, filesystems) and its operator is inside your trust boundary | Fewer than three tools that you could write yourself; the server is unreviewed or has no filter you can apply | `mcp_tool_inventory.py` manifest committed; `tool_filter` and `tool_name_prefix` present; declared tools equal the manifest in a test |
| `ToolboxToolset` (MCP Toolbox for Databases) | Database access with server-side SQL templates, bound parameters hidden from the model and workload or user identity handled by the Toolbox server | You need ad-hoc SQL (that is `adk-sql-agent-engineering`'s territory) or the Toolbox server is not deployable in your perimeter | `ToolboxToolset(server_url, toolset_name, tool_names, auth_token_getters, bound_params)` (source-verified 2.8.0 signature); newer `credentials=CredentialStrategy...` options are vendor docs, verify against the installed `toolbox-adk` |
| `ApplicationIntegrationToolset` | The system is reachable through an Application Integration connection or integration and you want Google-managed auth to it | You need operations the connector does not expose; latency budget is tight | `ApplicationIntegrationToolset(connection=, entity_operations=, actions=, tool_name_prefix=...)` (source-verified 2.8.0 signature); IAM role granted on Agent Runtime is the one the docs name for execution (vendor; see [platform-registration](platform-registration.md)) |
| `AgentTool` around a sub-agent that holds the toolset | More than about twenty tools, trial-and-error workflows, or results that would bloat the parent's context | The task is one deterministic call; the extra model turns cost more than they save | Parent history contains only the sub-agent's final text; sub-agent has its own `tool_filter` |
| `RemoteA2aAgent` | The capability is another agent, run as a separate service, by another team or in another framework | A tool would do; the "agent" is just an API with a model in front | Card validated with `agent_card_check.py`; contract table written ([topology](topology.md)) |

The ADK MCP overview table (documented behaviour, `docs/tools-custom/mcp-tools/index.md`)
characterises direct `McpToolset` as "high context bloat" (every tool
definition and raw output enters the primary agent's history), `AgentTool`
delegation as "zero context bloat" with model tiering, and `to_mcp_server`
as "isolated" for external callers. It recommends `AgentTool` delegation for
">20 tools where schema overload harms accuracy". Treat the thresholds as
vendor guidance, not measurements on your agent.

## Costs that differ by source

| Cost | FunctionTool | OpenAPIToolset | McpToolset | AgentTool wrapper | RemoteA2aAgent |
| --- | --- | --- | --- | --- | --- |
| Who writes the model-visible description | You | Spec author | Server operator (unfenced on 2.8.0; fenced from 2.10.0) | You (sub-agent description) | Remote operator (card description) |
| Identity | Agent's own | Agent's own or `auth_scheme` | `header_provider` per user, `auth_scheme`, or server-side | Same as parent | Declared in the card, carried in headers |
| Extra model turns | 0 | 0 | 0 | 2 or more | Remote agent's own, invisible to you |
| Context cost | Result only | Result only | All declarations plus raw results | Final text only | Final text and task messages |
| Failure surface | Exception in process | HTTP errors | Connection, timeout, dead session, `isError` results | Sub-agent failure | Error events, task `failed`, `rejected`, `canceled`, stream cut |

## Procedure

1. List the capabilities the agent needs as verbs on nouns, with read, write
   or irreversible marked (`adk-agent-security` tiers them).
2. For each, pick the first row in the table whose "choose it when" holds and
   whose "avoid it when" does not. Record the choice and the check.
3. When two sources share verbs (`search`, `read_file`, `query`), decide the
   prefix now; renaming later changes the model's history.
4. For `McpToolset` and `OpenAPIToolset`, review the AI-visible text before
   the first run with the manifest or the spec dump; the review belongs to
   `adk-agent-security` mode (c) when the operator is outside your team.
5. Write the row into the boundary contract table and move to the consuming
   reference: [mcp-consumption](mcp-consumption.md) or
   [a2a-contracts](a2a-contracts.md).

## Common mistakes

- Wrapping an HTTP API in an MCP server you then consume from the same
  process: two hops, one owner, no gain. Use `OpenAPIToolset` or a
  `FunctionTool`.
- Exposing a whole community server because the filter felt restrictive; the
  context cost and the write tools arrive together.
- Calling another team's ADK agent through `AgentTool` by importing their
  package: you now share their pins, identity and failure modes in process.
  That is the case for A2A ([topology](topology.md)).

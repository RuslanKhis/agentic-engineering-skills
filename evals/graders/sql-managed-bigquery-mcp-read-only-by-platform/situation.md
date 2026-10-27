# sql-managed-bigquery-mcp-read-only-by-platform: what the fixture holds

Base: sql-agent. Overlay:

- `analytics/agent.py`: `McpToolset` over `StreamableHTTPConnectionParams` to our self-hosted
  Toolbox, a static `Authorization: Bearer` header from an ID token minted once at start-up
  (`deploy/start.sh`; expires after an hour), no `tool_filter`, and an instruction sentence
  "only ever read data" as the only write control (A1: the write ban goes outside the model — an
  IAM deny on `mcp.googleapis.com/tools.call` with the `tool.isReadOnly` condition for the
  agent's principal, plus a tool_filter limited to read-only tools, noting tools/list still
  advertises execute_sql; A2: agent identity gets `roles/mcp.toolUser` plus BigQuery job and
  data-viewer roles, token via `header_provider`, not a static header).
- `deploy/agent-service.yaml`: the agent's own service account on Cloud Run.
- `deploy/tools.yaml`: the Toolbox being retired (free-form execute_sql).
- `deploy/iam.md`: current roles (Toolbox SA has dataEditor on `sales`) and the platform team's
  proposal to use the managed BigQuery MCP endpoint.
- Nothing checks result size or truncation of aggregates (A3: name the three-minute processing cap
  and the 3,000-row result cap; refuse or narrow instead of reporting a partial aggregate).
- A4: keep Toolbox as the choice when reviewed templates, dataset allowlists or model-invisible
  tenant binding are required; cite the official supported-products page with its date, not the
  google/mcp README.
- No network or credentials. `tests/` (base) passes offline.

Original context (unchanged).

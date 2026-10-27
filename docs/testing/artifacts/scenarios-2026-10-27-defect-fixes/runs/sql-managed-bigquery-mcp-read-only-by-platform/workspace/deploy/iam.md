# IAM today

| Principal | Role | Resource |
| --- | --- | --- |
| analytics-agent@fernhill-analytics.iam.gserviceaccount.com | roles/run.invoker | Cloud Run service analytics-toolbox |
| analytics-toolbox@fernhill-analytics.iam.gserviceaccount.com | roles/bigquery.jobUser | project fernhill-analytics |
| analytics-toolbox@fernhill-analytics.iam.gserviceaccount.com | roles/bigquery.dataEditor | dataset sales |

The Toolbox service account got dataEditor in July when we tried a scratch table for exports;
nobody has removed it.

## Proposed change (platform team)

Retire `analytics-toolbox` and point the agent at Google's managed BigQuery MCP server
(`https://bigquery.googleapis.com/mcp`), authenticating as the agent's own service account.

## Target state (vendor documentation, confirm on current docs; nothing here has been applied)

Read-only is enforced by the platform in three layers. The agent code (`analytics/mcp_policy.py`)
is only an early refusal on top.

| Layer | Setting | Why |
| --- | --- | --- |
| Agent identity | `roles/mcp.toolUser` (project), `roles/bigquery.jobUser` (job project), `roles/bigquery.dataViewer` on dataset `sales` only. No data-editing role anywhere. | Even a call that bypasses MCP, or a tool the deny misses, cannot write. The MCP deny governs MCP calls only. |
| IAM deny policy | Deny `mcp.googleapis.com/tools.call` with condition `api.getAttribute('mcp.googleapis.com/tool.isReadOnly', false) == false`, attached to the project | Refuses `execute_sql`, `cancel_job` and any future non-read-only tool. `tools/list` still advertises them, hence the `tool_filter`. |
| Client | `tool_filter=ALLOWED_TOOLS` and `before_tool_callback` | Keeps write tools away from the model and pins the job project. |

Decisions for the platform team:

- Deny policy principals: Google's example uses `principalSet://goog/public:all`, which blocks every
  MCP write tool for everyone in the project. Assumption: scope it to the agent's service account
  unless other MCP users should be blocked too.
- Remove `roles/bigquery.dataEditor` from `analytics-toolbox` and `roles/run.invoker` on
  `analytics-toolbox` when the Toolbox service is deleted. Cutover order: grant the agent's roles,
  apply the deny, test, deploy the agent, then retire Toolbox.
- Validate the deny policy JSON before attaching it (Google's sample has a trailing comma).

I've switched the agent to Google's managed BigQuery MCP server in the code and deploy files. I couldn't run the tests, because Bash is disabled in this session. Nothing has been applied to the cloud or tested against ADK or the live server.

## What to configure

**Platform (the real guarantee)**
1. Give `analytics-agent@…` these roles: `roles/mcp.toolUser`, `roles/bigquery.jobUser` on the job project, and `roles/bigquery.dataViewer` on dataset `sales` only. It should have no data-editing role anywhere.
2. Attach an IAM deny policy on `mcp.googleapis.com/tools.call` with the condition `api.getAttribute('mcp.googleapis.com/tool.isReadOnly', false) == false`. This blocks `execute_sql` and `cancel_job` even if the model calls them. Validate the policy JSON first, because Google's sample has a trailing comma.
3. Remove `dataEditor` from `analytics-toolbox` and delete that service once the agent has cut over.

**Agent (an early refusal, not the guarantee)**
- `analytics/agent.py` now points at `https://bigquery.googleapis.com/mcp`, with a `header_provider` that sends the service account's own access token.
- `tool_filter` allows only `list_dataset_ids`, `list_table_ids`, `get_dataset_info`, `get_table_info`, `execute_sql_readonly` and `get_query_results`.
- `analytics/mcp_policy.py` holds that list and a `before_tool_callback` that pins the job project, so the model can't choose where jobs run and bill.
- `deploy/start.sh` no longer mints a token, `TOOLBOX_URL` is gone from `deploy/agent-service.yaml`, and `deploy/iam.md` has the target IAM table.

## What to test

- **Offline (written, not run):** `tests/test_mcp_policy.py` checks that write and job-control tools are refused and that a model-chosen project is overwritten.
- **Once approved against the live server:**
  - `tools/list` returns the expected tools; save it as a manifest and diff it later.
  - `execute_sql_readonly` rejects an `INSERT`, a `CREATE TABLE` and a `DELETE` inside a CTE.
  - `execute_sql` called directly is denied by IAM. This proves the deny policy works even when the client filter is bypassed.
  - The agent's service account can't write to `sales` through the BigQuery API.
  - A call naming another project is overwritten to ours.
  - A `SELECT` that calls a remote function or `EXTERNAL_QUERY` fails or is harmless. Google says read-only `SELECT` can still invoke remote functions.
  - An aggregation over a large table returns a small result, and a result of 3,000 rows or more is reported as possibly incomplete.

## Things to know

- **Cost cap is lost.** The 2 GiB byte cap and labels in `analytics/executor.py` don't apply on the MCP path. The server also caps results at 3,000 rows and 3 minutes. I'd add a BigQuery custom quota for the service account, since I can't confirm the server has a byte limit.
- **`mcp==1.17.0` looks wrong for ADK 2.12.0.** The skill's notes say ADK 2.12.0 needs `mcp>=1.24,<3`. `AGENTS.md` forbids changing pins in a feature change, so I left it. Run `pip check` or the resolver before merging.
- **Argument names are unconfirmed.** I couldn't confirm the server's project argument name (`project_id` or `projectId`), so the callback handles both. Check it against the first live `tools/list`.
- **Import behaviour.** `agent.py` now calls `google.auth.default()` at import, so importing it without credentials fails. The tests don't import it.

## Questions I couldn't ask, and the assumptions I made

- **Deny policy scope:** should it apply to everyone in the project or only the agent's service account? I documented the agent's service account as the assumption; Google's example uses everyone.
- **Toolbox retirement:** I assumed it happens after cutover, so `deploy/tools.yaml` is still there.

## Left undone

- Running the tests and any live or IAM changes.
- Deleting `deploy/tools.yaml`.
- Finance-reviewed templates, which I didn't touch.
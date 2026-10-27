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

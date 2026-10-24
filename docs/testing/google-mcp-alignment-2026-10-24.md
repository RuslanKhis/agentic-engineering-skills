# google/mcp alignment — 24 October 2026

Source note: [google/mcp comparison](../research/google-mcp-comparison-2026-10-24.md).

## Changed journey

`adk-sql-agent-engineering`, the managed BigQuery MCP branch, with the
interoperability skill's section on Google's managed MCP servers.

## Fresh-agent trial

A fresh agent with only the skill packages pointed a synthetic ADK 2.12
analytics agent at Google's managed BigQuery MCP server under the rule that
the agent must be unable to write, and produced the wiring, the IAM changes
as reviewable files (not executed), truncation handling, offline tests and a
Toolbox decision.

Result: 11 tests passed against a fake server built on `mcp` 2.3.0, driving
the real `Runner` and `McpToolset` with a scripted model under a socket
guard; a model call to the filtered-out `execute_sql` came back as an error
event and the server recorded no call. Two mutations (restoring
`execute_sql` to the filter, disabling the cap disclosure) each made a test
fail. The inventory listed the fake server; `terraform fmt -check` passed;
`terraform validate`, the live inventory and every IAM change were not run.

Ease: 3 of 5. The managed-server paragraph was the right content; the
wire-level facts were missing.

## Frictions and fixes (same day)

Facts for 1 to 7 were read from Google's pages on 24 October 2026 (the
BigQuery MCP page of 2026-10-21, its tool reference of 2026-10-15 and the
IAM page of 2026-10-22).

1. Tool names. Fixed: the nine tools of the tool reference, and which a
   read-only agent may list.
2. The project argument. Fixed: `project_id`, pinned in a
   `before_tool_callback`.
3. The shape of a capped result. Partly fixed: the documentation does not
   describe it, so the skill gives the signals to treat as capped and asks
   to confirm the shape on the first approved live call.
4. Authentication to Google's server. Fixed: a per-request token through
   `header_provider` and the `bigquery` scope; `tools/list` needs no
   authentication there.
5. The deny-policy command. Fixed: the documented `gcloud iam policies
   create` command and attachment point, the sample's invalid trailing
   comma, and the routed IAM skill; the role needed to manage deny policies
   is not stated on the page and was not added.
6. Enablement. Fixed: the server is on when the BigQuery API is.
7. Write-proofing beyond MCP. Fixed: the three roles, no data-editing role,
   and why the MCP deny does not cover the identity's other paths.
8. The SQL skill's contract probe asserts ADK 2.8.0. Fixed by saying so at
   the command, with the scripted-`BaseLlm` alternative for newer pins.
9. pytest absent. Fixed in the same sentence (`python -m unittest`).
10. The interoperability skill's `verified-against` 2.8.0 beside 2.12
    facts. Not changed: the compatibility page dates each fact.
11. The pair-with-`tool_filter` rule lived only in the SQL skill. Fixed: the
    interoperability section states it.
12. ADK 2.12's own deprecation warning for `MCPTool`. Not changed: harmless.

## Limits

No Google endpoint was called and no IAM change was made.

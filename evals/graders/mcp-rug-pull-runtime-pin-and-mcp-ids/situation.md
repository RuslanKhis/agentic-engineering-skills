# mcp-rug-pull-runtime-pin-and-mcp-ids: what the fixture holds

Standalone project `filings-research` (google-adk==2.12.0, mcp 1.18.0).

- `app/agent.py`: remote `McpToolset` over `StreamableHTTPConnectionParams` with a list
  `tool_filter=["search_filings", "get_filing"]` and `tool_list_cache_ttl_seconds=None`; a second
  `McpToolset` with `StdioConnectionParams` for `pdf-extract-mcp`, no tool_filter, running inside
  the agent's own container (`Dockerfile`), hence with the agent's service identity (A4).
- `mcp/ledgerline.tools.json` + `scripts/check_mcp_inventory.py` + CI job `mcp-inventory`:
  definitions are compared only in CI (pull request and weekly), never at runtime, so a
  post-deploy description change is missed (A1). A list tool_filter cannot recompute hashes; a
  predicate tool_filter can (A1).
- `app/inventory.py` provides `tool_hash`/`diff_inventory` (stdlib) the agent can reuse for the
  runtime predicate. Tests `tests/test_inventory.py` pass offline. ADK/MCP not installed; Runner
  test with a server double changing a description mid-session must be reported as not run.
- A3: OWASP MCP Top 10 ids (MCP03:2025 tool poisoning beside LLM03/ASI04; MCP05/MCP09 for the
  bundled stdio server), cited by id with link, beta status, MCP06 title drift, no copied text.

# Filings research agent

Answers analysts' questions about company filings for Corrib Capital. Google ADK 2.12 on Cloud
Run (one container).

- Ledgerline's hosted MCP server (`https://mcp.ledgerline.example/mcp`, Streamable HTTP) supplies
  filing search and retrieval. We do not run or control it.
- A local PDF extraction MCP server (`pdf-extract-mcp`) runs over stdio inside the same container
  (see `Dockerfile`).
- `mcp/ledgerline.tools.json` is the tool inventory recorded from Ledgerline's server;
  `scripts/check_mcp_inventory.py` lists the server's tools in CI and fails on any difference.

## Tests

```bash
python -m unittest discover -s tests -t .
```

google-adk and the MCP SDK are not installed in this environment and there is no network.

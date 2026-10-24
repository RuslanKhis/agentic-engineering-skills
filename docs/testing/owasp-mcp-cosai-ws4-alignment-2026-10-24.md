# OWASP MCP Top 10 and CoSAI WS4 alignment — 24 October 2026

Source note: [comparison](../research/owasp-mcp-cosai-ws4-comparison-2026-10-24.md).

## Changed journey

`adk-agent-security`, MCP supply chain: a remote server that changes a tool
definition after deploy, a stdio server in the agent's container, and
findings in OWASP MCP Top 10 terms.

## Fresh-agent trial

Run on 25 October 2026. A fresh agent with only the skill packages reviewed
and fixed a synthetic ADK 2.12 agent that used a third-party Streamable HTTP
MCP server (name-list `tool_filter`, CI manifest diff) and a stdio PDF
server in the same container. It installed google-adk 2.12.0, mcp 2.3.0 and
pytest, and wrote a loopback fake vendor server that can change a tool's
description and schema mid-session, and a fake stdio PDF server.

Result: a run-time pin (`PinnedDefinitionFilter`) that recomputes the
inventory's hashes from `raw_mcp_tool`, admits a tool only when allowlisted
and matching the manifest, and withholds a changed one; name prefixes on
both toolsets; a tool gate that confines PDF paths to the session's upload
folder and keeps PDF text out of vendor arguments. It declined moving the
PDF server to its own service (cloud resources and approval; recommended),
a third-party scan (it uploads tool descriptions), a paid red-team run and
a reader redesign.

`pytest`: **12 passed**; the same suite against the original wiring failed
8 (all security tests) and passed 4. Inspector before and after: the
`mcp_unfiltered` and `egress_capable_tool` rows cleared; the stdio row
remains until the server moves. `mcp_tool_inventory.py --diff` after the
change reported `rug_pull_signal: true` and exited 0. Findings were filed
as MCP03 (beside LLM03, ASI04, AML.T0110), MCP02 and MCP10, MCP06, MCP08 and
an open MCP01/MCP07 item.

Ease: 3 of 5.

## Frictions and fixes (same day)

1. The ids had no scope, so MCP03 and MCP02 were guesses. Fixed: a table,
   in this skill's own words, from finding to id (no OWASP text copied).
2. The pin is checked once per invocation, because `get_tools_with_prefix`
   caches the filtered list for the invocation (2.12.0 `base_toolset.py`,
   checked). Fixed.
3. No code or field mapping for recomputing hashes, and no statement that
   the manifest is not the allowlist. Fixed: `model_dump(by_alias=True,
   mode="json", exclude_none=True)` into the inventory's `describe_tool`,
   with a parity test; allowlist and manifest both required.
4. `--diff` exits 0 on a rug-pull signal. Fixed: `--fail-on-diff` exits 3,
   with a test, documented where CI runs the diff.
5. The manifest never wrote `ui_resource_uri` or `ui_visibility`, so the
   diff's MCP Apps check could not fire end to end; a defect from the
   ext-apps change on the same day, found by reading. Fixed, with a test.
6. Inspector: a callable filter hid the egress row; no row for unprefixed
   toolsets; `all_three: false` for a three-leg agent. Fixed:
   `mcp_filter_predicate_review` marks the trifecta incomplete and
   `mcp_toolsets_without_prefix` fires. `file:line` pointing at `tools=` is
   unchanged.
7. "Replace every McpToolset with a double" conflicted with testing a
   filter. Fixed: a loopback fake server when the control lives in the
   toolset.
8. No pointer for moving the stdio server. Fixed: `deploy-adk-on-google-cloud`.
9. The skill's frontmatter says it was verified against 2.8.0 while the
   text sets a 2.12.0 floor. Not changed: the field records the package's
   last full verification; the 2.12.0 claims carry their own dates.

## Limits

No live server or model ran; the vendor's run-time behaviour is not pinned
by any of this.

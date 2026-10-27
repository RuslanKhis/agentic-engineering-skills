# MCP Apps charts: decisions, assumptions, open items

Why nothing showed: (1) ADK 2.12.0's McpToolset session doesn't advertise
`io.modelcontextprotocol/ui`, so the partner served `get_chart_text` and never
`get_chart` (`partner/tools-list-recorded-from-our-agent.json`); (2) ADK never fetches or
renders the HTML and `adk web` 2.12.0 doesn't show MCP widgets; (3) `useAgentStream.ts`
only read text parts; (4) ADK ignores `_meta.ui.visibility`, so with no filter `refresh_chart`
would reach the model as soon as the server lists it.

Changes: `agent.py` name allowlist (drops `refresh_chart`) + `show_chart` tool;
`mcp_app.py` UI-capable backend session, view reader, app-call guard; `server.py` widget SSE
event and `/api/mcp_app/{view,call}`; `useAgentStream.ts` widget items.

## Questions nobody could answer here, and the assumption taken
- Will the partner list UI tools to ADK's session if asked? Assumed no; asking them to is the
  simplest fix and would make ADK emit `render_ui_widgets` itself (the stream code already reads it).
- Which `mcp` version is installed, and does `ClientSession(extensions=...)` exist? Assumed
  mcp 2.x per the interop notes; `ui_session()` is unverified.
- Is the page origin for the sandbox available (a second origin)? Assumed not yet.
- Auth for the new endpoints: unspecified, left as a TODO.

## Not done
- React component hosting the view (AppBridge with a `null` client, different-origin sandbox
  proxy, CSP from `_meta.ui.csp`, wait for `initialized`, route `oncalltool` to
  `/api/mcp_app/call`). Charts will not appear until it exists.
- Nothing was run: google-adk, mcp, fastapi are not installed and no tool to execute was available.
- `show_chart` result carries a `_widget` marker the model also sees; harmless, could be stripped.
- Manifest of reviewed partner tools and a fake-server test of `show_chart`/`call_tool_for_app`.

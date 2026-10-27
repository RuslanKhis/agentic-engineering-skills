Charts won't render yet. The backend and stream wiring is written, but the React component that hosts the chart page doesn't exist. None of it has been run: I had no way to execute code, and google-adk, mcp and fastapi aren't installed.

**Why nothing showed**
- ADK 2.12.0's MCP session doesn't advertise `io.modelcontextprotocol/ui`. The partner therefore gave your agent `get_chart_text` and never `get_chart`, which matches `partner/tools-list-recorded-from-our-agent.json`.
- ADK doesn't fetch or render the chart HTML, and `adk web` 2.12.0 doesn't show MCP widgets.
- `useAgentStream.ts` only read text parts.
- ADK ignores `_meta.ui.visibility`. With no `tool_filter`, `refresh_chart` would reach the model as soon as the server lists it.

**What I changed**
- **`insights/agent.py`**:
  - `tool_filter` is now an allowlist of `get_sales_figures` and `get_chart_text`, so the model can't call `refresh_chart`.
  - I added a `show_chart` tool that fetches the chart through a second, UI-capable session. The instruction tells the model to use it for trends.
- **`insights/mcp_app.py`** (new): a backend MCP session that declares the UI extension. It reads the `ui://` page, relays calls from the chart view, and refuses any tool whose visibility lacks `"app"`.
- **`insights/server.py`**:
  - The SSE stream now emits an `mcp_widget` event when `show_chart` runs.
  - New `/api/mcp_app/view` and `/api/mcp_app/call` endpoints.
- **`web/src/chat/useAgentStream.ts`**: yields widget items from the new event, and from ADK's own `render_ui_widgets` if the partner ever lists UI tools to ADK. It drops widgets whose result was an error.
- **`tests/test_mcp_app.py`** (new): stdlib-only tests of the visibility guard against the partner's tools list.
- **`NOTES.md`** (new): the reasoning, the questions below, and the open items.

**Questions I couldn't ask, and what I assumed**
- Will the partner list UI tools to ADK's session if you ask? I assumed not. If they will, that is the simplest fix.
- Which `mcp` version is installed, and does `ClientSession(extensions=...)` exist? I assumed mcp 2.x, so `ui_session()` is unverified.
- Do you have a second origin available for the chart sandbox? I assumed not yet.
- What auth should the new endpoints use? Unspecified. I left a TODO.

**Left undone**
- **React chart host**: it needs `AppBridge` with a null client and a sandbox proxy on a different origin. It must also apply the CSP from `_meta.ui.csp`, wait for the view's `initialized` notification, and route `oncalltool` to `/api/mcp_app/call`.
- **Verification**: nothing has been run, including the new unit tests.
- **Fake-server tests and manifest**: there is no fake-server test of `show_chart` or the app-call path, and no committed manifest of the reviewed partner tools.
- **`_widget` marker**: the model also sees it in the `show_chart` result. It's harmless but could be stripped.
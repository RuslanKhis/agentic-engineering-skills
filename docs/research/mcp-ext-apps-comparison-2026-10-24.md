# MCP Apps (ext-apps) compared with this toolkit — 24 October 2026

## Scope and snapshot

A review of [modelcontextprotocol/ext-apps](https://github.com/modelcontextprotocol/ext-apps)
at commit `266a9e3` (2026-10-23; release 2.0.3), cloned on 24 October 2026
into its own directory and read, never run. Files read: `README.md`,
`LICENSE`, `.claude-plugin/marketplace.json`, the `mcp-apps` plugin manifest
and its four skills' front matter (`add-app-to-server` in full),
`specification/2026-01-26/apps.mdx` (Stable) and the draft revision,
`src/server/index.ts`, `src/app-bridge.ts`, `src/constants.ts`,
`examples/basic-host/src/{sandbox,implementation}.ts` and
`examples/qr-server/server.py`. Checked against the installed google-adk
2.12.0 (`events/ui_widget.py`, `tools/mcp_tool/{mcp_tool,mcp_toolset,session_context}.py`,
the `adk web` bundle) and `mcp` 2.3.0 (`client/session.py`).

**Licence.** A composite file: new code and specification contributions
Apache-2.0, earlier contributions not yet relicensed MIT, documentation
CC BY 4.0 (hence GitHub's NOASSERTION). All attribution-only; the skills
paraphrase with links and copy nothing, and the companion skills are routed.

**Maintenance.** Active; release 2.0.3 on 2026-09-25, wire protocol
unchanged between 1.x and 2.x.

**Conclusion.** The memo was right that ADK carries the MCP Apps resource
(`UiWidget(provider="mcp")`, present since 1.27.0) and that a custom frontend
needs a renderer ticket, and wrong that MCP Apps "reach ADK end to end":
ADK attaches the widget and renders nothing, `adk web` shows nothing, ADK
never advertises the UI extension (so a server that checks client
capabilities sends text-only tools), and ADK ignores tool visibility (so the
model can call tools meant only for the view, which the extension forbids).
Our consumption reference said ADK renders the widget; it now says what ADK
does and the two host duties left to the project, the inventory reads both
meta keys and flags app-only tools, and the frontend skill has the renderer
contract.

## Method

ADK behaviour was confirmed in the installed 2.12.0 source (the
`ClientSession` construction without `extensions=`, the unread
`McpTool.visibility`, both meta keys) before editing. One scenario case
covers the journey; the fresh-agent trial is in the
[testing record](../testing/mcp-ext-apps-alignment-2026-10-24.md).

## Drift corrected

- `mcp-consumption.md` said MCP App resources "are rendered as a
  `UiWidget`"; ADK attaches them and renders nothing.
- `mcp_tool_inventory.py` read only the nested `_meta.ui.resourceUri`, said
  "ADK 2.8.0 renders it", and ignored visibility.

## Imported, by specialist

- **adk-agent-interoperability.** What `McpTool` attaches, the missing
  capability advertisement and visibility handling with the `tool_filter`
  and backend rules; the inventory's flat-key support, `ui_visibility` and
  `mcp_app_tool_not_for_model` finding (one new test); in exposure, the
  companion skills for servers that ship UI and the text-fallback rule.
- **adk-frontend-integration.** "Render an MCP App widget": serving the HTML
  through the backend, `AppBridge` with a `null` client and backend-routed
  handlers, a sandbox on a different origin with CSP from `_meta.ui.csp`,
  nothing sent before `initialized`, and the app as the demo surface.

- **From the trial.** Widgets attached to error results, the
  unreferenced-page finding and the UI fields in the manifest diff, the
  failed-start behaviour of a stdio server, the stdio default environment
  (in `adk-agent-security`), and the backend-session remedy for servers that
  gate UI tools.

## Routed, not copied

The `mcp-apps` plugin's `add-app-to-server` and `create-mcp-app` skills, in
the consult-the-installed form, at the decision in the exposure reference.

## Vendored assets

None.

## Left out, with reasons

- Exposing a local server with `cloudflared`: against private by default.
- The `add-app-to-server` step that clones the repository and runs
  `basic-host`, and `basic-host` as a production host (the README says there
  is no supported host implementation).
- The example servers' third-party CDN allowances.
- MCP-UI as a host SDK: rated low in the memo; named only when a ticket asks.

## Limits

Nothing was executed against a live server; the capability and visibility
gaps were read in source. Event serialisation of `render_ui_widgets` over
`/run_sse` and ADK main after 2.12.0 were not checked. Three of the four
companion skills were read from their front matter only.

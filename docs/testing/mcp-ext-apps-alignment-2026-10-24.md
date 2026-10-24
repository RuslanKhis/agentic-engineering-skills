# MCP Apps (ext-apps) alignment — 24 October 2026

Source note: [ext-apps comparison](../research/mcp-ext-apps-comparison-2026-10-24.md).

## Changed journeys

`adk-agent-interoperability`, consuming an MCP server whose tools ship MCP
Apps UI; `adk-frontend-integration`, rendering a `provider == "mcp"` widget.

## Offline evidence

`mcp_tool_inventory.py` now reads both MCP Apps meta keys, records
`ui_visibility`, flags app-only tools (`mcp_app_tool_not_for_model`) and,
after the trial, MCP App pages no tool references
(`mcp_app_resource_unreferenced`), and its manifest diff counts the UI
fields as definition. The helper suite has 46 tests, three of them new.

## Fresh-agent trial

A fresh agent built, offline on google-adk 2.12.0 and mcp 2.3.0, a fake
vendor MCP server (a chart tool with a UI resource, an app-only
`rebalance_preview`, a model-only text tool, and a `--gate-ui` mode that
hides UI tools from clients without the extension), the ADK wiring, a
backend bridge and offline tests, and ran the inventory.

Result: 18 tests passed. ADK attached the widget and the React app ignored
it, as the skill predicted; the gated mode reproduced the missing-capability
case; a `tool_filter` predicate on visibility plus a `before_tool_callback`
kept `rebalance_preview` from the model (a scripted call got an error and
the server logged no call). The inventory reported the expected findings;
its diff against the gated server showed no change, which the trial flagged.
A TypeScript `AppBridge` host was written from memory and not compiled.

Ease: 3 of 5.

## Frictions and fixes (same day)

1. The interoperability `SKILL.md` did not mention MCP Apps. Fixed in mode
   (b).
2. ADK 2.12.0 attaches the widget to `isError: true` results too (the skill
   said "successful"). Fixed in consumption and the renderer contract.
3. A stdio server that fails to start yields no tools rather than a tool
   error dict. Fixed in the failure table.
4. "Spawns a process with the agent's own environment" was wrong: the `mcp`
   SDK passes a small default set plus `env=`. Fixed in the security
   supply-chain table, with the list from `mcp` 2.3.0.
5. No remedy for a server that gates UI tools, and no way to see it. Fixed:
   the `mcp_app_resource_unreferenced` finding, the vendor and
   backend-session remedies, and the capability payload.
6. The manifest did not pin `_meta.ui`, so dropped UI or a visibility change
   passed the diff. Fixed: the diff compares `ui_resource_uri` and
   `ui_visibility`; test added.
7. The manifest keys stdio sources by the full command line, and the notes
   still named ADK 2.8.0's `mcp<2` pin. The keying is unchanged (the
   single-target diff already ignores it); the note is updated with the
   MCP inspector source's change.
8. The renderer contract lacked the capability payload, the MIME type and
   the payload's `meta` key. Fixed for those three; the `AppBridge`
   constructor and sandbox message contract stay with the ext-apps
   specification and were not restated.
9. The scripted-model Runner pattern lives in another skill. Not changed.
10. Whether to reuse ADK's session for `resources/read`, and an anyio
    cancel-scope error in tests. Fixed: a separate backend session that
    declares the extension, opened and closed in one task.
11. The frontend routing table named only A2UI for widgets. Fixed.

## Limits

No live vendor server, no browser; the TypeScript host was not compiled.

## Correction, 25 October 2026

The manifest diff compared `ui_resource_uri` and `ui_visibility`, but
`build_manifest` never wrote them, so a run against a real server could not
report an MCP Apps change; only the unit test with hand-built manifests
did. The OWASP and CoSAI trial found it by reading the source; the manifest
now pins both fields when a tool declares them, with an end-to-end test
([record](owasp-mcp-cosai-ws4-alignment-2026-10-24.md)).

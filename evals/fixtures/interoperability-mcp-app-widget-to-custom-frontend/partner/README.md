# Partner analytics MCP server notes (from their docs, 2026-10-18)

Chart tools ship MCP Apps UI (`ui://` resources). The server registers its UI
tools only for clients that advertise the `io.modelcontextprotocol/ui`
extension; other clients get text-only equivalents. `tools-list-with-ui-capability.json`
is from their docs; `tools-list-recorded-from-our-agent.json` is what our agent saw.

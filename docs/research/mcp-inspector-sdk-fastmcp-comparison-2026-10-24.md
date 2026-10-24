# MCP Inspector, python-sdk and FastMCP compared with this toolkit — 24 October 2026

## Scope and snapshot

A review of [modelcontextprotocol/inspector](https://github.com/modelcontextprotocol/inspector)
at commit `0cac110` (release 2.12.0, 2026-10-21; MIT moving to Apache-2.0,
docs CC BY 4.0), [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)
at `2af9e30` (v2.3.0 line; MIT) and [PrefectHQ/fastmcp](https://github.com/PrefectHQ/fastmcp)
at `37301f9` (v4.1.3; Apache-2.0), each cloned on 24 October 2026 into its
own directory and read, never run. Files read are listed in the
interoperability skill's sources. Spikes, offline, in a scratch environment
with `mcp==2.3.0` and `google-adk==2.12.0` from PyPI: the published Inspector
CLI against a local `MCPServer` on both protocol eras; `to_mcp_server` with a
scripted model under the default and legacy client modes; and the toolkit's
inventory helper against a modern-only server.

**Maintenance.** All three active, each still patching its previous major.

**Conclusion.** The memo's claims about these tools hold. The review's main
result is that two things in this toolkit were wrong. The exposure
reference promised that `to_mcp_server` keeps one conversation per
connection; on 2026-07-28, the default for every current client, each call
starts a fresh ADK session (reproduced: `user_turns=1, 1` by default,
`1, 2` in legacy mode), and no server setting can switch an era off. And the
inventory's `server/discover` fallback probed with the old version and read
the wrong field names, so a modern-only server failed and the fixture that
tested it shared the mistake. Both are fixed. The Inspector CLI is now a
scriptable CI cross-check with recorded exit codes rather than a manual
step.

## Method

Facts were read from the SDK documentation and source, then confirmed by
the spikes; the continuity result was re-run by the maintainer before the
edit, and the helper fix was checked against the spike's modern-only server
(exit 1 before, exit 0 with version and server info after). One scenario
case covers the journey; the fresh-agent trial is in the
[testing record](../testing/mcp-inspector-sdk-fastmcp-alignment-2026-10-24.md).

## Drift corrected

- `mcp-exposure.md`: conversation per connection holds on the handshake
  revisions only.
- `mcp_tool_inventory.py`: probes `server/discover` at 2026-07-28, reads
  `supportedVersions` and `_meta["io.modelcontextprotocol/serverInfo"]`; the
  fixture now answers in the schema's shape and refuses an older probe, and
  the test asserts the server identity. Its protocol note no longer names
  only ADK 2.8.0.
- `validation.md`: the Inspector was "an independent manual cross-check"
  whose token storage "was not verified"; both are now settled.
- `compatibility.md`: the helper's discover support is no longer
  "best-effort".

## Imported, by specialist

- **adk-agent-interoperability.** The continuity split by era and the
  multi-turn options; legacy sessions per process and session affinity; the
  in-process two-mode test with `mcp.Client(server)`; the Inspector CLI
  command, era flag, exit codes, error envelope and storage isolation; the
  modern-flag elicitation failure.
- **adk-tool-auth-and-secrets.** FastMCP's provider verifiers need a pinned
  audience, and custom OAuth storage is plaintext without
  `FernetEncryptionWrapper`.

## Routed, not copied

None.

## Vendored assets

None.

## Left out, with reasons

- Inspector web, TUI and the skill-verification modes: no ADK decision
  depends on them.
- Stored-auth flags against a developer's store and automatic browser
  opening: weaker than private by default.
- The python-sdk's `--spec-version` conformance legs on alpha.11; the toolkit
  already pins the alpha.12 requirement run.
- FastMCP-internal changes and its provider catalogue.

## Limits

Streamable HTTP continuity was not observed (in-memory and stdio only);
Inspector exit codes 3, 4 and 6 were read, not provoked; FastMCP was read,
not installed; ADK's handling of an `input_required` result under the modern
flag was not tested.

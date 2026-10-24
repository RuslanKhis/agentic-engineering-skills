# MCP Inspector, python-sdk and FastMCP alignment — 24 October 2026

Source note: [comparison](../research/mcp-inspector-sdk-fastmcp-comparison-2026-10-24.md).

## Changed journey

`adk-agent-interoperability`, exposing an agent as an MCP server (mode c):
the multi-turn contract by protocol era, the exposure checks and the
independent-client step in validation; the inventory helper's modern path.

## Offline evidence

The inventory's `server/discover` fallback was fixed and its fixture
corrected to the 2026-07-28 schema (the fixture now refuses an older probe
and the test asserts the server identity). Against the spike's modern-only
server the helper exited 1 before the fix and 0 after, reporting
`server/discover`, 2026-07-28 and the server identity. The maintainer
re-ran the `to_mcp_server` continuity probe before editing (default client
`user_turns=1, 1`; legacy `1, 2`).

## Fresh-agent trial

A first trial run was stopped when work was paused and was discarded; the
trial was re-run from scratch in a new directory.

A fresh agent with only the skill package took `triage_agent` served with
`to_mcp_server` on google-adk 2.12.0 and mcp 2.3.0, promised hosts on the
default `mcp.Client` a multi-turn contract, proved it offline and wrote CI.
Following the skill, it replaced the stock server with a hand-built
`MCPServer` passing a server-minted, caller-bound, expiring conversation
handle.

Result: 9 tests passed under network denial, each in `auto` and `legacy`
mode (two turns gave `user_turns` 1 then 2 on both eras; forged, foreign and
expired handles returned `isError`; the stock `to_mcp_server` gave 1, 1 on
modern and 1, 2 on legacy). The inventory listed and diffed the server (exit
0). The Inspector CLI 2.12.0 listed tools in both eras (exit 0, the era
confirmed by capturing the stdio traffic), a stdlib hash comparison matched
the committed manifest on both and caught a deliberately altered one
(exit 1), and over loopback HTTP two Inspector calls continued the
conversation and a guessed handle exited 5. The conformance suite
0.2.0-alpha.12 ran per revision: 45 passed and 23 failed under 2025-11-25,
114 and 56 under 2026-07-28, each exiting 0 once its baseline was complete.
The GitHub Actions workflow parsed and its manifest steps replayed locally;
it has not run on GitHub.

Ease: 3 of 5.

## Frictions and fixes (same day)

1. The handle-based server had principles but no code; `MCPServer` hides
   ordinary exception text. Fixed: a short sketch with `get_access_token()`
   and `ToolError`, and why `ToolError`.
2. Unclear whether the hand-built server meant Shape 2. Fixed: it wraps the
   whole agent; Shape 2 is per tool.
3. The copy rule said "header intact (MIT)" but the script has no header.
   Fixed: copy the skill's MIT `LICENSE` beside it, or pin a commit.
4. The inventory cannot check the 2026-07-28 era on a dual-era server.
   Fixed: stated, with the Inspector's modern era as the check.
5. With a baseline, WARNING checks count as unexpected failures, and check
   ids are only in `checks.json`. Fixed in the conformance section, with the
   trial's observation.
6. Two more Inspector files under the home directory. Fixed:
   `MCP_CATALOG_PATH` and `MCP_CLIENT_CONFIG_PATH`.
7. The Inspector does not print the negotiated era. Fixed: stated.
8. Each Inspector stdio call starts a new server; multi-turn needs HTTP; a
   module server needs `--cwd`. Fixed.
9. No producer-side fake-test rows. Fixed: three rows in the exposure
   checks.
10. "Builds a `FastMCP` server (MCP SDK 1.x)" beside 2.12 observations.
    Fixed: on `mcp` 2.x ADK imports `MCPServer` under that name. The
    skill's `verified-against` front matter is unchanged; it records what
    the skill was last fully re-verified against.
11. No CI YAML. Fixed: the Inspector step with exit-code branching.

## Limits

The workflow did not run on GitHub; streamable HTTP continuity on the stock
`to_mcp_server` was not observed; the handle store is in memory.

# agents-shipgate alignment — 26 October 2026

Source note: [comparison](../research/agents-shipgate-comparison-2026-10-26.md).

## Changed journey

`adk-release-engineering`, a CI check that stops a pull request from
silently changing what the production agent can do, through
`adk-agent-security`'s inspector.

## Fresh-agent trial

A fresh agent built an ADK 2.12 support agent (a refund tool with
confirmation, a capability callback, an `McpToolset` with a name filter),
then a branch with a coding agent's kind of change, and one branch per
change. It built a gate that runs the security inspector from the base
commit, with a workflow file and code owners (nothing pushed), and also
tried agents-shipgate 1.2.0. No network or model was used.

| Change | Inspector `--compare` | agents-shipgate `diff --application` |
| --- | --- | --- |
| confirmation removed | 3, gate changed | 0, partial, no row |
| email tool added | 3, tool added, egress up | 0, partial, one row |
| MCP filter widened | 3, toolsets changed | 0, partial, no row |
| `Workflow` running a subprocess | 1, unread graph named | 0, no row |
| callback removed | 3, callbacks and gates changed | 0, partial, no row |

The trial's gate failed every planted change, passed a README-only pull
request and the labelled branch, and reported NOT RUN when the base had no
inspector. agents-shipgate's `verify` in strict mode failed even the
README-only pull request. Project tests: 2 passed. Ease: 3 of 5.

## Frictions and fixes (same day)

1. A partial run (exit 1) hid capability changes (exit 3), and a project
   with a `Workflow` failed every pull request. Fixed: exit 3 takes
   precedence, and `unread_paths` lets the gate block only when a changed
   file was not read (tested).
2. No way for CI to force review of an unread `Workflow`. Fixed by the same
   rule.
3. No CI steps: base-tree copy of the check, who applies the label, the
   bootstrap pull request. Fixed, with a snippet.
4. Where to vendor the inspector. Fixed: `.agents/skills/`, which it skips.
5. Only shipgate's `diff` was described, not its `verify`. Fixed.
6. The capability gate was not routed from the release skill. Fixed.
7. A base `google-adk` install lacks `mcp`. Not changed: the
   interoperability skill already says to add the `mcp` extra.
8. The inspector treats a "get" tool as egress, so the trifecta was already
   present on base. Not changed: a labelled heuristic.

## Limits

The CI workflow was not run on a hosting service; nothing was pushed.

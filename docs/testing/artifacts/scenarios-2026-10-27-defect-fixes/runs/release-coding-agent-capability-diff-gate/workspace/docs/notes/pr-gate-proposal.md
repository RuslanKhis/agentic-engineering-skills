# Gate for agent-authored PRs (proposal, Lena, 2026-10-23)

Most PRs are now opened by coding agents. Last week one PR added the weekly
reporting agent, which emails refund data, and nobody noticed it in review
until after merge.

Proposal from the platform channel: add `agents-shipgate diff --application`
(1.2.0) to CI against `main` and block the PR when it reports a change. Is that
enough on its own?

## Answer (2026-10-27)

No. Per the offline trial recorded in the adk-release-engineering skill
(`references/ci-eval-gates.md`; not re-run in this session), 1.2.0
`diff --application` exits 0 whatever it finds, so it cannot block anything, and
it reported no change when `require_confirmation` or a `before_tool_callback`
was removed or an `McpToolset` filter was widened. Any `McpToolset` makes its
comparison partial, and this agent has one. Its `verify` command is no better
here. It is useful as an advisory step because it hashes tool bodies and the
hosts they call, but it is not a gate.

The gate is `.github/workflows/capability-gate.yml`: the adk-agent-security
inspector run on base and head with `--compare`, run from the base commit.
Exit 1 means a tool, gate, callback, toolset, sub-agent or executor changed,
and the PR then needs the `capability-change-approved` label from a maintainer.
A changed `Workflow` file (the inspector does not read the graph) also blocks,
which covers the reporting-agent incident. NOT RUN blocks like a failure.

Known gaps:
- A change to a function the Workflow calls (`app/services.py`, `app/clients/`)
  is not seen. CODEOWNERS on those paths is the only control until a test covers it.
- A remote MCP server changing a tool definition is not seen by the diff.
  `mcp/catalogue-tools.json` has the wrong shape for `mcp_tool_inventory.py
  --diff` (`sha256` rather than `description_sha256` and `input_schema_sha256`)
  and its hashes look like placeholders. Regenerate it with `--out` against the
  real server, then add `--diff <manifest> --fail-on-diff`.
- The inspector is not vendored yet, so the first PR reports NOT RUN.
- Branch protection must require the check, and the workflow and `.agents/`
  need CODEOWNERS review, otherwise a PR can edit its own gate.

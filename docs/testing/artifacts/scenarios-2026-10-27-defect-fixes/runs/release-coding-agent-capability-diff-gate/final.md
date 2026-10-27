No, `agents-shipgate diff --application` isn't enough on its own. I've added a CI gate that blocks these PRs, but none of it has been run: shell access was disabled this session, so the workflow is untested.

**Why shipgate alone fails.** This comes from the adk-release-engineering skill's notes on an offline trial of 1.2.0. I did not re-run it here.
- `diff --application` exits 0 whatever it finds, so it can't block a PR.
- It missed a removed `require_confirmation`, a removed `before_tool_callback` and a widened `McpToolset` filter.
- Any `McpToolset` makes its comparison partial, and your root agent has one.
- Its `verify` command doesn't help, and it offers to `apply-patches` its own manifest, which would let the coding agent approve its own change.
- It is still useful as an advisory step, because it hashes tool bodies and the hosts they call. I left it out of the workflow because I couldn't confirm its flags offline.

**What I added**
- `.github/workflows/capability-gate.yml` runs the adk-agent-security inspector on the base and head commits with `--compare`. The inspector comes from the base commit, so a PR can't rewrite its own judge.
- A change to a tool, gate, callback, toolset, sub-agent or executor needs the `capability-change-approved` label. The label counts only if a maintainer or admin applied it, and a new push drops it.
- A changed `Workflow` file also blocks. That is the reporting-agent case, because the inspector names Workflow nodes but doesn't read them.
- If the comparison doesn't complete, the check fails rather than passing.
- `.github/CODEOWNERS` covers the agent, tools, `mcp/`, `.github/` and `.agents/`. `@OWNER/platform-leads` is a placeholder.
- `docs/notes/pr-gate-proposal.md` now has the answer and the known gaps.

**Not done**
- **Nothing was run.** I read the inspector's `--compare` source and exit codes to write the workflow. I didn't execute the workflow or the inspector.
- **Inspector not vendored.** I couldn't copy it into `.agents/skills/adk-agent-security/`, so the first PR will report NOT RUN until you vendor it.
- **Branch protection.** The check must be marked required, and `.github/` and `.agents/` need code-owner review. Otherwise a PR can edit its own gate.
- **Remote MCP changes.** A remote MCP server changing a tool's definition isn't covered. `mcp/catalogue-tools.json` has the wrong shape for `mcp_tool_inventory.py --diff` and its hashes look like placeholders. Regenerate it against the real server, then add `--diff ... --fail-on-diff`.
- **Indirect Workflow changes.** A change to code the Workflow calls, such as `app/services.py` or `app/clients/`, isn't seen. CODEOWNERS on those paths would help; I didn't add them.

**Assumptions** (nobody was available to ask):
- The `capability-change-approved` label name is mine.
- Maintainer or admin permission counts as "code owner".
- PRs come from the same repo, not forks.
- CI has network access to the GitHub API.
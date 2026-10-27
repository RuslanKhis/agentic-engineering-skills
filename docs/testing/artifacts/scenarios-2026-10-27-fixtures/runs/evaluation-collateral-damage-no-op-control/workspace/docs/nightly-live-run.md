# Nightly live run

Every night at 02:00 the GitHub Actions workflow `nightly-live` runs the 30 cases in
`eval_cases/cases.json` against the real model (gemini-3.5-flash on Vertex AI) and the real MCP
servers: the filesystem server over a copy of last week's receipts and the GitHub server against
the `finance-approvals-staging` repository.

Recorded today: the pass rate per case and overall, the date, and the model name. Results go to
the `nightly-results` artifact.

## What to record (proposed, not yet implemented)

A pass rate per case and a model name cannot explain a failure or show what changed between nights.
Record, per case and trial, so that a result can be audited and a regression traced:

- **Trials.** Run each case k times (k >= 3 to start) and record every trial's outcome. Report pass^k
  per case and overall; a case with fewer than k completed trials is NOT RUN, not a pass. Timeouts,
  Runner exceptions and `max_llm_calls` stops are recorded as failed trials, never dropped.
- **Tool-call trace.** Every call in order: tool name, which server it came from (database tools,
  filesystem, GitHub), arguments, the response or error, and whether it was a success. The multiset of
  successful write calls (`file_expense`, `update_profile`, `create_issue`) is compared with the case's
  expected writes, so a changed-and-restored profile is still seen.
- **End state, whole fixture.** The `tests/case_checks.snapshot`/`diff` of all 14 tables, per trial, on a
  freshly reset database; store the diff itself (tables, rows, fields), not only pass/fail. For GitHub,
  list the issues in `finance-approvals-staging` before and after each trial (the repo is not reset by
  a database fixture) and record the created ones; any issue in a case that expects none is a failure.
  The filesystem tools are read-only through `tool_filter`; still record the receipts manifest hash,
  because "last week's receipts" is a different input every week.
- **Final response** text and termination reason, per trial, so claims can be checked against the diff.
- **Provenance per run.** Requested and returned model version, generation settings, instruction text
  hash, `cases.json` version and hash, git commit of the agent and graders, the resolved dependency
  list (google-adk, google-genai, mcp), the database fixture hash, and the start time.
- **MCP server identity.** Both servers are currently unpinned in practice: `npx -y
  @modelcontextprotocol/server-filesystem` takes whatever is latest, and `ghcr.io/github/
  github-mcp-server:v0.9` is a tag that can be re-pushed. Pin the package to an exact version and the
  image by `@sha256:` digest (a change in `expense_agent/agent.py`, not made here), then record per run
  the version the server reports in its initialize response, the image digest actually run
  (`docker image inspect`), and a hash of each server's `tools/list` output (names, descriptions,
  input schemas, after `tool_filter`). A changed hash explains a behaviour change with no code change.
- **Per-case denominators.** The number of cases, trials, and graded components that actually ran,
  next to every rate.

Also run the do-nothing control (`tests/test_grader.py`) before the live cases each night; if it passes
an action case, the grader is broken and the live result is not trusted.

Known gap: none of the 30 cases exercises the over-limit path that opens a GitHub approval issue, so
the GitHub server is recorded but its effect is not graded until such cases exist.

Staging incident, 2026-10-16: during a manual staging session the agent changed emp-102's approver
while filing a claim. The nightly run that night was 30/30 green.

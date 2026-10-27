# Nightly live run

Every night at 02:00 the GitHub Actions workflow `nightly-live` runs the 30 cases in
`eval_cases/cases.json` against the real model (gemini-3.5-flash on Vertex AI) and the real MCP
servers: the filesystem server over a copy of last week's receipts and the GitHub server against
the `finance-approvals-staging` repository.

Staging incident, 2026-10-16: during a manual staging session the agent changed emp-102's approver
while filing a claim. The nightly run that night was 30/30 green, because it only recorded a pass
rate and the graders only looked at the expense row.

## What to record (replaces "pass rate, date, model name")

Pass rate stays as a summary, never as the only record. Write one JSON line per case trial and one
manifest per run, all into the `nightly-results` artifact.

Per trial (case id, trial number):
- **End state of the whole database**: the snapshot before and after, the set of tables that
  changed, and the row-level diff of each (`tests/case_checks.snapshot`). The grader compares this
  with the reference run's end state, so a stray write to `profiles` is a recorded failure.
- **Every tool call in order**: name, arguments, response status, and whether it counted as an
  effective mutation (`file_expense`, `update_profile`, GitHub `create_issue`). Grade the
  multiset of effective mutations against the reference.
- **GitHub side effects**, which SQLite does not show: issues and comments in
  `finance-approvals-staging` before and after the trial, the created issue's number and URL, and
  the cleanup done. Tag everything a trial creates with the run id and trial number.
- **Filesystem side effects**: a hash of the receipts copy before and after (the server is limited
  to `read_file` and `list_directory`; a changed hash means the filter was bypassed).
- Final response text, stop reason (finished, `max_llm_calls`, timeout, exception), model calls,
  tokens and elapsed time. A trial that ended for any reason other than the agent finishing scores
  zero and stays in the file.
- Grader failures as text, so the reason for a red case is in the artifact.

Per run (manifest):
- Exact versions: `google-adk`, `google-genai`, Python, and the resolved model version if Vertex
  reports one, not just `gemini-3.5-flash`.
- **Filesystem server version.** `npx -y @modelcontextprotocol/server-filesystem` floats, so the
  server can change between nights. Pin it (`@modelcontextprotocol/server-filesystem@<version>`)
  and record the `serverInfo` version from the MCP `initialize` response.
- **GitHub server image digest** (`sha256:...`), taken from the pulled image. The tag
  `ghcr.io/github/github-mcp-server:v0.9` can be re-pushed; pin the digest in `agent.py` and record
  it.
- A hash of each server's `list_tools` result (names, descriptions, schemas), to separate a tool
  schema change from a model change.
- Hashes of the agent instruction, `eval_cases/cases.json` (version 3) and the schema in `db.py`.
- Receipts copy: its source date and tree hash. "Last week's receipts" moves, so a changed input is
  visible.
- Case counts: planned, executed, passed, failed, not run. A case with no result row, a skipped
  trial or a missing grade is `not run`, never a pass.

Reliability: run each case k times (suggest k = 5) and report pass^k per case and overall, with the
count of cases that completed all k trials. Report the number of cases with a forbidden-write
failure separately; one such failure fails the night whatever the pass rate.

## Controls

- The do-nothing control (`tests/test_cases.py::test_do_nothing_control_fails_every_filing_case`)
  runs on every change offline, and may also run in the nightly job (it needs no model). A filing
  case it passes is vacuous.
- `tests/test_case_checks.py` holds the grader's own controls: reference passes, do-nothing fails,
  an extra approver change fails, a reverted edit fails, a write to an unlisted table fails.

## Known gap this does not close

`update_profile(employee_id, approver_id)` in `expense_agent/tools.py` accepts any employee id
and does not check it against the signed-in user, so the agent can still make the incident's edit.
Case c14 scripts exactly that edit. With the new grading it fails, and it should stay failing until
the tool refuses to edit another employee's profile (or the profile tools are removed from this
agent).

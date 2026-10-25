# AppWorld and MCPMark alignment — 25 October 2026

Source note: [comparison](../research/appworld-mcpmark-comparison-2026-10-25.md).

## Changed journey

`adk-agent-evaluation`, grading an outcome by end state and curating cases,
plus preparing a live run.

## Fresh-agent trial

A fresh agent with only the skill packages built a stand-in ADK 2.12
support agent (status update, comment, reassignment over an eight-table
SQLite store with `updated_at` on every row) whose tests checked only the
ticket's status, then made the suite catch collateral damage, proved no
action case passes when the model does nothing, and said what to record for
a live run with an unpinned `npx` server and a Docker tag. It installed
google-adk 2.12.0 and pytest; no network, npx, Docker or model was used.

Result: a grader that replays the reference on a fresh store, diffs all
eight tables at table, record and field level with per-field ignores,
checks the changed-table set, compares successful mutating calls and
multiplies the components; a strict scripted model; four action cases with
six correct agents; an MCP pin check and a live-run record template.

`pytest`: **29 passed**, twice. Correct agents 6 of 6 pass; deliberately bad
agents 5 of 5 fail (another ticket reassigned twice over, a user record
edited through an extra tool, a reassign-and-back detour, a wrong status).
The old status-only check passed 4 of the 5 and passed the do-nothing
agent on 2 of 4 cases; the new grader fails it on all 4. The user-record
edit was caught only by the whole-store diff.

Ease: 3 of 5.

## Frictions and fixes (same day)

1. The do-nothing control was not reachable from the routing table.
   Fixed.
2. The end-state section was one 600-word paragraph. Fixed: four numbered
   steps.
3. Raw or filtered diff for the table set. Fixed: raw, with named
   exceptions.
4. "Mutating calls whose result was a success" was undefined for ADK, and
   an unlisted tool escapes the multiset. Fixed: write- and
   irreversible-tier tools whose response the tool's contract marks a
   success; the diff is the backstop.
5. How to resolve versions, the tool-list hash, and an unpinned example in
   the interoperability skill. Fixed.
6. "Ended for any reason other than the agent or the user stopping" was
   not mapped to ADK. Fixed: Runner exception, `LlmCallsLimitExceededError`,
   `abort_signal`, harness timeout (checked in 2.12.0 source).
7. The do-nothing rule against non-action cases. Fixed: non-action cases
   are expected to pass it.
8. Whether a deterministic suite needs pass^k. Fixed: repeated trials are
   for live runs.
9. google-genai resolved 2.33.0, not 2.32.0. Fixed: both dates recorded.
10. Two expected log messages with a scripted model. Fixed (both checked in
    2.12.0 source).
11. How to grade what the agent had to communicate. Fixed: deterministic
    checks against the final response and the end state, or a listed judge.

## Limits

No live run; the pinned versions in the trial's tests were format examples.

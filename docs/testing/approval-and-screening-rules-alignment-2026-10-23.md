# Approval and screening rules alignment — 23 October 2026

*What changed, what was checked, and what a fresh agent did with it.*

## Change

See the [comparison note](../research/approval-and-screening-rules-comparison-2026-10-23.md).
In the repository: unanswered approvals rejected on the next run and
fail-closed approval rules in the guardrails skill's human-review reference;
four screening-placement rules in the security skill's agency reference; a
strict scripted-model rule in the evaluation skill's deterministic-tests
reference; atomic call-and-result groups and the three compaction points in
the optimise skill's context-window reference. After the trial: headings
over the approval rules, the ADK hook and the state-write rule for the
unanswered-approval check, the response-screen placement in the
sensitive-data skill's boundaries reference, the routing row naming screen
placement, the guardrails inspector's interpreter rule reconciled with the
engineer's, the compatibility gate's fallback when the SDK is absent, and the
engineer's `__getattr__` sentence reworded. **Two scenario cases**
(`guardrails-unanswered-approval-and-screening-placement`,
`optimise-compaction-atomic-groups-three-points`).

## Automated checks

`scripts/validate_skills.py` after the edits: **22 packages**, 0 errors,
0 warnings; `git diff --check` clean. The full `scripts/check_repo.py`
counts are in the README entry for this date.

## Fresh-agent trial

One trial, in a subagent with a fresh context, the 22 packages readable as
installed skills, no Google skill installed, no credentials, no network, no
ADK installed, on a synthetic project, without the expected answers.

### Guardrails: an approval executed after a weekend, and a screen that ran beside the tool

The project: an ADK 2.12 refund agent whose incident report showed a Friday
approval request answered by Monday's "any news?" and refunded, and an
output screen running beside the model call so the tool had fired before the
screen rejected the answer.

What the agent did: an SDK-free approval record in session state with a
deadline, closed as rejected by any new message and expired by the
deadline, reassigned at the top-level key; fail-closed amount validation;
explicit states with one execution per approval and an unknown-outcome
state for a provider exception; the screen moved into the request path with
the verdict stored per invocation and a second boundary in
`before_tool_callback`; wiring through `before_agent_callback`,
`after_model_callback` and `before_tool_callback`; 27 offline tests run on
two interpreters including the Friday-to-Monday incident, 3 Runner tests
reported as not run; a notes file naming the 2.12.0 assumptions and the
decisions a product owner still owns.

Ease rating: **4 of 5**. The exact rules existed; they sat deep in long
paragraphs and the routing for the screen half was ambiguous.

Frictions and what was done the same day:

| Friction | Fix |
| --- | --- |
| The routing table had no row for a response screen's position relative to tool dispatch | The sensitive-data row names it |
| The unanswered-approval rule sat in a 350-word paragraph | Two headings split the section |
| The rule named the mechanism but not the ADK hook; how to write the record into state safely was unsaid | Both stated: `before_agent_callback` classifying `adk_request_confirmation` responses, read in 2.12.0's confirmation flow, and top-level reassignment for state deltas |
| The guardrails skill said to run the inspector with the project's Python; the engineer says any 3.11+ interpreter | Reconciled in the guardrails step |
| The compatibility gate's "inspect its installed source" had no fallback without the SDK | The fallback is stated |
| "Screen before function calls are dispatched" was implied, not stated | Stated in the boundaries reference |
| The `__getattr__` sentence read as required | Reworded: `adk web` discovers `agent.py:root_agent` without it |
| The 2.8.0 baseline in two compatibility files; the "SDK absent" wording for the inspection step | Left: the baseline framing is stated per package; the inspector reports `null` |

## What this does not establish

The Runner tests did not run; the deadline value and the review service are
product decisions the trial could only name.

## Second trial: a summariser plugin that broke call pairs

One more trial on the same source covered the compaction rules, in a
subagent with a fresh context and no SDK, on a synthetic project: an ADK
2.12 assistant with a trimming plugin that sliced the last N contents and
produced requests with a dangling function call, and nobody able to say when
compaction ran. The agent moved the trim decision into an SDK-free policy
that cuts only at turn starts and always keeps the current turn, reported
unmatched calls rather than pruning them, added the `App` that carried the
plugin and token-based compaction (the README claimed compaction the code
did not have), wrote a design note mapping the three points, and ran 17
offline tests with 3 SDK tests reported as not run. Rated **3 of 5**: the
rule was correct but buried mid-sentence in a section about request
composition, and found by search.

| Friction | Fix |
| --- | --- |
| No routing row for a trim plugin or a dangling-call rejection | The optimise row names both |
| The atomic-group rule sat in the middle of a 15-line item with a stray line break | Its own section, "Trim or summarise without breaking call pairs", with the turn-start cut recipe |
| The three points were not mapped to ADK mechanisms | A table: `before_model_callback`, `App` events compaction, a store job, each with its test |
| "Prune orphans" against "never drop pending approvals" | Report, do not prune, until the owning flow records a call as abandoned |
| A Runner built from `root_agent` drops the plugin and compaction silently | Stated |
| The shipped compaction tests skip unless the version is exactly 2.8.0; the database-backend crash report | Left: re-pinning the test needs the 2.12.0 source run; the backend report stays in the pitfalls |

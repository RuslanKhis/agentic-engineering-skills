# Validate instruction work

Use the target's test runner and interpreter. Keep doubles at the model
boundary so the real loader, templating path and callbacks run. Never
promote a reviewer's reading of a prompt into evidence that the agent
behaves differently.

## What counts as evidence

| Tier | Artefact | What it supports | What it does not |
| --- | --- | --- | --- |
| Offline rendered | contract test output: instruction rendered with fixture state, sections present, no unresolved placeholder, prompt version recorded | the text is well-formed and renders under the pinned templating rules | anything about model behaviour |
| Offline recorded request | `system_instruction`, `contents` and `tools_dict` captured by a `before_model_callback` with a scripted model | what the model would receive: transfer text, static/dynamic placement, tool declarations, global prefix | the model's response to it |
| Hostile fixture | decision and trajectory unchanged with and without embedded instructions, scripted or recorded model | the data framing and the code guards hold together | immunity to injection |
| Live evaluated | adk-agent-evaluation run on the development set with category counts before and after, prompt version and exemplar IDs recorded | the change moved the targeted category without growing others | generalisation beyond the set (holdout, once, at the end) |
| Not run | anything above that was not executed | nothing; list it | |

A prompt diff is none of these. A screenshot of one good answer is not a
tier.

## Per mode

**Design a new instruction.** Contract test passes; the linter shows no
unresolved placeholders and no mandated calls; the first development run has
retained outputs and an error-analysis table; the thousand-word budget holds.

**Review.** Findings cite the linter code, the file and line, the rendered or
recorded text that shows the problem, and the observable check that would
show the fix. Say which findings are mechanical (templating, deprecated
field) and which are judgments (altitude, phrasing).

**Tool-use calibration.** Trajectory cases per situation pass; recorded
request shows declarations and prose agree; the tool mix was checked against
the limitations page before prose changed.

**Routing.** Recorded parent request shows the rendered agent list; routing
set with one ambiguous case per sibling pair passes; no sibling pair exceeds
the overlap threshold without a written reason.

**Model migration.** Baseline on the old model, unchanged prompt on the new
model, then one note at a time; configuration iterations handed to
adk-model-and-output-contracts and run separately; every run records model,
prompt version and settings.

**Prompt as code.** Loader test, contract test and hostile fixture pass
offline; `CHANGELOG.md` has a dated entry; the next evaluation record carries
the version.

## Linter limits

The linter reads source with `ast` and text files; it does not import the
project, so it cannot see instructions built at runtime, state keys written
by code, or tool names created by toolsets. It resolves module-level string
constants, `textwrap.dedent`/`inspect.cleandoc` wrappers and `.format` or
f-string literal parts within one file; cross-file references are reported as
`instruction_unresolved_reference`. Its phrasing heuristics (shouting
density, prohibitions, contradictions, tool-name mentions) are regular
expressions for a reviewer to confirm. For a prompt file the tool list is
unknown, so backticked names are listed under `tools_mentioned` instead of
being judged against `tools=`. A partial scan (exit code 1) names the
limit reached; inspect the omitted area by hand.

## Completion report

List the files changed, the exact commands run and their results, the ADK
version the mechanics were checked against, the evaluation run ID (or "not
run"), and unverified behaviour. Separate **offline rendered**, **offline
recorded request**, **hostile fixture**, **live evaluated** and **not run**.
On a second invocation, reuse the existing loader, tests and changelog rather
than creating a parallel prompt location.

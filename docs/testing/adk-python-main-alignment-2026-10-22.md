# google/adk-python main alignment — 22 October 2026

*What changed, what was checked, and what a fresh agent did with it.*

## Change

See the [comparison note](../research/adk-python-main-comparison-2026-10-22.md).
In the repository:

- **Facts** from google/adk-python main (commit `ed76f94`) and, after the
  trial, the installed 2.12.0 package, cited to the file and version: the
  code-execution environment layer (`EnvironmentToolset` and its backends
  with their first versions and maintenance state), the GKE sandbox mode's
  import, the three constructor cases of the Agent Engine sandbox executor,
  the Cloud Run sandbox executor's `allow_egress` default and what its
  source does not say, how input files reach an executor and how a tool
  stages one, the synchronous `execute_code` contract, and the inspector's
  two blind spots, all in the security skill's agency reference; the
  maintainer skill's three anti-flake habits and the Runner, model and
  session signatures in the evaluation skill's deterministic-tests
  reference; the SQLite memory service, the bundled BigQuery skills and the
  reference wiring samples in the memory, SQL and workflow skills; the
  `.agents/skills` tree in the engineer's composition reference.
- **Two wording fixes** from the trial: the security compatibility table now
  says 2.8.0 is this toolkit's reference baseline, not the project's pin;
  the engineer's interpreter rule says to write tests the standard library
  runner can collect when that is the runner that will see them.
- **No routing line**: the repository's skills are maintainer tooling.
- **One scenario case** (`security-code-execution-environment-selection`).

## Automated checks

`scripts/validate_skills.py` after the edits: **22 packages**, 0 errors,
0 warnings; `git diff --check` clean. The full `scripts/check_repo.py`
counts are in the README entry for this date. No helper script, test or
`last-tested` date changed.

## Fresh-agent trial

One trial, in a subagent with a fresh context, the 22 packages readable as
installed skills, no Google skill installed, no credentials, no network, no
ADK installed, on a synthetic project, without the expected answers.

### Security: choosing an execution environment for a data helper

The project: a Cloud Run agent that runs model-written Python over uploaded
CSVs with `UnsafeLocalCodeExecutor` and a Daytona-backed
`EnvironmentToolset`, with a mail tool whose recipient the model chose. The
request named three constraints: no credential reachable from executed code,
data stays in the project's region, no model-chosen recipient.

What the agent did: wrote the review first as the skill orders, chose the
Agent Engine sandbox executor bound to a named sandbox resource in the
region, rejected the local executor, the Daytona backend, the container and
GKE executors and the built-in one with reasons tied to the constraints, kept
the Cloud Run sandbox as a fallback because the skill did not record its
metadata-server isolation; removed the environment toolset; moved the
recipient to identity with a domain allow-list, fail closed; a fail-closed
`before_tool_callback`; `require_confirmation` on the mail tool; five
`ast`-based execution-surface tests, sixteen policy tests, six scripted-model
Runner tests and one opt-in live probe, with the inspector run before and
after. Ran what it could on the interpreters at hand (29 passed, 7 reported
not run); left the SDK-dependent tests, the sandbox provisioning and the
mail transport open.

Ease rating: **3 of 5**. The executor table answered the central question;
the SDK shapes the fix and the tests depend on were missing.

Frictions and what was done the same day:

| Friction | Fix |
| --- | --- |
| The Cloud Run sandbox row said nothing about the metadata server; the Agent Engine constructor was "`sandbox_resource_name` or `agent_engine_resource_name`" with no resolution | Both rows rewritten from the 2.12.0 source: the three constructor cases with the region consequence; `allow_egress=False`, the 300-second timeout, and the statement that the source is silent on the metadata server with the probe to run instead |
| No skill said how a tool hands a file to an executor, nor whether `execute_code` is synchronous | A paragraph before the environment layer: the input-file state key, what the flow stages on its own, how a tool stages a file, the synchronous contract and base defaults, with the Runner test as the proof |
| The Horizon `internet_access` sentence read as an ADK executor option | Reworded as Horizon's own sandbox setting |
| `inspect_security_surface.py` did not flag the `EnvironmentToolset` path and dropped the mail tool's `egress` flag once its recipient parameter went | Recorded in the agency reference as the two rows to review by hand; the helper change with its tests is owed and listed below |
| The deterministic-tests reference gave procedure but no signatures | The 2.12.0 signatures of `BaseLlm.generate_content_async`, `InMemoryRunner`, `create_session`, `Runner.run_async` and `execute_code`, labelled with the version |
| "2.8.0 (pinned)" read as the project's pin | Reworded as the toolkit's reference baseline |
| The interpreter rule forced `unittest`-style tests without saying so | One clause added to the rule |
| The validation step asks for log evidence of denied calls even when observability is out of scope; the deploy skill has no sandbox material | Left as they are: the evidence requirement is the control's own test, and sandbox provisioning belongs to the security skill's executor table, which the deploy skill's identity table now points at through the agent-sandbox change |

Owed: an inspector rule for `EnvironmentToolset` and for senders whose
recipient comes from identity, with tests and a `last-tested` re-run.

## What this does not establish

The executor and context facts were read in the installed 2.12.0 package and
on main, not executed; the trial's six Runner tests and its live probe did
not run. The trial used one project shape.

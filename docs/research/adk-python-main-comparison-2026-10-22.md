# google/adk-python at main compared with this toolkit — 22 October 2026

## Scope and snapshot

A source-level review of [google/adk-python](https://github.com/google/adk-python)
at main commit `ed76f94` (2026-10-21), with tags `v2.8.0` (the toolkit's
baseline) and `v2.12.0` (2026-10-13) and commit `c2ff634` (2026-10-15),
cloned on 22 October 2026 with lazy blobs into its own directory and read,
never run. Licence: Apache-2.0, no NOTICE. The release facts (the 2.12.0
entries, the `adk eval` exit code, the 2.9.0 failed-node rerun, the judge and
optimizer defaults, the `mcp` pin, the Model Armor plugin's tool-output
screening) were handled in [Phase B](drift-fixes-2026-10-22.md) and the
[Toolbox note](mcp-toolbox-comparison-2026-10-22.md); this note covers the
rest of what the memo named: the execution environment and sandbox layer,
the maintainer skills under `.agents/skills`, the `contributing/samples`
tree, the bundled BigQuery skills, the SQLite memory service and the
primitives the skills never named.

**Conclusion.** The largest correction is to the memo, not to the skills:
the sandbox layer did not arrive with 2.12.0. `git tag --contains` on the
files shows `EnvironmentToolset` since 1.29.0, the Agent Engine sandbox
environment since 1.31.0, E2B since 2.3.0, Daytona since 2.4.0 and the Cloud
Run sandbox executor since 2.5.0; only OpenSandbox (2026-10-13, unreleased)
and the 2.12.0 sandbox lifecycle helpers are newer than the 2.8.0 pin. The
security skill's executor table was nonetheless missing all of it, and now
carries it with the residency and maintenance caveats. The maintainer
skill's flake habits, the samples as fixture-grade references, the bundled
BigQuery skills and the SQLite memory service were imported as facts; the
maintainer skills are described in the composition reference as a
collection a project may adopt, with this toolkit's division of labour.

## Method

Each path the memo named was listed and read; the first release containing
each file was established with `git tag --contains` on its first commit;
every imported fact cites the file and the commit. One scenario case and one
fresh-agent trial cover the executor-selection journey (see the
[testing record](../testing/adk-python-main-alignment-2026-10-22.md)).

## Drift corrected

- "ADK 2.12 grew a sandbox layer": most of the layer predates 2.8.0 (see
  above). Written with the first release of each surface.
- `EnvironmentToolset` is described in the memo as "execute, read_file and
  edit_file tools"; the package also ships a write-file tool
  (`tools/environment/_write_file_tool.py`).
- The memo's "Cloud Run sandbox code executor" is `CloudRunSandboxCodeExecutor`
  in `integrations/cloud_run`, usable only inside a Cloud Run container with
  sandboxes enabled (its docstring), not from elsewhere.
- The adk-agent-builder testing reference carries no version note; the
  memo's "checked against 2.6.2" could not be confirmed and is not repeated.

## Imported, by specialist

- **adk-agent-security.** The `GkeCodeExecutor(executor_type="sandbox")`
  dependency on `k8s_agent_sandbox.SandboxClient`; a `CloudRunSandboxCodeExecutor`
  row; a paragraph on the environment layer (`BaseEnvironment` methods, the
  toolset's four tools, the five backends with their first releases, the
  2.9.0 process-tree kill on timeout, the 2.12.0 lifecycle helpers), the
  rule that an environment is tiered as a write tool, Daytona's public
  maintenance notice, and the residency consequence of off-GCP backends.
- **adk-agent-evaluation.** The three flake habits from the maintainer
  testing reference and the samples tree as fixture-grade reference code.
- **adk-memory-architecture.** The 2.11.0 SQLite memory service, with what
  it does not provide.
- **adk-sql-agent-engineering.** The bundled `bigquery-ai-ml` and
  `bigquery-graph` skill folders as operating references for the SQL text.
- **adk-workflow-design.** The workflow and HITL samples as reference wiring.
- **adk-engineer.** A composition bullet for the repository's `.agents/skills`
  (`adk-agent-builder`, `adk-architecture`, `adk-debug`, `adk-review`,
  `adk-unit-design` and others), not installed with the package, with the
  division of labour.

## Routed, not copied

The maintainer skills are described, not routed in the standard form: they
live in the repository, not in a published collection, and a project adopts
them by cloning. The bundled BigQuery skills are referenced by path inside the
installed package.

## Vendored assets

None.

## Left out, with reasons

- `Runner.rewind_async`: already cited in the memory skill's sessions
  reference; nothing new.
- `_tool_call_integrity_plugin`: already in the security compatibility table
  (2.11.0).
- `google.adk.platform.time` and `uuid`: their purpose (deterministic replay
  under a durable engine) belongs to the Temporal source later in the
  programme, where it can be cited with the integration that uses it.
- The 2.12.0 "40% faster first model request" highlight: a vendor
  performance claim with no measurement here.
- OpenSandbox as a backend: unreleased at 2.12.0; named only.

## Limits

Read, not run. The first-release dates come from tag containment of the
first commit touching each file and would move if history were rewritten.
The maintainer testing reference was read as guidance, not executed. No
sandbox was created.

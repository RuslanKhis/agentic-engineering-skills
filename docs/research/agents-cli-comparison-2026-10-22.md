# Agents CLI 1.11.0 compared with this toolkit — 22 October 2026

## Scope and conclusion

A file-level review of a local snapshot of
[google/agents-cli](https://github.com/google/agents-cli) at version 1.11.0
(release notes dated 20 October 2026; the seven bundled skills all declare
1.11.0) against the 22 packages here, following the
[23 September refresh](agents-cli-comparison-2026-09-23.md) made against 1.5
and 1.6. Three readers compared one cluster each: the workflow, scaffold and
ADK code skills; the evaluation skill; and the deployment, observability and
publish skills, each also reading the CLI source for the commands and flags
the skills describe. Facts that changed a specialist's text were checked
against the current official page where the specialist records a URL;
everything else is cited to the snapshot and dated. Nothing was installed or
run.

**Conclusion.** The division of labour recorded in September still holds and
no command in this toolkit's text was wrong, but the integration was stale in
three ways. Version and date citations named 1.5, 1.6 or 1.8. Product and
repository names moved: the publish command is `agents-cli publish gemini`,
the product is "Gemini (formerly Gemini Enterprise)", the `adk@<name>` recipe
shortcut is gone and the recipe repository is now `google/adk-recipes`. And
the fact import done for Google's cloud skills on 21 October had not been
done for this collection: the ADK code cheatsheet, the evaluation formats and
the deployment defaults carry facts that change what a reader configures.

## Drift corrected

- The integration guide said "thirteen" of this toolkit's skills (22) and
  that it had no registration specialist (`adk-agent-interoperability` now
  owns the card and the registration mode); the `1.5.0` observability
  reference and the September comparison date were re-stated against 1.11.0.
- Eleven specialist files cited the repository by its old name, `adk-samples`;
  GitHub now redirects those pages to `google/adk-recipes`, so the live
  citations were renamed and the dated September notes were left as written.
- Three contradictions between our text and the CLI's behaviour were
  verified against the current documentation before any change: the Agent
  Identity baseline role (`roles/aiplatform.user` granted by the CLI versus
  `roles/aiplatform.expressUser` from the docs page), the role the Discovery
  Engine service agent needs on a Cloud Run A2A agent (`run.invoker` versus
  `run.servicesInvoker`), and whether an Agent Gateway binding can change
  after creation (the CLI updates it with an update mask). The deployment
  and interoperability references record what the documentation says and
  what the CLI does where they differ.

## What changed in Agents CLI since September that matters here

- New projects scaffold on `google-adk>=2.12.0` and
  `google-cloud-aiplatform>=2.2,<3`, set `GOOGLE_GENAI_USE_ENTERPRISE=true`,
  and default to `gemini-3.8-flash`; this toolkit's recipes were checked
  against 2.8.0, so version-dependent facts carry a confirm note.
- Agent Identity is the default for new Agent Runtime projects
  (`agent_runtime_identity_default: agent_identity`, 1.10.0); `deploy
  --dry-run` makes read-only cloud calls and exits non-zero on a definite
  problem (1.9.0); `--ingress`, `--key` (customer-managed encryption,
  create-only), `--framework` and label flags were added; Terraform and the
  imperative deploy must not own the same engine; `deployment_metadata.json`
  records the engine ID the CLI updates.
- The workflow skill now has eight phases with a hard gate before scaffolding
  and a recipe-study phase, forbids behavioural unit tests in the build phase,
  and maps product names to "Gemini platform". The scaffold skill dropped the
  RAG flags and templates; Live (voice) agents are five edits, not a template.
- The ADK code skill's cheatsheets cover the graph Workflow API with
  per-node interrupts, task-mode delegation, tool confirmation and
  resumability, memory write and preload tools, state prefixes, events
  compaction and context caching, managed agents and ambient triggers. The
  recipe catalogue adds a scheduled production-trace evaluator.
- Evaluation: Live mode, user simulation (`dataset synthesize`), `analyze`,
  `optimize`, `submit` and `results`; datasets are the Agent Platform
  `EvaluationDataset` shape and results are `results_<timestamp>.json`, so
  this toolkit's CSV result checker cannot gate them; `eval generate` writes
  only the cases that succeeded and still exits 0; bare metric names resolve
  to the latest version; the scaffold's judge runs on the agent's own model.
- Deployment and telemetry: each target's environment defaults, the
  completion-upload variables and sink table names, Agent Registry
  auto-registration of runtime agents, the `/api` passthrough, and
  registration defaults (ADK native on Agent Runtime, A2A elsewhere, Live
  agents unsupported).
- Usage telemetry is on by default since 1.9.0 (opt out with
  `AGENTS_CLI_TELEMETRY=0` or `DO_NOT_TRACK=1`), and extensions can ship
  skills into `.agents/skills/`.

## What was imported, by specialist

- `adk-workflow-design`: graph Workflow interrupts and resume rules,
  `Event(state=)` over context state, parallel workers, retry configuration,
  task mode disabled inside a Workflow.
- `adk-operational-guardrails`: the tool confirmation and resumability APIs
  and the three approval recipes, with the rule that the gate is code and
  resume is tested against the real session backend.
- `adk-memory-architecture`: memory write paths, preload versus on-demand
  recall, state prefixes, rewind scope, the cross-session-memory recipe.
- `adk-tool-interface-design`: task-mode wiring, the built-in search plus
  function tools caveat, Google's docstring conventions.
- `adk-model-and-output-contracts`: the output-schema-versus-tools
  contradiction stated with both readings, scaffold default model and
  backend variable.
- `optimise-adk-on-google-cloud`: events compaction and context cache
  settings.
- `adk-agent-evaluation` and `adk-release-engineering`: the dataset and
  result shapes, the gate a results file needs, the silent drop on generate,
  the identity seed, simulation and region rules, rubric groups and judge
  sampling, built-in tools absent from trajectories, metric version pinning,
  the judge-follows-model hazard, the SDK data point.
- `deploy-adk-on-google-cloud`, `adk-agent-observability`,
  `adk-agent-interoperability`: Agent Identity mechanics and defaults,
  gateway binding on update and the root-certificate build argument,
  Terraform versus imperative ownership, dry-run semantics, environment
  defaults and reserved variables, the passthrough URL, publish defaults and
  idempotency, Agent Registry auto-registration and flags, completion-upload
  variables and sink names, the 2.9.0 analytics regression as a vendor
  report, MCP gotchas for Cloud Run ID tokens.

## Routed, not copied

Each specialist now names the Agents CLI skill that operates its mechanism
at the decision it serves, in the same form used for Google's cloud skills:
the deploy skill names `google-agents-cli-deploy` when a manifest,
`deployment_metadata.json` or generated Terraform exists; observability names
`google-agents-cli-observability` for the upload bucket, dataset and sinks;
interoperability names `google-agents-cli-publish`; evaluation and release
engineering name `google-agents-cli-eval` for the Agents CLI tier commands;
the workflow, guardrails, memory, tool-interface, instructions, model and
frontend skills name `google-agents-cli-adk-code` and its recipes when the
project has `agents-cli-manifest.yaml`.

## Left out

The ban on behavioural unit tests (this toolkit's scripted-model Runner tests
assert effects, not wording); temperature 0 as a flakiness fix; "use the
latest model" without a lifecycle date; mean-only comparison and per-case
fitting as regression proof; public-by-default Cloud Run Terraform with an
all-traffic ingress; a `latest` secret version in generated infrastructure;
project-wide storage administration grants; global `gcloud config set`;
force-unlocking Terraform state; a fail-open agent-card fetch; and the
telemetry default, which is a disclosure, not guidance.

## Limits

A local snapshot; the catalogue and CLI change weekly. Facts marked vendor
guidance were not exercised. Two fresh-agent trials covered a focused change
and a deployment ticket in a synthetic Agents CLI project; see the testing
record for 22 October 2026.

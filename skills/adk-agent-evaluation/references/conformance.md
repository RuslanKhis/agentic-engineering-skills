# ADK conformance recording and replay

Use this mode to detect changes against a reviewed exchange baseline. It complements behavioural evaluation; it does not prove that the baseline is correct. Inspect the project read-only first. The commands below are specific to the verified ADK 2.8.0 workflow. Check installed CLI help and plugin contracts on another version; preserve the target's pins rather than silently upgrading.

## Establish the boundary

Identify the agent import root, conformance root, expected cases, server URL, session store and every tool's external effects. Inspect existing recordings before proposing replacement. A case directory contains `spec.yaml`; recording generates `generated-recordings.yaml` and `generated-session.yaml` beside it. Adapt the specification to the actual agent, synthetic messages and trusted initial state; no particular refund fixture or identity is required.

Recording makes live model calls. Before running, show the exact project/account or Developer API route, region, model, case paths, commands, invocation/time/retry bounds and cost bound. Obtain explicit approval on an isolated target, reusing prior approval only for the same scope. Replacing a baseline and deleting its files also require confirmation under this skill's safety rules. Implementation permission does not authorise deployment, provisioning or cleanup.

Replay can execute ordinary tools. Verify that every mutating integration is a fake or an explicitly approved isolated service before running it. Stored model responses are not a guarantee of zero network access.

## Record

Set `AGENT_ROOT` to the directory ADK Web serves, `CONFORMANCE_ROOT` to the directory containing the selected case directories, and `CONFORMANCE_PORT` to the client's expected port. ADK 2.8.0's demonstrated client expects port **8000**. For another port, inspect supported client URL configuration first; do not invent a CLI option. Verify that the endpoint belongs to this task.

Adaptation command using those configured variables:

```bash
adk web "$AGENT_ROOT" --port "$CONFORMANCE_PORT" \
  --extra_plugins=google.adk.cli.plugins.recordings_plugin.RecordingsPlugin \
  --extra_plugins=google.adk.cli.plugins.replay_plugin.ReplayPlugin
```

Both plugins are needed. Repeat `--extra_plugins`; a comma-separated list fails to load correctly in the tested version. Start only an owned server, record its PID and impose an execution deadline. Do not stop unrelated processes to free the port.

From a second terminal, enter the target working directory and activate the same project environment before running the approved recording:

```bash
adk conformance record "$CONFORMANCE_ROOT" none
```

The positional `none` selects no environment-simulation file. Recording replaces generated files. Validate each expected file is nonempty and parses against installed `Recordings`/`Session` schemas. Inspect ordered exchanges, stable arguments, tool outcomes and a meaningful final session result. Do not assume a fixed exchange count: an application callback may render the final response without another model call. Record hashes and review/accept the baseline before replay.

## Replay and inspect

Reset only owned synthetic backend state with confirmed scope; a new session alone may retain business effects. Restarting an owned process resets only process-local fakes. Configure an external-network-denied replay environment where the integration permits, allowing required loopback connections and removing usable provider credentials from that child process. Keep denial logs separate from guard self-tests.

```bash
adk conformance test --mode=replay --streaming-mode=none "$CONFORMANCE_ROOT"
```

For ADK 2.8.0, replay supplies recorded Gemini responses and checks current model requests. Ordinary tools may execute before their recorded responses are supplied onward. Therefore validate actual effects independently; replay does not establish live model quality or actual-tool-result equality. Do not assume live conformance mode is implemented.

## Completion

Require the expected **nonzero** test count, all intended cases passed and no unexpected skips. Exit zero with missing recordings/zero tests is incomplete evidence. Confirm baseline hashes unchanged, real orchestration/backend outcomes and a truthful final result. Claim no external calls only with suitable guard/transport evidence, not historical token metadata. Report substituted boundaries.

Propose cleanup separately and obtain confirmation for exact owned servers, sessions and generated files; existing same-scope cleanup approval can be reused. Verify session and event removal where applicable. Preserve pre-existing resources and credentials, and disclose provider-retained data that local deletion cannot erase.

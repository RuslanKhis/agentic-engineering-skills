# Diagnose Agent Runtime deployment boundaries

Use this reference when source packaging, configuration, prerequisite checks or
an interrupted deployment behave differently from local tests. Read
[runtime-lifecycle.md](runtime-lifecycle.md) for ownership and operation rules;
this reference turns those rules into targeted investigations. Adapt the
project's existing deployment interface rather than adding another deployer.

The concrete SDK observations below come from ADK 2.8.0 and AI Platform SDK
1.153.1, with Google GenAI 2.19.0. They explain the retained source-deployment
campaign; inspect the installed target version before applying them. Source,
container and in-memory-object deployment are different paths.

## Start at the boundary that can explain the symptom

| Symptom | Boundary to inspect | Useful next check |
| --- | --- | --- |
| Local example works, deployed import fails | Staged package and generated archive | Compare required imports and package data with actual archive members; a helper elsewhere in the checkout may never have been uploaded. |
| Local tools are mock but deployed tools are real | Mode selection before module import | Inspect explicit mode settings and imports that change behaviour when mocks are absent; test the packaged layout in a fresh process. |
| Changing an environment variable changes nothing | Actual model/client constructor or deployment adapter | Trace the value through the consumer, serialisation and effective configuration; distinguish hosting region from model endpoint. |
| Deployment tests pass but submitted settings differ | Real SDK request serialisation | Exercise the installed generator and serialiser with transport doubled; inspect the outgoing spec, including zero-valued limits and environment entries. |
| Preflight passes but a hosted tool receives a permission error | Deployed workload identity and tool resource | Verify the identity and exact required access for that operation; operator access does not establish it. |
| Repeating setup creates another build | Setup reconciliation | Count create/update mutations across two fresh invocations and compare the saved source/configuration identity. |
| Deletion reports a parser error but the runtime disappears | Accepted operation identity | Reconcile the exact operation from provider evidence before considering another mutation. |

## Follow configuration into the artefact and request

Keep a small evidence table for each changed value: intended value, code that
consumes it, generated representation and independently observed effective value.
For example, a capacity field belongs in the provider deployment configuration;
an application retry setting belongs in the constructed model/client. Neither is
proved by finding its name in an environment template.

For the recorded source path, the useful inspection order is:

1. **Resolve entrypoint and imports.** Identify the intended `App`, agent, profile
   selection and startup command. Trace how the generated ADK API server loads
   the application. Merely importing `root_agent` can miss App-level behaviour.
2. **Stage the required source.** Use an explicit package allowlist. The retained
   companion staged only `__init__.py`, `agent.py` and `requirements.txt`, then
   ADK generated the Dockerfile and serving scaffolding. That three-file list is
   historical, not suitable for every application. Add a required helper and its
   data deliberately; record the resulting source change.
3. **Inspect the actual upload.** The recorded SDK serialised an inline source
   archive. Inspect archive member names and selected synthetic contents without
   extracting untrusted paths. Confirm required modules, dependency declarations
   and generated startup settings. Check synthetic credential/receipt markers
   are absent, along with unintended mocks and developer caches. An allowlist
   function returning the right names does not prove the uploader used it.
4. **Inspect the serialised request.** Retain a sanitised representation of the
   outgoing source and deployment spec. In this baseline, SDK dictionaries and
   wire payloads can use snake_case and camelCase; environment values can appear
   as a list of name/value entries. Test the actual emitted representation rather
   than making a permissive parser that accepts any guessed shape. Verify
   `min_instances=0` survives serialisation as well as max instances, CPU,
   memory, concurrency, profile, attempt limits and run limits where applicable.
5. **Verify effective configuration after an authorised deployment.** Compare
   provider state with the planned spec and bind it to the same owned resource.
   Packaging and serialisation tests establish what was submitted, not provider
   acceptance, successful startup or the deployed identity's permissions.

The historical path required no customer staging bucket. Verify the target
upload path before adding bucket provisioning or bucket cleanup. Provider-owned
build/image infrastructure can still exist behind an inline-source deployment.

Keep dependency extras in this chain. The recorded AI Platform SDK's `adk`
extra constrained ADK below 2.0; the tested application selected `agent_engines`
and pinned ADK separately. See [compatibility.md](compatibility.md). A direct pin
does not retain transitive resolution, and a newer documentation example does
not prove compatibility with an older installed SDK.

### Keep runtime and model locations separate

In the retained deployment, the generated Dockerfile used the selected project
and runtime region, while the application's `Gemini` constructor explicitly used
`location="global"`. The runtime environment passed profile and attempt/run
controls without adding duplicate project/location entries to the serialised
deployment environment. Inspect the installed CLI's treatment of those fields
before changing them: an environment file can supply deployment inputs, while
explicit CLI arguments or a model constructor take precedence elsewhere.

Record the resulting runtime region and model endpoint separately. Changing
one does not demonstrate that the other changed, and a global model endpoint is
not a regional processing guarantee. Preserve a target's legitimate endpoint
choice rather than reproducing this lab's settings automatically.

## Reproduce import and packaging differences offline

Run startup checks in a fresh process with the intended profile set before the
first application import. The companion once selected its real runner too late:
the agent had already been constructed with mock tools. A boundary test stopped
at construction of the managed-session service and inspected the selected model
there, without making a cloud request.

There is a second distinction: its agent also selects real mode when local mock
imports are unavailable. A clean deployment archive therefore behaves differently
from a checkout even with identical-looking environment variables. For a target
application, prefer explicit production mode and test the packaged import layout;
avoid using accidental import failure as proof of the operator's intent. Preserve
an existing offline teaching mode when it is still required.

A focused offline reproduction should:

- Copy only the intended source into temporary staging, excluding checkout-only
  helpers. Use a temporary home and isolate inherited Google/Vertex/agent
  configuration in the child process so cached local state cannot satisfy a
  missing prerequisite. Leave the user's global environment and credentials alone.
- Supply explicit synthetic configuration. Install no hooks into the user's
  normal application process; intercept authentication, model and control-plane
  transports before application code can reach them, and fail unexpected network
  access. Treat unfamiliar application imports as executable code.
- Run the real startup/import selection, ADK generator and SDK serialiser for the
  boundary being changed. Capture their outputs with transport doubles. A fake
  `adk` executable printing a success ID does not test source generation.
- Assert observable consequences: expected package members, active profile,
  preserved App configuration, emitted spec, accepted-operation persistence and
  mutation counts across repeat invocations. Include a private-marker exclusion
  case and a missing-required-helper failure.

The historical preparation used a clean declared installation and `pip check`;
it passed 43 offline tests, then 47 after the deletion-parser repair. Reusing an
available environment today is a valid local check, but is not another fresh
installation or hosted verification. Record the actual environment used.

## Interpret prerequisites without widening the task

Separate evidence for CLI operator, ADC identity, ADC quota project and deployed
workload identity. The companion preflight obtained an ADC access token to check
availability; that alone did not prove the account or quota project matched.
The live campaign checked that match separately, then used an existing managed
runtime identity and existing grants. Successful deployment did not establish
access to an optional historical-data table.

Classify API inspection into three outcomes: a successful complete listing with
the required API present; a successful listing showing it absent; or unknown
status because the read failed. Only the second supports proposing activation
of that missing API. A permission error cannot authorise activation, broader IAM
or a new service account. Keep explicitly approved activation separate from
deployment when the target interface permits it.

Report prerequisite completion at its actual scope: existing project, billing,
API availability and credentials. Model quota, workload permissions, source-build
readiness and fresh-project activation each need their own evidence. Continue
offline packaging and tests while a missing prerequisite blocks live work.

## Choose recovery from persisted state

Use this table after checking receipt integrity and the owned target through
[runtime-lifecycle.md](runtime-lifecycle.md). Preserve primary failure details
alongside recovery results.

| Persisted/observed state | Next action | Completion evidence |
| --- | --- | --- |
| Accepted create/update operation is pending | Resume bounded reads of that operation; keep dependencies available. | Terminal operation result recorded before deciding on the resource. |
| Submission intent exists but acknowledgement/operation ID is missing | Reconcile provider operation/audit evidence with the original target and submission. | An exact accepted operation or authoritative non-acceptance evidence; one empty list is insufficient. |
| Source update ended in failure | Settle known operations, inspect the surviving owned runtime, then perform authorised cleanup or a separately planned repair. | Original outcome retained and owned resource state independently established. |
| Completed setup matches source, ownership and effective spec | Verify the existing deployment in a fresh invocation. | No additional create, update or build submitted. |
| Source, ownership marker or deployed spec changed | Compare the change and reconcile ownership/update intent. | An explicit approved update/recovery plan; deleting local receipts does not create ownership. |
| DELETE accepted but response parser rejected its operation path | Recover the exact operation identity from target-linked evidence and resume reads. | Terminal successful operation plus exact runtime absence; retain the original receipt. |
| Completed deletion receipt exists | Verify absence with the same target and receipt. | Authorised absence evidence and no repeated DELETE; permission failures remain unknown. |

In the recorded API, create/update operations were nested under
`reasoningEngines/ID`, but deletion returned a regional operation. Accept that
regional form only for deletion already linked to the exact owned runtime and
matching project/region. Test foreign project, foreign region, different runtime
and regional create/update negatives. The historical acceptance branch was
regression-tested offline; live recovery polled the recovered regional operation
without submitting another DELETE.

The older SDK source-deploy route could create an unlabelled lightweight runtime
and initiate deletion after a failed update. The retained adapter avoided that
branch by creating a labelled runtime first and supplying its exact ID. It also
intercepted private SDK internals to save the update operation before polling.
Treat those details as reasons to inspect submission/compensation behaviour, not
as a portable monkey-patching recipe. Prefer a supported interface that exposes
accepted operations and ownership early enough for recovery.

Keep receipts, ownership records, locks and diagnostic logs private; retain
completed receipts and the original evidence when a repair is required. Confirm
sessions and runtime absence independently, then report customer-visible and
provider-managed retention separately. The bounded live campaign established
remote routing, continuity and recovered cleanup on an existing project; it did
not establish all deployment forms, full-profile permissions or fresh-project
onboarding.

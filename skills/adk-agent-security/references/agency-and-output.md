# Agency and output handling

Read this for mode (d). Excessive agency (OWASP LLM06, ASI02) is a design
property: the agent can do more than the task needs. Improper output handling
(LLM05) is a renderer property: model text becomes markup, a request or a
command. Both are fixed in code, not in the prompt.

## Tier every tool

| Tier | Definition | Required gate | Examples |
| --- | --- | --- | --- |
| Read | Returns data; no state change outside the session | None beyond authorisation in the tool body and result bounding | lookups, searches, retrieval |
| Write, reversible | Changes state the application can undo or that a human reviews before it takes effect | Argument validation in `before_tool_callback`; idempotency key (`safe-api-tool-calls`) | drafts, tickets, calendar holds |
| Irreversible or external | Money, deletion, messages that leave the perimeter, deployments, code with network access | Confirmation or durable review as code, identity binding outside the schema, allowlisted destinations | payments, refunds, sends, deletes, deploys |

The inspector labels write-like names (`write_tool_without_gate`); the owner
decides the tier. A tool that is read on one system and write on another
(a search that logs the query to a shared feed) takes the higher tier.

Least privilege comes before the gate: give the agent's identity only the
permissions the read tier needs, and a separate identity to the acting step.
The ADK safety page's agent-auth example (documented behaviour): with a
read-only IAM binding, writes fail regardless of what the model decides. On
Agent Runtime, Agent Identity gives each deployment a principal to which IAM
conditions can scope, for example, one BigQuery dataset (vendor guidance);
those conditions are not exercised by local `adk web` runs under developer
ADC.

An IAM v2 deny policy is the concrete form of "no matter what the model
decides": it is evaluated before every allow policy and names permissions the
agent's principal can never use, for example
`iam.googleapis.com/serviceAccounts.getAccessToken` or
`secretmanager.googleapis.com/versions.access` on a reader agent (Google's
`iam-helper-for-policy-management` skill, read 21 October 2026). A deny policy
holds when a binding is widened by mistake; an allow-only design does not.
When a binding or deny policy on the agent's service account must be created
or changed, consult the installed Google skill `iam-helper-for-policy-management`
(from google/skills); when an existing production binding is being narrowed,
replay it first with `iam-helper-for-policy-simulator`; if either is not
installed, adk-engineer explains how to get it.

## Confirmation as code

Human approval is a state transition in trusted code, not a sentence in the
prompt; the durable-record recipe lives in `adk-operational-guardrails`
(its `human-review` reference). In ADK 2.8.0 (source-verified):

- `FunctionTool(func, require_confirmation=True | callable)`; the callable
  receives the tool arguments as keyword arguments (and `tool_context` when
  its signature names it) and must return `bool`. Order on 2.12.0 (`flows/llm_flows/tools/_caller.py`, read 2026-10-22): the plugin's `before_tool_callback`, then each agent `before_tool_callback` in order, then `tool.run_async`, which evaluates `require_confirmation` and the attached `tool_confirmation` before the body; the confirmed resume re-dispatches the original call through the same path, so a `before_tool_callback` runs again on the resume and may refuse it. A bound that must hold whatever the model or the approver does therefore lives in the tool body or the store, with the callback as the early refusal.
  `check_require_confirmation` awaits it and the result is used directly;
  a non-bool truthy value or `None` is not a gate (community report #7010).
- `McpToolset(require_confirmation=...)` applies the same to server tools.
- Inside a tool, `tool_context.request_confirmation(hint=, payload=)` records
  a `ToolConfirmation` keyed by `function_call_id`; `FunctionTool.run_async`
  checks `tool_context.tool_confirmation.confirmed` before running. A custom
  `BaseTool` must perform this check itself (community report #7148; inspector
  `custom_tool_ignores_confirmation`).
- The confirmation answer must come from the authenticated controlling user
  through the application's API, never from A2A, an unauthenticated `/run` or
  a text the model wrote. Forged confirmation responses in history were
  fixed in 2.5.0 and 2.6.0 ("Prevent continuation forgery"); 2.10.0 holds
  the call in the framework; 2.11.0 adds HMAC stamps with
  `ToolCallIntegrityPlugin` ([compatibility](compatibility.md)).
- When the decision may take hours, another person decides, or completion
  must survive restarts, use a durable review record instead of the in-session
  confirmation; approval is permission, not completion.

Confirmation checklist: callable returns strict `bool`; custom tools check
`confirmed`; the approving principal is authenticated at the API; the resumed
call's id, name and arguments match the stored request; the UI shows the exact
arguments the human approves; a denial is logged as a security signal.

## Identity never comes from the model

A `user_id`, `tenant_id`, `email` or `role` parameter on a tool lets the model,
and therefore an injection, choose whose data to touch (inspector
`identity_parameter_review`). Read identity from `tool_context.user_id`,
`tool_context.state` written by the application, or the credential the
`header_provider` resolved; `adk-tool-auth-and-secrets` owns the plumbing.
Verify ownership of the resource inside the tool with that identity.

## Code execution

The ADK safety page: "sandboxing must be used to prevent model-generated code
to compromise the local environment"; custom executors should be hermetic
(no network or API calls) with full cleanup between executions (documented
behaviour). Source-verified facts for 2.8.0:

| Executor | Where code runs | Network | Notes |
| --- | --- | --- | --- |
| `UnsafeLocalCodeExecutor` | The agent process | Everything the process can reach | Docstring: "unsafely execute code in the current local context". Development only; inspector `unsafe_code_executor` |
| `BuiltInCodeExecutor` | Gemini server-side execution | Managed | Gemini models only; no local filesystem |
| `VertexAiCodeExecutor` | Vertex Code Interpreter extension | Managed | Managed sandbox; resource name per extension |
| `AgentEngineSandboxCodeExecutor` | Agent Engine code-execution sandbox | Managed; the sandbox is a resource of your project, so the serving container's credentials and metadata server are not in the code's reach | Three constructor cases (2.12.0 source, read 2026-10-22): `sandbox_resource_name` (`projects/P/locations/L/reasoningEngines/N/sandboxEnvironments/M`) names the sandbox and fixes project and region; else `agent_engine_resource_name` names the engine that will own it; else it creates an engine lazily at the first execution in `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` (default `us-central1`). For data residency, name the sandbox resource explicitly; the lazy path chooses the region for you |
| `ContainerCodeExecutor` | Docker container you host | `network_enabled: bool = False`; capabilities dropped so code cannot reach `169.254.169.254` | Docstring prefers `GkeCodeExecutor` or a managed executor for untrusted code; `network_enabled=True` only for trusted code (inspector `container_executor_network_enabled`) |
| `GkeCodeExecutor` | gVisor-sandboxed Pod on GKE, Job mode or Agent Sandbox mode | Cluster network policy | Non-root, no privileges, TTL cleanup; 2.6.0 stopped mounting a cluster credential into the sandbox. `executor_type="sandbox"` imports `k8s_agent_sandbox.SandboxClient`, the kubernetes-sigs/agent-sandbox client, so that mode depends on the Agent Sandbox controller being installed on the cluster (source-verified `gke_code_executor.py`, main ed76f94) |
| `CloudRunSandboxCodeExecutor` (`integrations/cloud_run`, since 2.5.0) | A Cloud Run sandbox on the same container, through the guest `sandbox` binary (`/usr/local/gcp/bin/sandbox do <python>`) | `allow_egress: bool = False` passes `--allow-egress` to the guest binary; the source says nothing about the metadata server, so a design that needs "no token reachable from code" proves it with a probe inside the sandbox (`169.254.169.254` unreachable, `google.auth.default()` failing) or chooses the Agent Engine sandbox | Runs only inside a Cloud Run container with sandboxes enabled, never from a local machine; `timeout_seconds` defaults to 300, `stateful` and `optimize_data_file` are frozen off; docstring and fields, source-verified on 2.12.0 (`integrations/cloud_run/_cloud_run_sandbox_code_executor.py`), read 2026-10-22 |

How data reaches an executor (2.12.0 source, `flows/llm_flows/extensions/_code_execution.py` and `code_executors/code_executor_context.py`, read 2026-10-22): every execution receives `input_files=CodeExecutorContext(session.state).get_input_files()`, a list of `File(name, content, mime_type)` kept under the session-state key `_code_executor_input_files`; the flow itself adds files only from inline data in user messages (CSV, JSON and the other `_DATA_FILE_UTIL_MAP` types), replacing each with an "Available file" placeholder. A tool that fetches a file for the sandbox stages it through that same context over its writable state (`CodeExecutorContext(tool_context.state).add_input_files([...])`) rather than the service filesystem, and a scripted-model Runner test asserts the executor saw the file name; that path was read in source, not executed, so the test is the proof. `BaseCodeExecutor.execute_code(invocation_context, code_execution_input) -> CodeExecutionResult` is synchronous on 2.12.0, with `error_retry_attempts=2`, `stateful=False`, `optimize_data_file=False` and `timeout_seconds=None` as base defaults, so a recording double implements it synchronously. `inspect_security_surface.py` works from names and parameters: it does not flag an `EnvironmentToolset` as an execution surface, and it drops a sender's `egress` flag once the recipient parameter is removed from the schema, so those two rows are reviewed by hand until the helper learns them.

GKE Agent Sandbox, the managed form of `GkeCodeExecutor`'s sandbox mode, is the kubernetes-sigs/agent-sandbox project (v1.0.7, commit f62190c, Apache-2.0; `README.md` and `examples/`, read 2026-10-22) installed by GKE: a `Sandbox` CRD for one stateful, stably named Pod, with `SandboxTemplate`, `SandboxClaim` and `SandboxWarmPool` extensions, delegating isolation to gVisor (or Kata, which the GKE page says is not a Google Cloud product). On the ADK side (2.12.0 `code_executors/gke_code_executor.py`, read 2026-10-23): `GkeCodeExecutor(executor_type="sandbox", namespace=..., sandbox_template="python-sandbox-template", sandbox_gateway_name=None, timeout_seconds=300, ...)` opens a `SandboxClient(template_name, gateway_name, namespace)` from the `k8s_agent_sandbox` package, which installs with the extra `google-adk[extensions]` (the validator raises `ImportError` naming that extra when it is missing), writes the code as `script.py` and runs `python3 script.py`; the runtime class and security context come from the named `SandboxTemplate`, not from the executor, so the template is the thing to review. On GKE the feature needs 1.36.3-gke.1767000 or later and `--enable-agent-sandbox` (Autopilot at creation; Standard with a `--sandbox=type=gvisor` node pool); a stated cluster version below that floor is a decision to raise it, recorded in the design, not a reason to run model-written code in Job mode. The Validating Admission Policy the install page documents (https://docs.cloud.google.com/kubernetes-engine/docs/how-to/how-install-agent-sandbox, updated 2026-10-14, read 2026-10-22) is the checklist for the template:

| Required | Forbidden |
| --- | --- |
| `runtimeClassName: gvisor` | host namespaces |
| `automountServiceAccountToken: false` | privileged mode |
| `runAsNonRoot: true` | `hostPath` volumes |
| `capabilities.drop: ["ALL"]` | added capabilities |
| CPU and memory limits | `hostPort` |
| the gVisor node selector and toleration | custom sysctls, projected token volumes |

Google announced it generally available on 21 May 2026 with warm pools allocating "300 sandboxes per second, per cluster" and 90 percent of allocations in 200 milliseconds (Google Cloud blog, read 2026-10-22; vendor figures); a warm sandbox is a scheduled Pod that charges while idle, which `deploy-adk-on-google-cloud`'s GKE reference and the designer's resource ledger account for. The repository's examples are the acceptance checks a design can name: `sandbox-ksa` (a sandbox under its own Kubernetes service account with no IAM binding), `composing-sandbox-nw-policies` (a KRO resource graph that composes a sandbox with a default-deny network policy) and `containarium-execution-scoped-token` (a per-execution token minted for one run, with a Cilium policy). Its own ADK example pins `google-adk==1.19.0` and predates the 2.x sandbox mode, so read it for the cluster setup only.

Beside the code executors, which run one code string, ADK has an execution environment layer for agents that read, write and run inside a workspace: `EnvironmentToolset` (`tools/environment/`, since 1.29.0) exposes execute, read-file, write-file and edit-file tools over a `BaseEnvironment` (`initialize`, `close`, `working_dir`, `execute`, `read_file`, `write_file`), with these backends on main (`integrations/`, read 2026-10-22): `LocalEnvironment` (the host process; 2.9.0 terminates the whole process tree when a local command times out), the Agent Engine sandbox (`vmaas`, since 1.31.0; 2.12.0 adds sandbox lifecycle helpers and per-container-config templates), Daytona (since 2.4.0), E2B (since 2.3.0) and OpenSandbox (added 2026-10-13, in no release at 2.12.0). Tier an environment like a write tool, because it is one. Two caveats on backend choice: Daytona's public repository states "This repository is no longer maintained" and that "as of June 2026, Daytona's core development has moved to a private codebase" (github.com/daytonaio/daytona README, read 2026-10-22); and Daytona, E2B and OpenSandbox run the code outside Google Cloud, which is a data-residency and egress decision for the design, not a default. Prefer the Agent Engine sandbox, the Cloud Run sandbox or GKE Agent Sandbox when the data must stay in the project. Most of this layer predates 2.8.0 and was simply absent from this table; only OpenSandbox and the 2.12.0 lifecycle helpers are newer than the pin.

`BashTool` runs commands under `BashToolPolicy`, whose
`allowed_command_prefixes` defaults to `("*",)` (source-verified). Set an
explicit prefix list, `blocked_operators`, timeout and resource limits; the
inspector reports `bash_policy_allow_all`. Google's long-horizon harness sample
(google/adk-recipes be63596, `core/python/long-horizon-harness/horizon/guardrails/`
and `docs/security-model.md`, read 2026-10-22; vendor sample) adds hard-deny
guards for exfiltration-shaped commands, metadata-server access and
pipe-to-interpreter before any soft approval, and treats "ask" as deny when no
human is present (`ask_is_deny=True` on headless sub-agent and routine chains);
copy that order. Its shape is worth copying in detail: a `before_tool_callback`
that returns `None` to allow or a dict with `error` to block; an argv classifier
(`shlex`, quote- and operator-aware) returning `deny` (recursive force-delete of
system or home roots, never demotable), `ask` (destructive deletes, cloud and
cluster deletes, force or history git, `sudo`, pipe into an interpreter,
recursive `chmod` or `chown` on a root; demotable to an interactive approval
only by an explicit per-session grant) or no opinion; a seed denylist of literal
catastrophic commands and credential reads (`cat ~/.ssh/`, `~/.aws/`,
`~/.config/gcloud/`, `~/.kube/`, `/etc/shadow`, `/etc/sudoers`) and protected
write paths (`*/.ssh/*`, `*/.aws/*`, `*/.config/gcloud/*`, `*/.kube/*`,
`/etc/passwd`); a rule that a grant or overlay for a shell tool must carry a
narrowing prefix, regex or argument pattern or is rejected at load, so no
session can approve "always allow bash"; and a one-time per-session grant for
an upload to a host outside the allowlist. Its sandbox egress is all or nothing
(Horizon's own Vertex sandbox setting, not an ADK executor option: it exposes
only `internet_access`, baked in at provision time, default off on Cloud Run
and on in local development), so an allowlisted host
is not available there; `exfil_guard` stays the exfiltration boundary whether
egress is on or off. One Horizon choice this skill does not adopt: its
`GuardrailsPlugin` spends one more model call on a "graceful handoff" turn
after a halt so the model summarises before the static envelope;
`adk-operational-guardrails` keeps the static stop as the default.

## Output handling

Model text reaches three sinks: the user's screen, the next tool's arguments,
and the next model's context. Rules per sink:

- **Screen.** Escape model text; render Markdown with a sanitiser that drops
  raw HTML, scripts, forms and images from non-allowlisted origins; make links
  visible with their full target and open only allowlisted schemes. The ADK
  safety page's examples (documented behaviour): an injected image tag sends
  session content to a third party; a crafted URL exfiltrates on click.
  `adk-frontend-integration` owns the renderer; this skill owns the
  requirement.
- **Tool arguments.** Validate type, range and allowlist in
  `before_tool_callback`; refuse tainted values in egress arguments
  ([injection patterns](injection-patterns.md)).
- **Context.** Bound size and label provenance in `after_tool_callback`
  ([tool supply chain](tool-supply-chain.md)); keep history out of acting
  agents with `include_contents='none'`.

System-prompt leakage (LLM07) is handled by not putting secrets, keys or
authorisation logic in the instruction; the instruction is observable text,
and `global_instruction` is rendered into every agent's request.

## Screening is a layer

Model Armor screens text for injection and jailbreak patterns, responsible AI
categories, sensitive data and malicious URLs (vendor docs); it is stateless
per message, does not decode encodings, and on 2.8.0 the native plugin skips
function responses and function-call arguments (2.12.0 adds tool-output
screening through `after_tool_callback`; arguments stay unscreened). It does not decide
authorisation, tool permissions, data flow or egress (from 2.12.0 the plugin
screens tool output as text through `after_tool_callback`, as the
sensitive-data skill records). Record it in the checklist's screening column
and configure it with `protect-adk-sensitive-data`; the controls above must
hold with screening switched off.

Four placement rules for any screening layer, whatever implements it, restated
from another framework's documented contract (openai/openai-agents-python commit 841dfdd, MIT, `docs/guardrails.md`, `docs/human_in_the_loop.md`, `docs/testing.md`, read 2026-10-23; another framework's documented behaviour, restated as a rule for ADK): screen user input
once, at the first agent in the chain, and final output once, at the agent
that produces it, with per-tool checks on every guarded call including
inside delegated specialists, so a handoff never bypasses the check; a
screen that runs in parallel with the agent saves latency but the agent may
have consumed tokens and executed tools before the verdict cancels it, so a
check that must prevent an effect runs blocking, before the agent; when an
output check rejects the final answer, keep the completed tool events and
their results in the session, drop the rejected text, and substitute a
static, data-free message (never the rejected content, never a formatter
that sees the run context's secrets), and when the rejected answer was a
tool's own result, withhold that payload from the session as well; and a
check that raises instead of returning a verdict is an unknown verdict, kept
separate from a rejection in the record. On ADK the first and last agent are
the root agent's model callbacks, the per-tool check is `before_tool_callback`
and `after_tool_callback`, and the static envelope is
`adk-operational-guardrails`' halt message.

A local alternative for tool results is Meta's LlamaFirewall with its Prompt
Guard 2 classifier, run in-process from `after_tool_callback` when tool
output may not leave the project or region, or as a second signal beside
Model Armor (meta-llama/PurpleLlama commit d934ea2, `LlamaFirewall/` (MIT
scanner code), read 2026-10-24). These facts decide whether it actually
screens. It scores only the first 512 tokens (`truncation=True,
max_length=512`), and the model card says longer inputs must be split, so
the shipped scanner is not a whole-result screen and an injection after
token 512 passes. Chunk the projected result and classify each segment:
count with the classifier's own tokenizer (the scanner's `pg.tokenizer`),
keep each window under 512 tokens and overlap the windows, and test with an
injection placed across a window boundary and one after token 512, since
window and overlap sizes are the project's choice. It flags explicit
attempts to override instructions, not every risk. Call one
`PromptGuardScanner` directly, never through `LlamaFirewall`: `scan()` runs
each scanner with `asyncio.run`, which raises inside ADK's running event
loop; `scan_async()` returns a successful `ALLOW` for every result that is
not a block or a human-review hold, a scanner `ERROR` included; both build a
new scanner, and so reload the model, on every scan; and a role with no
scanner configured returns `ALLOW`. The scanner's `scan()` is declared async
but runs the model synchronously, so call it through `asyncio.to_thread` to
keep ADK's loop free; it has no error handling, so an exception, a status
other than success, or a result over your size limit is the unknown verdict
and withholds. Its block reason embeds the full scanned text, so log the
decision and score, never the reason. Construct the scanner once at startup,
which loads the model, from weights already at
`$HF_HOME/meta-llama--Llama-Prompt-Guard-2-86M`, and refuse to start if that
directory is missing: when `HF_HOME` is unset the library sets it, for the
whole process, to a literal `~/.cache/huggingface`, and a missing directory
triggers a download and an interactive Hugging Face login. Tests use a fake
with the same interface, `async scan(message, past_trace=None) ->
ScanResult`, returning each decision, an `ERROR` status and an exception in
turn, beside the scripted-model Runner test in [adversarial
testing](adversarial-testing.md). The Prompt Guard 2 weights are gated under
the Llama 4 Community License, separate from the MIT code: whether a project
may use them is that project's licence decision, recorded before deployment;
this skill links to them and ships none. Its AlignmentCheck scanner is a
remote judge, not a local screen (see `protect-adk-sensitive-data`), and it
does nothing for sensitive data, which stays with Sensitive Data Protection.

A second screening layer now sits on Agent Gateway: Semantic Governance
Policies, natural-language constraints that a managed LLM policy engine
evaluates against the user's intent and the proposed tool call, returning
`ALLOW` or `DENY` with a rationale the calling agent (and possibly the end
user) sees. The page is explicit that the feature is in Preview, that "LLMs
are probabilistic and can make mistakes. Verdicts may not be accurate", and
that it complements IAM rather than replacing it
(https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/policies/semantic-governance-overview,
updated 2026-10-21, read 2026-10-22). Treat it exactly as Model Armor is
treated here: a layer in the screening column, never the enforcement point
for a contract. Google's own zero-trust blueprint shows why: its second act
has a semantic policy allow eight compliant $20 refunds in one session until
$160 has left on a $149 order, because each call passed a single-turn check;
the control that catches it is an aggregate bound keyed on the business
object (the order id) in trusted code, which `adk-operational-guardrails`
owns, and the blueprint's "anomaly detection" is a local simulation in its
demo code whose product status the governance documentation does not state
(GoogleCloudPlatform/generative-ai commit 3a716a8,
`agents/adk/zero-trust-agents-2/README.md` and `demo/`, read 2026-10-22;
vendor sample). The first part of that blueprint pairs three build-time
controls that map onto this reference: writes signed by a key the model
never holds and verified by the store (local HMAC, Cloud KMS in production),
a gVisor sandbox with no egress, and a deterministic input and output gateway
backed by unit tests in CI (`agents/adk/zero-trust-agents/README.md`, same
commit; `safe-api-tool-calls` carries the signed-write pattern).

## Completion

Every tool has a tier and the gate the tier requires; irreversible actions
have confirmation or review implemented as code with the checklist satisfied;
no tool takes identity from the model; the executor is sandboxed and any bash
policy is an allowlist; the renderer escapes and allowlists; the suite in
[adversarial testing](adversarial-testing.md) has one case per gate.

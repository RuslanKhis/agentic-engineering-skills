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

## Confirmation as code

Human approval is a state transition in trusted code, not a sentence in the
prompt; the durable-record recipe lives in `adk-operational-guardrails`
(its `human-review` reference). In ADK 2.8.0 (source-verified):

- `FunctionTool(func, require_confirmation=True | callable)`; the callable
  receives the tool arguments and must return `bool`.
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
| `AgentEngineSandboxCodeExecutor` | Agent Engine code-execution sandbox | Managed | `sandbox_resource_name` or `agent_engine_resource_name` |
| `ContainerCodeExecutor` | Docker container you host | `network_enabled: bool = False`; capabilities dropped so code cannot reach `169.254.169.254` | Docstring prefers `GkeCodeExecutor` or a managed executor for untrusted code; `network_enabled=True` only for trusted code (inspector `container_executor_network_enabled`) |
| `GkeCodeExecutor` | gVisor-sandboxed Pod on GKE, Job mode or Agent Sandbox mode | Cluster network policy | Non-root, no privileges, TTL cleanup; 2.6.0 stopped mounting a cluster credential into the sandbox |

`BashTool` runs commands under `BashToolPolicy`, whose
`allowed_command_prefixes` defaults to `("*",)` (source-verified). Set an
explicit prefix list, `blocked_operators`, timeout and resource limits; the
inspector reports `bash_policy_allow_all`. Google's long-horizon harness sample
(vendor sample) adds hard-deny guards for exfiltration-shaped commands,
metadata-server access and pipe-to-interpreter before any soft approval, and
treats "ask" as deny when no human is present; copy that order.

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
function responses and function-call arguments. It does not decide
authorisation, tool permissions, data flow or egress. Record it in the
checklist's screening column and configure it with
`protect-adk-sensitive-data`; the controls above must hold with screening
switched off.

## Completion

Every tool has a tier and the gate the tier requires; irreversible actions
have confirmation or review implemented as code with the checklist satisfied;
no tool takes identity from the model; the executor is sandboxed and any bash
policy is an allowlist; the renderer escapes and allowlists; the suite in
[adversarial testing](adversarial-testing.md) has one case per gate.

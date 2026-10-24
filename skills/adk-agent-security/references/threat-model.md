# Threat model for an ADK agent

Read this for mode (a). The output is the completed
[checklist and worksheet](../assets/threat-model-checklist.md) for each agent,
with an enforcement point and an observable check per row. Build it from the
inventory, not from the instruction text; the instruction is the one control
an attacker can argue with.

## 1. Inventory the four things that matter

| Column | What to list | Where to find it |
| --- | --- | --- |
| Assets | Data the agent can read (session state, memory, documents, databases, mail, files, credentials in `ToolContext`) and systems it can change | Tool bodies, toolsets, memory and artifact services, `header_provider`, `auth_credential` |
| Untrusted inputs | Text the model will read that someone other than the controlling user can author: user turns from unauthenticated clients, retrieved chunks, fetched pages, mail and tickets, MCP descriptions and results, OpenAPI responses, other agents' output, memories written from earlier turns, A2A peer messages, tool error strings | Inspector `untrusted_content_source` rows; sub-agents; `RemoteA2aAgent` |
| Consequential actions | Writes, sends, payments, deletions, deployments, code execution, state writes that later steps trust, transfers to privileged agents | Inspector `write_tool_without_gate`, bash tools, executors, `transfer_to_agent` targets |
| Egress | Any path by which bytes leave the perimeter under model control: HTTP tools, mail, webhooks, URL-fetching built-ins (`url_context`), model-chosen query strings, links and images in rendered output, A2A replies | Inspector `egress_capable_tool`; UI renderer |

Name the controlling human for each agent (Google's secure-agents framework:
well-defined human controllers, carefully limited powers, observable actions;
vendor guidance). An agent triggered by a webhook, a GitHub event or another
agent has no human controller in the loop and must be treated as having
inherited the trust of whoever can produce that trigger.

## 2. The trifecta check, per agent and per workflow

Simon Willison's lethal trifecta (community report, 2025-06-16): private data,
exposure to untrusted content and a way to communicate externally, in one
agent, means a successful injection can exfiltrate. The inspector computes the
three legs per agent over its own tools plus the tools of its sub-agents,
because a sub-agent's output is rendered into the parent's context.

For each agent whose `trifecta.all_three` is true, decide which leg to remove:

| Remove | How in ADK | Cost |
| --- | --- | --- |
| Untrusted content | Move reading into a quarantined sub-agent with `include_contents='none'` and no tools; return structured fields the parent validates ([injection patterns](injection-patterns.md)) | A second model call per document |
| Egress | Replace free-form send or fetch tools with allowlisted destinations resolved in code; keep model output text-only in the UI | Fewer destinations |
| Private data | Run the reader with agent-auth that can see only public data; fetch private data in a later, injection-free step | Workflow restructuring |

A `SequentialAgent` or `LoopAgent` whose children together hold all three legs
is flagged `trifecta_across_workflow`. Shared session state is a channel: a
reader step that writes free text into `state['summary']` and a writer step
that acts on it is one agent for the purpose of this check. Pass structured,
validated values between steps; `adk-workflow-design` owns the handoff shape.

Detection does not remove a leg. "95% detection is a failing grade" (community
report): a screening product in front of the model changes the odds, not the
blast radius. Record Model Armor or judge plugins as layers in column
"screening", never as the enforcement point for a row.

## 3. Map each row to an enforcement point

| Enforcement point | What it can decide | What it cannot see |
| --- | --- | --- |
| Identity source (agent-auth service account, user OAuth token, Agent Identity principal, IAM conditions) | Whether an action is possible at all; the ADK safety page: a read-only IAM binding fails writes "no matter what the model decides" (documented behaviour) | Which of several permitted actions the user meant |
| `before_model_callback` or plugin `before_model_callback` | Request shape, context size, which tools are declared this turn | Tool results not yet produced |
| `before_tool_callback` or plugin `before_tool_callback` | Arguments against `tool_context.state`, tool tier, per-invocation capability tags; returning a dict skips the tool (source-verified `functions.py`, 2.8.0) | Anything inside the external system |
| Tool body | Authorisation with identity from `ToolContext`, resource ownership, idempotency, result shaping | What the model will do with the result |
| `after_tool_callback` | Provenance labels, size limits, screening of unfenced tool results before they re-enter context | Whether the model obeys the label |
| Workflow structure | Which agent sees which inputs; whether a consequential step can be reached after untrusted input | Content semantics |
| Code executor | Network, filesystem, credentials and lifetime of model-generated code | The intent of the code |
| Perimeter (VPC-SC, Private Google Access, egress policy, hermetic sandbox network) | Where bytes can go | Which bytes are sensitive |
| Agent Gateway (Agent Runtime ingress `CLIENT_TO_AGENT`, egress `AGENT_TO_ANYWHERE`) | On egress, which MCP tool names the agent's principal may call: `roles/iap.egressor` with a CEL condition such as `api.getAttribute('iap.googleapis.com/mcp.toolName', '') in ['search', '']` (the empty name lets `initialize` and `tools/list` pass); on ingress, Model Armor before the agent. Decided by IAM, not by the model (vendor guidance, codelab https://codelabs.developers.google.com/agw-cuj-arun-egress-emcp read 2026-10-21) | Arguments, results and anything outside Agent Runtime or Gemini Enterprise: it does not govern Cloud Run or GKE agents, and A2A calls from Gemini Enterprise bypass it (Agent Gateway overview, read 2026-10-21) |
| UI rendering | Whether model text can become markup, a request or a click | The model's intent |

Choose the earliest point that has the information to decide. Authorisation
needs identity, so it lives in the tool body or IAM; argument policy lives in
`before_tool_callback`; blast-radius decisions live in workflow structure and
the perimeter.

## 4. Agent-to-agent trust

The Pillar Security disclosure (community report, 2026-08-04): Google's public
issue-triage agent was injected through issue text into posting a command that
triggered a privileged fix agent holding a personal access token, an API key
and a service-account credential. Lessons that generalise:

- A privileged agent must be gated on a signal untrusted text cannot produce
  (an authenticated human action, a signed event), never on a comment, label
  or message a less-privileged agent can emit.
- Each agent has its own identity with only the scopes its tools need; a
  reader agent holds no write credential.
- Peer output is data. ADK 2.8.0 fences relayed agent output (source-verified
  `_fencing.py`) and its own comment says this "raises the bar rather than
  closing the class". Structure still decides what the receiving agent can do.
- A2A inbound content arrives with `role=user`; do not derive authority from
  the role or author field (google/adk-python#6461, open). Accept approvals
  only from the authenticated controlling user at the API layer. An
  unauthenticated caller of a `to_a2a` agent runs as `A2A_USER_<context_id>`
  on 2.12.0, and the task history it gets back carries tool arguments and
  results; `adk-agent-interoperability`'s A2A contracts own the inbound
  authentication that turns this into a real principal.

## 5. Deployment surface

- ADK Web is "not meant for use in production deployments" (documented
  behaviour); the API server's `/run` and `/run_sse` must sit behind
  authentication. `adk deploy cloud_run` examples use
  `--no-allow-unauthenticated`; the inspector reports
  `unauthenticated_exposure_hint` for the opposite flag.
- A `google-adk` pin below 2.7.0 is inside published adk web remote code
  execution ranges ([compatibility](compatibility.md)); the inspector reports
  `known_cve_range`.
- Log and alert on denied tool calls, refused confirmations and blocked
  screening verdicts: the failed attempt is the attack signal (vendor
  guidance, Google Cloud blog 2025-10-24).
- Local `adk web` runs use the developer's ADC, so IAM conditions written for
  the deployed Agent Identity are not exercised until deployment (vendor
  codelab caveat). Test them deployed.
- Security Command Center is the platform-side alert source: Agent Platform
  Threat Detection watches Agent Runtime `stdout`/`stderr` and audit logs for
  reverse shells, credential harvesting, metadata-service abuse and
  exfiltration tooling (vendor docs, read 2026-10-21); `findingClass="SECRET"`
  reports leaked plaintext credentials and `TOXIC_COMBINATION` reports a
  reachable attack path (Google's `google-cloud-scc-query` skill, read
  21 October 2026). When a finding on the agent's project needs triage,
  consult the installed Google skill `google-cloud-scc-query` (from
  google/skills); when it needs fixing, `google-cloud-scc-remediation`; if
  either is not installed, adk-engineer explains how to get it.

## 6. Map findings to OWASP identifiers

Use the LLM Top 10 (2025) for model-boundary findings and the Agentic Top 10
(2026) for action-boundary findings; the checklist asset holds the full table.
A finding usually maps to one of each: an unfiltered MCP server with a
poisoned description is LLM03 Supply Chain and ASI04 Agentic Supply Chain Vulnerabilities; a
free-form send tool reachable after reading mail is LLM06 Excessive Agency and
ASI02 Tool Misuse and Exploitation with LLM01 as the trigger.

When the reader works from MITRE ATLAS or the CoSAI Risk Map, put that
identifier beside the OWASP one rather than translating; both are Apache-2.0
and are cited by id with a link, never copied as tables. ATLAS 2026.09
(mitre-atlas/atlas-data commit 3259f38, `dist/ATLAS-latest.yaml`, read
2026-10-23: 16 tactics, 136 techniques, 88 sub-techniques by count of that
file) names the agent techniques this skill's findings land on: `AML.T0051`
LLM Prompt Injection, `AML.T0080` AI Agent Context Poisoning (with `.000`
Memory), `AML.T0070` RAG Poisoning, `AML.T0110` AI Agent Tool Poisoning,
`AML.T0084.001` discovery of tool definitions, `AML.T0083` Credentials from AI
Agent Configuration, `AML.T0098` AI Agent Tool Credential Harvesting,
`AML.T0086` Exfiltration via AI Agent Tool Invocation, `AML.T0101` Data
Destruction via AI Agent Tool Invocation, `AML.T0034.002` Agentic Resource
Consumption and `AML.T0118` Autonomous AI Agent Communication. The CoSAI
Risk Map (cosai-oasis/secure-ai-tooling commit 622605a, `risk-map/yaml/`,
read 2026-10-23) names the risks a security ticket can cite
(`riskPromptInjection`, `riskRogueActions`, `riskToolSourceProvenance`,
`riskToolRegistryTampering`, `riskRetrievalVectorStorePoisoning`,
`riskRunawayAgentToolLoops`, `riskEconomicDenialOfWallet`,
`riskAgentDelegationChainOpacity`, `riskStaleAgentIdentityBinding`,
`riskOrchestratorRouteHijacking`) and the controls this toolkit implements
under its own names: `controlAgentExecutionBounds` (a mandatory `max_turns`
default, per-agent and per-session tool-call budgets enforced before each
invocation, a context-window budget and circuit breakers, which is
`adk-operational-guardrails`' runtime bounds), `controlAgentCredentialIsolation`,
`controlToolRegistryAndDiscoveryIntegrity`, `controlAgentPluginPermissions`,
`controlComponentIdentityProvenance` and `controlAgentObservability`. One
caution: the Risk Map's `frameworks.yaml` pins `mitre-atlas@2026.09` as
current, but its risk entries still map to `@5.0.1` technique ids, so take
ATLAS ids from ATLAS, not from the map. The OWASP MCP Top 10
(github.com/OWASP/www-project-mcp-top-10, commit 165fe0f, 2026-07-29; ids
MCP01:2025 to MCP10:2025, still beta) is the MCP-specific list; its licence
files disagree (CC BY-SA in `LICENSE.md`, CC BY-NC-SA linked from the index),
so this skill cites ids with a link and copies none of its text. MCP06's
title differs between the repository and owasp.org, so cite the id, not the
title. The checklist's companion line maps the ten ids. To pick an id for a
finding, this skill's own sorting (open the linked entry to confirm):

| Finding in this skill's terms | MCP id |
| --- | --- |
| A token or secret reaches a server, its logs or the model (passthrough, a key in arguments) | MCP01 |
| A server or tool holds more permission than its task (a shared runtime identity, broad scopes) | MCP02 |
| A tool definition carries hidden instructions or changed after review (rug pull) | MCP03 |
| An unpinned or tampered server package or dependency | MCP04 |
| Tool arguments reach a shell, an interpreter or a file path the model chose | MCP05 |
| Content a tool returned redirects the agent's goal or plan | MCP06 |
| Missing or weak authentication or authorisation between client and server | MCP07 |
| No record of which tool calls ran, or which were withheld and why | MCP08 |
| A server in use that nobody approved or registered | MCP09 |
| Private context sent to a server, or to another user, beyond what the task needs | MCP10 |

## Completion

Every agent has a worksheet; every trifecta agent has a named leg to remove or
a written acceptance of residual risk by the owner; every consequential action
has an enforcement point other than the instruction; every untrusted input has
a row saying where it is fenced, screened or quarantined. Hand the worksheet to
mode (b), (c) or (d) for the change, and to mode (e) for the regression suite.

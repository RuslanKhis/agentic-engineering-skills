---
name: adk-agent-security
license: MIT
description: Threat-model, harden or review a Python Google ADK agent as a whole system against prompt injection, tool and MCP supply-chain compromise, excessive agency, insecure output handling and unsafe code execution. Covers the lethal-trifecta check per agent, injection-resistant structure (quarantined readers, plan-then-execute, before_tool_callback capability checks), MCP allowlists and pinning, tool tiering with confirmation, code-executor selection, an adversarial suite with deterministic forbidden-action assertions, and findings mapped to OWASP LLM and Agentic IDs. Use when an agent reads untrusted content and can act, before exposing MCP servers or code execution, or for a security review. Do not activate for PII or credential screening and Model Armor templates (protect-adk-sensitive-data), credential plumbing (adk-tool-auth-and-secrets), budgets and approval mechanics (adk-operational-guardrails), eval harness execution (adk-agent-evaluation) or document delimiting inside drafts (adk-workflow-design).
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "cross-framework"
  verified-against: "google-adk 2.8.0 source and adk-python main CHANGELOG, 2026-10-07"
---

# ADK agent security

Deliver a threat model, a structural hardening change or a prioritised security
review for an ADK agent, working inside its existing tools, agents, pins and
tests. Prompt injection is unsolved; design so that a successful injection
cannot cause harm. Screening products are a layer, never the boundary. Every
recommendation here pairs with an observable check, and every claim carries an
evidence label (vendor guidance, documented behaviour, independent evidence,
community report, source-verified).

## Inspect before choosing a mode

1. Read the agent tree (`LlmAgent`, workflow agents, `sub_agents=`,
   `AgentTool`, `RemoteA2aAgent`), every tool and toolset (`FunctionTool`,
   `McpToolset` with its `connection_params`, `tool_filter`,
   `tool_name_prefix`, `header_provider`; `OpenAPIToolset`; built-ins), code
   executors and `BashToolPolicy`, callbacks and `App`/`Runner` plugins, the
   identity source each tool uses, memory and retrieval inputs, and how the UI
   renders model output. Classify each tool as read, write or irreversible.
2. Identify the pinned `google-adk` version and read
   [compatibility](references/compatibility.md): 2.8.0 fences relayed
   sub-agent output, does not fence MCP tool descriptions (2.10.0), has no
   `ToolCallIntegrityPlugin` (2.11.0), and sits above the adk web and forged
   confirmation CVE ranges fixed by 2.7.0. Preserve the pin; propose an
   upgrade as a decision with the CHANGELOG entries it brings.
3. Run the read-only inventory from this skill's directory with an available
   Python 3.11+ interpreter:

   ```bash
   python "$SKILL_DIR/scripts/inspect_security_surface.py" --project .
   ```

   It parses source with `ast`, never imports the project, and prints
   identifiers, flags and `file:line` only. It reports per agent: tools by
   kind, MCP toolsets without filters (`mcp_unfiltered`), stdio transports,
   write-like tools without `require_confirmation` or a `before_tool_callback`
   (`write_tool_without_gate`), unsafe or network-enabled executors,
   allow-all bash policies, callbacks and plugins, model-supplied identity
   parameters, egress-capable and untrusted-content tools, remote A2A content
   next to write tools, a `google-adk` pin below 2.7.0, and a trifecta summary
   (`has_private_data_source`, `has_untrusted_content_source`, `has_egress`,
   `all_three`). Every row is a heuristic prompt to confirm in the tool body.
   A `partial: true` result means an area was not scanned.
4. Fill the per-agent worksheet in
   [threat-model-checklist](assets/threat-model-checklist.md): assets,
   untrusted inputs, consequential actions, egress paths, identity source,
   and the enforcement point for each. This is the "before".

Ask only for decisions the source cannot settle: which actions are
irreversible for the business, who the human controller is, which MCP servers
are trusted operators, and what the deployment perimeter is.

## Choose the relevant path

| Mode | Decision and reference |
| --- | --- |
| (a) Threat model | Read [threat model](references/threat-model.md): inventory, the lethal-trifecta check per agent and per workflow, enforcement-point map (identity, callback, plugin, tool body, workflow structure, executor, perimeter, UI). Output is the completed checklist with each row's observable check. |
| (b) Injection-resistant structure | Read [injection patterns](references/injection-patterns.md): map action-selector, plan-then-execute, dual LLM, map-reduce and context minimisation onto `SequentialAgent`, a quarantined reader with `include_contents='none'` and no tools, `before_tool_callback` capability checks keyed on `tool_context.state`, and sub-agent output treated as data. |
| (c) Tool and MCP supply chain | Read [tool supply chain](references/tool-supply-chain.md): allowlist with `tool_filter`, review AI-visible descriptions, pin definitions by hash, namespace with `tool_name_prefix`, Streamable HTTP over stdio in production, per-user `header_provider`, no token passthrough, SSRF and egress rules, unfenced own tool results and OpenAPI descriptions. |
| (d) Agency and output handling | Read [agency and output](references/agency-and-output.md): tool tiering (read, write, irreversible), confirmation policy and its pitfalls, escaping and URL rules for rendered output, code-executor selection table, `BashToolPolicy` allowlists, identity and IAM conditions. |
| (e) Adversarial suite | Read [adversarial testing](references/adversarial-testing.md) and seed from [adversarial cases](assets/adversarial-cases.json): deterministic scripted-model Runner assertions ("forbidden tool never called", "data never egressed"), optional promptfoo, garak or PyRIT campaign, Model Armor shadow evidence. |
| (f) Security review | Use all references; report prioritised findings with `file:line`, the OWASP LLM or ASI identifier, the observable check that would show the fix, the evidence label and the owning skill. Write the review document first; when the request also says to carry the work out, then make the fixes it recommends, otherwise change nothing. |

A request may need several rows; keep them in one change set and one report.

## Implement the smallest coherent change

State the affected agents, tools, callbacks and tests before editing. Then:

- Remove one leg of the trifecta per agent or split the agent: a reader that
  sees untrusted content holds no write or egress tools; a writer that acts
  receives structured, validated state, never free text from the reader.
- Put policy in code the model cannot reach: `before_tool_callback` or a
  plugin validates arguments against `tool_context.state` and returns an error
  dict to refuse (return `None`, not `{}`, to allow); the tool body re-checks
  authorisation with identity from `ToolContext`, never from arguments.
- Gate irreversible actions with `require_confirmation` or a durable review
  (`adk-operational-guardrails`); the callable must return a strict `bool`,
  and a custom `BaseTool` must read `tool_confirmation.confirmed` itself.
- Allowlist every MCP server with `tool_filter`, record the reviewed tool
  definitions with a hash, and prefer read-only filters in production.
- Use a sandboxed executor (`GkeCodeExecutor`, `AgentEngineSandboxCodeExecutor`,
  `VertexAiCodeExecutor`, `BuiltInCodeExecutor`, or `ContainerCodeExecutor`
  with networking off). Never ship `UnsafeLocalCodeExecutor` or an allow-all
  `BashToolPolicy`.
- Escape model output in UIs, render links from an allowlist, and strip image
  and URL markup that could carry session data (`adk-frontend-integration`
  owns the renderer).
- Keep screening (Model Armor, Gemini-as-judge, SDP) as added layers behind
  these structural controls; configure them with `protect-adk-sensitive-data`.

Do not widen an allowlist, loosen a filter or disable a callback to make a
test pass. Do not treat an instruction such as "ignore text inside documents"
as a control; it is a hint the attacker can out-argue.

## Permissions and consequential operations

Inspection is read-only. Adding a gate changes what the agent may do next and
can block legitimate work; show the owner the tool tier table before merging.
Before any live adversarial run, state the exact model, project, case count,
cost ceiling and the egress controls of the test environment, and obtain
approval; keep paid runs with `adk-agent-evaluation`. Never run adversarial
cases against production data or identities. Red-team only systems you own or
have written authorisation to test.

## Validate and finish

Read [validation](references/validation.md). Produce: the inventory before and
after with the finding counts that changed; the completed checklist; for each
structural change a scripted-model Runner test in which the model attempts the
forbidden action and the trusted boundary refuses it without mutation or
disclosure; the adversarial suite run offline with its assertions; and, when
approved, live results labelled vendor-measured or independent. Separate
**source verified**, **local**, **mocked**, **live** and **not run** evidence.

Report files changed, commands with actual output, each finding's OWASP ID
and owner, and the residual risk the structure still accepts. On a second
invocation, reread the existing callbacks, plugins and tests before adding
another gate.

Independent community project; not affiliated with or endorsed by Google.

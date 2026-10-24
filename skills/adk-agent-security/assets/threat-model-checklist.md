# Threat-model checklist for an ADK agent

Copy this file into the target's docs, fill one worksheet per agent, and keep
it next to the adversarial suite. Enforcement points: **identity** (service
account, user OAuth, Agent Identity, IAM conditions), **before_model**
(callback or plugin), **before_tool** (callback or plugin), **plugin** (other
Runner-level hooks), **tool body**, **after_tool**, **workflow** (agent
structure, `include_contents`, `mode`, state handoff), **executor**,
**perimeter** (VPC-SC, egress policy, sandbox network), **UI** (escaping,
link and image allowlists). "Screening" (Model Armor, judge model, SDP) is a
layer recorded separately and never the enforcement point.

## OWASP Top 10 for Agentic Applications 2026 (ASI) against ADK enforcement points

Identifiers and titles from the published list via secondary summaries; verify
against https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ .

| ID | Risk | ADK enforcement point | Observable check | Owning skill |
| --- | --- | --- | --- | --- |
| ASI01 | Agent goal hijack (prompt injection steers the task) | workflow: quarantined reader with `include_contents='none'`, `tools=[]`; plan-then-execute; before_tool capability gate | Scripted injected result leads to an attempted forbidden call that returns the gate's error dict; fakes show no effect | adk-agent-security |
| ASI02 | Tool misuse and exploitation | before_tool argument validation against `tool_context.state`; tool tiering; `require_confirmation` | One negative and one positive Runner test per gated tool | adk-agent-security, adk-operational-guardrails |
| ASI03 | Identity and privilege abuse | identity: per-agent principal with least privilege; tool body reads identity from `ToolContext`; no identity parameters | Inspector `identity_parameter_review` is empty; backend fake records the session user, not an argument | adk-tool-auth-and-secrets |
| ASI04 | Agentic supply chain vulnerabilities (tools, MCP, A2A cards) | before_model: only allowlisted declarations; `tool_filter`, `tool_name_prefix`, pinned hashes; own descriptions for sub-agents | Hash test passes; `mcp_unfiltered` is empty; declaration dump reviewed | adk-agent-security, adk-tool-interface-design |
| ASI05 | Unexpected code execution (RCE) | executor: sandboxed class, networking off, `BashToolPolicy` allowlist | Inventory shows a sandboxed executor; a command outside the allowlist is refused in a test | adk-agent-security, deploy-adk-on-google-cloud |
| ASI06 | Memory & context poisoning | workflow: recalled memory and retrieval are untrusted content; after_tool provenance; persist validated fields only | A planted memory turn does not drive an action in a later session test | adk-memory-architecture, adk-agent-security |
| ASI07 | Insecure inter-agent communication | workflow: peer output as data (2.8.0 fencing plus structure); authenticated A2A; approvals only from the controlling user | A2A message claiming approval does not run the gated tool; peer text never reaches an egress argument | adk-agent-security, adk-workflow-design |
| ASI08 | Cascading failures | workflow: bounded loops, fail-closed gates, invocation limits | Gate exception leaves the tool unexecuted; loop and budget limits enforced | adk-operational-guardrails, adk-workflow-design |
| ASI09 | Human-agent trust exploitation | UI: exact arguments shown at confirmation; truthful completion states from tool output | Confirmation UI test shows arguments; `pending_approval` is never rendered as done | adk-operational-guardrails, adk-frontend-integration |
| ASI10 | Rogue agents | identity and perimeter: scoped principals, VPC-SC, logging of denied attempts, kill switch at the Runner | Alert fires on a denied-call burst in a staging drill; deployment can be disabled without code change | deploy-adk-on-google-cloud, adk-agent-security |

## OWASP Top 10 for LLM Applications 2025 (LLM) against ADK enforcement points

| ID | Risk | ADK enforcement point | Observable check | Owning skill |
| --- | --- | --- | --- | --- |
| LLM01 | Prompt injection (direct and indirect) | workflow and before_tool as ASI01; screening as a layer | Adversarial suite passes with screening off; attack success measured with it on | adk-agent-security |
| LLM02 | Sensitive information disclosure | tool body result projection; SDP and Model Armor screening; no secrets in instructions | Behavioural canary: blocked data never reaches a model request, event, log or response | protect-adk-sensitive-data |
| LLM03 | Supply chain | as ASI04 plus pinned `google-adk` at or above the CVE floor | `adk_pins` status is `at_or_above_cve_floor`; hash test passes | adk-agent-security |
| LLM04 | Data and model poisoning | perimeter and store controls on retrieval corpora and memory | Provenance recorded on retrieved chunks; write path to the corpus is authenticated | adk-memory-architecture |
| LLM05 | Improper output handling | UI escaping and allowlists; before_tool validation of model-supplied arguments | Renderer test: image and script markup from model text is inert; link targets visible | adk-frontend-integration, adk-agent-security |
| LLM06 | Excessive agency | identity least privilege; tool tiering; confirmation as code | Inventory shows every write-tier tool gated; IAM denies writes for the reader identity | adk-agent-security, adk-operational-guardrails |
| LLM07 | System prompt leakage | no secrets or authorisation logic in instructions; `global_instruction` reviewed | Extraction case yields nothing that grants access | adk-agent-instructions |
| LLM08 | Vector and embedding weaknesses | retrieval scoped by identity and tenant; chunks as untrusted content | Cross-tenant retrieval test returns nothing; poisoned chunk case passes | adk-memory-architecture |
| LLM09 | Misinformation | truthful tool-derived status; grounded output checks | Receipt and status rendered from trusted tool output in tests | adk-model-and-output-contracts, adk-agent-evaluation |
| LLM10 | Unbounded consumption | invocation, token and tool-repeat limits; result size bounds | Budget tests from the guardrails skill pass | adk-operational-guardrails |

Companion identifiers for readers on other frameworks (ATLAS 2026.09 and the CoSAI Risk Map, cited by id; see the threat-model reference): LLM01 with `AML.T0051` and `riskPromptInjection`; LLM02 with `AML.T0083` and `AML.T0098`; LLM03 with `AML.T0110`, `riskToolSourceProvenance` and `riskToolRegistryTampering`; LLM04 and LLM08 with `AML.T0070`, `AML.T0080` and `riskRetrievalVectorStorePoisoning`; LLM06 with `AML.T0086`, `AML.T0101` and `riskRogueActions`; LLM10 with `AML.T0034.002`, `riskRunawayAgentToolLoops` and `controlAgentExecutionBounds`; LLM02 by cross-tenant retrieval with `riskSensitiveDataDisclosure` (ATLAS 2026.09 has no technique for the disclosure itself; cite `AML.T0064` Gather RAG-Indexed Targets when an attacker probes the index); LLM05 with `riskInsecureModelOutput`; LLM07 with `AML.T0084` Discover AI Agent Configuration and `AML.T0083`. Where no companion id fits, write "no listed ATLAS id" rather than stretching one. For an MCP boundary, MCP-focused reviewers also expect the OWASP MCP Top 10 ids (beta; cite by id with a link, copy no text): MCP01 beside LLM02 and ASI03; MCP02 beside LLM06 and ASI03; MCP03 beside LLM03, ASI04 and `AML.T0110`; MCP04 beside LLM03 and ASI04; MCP05 beside LLM05 and ASI05; MCP06 beside LLM01 and ASI01; MCP07 beside ASI03 and ASI07; MCP08 beside ASI10; MCP09 beside ASI04; MCP10 beside LLM02 and ASI06.

## Per-agent trifecta worksheet

Fill one per `LlmAgent` and one per workflow agent that chains children through
state. Start from the inspector's `agents[]` entry and confirm every row by
reading the tool body.

```
Agent: ______________________   Class: __________   File:line: ______________
Controlling human: ________________________   Trigger (user turn / event / peer): __________
Identity the tools run as: ___________________   Scopes or IAM bindings: ______________________

Private data reachable (tools, state, memory, artifacts):
  - ________________________________________________  tier: read
  - ________________________________________________  tier: read
Untrusted content reachable (retrieval, fetch, mail, MCP, peer output, memory):
  - ________________________________________________  fenced on this version? ___  provenance labelled? ___
  - ________________________________________________
Consequential actions (write / irreversible):
  - ________________________  tier: ______  gate: require_confirmation / before_tool / review / none
  - ________________________  tier: ______  gate: ______
Egress paths (send, fetch, webhook, URL built-ins, rendered links):
  - ________________________  destination allowlist? ___  taint check? ___

Trifecta: private [ ]  untrusted [ ]  egress [ ]   all three? [ ]
If all three: leg removed ______________________  or residual risk accepted by __________ on ________

Sub-agents: name / include_contents / mode / tools
  - ________________________________________________
Code executor: ______________  network: ______  bash policy: ______
Screening layers (recorded, not enforcement): ____________________________
Adversarial cases covering this agent: ______________________________________
```

## Review sign-off

| Item | Done |
| --- | --- |
| Inventory attached (before and after) | |
| Every trifecta agent has a removed leg or signed acceptance | |
| Every consequential action has a non-instruction enforcement point | |
| Every MCP server allowlisted, reviewed, hashed and namespaced | |
| Executor sandboxed; bash policy allowlisted | |
| Confirmation checklist satisfied for irreversible tools | |
| Renderer escapes and allowlists | |
| Adversarial suite passes offline with egress denied | |
| Denied attempts logged and alerted | |
| `google-adk` pin at or above 2.7.0, upgrade decision recorded | |

# Sources

Each entry carries its evidence label and the date it was read or supplied.
Entries marked "not re-fetched" were supplied by the coordinator's research on
2026-10-07 and should be confirmed before being quoted to an owner.

## ADK source and documentation (source-verified, documented behaviour)

- `google-adk` 2.8.0 source, tag v2.8.0, read 2026-10-07: `plugins/base_plugin.py`,
  `flows/llm_flows/functions.py`, `flows/llm_flows/_fencing.py`,
  `flows/llm_flows/agent_transfer.py`, `tools/function_tool.py`,
  `tools/base_toolset.py`, `tools/mcp_tool/mcp_toolset.py`,
  `tools/mcp_tool/mcp_tool.py`, `tools/mcp_tool/mcp_session_manager.py`,
  `tools/bash_tool.py`, `tools/tool_confirmation.py`, `agents/context.py`,
  `agents/llm_agent.py`, `agents/remote_a2a_agent.py`, `code_executors/*.py`,
  `evaluation/eval_metrics.py`, `evaluation/request_intercepter_plugin.py`.
- `adk-python` main at 2.11.0 and `CHANGELOG.md`, read 2026-10-07:
  `plugins/_tool_call_integrity_plugin.py`, `flows/llm_flows/context/_fencing.py`,
  `tools/mcp_tool/mcp_tool.py`, `a2a/agent/_remote_a2a_agent.py`.
- ADK docs, Safety and Security: https://adk.dev/safety/ (source
  `docs/safety/index.md`, read 2026-10-07). Agent-auth versus user-auth,
  in-tool guardrails from `ToolContext`, callbacks and plugins, sandboxed code
  execution ("sandboxing must be used to prevent model-generated code to
  compromise the local environment"), VPC-SC as a coarse control, "always
  escape model-generated content in UIs", vague instructions as a risk source.
- ADK docs, Plugins: https://adk.dev/plugins/ ; Tool confirmation:
  https://adk.dev/tools-custom/confirmation/ ; MCP tools:
  https://adk.dev/tools-custom/mcp-tools/ (tool_filter, read-only filters in
  production, header_provider, stdio for development); Code execution:
  https://adk.dev/integrations/code-execution/ and
  https://adk.dev/integrations/gke-code-executor/ ; Web interface:
  https://adk.dev/runtime/web-interface/ ("not meant for use in production
  deployments"); Evaluate: https://adk.dev/evaluate/ (read 2026-10-07).
- adk-samples `core/python/safety-plugins/AGENTS.md` (LlmAsAJudge and Model
  Armor plugins, planted poisoned tool result demonstration) and
  `long-horizon-harness/docs/security-model.md` (hard-deny guards before
  soft-ask approval, headless "ask as deny", hermetic network). Vendor
  samples; supplied by research, not re-fetched.

## Google frameworks and GCP (vendor guidance)

- Díaz, Olive, "An Introduction to Google's Approach for Secure AI Agents",
  2025. https://research.google/pubs/an-introduction-to-googles-approach-for-secure-ai-agents/
  and PDF https://storage.googleapis.com/gweb-research2023-media/pubtools/1018686.pdf
  (well-defined human controllers, carefully limited powers, observable
  actions and planning; hybrid deterministic runtime policy plus
  reasoning-based defences). Read 2026-10-07.
- Google Cloud blog, "Agent Factory recap: securing AI agents in production",
  2025-10-24. https://cloud.google.com/blog/topics/developers-practitioners/agent-factory-recap-securing-ai-agents-in-production
  (Model Armor pre-inference, gVisor and ephemeral Cloud Run with IAM least
  privilege, Private Google Access and VPC-SC, logging of failed attempts as
  the attack signal, ADK callbacks; authenticate agents to each other).
  Supplied by research, not re-fetched.
- Agent Identity: https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/agent-identity
  (lifecycle-bound principal, certificate-bound tokens, new principal per
  redeploy; IAM conditions scoped to one dataset). Supplied by research.
- Model Armor overview: https://docs.cloud.google.com/model-armor/overview
  (prompt injection and jailbreak, responsible AI, SDP, malicious URL filters;
  stateless per message; floor settings). Read 2026-10-07. Configuration
  belongs to `protect-adk-sensitive-data`.
- Vertex Gen AI Evaluation metric templates:
  https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/metrics-templates
  ("Safety" and "Multi-turn Safety" measure harmlessness, not injection
  resistance or forbidden tool calls). Read 2026-10-07.

## Independent evidence (peer-reviewed or benchmark)

- Debenedetti et al., "Defeating Prompt Injections by Design" (CaMeL), Google
  DeepMind et al., arXiv 2503.18813, v1 2025-03, v2 2025-06. Privileged and
  quarantined LLM split, capability tags enforced at tool call; 77% versus 84%
  task success on AgentDojo with provable security. Not re-fetched.
- Beurer-Kellner et al., "Design Patterns for Securing LLM Agents against
  Prompt Injections", arXiv 2506.08837, June 2025. Action-selector,
  plan-then-execute, map-reduce, dual LLM, code-then-execute,
  context-minimisation; principle that an agent which has ingested untrusted
  input must not take consequential actions. Not re-fetched.
- Debenedetti et al., "AgentDojo", arXiv 2406.13352, NeurIPS 2024 Datasets and
  Benchmarks. Not re-fetched.

## Community taxonomies and practitioner analyses (community report)

- OWASP Top 10 for LLM Applications 2025: https://genai.owasp.org/llm-top-10/
  (LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM03
  Supply Chain, LLM05 Improper Output Handling, LLM06 Excessive Agency, LLM07
  System Prompt Leakage, LLM08 Vector and Embedding Weaknesses, LLM10 Unbounded
  Consumption). Read 2026-10-07.
- OWASP Top 10 for Agentic Applications 2026, published 2025-12-09:
  https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
  (ASI01 Goal Hijack, ASI02 Tool Misuse, ASI03 Identity and Privilege Abuse,
  ASI04 Agentic Supply Chain, ASI05 Unexpected Code Execution, ASI06 Memory
  and Context Poisoning, ASI07 Insecure Inter-Agent Communication, ASI08
  Cascading Failures, ASI09 Human-Agent Trust Exploitation, ASI10 Rogue
  Agents). List taken from secondary summaries; verify titles against the
  published document.
- Simon Willison, "The lethal trifecta for AI agents", 2025-06-16.
  https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ ("95% detection
  is a failing grade"). Read 2026-10-07.
- Invariant Labs, "MCP Security Notification: Tool Poisoning Attacks",
  2025-04-01. https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks
  and "WhatsApp MCP Exploited", https://invariantlabs.ai/blog/whatsapp-mcp-exploited
  (cross-server shadowing). Read 2026-10-07.
- Model Context Protocol, Security Best Practices, revision 2025-11-25.
  https://modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices
  (token passthrough MUST NOT, confused deputy and per-client consent, SSRF
  guards, session IDs bound to user, scope minimisation; annotations are
  hints). Documented behaviour. Read 2026-10-07.
- Pillar Security disclosure, reported 2026-08-04:
  https://thehackernews.com/2026/08/google-deletes-3-adk-ai-workflows-after.html
  (public issue-triage agent injected to trigger a privileged fix agent
  holding a PAT, API key and service-account credential; three workflows
  deleted). Supplied by research, not re-fetched.
- CVE-2026-4810 https://osv.dev/vulnerability/CVE-2026-4810 (adk web, 1.7.0 to
  1.28.0, fixed 1.28.1, published 2026-04-13); CVE-2026-79696
  https://www.mend.io/vulnerability-database/CVE-2026-79696/ (adk web RCE via
  crafted test-session replay, 2.0.0 to 2.6.0, fixed 2.7.0, published
  2026-09-09); CVE-2026-79707 (builder endpoint path traversal, 1.9.0 to
  1.21.0); CVE-2026-18236 (forged `adk_request_confirmation` response, fixed
  2.5.0 and 2.6.0). Supplied by research; CHANGELOG entries for the fixes were
  verified locally.
- google/adk-python issues #6461, #7148, #7010, #7076, #6828, #7311, #5112,
  #7103, #6964, #7369. Supplied by research, not re-fetched.

## Cross-vendor confirmation and tooling (vendor guidance)

- Anthropic, "Piloting Claude for Chrome", 2025-08-25.
  https://claude.com/blog/claude-for-chrome (123 cases, 29 injection
  scenarios, 23.6% attack success without mitigations; vendor-measured). Read
  2026-10-07.
- OpenAI Agents SDK guardrails: https://openai.github.io/openai-agents-python/guardrails/
  (input, output and tool guardrails as code around the model). Read
  2026-10-07.
- promptfoo: ADK guide https://promptfoo.dev/docs/guides/evaluate-google-adk
  (in-process Python provider, `trajectory:tool-used`, `tool-args-match`,
  `tool-sequence` assertions; updated 2026-10-06) and red-team plugins
  https://promptfoo.dev/docs/red-team/plugins/indirect-prompt-injection .
  NVIDIA garak (model endpoints) and Microsoft PyRIT (orchestrated attack
  generation). Read 2026-10-07.

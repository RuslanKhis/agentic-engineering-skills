# Situation: release-coding-agent-capability-diff-gate

Overlay on support-assistant:
- `app/agent.py`: root LlmAgent with `FunctionTool(refund_order, require_confirmation=True)`,
  `before_tool_callback=capability_check`, one `McpToolset` with `tool_filter`, two sub-agents
  (returns_agent, mail_agent) and a new `Workflow`-based `reporting_agent` (app/reporting.py)
  whose function nodes read refunds and email them (A4: function nodes not read by either tool;
  need hand review).
- `.github/workflows/ci.yml` runs unit tests only.
- `mcp/catalogue-tools.json`: committed MCP definition record (A5: keep the MCP pin check
  separate from the binding diff).
- `docs/notes/pr-gate-proposal.md`: the agents-shipgate suggestion (A1-A3 are about the
  tool's exit code, what it does not compare, and inspect_security_surface.py --compare).
The agent has no shell, so the inspector and shipgate cannot be run; graded on the gate design.
Context unchanged.

# Situation: interoperability-expose-and-register-a2a

Standalone project:
- pyproject: google-adk 2.8.0, a2a-sdk >=0.3.4,<0.4 (A2: A2A 0.3 card and streaming constraint).
- `research_agent/agent.py`: root with two `mode="single_turn"` sub-agents; one holds
  `FunctionTool(submit_procurement_request, require_confirmation=True)` (A3: inbound peer messages
  are data, not user authority; approval-over-A2A gap to adk-agent-security).
- `docs/hosting-plan.md`: Cloud Run private ingress, same project as Gemini Enterprise
  (A2 registration constraints, A4 deployment left to the deploy skill, approvals listed).
- No agent card exists yet (A1: to_a2a / api_server a2a, card with required fields and no
  instructions, validate with agent_card_check.py — the agent has no shell; graded on whether
  it validates by reading or proposes the command).
Context unchanged.

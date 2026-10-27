Coding agents now open most PRs on our ADK support agent. Add a CI check that blocks a PR which changes what the production agent can do unless a human approves it. Someone suggested agents-shipgate diff --application; is that enough?

---
Situation (from the person asking): google-adk 2.12.0; root LlmAgent with FunctionTool(refund_order, require_confirmation=True), a before_tool_callback capability check, one McpToolset with tool_filter, two sub-agents, and a new Workflow-based reporting agent; GitHub Actions; no network in the session.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.
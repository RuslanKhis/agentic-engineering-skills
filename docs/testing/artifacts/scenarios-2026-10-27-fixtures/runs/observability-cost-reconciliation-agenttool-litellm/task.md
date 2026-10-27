Our ADK cost dashboard and invocation_summary.py say a research turn costs far less than the invoice, yet output tokens look higher than the provider reports. What is wrong and which cost tests should we add?

---
Situation (from the person asking): google-adk 2.12.0 root LlmAgent with two AgentTool sub-agents; models via LiteLlm to an OpenAI-style reasoning model; HttpOptions retry_options attempts=2; cost computed from saved parent sessions; no network in the session.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.
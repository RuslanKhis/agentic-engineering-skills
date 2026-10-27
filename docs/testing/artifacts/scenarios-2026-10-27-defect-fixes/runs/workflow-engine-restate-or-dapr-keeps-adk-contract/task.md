We want our ADK refund agent to survive worker crashes and wait days for a manager. Ops prefers Restate or our existing Dapr on GKE over Temporal. Pick one, wire it, and tell us what to test before we trust it.

---
Situation (from the person asking): ADK 2.12 App: SequentialAgent(intake LlmAgent, refund LlmAgent); before_model and after_model callbacks enforce a token budget; RunConfig max_llm_calls=8; refund tool uses FunctionTool(require_confirmation=True) and a payments API with idempotency keys; state templating {user:tier} in the instruction; company of 4,000 staff; no network in the session.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.
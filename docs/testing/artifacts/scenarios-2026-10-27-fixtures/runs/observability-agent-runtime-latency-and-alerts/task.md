Our Agent Runtime agent's p95 doubled. Instrument it so we can attribute time to model, tools and session loading, define an SLO, and alert on it. Keep prompts out of the traces.

---
Situation (from the person asking): ADK 2.8.0 agent deployed with adk deploy agent_engine; no telemetry flags set; a saved session export with usage metadata is available; Cloud project has Cloud Trace but the Telemetry API is not enabled.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.
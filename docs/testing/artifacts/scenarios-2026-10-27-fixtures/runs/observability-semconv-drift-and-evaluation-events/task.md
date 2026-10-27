We send traces to a third-party OTLP backend. Are our dashboards still using the right GenAI attribute names? I'd like something that warns us when ADK's telemetry stops matching the standard, and I want our nightly judge scores to show up on the traces, not just in BigQuery.

---
Situation (from the person asking): An ADK 2.11 agent exporting OTLP to a third-party backend, dashboards keyed on gen_ai.system, a nightly judge writing scores to BigQuery. No network or credentials in the session.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.
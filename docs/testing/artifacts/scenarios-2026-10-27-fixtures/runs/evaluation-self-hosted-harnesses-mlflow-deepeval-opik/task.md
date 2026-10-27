Compliance says no agent data may leave our GCP project. Data science wants deepeval's ADK integration for agent metrics, MLflow's Google ADK scorers for nightly scoring and Opik for traces. Tell us what we can use, how to configure it, and how the nightly job should record MLflow's results.

---
Situation (from the person asking): An ADK 2.12 agent with content capture off in production, no Confident AI or Comet account, Vertex AI under a service account, no model calls allowed in this session.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.
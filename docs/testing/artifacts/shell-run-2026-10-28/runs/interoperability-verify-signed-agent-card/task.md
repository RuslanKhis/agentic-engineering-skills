A partner now signs the A2A agent card our ADK orchestrator calls by URL. Make our side refuse the card unless the signature checks out, and tell me what our card checker should flag.

---
Situation (from the person asking): ADK 2.12.0 with a2a-sdk 1.2.3 pinned; RemoteA2aAgent(agent_card='https://partner.example/.well-known/agent-card.json'); the partner shared its JWKS URL and key ids out of band; no cloud credentials and no network in the session.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.
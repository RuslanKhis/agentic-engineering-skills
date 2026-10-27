Expose our ADK triage agent over A2A for a partner team and write the acceptance checks for the card, versioning and authentication before we register it anywhere.

---
Situation (from the person asking): An ADK 2.12 project with a2a-sdk 1.x pinned, one root agent, to_a2a available, a partner that will call with an OAuth client-credentials token, no cloud credentials and no network in the session.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.
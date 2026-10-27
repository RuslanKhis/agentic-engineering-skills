We want assistant-ui instead of CopilotKit for our Python ADK support agent, with approvals for refunds and an edit button on user messages. Wire it up.

---
Situation (from the person asking): google-adk 2.12.0 FastAPI app with IAP-verified principal; refund tool uses require_confirmation; Vite React SPA; candidate @assistant-ui/react-google-adk 0.0.40. Offline; nothing installed.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.
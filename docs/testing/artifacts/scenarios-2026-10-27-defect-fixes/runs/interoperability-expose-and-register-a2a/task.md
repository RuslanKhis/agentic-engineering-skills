Expose our ADK research agent so Gemini Enterprise users can invoke it, with an agent card and authentication, and make sure a poisoned reply from the remote peer cannot approve anything on our side.

---
Situation (from the person asking): ADK 2.8.0 project with a2a-sdk 0.3.x pinned, a root agent with two single_turn sub-agents, planned hosting on Cloud Run. No cloud credentials available.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.
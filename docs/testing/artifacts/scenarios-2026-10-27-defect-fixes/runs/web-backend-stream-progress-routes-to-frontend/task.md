Show each tool call as a line in the chat while the agent runs, and keep the partial answer if the run fails halfway.

---
Situation (from the person asking): An ADK web app with a FastAPI backend and a Vite React SPA themed from docs/design/DESIGN.md; the agent route returns JSON today.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.
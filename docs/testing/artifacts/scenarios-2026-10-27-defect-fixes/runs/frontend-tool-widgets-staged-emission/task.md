Our shopping agent's A2UI widgets misbehave: two tools that stage the same widget id show the cards twice, a refresh callback that re-renders after a preference change reaches the browser as nothing, and 'show me those again' re-runs the search. Fix the widget pipeline; keep the tools' names and result shapes; offline tests only.

---
Situation (from the person asking): An ADK agent whose three tools each call render_ui_widget inline and an after_agent_callback that renders without writing state. google-adk not installed; no network.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.
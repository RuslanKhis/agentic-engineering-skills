Every so often the model rejects a request because our custom summariser plugin left a function call without its result. And nobody here can tell me when compaction actually runs. Can you fix the plugin and pin that down?

---
Situation (from the person asking): An ADK 2.12 agent with App-level compaction plus a custom trimming plugin, a Postgres session store, no model access in the session.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.
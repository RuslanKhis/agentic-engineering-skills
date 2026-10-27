Our extraction agent has output_schema plus two tools and sometimes returns prose or fenced JSON; output_key then raises. Make it reliable and prove which path the model uses.

---
Situation (from the person asking): ADK 2.8.0 project using the API-key backend with gemini-3.5-flash, a Pydantic output_schema of twelve fields with nested optionals, and no request capture in tests.

Run conditions: this is a non-interactive session and nobody will answer questions. Where you would ask the user something, write the question down, state the assumption you proceed on, and carry on. Work only inside the current directory; do not install packages, make network requests or touch cloud resources. End with a short summary of what you did and what you left undone.